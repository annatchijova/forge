"""Bug Investigator: hypothesis generation plus evidence-based actionability."""
from dataclasses import dataclass
from forge.hypotheses import generate_hypotheses
from forge.verification import verify_hypotheses

@dataclass(frozen=True)
class RankedHypotheses:
    hypotheses: tuple
    verification: object
    manifest: object = None

def investigate(triage_manifest) -> RankedHypotheses:
    hypotheses = generate_hypotheses(triage_manifest)
    verified = verify_hypotheses(hypotheses)
    # Structural verification is the real property: verified families have a
    # runnable AST check today; the rest remain lower-actionability candidates.
    families = verified.ast_verified_families
    ordered = tuple(sorted(hypotheses.hypotheses,
        key=lambda h: (not any(f.lower() in h.description.lower() for f in families), h.module_path, h.rank)))
    return RankedHypotheses(ordered, verified, hypotheses)
