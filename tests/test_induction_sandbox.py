import json

from forge import Runtime


def test_runtime_can_disable_target_induction(tmp_path):
    (tmp_path / "main.py").write_text("import json\ndef load(raw):\n    return json.loads(raw)\n")
    result = Runtime(induction=False).audit(tmp_path, tmp_path / "out")
    verification = json.loads((tmp_path / "out" / "verification-manifest.json").read_text())
    assert verification["induction"] == []
    assert any(item["epistemic_level"] == "PLAUSIBLE HYPOTHESIS" for item in verification["findings"])
