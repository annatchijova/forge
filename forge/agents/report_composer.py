"""Optional Report Composer agent, preserving the established HTML renderer."""
from forge.report import render_report

def compose(triage_path, hypotheses_path, sealed_path, destination, coverage_path=None, metrics=None):
    return render_report(triage_path, hypotheses_path, sealed_path, destination, coverage_path, metrics)
