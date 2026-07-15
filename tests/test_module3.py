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

def test_parser_known_handler_is_benign_but_generic_is_not(tmp_path):
    (tmp_path / "main.py").write_text("import json\ndef load(raw):\n    try:\n        return json.loads(raw)\n    except json.JSONDecodeError:\n        return None\n")
    result = verify_hypotheses(generate_hypotheses(triage(tmp_path)))
    assert result.ast_verified_families == ("subprocess", "parser", "float comparison", "eval/exec")
    assert not result.findings

def test_eval_literal_benign_and_variable_is_finding(tmp_path):
    (tmp_path / "main.py").write_text("def run(expr):\n    return eval(expr)\n")
    result = verify_hypotheses(generate_hypotheses(triage(tmp_path)))
    assert result.findings and "eval" in result.findings[0].description
    (tmp_path / "main.py").write_text("def run():\n    return eval('1 + 1')\n")
    result = verify_hypotheses(generate_hypotheses(triage(tmp_path)))
    assert not result.findings and result.discarded

def test_float_tolerance_is_benign_exact_float_remains_candidate(tmp_path):
    (tmp_path / "main.py").write_text("import math\ndef score(x):\n    return math.isclose(x, 1.0, abs_tol=0.01)\n")
    result = verify_hypotheses(generate_hypotheses(triage(tmp_path)))
    assert not result.findings
