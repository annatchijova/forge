import json

from forge.precision import run_precision


def test_golden_corpus_has_three_positive_and_negative_cases_per_agent():
    result = run_precision("tests/corpus")
    assert result["case_count"] == 18
    for agent in {row["agent"] for row in result["cases"]}:
        cases = [row for row in result["cases"] if row["agent"] == agent]
        assert len([row for row in cases if row["expected_families"]]) == 3
        assert len([row for row in cases if not row["expected_families"]]) == 3


def test_golden_corpus_baseline_is_exact():
    result = run_precision("tests/corpus")
    assert all(score["f1"] == 1.0 for score in result["by_family"].values()), json.dumps(result, indent=2)
