import subprocess
from fractions import Fraction

def test_stack_confidence_is_exact_fraction(tmp_path):
    from forge.detector.stack import detect_stack
    (tmp_path / "a.py").write_text("x = 1\n")
    stack = detect_stack(tmp_path)[0]
    assert stack.confidence == Fraction(55, 100)

def test_git_blame_timeout_degrades_honestly(monkeypatch):
    from forge.report import _blame
    def timeout(*args, **kwargs):
        raise subprocess.TimeoutExpired(args[0], 30)
    monkeypatch.setattr(subprocess, "check_output", timeout)
    assert "timed out" in _blame(".", "missing.py", 1)

def test_held_out_timeout_degrades_honestly(monkeypatch):
    from forge.harness import validation
    def timeout(*args, **kwargs):
        raise subprocess.TimeoutExpired(args[0], 120)
    monkeypatch.setattr(validation.subprocess, "run", timeout)
    result = validation.run_held_out_suite()
    assert result["passed"] is False and result["timed_out"] is True
