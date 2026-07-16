# ARGOS Loop Hardening

**Date:** 2026-07-15
**Scope:** FORGE induction, hypothesis generation, verification, and integrity scanning

## Changes

- Parser induction now imports package-contained modules through their real
  package name, so relative imports are tested in the same context as the
  audited application. Import/setup failures are reported as
  `UNDETERMINED`, never as confirmed defects.
- When a parser call is inside a private helper and the module exposes
  `analyze()`, induction exercises that public boundary. This prevents a
  trusted lexicon loader from being mistaken for a user-input parser.
- Hypothesis generation ignores `json.load()` calls that clearly read a
  repository-owned, `__file__`-anchored lexicon. The boundary is provenance,
  not the spelling of `json.load()` alone.
- Parser verification recognizes an explicit broad exception boundary when it
  returns a degraded result or raises. Optional integrations such as Gemini
  can therefore degrade visibly without creating a parser finding.
- Integrity scanning no longer treats `float()` used only by serialization
  functions such as `to_dict()` as decision arithmetic. Floats that reach an
  actual comparison or verdict return remain eligible findings.
- Hypothesis generation now includes `FOSSIL_HIGH_RISK` Python modules, while
  the integrity agent retains its existing `CONNECTED_ALIVE` contract. The
  scope expansion is therefore explicit and agent-specific rather than an
  accidental broadening of every detector.

## Re-audit result

Against ARGOS commit `3415ec32f8561663edfb2d3dd5c005b7ee43b66f`:

```text
FORGE tests: 130 passed
ARGOS findings: 0
Discarded hypotheses: 1
Coverage: 23/70 (32.9%)
Disposition: ABSTAIN_INSUFFICIENT_SCOPE
```

The discarded hypothesis is the Gemini JSON parser candidate. FORGE now
recognizes its explicit exception boundary and does not report it as a
finding.

The coverage abstention remains intentional. ARGOS still contains 15
unsupported TypeScript files, 2 unsupported JavaScript files, 13 binary
assets, and modules outside the connected audit scope. The next scope
improvement should be a dedicated TypeScript/JavaScript static-analysis agent
and an explicit policy for configuration and frontend assets; changing the
status without those checks would be an overclaim.

