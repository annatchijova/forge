"""Stage 1: deterministic weakness signatures from sealed historical runs."""
from __future__ import annotations
import json
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
from forge.io import load_json

@dataclass(frozen=True)
class FailureInstance:
    run: str; module_path: str; agent: str; family: str; check: str; mechanism: str
@dataclass(frozen=True)
class WeaknessCluster:
    signature: tuple[str, str, str]; frequency: int; examples: tuple[FailureInstance, ...]; agent: str; family: str
@dataclass(frozen=True)
class WeaknessBundle:
    clusters: tuple[WeaknessCluster, ...]

def _read(run):
    if isinstance(run, (str, Path)): return load_json(run, f"mined run {run}"), str(run)
    return run, "memory"

def mine(runs) -> WeaknessBundle:
    groups = defaultdict(list)
    for run in runs:
        data, label = _read(run); manifest = data.get("manifest", data)
        for item in manifest.get("discarded", []):
            check=item.get("reason", "unknown discard check"); agent=item.get("agent", "bug_investigator"); family=item.get("family", item.get("pattern_family", "unknown")); mechanism=item.get("mechanism", item.get("description", check))
            groups[(check, agent, mechanism)].append(FailureInstance(label, item.get("module_path", "unknown"), agent, family, check, mechanism))
        findings = list(manifest.get("findings", []))
        findings.extend(entry.get("finding", {}) for entry in data.get("chain", []))
        for item in findings:
            agent=item.get("agent", "bug_investigator"); check=item.get("reasoning", "finding survived verification"); family=item.get("family", item.get("pattern_family", "unknown")); mechanism=item.get("mechanism", item.get("description", "unknown mechanism"))
            groups[(check, agent, mechanism)].append(FailureInstance(label, item.get("module_path", "unknown"), agent, family, check, mechanism))
    clusters=[WeaknessCluster(sig, len(items), tuple(items[:5]), items[0].agent, items[0].family) for sig, items in groups.items()]
    return WeaknessBundle(tuple(sorted(clusters, key=lambda c: (-c.frequency, c.signature))))
