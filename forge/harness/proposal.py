"""Stage 2: deterministic proposals anchored to editable FORGE surfaces."""
from dataclasses import dataclass
from .mining import WeaknessBundle
@dataclass(frozen=True)
class HarnessProposal:
    mechanism: str; target_file: str; target_function: str; change: str; regression_risk: str
def propose(bundle: WeaknessBundle, configuration=None):
    out=[]
    for c in bundle.clusters:
        text=" ".join(c.signature).lower()
        if "comment" in text:
            out.append(HarnessProposal(c.signature[2], "forge/hypotheses.py", "_candidates", "apply _code_before_comment() to each detector line before pattern matching", "Could suppress a true positive whose syntax intentionally follows a comment marker."))
        elif "string literal" in text or "keyword" in text:
            out.append(HarnessProposal(c.signature[2], "forge/hypotheses.py", "_candidates", "add an ast.Constant string-literal exclusion check", "Could suppress a real finding expressed through a literal constructed at runtime."))
        elif c.frequency >= 2:
            out.append(HarnessProposal(c.signature[2], "forge/forge/agents/", c.family or "family checker", "narrow this family's trigger condition; human review required", "Narrowing can suppress true positives previously caught."))
    return tuple(out)
