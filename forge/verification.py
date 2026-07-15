"""Module 3: adversarial verification of abductive hypotheses."""
from __future__ import annotations
import ast, json, time
import re
from pathlib import Path
from forge.models import Evidence, Finding, HypothesesManifest, VerificationManifest

def _call_name(call: ast.Call) -> str:
    return ast.unparse(call.func)

def _call_at(tree: ast.AST, line: int, function_name: str | None = None):
    calls = (n for n in ast.walk(tree) if isinstance(n, ast.Call) and getattr(n, "lineno", -1) == line)
    if function_name is None:
        # Known limitation: unmatched hypothesis descriptions fall back to the
        # first AST call on the line, which is arbitrary when calls are nested.
        return next(calls, None)
    return next((c for c in calls if _call_name(c) == function_name), None)

def _subprocess_enclosure(tree: ast.AST, target_line: int, function_name: str | None = None) -> bool:
    parents = {}
    for parent in ast.walk(tree):
        for child in ast.iter_child_nodes(parent):
            parents[child] = parent
    node = _call_at(tree, target_line, function_name)
    while node in parents:
        node = parents[node]
        if isinstance(node, ast.Try):
            return True
    return False

def _description_call_name(description: str) -> str | None:
    match = re.search(r"`([A-Za-z_]\w*(?:\.[A-Za-z_]\w*)*)\s*\(", description)
    return match.group(1) if match else None

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

def _parser_benign(tree: ast.AST, line: int, function_name: str | None = None,
                   handler_names: tuple[str, ...] = ("JSONDecodeError", "ValueError", "YAMLError", "TomlDecodeError")) -> bool:
    call = _call_at(tree, line, function_name)
    return bool(call and _named_handler(tree, call, handler_names))

_DANGEROUS_EVAL_CONTENT = re.compile(
    r"\b(os\.system|os\.popen|os\.exec\w*|os\.remove|os\.unlink|subprocess\.\w+|"
    r"shutil\.rmtree|__import__|\beval\s*\(|\bexec\s*\()"
)

def _eval_benign(tree: ast.AST, line: int, function_name: str | None = None) -> bool:
    call = _call_at(tree, line, function_name)
    if not (call and call.args and isinstance(call.args[0], ast.Constant) and isinstance(call.args[0].value, str)):
        return False
    # A literal argument only proves the *provenance* is fixed at read time; it
    # does not prove the literal's own content is safe to execute. A literal
    # that itself invokes OS-level execution is a finding regardless of
    # provenance, so it must not be discarded by the literal-argument carve-out.
    return not _DANGEROUS_EVAL_CONTENT.search(call.args[0].value)

def _float_benign(tree: ast.AST, line: int, source: str, function_name: str | None = None) -> bool:
    call = _call_at(tree, line, function_name)
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
            call_name = _description_call_name(h.description)
            if "subprocess" in h.description:
                benign = _subprocess_enclosure(tree, line, call_name) and _named_handler(tree, _call_at(tree, line, call_name), ("SubprocessError", "OSError"))
                reason = "AST proves explicit subprocess exception enclosure."
            elif "parser call" in h.description:
                benign = _parser_benign(tree, line, call_name, ("JSONDecodeError", "ValueError", "ForgeArtifactError")); reason = "AST proves known parser exception handler."
            elif "dynamic evaluation" in h.description.lower():
                benign = _eval_benign(tree, line, call_name); reason = "AST proves literal string argument."
            elif "float threshold" in h.description or "tolerance call" in h.description:
                benign = _float_benign(tree, line, source, call_name); reason = "AST proves exact-type operands or explicit tolerance."
            if benign:
                discarded.append({"module_path": h.module_path, "reason": reason}); continue
        findings.append(Finding("INFERRED", "PLAUSIBLE HYPOTHESIS", h.module_path, h.description, evidence, "Observed construct matches; no induction was run, so level is capped at PLAUSIBLE HYPOTHESIS."))
    return VerificationManifest("1.0", "0.1.0", manifest.schema_version, manifest.root, int(time.time()), tuple(findings), tuple(discarded), verified, ())

def write_verification_manifest(manifest: VerificationManifest, destination: str | Path) -> None:
    Path(destination).write_text(json.dumps(manifest.to_dict(), sort_keys=True, indent=2) + "\n", encoding="utf-8")
