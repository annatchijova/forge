"""Fail-closed validation for externally supplied multi-agent work products.

The native runtime has deterministic specialist workers. A Codex or other
external orchestrator may attach richer agent outputs, but a protocol ledger
alone is not evidence of independent work. This module validates that claim
before a run is presented as multi-agent.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any, Iterable


PROTOCOL_ONLY_KEYS = {"requested_role", "native_forge_role", "adi", "scope", "skills"}
REQUIRED_WORK_FIELDS = ("observations", "hypotheses", "deductions", "evidence", "decision")


class AgentIndependenceError(ValueError):
    """Raised when agent outputs do not demonstrate independent work."""


def _text_items(value: Any) -> tuple[str, ...]:
    if isinstance(value, str):
        return (value,) if value.strip() else ()
    if not isinstance(value, (list, tuple)):
        return ()
    return tuple(str(item).strip() for item in value if str(item).strip())


def _fingerprint(work: dict[str, Any]) -> str:
    payload = json.dumps(work, sort_keys=True, separators=(",", ":"), default=str)
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def validate_independent_results(
    results: dict[str, dict[str, Any]],
    required_agents: Iterable[str],
) -> dict[str, Any]:
    """Validate external agent results and return an audit-ready summary.

    Each result must contain a ``work_product`` with concrete observations,
    hypotheses, deductions, evidence, and a decision. A protocol-only record,
    a missing role, or duplicated work product fails closed.
    """
    required = tuple(required_agents)
    missing = sorted(set(required) - set(results))
    if missing:
        raise AgentIndependenceError(f"agent results missing: {missing}")
    fingerprints: dict[str, str] = {}
    for agent in required:
        record = results[agent]
        if not isinstance(record, dict):
            raise AgentIndependenceError(f"{agent} result is not an object")
        if set(record).issubset(PROTOCOL_ONLY_KEYS):
            raise AgentIndependenceError(f"{agent} supplied protocol only; independent work product is missing")
        work = record.get("work_product")
        if not isinstance(work, dict):
            raise AgentIndependenceError(f"{agent} work_product is missing")
        missing_fields = [field for field in REQUIRED_WORK_FIELDS if field not in work]
        if missing_fields:
            raise AgentIndependenceError(f"{agent} work_product missing fields: {missing_fields}")
        if not _text_items(work.get("observations")):
            raise AgentIndependenceError(f"{agent} has no concrete observations")
        if not _text_items(work.get("evidence")):
            raise AgentIndependenceError(f"{agent} has no evidence references")
        if not _text_items(work.get("decision")):
            raise AgentIndependenceError(f"{agent} has no decision")
        fingerprints[agent] = _fingerprint(work)
    duplicates: dict[str, list[str]] = {}
    for agent, digest in fingerprints.items():
        duplicates.setdefault(digest, []).append(agent)
    repeated = [agents for agents in duplicates.values() if len(agents) > 1]
    if repeated:
        raise AgentIndependenceError(f"duplicate agent work products: {repeated}")
    return {
        "status": "INDEPENDENCE_VERIFIED",
        "agents": list(required),
        "unique_work_products": len(fingerprints),
        "work_product_digests": fingerprints,
    }


def load_and_validate(directory: str | Path, required_agents: Iterable[str]) -> dict[str, Any]:
    """Load ``*.json`` agent records from a directory and validate them."""
    root = Path(directory)
    results: dict[str, dict[str, Any]] = {}
    for path in sorted(root.glob("*.json")):
        record = json.loads(path.read_text(encoding="utf-8"))
        if not isinstance(record, dict):
            continue
        agent = record.get("agent") or record.get("requested_role")
        if agent:
            results[str(agent)] = record
    return validate_independent_results(results, required_agents)


__all__ = ("AgentIndependenceError", "load_and_validate", "validate_independent_results")
