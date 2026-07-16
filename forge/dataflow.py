"""Small, conservative AST data-flow helpers shared by detectors."""
from __future__ import annotations

import ast


def float_calls_reaching_return(function: ast.FunctionDef | ast.AsyncFunctionDef) -> set[int]:
    """Return float() lines with a shallow path to the function return."""
    assignments: list[tuple[str, ast.AST]] = []
    for node in ast.walk(function):
        if isinstance(node, ast.Assign):
            assignments.extend((target.id, node.value) for target in node.targets if isinstance(target, ast.Name))
        elif isinstance(node, ast.AnnAssign) and isinstance(node.target, ast.Name) and node.value is not None:
            assignments.append((node.target.id, node.value))
    tainted: dict[str, set[int]] = {}
    changed = True
    while changed:
        changed = False
        for name, value in assignments:
            float_lines = {node.lineno for node in ast.walk(value) if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id == "float"}
            referenced = {node.id for node in ast.walk(value) if isinstance(node, ast.Name)}
            sources = float_lines | set().union(*(tainted.get(ref, set()) for ref in referenced))
            current = tainted.get(name, set())
            # Union into the existing taint set rather than overwriting it: a
            # name reassigned more than once (a loop body, if/else branches)
            # produces one (name, value) pair per assignment, all keyed by
            # the same name. Overwriting made `sources != tainted[name]`
            # permanently true whenever two assignments' float-call lines
            # differed, so `changed` never settled to False - an infinite
            # loop on any function reassigning a name with different float()
            # calls in different branches (a common, ordinary pattern).
            if not sources <= current:
                tainted[name] = current | sources
                changed = True
    flagged: set[int] = set()
    for node in ast.walk(function):
        if not isinstance(node, ast.Return) or node.value is None:
            continue
        if isinstance(node.value, ast.Name):
            flagged.update(tainted.get(node.value.id, set()))
        elif isinstance(node.value, ast.Call) and isinstance(node.value.func, ast.Name) and node.value.func.id == "float":
            flagged.add(node.value.lineno)
        elif isinstance(node.value, (ast.BinOp, ast.BoolOp, ast.Compare, ast.UnaryOp)):
            flagged.update(child.lineno for child in ast.walk(node.value) if isinstance(child, ast.Call) and isinstance(child.func, ast.Name) and child.func.id == "float")
            referenced = {child.id for child in ast.walk(node.value) if isinstance(child, ast.Name)}
            flagged.update(set().union(*(tainted.get(ref, set()) for ref in referenced)))
    return flagged


def comparison_reaches_return(tree: ast.AST, line: int) -> bool:
    """Return whether a comparison on ``line`` reaches its enclosing return."""
    parents = {child: parent for parent in ast.walk(tree) for child in ast.iter_child_nodes(parent)}
    comparisons = [node for node in ast.walk(tree) if isinstance(node, ast.Compare) and node.lineno == line]
    if not comparisons:
        return False
    comparison = comparisons[0]
    function = comparison
    while function in parents and not isinstance(function, (ast.FunctionDef, ast.AsyncFunctionDef)):
        function = parents[function]
    if not isinstance(function, (ast.FunctionDef, ast.AsyncFunctionDef)):
        return False
    names: set[str] = set()
    for node in ast.walk(function):
        if isinstance(node, ast.Assign) and isinstance(node.value, ast.Compare) and node.value.lineno == line:
            names.update(target.id for target in node.targets if isinstance(target, ast.Name))
        elif isinstance(node, ast.AnnAssign) and isinstance(node.value, ast.Compare) and node.value.lineno == line and isinstance(node.target, ast.Name):
            names.add(node.target.id)
    for node in ast.walk(function):
        if isinstance(node, ast.Return):
            if node.value is not None and (comparison in ast.walk(node.value) or (isinstance(node.value, ast.Name) and node.value.id in names)):
                return True
    return False
