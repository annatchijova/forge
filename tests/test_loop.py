import json
import subprocess

from forge.loop import run_loop
from forge.loop_mcp import loop_audit


def git(repo, *args):
    return subprocess.run(["git", "-C", str(repo), *args], check=True,
                          text=True, stdout=subprocess.PIPE,
                          stderr=subprocess.PIPE).stdout.strip()


def fixture_repo(tmp_path):
    repo = tmp_path / "repo"
    repo.mkdir()
    git(repo, "init", "-b", "main")
    git(repo, "config", "user.email", "forge-tests@example.invalid")
    git(repo, "config", "user.name", "FORGE tests")
    (repo / "main.py").write_text("import security\n")
    (repo / "security.py").write_text("password = 'secret'\n")
    git(repo, "add", ".")
    git(repo, "commit", "-m", "finding")
    return repo


def safe_patch():
    return """diff --git a/security.py b/security.py
index 8a3e1e8..d9d7f4a 100644
--- a/security.py
+++ b/security.py
@@ -1 +1 @@
-password = 'secret'
+password = '<placeholder>'
"""


def test_credit_free_loop_reaudits_human_patch_and_converges(tmp_path):
    repo = fixture_repo(tmp_path)
    branch = git(repo, "rev-parse", "--abbrev-ref", "HEAD")
    status = git(repo, "status", "--short")
    result = run_loop(repo, "main", tmp_path / "loop", proposal_provider="human",
                      patches=[safe_patch()])

    assert result["status"] == "CONVERGED"
    assert result["iterations"][0]["tests"]["status"] == "NOT_REQUESTED"
    assert result["iterations"][0]["delta"]["resolved"]
    assert git(repo, "rev-parse", "--abbrev-ref", "HEAD") == branch
    assert git(repo, "status", "--short") == status == ""
    assert json.loads((tmp_path / "loop" / "loop-report.json").read_text())["authority"] == "FORGE"


def test_deterministic_mode_abstains_without_a_known_or_supplied_patch(tmp_path):
    repo = fixture_repo(tmp_path)
    result = run_loop(repo, "main", tmp_path / "loop")
    assert result["status"] == "ABSTAIN_NO_PROPOSAL"
    assert any(item["state"] == "ABSTAIN_NO_PROPOSAL" for item in result["trace"])


def test_llm_mode_is_explicitly_unavailable_and_does_not_fake_calls(tmp_path):
    repo = fixture_repo(tmp_path)
    result = run_loop(repo, "main", tmp_path / "loop", proposal_provider="llm")
    assert result["status"] == "ABSTAIN_PROVIDER_UNAVAILABLE"
    assert any("no LLM proposal adapter" in item.get("reason", "") for item in result["trace"])


def test_loop_mcp_returns_structured_result(tmp_path):
    repo = fixture_repo(tmp_path)
    result = loop_audit(str(repo), "main", proposal_provider="deterministic",
                        output_dir=str(tmp_path / "mcp-loop"))
    assert result["ok"] is True
    assert result["status"] == "ABSTAIN_NO_PROPOSAL"
