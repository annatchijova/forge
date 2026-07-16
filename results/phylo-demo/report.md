# FORGE Security-Audit Demo — phylo

## Executive status

Forge completed a sealed, scope-limited audit. The result is **ABSTAIN_INSUFFICIENT_SCOPE**, not a green or complete security verdict. The fail-closed red-team gate passed before the audit: **8/8 tests passed**. The Forge full suite also passed: **147 passed**.

- Repository: `/home/labestiadevigia/phylo`
- Audited revision: `26cfd2d22c0d22b5a1a883922909989476579804`
- Forge snapshot SHA-256: `6576700de9e634e50a72cd0d7c08e639f9e6eb40bede9e5ae5a8979471654ead`
- Forge version: `0.1.0`
- Connected-module cap: `100`; detected connected-alive modules: `24`
- Findings emitted: `12`; discarded candidates: `0`

## Invocation

MCP workflow invocation:

```text
mcp__forge__repository_summary({"path":"/home/labestiadevigia/phylo"})
mcp__forge__triage_repository({"path":"/home/labestiadevigia/phylo"})
python3 -m pytest -q tests/test_red_team_adversarial.py
mcp__forge__audit_repository({"path":"/home/labestiadevigia/phylo","output_dir":"/tmp/forge-phylo-demo-audit","max_connected":100})
mcp__forge__verify_seal({"sealed_path":"/tmp/forge-phylo-demo-audit/run-cef85o2h/verification-manifest.sealed.json"})
python3 -m pytest -q
```

## Preflight

Forge detected **33 modules** and these stacks:

| Stack | Detection evidence | Audit status |
|---|---:|---|
| TypeScript | 28 files | Selected files analyzed by `web_auditor`; not repository-wide |
| Python | 3 files | `tools/evolution_bundle.py` analyzed; fossil Python modules excluded |
| JavaScript | 2 files | Selected files analyzed by `web_auditor`; not repository-wide |

| Module class | Count |
|---|---:|
| CONNECTED_ALIVE | 24 |
| DEAD_WEIGHT | 6 |
| FOSSIL_HIGH_RISK | 3 |

Dead-weight modules were `lib/dynamo.ts`, `lib/evolution-client.ts`, `lib/run-history.js`, `next-env.d.ts`, `tests/llm_test.ts`, and `tests/sandbox_test.ts`. Fossil/high-risk modules were `tools/adaptive_gene_pool.py`, `tools/verify_bundle.py`, and `types/index.ts`. The triage deletion judgments say these are unreachable/deletion-sensitive, but they were not audited as connected live scope.

## Findings

The following are Forge observations, grouped by language, severity, agent, and epistemic status. “Code fact” means the construct was observed; it does not by itself prove exploitability. The two inferred candidates remained undetermined by induction and are therefore only plausible hypotheses.

| Language | Severity | Agent | Epistemic status | Module / observation |
|---|---|---|---|---|
| Python | MEDIUM | `bug_investigator` | PLAUSIBLE HYPOTHESIS; induction UNDETERMINED | `tools/evolution_bundle.py:548`: `json.loads(...)` lacks nearby exception handling; module-load context failed during induction |
| Python | MEDIUM | `bug_investigator` | PLAUSIBLE HYPOTHESIS; induction UNDETERMINED | `tools/verify_bundle.py:404`: binary-float threshold; no executable harness; module was fossil/excluded from live audit |
| Python | MEDIUM | `integrity_inspector` | CODE FACT | `tools/evolution_bundle.py:468`: unversioned serialization |
| Python | MEDIUM | `integrity_inspector` | CODE FACT | `tools/evolution_bundle.py:543`: unversioned serialization |
| TypeScript | MEDIUM | `web_auditor` | CODE FACT | `tests/llm_test.ts:18`: `JSON.parse` without nearby visible try/catch; test module is dead weight |
| JavaScript | MEDIUM | `web_auditor` | CODE FACT | `components/EvolveScreen.jsx:299`: `JSON.parse` without nearby visible try/catch |
| TypeScript | MEDIUM | `web_auditor` | CODE FACT | `app/api/ci/route.ts:167`: `JSON.parse` without nearby visible try/catch |
| TypeScript | CRITICAL | `web_auditor` | CODE FACT | `app/api/save-run/route.ts:107`: filesystem path reaches file operation without visible normalization |
| TypeScript | MEDIUM | `web_auditor` | CODE FACT | `app/api/save-run/route.ts:110`: `JSON.parse` without nearby visible try/catch |
| TypeScript | CRITICAL | `web_auditor` | CODE FACT | `app/api/sandbox/javascript/route.ts:163`: dynamic evaluation at a data-to-code boundary |
| TypeScript | CRITICAL | `web_auditor` | CODE FACT | `app/api/sandbox/javascript/route.ts:170`: dynamic evaluation at a data-to-code boundary |
| TypeScript | MEDIUM | `web_auditor` | CODE FACT | `app/api/sandbox/python/route.ts:226`: `JSON.parse` without nearby visible try/catch |

No finding is labeled “false positive.” Forge did not execute enough application-level induction to establish that label. The two parser/float candidates are **inferred**, not confirmed. The remaining entries are **observed/code facts**, not claims that the associated behavior is exploitable in deployment.

## Discarded or downgraded candidates

- Discarded candidates: **0** according to the sealed manifest.
- Downgraded/limited candidates: two `bug_investigator` hypotheses remained `PLAUSIBLE HYPOTHESIS` because induction was undetermined: one because the target module could not load in package context, and one because no executable harness was registered.
- No language was upgraded from detection to repository-wide audit coverage. Fossil/dead-weight modules were excluded by Forge scope policy.

## Abstentions and exact boundaries

Forge discovered **14,624 files**, analyzed **40**, and skipped **14,584**. The coverage artifact records **5/1,828 = 0.3%** for its measured coverage ratio. Nine modules were excluded from connected analysis: `lib/dynamo.ts`, `lib/evolution-client.ts`, `lib/run-history.js`, `next-env.d.ts`, `tests/llm_test.ts`, `tests/sandbox_test.ts`, `tools/adaptive_gene_pool.py`, `tools/verify_bundle.py`, and `types/index.ts`.

Forge excluded `.git`, `node_modules`, `.next`, `.turbo`, build/dist/target outputs, caches, binaries, generated artifacts, and other policy-excluded files. Non-Python files without an applicable web analysis path were reported as `non_python_not_analyzed`; this includes configuration, documentation, CSS, SQL, JSON demo data, and package metadata. The audit therefore does not establish coverage of all TypeScript, JavaScript, Python, configuration, dependency, deployment, or runtime behavior.

## Cross-check and integrity

- ARGOS: no ARGOS run was invoked for this demo.
- Independent Forge cross-check: `verify_seal` returned `ok=true`, `linkage_ok=true`, `integrity_ok=true`, `issues=[]`.
- The seal verifies post-sealing integrity and linkage; it does not prove that findings are correct.
- Audit trace reported zero contradictions and one abstention; the self-assessment confidence boundary was `scope-limited`.

## Red-team and full-suite results

- Fail-closed red-team gate: `python3 -m pytest -q tests/test_red_team_adversarial.py` → **8 passed in 0.26s**.
- Full Forge suite: `python3 -m pytest -q` → **147 passed in 2.41s**.
- Because the red-team gate passed, the audit was allowed to run. No red-team failure was suppressed.

## Runtime, memory, coverage, integrity, reproducibility

- Audit wall/runtime recorded by Forge: **12.390902 seconds** in the generated Markdown report; archaeologist agent time: **10.803376 seconds**.
- Peak memory: not populated by this Forge run (`metrics.json` provides no measured peak RSS value).
- Coverage: 40/14,624 files analyzed; 24/33 modules covered; 71 functions and 2,067 lines analyzed; 9 modules excluded by scope.
- Integrity: sealed chain length 12; independent seal verification passed with no issues.
- Reproducibility: Linux, Python 3.12.3, Forge 0.1.0, snapshot SHA-256 recorded above; artifact hashes and deterministic-runtime flag were not populated by Forge, so those properties remain undetermined from this run.

## Result classification

- **Confirmed:** red-team gate pass, full-suite pass, seal linkage/integrity pass, and direct AST/code observations labeled `CODE FACT`.
- **Inferred:** two `bug_investigator` candidates labeled `PLAUSIBLE HYPOTHESIS`.
- **Rejected:** none in the sealed audit (`discarded=0`); no candidate is called a false positive.
- **Undetermined:** exploitability, runtime impact, induction for both hypotheses, completeness of language coverage, peak memory, artifact-hash reproducibility, and behavior of excluded modules/files.

## Machine-readable artifacts

All generated artifacts are in this directory alongside this report:

- `triage-manifest.json`
- `hypotheses-manifest.json`
- `verification-manifest.json`
- `verification-manifest.sealed.json`
- `coverage-report.json`
- `skills-runtime.json`
- `metrics.json`
- `repository-profile.json`
- `audit-trace.json`
- `forge-report-json.json`
- `forge-report.html`, `forge-report-summary.html`, `forge-report-standard.html`, `forge-report-extended.html`

Original temporary run directory: `/tmp/forge-phylo-demo-audit/run-cef85o2h`.
