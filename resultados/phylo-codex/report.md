# Forge audit — phylo

## Status
**ABSTAINED**. The Forge red-team gate and full Forge suite passed, but ARGOS was unavailable and the target application was not executed. No candidate is confirmed by induction.

## Scope and languages
- Repository: `/home/labestiadevigia/phylo`
- Git revision: `26cfd2d22c0d22b5a1a883922909989476579804`
- Detected: TypeScript, JavaScript, Python.
- Effectively analyzed: Python via AST detectors; JavaScript/TypeScript via bounded lexical web auditor.
- Discovered 14,624 files; 14,598 excluded by policy; 26 analyzed; 24 connected modules.
- Excluded: `.git`, `.gitignore`, dependencies, `node_modules`, `.venv`, `venv`, caches, `.next`, build/dist/target, binaries, generated/minified/large artifacts. Manifests supplied stack evidence only.

## Findings
Seven static candidates were emitted: three CRITICAL observations (path operation without visible normalization; two dynamic-evaluation observations), four MEDIUM parser-boundary observations/hypotheses. The Python parser candidate is **INFERRED / PLAUSIBLE HYPOTHESIS / UNDETERMINED**, because loading the target module in package context failed. The web candidates are **OBSERVED / CODE FACT**, not confirmed vulnerabilities; Forge explicitly does not convert these lexical patterns into exploitability. No CONFIRMED, REJECTED, or induction-confirmed finding was produced.

Findings are broken down in `findings.json`, with module, severity, agent, epistemic state, evidence, and provenance.

## A-D-I and skills
Eight requested-role protocol records are present under `agent-results/` and `agent-protocols.json`; each includes abduction, deduction, induction, evidence, and every one of the 20 Markdown skills from `forge/skills-gpt/`. Skills were loaded and applied as recorded policy inputs. Their semantic enforcement is limited where Forge has no executable checker, and those limitations are explicit per skill.

## Red team, suites, integrity
- Fail-closed exclusion gate: PASS; `tests/test_red_team_adversarial.py`: 8 passed.
- Full Forge suite: `tests`: 150 passed.
- Sealed manifest: `verification-manifest.sealed.json`; snapshot and source attestations are present.
- Baseline comparison: valid previous Forge run; 7 unchanged, 0 new, 0 resolved.
- Runtime target code execution: none authorized or performed.
- ARGOS: ABSTAINED, unavailable; independent reviewer recorded the exact limitation.
- Contradictions: none reported; no candidate was labeled false positive without falsification evidence.

## Runtime and reproducibility
Forge recorded coverage, snapshot SHA-256, audit trace, metrics, skills runtime, and sealed verification data. Static results are reproducible from the recorded revision and snapshot; application-behavior claims remain undetermined because no safe harness was available/authorized.

## Limitations
The built-in Forge runtime does not provide the requested native specialist names or parallel execution model; the output records requested roles mapped to Forge-native protocol roles. JavaScript/TypeScript analysis is bounded and non-AST. Dependencies and generated artifacts were not audited.
