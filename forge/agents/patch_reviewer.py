"""Optional surgical patch review; deliberately not part of repository scans."""
from __future__ import annotations
import ast, re
from dataclasses import dataclass

@dataclass(frozen=True)
class PatchReview:
    changed_lines: int; touched_scopes: tuple[str, ...]; ratio: float; flags: tuple[str, ...]

def review(unified_diff: str, intent: str, before: str = "", after: str = "") -> PatchReview:
    lines = unified_diff.splitlines()
    changed = [l for l in lines if (l.startswith("+") or l.startswith("-")) and not l.startswith(("+++","---"))]
    new_lines = []
    cursor = 0
    for line in lines:
        m = re.match(r"@@ -\d+(?:,\d+)? \+(\d+)(?:,\d+)? @@", line)
        if m: cursor = int(m.group(1)); continue
        if line.startswith("+") and not line.startswith("+++"): new_lines.append(cursor); cursor += 1
        elif line.startswith("-") and not line.startswith("---"): pass
        elif line.startswith(" "): cursor += 1
    tree = ast.parse(after or before or "")
    scopes=[]
    scope_sizes=[]
    for n in ast.walk(tree):
        if isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef,ast.ClassDef)):
            end = getattr(n, "end_lineno", n.lineno)
            touched = any(n.lineno <= line <= end for line in new_lines)
            if touched: scopes.append(n.name); scope_sizes.append(max(1, end - n.lineno + 1))
    ratio = len(changed) / max(sum(scope_sizes), 1)
    intent_word = intent.split()[0] if intent.split() else ""
    flags = ()
    if intent_word and not any(re.search(re.escape(intent_word), s, re.I) for s in scopes):
        flags = ("changed lines do not match stated intent",)
    if new_lines and not scopes: flags += ("changed lines fall outside any function or class",)
    return PatchReview(len(changed), tuple(scopes), ratio, flags)
