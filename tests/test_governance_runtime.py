import json
from forge.detector.stack import triage
from forge.governance.runtime import load_skills, run_skills

def put(root, name, text):
    path=root/name; path.parent.mkdir(parents=True, exist_ok=True); path.write_text(text)

def test_validate_boundary_contract_emits_only_for_unguarded_live_boundary(tmp_path):
    put(tmp_path, "main.py", "import unsafe\nimport safe\n")
    put(tmp_path, "unsafe.py", "import json\ndef load(raw):\n    return json.loads(raw)\n")
    put(tmp_path, "safe.py", "import json\ndef load(raw):\n    if not isinstance(raw, str):\n        raise ValueError('raw must be text')\n    return json.loads(raw)\n")
    result=run_skills(triage(tmp_path))
    findings=[f for f in result.findings if f.agent == "validate-at-the-boundary"]
    assert [f.module_path for f in findings] == ["unsafe.py"]
    assert findings[0].outcome == "PROTOCOL_GAP"
    assert result.applicability["unsafe.py"]["validate-at-the-boundary"] == "APPLICABLE"

def test_runtime_loads_new_skill_plugin_without_core_change(tmp_path):
    plugin=tmp_path/"example"; plugin.mkdir()
    (plugin/"manifest.json").write_text(json.dumps({"name":"example-skill","version":"1.0","entrypoint":"contract.py","class_name":"ExampleSkill"}))
    (plugin/"contract.py").write_text("""from forge.models import Applicability, SkillContract\nclass ExampleSkill:\n    contract=SkillContract('example-skill','1.0',(),(),(),())\n    def applicability(self, context): return Applicability.APPLICABLE\n    def evaluate(self, context): return ()\n""")
    loaded=load_skills(tmp_path)
    assert len(loaded) == 1 and loaded[0].contract.name == "example-skill"
    repo=tmp_path/"repo"; repo.mkdir(); (repo/"main.py").write_text("x = 1\n")
    result=run_skills(triage(repo), tmp_path)
    assert result.applicability["main.py"]["example-skill"] == "APPLICABLE"

def test_run_skills_survives_a_skill_that_raises(tmp_path):
    plugin=tmp_path/"broken"; plugin.mkdir()
    (plugin/"manifest.json").write_text(json.dumps({"name":"broken-skill","version":"1.0","entrypoint":"contract.py","class_name":"BrokenSkill"}))
    (plugin/"contract.py").write_text(
        "from forge.models import SkillContract\n"
        "class BrokenSkill:\n"
        "    contract=SkillContract('broken-skill','1.0',(),(),(),())\n"
        "    def applicability(self, context): raise RuntimeError('boom')\n"
        "    def evaluate(self, context): return ()\n"
    )
    repo=tmp_path/"repo"; repo.mkdir(); (repo/"main.py").write_text("x = 1\n")
    # Must not raise: one broken skill must not take down the whole governance run.
    result=run_skills(triage(repo), tmp_path)
    assert result.applicability["main.py"]["broken-skill"] == "ERROR"
    assert any("broken-skill" in note and "boom" in note for note in result.limitations)

def test_a_skill_with_a_missing_entrypoint_is_visible_in_limitations_not_silently_dropped(tmp_path):
    plugin=tmp_path/"missing_entrypoint"; plugin.mkdir()
    (plugin/"manifest.json").write_text(json.dumps({"name":"ghost-skill","version":"1.0","entrypoint":"does_not_exist.py","class_name":"GhostSkill"}))
    failures: list[str] = []
    loaded=load_skills(tmp_path, failures=failures)
    assert loaded == ()
    assert any("does_not_exist.py" in note or "missing_entrypoint" in note for note in failures), failures
    repo=tmp_path/"repo"; repo.mkdir(); (repo/"main.py").write_text("x = 1\n")
    result=run_skills(triage(repo), tmp_path)
    assert result.applicability == {"main.py": {}}
    assert any("missing_entrypoint" in note or "does_not_exist.py" in note for note in result.limitations), result.limitations

def test_a_skill_with_invalid_manifest_json_is_visible_in_limitations(tmp_path):
    plugin=tmp_path/"broken_manifest"; plugin.mkdir()
    (plugin/"manifest.json").write_text("{not valid json")
    failures: list[str] = []
    loaded=load_skills(tmp_path, failures=failures)
    assert loaded == ()
    assert any("broken_manifest" in note for note in failures), failures
