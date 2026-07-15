"""Bounded reproducibility benchmark over a local corpus of repositories."""
from __future__ import annotations

import html
import json
import time
from pathlib import Path
from typing import Any

from forge.runtime import Runtime


_MARKERS = {".git", "pyproject.toml", "setup.py", "requirements.txt", "package.json", "Cargo.toml"}


def discover_repositories(corpus: str | Path) -> tuple[Path, ...]:
    root = Path(corpus).resolve()
    if not root.is_dir():
        raise ValueError(f"benchmark corpus is not a directory: {corpus}")
    marked = [path for path in root.rglob("*") if path.is_dir() and any((path / marker).exists() for marker in _MARKERS)]
    if marked:
        candidates = marked
    else:
        candidates = [path for path in root.rglob("*") if path.is_dir() and any(path.glob("*.py"))]
    selected = [path for path in candidates if not any(other != path and path in other.parents for other in candidates)]
    return tuple(sorted(selected, key=lambda path: str(path)))


def _slug(root: Path, repository: Path) -> str:
    return "-".join(repository.relative_to(root).parts).replace(" ", "-")


def _render_html(rows: list[dict[str, Any]], corpus: Path) -> str:
    body = "".join(
        f"<tr><td>{html.escape(row['repository'])}</td><td>{html.escape(str(row['findings']))}</td>"
        f"<td>{html.escape(str(row['discarded']))}</td><td>{html.escape(row['coverage'])}</td>"
        f"<td>{html.escape(str(row['seconds']))}</td><td>{html.escape(str(row['modules']))}</td>"
        f"<td>{html.escape(row['status'])}</td></tr>"
        for row in rows
    )
    return f"""<!doctype html><html lang=\"en\"><meta charset=\"utf-8\"><title>FORGE benchmark</title>
<style>body{{font:16px system-ui,sans-serif;max-width:1100px;margin:2rem auto;padding:0 1rem;color:#202124}}table{{border-collapse:collapse;width:100%}}th,td{{padding:.65rem;border-bottom:1px solid #ddd;text-align:left}}th{{background:#eef1ed;font:12px monospace;text-transform:uppercase}}.ok{{color:#176b3a}}.error{{color:#a33}}</style>
<h1>FORGE benchmark</h1><p>Corpus: <code>{html.escape(str(corpus))}</code></p>
<table><thead><tr><th>Repository</th><th>Findings</th><th>Discarded</th><th>Coverage</th><th>Time (s)</th><th>Modules</th><th>Status</th></tr></thead><tbody>{body}</tbody></table></html>"""


def run_benchmark(corpus: str | Path, output_dir: str | Path, max_connected: int = 100) -> dict[str, Any]:
    root = Path(corpus).resolve()
    output = Path(output_dir).resolve()
    output.mkdir(parents=True, exist_ok=True)
    repositories = discover_repositories(root)
    rows: list[dict[str, Any]] = []
    for repository in repositories:
        started = time.monotonic()
        run_output = output / _slug(root, repository)
        try:
            result = Runtime(max_connected=max_connected).audit(repository, run_output, max_connected=max_connected)
            ratio = result.coverage.get("coverage_ratio", {})
            denominator = ratio.get("denominator", 0)
            percent = (100 * ratio.get("numerator", 0) / denominator) if denominator else 0
            rows.append({"repository": str(repository.relative_to(root)), "findings": result.findings, "discarded": result.discarded, "coverage": f"{percent:.1f}%", "seconds": round(time.monotonic() - started, 3), "modules": result.connected_alive, "status": "OK", "output_dir": str(run_output)})
        except Exception as exc:  # one broken corpus entry must not hide the rest
            rows.append({"repository": str(repository.relative_to(root)), "findings": None, "discarded": None, "coverage": "n/a", "seconds": round(time.monotonic() - started, 3), "modules": None, "status": f"ERROR: {exc}", "output_dir": str(run_output)})
    payload = {"benchmark_schema_version": "1.0", "corpus": str(root), "repositories": rows}
    (output / "benchmark.json").write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    (output / "benchmark.html").write_text(_render_html(rows, root), encoding="utf-8")
    return payload
