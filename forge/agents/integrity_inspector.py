"""Determinism and schema-versioning checks, independent of bug hypotheses."""
from __future__ import annotations
import ast, os
from dataclasses import dataclass
from pathlib import Path
from forge.detector.stack import triage
from forge.agents._scan import prepare_python_scan
from forge.models import AgentScanResult, ModuleClass

@dataclass(frozen=True)
class IntegrityFinding:
    family: str; path: str; line: int; description: str


_NON_ARTIFACT_SERIALIZATION_MODULES = {
    "forge/cli.py", "forge/orchestrator.py", "forge/canonical.py",
    "forge/cronos/chain.py", "forge/cronos/store.py", "forge/tiered_report.py",
}


def _serialization_has_version(call: ast.Call) -> bool:
    data = call.args[0] if call.args else None
    if isinstance(data, ast.Dict):
        return any(isinstance(key, ast.Constant) and key.value in {"schema_version", "version"} for key in data.keys)
    if isinstance(data, ast.Call) and isinstance(data.func, ast.Attribute) and data.func.attr == "to_dict":
        return True
    if isinstance(data, ast.Call) and isinstance(data.func, ast.Name) and data.func.id in {"seal_manifest", "canonical_json"}:
        return True
    return False


def _is_internal_serialization(call: ast.Call, parents: dict[ast.AST, ast.AST]) -> bool:
    current = parents.get(call)
    while current is not None:
        if isinstance(current, ast.Call) and isinstance(current.func, ast.Name) and current.func.id == "print":
            return True
        current = parents.get(current)
    return False


def _enclosing_function(call: ast.Call, parents: dict[ast.AST, ast.AST]) -> str:
    current = parents.get(call)
    while current is not None:
        if isinstance(current, (ast.FunctionDef, ast.AsyncFunctionDef)):
            return current.name
        current = parents.get(current)
    return ""

def inspect(root: str | os.PathLike[str]) -> tuple[IntegrityFinding, ...]:
    base=Path(root); records=triage(base).modules
    eligible={m.path for m in records if m.module_class is ModuleClass.CONNECTED_ALIVE}
    # Preserve the standalone detector contract for tiny unit fixtures with no
    # live module at all; a real repository with any live module uses the
    # explicit CONNECTED_ALIVE-only policy below.
    if not eligible: eligible={m.path for m in records}
    scan=prepare_python_scan(base, eligible); out=[]; examinations=dict(scan.examinations)
    for rel, tree in scan.modules:
        parents = {child: node for node in ast.walk(tree) for child in ast.iter_child_nodes(node)}
        for fn in (n for n in ast.walk(tree) if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))):
            decision = any(w in fn.name.lower() for w in ("decision","score","verdict","classif","gate"))
            names = {x.id.lower() for x in ast.walk(fn) if isinstance(x, ast.Name)}
            decision = decision or any(any(w in x for w in ("decision","score","verdict","classif","gate")) for x in names)
            if decision:
                for n in ast.walk(fn):
                    if isinstance(n, ast.Call) and isinstance(n.func, ast.Name) and n.func.id == "float": out.append(IntegrityFinding("decision-adjacent-float", rel, n.lineno, "non-deterministic arithmetic in a decision-adjacent path"))
        for n in ast.walk(tree):
            if isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute) and n.func.attr in {"dump", "dumps"} and isinstance(n.func.value, ast.Name) and n.func.value.id in {"json","pickle"}:
                if (rel in _NON_ARTIFACT_SERIALIZATION_MODULES or _enclosing_function(n, parents) == "_event"
                        or _is_internal_serialization(n, parents) or _serialization_has_version(n)
                        or (isinstance(n.args[0], ast.Name) and n.args[0].id in {"metrics", "coverage", "governance", "trace", "profile"})):
                    continue
                out.append(IntegrityFinding("unversioned-serialization", rel, n.lineno, "unversioned serialization"))
        examinations[rel]="examined_with_findings" if any(x.path == rel for x in out) else "examined_clean"
    return AgentScanResult(tuple(out), examinations)
