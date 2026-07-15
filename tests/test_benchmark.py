import json

from forge.benchmark import discover_repositories, run_benchmark


def test_benchmark_discovers_and_summarizes_multiple_repositories(tmp_path):
    corpus = tmp_path / "benchmarks"
    first = corpus / "parser" / "demo-one"
    second = corpus / "legacy" / "demo-two"
    first.mkdir(parents=True)
    second.mkdir(parents=True)
    (first / "main.py").write_text("x = 1\n")
    (second / "main.py").write_text("def run(value):\n    return eval(value)\n")

    assert discover_repositories(corpus) == tuple(sorted((first.resolve(), second.resolve()), key=str))
    payload = run_benchmark(corpus, tmp_path / "results")
    assert len(payload["repositories"]) == 2
    assert {row["status"] for row in payload["repositories"]} == {"OK"}
    assert (tmp_path / "results" / "benchmark.json").exists()
    assert (tmp_path / "results" / "benchmark.html").exists()
    assert json.loads((tmp_path / "results" / "benchmark.json").read_text())["benchmark_schema_version"] == "1.0"
