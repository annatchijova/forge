import html
import json


def canonical_findings_bytes(findings):
    # "canonical_*" is the same naming convention as canonical_json - a
    # deterministic serialization primitive, versioned one layer up by
    # whatever payload embeds its output.
    return json.dumps(findings, sort_keys=True, separators=(",", ":")).encode("utf-8")


def render_coverage_section(coverage):
    # Presentation: a JSON dump escaped for embedding as readable text in an
    # HTML report, never a persisted artifact needing its own version key.
    return "<pre>" + html.escape(json.dumps(coverage, indent=2, sort_keys=True)) + "</pre>"
