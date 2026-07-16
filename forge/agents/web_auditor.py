"""Bounded static checks for JavaScript and TypeScript source.

This is intentionally not a JavaScript parser. It scans executable-looking
source lines for a small set of high-signal boundaries and reports CODE FACTs;
it never claims exploitability without a language-specific induction harness.
"""
from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

from forge.detector.stack import discover_files, is_excluded_by_policy
from forge.models import AgentScanResult
from forge.agent_protocol import mandatory_protocol


WEB_EXTENSIONS = {".js", ".jsx", ".ts", ".tsx"}


@dataclass(frozen=True)
class WebFinding:
    family: str
    path: str
    line: int
    description: str


_PATTERNS = (
    ("dynamic-evaluation", re.compile(r"\beval\s*\(|\bnew\s+Function\s*\("), "dynamic code evaluation crosses a data-to-code boundary"),
    ("subprocess", re.compile(r"\bchild_process\.(?:exec|execSync|spawn|spawnSync)\s*\("), "child_process execution call requires an explicit command boundary"),
)


def _has_nearby_try(lines: list[str], line_number: int, radius: int = 8) -> bool:
    start = max(0, line_number - radius - 1)
    end = min(len(lines), line_number + radius)
    return any(re.search(r"\btry\s*\{", line) for line in lines[start:end])


def _mask_string_literals(line: str) -> str:
    """Preserve line shape while removing quoted data in linear time.

    A regex with a repeated negative lookahead can catastrophically backtrack
    on minified input or an unterminated template literal. This scanner has a
    strict O(n) bound and masks the remainder of an unterminated literal.
    """
    chars = list(line)
    quote: str | None = None
    escaped = False
    for index, char in enumerate(line):
        if quote is None:
            if char in {"'", '"', "`"}:
                quote = char
                chars[index] = " "
            continue
        chars[index] = " "
        if escaped:
            escaped = False
        elif char == "\\":
            escaped = True
        elif char == quote:
            quote = None
    return "".join(chars)


def audit(root: str | Path, eligible: set[str] | None = None) -> tuple[AgentScanResult, tuple[str, ...]]:
    base = Path(root)
    findings: list[WebFinding] = []
    examinations: dict[str, str] = {}
    analyzed: list[str] = []
    for path in discover_files(base, include_excluded=True):
        rel = str(path.relative_to(base))
        if is_excluded_by_policy(path, base):
            examinations[rel] = "excluded_by_policy"
            continue
        if eligible is not None and rel not in eligible:
            examinations[rel] = "excluded_by_scope"
            continue
        if path.suffix.lower() not in WEB_EXTENSIONS:
            examinations[rel] = "excluded_by_scope"
            continue
        try:
            source = path.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            examinations[rel] = "excluded_by_scope"
            continue
        analyzed.append(rel)
        lines = source.splitlines()
        sanitized_names = {
            match.group(1)
            for match in re.finditer(r"\b(\w+)\s*=.*?\.replace\s*\(", source)
            if re.search(r"\[\^|separator|slash|path|name|slug", match.group(0), re.I)
        }
        # Carry the evidence through simple filename assignments such as
        # ``filename = f"{slug}_{timestamp}.json"``.  A sanitizer on ``slug``
        # is still relevant when that value is the only user-derived part of
        # the final path component.
        changed = True
        while changed:
            changed = False
            for match in re.finditer(r"\b(\w+)\s*=([^\n;]+)", source):
                target, expression = match.group(1), match.group(2)
                if target not in sanitized_names and any(re.search(rf"\b{re.escape(name)}\b", expression) for name in sanitized_names):
                    sanitized_names.add(target)
                    changed = True
        local: list[WebFinding] = []
        for number, line in enumerate(lines, 1):
            stripped = line.strip()
            if not stripped or stripped.startswith(("//", "/*", "*")):
                continue
            code_line = _mask_string_literals(line)
            for family, pattern, description in _PATTERNS:
                if pattern.search(code_line):
                    local.append(WebFinding(family, rel, number, description))
            if re.search(r"\bJSON\.parse\s*\(", code_line) and not _has_nearby_try(lines, number):
                local.append(WebFinding("parser-boundary", rel, number, "JSON.parse call has no nearby visible try/catch boundary"))
            if re.search(r"\b(?:readFile|readFileSync|writeFile|writeFileSync|unlink|rm)\s*\(", code_line):
                names = set(re.findall(r"\b(?:user|request|input|path|file|name)\w*\b", code_line, re.I))
                if names - sanitized_names and not re.search(r"\b(?:resolve|normalize|basename)\s*\(", code_line):
                    local.append(WebFinding("path-traversal", rel, number, "filesystem path reaches a file operation without visible normalization"))
        findings.extend(local)
        examinations[rel] = "examined_with_findings" if local else "examined_clean"
    protocol = mandatory_protocol(
        "web_auditor",
        tuple(f"{item.family} observed at {item.path}:{item.line}" for item in findings),
        analyzed,
    )
    return AgentScanResult(tuple(findings), examinations, protocol), tuple(sorted(analyzed))


__all__ = ("WEB_EXTENSIONS", "WebFinding", "audit")
