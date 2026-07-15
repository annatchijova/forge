from forge.detector.stack import triage
from forge.hypotheses import generate_hypotheses
from forge.verification import verify_hypotheses
from forge.models import Hypothesis, HypothesesManifest

def test_ast_overrides_proximity_false_negative(tmp_path):
    (tmp_path / "main.py").write_text("import subprocess\ndef run(cmd):\n    try:\n        harmless = 1\n    except Exception:\n        harmless = 2\n    return subprocess.run(cmd)\n")
    manifest = HypothesesManifest("1.0", "0.1.0", "1.0", str(tmp_path), 0, (Hypothesis("main.py", 1, "subprocess.run call", (4,), "force failure"),), ("main.py",))
    result = verify_hypotheses(manifest)
    assert result.findings
    assert not result.discarded

def test_ast_discards_actually_enclosed_subprocess(tmp_path):
    (tmp_path / "main.py").write_text("import subprocess\ndef run():\n    try:\n        return subprocess.run(['trusted'], check=True)\n    except subprocess.SubprocessError as exc:\n        raise RuntimeError from exc\n")
    manifest = HypothesesManifest("1.0", "0.1.0", "1.0", str(tmp_path), 0, (Hypothesis("main.py", 1, "subprocess.run call", (4,), "force failure"),), ("main.py",))
    result = verify_hypotheses(manifest)
    assert not result.findings
    assert result.discarded
