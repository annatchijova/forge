import json

from forge.multi_agent import build_canonical_findings
from forge.sealing import seal_findings, verify_sealed


def test_canonical_findings_preserve_external_and_native_layers():
    records = build_canonical_findings([{"id": "H1", "statement": "external"}], [{"agent": "web_auditor", "description": "native"}])
    assert [item["source_layer"] for item in records] == ["codex_external", "forge_native"]
    assert records[0]["record_id"] == "codex_external:H1"


def test_canonical_finding_set_can_be_sealed_and_verified():
    records = build_canonical_findings([{"id": "H1", "statement": "external"}], [])
    sealed = seal_findings(records, {"finding_set_digest": "test"})
    assert verify_sealed(sealed)["ok"]
    assert sealed["chain"][0]["finding"]["source_layer"] == "codex_external"
