"""Determinism and schema-versioning checks, independent of bug hypotheses."""
from __future__ import annotations
import ast, os
from dataclasses import dataclass
from pathlib import Path

@dataclass(frozen=True)
class IntegrityFinding:
    family: str; path: str; line: int; description: str

def inspect(root: str | os.PathLike[str]) -> tuple[IntegrityFinding, ...]:
    out=[]
    for p in Path(root).rglob("*.py"):
        try: tree=ast.parse(p.read_text())
        except SyntaxError: continue
        for fn in (n for n in ast.walk(tree) if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))):
            decision = any(w in fn.name.lower() for w in ("decision","score","verdict","classif","gate"))
            names = {x.id.lower() for x in ast.walk(fn) if isinstance(x, ast.Name)}
            decision = decision or any(any(w in x for w in ("decision","score","verdict","classif","gate")) for x in names)
            if decision:
                for n in ast.walk(fn):
                    if isinstance(n, ast.Call) and isinstance(n.func, ast.Name) and n.func.id == "float": out.append(IntegrityFinding("decision-adjacent-float", str(p.relative_to(root)), n.lineno, "non-deterministic arithmetic in a decision-adjacent path"))
        for n in ast.walk(tree):
            if isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute) and n.func.attr in {"dump", "dumps"} and isinstance(n.func.value, ast.Name) and n.func.value.id in {"json","pickle"}:
                data = n.args[0] if n.args else None
                versioned = isinstance(data, ast.Dict) and any(isinstance(k, ast.Constant) and k.value in {"schema_version","version"} for k in data.keys)
                if not versioned: out.append(IntegrityFinding("unversioned-serialization", str(p.relative_to(root)), n.lineno, "unversioned serialization"))
    return tuple(out)

