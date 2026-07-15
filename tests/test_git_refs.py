import json
import subprocess

import pytest

from forge import Runtime
from forge.mcp_server import audit_ref, compare_refs


def git(repo, *args):
    return subprocess.run(["git", "-C", str(repo), *args], check=True, text=True,
                          stdout=subprocess.PIPE, stderr=subprocess.PIPE).stdout.strip()


def commit(repo, message):
    git(repo, "add", ".")
    git(repo, "commit", "-m", message)


def fixture_repo(tmp_path):
    repo = tmp_path / "repo"
    repo.mkdir()
    git(repo, "init", "-b", "main")
    git(repo, "config", "user.email", "forge-tests@example.invalid")
    git(repo, "config", "user.name", "FORGE tests")
    (repo / "main.py").write_text("import target\n")
    (repo / "target.py").write_text("password = 'old-secret'\n")
    commit(repo, "base credential")
    git(repo, "branch", "base")
    git(repo, "switch", "-c", "feature")
    (repo / "target.py").write_text("value = 1\n")
    (repo / "new.py").write_text("password = 'new-secret'\n")
    (repo / "main.py").write_text("import target\nimport new\n")
    commit(repo, "replace old credential with new one")
    git(repo, "switch", "main")
    return repo


def test_audit_ref_reads_committed_tree_without_mutating_repository(tmp_path):
    repo = fixture_repo(tmp_path)
    original_branch = git(repo, "rev-parse", "--abbrev-ref", "HEAD")
    original_status = git(repo, "status", "--short")

    result = Runtime().audit_ref(repo, "feature", tmp_path / "feature-audit")
    sealed = json.loads((tmp_path / "feature-audit" / "verification-manifest.sealed.json").read_text())
    events = sealed["audit_trace"]["events"]
    resolved = next(event for event in events if event["kind"] == "ref_resolved")

    assert result.findings == 1
    assert resolved["payload"]["ref"] == "feature"
    assert resolved["payload"]["commit"] == git(repo, "rev-parse", "feature")
    assert git(repo, "rev-parse", "--abbrev-ref", "HEAD") == original_branch
    assert git(repo, "status", "--short") == original_status == ""


def test_audit_ref_different_refs_produce_different_finding_sets(tmp_path):
    repo = fixture_repo(tmp_path)
    base = Runtime().audit_ref(repo, "base", tmp_path / "base-audit")
    feature = Runtime().audit_ref(repo, "feature", tmp_path / "feature-audit")

    assert [item.module_path for item in base.finding_records] == ["target.py"]
    assert [item.module_path for item in feature.finding_records] == ["new.py"]


def test_compare_refs_buckets_new_and_fixed_findings(tmp_path):
    repo = fixture_repo(tmp_path)
    result = Runtime().compare_refs(repo, "base", "feature", tmp_path / "comparison")

    assert result["base_commit"] == git(repo, "rev-parse", "base")
    assert result["head_commit"] == git(repo, "rev-parse", "feature")
    assert [item["module_path"] for item in result["new"]] == ["new.py"]
    assert [item["module_path"] for item in result["resolved"]] == ["target.py"]
    assert result["unchanged"] == []
    assert (tmp_path / "comparison" / "branch-comparison.json").exists()
    assert (tmp_path / "comparison" / "base" / "verification-manifest.sealed.json").exists()
    assert (tmp_path / "comparison" / "head" / "verification-manifest.sealed.json").exists()


def test_git_ref_mcp_errors_are_structured(tmp_path):
    repo = fixture_repo(tmp_path)
    result = audit_ref(str(repo), "does-not-exist", output_dir=str(tmp_path / "out"))
    assert result["ok"] is False
    assert result["error"]["code"] == "audit_ref_failed"
    assert "git ref not found" in result["error"]["message"]

