import json
from fractions import Fraction

from forge.orchestrator import run_specialized_pipeline

def put(root, name, text):
    path = root / name
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text)

def test_specialized_pipeline_merges_seals_and_attributes_all_agents(tmp_path):
    put(tmp_path, "main.py", "import bad\nimport security\nimport integrity\n")
    put(tmp_path, "bad.py", "import subprocess\ndef run(cmd):\n    return subprocess.run(cmd)\n")
    put(tmp_path, "security.py", "password = 'real-secret'\nimport pickle\npickle.loads(raw)\n")
    put(tmp_path, "integrity.py", "import json\ndef score(decision):\n    value = float(decision)\n    json.dump({'score': value}, out)\n")
    result = run_specialized_pipeline(tmp_path, tmp_path / "out")
    sealed = json.loads((tmp_path / "out/verification-manifest.sealed.json").read_text())
    agents = {entry["finding"]["agent"] for entry in sealed["chain"]}
    assert {"bug_investigator", "security_auditor", "integrity_inspector"} <= agents
    assert json.loads((tmp_path / "out/verification-manifest.sealed.json").read_text())
    report = (tmp_path / "out/forge-report.html").read_text()
    assert "Coverage" in report and "security_auditor" in report and "integrity_inspector" in report
    assert result["coverage"]["coverage_ratio"] == {"numerator": 1, "denominator": 1}

def test_coverage_surfaces_policy_exclusions(tmp_path):
    put(tmp_path, "main.py", "x = 1\n")
    put(tmp_path, ".venv/lib/hidden.py", "password = 'never-scanned'\n")
    result = run_specialized_pipeline(tmp_path, tmp_path / "out")
    coverage = result["coverage"]
    assert ".venv/lib/hidden.py" in coverage["skipped_reasons"]["excluded_by_policy"]
    assert coverage["files_skipped"] >= 1

def test_coverage_counts_syntax_errors(tmp_path):
    put(tmp_path, "main.py", "x = 1\n")
    put(tmp_path, "broken.py", "def broken(:\n")
    result = run_specialized_pipeline(tmp_path, tmp_path / "out")
    coverage = result["coverage"]
    assert "broken.py" in coverage["skipped_reasons"]["syntax_error"]
    assert coverage["files_analyzed"] == 1
    assert Fraction(coverage["coverage_ratio"]["numerator"], coverage["coverage_ratio"]["denominator"]) == Fraction(1, 2)

def test_ast_structural_agents_use_red_team_auditing_epistemic_vocabulary(tmp_path):
    put(tmp_path, "main.py", "import security\nimport integrity\n")
    put(tmp_path, "security.py", "password = 'real-secret'\n")
    put(tmp_path, "integrity.py", "def score(decision):\n    value = float(decision)\n    return value\n")
    result = run_specialized_pipeline(tmp_path, tmp_path / "out")
    sealed = json.loads((tmp_path / "out/verification-manifest.sealed.json").read_text())
    valid_levels = {"CODE FACT", "PLAUSIBLE HYPOTHESIS", "CONFIRMED BY INDUCTION", "FALSIFIED"}
    ast_agent_findings = [
        entry["finding"] for entry in sealed["chain"]
        if entry["finding"]["agent"] in {"security_auditor", "integrity_inspector"}
    ]
    assert ast_agent_findings, "fixture must produce at least one AST-structural finding to exercise the assertion"
    for finding in ast_agent_findings:
        assert finding["epistemic_level"] in valid_levels, (
            f"{finding['agent']} used epistemic_level={finding['epistemic_level']!r}, "
            f"which is not in the red-team-auditing vocabulary {valid_levels} "
            "(it must not reuse the category field's own value, e.g. 'OBSERVED')"
        )
        assert finding["epistemic_level"] != finding["category"], (
            "epistemic_level must not conflate with the category field (OBSERVED/INFERRED/OPINION)"
        )

def test_coverage_accounting_never_loses_readable_non_python_files(tmp_path):
    put(tmp_path, "main.py", "x = 1\n")
    put(tmp_path, "README.md", "# not python, but readable text\n")
    result = run_specialized_pipeline(tmp_path, tmp_path / "out")
    coverage = result["coverage"]
    accounted_for = coverage["files_analyzed"] + sum(len(v) for v in coverage["skipped_reasons"].values())
    assert coverage["files_discovered"] == accounted_for, (
        "every discovered file must land in exactly one bucket: analyzed or a skipped_reasons category"
    )
    assert "README.md" in coverage["skipped_reasons"].get("non_python_not_analyzed", ())
