# Lessons from the `phylo` multi-agent audit

Date: 2026-07-16  
Audited repository: `/home/labestiadevigia/phylo`  
Audited revision: `26cfd2d22c0d22b5a1a883922909989476579804`  
Artifacts: [`resultados/phylo-codex/`](../resultados/phylo-codex/)

## Executive summary

The run correctly enforced Forge's abstention behavior: red-team 8/8, full
suite 150/150, seal verified, the audited repository was not modified, and the
final status was `ABSTAINED`.

The main lesson is that the current multi-agent mode does not yet demonstrate
independent multi-agent deliberation. Eight roles and A-D-I protocols were
recorded, but the agent results were largely generic protocol records copied
from the same context. There is not enough evidence that each agent produced
independent hypotheses, tests, contradictions, or decisions.

This run is valid as a test of scope boundaries, integrity, and abstention. It
is not yet a demonstration of autonomous specialist agents.

## Evidence from the run

- 33 modules detected: 24 `CONNECTED_ALIVE`, 6 `DEAD_WEIGHT`, and 3
  `FOSSIL_HIGH_RISK`.
- Detected languages: TypeScript, JavaScript, and Python.
- Python: effective AST analysis.
- JavaScript/TypeScript: bounded web scan, not a full language audit.
- Excluded: dependencies, virtual environments, `.git`, `.gitignore`, caches,
  builds, binaries, generated code, minified files, and large artifacts.
- Seven observations: three critical and four medium.
- Zero results confirmed by dynamic induction.
- ARGOS was unavailable and was explicitly recorded as an abstention.
- The seal proves artifact integrity, not finding correctness.

## 1. Roles do not prove independent agents

The eight recorded roles were:

- `coordinator`
- `scope_triage`
- `python_security`
- `web_security`
- `integrity_numeric`
- `abduction_hypotheses`
- `adversarial_redteam`
- `independent_reviewer`

However, the files under `agent-results/` contain almost exclusively the same
generic A-D-I block, the same references to `verification-manifest.json` and
`audit-trace.json`, and the same catalog of 20 skills. There is no material
evidence of role-specific analysis.

The `independent_reviewer` also supplied no material independent review. The
absence of contradictions does not demonstrate independence when there is no
independent output to compare.

### Required change

Each agent must produce its own result containing observed inputs, hypotheses,
falsifiable deductions, executed tests or abstentions, an epistemic decision,
evidence, and disagreements with other agents. The coordinator must reject a
run when the outputs are only copies of the shared protocol.

## 2. A-D-I exists as a contract, not yet as behavior

All agents recorded the same states:

- abduction: `PLAUSIBLE_HYPOTHESIS`;
- deduction: `PREDICTION_REQUIRED`;
- induction: `UNDETERMINED`.

This proves that the schema is present, but not that each agent performed a
specific abduction or deduction. The ledger must be per hypothesis, not merely
per agent.

Each A-D-I entry must contain a concrete claim, a concrete falsifier, and the
evidence that changed its state.

## 3. Skills are loaded but over-declared as applied

All 20 skills appear as `APPLIED`, but the recorded action is essentially
“load the Markdown policy and record its application.” That proves documentary
loading, not semantic application.

The quality metric reports `contract_coverage: covered 0 / total 1` and
`skill_versions: {}`. Most skills therefore do not yet have an executable
checker or verifiable obligation.

### Required change

Create a `skill_obligation_ledger` containing the skill, concrete obligation,
responsible agent, A-D-I stage, expected evidence, observed evidence, and
status: `APPLIED`, `REJECTED`, or `UNDETERMINED`. `APPLIED` must mean that the
skill changed an observable decision, not merely that it was read.

## 4. Path handling exposed a real analysis limitation

Forge marked `app/api/save-run/route.ts:107` as critical path traversal because
it saw `writeFile(join(dir, filename), ...)`. However, `filename` is derived
from a `slug` sanitized by restrictive replacements on the preceding lines.

The sanitization is distributed across a multiline expression, and the
analyzer does not correctly propagate that evidence to the final use. This
must not automatically be called a false positive: the correct current state
is “observation with a plausible benign explanation, pending verification.”

### Required change

Implement conservative propagation for multiline assignments, variables derived
from sanitized names, `basename`, `normalize`, `resolve`, extension checks,
concatenations, and templates before uses in `join`, `writeFile`, `readFile`,
`unlink`, and `rm`.

## 5. `eval` is an observed boundary, not a confirmed vulnerability

The observations in `app/api/sandbox/javascript/route.ts` show code execution
through `eval`. This is real evidence of a data-to-code boundary, but it does
not demonstrate sandbox escape, server-process control, secret access, or
remote exploitability.

The correct classification is: observed, yes; plausible design risk, yes;
confirmed exploit, no; induction, abstained.

Forge must distinguish the presence of a dangerous boundary, input
controllability, and exploitability.

## 6. Python induction failed during module loading

The hypothesis about `json.loads` at `tools/evolution_bundle.py:548` remained
plausible because loading the module in package context failed with:

`AttributeError: 'NoneType' object has no attribute '__dict__'`

This is an infrastructure abstention, not evidence about the module's security.

Forge needs an induction loader that builds the correct package context, uses
isolated read-only harnesses, and distinguishes “harness unavailable” from
“harness failed.”

## 7. Historical comparison must compare perimeters

The comparison reported seven previous findings, seven current findings, and
seven unchanged findings. That is useful as an entry comparison, but its
`coverage_delta` uses a trivial denominator of 1 and does not demonstrate
coverage equivalence.

Future comparisons must include hashes or versions for the repository revision,
Forge, skills, scope manifest, agent configuration, auditable file set, and
available harnesses.

## 8. Red-team and full suite validate Forge, not `phylo`

The `8 passed` and `150 passed` results prove that Forge's tests passed. They do
not prove that `phylo` is secure or that the seven findings are exploitable.
This distinction must remain visible in HTML reports and final status.

## Prioritized backlog

### P0: required before calling the mode multi-agent

- Independent output from each agent.
- A-D-I ledger per hypothesis.
- Independent reviewer with its own evidence.
- Fail closed when outputs are generic protocol copies.
- Skills with verifiable obligations.

### P1: finding quality

- Multiline data-flow for sanitization.
- Separation of pattern, controllability, and exploitability.
- Safe loader for Python induction.
- Real parser or structural analysis for JavaScript/TypeScript.
- Severity based on input flow and evidence, not only AST family.

### P2: comparison and operations

- Effective coverage over the auditable perimeter.
- Historical comparison with a scope hash.
- Versioning for skills and executable contracts.
- Metrics for agent independence and disagreement.
- ARGOS integration or formal abstention.

## Success criteria for the next run

The next run must demonstrate that each agent produced materially distinct
analysis, each hypothesis has its own A-D-I record, each applied skill has
concrete evidence, the reviewer can contradict the coordinator, and the
artifacts reproduce who decided what and why.
