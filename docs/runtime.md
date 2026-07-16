# Unified runtime and frontends

`forge.Runtime` is the single execution engine. It owns discovery, triage,
domain hypotheses, executable skill contracts, findings, sealing, and report
artifacts. The four supported frontends are thin adapters over this same
engine:

| Mode | Entry point | Use case |
|---|---|---|
| **Python API** | `from forge import Runtime` | Embed an audit in Python code or tests. |
| **CLI** | `python3 -m forge audit ...` | Run audits and render reports from a shell or CI job. |
| **Orchestrator** | `python3 -m forge.orchestrator ...` | Use the backward-compatible orchestration entry point. |
| **MCP** | `python3 -m forge.mcp_server` | Expose the same operations through MCP tools. |

CI is an invocation environment, not a fifth FORGE frontend: the CLI can run
inside CI, and CI configuration is only reported as a detected repository
stack when present.

```python
from forge import Runtime
result = Runtime().audit("/path/to/repository", "forge-run")
```

The fully automated CLI is:

```bash
python3 -m forge audit /path/to/repository -o forge-run --max-connected 100
```

Every audit produces an evidence package in the output directory:
`forge-report.html` (interactive), `report.md`, `repository-profile.json`,
`metrics.json`, `audit-trace.json`, `coverage-report.json`, and the sealed
verification manifest. JSON artifacts are the machine-readable source; HTML
and Markdown are presentation layers over those artifacts.

The visual package is generated automatically by the public reporting module:

```python
from forge import render_dashboard

paths = render_dashboard("forge-run")
```

This writes the main WOW-effect dashboard plus `summary`, `standard`, and
`extended` HTML tiers and the structured `json` mode. The four projections are
derived from the same sealed manifest, so presentation cannot silently change
the findings. A normal `Runtime().audit(...)` run invokes this renderer
automatically; no second reporting command is required.

## Large-repository demo mode

For a large repository, do one discovery-only preflight before the expensive
audit. It reports the connected-module count and checks the scope guard without
producing findings or changing the target repository:

```bash
python3 -m forge preflight /path/to/large-repository --max-connected 100 \
  > /tmp/forge-preflight.json
```

Then run the audit once, with artifacts outside the target repository and
compact stdout. `--summary` avoids printing every finding into a terminal,
chat transcript, or CI log; the complete evidence remains on disk:

```bash
python3 -m forge audit /path/to/large-repository \
  -o /tmp/forge-large-demo \
  --max-connected 100 \
  --summary > /tmp/forge-large-demo-summary.json
```

If preflight reports more connected modules than the selected limit, choose an
explicitly bounded higher limit before the one full run. Do not silently treat
the scope guard as full-repository coverage. For Git repositories, each
finding's HTML/Markdown evidence includes the source commit when `git blame`
is available; unavailable blame is labeled rather than inferred.

The discovery boundary is applied before detector reads. Dependency trees,
virtual environments, VCS metadata, caches, generated audit output, binaries,
and files larger than 5 MiB are excluded by policy and remain visible in
coverage as `excluded_by_policy`. This prevents prior reports or large
artifacts from becoming accidental audit input.

## Reproducible benchmark corpus

Place local repositories under a corpus directory and run:

```bash
python3 -m forge benchmark benchmarks/ -o benchmark-run/ --max-connected 100
```

FORGE audits each detected repository through the same `Runtime`, then writes
`benchmark.json` and `benchmark.html` with findings, discarded hypotheses,
coverage percentage, elapsed time, connected modules, and status. It does not
modify corpus repositories. The corpus can contain deterministic, parser,
web, ML, crypto, and legacy fixtures without special cases in the engine.

MCP exposes the same runtime through triage, domain inference, skill
listing/execution, audit, sealing, verification, and report tools.
`run_pipeline()` and `run_specialized_pipeline()` remain compatibility wrappers
around `Runtime.audit()` for Python callers and the orchestrator frontend.

## `forge.orchestrator.run_pipeline()` — the original 5-stage pipeline

The module-1-through-5 pipeline (triage → hypothesis generation →
adversarial verification → sealing → reporting) as one dependency-ordered
call chain. Runnable via `python3 -m forge.orchestrator`.

## `forge.orchestrator.run_specialized_pipeline()` — the automatic audit pipeline

Runs Archaeologist, Bug Investigator, Security Auditor and Integrity
Inspector, merges and seals their findings into a single `VerificationManifest`
(`schema_version="2.0"`), and renders one HTML report that also carries a
coverage breakdown. Called from Python today (`from forge.orchestrator import
run_specialized_pipeline`) and through `forge audit`/MCP via the unified
runtime.

Both entry points share a scope guard: they refuse to run downstream agents
when a repository has more `CONNECTED_ALIVE` modules than `--max-connected`
allows. The guard runs immediately after triage, so it bounds the rest of the
pipeline but not triage's own cost.

An MCP transport is available in `forge/mcp_server.py` — see
[`docs/mcp.md`](mcp.md) for the full tool list and Claude Code registration.
