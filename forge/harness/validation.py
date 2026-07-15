"""Stage 3: transparent held-in/held-out acceptance gate."""
from dataclasses import dataclass
import subprocess
@dataclass(frozen=True)
class ValidationRecord:
    proposal: object; delta_held_in: int; delta_held_out: int; accepted: bool; reason: str
def validate(proposal, held_in_before, held_in_after, held_out_before, held_out_after):
    di=held_in_after-held_in_before; do=held_out_after-held_out_before; accepted=di >= 0 and do >= 0 and max(di, do) > 0
    return ValidationRecord(proposal, di, do, accepted, "accepted by exact delta rule" if accepted else "rejected by exact delta rule")
def validate_many(proposals, measurements):
    return tuple(validate(p, *measurements[i]) for i,p in enumerate(proposals))

def run_held_out_suite(repo_root="."):
    """Run FORGE's actual regression suite and return its test count/status."""
    result = subprocess.run(["pytest", "-q"], cwd=repo_root, text=True, capture_output=True, check=False)
    return {"passed": result.returncode == 0, "output": result.stdout + result.stderr}
