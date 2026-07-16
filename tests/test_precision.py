import json

from forge.precision import run_precision


def test_golden_corpus_has_three_positive_and_negative_cases_per_agent():
    result = run_precision("tests/corpus")
    # integrity_inspector carries two extra cases beyond the base 3+3:
    # - negative-4: a machine_learning-domain module whose float() would
    #   otherwise trigger decision-adjacent-float (domain-aware suppression,
    #   no equivalent rule in security_auditor/web_auditor).
    # - positive-4 / negative-5: money-as-float (SQLite REAL money column
    #   and round()-over-division on a money-shaped name, with a Fraction-
    #   based negative counterpart) - a value can be float-typed without
    #   ever calling float(), so this is a separate detection path from
    #   decision-adjacent-float entirely.
    assert result["case_count"] == 21
    for agent in {row["agent"] for row in result["cases"]}:
        cases = [row for row in result["cases"] if row["agent"] == agent]
        expected_positives = 4 if agent == "integrity_inspector" else 3
        expected_negatives = 5 if agent == "integrity_inspector" else 3
        assert len([row for row in cases if row["expected_families"]]) == expected_positives
        assert len([row for row in cases if not row["expected_families"]]) == expected_negatives


def test_golden_corpus_baseline_is_exact():
    result = run_precision("tests/corpus")
    assert all(score["f1"] == 1.0 for score in result["by_family"].values()), json.dumps(result, indent=2)
