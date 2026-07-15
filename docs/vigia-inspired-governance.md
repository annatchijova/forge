# VIGÍA-inspired governance for FORGE

This is an implementation log for ideas extracted from the VIGÍA repository.
It records what FORGE adopts, what remains deliberately different, and the
evidence required before each future expansion.

## Why VIGÍA is a useful reference

VIGÍA treats uncertainty as part of the product contract. Its deterministic
engine does not equate “no alert” with “safe”, and its LLM boundary is outside
the sealed decision path. The most transferable ideas are governance patterns,
not forensic domain rules.

## Adopted first: global audit disposition

FORGE previously represented uncertainty locally through `UNDETERMINED`,
limitations, skipped files, and unresolved hypotheses. It did not combine those
signals into a repository-level disposition.

`forge/disposition.py` now adds a deterministic, non-destructive disposition:

| Status | Meaning | Required action |
|---|---|---|
| `COMPLETE_NO_FINDINGS` | Declared source scope verified; no finding survived | No action within declared scope |
| `COMPLETE_WITH_FINDINGS` | Declared source scope verified; findings survived | Review evidence and findings |
| `ABSTAIN_INSUFFICIENT_SCOPE` | Source boundary was skipped, unreadable, syntactically invalid, or outside audit scope | Complete the scope and rerun |
| `ABSTAIN_UNDETERMINED` | Governance applicability could not be determined | Resolve applicability and rerun |

The disposition does not erase findings. This is the key separation learned
from VIGÍA: a run can contain useful evidence and still abstain from claiming
complete repository coverage.

Intentional language boundaries (`non_python_not_analyzed`) are disclosed but
do not independently trigger abstention. The current AST engine is allowed to
say exactly what it did not analyze.

## VIGÍA patterns queued for FORGE

### 1. Pre-emission corroboration gate

VIGÍA lowers or abstains before sealing when evidence does not meet the required
bar. FORGE should add a deterministic finding gate that distinguishes:

- structural fact;
- surviving but unconfirmed hypothesis;
- confirmed by induction;
- discarded/falsified hypothesis.

The gate must never upgrade a proxy signal merely because it has a high label or
severity. This is the direct lesson from the self-audit false positives.

### 2. Contradiction and dissent states

VIGÍA models contradiction and specialist dissent separately from ordinary
uncertainty. FORGE can use the same idea when agents disagree about the same
module or when security/integrity evidence conflicts with a discarded benign
hypothesis. Candidate future states are `ABSTAIN_CONTRADICTION` and
`ESCALATE_REVIEW`.

### 3. Evidence-boundary ledger

VIGÍA preserves unusable evidence and records why it could not be processed.
FORGE should add a first-class ledger for skipped files, syntax failures,
binary inputs, policy exclusions, and missing harnesses rather than leaving
these only in aggregate coverage counters.

### 4. Action attached to uncertainty

Every abstention should say what resolves it: rerun with a larger scope, repair
syntax, add a permitted induction harness, resolve a skill contract, or request
human review. A status without a next action is only a label.

### 5. Deterministic self-correction

VIGÍA's contradiction checks run before optional narrative enrichment. FORGE
should keep any future natural-language narrator after sealing and use a
deterministic pre-report quality gate for duplicate findings, inconsistent
severity, unsupported “confirmed” language, and missing evidence.

### 6. Explicit limitation corpus

VIGÍA maintains a numbered limitations register and adversarial boundary cases.
FORGE should grow `docs/` and regression fixtures together: every known blind
spot gets a reason, a reproducer, an expected disposition, and a status.

### 7. Honest fallback for optional agents

The fallback path in `vigia_agent.py` maps unavailable pipelines, unsupported
formats, unreadable inputs, and analyzer errors to `ABSTAIN` rather than to a
benign or empty result. FORGE now applies the same rule to specialized
Security and Integrity agents: an agent failure is recorded, the surviving
agents still produce their evidence, and the global disposition becomes
`ABSTAIN_DEGRADED`. This keeps useful partial work without laundering a
partial audit into a complete one.

## What FORGE should not copy blindly

- VIGÍA's forensic verdict vocabulary does not map directly to code-audit
  findings.
- Confidence thresholds should not be invented without a calibration corpus.
- `ABSTAIN` must not become a catch-all for low coverage or zero findings.
- Cryptographic evidence sealing proves artifact integrity, not analytical
  correctness or repository completeness.
- LLM narration must remain outside the decision and sealing path.

## Current evidence

The first implementation is covered by regression tests for an incomplete
source boundary and for a complete run with findings. The full FORGE suite is
the acceptance gate for subsequent VIGÍA-inspired changes.

## Fallback-derived implementation status

The current FORGE implementation now also includes:

- cross-agent contradiction records with an `ABSTAIN_UNDETERMINED` disposition;
- primary/derived/recommendation evidence roles and finding provenance;
- a deterministic repository snapshot SHA-256 included in the sealed manifest;
- actionable unsupported-language coverage boundaries;
- a self-assessment section that reports agent availability, contradictions,
  abstentions, limitations, and a qualitative confidence boundary.

Still planned as separate contracts:

- signed or human-reviewed false-positive ledger entries;
- persisted cross-run comparison with resolved/new/unchanged findings;
- an explicit auditor-of-the-auditor report section backed by seal verification
  and CRONOS chain status.
