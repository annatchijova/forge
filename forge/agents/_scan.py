"""Shared AST scan plumbing for repository detector agents."""
from __future__ import annotations
import ast
import os
from dataclasses import dataclass
from pathlib import Path
from forge.detector.stack import discover_files, is_excluded_by_policy

@dataclass(frozen=True)
class PythonScanSet:
    root: Path
    modules: tuple[tuple[str, ast.AST], ...]
    examinations: dict[str, str]

def prepare_python_scan(root: str | os.PathLike[str], eligible: set[str]) -> PythonScanSet:
    base = Path(root)
    examinations: dict[str, str] = {}
    modules: list[tuple[str, ast.AST]] = []
    for path in discover_files(base, include_excluded=True):
        rel = str(path.relative_to(base))
        if is_excluded_by_policy(path, base):
            examinations[rel] = "excluded_by_policy"
            continue
        if rel not in eligible or path.suffix != ".py":
            examinations[rel] = "excluded_by_scope"
            continue
        try:
            tree = ast.parse(path.read_text())
        except SyntaxError:
            examinations[rel] = "syntax_error"
            continue
        except (OSError, UnicodeDecodeError):
            examinations[rel] = "binary_or_unreadable"
            continue
        modules.append((rel, tree))
    return PythonScanSet(base, tuple(modules), examinations)
