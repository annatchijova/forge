"""Determinism and schema-versioning checks, independent of bug hypotheses."""
from __future__ import annotations
import ast, os
from dataclasses import dataclass
from pathlib import Path
from forge.detector.stack import triage
from forge.agents._scan import prepare_python_scan
from forge.models import AgentScanResult, ModuleClass
from forge.agent_protocol import mandatory_protocol

@dataclass(frozen=True)
class IntegrityFinding:
    family: str; path: str; line: int; description: str


_NON_ARTIFACT_SERIALIZATION_MODULES = {
    "forge/cli.py", "forge/orchestrator.py", "forge/canonical.py",
    "forge/cronos/chain.py", "forge/cronos/store.py", "forge/tiered_report.py",
    # These are presentation serializers: JSON is embedded in HTML and is not
    # a versioned interchange artifact.
    "forge/report.py",
}
_SERIALIZATION_FUNCTION_NAMES = {
    "as_dict", "serialize", "to_dict", "to_json", "jsonable_encoder",
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


def _versioned_payload_names(tree: ast.AST) -> set[str]:
    """Find simple local names bound to dicts carrying a schema/version key."""
    names: set[str] = set()
    for node in ast.walk(tree):
        if not isinstance(node, (ast.Assign, ast.AnnAssign)):
            continue
        value = node.value
        if not isinstance(value, ast.Dict):
            continue
        if not any(isinstance(key, ast.Constant) and key.value in {"schema_version", "version", "benchmark_schema_version"}
                   for key in value.keys):
            continue
        targets = node.targets if isinstance(node, ast.Assign) else [node.target]
        names.update(target.id for target in targets if isinstance(target, ast.Name))
    return names


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


def _float_calls_reaching_return(fn: ast.FunctionDef | ast.AsyncFunctionDef) -> set[int]:
    """Return float() lines with a shallow path to the function's return.

    This intentionally follows only named assignments and return expressions.
    A float stored in telemetry (including a dict later passed as a keyword to
    a result object) is not treated as decision arithmetic.
    """
    assignments: list[tuple[str, ast.AST]] = []
    for node in ast.walk(fn):
        if isinstance(node, ast.Assign):
            targets = [target.id for target in node.targets if isinstance(target, ast.Name)]
            assignments.extend((target, node.value) for target in targets)
        elif isinstance(node, ast.AnnAssign) and isinstance(node.target, ast.Name) and node.value is not None:
            assignments.append((node.target.id, node.value))

    tainted: dict[str, set[int]] = {}
    changed = True
    while changed:
        changed = False
        for name, value in assignments:
            float_lines = {node.lineno for node in ast.walk(value)
                           if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id == "float"}
            referenced = {node.id for node in ast.walk(value) if isinstance(node, ast.Name)}
            sources = float_lines | set().union(*(tainted.get(ref, set()) for ref in referenced))
            if sources and sources != tainted.get(name, set()):
                tainted[name] = sources
                changed = True

    flagged: set[int] = set()
    for node in ast.walk(fn):
        if not isinstance(node, ast.Return) or node.value is None:
            continue
        if isinstance(node.value, ast.Name):
            flagged.update(tainted.get(node.value.id, set()))
        elif isinstance(node.value, ast.Call) and isinstance(node.value.func, ast.Name) and node.value.func.id == "float":
            flagged.add(node.value.lineno)
        elif isinstance(node.value, (ast.BinOp, ast.BoolOp, ast.Compare, ast.UnaryOp)):
            direct = {child.lineno for child in ast.walk(node.value)
                      if isinstance(child, ast.Call) and isinstance(child.func, ast.Name) and child.func.id == "float"}
            flagged.update(direct)
            referenced = {child.id for child in ast.walk(node.value) if isinstance(child, ast.Name)}
            flagged.update(set().union(*(tainted.get(ref, set()) for ref in referenced)))
    return flagged

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
        versioned_payload_names = _versioned_payload_names(tree)
        for fn in (n for n in ast.walk(tree) if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))):
            if fn.name in _SERIALIZATION_FUNCTION_NAMES:
                continue
            for line in sorted(_float_calls_reaching_return(fn)):
                out.append(IntegrityFinding("decision-adjacent-float", rel, line, "non-deterministic arithmetic in a decision-adjacent path"))
        for n in ast.walk(tree):
            if isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute) and n.func.attr in {"dump", "dumps"} and isinstance(n.func.value, ast.Name) and n.func.value.id in {"json","pickle"}:
                if (rel in _NON_ARTIFACT_SERIALIZATION_MODULES or _enclosing_function(n, parents) in {"_event", "_sha256_dict", "save"}
                        or _is_internal_serialization(n, parents) or _serialization_has_version(n)
                        or (isinstance(n.args[0], ast.Name) and n.args[0].id in versioned_payload_names)
                        or (isinstance(n.args[0], ast.Name) and n.args[0].id in {"metrics", "coverage", "governance", "trace", "profile"})):
                    continue
                out.append(IntegrityFinding("unversioned-serialization", rel, n.lineno, "unversioned serialization"))
        examinations[rel]="examined_with_findings" if any(x.path == rel for x in out) else "examined_clean"
    return AgentScanResult(
        tuple(out), examinations,
        mandatory_protocol(
            "integrity_inspector",
            tuple(f"{item.family} observed at {item.path}:{item.line}" for item in out),
            examinations,
        ),
    )
