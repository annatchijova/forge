"""Bug Investigator: hypothesis generation plus evidence-based actionability."""
from dataclasses import dataclass
from forge.hypotheses import generate_hypotheses
from forge.verification import verify_hypotheses
from forge.agent_protocol import mandatory_protocol

@dataclass(frozen=True)
class RankedHypotheses:
    hypotheses: tuple
    verification: object
    manifest: object = None
    protocol: object = None

def investigate(triage_manifest, induce: bool = False) -> RankedHypotheses:
    hypotheses = generate_hypotheses(triage_manifest)
    verified = verify_hypotheses(hypotheses, induce=induce)
    # Structural verification is the real property: verified families have a
    # runnable AST check today; the rest remain lower-actionability candidates.
    families = verified.ast_verified_families
    ordered = tuple(sorted(hypotheses.hypotheses,
        key=lambda h: (not any(f.lower() in h.description.lower() for f in families), h.module_path, h.rank)))
    return RankedHypotheses(
        ordered,
        verified,
        hypotheses,
        mandatory_protocol(
            "bug_investigator",
            tuple(h.description for h in hypotheses.hypotheses),
            hypotheses.audited_modules,
            induction_reason="Module 3 verification executed; each unsupported family remains explicitly UNDETERMINED.",
        ),
    )
