"""Mandatory agent protocol: A-D-I plus the complete skills catalog.

The detector implementations are intentionally deterministic, but their
outputs are not allowed to bypass the inquiry protocol.  Static detectors may
stop at ``UNDETERMINED`` when no safe induction harness exists; they must still
record the hypothesis and the falsifying experiment they would run.
"""
from __future__ import annotations

import re
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable


ADI_STAGES = ("abduction", "deduction", "induction")
AGENT_NAMES = (
    "archaeologist",
    "bug_investigator",
    "integrity_inspector",
    "patch_reviewer",
    "recommendation_agent",
    "report_composer",
    "security_auditor",
    "web_auditor",
)


@dataclass(frozen=True)
class ADIEntry:
    stage: str
    statement: str
    evidence: tuple[str, ...] = ()
    status: str = "UNDETERMINED"

    def __post_init__(self) -> None:
        if self.stage not in ADI_STAGES:
            raise ValueError(f"invalid A-D-I stage: {self.stage}")
        if not self.statement.strip():
            raise ValueError("A-D-I statement is required")


@dataclass(frozen=True)
class SkillApplication:
    name: str
    source: str
    status: str
    evidence: tuple[str, ...]
    limitation: str


@dataclass(frozen=True)
class AgentProtocol:
    agent: str
    adi: tuple[ADIEntry, ...]
    skills: tuple[SkillApplication, ...]
    scope: tuple[str, ...]

    def __post_init__(self) -> None:
        if self.agent not in AGENT_NAMES:
            raise ValueError(f"unknown agent: {self.agent}")
        stages = {entry.stage for entry in self.adi}
        missing = set(ADI_STAGES) - stages
        if missing:
            raise ValueError(f"A-D-I ledger missing stages: {sorted(missing)}")

    def to_dict(self) -> dict:
        return {
            "agent": self.agent,
            "adi": [asdict(item) for item in self.adi],
            "skills": [asdict(item) for item in self.skills],
            "scope": list(self.scope),
        }


def skills_catalog(skills_root: str | Path | None = None) -> tuple[tuple[str, str, str], ...]:
    """Load every policy skill, including Markdown-only skills.

    Markdown skills are policy instructions, not executable detectors.  They
    nevertheless belong to the mandatory agent contract and are therefore
    recorded for every agent, with an explicit limitation when no executable
    checker exists yet.
    """
    root = Path(skills_root) if skills_root else Path(__file__).resolve().parents[1] / "skills-gpt"
    records = []
    for path in sorted(root.glob("*.md")):
        text = path.read_text(encoding="utf-8")
        match = re.search(r"^name:\s*(.+?)\s*$", text, re.MULTILINE)
        name = match.group(1).strip() if match else path.stem
        records.append((name, str(path), text))
    return tuple(records)


def mandatory_protocol(
    agent: str,
    observations: Iterable[str],
    scope: Iterable[str],
    skills_root: str | Path | None = None,
    induction_status: str = "UNDETERMINED",
    induction_reason: str = "No language-specific induction harness was registered for this observation.",
) -> AgentProtocol:
    """Build the required protocol ledger for every agent invocation."""
    obs = tuple(item for item in observations if item.strip())
    if not obs:
        obs = ("No actionable observation was emitted in the examined scope.",)
    observation_text = "; ".join(obs[:5])
    adi = (
        ADIEntry("abduction", f"Observed evidence may be explained by: {observation_text}.", obs, "PLAUSIBLE_HYPOTHESIS"),
        ADIEntry("deduction", "A falsification experiment must distinguish the observed mechanism from a benign structural explanation.", obs, "PREDICTION_REQUIRED"),
        ADIEntry("induction", induction_reason, obs, induction_status),
    )
    applications = tuple(
        SkillApplication(
            name=name,
            source=source,
            status="APPLIED",
            evidence=(f"{agent} received the mandatory policy catalog entry {name} before producing its result.",),
            limitation="Policy text is loaded and recorded; semantic enforcement requires an executable checker for this skill.",
        )
        for name, source, _text in skills_catalog(skills_root)
    )
    return AgentProtocol(agent, adi, applications, tuple(scope))


def validate_protocols(protocols: dict[str, AgentProtocol]) -> None:
    """Fail closed if any required agent or skill ledger is absent."""
    missing_agents = set(AGENT_NAMES) - set(protocols)
    if missing_agents:
        raise ValueError(f"agent protocol missing: {sorted(missing_agents)}")
    expected_skills = {name for name, _source, _text in skills_catalog()}
    for agent, protocol in protocols.items():
        actual = {item.name for item in protocol.skills}
        missing = expected_skills - actual
        if missing:
            raise ValueError(f"{agent} protocol missing skills: {sorted(missing)}")
