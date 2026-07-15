"""Cross-agent contradiction detection, kept deterministic and explainable."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Iterable


@dataclass(frozen=True)
class Contradiction:
    module_path: str
    agents: tuple[str, ...]
    description: str
    evidence: tuple[str, ...]

    def to_dict(self) -> dict[str, Any]:
        return {
            "module_path": self.module_path,
            "agents": self.agents,
            "description": self.description,
            "evidence": self.evidence,
        }


def find_contradictions(findings: Iterable[Any], discarded: Iterable[dict[str, Any]] = ()) -> tuple[Contradiction, ...]:
    """Find explicit evidence collisions without guessing from severity.

    The first rule is intentionally narrow: a credential finding is in tension
    with a placeholder/test/fixture explanation on the same module. More rules
    should be added only with a regression fixture and an explicit evidence
    contract.
    """
    records = list(findings)
    discards = list(discarded)
    out: list[Contradiction] = []
    for finding in records:
        text = " ".join((str(getattr(finding, "description", "")), str(getattr(finding, "reasoning", "")))).lower()
        if "credential" not in text and "secret" not in text and "token" not in text:
            continue
        module = str(getattr(finding, "module_path", ""))
        alternatives = [
            str(item.get("reason", "")) for item in discards
            if str(item.get("module_path", "")) == module
        ]
        alternatives += [
            str(other.description) for other in records
            if other is not finding and str(getattr(other, "module_path", "")) == module
        ]
        for alternative in alternatives:
            lowered = alternative.lower()
            if any(marker in lowered for marker in ("placeholder", "fixture", "test value", "test-only", "example")):
                agents = tuple(sorted({str(getattr(finding, "agent", "unknown")), "alternative-explanation"}))
                out.append(Contradiction(
                    module,
                    agents,
                    "Credential-like evidence conflicts with a placeholder/test explanation.",
                    (str(getattr(finding, "description", "")), alternative),
                ))
                break
    return tuple(out)


__all__ = ("Contradiction", "find_contradictions")
