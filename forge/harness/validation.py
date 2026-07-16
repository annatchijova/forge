"""Stage 3: transparent held-in/held-out acceptance gate."""
from dataclasses import dataclass
import subprocess

from forge.precision import run_precision
@dataclass(frozen=True)
class ValidationRecord:
    proposal: object; delta_held_in: int; delta_held_out: int; accepted: bool; reason: str
def validate(proposal, held_in_before, held_in_after, held_out_before, held_out_after):
    di=held_in_after-held_in_before; do=held_out_after-held_out_before; accepted=di >= 0 and do >= 0 and max(di, do) > 0
    return ValidationRecord(proposal, di, do, accepted, "accepted by exact delta rule" if accepted else "rejected by exact delta rule")
def validate_many(proposals, measurements):
    return tuple(validate(p, *measurements[i]) for i,p in enumerate(proposals))

def run_held_out_suite(repo_root="."):
    """Run the red-team gate first, then the complete regression suite.

    A green general suite is not sufficient if the adversarial contract was
    skipped or filtered. Red-team failure is therefore fail-closed and stops
    the held-out acceptance run before it can report success.
    """
    try:
        red_team = subprocess.run(
            ["pytest", "-q", "tests/test_red_team_adversarial.py"],
            cwd=repo_root, text=True, capture_output=True, check=False, timeout=120,
        )
        red_output = red_team.stdout + red_team.stderr
        if red_team.returncode != 0:
            return {"passed": False, "stage": "red_team", "red_team_passed": False, "output": red_output}
        result = subprocess.run(["pytest", "-q"], cwd=repo_root, text=True, capture_output=True, check=False, timeout=120)
        return {"passed": result.returncode == 0, "stage": "full_suite", "red_team_passed": True, "output": red_output + result.stdout + result.stderr}
    except subprocess.TimeoutExpired as exc:
        return {"passed": False, "timed_out": True, "stage": "red_team_or_full_suite", "output": "held-out pytest suite timed out after 120 seconds; validation did not complete."}


def run_held_in_gate(corpus="tests/corpus", min_f1=1.0):
    """Measure a proposed rule change against the labelled golden corpus.

    This is the held-in half of the acceptance gate: does the change hold on
    the fixtures we already have adjudicated labels for? `run_held_out_suite`
    is the complementary held-out half (the general regression + red-team
    suite, which the corpus does not cover). Neither substitutes for the
    other: held-in can regress a labelled family while the general suite
    stays green, and held-out can break unrelated behaviour the corpus never
    exercised.
    """
    result = run_precision(corpus)
    below = {family: score["f1"] for family, score in result["by_family"].items() if score["f1"] < min_f1}
    return {"passed": not below, "stage": "held_in_corpus", "by_family": result["by_family"], "below_threshold": below}
