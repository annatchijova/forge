import pytest

from forge.agent_independence import AgentIndependenceError, validate_independent_results


ROLES = ("scope_triage", "python_security", "independent_reviewer")


def work(agent):
    return {
        "requested_role": agent,
        "work_product": {
            "observations": [f"{agent} observed source boundary"],
            "hypotheses": [f"{agent} hypothesis"],
            "deductions": [f"{agent} falsifier"],
            "evidence": [f"{agent}.json:1"],
            "decision": ["UNDETERMINED"],
        },
    }


def test_independence_requires_real_work_product_not_protocol_only():
    protocol_only = {role: {"requested_role": role, "adi": [], "skills": [], "scope": []} for role in ROLES}
    with pytest.raises(AgentIndependenceError, match="protocol only"):
        validate_independent_results(protocol_only, ROLES)


def test_independence_rejects_duplicate_work_products():
    records = {role: work(role) for role in ROLES}
    records["independent_reviewer"]["work_product"] = records["scope_triage"]["work_product"]
    with pytest.raises(AgentIndependenceError, match="duplicate"):
        validate_independent_results(records, ROLES)


def test_independence_accepts_distinct_evidence_backed_products():
    result = validate_independent_results({role: work(role) for role in ROLES}, ROLES)
    assert result["status"] == "INDEPENDENCE_VERIFIED"
    assert result["unique_work_products"] == len(ROLES)
