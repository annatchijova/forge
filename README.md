# FORGE

![Python](https://img.shields.io/badge/python-3.10+-blue)
![Architecture](https://img.shields.io/badge/architecture-multi--agent-darkgreen)
![Deterministic](https://img.shields.io/badge/decision%20path-deterministic-success)
![Audit](https://img.shields.io/badge/audit-SHA--256%20sealed-brightgreen)
![License](https://img.shields.io/badge/license-Apache%202.0-blue)

> **Forensic Repository Governance Engine**
>
> A deterministic multi-agent system for repository governance, forensic
> software engineering, architectural archaeology, and evidence-driven code
> review.

---

## Why FORGE?

Modern AI coding assistants are excellent at producing code.

They are considerably less disciplined at explaining **why** something is a
defect, distinguishing evidence from speculation, documenting discarded
hypotheses, or proving what was actually inspected.

FORGE addresses that gap.

Rather than behaving like another autonomous coding agent, FORGE behaves like
a forensic engineering team:

* observes before concluding,
* generates competing hypotheses,
* actively attempts to falsify them,
* reports both findings and discarded explanations,
* seals the complete audit trail.

Model routing is explicit and shared by the CLI, MCP, and Python runtime. The
built-in detectors remain deterministic and do not invoke models yet; routing
is recorded in the audit trace so a future model-backed stage cannot hide its
provider choice:

```bash
python3 -m forge audit /path/to/repo \
  --orchestrator-model large-model \
  --agent-model bug_investigator=small-model \
  --agent-model security_auditor=small-model
```

The same configuration is available through `Runtime(model_routing=...)` and
the MCP `audit_repository` tool. An agent model name is configuration metadata
until that agent has a model-backed implementation; it is never presented as
evidence that a model was called.

For a full execution trace, enable the optional CRONOS runtime store:

```bash
python3 -m forge audit /path/to/repository \
  --output-dir forge-run \
  --cronos-db forge-run/cronos.sqlite3
```

The repository remains read-only. The SQLite database is an output artifact
owned by FORGE, not a file written into the audited repository unless the
caller explicitly chooses such an output location.

The objective is not simply finding more bugs.

The objective is producing findings that another engineer can independently
reproduce, challenge, or verify.

---

## Engineering philosophy

FORGE is built around one principle:

> **Engineering should optimize for correctness before confidence.**

Every repository audit follows the Peircean reasoning loop:

```
Observation
      │
      ▼
Abduction
(generate hypotheses)
      │
      ▼
Deduction
(design falsification tests)
      │
      ▼
Induction
(earn only bounded conclusions)
```

A plausible pattern is never promoted into a defect merely because it looks
convincing. Evidence remains separate from inference throughout the entire
pipeline: every finding carries an explicit epistemic level from the
red-team-auditing vocabulary — **CODE FACT** for a directly observed AST
match, **PLAUSIBLE HYPOTHESIS** for an unexecuted abduction, **CONFIRMED BY
INDUCTION** for a reproduced prediction, **FALSIFIED** for a refuted one —
and that level is never invented or conflated with the OBSERVED / INFERRED /
OPINION category field it sits next to.

---

## Multi-agent architecture

`forge.orchestrator.run_specialized_pipeline()` sequences six specialized,
single-responsibility agent modules. Five participate in the repository audit;
Patch Reviewer is deliberately kept outside that scan because it reviews a
proposed diff, not a whole repository. Report Composer renders the result but
does not invent findings.

```
                          Repository
                              │
                              ▼
                    ┌──────────────────┐
                    │  ARCHAEOLOGIST   │
                    │  triage + module │
                    │  classification  │
                    └──────────────────┘
                              │
              ┌───────────────┼────────────────┐
              ▼               ▼                ▼
   ┌────────────────┐ ┌───────────────┐ ┌────────────────────┐
   │ BUG INVESTIGATOR│ │SECURITY AUDITOR│ │INTEGRITY INSPECTOR │
   │ hypothesis gen. │ │ AST security   │ │ determinism +      │
   │ + AST-verified  │ │ pattern checks │ │ schema-versioning  │
   │ adversarial test│ │                │ │ checks             │
   └────────────────┘ └───────────────┘ └────────────────────┘
              │               │                │
              └───────────────┼────────────────┘
                              ▼
                    ┌──────────────────┐
                    │  merge + seal    │
                    │  SHA-256 chain   │
                    └──────────────────┘
                              │
                              ▼
                    ┌──────────────────┐
                    │ REPORT COMPOSER  │
                    │ HTML forensic    │
                    │ report           │
                    └──────────────────┘

   ┌─────────────────────────────────────────────────────┐
   │ PATCH REVIEWER — optional, evaluates a single diff   │
   │ against its stated intent. Not part of the repo scan.│
   └─────────────────────────────────────────────────────┘
```

Each agent has a strictly bounded responsibility. No agent silently changes
another agent's conclusions: findings are merged into one
`VerificationManifest`, sealed once, and rendered once.

---

## Two orchestrator entry points

## Unified runtime and frontends

`forge.Runtime` is the single execution engine. It owns discovery, triage,
domain hypotheses, executable skill contracts, findings, sealing, and report
artifacts. CLI, MCP, and Python callers are frontends over this same engine.

```python
from forge import Runtime
result = Runtime().audit("/path/to/repository", "forge-run")
```

The fully automated CLI is `python3 -m forge audit /path/to/repository -o
forge-run`. MCP exposes the same runtime through triage, domain inference,
skill listing/execution, audit, sealing, verification, and report tools.
`run_pipeline()` and `run_specialized_pipeline()` remain compatibility wrappers
around `Runtime.audit()`.

### `forge.orchestrator.run_pipeline()` — the original 5-stage pipeline

The module-1-through-5 pipeline (triage → hypothesis generation →
adversarial verification → sealing → reporting) as one dependency-ordered
call chain. Runnable via `python3 -m forge.orchestrator`.

### `forge.orchestrator.run_specialized_pipeline()` — the six-agent pipeline

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

An MCP transport is now available in `forge/mcp_server.py`. It exposes
`audit_repository`, `get_coverage`, `get_findings`, `verify_seal`, and the
standalone `review_patch` tool. It changes **how** FORGE is invoked, not
**how** FORGE reasons.

### Running the MCP server

With the Python MCP SDK installed, start the stdio server with:

```bash
python3 -m forge.mcp_server
```

### Running the optional CRONOS MCP server

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

### Agent status: no seventh agent yet

FORGE currently has exactly six agent modules:

| Agent | Automatic repository scan | Role |
|---|---:|---|
| Archaeologist | Yes | discovery, triage, deletion judgments |
| Bug Investigator | Yes | hypotheses and falsification |
| Security Auditor | Yes | AST security checks |
| Integrity Inspector | Yes | decision-path and serialization integrity |
| Report Composer | Yes, presentation only | HTML rendering |
| Patch Reviewer | No | review a requested unified diff |

There is **no seventh recommendation agent implemented**. Recommendations
will only be added after contextual domain hypotheses and executable skill
contracts are mature; they must not compensate for a rigid or misapplied
audit. The current model-routing options are configuration metadata only: the
built-in agents do not call an LLM yet.

## CRONOS as FORGE infrastructure

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

---

## The six agents

### Archaeologist (`forge/agents/archaeologist.py`)

Runs stack detection and module triage, then attaches a `deletion_judgments`
entry for every module classified `FOSSIL_HIGH_RISK` or `DEAD_WEIGHT`,
explaining in one sentence what deleting it would cost or save.

Classifies every module as `CONNECTED_ALIVE`, `FOSSIL_HIGH_RISK`,
`FOSSIL_LOW_RISK`, `DEAD_WEIGHT`, or `DUPLICATE`.

### Bug Investigator (`forge/agents/bug_investigator.py`)

Generates falsifiable hypotheses from live modules, then runs the module-3
adversarial verifier against them and ranks survivors by whether they fall
under an **AST-verified family** — a structural check that has an actual
implemented proof obligation, not just a keyword match:

* parser call without a real exception handler
* float comparison without `Decimal`/`Fraction`/`math.isclose`
* `eval`/`exec` on a non-constant argument
* `subprocess` call without a real `except` boundary

Anything outside those four families is capped at `PLAUSIBLE HYPOTHESIS` —
never promoted to a stronger claim without an executed check.

### Security Auditor (`forge/agents/security_auditor.py`)

Pure AST scanning, no network calls, no execution. Flags three families with
conservative, named benign criteria (see `DECISIONS.md`):

* **hardcoded-credential** — a non-empty, non-placeholder string literal
  assigned to a credential-shaped name, unless it comes from `os.getenv(...)`
* **unsafe-deserialization** — `pickle.load(s)`, `marshal.loads`, or
  `yaml.load` without `Loader=yaml.SafeLoader`
* **path-traversal** — a function parameter reaching `os.path.*` or `open()`
  without a visible `normpath`/`realpath` step first

### Integrity Inspector (`forge/agents/integrity_inspector.py`)

Also pure AST scanning. Flags two families:

* **decision-adjacent-float** — a `float(...)` call inside (or touching a
  variable named like) a function whose name or locals suggest a decision,
  score, verdict, classification, or gate
* **unversioned-serialization** — a `json`/`pickle` dump whose payload is not
  visibly a mapping containing `schema_version` or `version`

### Patch Reviewer (`forge/agents/patch_reviewer.py`)

Evaluates a unified diff against a stated intent: how much of the change sits
inside touched functions/classes versus outside any scope, and whether the
stated intent shows up in the names of the scopes it touched. Deliberately
excluded from the automatic repository scan — it reviews one proposed change,
not a whole tree.

### Report Composer (`forge/agents/report_composer.py`)

Wraps the self-contained HTML forensic report renderer: findings, discarded
hypotheses, clean modules, out-of-scope modules, a coverage table, and the
SHA-256 chain-of-custody block, all in one file with no external assets.

---

## Sealing

Every completed `run_specialized_pipeline()` and `run_pipeline()` call
canonically serializes its `VerificationManifest` and seals it into a
SHA-256, append-only, genesis-anchored hash chain
(`forge/sealing.py::seal_manifest`).

The seal proves that sealed findings were not altered after sealing. It does
**not** prove the findings are correct, and it does not defend against a
full-access attacker forging a consistent replacement chain from scratch —
`DECISIONS.md` documents that boundary explicitly so it is never presented as
a stronger guarantee than it is.

---

## Engineering discipline

FORGE keeps the engineering methodologies in `skills-gpt/` as shared source
material and is migrating them into executable, contextual skill contracts.
The runtime must not apply every skill as a universal policy: a module's
domain hypothesis determines applicability. At present,
`validate-at-the-boundary` is the complete executable reference plugin; the
remaining catalog is not represented as active checks merely because its
documentation exists.

**Core reasoning** — Abductive Engineering · Red-Team Auditing · Secure by
Construction · Software Archaeology · Diagnosing Bugs · Codebase Health
Assessment · Reverse Engineering · Daubert-Defensible Writing · Claim
Provenance Discipline

**Determinism & integrity** — Deterministic Core · LLM Out of the Loop ·
Tamper-Evident Audit Chain · Atomic State Mutation · Versioned Schema
Evolution

**Safe editing** — Surgical Patcher · Audit Before Patch

**Data integrity** — Validate at the Boundary · Honest Degradation · SQL
Aggregation over Materialization

**Process discipline** — Git Discipline

---

## Evidence before confidence

FORGE reports what was actually inspected, using the real field names that
`run_specialized_pipeline()` writes to `coverage-report.json` and the report's
Quality Metrics table — not a rounded PR-deck summary:

```
files_discovered ................. every file under the audited root
files_analyzed .................... .py files that parsed cleanly
files_skipped ...................... files_discovered - files_analyzed
skipped_reasons
  excluded_by_policy ............... under a SKIP_DIRS entry (e.g. .venv)
  binary_or_unreadable .............. not valid UTF-8 text
  syntax_error ....................... .py file that failed ast.parse
  non_python_not_analyzed ........... readable, not excluded, not .py

coverage_ratio ..................... files_analyzed / files_discovered

audited_modules .................... modules read for hypothesis generation
findings (surviving) ............... entries in the sealed chain
discarded hypotheses ................ ruled out, kept with their reason
clean modules ........................ audited, zero surviving findings
out of scope .......................... not CONNECTED_ALIVE this run

chain_integrity ...................... OK / BROKEN (+ issues)
```

Every discovered file lands in exactly one bucket — `files_analyzed` or one
`skipped_reasons` entry — never both, never neither. That arithmetic
invariant is enforced by an adversarial regression test
(`tests/test_specialized_pipeline.py`), not just asserted in prose.

---

## Design principles

* Deterministic decision path
* No hidden reasoning promotion
* Evidence precedes conclusions
* Hypotheses remain auditable
* `ABSTAIN` is a valid outcome
* Honest degradation over false certainty
* Canonical, typed serialization
* Bit-for-bit reproducibility of the seal
* Minimal, read-only repository interaction
* Security-first engineering

---

## What FORGE does not do

FORGE intentionally does **not**:

* rewrite repositories automatically — every agent is read-only against the
  audited repository
* invent severity or epistemic labels — `epistemic_level` is drawn from the
  red-team-auditing vocabulary and never conflated with the `category` field
* hide discarded hypotheses — they are rendered in the report with their
  discard reason, not silently dropped
* convert an AST pattern match into a claim about runtime behavior it did not
  observe
* claim cryptographic guarantees beyond its documented threat model — the
  seal is tamper-evident, not tamper-proof, and says so
* replace human engineering judgment

---

## Development

Run all commands (`pytest`, `python3 -m forge`, and Git operations) from the
repository root: `/home/labestiadevigia/forge`. Running from a parent
directory can pick up unrelated files and produce misleading test or audit
results. This happened during the Kimi audit verification step.

Agent role contracts live in [`agents/README.md`](agents/README.md).

## Vision

FORGE treats repository governance as an engineering discipline rather than a
prompt engineering exercise.

Its goal is not to generate convincing explanations.

Its goal is to produce findings that survive independent scrutiny.

## License

Licensed under the Apache License, Version 2.0. See [LICENSE](LICENSE) for
the full text and [NOTICE](NOTICE) for attribution.
