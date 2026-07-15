from pathlib import Path

import pytest

from forge.orchestrator import run_pipeline


def test_orchestrator_runs_bounded_pipeline(tmp_path: Path):
    repo = tmp_path / "repo"
    repo.mkdir()
    (repo / "main.py").write_text("def greet():\n    return 'hello'\n")
    result = run_pipeline(repo, tmp_path / "out")
    assert result["connected_alive"] == 1
    assert result["findings"] == 0
    assert (tmp_path / "out" / "forge-report.html").exists()


def test_orchestrator_scope_guard_stops_broad_runs(tmp_path: Path):
    repo = tmp_path / "repo"
    repo.mkdir()
    (repo / "main.py").write_text("from a import x\n")
    (repo / "a.py").write_text("def x(): return 1\n")
    with pytest.raises(ValueError, match="scope guard"):
        run_pipeline(repo, tmp_path / "out", max_connected=0)
