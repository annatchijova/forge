"""Executable contract derived from skills-gpt/validate-at-the-boundary.md."""
from __future__ import annotations
import ast
from forge.models import Applicability, EvaluationContext, Evidence, Finding, ModuleClass, SkillContract

class ValidateAtBoundarySkill:
    contract = SkillContract(
        "validate-at-the-boundary", "1.0",
        ("untrusted input is validated before sensitive use", "validation raises a named error"),
        ("path parameter reaches open", "serialized input reaches parser"),
        ("AST evidence of a boundary check and explicit raise",),
        ("recognizes only direct Python AST patterns; aliases and framework wrappers are undetermined",),
    )

    def applicability(self, context: EvaluationContext) -> Applicability:
        if context.module.module_class is not ModuleClass.CONNECTED_ALIVE: return Applicability.NOT_APPLICABLE
        return Applicability.APPLICABLE if "input_boundary" in context.domain_hypothesis.domains else Applicability.UNDETERMINED

    def evaluate(self, context: EvaluationContext) -> tuple[Finding, ...]:
        try: tree=ast.parse(context.source)
        except SyntaxError: return ()
        findings=[]
        for fn in (n for n in ast.walk(tree) if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))):
            params={arg.arg for arg in fn.args.args}
            guarded={name for n in ast.walk(fn) if isinstance(n, ast.If) and any(isinstance(x, ast.Raise) for x in ast.walk(n)) for name in params if any(isinstance(x, ast.Name) and x.id == name for x in ast.walk(n.test))}
            for call in (n for n in ast.walk(fn) if isinstance(n, ast.Call)):
                sensitive=(isinstance(call.func, ast.Name) and call.func.id == "open") or (isinstance(call.func, ast.Attribute) and call.func.attr in {"load", "loads", "parse"})
                if not sensitive or not call.args: continue
                arg=call.args[0]
                if isinstance(arg, ast.Name) and arg.id in params and arg.id not in guarded:
                    detail=f"parameter `{arg.id}` reaches a sensitive boundary call without an explicit raising validation"
                    findings.append(Finding("INFERRED", "PROTOCOL_GAP", context.module.path, detail, (Evidence("source", f"{context.module.path}:{call.lineno}", detail),), "validate-at-the-boundary applies because direct external input reaches a parser or filesystem call.", "validate-at-the-boundary", "PROTOCOL_GAP"))
        return tuple(findings)
