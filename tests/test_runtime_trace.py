import json
import sqlite3
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


def test_runtime_trace_records_phase_timings_and_peak_rss(tmp_path):
    (tmp_path / "main.py").write_text("x = 1\n")
    result = Runtime().audit(tmp_path, tmp_path / "out")
    trace = json.loads((tmp_path / "out" / "audit-trace.json").read_text())
    started = {event["payload"]["phase"] for event in trace["events"] if event["kind"] == "phase_started"}
    completed = {event["payload"]["phase"] for event in trace["events"] if event["kind"] == "phase_completed"}
    assert {"discovery", "triage", "coverage", "canonicalization"} <= started
    assert started == completed
    metrics = json.loads((tmp_path / "out" / "metrics.json").read_text())
    assert metrics["runtime"]["phases"]["triage"]["status"] == "COMPLETED"
    assert "peak_rss_bytes" in metrics["runtime"]


def test_cronos_trace_store_is_optional_and_records_the_runtime(tmp_path):
    (tmp_path / "main.py").write_text("x = 1\n")
    database = tmp_path.parent / f"{tmp_path.name}-cronos.sqlite3"
    result = Runtime(cronos_db=database).audit(tmp_path, tmp_path / "out")

    assert result.artifacts["cronos_db"] == str(database)
    connection = sqlite3.connect(database)
    assert connection.execute("SELECT COUNT(*) FROM traces").fetchone()[0] == 1
    assert connection.execute("SELECT COUNT(*) FROM trace_steps").fetchone()[0] >= 2
    assert connection.execute("SELECT COUNT(*) FROM trace_chain").fetchone()[0] == 1
    connection.close()


def test_cronos_and_output_parent_dirs_are_created_before_audit(tmp_path):
    repo = tmp_path / "repo"
    repo.mkdir()
    (repo / "main.py").write_text("x = 1\n")
    output = tmp_path / "fresh-run" / "nested-output"
    database = output / "cronos.sqlite3"

    result = Runtime(cronos_db=database).audit(repo, output)

    assert output.is_dir()
    assert database.is_file()
    assert result.artifacts["cronos_db"] == str(database)


def test_cronos_persists_open_steps_before_context_exit(tmp_path):
    from forge.cronos import CronosTracer, TraceStore

    database = tmp_path / "incremental.sqlite3"
    store = TraceStore(str(database))
    tracer = CronosTracer(store, "agent", "", "", "incremental test")
    tracer.__enter__()
    tracer.call_tool("fixture", "step persisted before close")

    connection = sqlite3.connect(database)
    row = connection.execute(
        "SELECT closed_at, chain_ok FROM traces WHERE trace_id = ?", (tracer.trace.trace_id,)
    ).fetchone()
    steps = connection.execute(
        "SELECT kind, payload FROM trace_steps WHERE trace_id = ? ORDER BY seq", (tracer.trace.trace_id,)
    ).fetchall()
    connection.close()
    store._conn.close()

    assert row == (None, 0)
    assert [item[0] for item in steps] == ["objective", "tool"]
    assert "step persisted before close" in steps[1][1]


def test_cronos_store_cannot_write_inside_the_audited_repository(tmp_path):
    (tmp_path / "main.py").write_text("x = 1\n")
    with pytest.raises(ValueError, match="outside the audited repository"):
        Runtime(cronos_db=tmp_path / "cronos.sqlite3").audit(tmp_path, tmp_path / "out")


def test_seal_results_requires_a_forge_source_attestation(tmp_path):
    (tmp_path / "main.py").write_text("x = 1\n")
    result = Runtime().audit(tmp_path, tmp_path / "out")
    verification = tmp_path / "out" / "verification-manifest.json"
    sealed = Runtime().seal_results(verification, tmp_path / "res ealed.json")
    assert sealed.exists()

    fabricated = json.loads(verification.read_text())
    fabricated.pop("source_attestation", None)
    fake = tmp_path / "fake.json"
    fake.write_text(json.dumps(fabricated))
    with pytest.raises(ValueError, match="source attestation"):
        Runtime().seal_results(fake, tmp_path / "fake.sealed.json")


def test_seal_results_rejects_manifest_tampered_after_audit(tmp_path):
    (tmp_path / "main.py").write_text("x = 1\n")
    Runtime().audit(tmp_path, tmp_path / "out")
    verification = tmp_path / "out" / "verification-manifest.json"
    data = json.loads(verification.read_text())
    data["root"] = "/fabricated"
    verification.write_text(json.dumps(data))
    with pytest.raises(ValueError, match="source attestation"):
        Runtime().seal_results(verification, tmp_path / "tampered.sealed.json")
