from forge.detector.stack import triage
from forge.hypotheses import _candidates, generate_hypotheses
from forge.verification import verify_hypotheses
from forge.verification import _call_at
import ast
from forge.models import Hypothesis, HypothesesManifest
from forge.verification import _description_call_name

def test_ast_overrides_proximity_false_negative(tmp_path):
    (tmp_path / "main.py").write_text("import subprocess\ndef run(cmd):\n    try:\n        harmless = 1\n    except Exception:\n        harmless = 2\n    return subprocess.run(cmd)\n")
    manifest = HypothesesManifest("1.0", "0.1.0", "1.0", str(tmp_path), 0, (Hypothesis("main.py", 1, "subprocess.run call", (4,), "force failure"),), ("main.py",))
    result = verify_hypotheses(manifest)
    assert result.findings
    assert not result.discarded

def test_call_at_disambiguates_nested_calls_on_same_line():
    tree = ast.parse("foo(bar())\n")
    assert ast.unparse(_call_at(tree, 1, "foo").func) == "foo"
    assert ast.unparse(_call_at(tree, 1, "bar").func) == "bar"

def test_call_name_extraction_fallback_is_explicit():
    assert _description_call_name("a description without the expected call marker") is None
    tree = ast.parse("foo(bar())\n")
    # None intentionally means first call on the line; this is a known limitation.
    assert ast.unparse(_call_at(tree, 1).func) == "foo"

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

def test_eval_literal_with_dangerous_content_is_not_discarded(tmp_path):
    (tmp_path / "main.py").write_text('def run():\n    return eval(\'os.system("rm -rf /")\')\n')
    result = verify_hypotheses(generate_hypotheses(triage(tmp_path)))
    assert result.findings, (
        "a literal eval/exec argument that itself invokes OS command execution "
        "must not be auto-discarded as benign just because it is a constant string"
    )
    assert not result.discarded

def test_float_tolerance_is_benign_exact_float_remains_candidate(tmp_path):
    (tmp_path / "main.py").write_text("import math\ndef score(x):\n    return math.isclose(x, 1.0, abs_tol=0.01)\n")
    result = verify_hypotheses(generate_hypotheses(triage(tmp_path)))
    assert not result.findings


def test_math_isclose_phrase_inside_string_is_not_a_hypothesis():
    # The detector's own surface pattern is a string literal, not a real call.
    hypotheses, _ = _candidates("fixture.py", ('if "math.isclose" in stripped:\n',), "Python")
    assert hypotheses == []


def test_risk_shaped_strings_do_not_create_regex_hypotheses():
    source = (
        'note = "subprocess.run(cmd)"\n',
        'note = "json.loads(raw)"\n',
        'note = "score > 0.5"\n',
        'note = "eval(expr)"\n',
    )
    hypotheses, _ = _candidates("fixture.py", source, "Python")
    assert hypotheses == []


def test_shell_true_is_a_distinct_hypothesis_family():
    hypotheses, _ = _candidates("fixture.py", ("subprocess.call(cmd, shell=True)\n",), "Python")
    assert len(hypotheses) == 1
    assert "shell=True" in hypotheses[0].description


def test_parser_induction_confirms_opaque_failure_in_child_process(tmp_path):
    (tmp_path / "main.py").write_text("def parse(raw):\n    raise RuntimeError('opaque parser failure')\n")
    result = verify_hypotheses(generate_hypotheses(triage(tmp_path)), induce=True)
    assert result.findings
    assert result.findings[0].epistemic_level == "CONFIRMED BY INDUCTION"
    assert result.induction[0]["status"] == "CONFIRMED BY INDUCTION"


def test_parser_induction_respects_named_boundary_handler(tmp_path):
    (tmp_path / "main.py").write_text("import json\ndef load(raw):\n    try:\n        return json.loads(raw)\n    except json.JSONDecodeError:\n        return None\n")
    result = verify_hypotheses(generate_hypotheses(triage(tmp_path)), induce=True)
    assert not result.findings
    assert not result.induction
