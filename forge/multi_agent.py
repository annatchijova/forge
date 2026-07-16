"""Canonicalization and sealing of external multi-agent audit results."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

from forge.canonical import canonical_json
from forge.agent_independence import load_and_validate
from forge.io import load_json
from forge.sealing import write_sealed_findings


def _digest(records: list[dict[str, Any]]) -> str:
    return hashlib.sha256(canonical_json(records).encode("utf-8")).hexdigest()


def _external_findings(path: Path) -> list[dict[str, Any]]:
    data = load_json(path, f"external findings {path}")
    findings = data.get("findings")
    if not isinstance(findings, list):
        raise ValueError(f"external findings artifact has no findings list: {path}")
    return findings


def _native_findings(path: Path) -> list[dict[str, Any]]:
    data = load_json(path, f"native sealed findings {path}")
    chain = data.get("chain")
    if not isinstance(chain, list):
        raise ValueError(f"sealed artifact has no chain: {path}")
    return [entry["finding"] for entry in chain if isinstance(entry, dict) and isinstance(entry.get("finding"), dict)]


def build_canonical_findings(external: list[dict[str, Any]], native: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Keep source layers explicit while producing one deterministic finding set."""
    records: list[dict[str, Any]] = []
    for index, finding in enumerate(external):
        records.append({"record_id": f"codex_external:{finding.get('id', index + 1)}", "source_layer": "codex_external", "finding": finding})
    for index, finding in enumerate(native):
        records.append({"record_id": f"forge_native:{index}", "source_layer": "forge_native", "finding": finding})
    return records


def finalize_multi_agent_run(run_dir: str | Path, required_agents: list[str], external_findings_path: str | Path | None = None, native_sealed_path: str | Path | None = None) -> dict[str, Any]:
    """Validate independence, canonicalize both layers, and seal the result."""
    root = Path(run_dir)
    independence = load_json(root / "agent-independence.json", "agent independence artifact")
    if independence.get("status") != "INDEPENDENCE_VERIFIED":
        raise ValueError("multi-agent close requires INDEPENDENCE_VERIFIED")
    validated = load_and_validate(root / "agent-results", required_agents)
    external_path = Path(external_findings_path) if external_findings_path else root / "findings.json"
    native_path = Path(native_sealed_path) if native_sealed_path else root / "verification-manifest.sealed.json"
    external = _external_findings(external_path)
    native = _native_findings(native_path)
    records = build_canonical_findings(external, native)
    finding_set_digest = _digest(records)
    canonical = {
        "schema_version": "1.0",
        "finding_set_digest": finding_set_digest,
        "independence": validated,
        "source_layers": {"codex_external": len(external), "forge_native": len(native)},
        "records": records,
    }
    canonical_path = root / "canonical-findings.json"
    canonical_path.write_text(json.dumps(canonical, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    sealed_path = root / "verification-manifest.canonical.sealed.json"
    write_sealed_findings(records, {"schema_version": "1.0", "finding_set_digest": finding_set_digest, "root": str(root), "source_layers": canonical["source_layers"]}, sealed_path)
    return {"status": "CANONICAL_FINDINGS_SEALED", "finding_set_digest": finding_set_digest, "source_layers": canonical["source_layers"], "canonical": str(canonical_path), "sealed": str(sealed_path)}


__all__ = ("build_canonical_findings", "finalize_multi_agent_run")
