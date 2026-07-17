"""Deterministic severity and finding-family classification."""
from __future__ import annotations


CORE_MODULE_MARKERS = ("__main__", "runtime", "sealing", "verification", "cronos/chain")

_SEVERITY_RANK = {"INFO": 0, "LOW": 1, "MEDIUM": 2, "HIGH": 3, "CRITICAL": 4}
_IMPACT_BY_FAMILY = {
    "credential": "CRITICAL",
    "path-traversal": "CRITICAL",
    "shell-true": "CRITICAL",
    "dynamic-evaluation": "CRITICAL",
    "unverified-webhook": "CRITICAL",
    "subprocess": "HIGH",
    "parser-boundary": "HIGH",
    "numeric-boundary": "MEDIUM",
    "unversioned-serialization": "MEDIUM",
}
_CONFIDENCE_CEILING = {
    "PLAUSIBLE HYPOTHESIS": "MEDIUM",
    "CODE FACT": "HIGH",
    "CONFIRMED BY INDUCTION": "CRITICAL",
    "FALSIFIED": "INFO",
    "PROTOCOL_GAP": "LOW",
    "DESIGN_INCONSISTENCY": "LOW",
    "UNDETERMINED": "LOW",
    "NOT_APPLICABLE": "INFO",
}


def finding_family(description: str) -> str:
    text = description.lower()
    if "webhook" in text:
        return "unverified-webhook"
    if "unversioned serialization" in text or "unversioned-serialization" in text:
        return "unversioned-serialization"
    if "parser call" in text or "parser boundary" in text:
        return "parser-boundary"
    if "shell=true" in text:
        return "shell-true"
    if "subprocess" in text or "os.system" in text:
        return "subprocess"
    if "float" in text or "tolerance" in text:
        return "numeric-boundary"
    if "credential" in text or "secret" in text:
        return "credential"
    if "path" in text and "open" in text:
        return "path-traversal"
    if "eval" in text or "exec" in text:
        return "dynamic-evaluation"
    return "other"


def severity_for(
    module_path: str,
    epistemic_level: str,
    description: str,
    agent: str = "",
    family: str | None = None,
    controllability: str = "UNDETERMINED",
    exploitability: str = "NOT_ASSESSED",
) -> str:
    """Derive severity deterministically from four independent axes.

    Family describes potential impact; epistemic level, controllability and
    exploitability bound what may be claimed.  In particular, no finding is
    HIGH/CRITICAL unless attacker control and flow evidence are explicit.
    """
    family = family or finding_family(description)
    impact = _IMPACT_BY_FAMILY.get(family, "MEDIUM")
    ceiling = _CONFIDENCE_CEILING.get(epistemic_level, "LOW")
    severity = impact if _SEVERITY_RANK[impact] <= _SEVERITY_RANK[ceiling] else ceiling
    if controllability != "ATTACKER_CONTROLLED":
        ceiling = "MEDIUM"
    elif exploitability not in {"PLAUSIBLE", "CONFIRMED"}:
        ceiling = "MEDIUM"
    return severity if _SEVERITY_RANK[severity] <= _SEVERITY_RANK[ceiling] else ceiling
