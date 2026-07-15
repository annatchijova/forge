import json

from forge import Runtime
from forge.comparison import compare_runs


def test_compare_runs_reports_unchanged_and_new_findings(tmp_path):
    repo = tmp_path / "repo"
    repo.mkdir()
    (repo / "main.py").write_text("def run(value):\n    return eval(value)\n")
    first = tmp_path / "first"
    second = tmp_path / "second"
    Runtime().audit(repo, first)
    (repo / "security.py").write_text("password = 'real-secret'\n")
    Runtime().audit(repo, second)
    result = compare_runs(first, second)
    assert result["current_findings"] >= result["previous_findings"]
    assert "coverage_delta" in result
    assert len(result["unchanged"]) >= 1


def test_compare_runs_rejects_tampered_run(tmp_path):
    repo = tmp_path / "repo"
    repo.mkdir()
    (repo / "main.py").write_text("x = 1\n")
    run = tmp_path / "run"
    Runtime().audit(repo, run)
    sealed = run / "verification-manifest.sealed.json"
    data = json.loads(sealed.read_text())
    data["reported_chain_length"] = 99
    sealed.write_text(json.dumps(data))
    try:
        compare_runs(run, run)
    except ValueError as exc:
        assert "unverified" in str(exc)
    else:
        raise AssertionError("tampered runs must not be compared")
