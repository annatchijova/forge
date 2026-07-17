# Governance skills

FORGE keeps the engineering methodologies in `skills-gpt/` as shared source
material and is migrating them into executable, contextual skill contracts.
The runtime must not apply every skill as a universal policy: a module's
domain hypothesis determines applicability. At present,
`validate-at-the-boundary` remains the reference plugin. Five additional
Class-A obligations are executable as of 2026-07-17: `honest-degradation`,
`deterministic-core`, `atomic-state-mutation`,
`sql-aggregation-not-materialization`, and `tamper-evident-audit-chain`.
Markdown is not treated as execution evidence: every plugin has an explicit
manifest, `applicability()` and `evaluate()` contract, and a positive and
negative precision-corpus case.

A governance skill is not a hardcoded `if float(): finding` check bolted onto
the core. It is a pipeline stage:

```
module
   │
   ▼
domain hypothesis            (infer_domains: machine_learning /
   │                          input_boundary / cryptographic /
   │                          persistence / audit-ledger / determinism, or none)
   ▼
applicable contracts         (each skill's own applicability() decides
   │                          APPLICABLE / NOT_APPLICABLE / UNDETERMINED)
   ▼
executable checks            (each applicable skill's evaluate())
   │
   ▼
findings
```

## Ledger semantics

The native agent ledger projects the `SkillRun` instead of copying a generic
catalog status. An executable skill is `APPLIED` only when at least one module
in the agent scope was `APPLICABLE` and its `evaluate()` method ran; evidence
is either its real findings or a recorded clean evaluation. `NOT_APPLICABLE`,
`UNDETERMINED`, and `ERROR` preserve the native outcome. `LOADED_ONLY` means a
catalog document has no executable contract yet.

Process disciplines do not pretend to be per-module scanners. The following
are recorded as `PROCESS_LEVEL`: abductive engineering, audit-before-patch,
claim provenance, codebase health, Daubert writing, diagnosing bugs, git
discipline, LLM out of the loop, red-team auditing, reverse engineering,
secure by construction, software archaeology, and surgical patcher. A future
run-level evaluator will check their obligations against FORGE artifacts.

External multi-agent submissions are cross-checked when a native `SkillRun` is
available: declaring an executable skill `APPLIED` while the native run found
it `NOT_APPLICABLE` for every module fails closed.

A new skill is a new directory under `forge/skills/` with a `manifest.json`
and a contract class — `forge/governance/runtime.py::load_skills()` discovers
it by walking `skills_root`, with no change to the core required. That is
the actual extensibility path today: a compliance, privacy, licensing, or
performance skill plugs in the same way `validate-at-the-boundary` did.
Adding a wholly new *specialized agent* (in the `Runtime._audit()` sense,
like Security Auditor) is a different, less pluggable path — it still means
touching the runtime — so this extensibility claim is scoped precisely to
governance skills, not to agents in general.

## Honest degradation boundary

`honest-degradation` does not treat every log call as sufficient disclosure.
A handler that logs an exception and then drops the current item with
`continue` still leaves the caller with a plausible partial result unless it
also raises or records explicit degraded/error state. The executable contract
therefore flags `log; continue` discard paths without such state, while
leaving logged handlers clean when the degraded outcome is propagated.

The current executable subset covers two direct AST patterns:

- loop drops: an exception handler inside a loop silently reduces a returned
  collection;
- stage swallows: an exception handler replaces a stage/component result with
  `None` or an empty/default value and returns it as ordinary output.
- default returns: a required stage/conversion helper logs and returns
  `None`/empty/default without emitting an unanalyzed/degraded marker.

Required-stage name matching uses complete verb segments (for example,
`to_signal`, `run_full`, or `load_artifact`), never bare letter prefixes such
as `to` matching `token_count`. A `None` sentinel is also accepted only when
the handler catches a narrow, explicitly named parse/decode exception (such as
`SyntaxError`, `JSONDecodeError`, or `UnicodeDecodeError`); the function name
does not grant that exception. A broad handler in `parse_x` remains auditable.
The narrow gate deliberately leaves helpers outside this vocabulary (for
example `deserialize`) as visible coverage limits rather than guessing.

The accepted visibility actions are structural, not narrative: raise, emit an
`*_UNANALYZED`-style sentinel, append to an error/drop accumulator, set an
explicit degraded/skipped/error flag, or call a named marker such as
`mark_degraded` or `record_drop`. Optional field defaults and cleanup paths are
corpus guardrails because they are not degraded-stage evidence.

## Catalog

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
