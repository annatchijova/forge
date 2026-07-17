"""Shared AST scan plumbing for repository detector agents."""
from __future__ import annotations
import ast
import os
from dataclasses import dataclass
from pathlib import Path
from forge.detector.stack import discover_files, exclusion_reason

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
        reason = exclusion_reason(path, base)
        if reason:
            examinations[rel] = reason
            continue
        if rel not in eligible or path.suffix != ".py":
            examinations[rel] = "excluded_by_scope"
            continue
        try:
            tree = ast.parse(path.read_text())
        except SyntaxError:
            examinations[rel] = "syntax_error"
            continue
        except OSError:
            examinations[rel] = "unreadable_file"
            continue
        except UnicodeDecodeError:
            examinations[rel] = "non_utf8_text"
            continue
        modules.append((rel, tree))
    return PythonScanSet(base, tuple(modules), examinations)
