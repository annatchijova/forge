"""Module 3: adversarial verification of abductive hypotheses."""
from __future__ import annotations
import ast, json, time
from pathlib import Path
from forge.models import Evidence, Finding, HypothesesManifest, VerificationManifest

def _subprocess_enclosure(tree: ast.AST, target_line: int) -> bool:
    parents = {}
    for parent in ast.walk(tree):
        for child in ast.iter_child_nodes(parent):
            parents[child] = parent
    node = next((n for n in ast.walk(tree) if isinstance(n, ast.Call) and getattr(n, "lineno", -1) == target_line), None)
    while node in parents:
        node = parents[node]
        if isinstance(node, ast.Try):
            return True
    return False

def _call_at(tree: ast.AST, line: int):
    return next((n for n in ast.walk(tree) if isinstance(n, ast.Call) and getattr(n, "lineno", -1) == line), None)

def _ancestors(tree: ast.AST, node: ast.AST):
    parents = {}
    for parent in ast.walk(tree):
        for child in ast.iter_child_nodes(parent): parents[child] = parent
    out = []
    while node in parents:
        node = parents[node]; out.append(node)
    return out

def _named_handler(tree: ast.AST, call: ast.AST, names: tuple[str, ...]) -> bool:
    for parent in _ancestors(tree, call):
        if isinstance(parent, ast.Try):
            for handler in parent.handlers:
                for typ in ([handler.type] if handler.type else []):
                    text = ast.unparse(typ)
                    if any(name in text for name in names): return True
    return False

def _parser_benign(tree: ast.AST, line: int) -> bool:
    call = _call_at(tree, line)
    return bool(call and _named_handler(tree, call, ("JSONDecodeError", "ValueError", "YAMLError", "TomlDecodeError")))

def _eval_benign(tree: ast.AST, line: int) -> bool:
    call = _call_at(tree, line)
    return bool(call and call.args and isinstance(call.args[0], ast.Constant) and isinstance(call.args[0].value, str))

def _float_benign(tree: ast.AST, line: int, source: str) -> bool:
    call = _call_at(tree, line)
    if call and isinstance(call.func, ast.Attribute) and call.func.attr == "isclose":
        return len(call.args) >= 2 and any(k in {kw.arg for kw in call.keywords} for k in ("rel_tol", "abs_tol"))
    node = next((n for n in ast.walk(tree) if isinstance(n, ast.Compare) and getattr(n, "lineno", -1) == line), None)
    if not node: return False
    text = ast.unparse(node)
    return "Decimal(" in text or "Fraction(" in text

def verify_hypotheses(manifest: HypothesesManifest) -> VerificationManifest:
    findings, discarded = [], []
    root = Path(manifest.root)
    verified = ("subprocess", "parser", "float comparison", "eval/exec")
    for h in manifest.hypotheses:
        path = root / h.module_path
        source = path.read_text(encoding="utf-8", errors="replace")
        line = h.file_lines[0]
        evidence = (Evidence("source", f"{h.module_path}:{line}", source.splitlines()[line - 1].strip()),)
        if path.suffix == ".py":
            try:
                tree = ast.parse(source, filename=str(path))
            except SyntaxError as exc:
                discarded.append({"module_path": h.module_path, "reason": f"AST parse failed: {exc}"})
                continue
            benign = False
            reason = ""
            if "subprocess" in h.description:
                benign = _subprocess_enclosure(tree, line) and _named_handler(tree, _call_at(tree, line), ("SubprocessError", "OSError"))
                reason = "AST proves explicit subprocess exception enclosure."
            elif "parser call" in h.description:
                benign = _parser_benign(tree, line); reason = "AST proves known parser exception handler."
            elif "dynamic evaluation" in h.description.lower():
                benign = _eval_benign(tree, line); reason = "AST proves literal string argument."
            elif "float threshold" in h.description or "tolerance call" in h.description:
                benign = _float_benign(tree, line, source); reason = "AST proves exact-type operands or explicit tolerance."
            if benign:
                discarded.append({"module_path": h.module_path, "reason": reason}); continue
        findings.append(Finding("INFERRED", "PLAUSIBLE HYPOTHESIS", h.module_path, h.description, evidence, "Observed construct matches; no induction was run, so level is capped at PLAUSIBLE HYPOTHESIS."))
    return VerificationManifest("1.0", "0.1.0", manifest.schema_version, manifest.root, int(time.time()), tuple(findings), tuple(discarded), verified, ())

def write_verification_manifest(manifest: VerificationManifest, destination: str | Path) -> None:
    Path(destination).write_text(json.dumps(manifest.to_dict(), sort_keys=True, indent=2) + "\n", encoding="utf-8")
