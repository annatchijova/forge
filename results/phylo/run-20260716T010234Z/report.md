# FORGE audit report

Repository: `/home/labestiadevigia/phylo`
Seal: **VERIFIED**
Findings: **7** · Discarded hypotheses: **0**
Coverage: **13/7312 (0.2%)**
Audit disposition: **ABSTAIN_INSUFFICIENT_SCOPE**

## Repository profile

- Modules: 33 (24 connected)
- Domains: cryptographic, input_boundary, machine_learning
- Audit duration: 9.995566 seconds

## Findings

### MEDIUM · tools/evolution_bundle.py
- Agent: `bug_investigator`
- Status: `PLAUSIBLE HYPOTHESIS`
- Description: The parser call `return json.loads(Path(path).read_text(encoding="utf-8"))` at tools/evolution_bundle.py:548 has no nearby exception handling, so malformed input may escape as an opaque failure.
- Reasoning: Observed construct matches; induction was undetermined: Target module could not be loaded in its package context: AttributeError: 'NoneType' object has no attribute '__dict__'
- Source commit: `dea9cb032595b8dc970667cf896d7717c3157492`

### MEDIUM · app/api/ci/route.ts
- Agent: `web_auditor`
- Status: `CODE FACT`
- Description: JSON.parse call has no nearby visible try/catch boundary
- Reasoning: AST detector emitted this observation: parser-boundary.
- Source commit: `dea9cb032595b8dc970667cf896d7717c3157492`

### CRITICAL · app/api/save-run/route.ts
- Agent: `web_auditor`
- Status: `CODE FACT`
- Description: filesystem path reaches a file operation without visible normalization
- Reasoning: AST detector emitted this observation: path-traversal.
- Source commit: `6c9c85a5ae37a6849b187c07758369eeb294ff34`

### MEDIUM · app/api/save-run/route.ts
- Agent: `web_auditor`
- Status: `CODE FACT`
- Description: JSON.parse call has no nearby visible try/catch boundary
- Reasoning: AST detector emitted this observation: parser-boundary.
- Source commit: `6c9c85a5ae37a6849b187c07758369eeb294ff34`

### CRITICAL · app/api/sandbox/javascript/route.ts
- Agent: `web_auditor`
- Status: `CODE FACT`
- Description: dynamic code evaluation crosses a data-to-code boundary
- Reasoning: AST detector emitted this observation: dynamic-evaluation.
- Source commit: `eaae67e748f766cc3f53bcd3564f13666ce5d264`

### CRITICAL · app/api/sandbox/javascript/route.ts
- Agent: `web_auditor`
- Status: `CODE FACT`
- Description: dynamic code evaluation crosses a data-to-code boundary
- Reasoning: AST detector emitted this observation: dynamic-evaluation.
- Source commit: `eaae67e748f766cc3f53bcd3564f13666ce5d264`

### MEDIUM · app/api/sandbox/python/route.ts
- Agent: `web_auditor`
- Status: `CODE FACT`
- Description: JSON.parse call has no nearby visible try/catch boundary
- Reasoning: AST detector emitted this observation: parser-boundary.
- Source commit: `dea9cb032595b8dc970667cf896d7717c3157492`

## Limitations

- Hypotheses require module 3 verification; parser candidates may receive isolated induction, while unsupported families remain AST-only.
- 14598 discovered file(s) were skipped; see skipped_reasons for the exact paths and policy categories.
- 9 triaged module(s) were outside CONNECTED_ALIVE audit scope.
- 18 skill applicability result(s) were UNDETERMINED; no conclusion was inferred for them.
- 1 hypothesis/hypotheses survived structural verification without dynamic induction; they remain plausible hypotheses, not confirmed defects.
