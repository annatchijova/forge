# CRONOS as FORGE infrastructure

CRONOS and FORGE answer two different questions, and neither substitutes for
the other:

* **CRONOS asks: what did the system do?** — the event-level trace of the
  runtime itself: which stage ran, in what order, what it read, what it
  decided to skip.
* **FORGE asks: what did the system find?** — the sealed findings, discarded
  hypotheses, and coverage that make up the actual audit result.

One audits the process; the other audits the software. FORGE's sealed
`audit-trace.json` is where they meet: it is CRONOS's answer, cryptographically
bound to FORGE's answer, so a verifier can confirm not just *that* findings
weren't altered, but *how the run that produced them actually proceeded*.

CRONOS is a private project owned by the FORGE maintainer and is not a user
dependency or a public repository requirement. We use its strongest ideas
inside FORGE's runtime rather than exposing CRONOS as an agent:

* event-level tracing while the audit executes, not post-hoc narration;
* structured objective, discovery, hypothesis, evidence, discard, finding,
  artifact, and completion events;
* quality and limitation accounting derived from observed events;
* exact Fraction-based values where a ratio or confidence-like quantity is
  meaningful;
* tamper-evident binding of the trace to FORGE's sealed findings artifact;
* preservation of a partial trace when the runtime fails.

The current native implementation is `forge/tracing.py` plus the sealed
`audit-trace.json` artifact. It is adapted to FORGE's repository-audit domain:
CRONOS concepts such as recalls, tool calls, hypotheses, evidence, decisions,
quality, contradictions, and chain verification map to FORGE stages and
findings. The runtime remains the single execution engine; CLI, MCP, and
Python API all consume it.

The next CRONOS-powered layer is not another detector. It is a forensic
runtime store and trace-quality subsystem that can support cross-run history,
quality/diversity/contradiction checks, atomic persistence, and richer audit
trail metrics without changing detector logic. Until that exists, FORGE makes
no claim of an external append-only CRONOS database: its trace is persisted as
JSON and cryptographically bound into the sealed artifact.

## Running the optional CRONOS MCP server

FORGE also vendors the private CRONOS runtime under `forge/cronos/`. Its MCP
surface is deliberately separate from the FORGE audit tools and is not started
by the normal server:

```bash
python3 -m forge.cronos_mcp_server
```

This optional server exposes CRONOS trace operations for an external agent.
The normal FORGE audit can use the same CRONOS implementation directly with
`Runtime(cronos_db=...)` or the MCP `audit_repository(..., cronos_db=...)` tool.
CRONOS records how FORGE executed; FORGE remains responsible for repository
discovery, governance skills, findings, sealing, and reports.
