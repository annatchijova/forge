# False-positive investigation log

This document records false positives found while self-auditing FORGE. It is
part of the engineering evidence for improving detector precision without
silently weakening valid findings.

## Scope

The source run reviewed was the FORGE self-audit of commit
`93c616260be01e8d581b12fb3338315f92739a31`.

The run reported five findings:

- one HIGH finding from Bug Investigator;
- four MEDIUM findings from Integrity Inspector;
- no Security Auditor findings.

The audit was sealed and the CRONOS chain verified. The run also reported one
successful induction.

## Finding 1: decision-adjacent float

### Trigger

The original detector treated a `float(...)` call as decision-adjacent when it
was located in a function whose name, or a nearby variable name, contained
words such as `decision`, `score`, `verdict`, or `classification`.

This was a naming-proximity heuristic. It did not establish that the value
returned by `float(...)` reached the function's actual decision output.

### Concrete false positive

The real-world pattern in `mutante_semiotic_evaluator.py` computed a float into
an unrelated telemetry dictionary inside a function with verdict-related
naming. The function returned a separate verdict value. The detector reported
the telemetry conversion even though it could not affect the returned result.

### Resolution

The detector now follows a deliberately shallow AST path:

- direct `float(...)` in a return expression;
- a named variable assigned from `float(...)` and later returned;
- a simple arithmetic, boolean, comparison, or unary return expression using
  that value;
- one-hop propagation through named assignments.

Unrelated telemetry values are no longer treated as decision arithmetic.

### Regression coverage

The regression fixture contains both cases:

- a `verdict(...)` function with unrelated telemetry, which must be clean;
- a `verdict(...)` function returning `float(response) > 0.5`, which must be
  reported.

## Findings 2–5: unversioned serialization

### Trigger

The serialization detector inspected `json.dump`, `json.dumps`, and pickle
calls. Its initial AST check could recognize a schema version when the payload
was an inline dictionary, but not when the dictionary was first assigned to a
variable.

### Concrete false positives

Two patterns produced the four reported findings:

1. `forge/benchmark.py` assigned a payload containing
   `benchmark_schema_version` to `payload`, then serialized `payload`. The
   detector saw only the variable name and missed the version field.
2. `forge/report.py` used several `json.dumps(...)` calls to embed metrics in
   the visual HTML report. These are presentation serializers, not persisted
   interchange artifacts. Three calls on the same source line were counted as
   three findings even though they belonged to one presentation operation.

### Resolution

The detector now:

- tracks simple names assigned to dictionaries containing `schema_version`,
  `version`, or `benchmark_schema_version`;
- treats those named payloads as versioned;
- excludes presentation-only serialization in `forge/report.py` from the
  unversioned-artifact rule.

This preserves the valid rule for genuinely unversioned persisted payloads.

### Regression coverage

Tests cover:

- a versioned dictionary assigned to `payload` before `json.dumps(payload)`;
- JSON embedded in presentation HTML;
- an actual unversioned serialization finding;
- existing versioned inline serialization.

## Bug Investigator finding: missing exception handling in `reporting.py`

### Trigger

Bug Investigator flagged the call to `render_report(...)` in
`forge/reporting.py` because it had no nearby `try/except` block. Its induction
path exercised an incomplete run and observed `FileNotFoundError`.

### Classification

This is a false positive as a defect and an overstatement as a HIGH finding.
`render_dashboard()` validates all required sidecars before rendering and
raises a named `FileNotFoundError` containing the exact missing paths. The
failure is explicit and actionable for a direct API caller; it is not an
opaque unhandled parser failure.

The induction result is still useful: it proves the incomplete-run contract is
reachable and should remain covered by tests. It does not prove a security
impact or justify HIGH severity.

## What caused the false positives

The common causes were:

1. **Proxy signals instead of data flow.** Names such as `verdict` and `score`
   were used as substitutes for proving value propagation.
2. **AST-local context was too narrow.** The serializer rule understood inline
   dictionaries but not a nearby assignment to a named payload.
3. **Presentation and persistence were conflated.** JSON used inside an HTML
   report was treated like a durable interchange artifact.
4. **Finding identity was too granular.** Multiple calls on one source line
   produced duplicate findings without a distinct risk or evidence identity.
5. **Exception presence was used as a quality proxy.** The absence of a local
   `try/except` was treated as an opaque failure even when the API emitted a
   precise, documented exception.

## Current status

After the detector changes:

- direct Integrity Inspector inspection of the current FORGE tree produces
  zero findings for the audited false-positive patterns;
- the full test suite passes: **108 tests**;
- valid direct-return float detection remains active;
- valid unversioned serialization detection remains active.

## Follow-up work

The next precision improvements should be tracked separately from detector
fixes:

- deduplicate findings by family, path, line, and normalized evidence;
- make severity depend on demonstrated impact rather than detector category;
- distinguish `confirmed by induction` from “the error path was reachable”;
- add explicit repository exclusions for generated reports, databases, and
  prior audit output so coverage denominators are not polluted;
- record whether a finding is a source defect, detector limitation, or
  presentation-only observation.

The governing rule is: a detector may report a hypothesis, but the report must
make the evidence boundary and confidence level visible instead of presenting
a proxy signal as a confirmed defect.
