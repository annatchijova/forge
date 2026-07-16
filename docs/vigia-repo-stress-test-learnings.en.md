# Lessons from the `vigia-repo` bounded stress test

## Scope and provenance

This document records the bounded Forge stress test performed against two explicit scopes of `vigia-repo`:

- `vigia/core`
- `vigia/tools`

The target revision was `c28f31a1deaf21aba1df3f3162dd0490e5be9729`. The target repository was unchanged; 23 pre-existing worktree entries were preserved. The output directory was `forge/resultados/vigia-core-tools-stress`.

This was not a full `vigia-repo` audit. The combined scope was preflighted only and produced no combined audit result.

## Outcome

The final status was `BLOCKED`, and that status is valid and fail-closed:

- Red-team gate: `PASS`, 8/8.
- Full Forge suite: `PASS`, 158/158.
- `vigia/core`: 47 modules discovered, 15 connected; two audit attempts timed out after 300 seconds each.
- `vigia/tools`: 33 modules discovered, 16 connected; audit completed in 2.91 seconds.
- Combined bounded scope: 80 preflight modules; no combined audit was produced.
- Peak RSS: unavailable.
- Native tools seal: present, but MCP verification timed out.
- Canonical seal and digest: not generated.
- Independence validation: not completed because the core audit did not finish.

The timeout is an operational result about Forge execution. It is not evidence that `vigia/core` is vulnerable or safe.

## Completed `vigia/tools` evidence

Forge discovered 59 files in the tools scope: 33 Python files and 26 other files. It analyzed 33 files and skipped 26, giving file coverage of 33/59. The scope contained 365 functions and 22,263 lines of code. Sixteen modules were connected, eight were dead-weight, and nine were classified as fossil/high-risk candidates.

The completed tools run emitted 43 candidates and discarded three. The candidates were distributed as follows:

- By agent: integrity inspector 22, security auditor 8, bug investigator 7, boundary validator 6.
- By epistemic status: 30 code facts, 7 plausible hypotheses, 6 protocol gaps.
- By family: 6 numeric-boundary, 17 unversioned-serialization, 1 parser-boundary, 1 credential, and 18 other.

Seven candidates were marked critical. They primarily repeated path-normalization hypotheses in `document_integrity.py` and `metabolic_profiler.py`. These are static observations and were not induction-confirmed. They must not be reported as seven confirmed vulnerabilities.

The tools metrics correctly ended in `ABSTAIN_INSUFFICIENT_SCOPE` because the skipped files, unavailable runtime evidence, and absent independent confirmation prevented a complete security conclusion.

## What the stress test revealed about Forge

### 1. A repository-level timeout is too coarse

The core scope exceeded the practical audit window, but the report did not identify the phase, module, detector, or artifact responsible. Forge needs phase-level checkpoints and resumable partial results. Each phase should record start time, completion time, module, detector, findings emitted, and resource usage.

### 2. Large scopes need deterministic sharding

The core scope should be split into reproducible shards based on a stable module ordering or dependency graph. Shards must retain exact scope boundaries and be mergeable without changing finding identity or severity.

### 3. Resource measurement must be first-class

Peak RSS was unavailable for both scopes. Runtime without memory data is insufficient for a stress test. Forge should collect wall time, CPU time, peak RSS, file counts, analyzed/skipped counts, and per-phase timings, including partial runs that terminate by timeout.

### 4. Seal verification must be independent of the MCP request

The native tools seal was present, but verification timed out at the MCP layer. Forge should provide a bounded local verification path that can validate completed artifacts even when orchestration or transport is slow. A transport timeout must remain distinct from an invalid seal.

### 5. Candidate explosion needs stronger evidence separation

Repeated path-normalization candidates show that static detectors can identify a useful risk family while still overproducing hypotheses. The agents need explicit data-flow checks for normalization, resolution, allowlists, caller context, internal-only paths, and whether a value is actually attacker-controlled. Candidate records must preserve the distinction between code fact, plausible hypothesis, protocol gap, rejected candidate, and undetermined result.

### 6. Scope arithmetic must remain auditable

The report usefully separated discovered, connected, dead-weight, fossil/high-risk, analyzed, and skipped modules. This distinction must remain mandatory. No conclusion from `vigia/tools` may be extrapolated to `vigia/core` or to the full repository.

## Recommended next experiment

The next run should shard `vigia/core`, measure each phase, and identify the first expensive detector or module. Each shard should produce independently verifiable artifacts. Only after all shards complete should Forge run canonicalization, independence validation, and the final seal. This sequence will distinguish a performance bottleneck from a finding-volume bottleneck and will make the failure reproducible.

## Git history and Python packaging policy

The audit reports and machine-readable artifacts are intentionally kept in Git so the evolution of Forge and its audit evidence remains reviewable. They must not be hidden with `.gitignore`.

When Forge is later prepared for `pip install`, generated audit results under `resultados/` should be excluded from both source distributions and wheels through the packaging configuration (`MANIFEST.in`, `pyproject.toml`, and package-data rules as applicable). This keeps the evidence available in the Forge repository while preventing generated reports from being downloaded or installed as package payload.

## Final interpretation

This stress test was useful even though it was blocked. It demonstrated that Forge can pass its safety gates and complete a bounded tools audit, while also exposing missing observability, weak timeout granularity, insufficient sharding, and an MCP-dependent verification path. The 43 tools candidates are evidence requiring triage, not a vulnerability count; the core timeout provides no security verdict. The correct next goal is a reproducible, resource-instrumented, shardable run that can reach independent canonicalization without relaxing fail-closed behavior.
