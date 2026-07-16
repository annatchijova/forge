"""Conservative, time-bounded execution for parser hypotheses.

Induction is deliberately narrower than arbitrary fuzzing.  It only invokes a
module-level function for parser hypotheses, in a spawned child process, with
synthetic malformed text.  Other hypothesis families remain AST-only until a
family-specific harness exists.
"""
from __future__ import annotations

import ast
import importlib.util
import inspect
import multiprocessing
import sys
from queue import Empty
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any


_NAMED_BOUNDARY_ERRORS = {"JSONDecodeError", "ValueError", "YAMLError", "TomlDecodeError", "ForgeArtifactError"}


@dataclass(frozen=True)
class InductionResult:
    status: str
    family: str
    detail: str
    evidence: str

    def to_dict(self) -> dict[str, str]:
        return asdict(self)


def _function_for_line(tree: ast.AST, line: int) -> ast.FunctionDef | ast.AsyncFunctionDef | None:
    parents: dict[ast.AST, ast.AST] = {}
    for parent in ast.walk(tree):
        for child in ast.iter_child_nodes(parent):
            parents[child] = parent
    candidates = []
    for node in ast.walk(tree):
        if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            continue
        if not (node.lineno <= line <= getattr(node, "end_lineno", node.lineno)):
            continue
        parent = parents.get(node)
        nested = False
        while parent is not None:
            if isinstance(parent, (ast.FunctionDef, ast.AsyncFunctionDef)):
                nested = True
                break
            parent = parents.get(parent)
        if not nested:
            candidates.append(node)
    return min(candidates, key=lambda node: getattr(node, "end_lineno", node.lineno) - node.lineno, default=None)


def _synthetic_value(name: str) -> str:
    return "{not valid json"


def _module_name(root: Path, module_path: str) -> str | None:
    """Return a package-qualified module name when the path has a package."""
    path = Path(module_path)
    parts = list(path.with_suffix("").parts)
    if not parts or any(part == ".." for part in parts):
        return None
    package_parts: list[str] = []
    for part in parts[:-1]:
        package_parts.append(part)
        if not (root.joinpath(*package_parts) / "__init__.py").is_file():
            return None
    return ".".join(parts)


def _invoke_worker(root: str, module_path: str, function_name: str, queue: Any) -> None:
    try:
        root_path = Path(root)
        qualified_name = _module_name(root_path, module_path)
        if qualified_name:
            sys.path.insert(0, str(root_path))
            try:
                module = importlib.import_module(qualified_name)
            except BaseException as exc:
                queue.put(("import-error", type(exc).__name__, str(exc)[:240]))
                return
        else:
            module_name = f"forge_induction_{abs(hash(module_path))}"
            spec = importlib.util.spec_from_file_location(module_name, root_path / module_path)
            if spec is None or spec.loader is None:
                queue.put(("import-error", "ModuleSpecError", "module spec unavailable"))
                return
            module = importlib.util.module_from_spec(spec)
            try:
                spec.loader.exec_module(module)
            except BaseException as exc:
                queue.put(("import-error", type(exc).__name__, str(exc)[:240]))
                return
        function = getattr(module, function_name)
        signature = inspect.signature(function)
        args: list[str] = []
        for parameter in signature.parameters.values():
            if parameter.kind in (parameter.VAR_POSITIONAL, parameter.VAR_KEYWORD):
                continue
            if parameter.kind is parameter.KEYWORD_ONLY and parameter.default is not parameter.empty:
                continue
            if parameter.default is not parameter.empty and parameter.kind is not parameter.KEYWORD_ONLY:
                continue
            args.append(_synthetic_value(parameter.name))
        result = function(*args)
        queue.put(("returned", type(result).__name__))
    except BaseException as exc:  # child boundary: never leak target exceptions to the audit process
        queue.put(("exception", type(exc).__name__, str(exc)[:240]))


def induce_hypothesis(root: str | Path, module_path: str, line: int, description: str) -> InductionResult:
    family = "parser" if "parser call" in description.lower() else "unsupported"
    if family != "parser":
        return InductionResult("UNDETERMINED", family, "No executable harness is registered for this hypothesis family.", "AST-only verification")
    path = (Path(root) / module_path).resolve()
    root_path = Path(root).resolve()
    if path.suffix != ".py" or root_path not in path.parents:
        return InductionResult("UNDETERMINED", family, "Module is outside the permitted Python audit scope.", str(path))
    try:
        source = path.read_text(encoding="utf-8", errors="replace")
        tree = ast.parse(source, filename=str(path))
        function = _function_for_line(tree, line)
    except (OSError, SyntaxError) as exc:
        return InductionResult("UNDETERMINED", family, f"Cannot prepare isolated execution: {exc}", f"{module_path}:{line}")
    if function is None or isinstance(function, ast.AsyncFunctionDef):
        return InductionResult("UNDETERMINED", family, "No synchronous module-level function boundary was found.", f"{module_path}:{line}")

    # Test the public detector boundary when the parser call is in a private
    # helper. This avoids treating trusted lexicon loaders as user-input APIs.
    function_name = function.name
    if function_name.startswith("_"):
        public_entrypoint = next(
            (node for node in tree.body
             if isinstance(node, ast.FunctionDef) and node.name == "analyze"),
            None,
        )
        if public_entrypoint is not None:
            function_name = public_entrypoint.name

    context = multiprocessing.get_context("spawn")
    queue = context.Queue()
    process = context.Process(target=_invoke_worker, args=(str(root_path), module_path, function_name, queue))
    process.start()
    process.join(1.0)
    if process.is_alive():
        process.terminate()
        process.join(0.5)
        return InductionResult("UNDETERMINED", family, "Induction timed out after 1.0s; child process was terminated.", f"{module_path}:{line}")
    try:
        result = queue.get(timeout=0.2)
    except Empty:
        return InductionResult("UNDETERMINED", family, f"Child exited without a result (exitcode={process.exitcode}).", f"{module_path}:{line}")
    if result[0] == "import-error":
        return InductionResult("UNDETERMINED", family, f"Target module could not be loaded in its package context: {result[1]}: {result[2]}", f"{module_path}:{line}")
    if result[0] == "exception":
        error_name, detail = result[1], result[2]
        if error_name in _NAMED_BOUNDARY_ERRORS:
            return InductionResult("FALSIFIED", family, f"Named boundary error {error_name} was raised for malformed input.", f"{module_path}:{line}: {error_name}: {detail}")
        return InductionResult("CONFIRMED BY INDUCTION", family, f"Malformed input raised opaque {error_name}.", f"{module_path}:{line}: {error_name}: {detail}")
    if result[0] == "returned":
        return InductionResult("FALSIFIED", family, "Malformed input was accepted without an exception.", f"{module_path}:{line}: returned {result[1]}")
    return InductionResult("UNDETERMINED", family, str(result[1]), f"{module_path}:{line}")
