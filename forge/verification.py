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

def verify_hypotheses(manifest: HypothesesManifest) -> VerificationManifest:
    findings, discarded = [], []
    root = Path(manifest.root)
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
            if "subprocess" in h.description and _subprocess_enclosure(tree, line):
                discarded.append({"module_path": h.module_path, "reason": "AST proves actual try/except enclosure; benign explanation survives."})
                continue
        findings.append(Finding("INFERRED", "PLAUSIBLE HYPOTHESIS", h.module_path, h.description, evidence, "Observed construct matches; no induction was run, so level is capped at PLAUSIBLE HYPOTHESIS."))
    return VerificationManifest("1.0", "0.1.0", manifest.schema_version, manifest.root, int(time.time()), tuple(findings), tuple(discarded))

def write_verification_manifest(manifest: VerificationManifest, destination: str | Path) -> None:
    Path(destination).write_text(json.dumps(manifest.to_dict(), sort_keys=True, indent=2) + "\n", encoding="utf-8")
