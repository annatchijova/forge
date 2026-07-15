"""Forensic runtime trace, inspired by CRONOS but native to FORGE."""
from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime, timezone
from uuid import uuid4
from typing import Any

def _now() -> str:
    return datetime.now(timezone.utc).isoformat()

@dataclass(frozen=True)
class TraceEvent:
    sequence: int
    kind: str
    timestamp: str
    payload: dict[str, Any]

@dataclass
class RuntimeTrace:
    run_id: str = field(default_factory=lambda: str(uuid4()))
    started_at: str = field(default_factory=_now)
    events: list[TraceEvent] = field(default_factory=list)

    def record(self, kind: str, **payload: Any) -> TraceEvent:
        event = TraceEvent(len(self.events), kind, _now(), payload)
        self.events.append(event)
        return event

    def to_dict(self) -> dict[str, Any]:
        return {"trace_version": "1", "run_id": self.run_id, "started_at": self.started_at, "events": [{"sequence": e.sequence, "kind": e.kind, "timestamp": e.timestamp, "payload": e.payload} for e in self.events]}
