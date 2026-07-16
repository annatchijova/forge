"""Optional Report Composer agent, preserving the established HTML renderer."""
from forge.report import render_report
from forge.agent_protocol import mandatory_protocol

def compose(triage_path, hypotheses_path, sealed_path, destination, coverage_path=None, metrics=None):
    return render_report(triage_path, hypotheses_path, sealed_path, destination, coverage_path, metrics)


def protocol(destination="report"):
    return mandatory_protocol(
        "report_composer",
        (f"report composition target: {destination}",),
        (),
        induction_reason="Report rendering is deterministic; reader interpretation and finding correctness remain separate questions.",
    )
