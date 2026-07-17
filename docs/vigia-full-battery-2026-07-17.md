# VIGÍA full FORGE battery — read-only harvest

**Date:** 2026-07-17  
**Target:** `annatchijova/vigia-intent-analysis`  
**Mode:** read-only; induction enabled; no VIGÍA source was changed.

## Declared source scope

The repository contains a large forensic-evidence tree, virtual environments,
captured artifacts, test harnesses, and operational scripts. A raw discovery
of the checkout found more than 100,000 files and 500 nominally eligible source
files, while `vigia/**` itself contained 193 Python files. That denominator is
not an honest proxy for the production decision path.

No global FORGE exclusion policy was changed. Instead, the run used a temporary,
content-preserving source view containing the production VIGÍA package while
excluding its nested `tests/`, `scripts/`, and data directories, plus the live
top-level `vigia_scorer.py`. This is a declared audit scope, not a claim that
the excluded files were binary or unimportant.

| Metric | Result |
|---|---:|
| Python files in declared production view | 167 |
| Eligible source files | 167 |
| Files analyzed | 167 |
| Semantic source coverage | 167/167 (100%) |
| Files discovered in the view | 343 |
| Discovery ratio | 167/343 |
| Findings emitted | 212 |
| Discarded hypotheses | 5 |

The first direct `vigia/**` run is retained as a scope diagnostic only: its
193/193 source coverage included nested tests and scripts, and all 77 emitted
findings came from those roles. It is not used as the production finding set.

### Parsed source is not detector attention

That direct scope diagnostic also exposed a second coverage boundary. Its
triage manifest classified 193 modules, but only **29** as `CONNECTED_ALIVE`;
the remainder was 68 `DEAD_WEIGHT`, 84 `FOSSIL_HIGH_RISK`, and 12 `DUPLICATE`.
FORGE's specialized static agents and executable skills run on the
`CONNECTED_ALIVE` component. Therefore `193/193` means every eligible Python
file was parsed/accounted for; it does **not** mean all 193 received the same
detector attention. The test/script component dominated the connected seed in
that run, which explains why it emitted 77 harness findings while production
signals were absent.

The isolated production view was a diagnostic workaround, not a substitute for
a final original-tree audit: relocating source can alter imports and removes
Git provenance. A future runtime feature should declare production entrypoints
or a connected-alive seed on the original checkout, then report alongside
source coverage: modules classified, modules in detector scope, and modules
parsed but outside detector scope.

## Artifact set

The complete sealed diagnostic run was produced at
`/tmp/forge-vigia-production-20260717-induced/` during the audit session and
was preserved byte-for-byte at
[`results/vigia-full-battery-20260717/`](../results/vigia-full-battery-20260717/):

- `verification-manifest.sealed.json`
- `findings.jsonl`
- `coverage-report.json`
- `skills-runtime.json`
- `metrics.json`
- standard, summary, and extended HTML reports

The preserved files are useful diagnostic artifacts, but they are not a
Git-provenanced final audit of the original checkout: the production view was
relocated into `/tmp`. Do not regenerate it under a different tree and call it
the same run; a citable final run must preserve the original repository and
declare its production seed.

## Signal inventory — not a bug count

| Producer | Signals | Status at harvest |
|---|---:|---|
| Security Auditor | 67 | Mostly path-boundary and filesystem-flow leads; reachability and attacker control remain unadjudicated. One SQL interpolation lead is prioritized below. |
| Integrity Inspector | 46 | Serialization and numeric/determinism observations; no end-to-end severity is inferred from syntax alone. |
| Honest Degradation | 35 | Includes the previously adjudicated loop-drop cohort and new direct-return candidates. |
| Tamper-Evident Audit Chain | 32 | `append`-without-visible-link observations; a ledger context review is required before treating any as an integrity defect. |
| Validate at the Boundary | 14 | Boundary protocol gaps, not exploit confirmations. |
| Bug Investigator | 12 | Parser, subprocess, and threshold hypotheses; induction yielded 11 `UNDETERMINED` and one error path, not a promoted exploit claim. |
| Deterministic Core | 1 | Float/division value enters a sealed payload; decision impact remains unadjudicated. |
| SQL aggregation | 5 | Potential N+1 observations, separate from security findings. |

The emitted severity labels are detector priors. They are not the final VIGÍA
severity labels. Every item requires one of the three adjudication buckets:
end-to-end confirmed defect, CODE FACT with reachability unresolved, or false
positive/contextual carve-out.

## High-information leads

### 1. Partial engine attestation — known live FORGE false negative

The previous breadth audit established that
`vigia/pipeline/pipeline.py::_compute_attestation()` suppresses `OSError` while
collecting source bytes and hashes a reduced set as a normal SHA-256
attestation. The run again did **not** emit a finding for that live function.
It remains a documented FORGE false negative. A dead duplicate in
`vigia/core/bundle_builder.py` was the original evidence lead, not the
reachable finding.

This battery does not change that provenance. The future FORGE candidate is a
narrow integrity subpattern: reduced source coverage flowing into a
hash/digest/attestation claim without an explicit coverage manifest. It is not
implemented as part of this harvest.

### 2. CAIE-bound evidence normalization — already induced P1

The full battery includes the previously documented `honest-degradation` lead
at `vigia_scorer.py:657`; its local discard branch remains CODE FACT with
end-to-end clean-verdict reachability unresolved. Separately, bounded induction
already confirmed the live P1 normalization path: malformed `metadata` can be
silently rewritten to `{}`, pass validation, remove a temporal assertion, and
flip `SUSPICION` to `NOISE` without a coverage marker. See the
[breadth-adjudication record](vigia-honest-degradation-breadth-2026-07-17.md).

`vigia_scorer.py` was included in the production view and classified
`CONNECTED_ALIVE` (two callers). Integrity Inspector emitted five
decision-adjacent arithmetic observations there (lines 190, 1059, 1090, 1091,
and 1102). It was not outside the battery measurement; none of those static
observations alone establishes an end-to-end decision defect.

### 3. SecurityAudit `/dev/null` fallback — falsified silent-drop lead

The induction sandbox forced the last-resort fallback path in
`vigia/security/security.py`, which returns `/dev/null` after it cannot create
a secure temporary log. A focused, read-only behavioral check established that
this does **not** continue silently: the next log write calls `os.fsync()`, gets
`EINVAL` on `/dev/null`, and raises `RuntimeError` before advancing the HMAC
chain. The constructor delays that failure until the first event, which is worth
design review in VIGÍA, but it is not an `honest-degradation` finding or a
FORGE false negative under the current contract.

### 4. Browser SQL interpolation — static lead, likely contextual false positive

`vigia/sift/browser_forensics.py:236` constructs a query with an f-string.
The interpolated `url_expr`, however, is selected only from two constant SQL
fragments based on the local boolean `has_chains`; it is not derived from a
database path, evidence content, or caller input. This is a useful precision
lead for the SQL detector, but not evidence of an exploitable SQL injection
without a contrary dataflow trace. It is recorded here as a candidate false
positive; no detector change is made during this harvest.

### 5. Loop drops in forensic parsers — structural coverage leads

The run reconfirms the previously triaged direct-AST loop-drop sites in disk,
EVTX, memory, registry, adapter, paired-review, and the live scorer. The
current evidence supports the structural statement — an item can be omitted
without a count or F7 marker — but final VIGÍA severity remains dependent on
whether that item reaches a verdict or an integrity claim. Existing F7 fixes
(`*_drops` plus returned `*_unanalyzed`, and emitted `unparsed_files`) remain
recognized as benign and must not be relitigated.

## Explicit limits

- The run does not prove a path traversal, SQL injection, credential leak, or
  tamper defect merely because a syntactic detector emitted a signal.
- A direct-AST skill cannot generally see a caller that records a fallback, a
  later F7 materialization, or a terminal-only output. Those are declared
  intra-function scope limits, not silent reclassifications as clean.
- Temporal, stateful, cross-message, and cross-process defects remain
  unmodeled unless a dedicated detector is specified.
- Sandbox-induced parser harness failures are preserved as `UNDETERMINED` or
  error-path evidence. They are not promoted to confirmations.

## FORGE regression-gate status at this snapshot

The harvest made no detector or policy change. Targeted recall tests pass
(`tests/test_recall.py`: 4 passed), and the recall runner reports no variant
regressions or unrecorded known gaps. The runner was also re-executed from a
real `.py` entrypoint: `fp_on_twins = 0`. The earlier
`recall-parser-named-error` twin was an induction-spawn artifact caused by
running the parent program from `<stdin>`, not a precision regression.

One independent FORGE maintenance item was identified: the ledger harness
froze its expectation at six clusters although the versioned ledger now
contains FP-007 and FP-008. The replacement asserts that documented ledger
entries are mined, without treating a new documented cluster as a test failure.

These are FORGE maintenance items, not VIGÍA findings and not evidence against
the sealed VIGÍA run. They are recorded so the run cannot be presented as a
blanket green regression gate.

## Next adjudication order

1. Keep VIGÍA read-only while tracing the high-information integrity and
   decision-adjacent leads to observable effects.
2. Record every resolved item with module, line, family, mechanism, exact
   trigger, adjudication bucket, and reachability state before writing a VIGÍA
   fix specification.
3. Sample the broad `pass`/append cohorts instead of claiming an unreviewed
   census precision rate.
4. Publish the sealed artifact set unchanged, then implement VIGÍA fixes in
   separate commits with their own reproductions and regressions.
