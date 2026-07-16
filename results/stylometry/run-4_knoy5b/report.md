# FORGE audit report

Repository: `/home/labestiadevigia/stylometry`
Seal: **VERIFIED**
Findings: **6** · Discarded hypotheses: **1**
Coverage: **31/241 (12.9%)**
Audit disposition: **ABSTAIN_INSUFFICIENT_SCOPE**

## Repository profile

- Modules: 31 (16 connected)
- Domains: cryptographic, input_boundary
- Audit duration: 0.439601 seconds

## Findings

### MEDIUM · src/report_exporter.py
- Agent: `integrity_inspector`
- Status: `CODE FACT`
- Description: non-deterministic arithmetic in a decision-adjacent path
- Reasoning: AST detector emitted this observation: decision-adjacent-float.
- Source commit: `618402b4817bcc6e41ce6a5e76bf170b1f47de71`

### MEDIUM · src/report_exporter.py
- Agent: `integrity_inspector`
- Status: `CODE FACT`
- Description: unversioned serialization
- Reasoning: AST detector emitted this observation: unversioned-serialization.
- Source commit: `618402b4817bcc6e41ce6a5e76bf170b1f47de71`

### MEDIUM · src/report_exporter.py
- Agent: `integrity_inspector`
- Status: `CODE FACT`
- Description: unversioned serialization
- Reasoning: AST detector emitted this observation: unversioned-serialization.
- Source commit: `ac17b416164f77b097dd3dd6cec1c7cf09ab5a4e`

### MEDIUM · src/stylometry_core/commit_atomicity_core.py
- Agent: `integrity_inspector`
- Status: `CODE FACT`
- Description: unversioned serialization
- Reasoning: AST detector emitted this observation: unversioned-serialization.
- Source commit: `ac17b416164f77b097dd3dd6cec1c7cf09ab5a4e`

### MEDIUM · src/stylometry_core/syntax_fingerprint_core.py
- Agent: `integrity_inspector`
- Status: `CODE FACT`
- Description: unversioned serialization
- Reasoning: AST detector emitted this observation: unversioned-serialization.
- Source commit: `ac17b416164f77b097dd3dd6cec1c7cf09ab5a4e`

### MEDIUM · src/stylometry_core/identifier_fingerprint_core.py
- Agent: `integrity_inspector`
- Status: `CODE FACT`
- Description: unversioned serialization
- Reasoning: AST detector emitted this observation: unversioned-serialization.
- Source commit: `ac17b416164f77b097dd3dd6cec1c7cf09ab5a4e`

## Limitations

- Hypotheses require module 3 verification; parser candidates may receive isolated induction, while unsupported families remain AST-only.
- 210 discovered file(s) were skipped; see skipped_reasons for the exact paths and policy categories.
- 15 triaged module(s) were outside CONNECTED_ALIVE audit scope.
- 12 skill applicability result(s) were UNDETERMINED; no conclusion was inferred for them.
