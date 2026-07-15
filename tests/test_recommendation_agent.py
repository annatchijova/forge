import json

from forge import Runtime


def test_recommendation_agent_is_optional_and_consumes_sealed_evidence(tmp_path):
    (tmp_path / "main.py").write_text("import security\n")
    (tmp_path / "security.py").write_text("password = 'synthetic-secret'\n")
    result = Runtime().audit(tmp_path, tmp_path / "out")

    recommendations = Runtime().recommend(result.artifacts["sealed"], result.artifacts["metrics"])
    assert len(recommendations) == 1
    recommendation = recommendations[0]
    assert recommendation.agent == "recommendation_agent"
    assert "secret" in recommendation.action.lower()
    assert recommendation.basis[1:] == ("security_auditor", "hardcoded-credential")


def test_recommendation_agent_does_not_run_during_normal_audit(tmp_path):
    (tmp_path / "main.py").write_text("x = 1\n")
    result = Runtime().audit(tmp_path, tmp_path / "out")
    sealed = json.loads(open(result.artifacts["sealed"]).read())
    assert not any(item.get("agent") == "recommendation_agent" for item in sealed["manifest"].get("findings", []))


def test_recommendation_agent_handles_audit_wording_for_serialization_and_parser_findings(tmp_path):
    sealed = {
        "chain": [
            {"hash": "h1", "finding": {"module_path": "a.py", "description": "unversioned serialization"}},
            {"hash": "h2", "finding": {"module_path": "b.py", "description": "The parser call `json.loads(raw)` has no nearby exception handling."}},
        ]
    }
    sealed_path = tmp_path / "sealed.json"
    sealed_path.write_text(json.dumps(sealed))

    recommendations = Runtime().recommend(sealed_path)

    assert len(recommendations) == 2
    assert any("schema_version" in item.action for item in recommendations)
    assert any("named input" in item.action for item in recommendations)
