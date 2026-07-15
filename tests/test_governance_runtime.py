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
