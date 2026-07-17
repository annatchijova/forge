"""Cross-run comparison of sealed FORGE audits."""
from __future__ import annotations

import hashlib
import json
from fractions import Fraction
from pathlib import Path
from typing import Any

from forge.canonical import canonical_json
from forge.io import load_json
from forge.sealing import verify_sealed


def _finding_key(finding: dict[str, Any]) -> str:
    identity = {
        "agent": finding.get("agent"),
        "module_path": finding.get("module_path"),
        "description": finding.get("description"),
        "evidence": finding.get("evidence", []),
    }
    return hashlib.sha256(canonical_json(identity).encode("utf-8")).hexdigest()


def _findings(run: Path) -> dict[str, dict[str, Any]]:
    canonical = run / "verification-manifest.canonical.sealed.json"
    sealed_path = canonical if canonical.is_file() else run / "verification-manifest.sealed.json"
    sealed = load_json(sealed_path, f"sealed manifest in {run}")
    verification = verify_sealed(sealed)
    if not verification["ok"]:
        raise ValueError(f"cannot compare unverified run {run}: {verification['issues']}")
    return {_finding_key(entry["finding"]): entry["finding"] for entry in sealed.get("chain", [])}


def _coverage(run: Path) -> Fraction:
    data = load_json(run / "metrics.json", f"metrics in {run}")
    ratio = data.get("quality", {}).get("repository_coverage", {})
    return Fraction(int(ratio.get("covered", 0)), int(ratio.get("total", 1)) or 1)


def _comparison_input(run: Path, findings: dict[str, dict[str, Any]]) -> dict[str, Any]:
    """Bind a comparison to its scope, engine and detector configuration."""
    triage = load_json(run / "triage-manifest.json", f"triage manifest in {run}")
    metrics = load_json(run / "metrics.json", f"metrics in {run}")
    skills_path = run / "skills-runtime.json"
    skills = load_json(skills_path, f"skills runtime in {run}") if skills_path.is_file() else {}
    scope = [
        {"path": item.get("path"), "language": item.get("language"), "module_class": item.get("module_class")}
        for item in triage.get("modules", []) if isinstance(item, dict)
    ]
    scope_hash = hashlib.sha256(canonical_json(scope).encode("utf-8")).hexdigest()
    finding_set_digest = hashlib.sha256(canonical_json(sorted(findings)).encode("utf-8")).hexdigest()
    return {
        "finding_set_digest": finding_set_digest,
        "scope_hash": scope_hash,
        "forge_version": triage.get("forge_version"),
        "agent_config": sorted(metrics.get("agents", {}).keys()) if isinstance(metrics.get("agents"), dict) else [],
        "skills": hashlib.sha256(canonical_json(skills).encode("utf-8")).hexdigest(),
    }


def compare_runs(previous: str | Path, current: str | Path) -> dict[str, Any]:
    before, after = Path(previous), Path(current)
    old = _findings(before)
    new = _findings(after)
    old_input = _comparison_input(before, old)
    new_input = _comparison_input(after, new)
    old_keys, new_keys = set(old), set(new)
    comparable = old_input["scope_hash"] == new_input["scope_hash"]
    delta = _coverage(after) - _coverage(before) if comparable else None
    return {
        "comparison_schema_version": "1.1",
        "previous_run": str(before),
        "current_run": str(after),
        "previous_findings": len(old),
        "current_findings": len(new),
        "resolved": [old[key] for key in sorted(old_keys - new_keys)],
        "new": [new[key] for key in sorted(new_keys - old_keys)],
        "unchanged": [new[key] for key in sorted(old_keys & new_keys)],
        "coverage_comparable": comparable,
        "coverage_delta": {"numerator": delta.numerator, "denominator": delta.denominator} if delta is not None else None,
        "previous_coverage": {"numerator": _coverage(before).numerator, "denominator": _coverage(before).denominator},
        "current_coverage": {"numerator": _coverage(after).numerator, "denominator": _coverage(after).denominator},
        "finding_set": {
            "previous": "canonical" if (before / "verification-manifest.canonical.sealed.json").is_file() else "native",
            "current": "canonical" if (after / "verification-manifest.canonical.sealed.json").is_file() else "native",
        },
        "comparison_input": {"previous": old_input, "current": new_input},
    }


__all__ = ("compare_runs",)
