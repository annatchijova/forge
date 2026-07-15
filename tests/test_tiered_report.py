import json
from forge.models import Evidence, Finding, VerificationManifest
from forge.sealing import write_sealed_manifest
from forge.tiered_report import render_tiered_report, rendered_finding_bytes

def test_all_tiers_preserve_identical_sealed_findings_and_outcomes(tmp_path):
    findings=(
        Finding("OBSERVED", "CODE FACT", "a.py", "credential observed", (Evidence("source", "a.py:1", "password = 'x'"),), "AST assignment check.", "security_auditor", "OBSERVED"),
        Finding("INFERRED", "PROTOCOL_GAP", "b.py", "boundary validation absent", (Evidence("source", "b.py:2", "json.loads(raw)"),), "Boundary contract applies.", "validate-at-the-boundary", "PROTOCOL_GAP"),
    )
    manifest=VerificationManifest("2.0", "0.1.0", "1.0", str(tmp_path), 0, findings, ())
    sealed=tmp_path/"verification-manifest.sealed.json"; write_sealed_manifest(manifest, sealed)
    outputs={mode: render_tiered_report(sealed, mode, tmp_path/f"{mode}.{'json' if mode == 'json' else 'html'}") for mode in ("summary", "standard", "extended", "json")}
    payloads={mode: rendered_finding_bytes(path, mode) for mode, path in outputs.items()}
    assert len(set(payloads.values())) == 1
    projected=[(item["category"], item.get("outcome", "OBSERVED")) for item in json.loads(next(iter(payloads.values())))]
    assert projected == [("OBSERVED", "OBSERVED"), ("INFERRED", "PROTOCOL_GAP")]
    assert "Discarded hypotheses" not in outputs["summary"].read_text()
    assert "Discarded hypotheses" in outputs["standard"].read_text()
    assert "Contract evaluations" in outputs["extended"].read_text()

def test_report_cli_renders_existing_sealed_artifact(tmp_path, monkeypatch, capsys):
    manifest=VerificationManifest("2.0", "0.1.0", "1.0", str(tmp_path), 0, (), ())
    sealed=tmp_path/"sealed.json"; write_sealed_manifest(manifest, sealed)
    from forge.cli import main
    monkeypatch.setattr("sys.argv", ["forge", "report", str(sealed), "--mode", "summary"])
    assert main() == 0
    assert capsys.readouterr().out.strip().endswith(".summary.html")
