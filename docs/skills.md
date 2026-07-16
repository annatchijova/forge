# Governance skills

FORGE keeps the engineering methodologies in `skills-gpt/` as shared source
material and is migrating them into executable, contextual skill contracts.
The runtime must not apply every skill as a universal policy: a module's
domain hypothesis determines applicability. At present,
`validate-at-the-boundary` is the complete executable reference plugin; the
remaining catalog is not represented as active checks merely because its
documentation exists.

A governance skill is not a hardcoded `if float(): finding` check bolted onto
the core. It is a pipeline stage:

```
module
   │
   ▼
domain hypothesis            (infer_domains: machine_learning /
   │                          input_boundary / cryptographic, or none)
   ▼
applicable contracts         (each skill's own applicability() decides
   │                          APPLICABLE / NOT_APPLICABLE / UNDETERMINED)
   ▼
executable checks            (each applicable skill's evaluate())
   │
   ▼
findings
```

A new skill is a new directory under `forge/skills/` with a `manifest.json`
and a contract class — `forge/governance/runtime.py::load_skills()` discovers
it by walking `skills_root`, with no change to the core required. That is
the actual extensibility path today: a compliance, privacy, licensing, or
performance skill plugs in the same way `validate-at-the-boundary` did.
Adding a wholly new *specialized agent* (in the `Runtime._audit()` sense,
like Security Auditor) is a different, less pluggable path — it still means
touching the runtime — so this extensibility claim is scoped precisely to
governance skills, not to agents in general.

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
