"""Optional, deterministic post-audit recommendation agent.

This agent consumes sealed findings and already-produced metrics. It never
walks or modifies the audited repository, never changes a finding, and never
claims that a recommendation was applied.
"""
from __future__ import annotations

import json
import re
from pathlib import Path
from forge.models import Recommendation
from forge.io import load_json


def _domains(metrics: dict, module: str) -> set[str]:
    return {
        item.get("domains", [])[0]
        for item in metrics.get("domain_classification", {}).get("hypothesis_confidence", [])
        if item.get("module_path") == module and item.get("domains")
    }


def recommend(sealed_path: str | Path, metrics_path: str | Path | None = None) -> tuple[Recommendation, ...]:
    """Generate bounded suggestions from a completed sealed artifact."""
    sealed = load_json(sealed_path, f"sealed manifest {sealed_path}")
    metrics = load_json(metrics_path, f"metrics artifact {metrics_path}") if metrics_path else {}
    output: list[Recommendation] = []
    counters: dict[str, int] = {}

    def add(module: str, action: str, rationale: str, risk: str, basis: tuple[str, ...]) -> None:
        key = re.sub(r"[^a-z0-9]+", "-", action.lower()).strip("-")
        counters[key] = counters.get(key, 0) + 1
        output.append(Recommendation(f"rec-{counters[key]}-{key}", module, action, rationale, risk, basis))

    for entry in sealed.get("chain", []):
        finding = entry.get("finding", {})
        module = finding.get("module_path", "unknown")
        family = finding.get("description", "").lower()
        if "hardcoded-credential" in family or "credential" in family:
            add(module, "Move the credential to an approved secret provider or environment boundary",
                "The Security Auditor observed a non-placeholder credential-like literal.",
                "Rotation and deployment changes can break consumers if the new secret boundary is not staged.",
                (entry.get("hash", ""), "security_auditor", "hardcoded-credential"))
        elif "unsafe-deserialization" in family or "deserialization" in family:
            add(module, "Replace unsafe deserialization with an explicitly constrained loader and validate the boundary",
                "The Security Auditor observed a deserialization call outside its benign criteria.",
                "A format or compatibility change may reject inputs that were previously accepted.",
                (entry.get("hash", ""), "security_auditor", "unsafe-deserialization"))
        elif "path-traversal" in family or "path traversal" in family:
            add(module, "Validate and constrain user-controlled path components before filesystem access",
                "The Security Auditor observed a path component reaching filesystem access without a recognized validation step.",
                "Overly strict canonicalization can reject legitimate paths; preserve an explicit allowlist policy.",
                (entry.get("hash", ""), "security_auditor", "path-traversal"))
        elif "unversioned-serialization" in family or "unversioned serialization" in family:
            add(module, "Add an explicit schema_version or version field to the serialized structure",
                "The Integrity Inspector observed serialization without a visible schema version.",
                "Readers and writers must be migrated together or support the prior format.",
                (entry.get("hash", ""), "integrity_inspector", "unversioned-serialization"))
        elif "parser call" in family:
            add(module, "Wrap the parser boundary with a named input or artifact error",
                "The Bug Investigator found a parser call whose malformed-input behavior was not established by structural verification.",
                "Changing exception types can affect callers; preserve the original exception as the cause and document the boundary contract.",
                (entry.get("hash", ""), "bug_investigator", "parser-boundary"))
        elif "tolerance call" in family or "float threshold" in family:
            add(module, "Document and test the numeric tolerance policy at the decision boundary",
                "The Bug Investigator found a float comparison or tolerance call without an induced boundary test.",
                "Changing tolerance values can alter classifications; test below, at, and above the boundary before changing arithmetic.",
                (entry.get("hash", ""), "bug_investigator", "numeric-boundary"))
        elif "decision-adjacent-float" in family or "non-deterministic arithmetic" in family:
            if "machine_learning" in _domains(metrics, module):
                action = "Document model reproducibility, threshold semantics, calibration, and numeric tolerance policy"
                rationale = "The finding is in an ML-hypothesized module; floating point is not treated as a defect by itself."
            else:
                action = "Document the numeric decision contract and choose an arithmetic policy appropriate to the domain"
                rationale = "The Integrity Inspector observed float construction near decision logic; domain intent must be established before changing arithmetic."
            add(module, action, rationale, "Changing numeric representation can alter thresholds and existing decisions.", (entry.get("hash", ""), "integrity_inspector", "decision-adjacent-float"))

    return tuple(output)
