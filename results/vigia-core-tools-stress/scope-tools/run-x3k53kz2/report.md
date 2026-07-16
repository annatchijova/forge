# FORGE audit report

Repository: `/home/labestiadevigia/vigia-repo/vigia/tools`
Seal: **VERIFIED**
Findings: **43** · Discarded hypotheses: **3**
Coverage: **33/59 (55.9%)**
Audit disposition: **ABSTAIN_INSUFFICIENT_SCOPE**

## Repository profile

- Modules: 33 (16 connected)
- Domains: cryptographic, input_boundary, machine_learning
- Audit duration: 2.909736 seconds

## Findings

### MEDIUM · adversarial_nlp.py
- Agent: `bug_investigator`
- Status: `PLAUSIBLE HYPOTHESIS`
- Description: The parser call `return json.load(f)` at adversarial_nlp.py:177 has no nearby exception handling, so malformed input may escape as an opaque failure.
- Reasoning: Observed construct matches; induction was undetermined: Target module could not be loaded in its package context: ModuleNotFoundError: No module named 'vigia'
- Source commit: `5cddf9560b7e3fd2ef67a94dd26f3d7efd780c33`

### MEDIUM · adversarial_nlp.py
- Agent: `bug_investigator`
- Status: `PLAUSIBLE HYPOTHESIS`
- Description: The decision comparison `verdict    = "FABRICADO" if mcp >= 4.0 else "SOSPECHOSO" if mcp >= 2.5 else "AUTÉNTICO"` at adversarial_nlp.py:1130 uses a binary float threshold, so rounding at the boundary may flip the result.
- Reasoning: Observed construct matches; induction was undetermined: No executable harness is registered for this hypothesis family.
- Source commit: `5cddf9560b7e3fd2ef67a94dd26f3d7efd780c33`

### MEDIUM · document_integrity.py
- Agent: `bug_investigator`
- Status: `PLAUSIBLE HYPOTHESIS`
- Description: The decision comparison `if score >= 0.7:` at document_integrity.py:81 uses a binary float threshold, so rounding at the boundary may flip the result.
- Reasoning: Observed construct matches; induction was undetermined: No executable harness is registered for this hypothesis family.
- Source commit: `86de69e90eebfc5b3dc9c3b47bea37e827f75ce1`

### MEDIUM · document_integrity.py
- Agent: `bug_investigator`
- Status: `PLAUSIBLE HYPOTHESIS`
- Description: The decision comparison `if score >= 0.4:` at document_integrity.py:83 uses a binary float threshold, so rounding at the boundary may flip the result.
- Reasoning: Observed construct matches; induction was undetermined: No executable harness is registered for this hypothesis family.
- Source commit: `86de69e90eebfc5b3dc9c3b47bea37e827f75ce1`

### MEDIUM · vigia_planner.py
- Agent: `bug_investigator`
- Status: `PLAUSIBLE HYPOTHESIS`
- Description: The decision comparison `f"CLIP visual_malice_score={score:.3f} > 0.4. "` at vigia_planner.py:343 uses a binary float threshold, so rounding at the boundary may flip the result.
- Reasoning: Observed construct matches; induction was undetermined: No executable harness is registered for this hypothesis family.
- Source commit: `64e6f95cd5f39c76428ddd4ef1d5f8b6a69c1b4e`

### MEDIUM · vigia_planner.py
- Agent: `bug_investigator`
- Status: `PLAUSIBLE HYPOTHESIS`
- Description: The decision comparison `if score >= 0.5:` at vigia_planner.py:796 uses a binary float threshold, so rounding at the boundary may flip the result.
- Reasoning: Observed construct matches; induction was undetermined: No executable harness is registered for this hypothesis family.
- Source commit: `64e6f95cd5f39c76428ddd4ef1d5f8b6a69c1b4e`

### MEDIUM · vigia_planner.py
- Agent: `bug_investigator`
- Status: `PLAUSIBLE HYPOTHESIS`
- Description: The decision comparison `elif score >= 0.2:` at vigia_planner.py:798 uses a binary float threshold, so rounding at the boundary may flip the result.
- Reasoning: Observed construct matches; induction was undetermined: No executable harness is registered for this hypothesis family.
- Source commit: `64e6f95cd5f39c76428ddd4ef1d5f8b6a69c1b4e`

### MEDIUM · mitre_mapping.py
- Agent: `security_auditor`
- Status: `CODE FACT`
- Description: non-empty credential-like string assigned to CREDENTIAL_ACCESS
- Reasoning: AST detector emitted this observation: hardcoded-credential.
- Source commit: `6ea18c6675815329c7fb39696ec27a06b15b183f`

### CRITICAL · document_integrity.py
- Agent: `security_auditor`
- Status: `CODE FACT`
- Description: parameter reaches open() without proven normalization
- Reasoning: AST detector emitted this observation: path-traversal.
- Source commit: `86de69e90eebfc5b3dc9c3b47bea37e827f75ce1`

### CRITICAL · document_integrity.py
- Agent: `security_auditor`
- Status: `CODE FACT`
- Description: parameter reaches open() without proven normalization
- Reasoning: AST detector emitted this observation: path-traversal.
- Source commit: `86de69e90eebfc5b3dc9c3b47bea37e827f75ce1`

### CRITICAL · metabolic_profiler.py
- Agent: `security_auditor`
- Status: `CODE FACT`
- Description: parameter reaches open() without proven normalization
- Reasoning: AST detector emitted this observation: path-traversal.
- Source commit: `b0cb16c83a8358d65b17a01a49c8ae5fa1547dfd`

### CRITICAL · metabolic_profiler.py
- Agent: `security_auditor`
- Status: `CODE FACT`
- Description: parameter reaches open() without proven normalization
- Reasoning: AST detector emitted this observation: path-traversal.
- Source commit: `b0cb16c83a8358d65b17a01a49c8ae5fa1547dfd`

### CRITICAL · metabolic_profiler.py
- Agent: `security_auditor`
- Status: `CODE FACT`
- Description: parameter reaches open() without proven normalization
- Reasoning: AST detector emitted this observation: path-traversal.
- Source commit: `b0cb16c83a8358d65b17a01a49c8ae5fa1547dfd`

### CRITICAL · metabolic_profiler.py
- Agent: `security_auditor`
- Status: `CODE FACT`
- Description: parameter reaches open() without proven normalization
- Reasoning: AST detector emitted this observation: path-traversal.
- Source commit: `b0cb16c83a8358d65b17a01a49c8ae5fa1547dfd`

### CRITICAL · metabolic_profiler.py
- Agent: `security_auditor`
- Status: `CODE FACT`
- Description: parameter reaches open() without proven normalization
- Reasoning: AST detector emitted this observation: path-traversal.
- Source commit: `b0cb16c83a8358d65b17a01a49c8ae5fa1547dfd`

### MEDIUM · signal_contract.py
- Agent: `integrity_inspector`
- Status: `CODE FACT`
- Description: non-deterministic arithmetic in a decision-adjacent path
- Reasoning: AST detector emitted this observation: decision-adjacent-float.
- Source commit: `64e6f95cd5f39c76428ddd4ef1d5f8b6a69c1b4e`

### MEDIUM · vigia_planner.py
- Agent: `integrity_inspector`
- Status: `CODE FACT`
- Description: non-deterministic arithmetic in a decision-adjacent path
- Reasoning: AST detector emitted this observation: decision-adjacent-float.
- Source commit: `64e6f95cd5f39c76428ddd4ef1d5f8b6a69c1b4e`

### MEDIUM · vigia_planner.py
- Agent: `integrity_inspector`
- Status: `CODE FACT`
- Description: unversioned serialization
- Reasoning: AST detector emitted this observation: unversioned-serialization.
- Source commit: `64e6f95cd5f39c76428ddd4ef1d5f8b6a69c1b4e`

### MEDIUM · vigia_planner.py
- Agent: `integrity_inspector`
- Status: `CODE FACT`
- Description: unversioned serialization
- Reasoning: AST detector emitted this observation: unversioned-serialization.
- Source commit: `64e6f95cd5f39c76428ddd4ef1d5f8b6a69c1b4e`

### MEDIUM · vigia_planner.py
- Agent: `integrity_inspector`
- Status: `CODE FACT`
- Description: unversioned serialization
- Reasoning: AST detector emitted this observation: unversioned-serialization.
- Source commit: `64e6f95cd5f39c76428ddd4ef1d5f8b6a69c1b4e`

### MEDIUM · vigia_planner.py
- Agent: `integrity_inspector`
- Status: `CODE FACT`
- Description: unversioned serialization
- Reasoning: AST detector emitted this observation: unversioned-serialization.
- Source commit: `64e6f95cd5f39c76428ddd4ef1d5f8b6a69c1b4e`

### MEDIUM · vigia_planner.py
- Agent: `integrity_inspector`
- Status: `CODE FACT`
- Description: unversioned serialization
- Reasoning: AST detector emitted this observation: unversioned-serialization.
- Source commit: `64e6f95cd5f39c76428ddd4ef1d5f8b6a69c1b4e`

### MEDIUM · vigia_planner.py
- Agent: `integrity_inspector`
- Status: `CODE FACT`
- Description: unversioned serialization
- Reasoning: AST detector emitted this observation: unversioned-serialization.
- Source commit: `64e6f95cd5f39c76428ddd4ef1d5f8b6a69c1b4e`

### MEDIUM · vigia_planner.py
- Agent: `integrity_inspector`
- Status: `CODE FACT`
- Description: unversioned serialization
- Reasoning: AST detector emitted this observation: unversioned-serialization.
- Source commit: `64e6f95cd5f39c76428ddd4ef1d5f8b6a69c1b4e`

### MEDIUM · entropy_kernel.py
- Agent: `integrity_inspector`
- Status: `CODE FACT`
- Description: non-deterministic arithmetic in a decision-adjacent path
- Reasoning: AST detector emitted this observation: decision-adjacent-float.
- Source commit: `31df9fc2610c92c0946b262446ab5d82cbb57094`

### MEDIUM · entropy_kernel.py
- Agent: `integrity_inspector`
- Status: `CODE FACT`
- Description: non-deterministic arithmetic in a decision-adjacent path
- Reasoning: AST detector emitted this observation: decision-adjacent-float.
- Source commit: `31df9fc2610c92c0946b262446ab5d82cbb57094`

### MEDIUM · adversarial_nlp.py
- Agent: `integrity_inspector`
- Status: `CODE FACT`
- Description: unversioned serialization
- Reasoning: AST detector emitted this observation: unversioned-serialization.
- Source commit: `5cddf9560b7e3fd2ef67a94dd26f3d7efd780c33`

### MEDIUM · mitre_mapping.py
- Agent: `integrity_inspector`
- Status: `CODE FACT`
- Description: unversioned serialization
- Reasoning: AST detector emitted this observation: unversioned-serialization.
- Source commit: `64e6f95cd5f39c76428ddd4ef1d5f8b6a69c1b4e`

### MEDIUM · mitre_mapping.py
- Agent: `integrity_inspector`
- Status: `CODE FACT`
- Description: unversioned serialization
- Reasoning: AST detector emitted this observation: unversioned-serialization.
- Source commit: `6ea18c6675815329c7fb39696ec27a06b15b183f`

### MEDIUM · forensic_db.py
- Agent: `integrity_inspector`
- Status: `CODE FACT`
- Description: unversioned serialization
- Reasoning: AST detector emitted this observation: unversioned-serialization.
- Source commit: `5613cb9efc16d1c1733ef56dce36aa7d3157b082`

### MEDIUM · forensic_db.py
- Agent: `integrity_inspector`
- Status: `CODE FACT`
- Description: unversioned serialization
- Reasoning: AST detector emitted this observation: unversioned-serialization.
- Source commit: `5613cb9efc16d1c1733ef56dce36aa7d3157b082`

### MEDIUM · forensic_db.py
- Agent: `integrity_inspector`
- Status: `CODE FACT`
- Description: unversioned serialization
- Reasoning: AST detector emitted this observation: unversioned-serialization.
- Source commit: `5613cb9efc16d1c1733ef56dce36aa7d3157b082`

### MEDIUM · forensic_db.py
- Agent: `integrity_inspector`
- Status: `CODE FACT`
- Description: unversioned serialization
- Reasoning: AST detector emitted this observation: unversioned-serialization.
- Source commit: `5613cb9efc16d1c1733ef56dce36aa7d3157b082`

### MEDIUM · forensic_db.py
- Agent: `integrity_inspector`
- Status: `CODE FACT`
- Description: unversioned serialization
- Reasoning: AST detector emitted this observation: unversioned-serialization.
- Source commit: `5613cb9efc16d1c1733ef56dce36aa7d3157b082`

### MEDIUM · forensic_db.py
- Agent: `integrity_inspector`
- Status: `CODE FACT`
- Description: unversioned serialization
- Reasoning: AST detector emitted this observation: unversioned-serialization.
- Source commit: `5613cb9efc16d1c1733ef56dce36aa7d3157b082`

### MEDIUM · caie.py
- Agent: `integrity_inspector`
- Status: `CODE FACT`
- Description: non-deterministic arithmetic in a decision-adjacent path
- Reasoning: AST detector emitted this observation: decision-adjacent-float.
- Source commit: `35c21915fa6a0d821bf4e9fcc02abcfb16fb82f7`

### MEDIUM · caie.py
- Agent: `integrity_inspector`
- Status: `CODE FACT`
- Description: unversioned serialization
- Reasoning: AST detector emitted this observation: unversioned-serialization.
- Source commit: `5cddf9560b7e3fd2ef67a94dd26f3d7efd780c33`

### MEDIUM · document_integrity.py
- Agent: `validate-at-the-boundary`
- Status: `PROTOCOL_GAP`
- Description: parameter `path` reaches a sensitive boundary call without an explicit raising validation
- Reasoning: validate-at-the-boundary applies because direct external input reaches a parser or filesystem call.
- Source commit: `86de69e90eebfc5b3dc9c3b47bea37e827f75ce1`

### MEDIUM · metabolic_profiler.py
- Agent: `validate-at-the-boundary`
- Status: `PROTOCOL_GAP`
- Description: parameter `path` reaches a sensitive boundary call without an explicit raising validation
- Reasoning: validate-at-the-boundary applies because direct external input reaches a parser or filesystem call.
- Source commit: `b0cb16c83a8358d65b17a01a49c8ae5fa1547dfd`

### MEDIUM · metabolic_profiler.py
- Agent: `validate-at-the-boundary`
- Status: `PROTOCOL_GAP`
- Description: parameter `path` reaches a sensitive boundary call without an explicit raising validation
- Reasoning: validate-at-the-boundary applies because direct external input reaches a parser or filesystem call.
- Source commit: `b0cb16c83a8358d65b17a01a49c8ae5fa1547dfd`

### MEDIUM · metabolic_profiler.py
- Agent: `validate-at-the-boundary`
- Status: `PROTOCOL_GAP`
- Description: parameter `path` reaches a sensitive boundary call without an explicit raising validation
- Reasoning: validate-at-the-boundary applies because direct external input reaches a parser or filesystem call.
- Source commit: `b0cb16c83a8358d65b17a01a49c8ae5fa1547dfd`

### MEDIUM · metabolic_profiler.py
- Agent: `validate-at-the-boundary`
- Status: `PROTOCOL_GAP`
- Description: parameter `path` reaches a sensitive boundary call without an explicit raising validation
- Reasoning: validate-at-the-boundary applies because direct external input reaches a parser or filesystem call.
- Source commit: `b0cb16c83a8358d65b17a01a49c8ae5fa1547dfd`

### MEDIUM · metabolic_profiler.py
- Agent: `validate-at-the-boundary`
- Status: `PROTOCOL_GAP`
- Description: parameter `path` reaches a sensitive boundary call without an explicit raising validation
- Reasoning: validate-at-the-boundary applies because direct external input reaches a parser or filesystem call.
- Source commit: `b0cb16c83a8358d65b17a01a49c8ae5fa1547dfd`

## Limitations

- Hypotheses require module 3 verification; parser candidates may receive isolated induction, while unsupported families remain AST-only.
- 26 discovered file(s) were skipped; see skipped_reasons for the exact paths and policy categories.
- 17 triaged module(s) were outside CONNECTED_ALIVE audit scope.
- 11 skill applicability result(s) were UNDETERMINED; no conclusion was inferred for them.
- 7 hypothesis/hypotheses survived structural verification without dynamic induction; they remain plausible hypotheses, not confirmed defects.
