"""Module 2: abductive, read-before-reason hypothesis generation."""
from __future__ import annotations

import json
import io
import re
import time
import tokenize
from pathlib import Path

from forge.models import HypothesesManifest, Hypothesis, ModuleClass, TriageManifest


def _lines(path: Path) -> tuple[str, ...]:
    # Reading the actual source is a hard precondition for generation.
    return tuple(path.read_text(encoding="utf-8", errors="replace").splitlines())


def _code_before_comment(line: str) -> str:
    """Return code before an inline comment, preserving '#' inside strings."""
    quote = None
    escaped = False
    for index, char in enumerate(line):
        if escaped:
            escaped = False
        elif char == "\\" and quote:
            escaped = True
        elif char in {"'", '"'}:
            quote = None if quote == char else char if quote is None else quote
        elif char == "#" and quote is None:
            return line[:index]
    return line


def _mask_string_literals(source: tuple[str, ...]) -> tuple[str, ...]:
    """Return source with string-token contents blanked for regex matching.

    Candidate detection is line-oriented, but a plain regex must not mistake a
    risk-shaped phrase inside a literal for executable code. Tokenization keeps
    the original line/column layout while making that distinction explicit.
    If an incomplete synthetic fragment cannot be tokenized, the original
    lines are returned and the AST verifier remains the safety boundary.
    """
    text = "".join(line if line.endswith("\n") else line + "\n" for line in source)
    chars = list(text)
    try:
        tokens = tokenize.generate_tokens(io.StringIO(text).readline)
        for token in tokens:
            if token.type != tokenize.STRING:
                continue
            (start_line, start_col), (end_line, end_col) = token.start, token.end
            for line_number in range(start_line, end_line + 1):
                begin = start_col if line_number == start_line else 0
                end = end_col if line_number == end_line else len(text.splitlines(keepends=True)[line_number - 1])
                offset = sum(len(row) for row in text.splitlines(keepends=True)[:line_number - 1])
                for index in range(offset + begin, min(offset + end, len(chars))):
                    if chars[index] not in {"\n", "\r"}:
                        chars[index] = " "
    except (tokenize.TokenError, IndentationError):
        return source
    return tuple("".join(chars).splitlines())


def _candidates(module_path: str, source: tuple[str, ...], language: str) -> list[Hypothesis]:
    candidates: list[tuple[str, int, str]] = []
    matching_source = _mask_string_literals(source)
    for number, (line, matching_line) in enumerate(zip(source, matching_source), 1):
        stripped = _code_before_comment(line).strip()
        matching_stripped = _code_before_comment(matching_line).strip()
        # Ignore comments and strings that merely mention a risk word.
        if not stripped or stripped.startswith("#"):
            continue
        if re.search(r"\b(subprocess\.(?:run|Popen|call|check_call|check_output)|os\.system)\s*\(", matching_stripped):
            if re.search(r"\bshell\s*=\s*True\b", matching_stripped):
                candidates.append((f"The subprocess call `{stripped}` at {module_path}:{number} enables shell=True, so command data may cross a shell interpretation boundary.", number, "Invoke the call with a harmless metacharacter fixture in the isolated harness; a named rejection without shell expansion falsifies the hypothesis."))
                continue
            if not any("try:" in source[i] for i in range(max(0, number - 4), number)):
                candidates.append((f"The dynamic command invocation `{stripped}` at {module_path}:{number} may pass attacker-controlled arguments without an enclosing failure boundary.", number, f"Invoke this call with a harmless invalid executable and a shell metacharacter fixture; an explicit exception path with no command execution falsifies the hypothesis."))
        if re.search(r"\b(?:json|yaml|toml)\.loads?\s*\(|\bparse\s*\(", matching_stripped):
            if not any("except" in source[i] for i in range(number, min(len(source), number + 5))):
                candidates.append((f"The parser call `{stripped}` at {module_path}:{number} has no nearby exception handling, so malformed input may escape as an opaque failure.", number, f"Feed malformed input to the function containing line {number}; a named boundary error or explicit rejection falsifies the hypothesis."))
        if re.search(r"\b(?:score|verdict|classif\w*)\b.*(?:[<>]=?|==).*\d+\.\d+", matching_stripped):
            candidates.append((f"The decision comparison `{stripped}` at {module_path}:{number} uses a binary float threshold, so rounding at the boundary may flip the result.", number, f"Run inputs immediately below, exactly at, and above the threshold using exact decimal values; stable, documented boundary behavior falsifies the hypothesis."))
        if re.search(r"\bmath\.isclose\s*\(", matching_stripped):
            candidates.append((f"The tolerance call `{stripped}` at {module_path}:{number} governs a float decision and must expose an explicit tolerance policy.", number, f"Vary values within and outside the stated tolerance; a documented, stable boundary falsifies this hypothesis."))
        if re.search(r"\b(eval|exec)\s*\(", matching_stripped):
            candidates.append((f"The dynamic evaluation `{stripped}` at {module_path}:{number} may execute data as code instead of treating it as data.", number, f"Supply a payload that would create a harmless sentinel file; absence of the sentinel and explicit rejection falsify the hypothesis."))
    hypotheses = [Hypothesis(module_path, rank, desc, (line,), test) for rank, (desc, line, test) in enumerate(candidates[:5], 1)]
    omitted = len(candidates) - len(hypotheses)
    return hypotheses, omitted


def generate_hypotheses(triage: TriageManifest) -> HypothesesManifest:
    hypotheses: list[Hypothesis] = []
    audited: list[str] = []
    limitations: list[str] = ["Hypotheses require module 3 verification; parser candidates may receive isolated induction, while unsupported families remain AST-only."]
    root = Path(triage.root)
    for module in sorted(triage.modules, key=lambda m: (m.module_class != ModuleClass.CONNECTED_ALIVE, m.path)):
        if module.module_class is not ModuleClass.CONNECTED_ALIVE:
            continue
        path = root / module.path
        source = _lines(path)
        audited.append(module.path)
        module_hypotheses, omitted = _candidates(module.path, source, module.language)
        hypotheses.extend(module_hypotheses)
        if omitted:
            limitations.append(
                f"{module.path}: {omitted} additional risk pattern(s) beyond the 5-candidate "
                "cap were detected but omitted from this report; this is a completeness "
                "limitation, not evidence those patterns were absent."
            )
    return HypothesesManifest("1.0", "0.1.0", triage.schema_version, triage.root, int(time.time()), tuple(hypotheses), tuple(audited), tuple(limitations))


def write_hypotheses_manifest(manifest: HypothesesManifest, destination: str | Path) -> None:
    Path(destination).write_text(json.dumps(manifest.to_dict(), sort_keys=True, indent=2) + "\n", encoding="utf-8")
