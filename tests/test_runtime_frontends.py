import json
from forge import Runtime
from forge.cli import main as cli_main
from forge.mcp_server import audit_repository
from forge.orchestrator import run_specialized_pipeline

def put(root, name, text):
    path=root/name; path.parent.mkdir(parents=True, exist_ok=True); path.write_text(text)

def canonical(records):
    return json.dumps(records, sort_keys=True, separators=(",", ":"))

def test_python_api_cli_and_mcp_use_equivalent_runtime_findings(tmp_path, monkeypatch, capsys):
    put(tmp_path, "main.py", "import security\n")
    put(tmp_path, "security.py", "password = 'synthetic-secret'\n")
    api = Runtime().audit(tmp_path, tmp_path/"api-out").to_dict()
    wrapper = run_specialized_pipeline(tmp_path, tmp_path/"wrapper-out")
    monkeypatch.setattr("sys.argv", ["forge", "audit", str(tmp_path), "--output-dir", str(tmp_path/"cli-out")])
    assert cli_main() == 0
    cli=json.loads(capsys.readouterr().out)
    mcp=audit_repository(str(tmp_path), output_dir=str(tmp_path/"mcp-out"))
    assert len({canonical(item["finding_records"]) for item in (api, wrapper, cli, mcp)}) == 1
    assert api["connected_alive"] == wrapper["connected_alive"] == cli["connected_alive"] == mcp["connected_alive"]

def test_mcp_interactive_operations_delegate_to_runtime(tmp_path):
    put(tmp_path, "main.py", "import json\n")
    put(tmp_path, "loader.py", "import json\ndef load(raw):\n    return json.loads(raw)\n")
    from forge.mcp_server import infer_module_domains, list_available_skills, repository_summary, run_skill, triage_repository
    assert triage_repository(str(tmp_path))["ok"]
    assert infer_module_domains(str(tmp_path))["ok"]
    assert repository_summary(str(tmp_path))["ok"]
    assert list_available_skills()["skills"][0]["name"] == "validate-at-the-boundary"
    assert run_skill(str(tmp_path), "validate-at-the-boundary")["ok"]
