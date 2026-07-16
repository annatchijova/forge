# Phylo Forge security audit (Codex multi-agent v2)

## Final status

**ABSTAINED.** The fail-closed gate and Forge suite passed, and eight independent Codex work products were validated. No target-repository code was executed, so no static candidate is confirmed by induction.

Audited repository: `/home/labestiadevigia/phylo`  
Git revision: `26cfd2d22c0d22b5a1a883922909989476579804`

## Scope

Forge detected TypeScript, JavaScript, Python, SQL, CSS, YAML, and MJS. Python was effectively analyzed; JavaScript/TypeScript received bounded Forge-supported lexical review. SQL, CSS, YAML, and MJS were detected but not effectively audited. Forge preflight counted 33 modules: 24 `CONNECTED_ALIVE`, 6 `DEAD_WEIGHT`, and 3 `FOSSIL_HIGH_RISK`; the connected count is within the 100-module limit. A specialist inventory separately identified 47 statically traceable product/runtime files; this is a file count, not a competing Forge connected-module count.

The audit excluded `.git`, `.gitignore`, dependencies, `node_modules`, vendor and environment directories, caches, `.next`, build/dist/target, binaries, generated/minified code, and large artifacts. Manifests supplied stack evidence only. No target files changed.

## Findings and epistemic status

Six Codex hypotheses are recorded in `findings.json`, by language, severity, and agent. They concern unauthenticated or client-controlled persistence and evolution inputs, wildcard key scopes, sandbox isolation/timeouts, Python path/error handling, and bundle integrity/numeric/provenance gaps. The web and red-team agents identified the highest-severity surfaces; the Python and integrity agents identified medium/high integrity hypotheses. The independent reviewer reopened these candidates and downgraded any static claim of exploitability.

Confirmed: 0. Inferred/static hypotheses: 6, all **UNDETERMINED**. Rejected: 0. Abstained: runtime exploitability, full JS/TS semantics, unsupported languages, ARGOS, dependencies, and generated artifacts. No candidate is called a false positive without falsification evidence; downgraded candidates and reasons are in `discarded-candidates.json`.

## A-D-I, independence, and skills

Every role file contains hypothesis-specific abduction, deduction, and induction entries with evidence and an explicit induction limitation. `agent-independence.json` reports `INDEPENDENCE_VERIFIED`, eight unique work products, and eight distinct digests. The coordinator tracked scope and contradictions; the independent reviewer used its own evidence and reopened/downgraded claims rather than copying conclusions.

All agents loaded the 20 Markdown skills in `forge/skills-gpt`; each work product records concrete material skill actions or limitations. The detailed per-agent records are authoritative for those actions; the aggregate protocol index is in `agent-protocols.json`.

## Red-team, tests, ARGOS, and comparison

The fail-closed adversarial gate ran first and passed: `tests/test_red_team_adversarial.py`, 8 passed, 0 failed. It covered exclusions, generated/minified files, unterminated strings, large artifacts, binaries, dependencies, virtual environments, `.git`, and `.gitignore`. The full Forge suite then passed: 155 passed, 0 failed. ARGOS was unavailable, so independent cross-check status is **ABSTAINED**. A valid baseline comparison found 7 unchanged, 0 new, and 0 resolved deterministic candidates.

## Runtime, memory, coverage, integrity, reproducibility

No target runtime or arbitrary harness was executed. Forge recorded audit trace, metrics, coverage, snapshot/hash and sealed verification artifacts. Coverage is bounded by the scope manifest and Forge reports; unsupported languages and exclusions are explicit. Target runtime memory/behavior measurements are unavailable by design. The run is reproducible from the recorded Git revision, Forge artifacts, read-only scope, and test commands, subject to the stated abstentions.

## Required artifact index

`agent-results/*.json`, `agent-protocols.json`, `scope-manifest.json`, `findings.json`, `discarded-candidates.json`, `abstentions.json`, `contradictions.json`, `red-team-results.json`, `full-suite-results.json`, `comparison.json`, `audit-trace.json`, `coverage-report.json`, `verification-manifest.sealed.json`, and `agent-independence.json` are present in this directory.

Unexpected finding: the most consequential pattern was not a single confirmed exploit but a cluster of unauthenticated/client-controlled persistence and sandbox-boundary hypotheses; the independent reviewer specifically rejected treating comments or escrow atomicity as proof of isolation or authorization.
