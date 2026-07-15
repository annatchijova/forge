import json
from forge import Runtime
from forge.sealing import verify_sealed
from forge.models import ModelRouting
import pytest

def test_runtime_trace_is_embedded_sealed_and_tamper_evident(tmp_path):
    (tmp_path/"main.py").write_text("import security\n")
    (tmp_path/"security.py").write_text("password = 'synthetic-secret'\n")
    result=Runtime().audit(tmp_path, tmp_path/"out").to_dict()
    sealed_path=tmp_path/"out/verification-manifest.sealed.json"
    sealed=json.loads(sealed_path.read_text())
    trace=sealed["audit_trace"]
    assert "run_started" in [event["kind"] for event in trace["events"]]
    assert json.loads((tmp_path/"out/audit-trace.json").read_text()) == trace
    assert verify_sealed(sealed)["ok"]
    trace["events"][0]["payload"]["repository"] = "tampered"
    checked=verify_sealed(sealed)
    assert not checked["ok"] and "audit trace hash mismatch" in checked["issues"]

def test_failed_runtime_retains_partial_trace(tmp_path):
    (tmp_path/"main.py").write_text("x = 1\n")
    with pytest.raises(ValueError, match="scope guard"):
        Runtime(max_connected=0).audit(tmp_path, tmp_path/"failed")
    trace=json.loads((tmp_path/"failed/audit-trace.json").read_text())
    assert trace["events"][-1]["kind"] == "run_failed"


def test_model_routing_is_explicitly_recorded_without_faking_model_calls(tmp_path):
    (tmp_path / "main.py").write_text("x = 1\n")
    routing = ModelRouting("large-orchestrator", {
        "bug_investigator": "small-bug-model",
        "security_auditor": "small-security-model",
    })
    result = Runtime(model_routing=routing).audit(tmp_path, tmp_path / "out")
    trace = json.loads((tmp_path / "out/audit-trace.json").read_text())
    started = trace["events"][0]
    assert started["kind"] == "run_started"
    assert started["payload"]["model_routing"] == routing.to_dict()
    assert result.artifacts["trace"].endswith("audit-trace.json")
