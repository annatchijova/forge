# Codex terminal prompts

These prompts are intentionally conservative. FORGE performs the audit and
CRONOS records the trace; Codex reviews the sealed evidence and does not patch
the target repository unless the operator explicitly asks for a separate fix.

## Prompt 1 — read-only audit with CRONOS

Paste this into Codex from the FORGE checkout:

```text
Run a read-only FORGE audit of the repository at /absolute/path/to/repository.
Do not modify, format, install into, or commit anything in the target repo.

Use the local deterministic runtime with CRONOS tracing:

python3 -m forge audit /absolute/path/to/repository \
  --output-dir /absolute/path/to/forge-run \
  --cronos-db /absolute/path/to/forge-run/cronos.sqlite3 \
  --summary

After it finishes, verify the sealed manifest:

python3 -m forge verify /absolute/path/to/forge-run/verification-manifest.sealed.json

Render the standard human report:

python3 -m forge report /absolute/path/to/forge-run/verification-manifest.sealed.json \
  --mode standard -o /absolute/path/to/forge-run/report-standard.html

Report separately:
1. parsed source coverage;
2. CONNECTED_ALIVE detector scope and modules outside it;
3. findings grouped by epistemic status (CODE FACT, PROTOCOL_GAP,
   PLAUSIBLE HYPOTHESIS, and confirmed induction);
4. discarded hypotheses and explicit limitations;
5. CRONOS trace/seal verification status.

Do not call any finding a confirmed bug without tracing reachability and
testing the stated mechanism. Preserve false positives and unresolved leads as
such. Do not change the target repository.
```

## Prompt 2 — adjudicate the sealed evidence

Use this after the audit, with the run directory available:

```text
Review this FORGE run read-only:
/absolute/path/to/forge-run

Read verification-manifest.sealed.json, coverage-report.json,
metrics.json, findings.jsonl, report-standard.html, and the CRONOS database if
available. Verify the seal before interpreting findings.

For each high-priority lead, inspect the exact source line and answer:
- what mechanism the detector actually observed;
- whether the input is reachable from a real caller;
- whether the output reaches a decision, persisted artifact, or integrity claim;
- what experiment would falsify the hypothesis;
- whether the disposition is confirmed defect, CODE FACT with reachability
  unresolved, contextual false positive, or out of scope.

Keep FORGE's provenance intact. Do not rewrite a lead as a bug merely because
it sounds plausible, and do not hide a detector false negative. Produce a short
adjudication table and proposed regression tests. Do not patch or commit code.
```

The same workflow can audit FORGE itself by using the checkout as the target;
that dogfood run is useful because the tool's own scope and false positives stay
visible to reviewers.
