"""Archaeologist agent: the existing triage assessment plus deletion judgments."""
from forge.detector.stack import triage
from forge.models import TriageManifest

def assess(root: str) -> TriageManifest:
    manifest = triage(root)
    judgments = dict(manifest.deletion_judgments)
    for module in manifest.modules:
        if module.module_class.value in {"FOSSIL_HIGH_RISK", "DEAD_WEIGHT"}:
            judgments[module.path] = (
                "deleting would concentrate complexity elsewhere"
                if module.caller_count or module.import_count
                else "deleting would remove unreachable code"
            )
    # Preserve the established manifest contract while exposing the new output.
    from dataclasses import replace
    return replace(manifest, deletion_judgments=judgments)

archaeologize = assess
