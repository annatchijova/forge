# FORGE audit report

Repository: `/tmp/forge-vigia-production-view`
Seal: **VERIFIED**
Findings: **212** · Discarded hypotheses: **5**
Finding-set digest: `fe505cd792686799362763b7dbb8fb77e686db49dc3ab73eb6f53426f5ba773c`
Eligible source coverage: **167/167 (100.0%)**
Discovery accounting: **167/343 discovered files**
Audit disposition: **ABSTAIN_INSUFFICIENT_SCOPE**

## Repository profile

- Modules: 167 (77 connected)
- Domains: audit_or_ledger, cryptographic, determinism_sensitive, input_boundary, machine_learning, serialization_or_persistence
- Audit duration: 16.439269 seconds

## Findings

### MEDIUM · vigia/core/entanglement.py
- Agent: `bug_investigator`
- Status: `PLAUSIBLE HYPOTHESIS`
- Description: The decision comparison `return score >= 2.0, max(1, len(strong)), min(1.0, score / 5.0)` at vigia/core/entanglement.py:505 uses a binary float threshold, so rounding at the boundary may flip the result.
- Reasoning: Observed construct matches; induction was undetermined: No supported float(x) comparison shape was found for differential induction.
- Source commit: unavailable (source evidence retained)

### MEDIUM · vigia/core/lr_calibration.py
- Agent: `bug_investigator`
- Status: `PLAUSIBLE HYPOTHESIS`
- Description: The parser call `data = json.load(f)` at vigia/core/lr_calibration.py:490 has no nearby exception handling, so malformed input may escape as an opaque failure.
- Reasoning: Observed construct matches, but induction only established that an error path is reachable: Malformed input reached an opaque AttributeError, but the exception did not originate at the hypothesized parser call. Evidence: vigia/core/lr_calibration.py:490: AttributeError: module 'vigia.core.lr_calibration' has no attribute 'load'
- Source commit: unavailable (source evidence retained)

### MEDIUM · vigia/pipeline/pipeline.py
- Agent: `bug_investigator`
- Status: `PLAUSIBLE HYPOTHESIS`
- Description: The dynamic command invocation `proc = subprocess.run(` at vigia/pipeline/pipeline.py:1165 may pass attacker-controlled arguments without an enclosing failure boundary.
- Reasoning: Observed construct matches; induction was undetermined: Target module could not be loaded in its package context: TypeError: function() argument 'code' must be code, not str
- Source commit: unavailable (source evidence retained)

### MEDIUM · vigia/pipeline/pipeline.py
- Agent: `bug_investigator`
- Status: `PLAUSIBLE HYPOTHESIS`
- Description: The parser call `bundle_dict = json.load(f)` at vigia/pipeline/pipeline.py:1272 has no nearby exception handling, so malformed input may escape as an opaque failure.
- Reasoning: Observed construct matches; induction was undetermined: Target module could not be loaded in its package context: TypeError: function() argument 'code' must be code, not str
- Source commit: unavailable (source evidence retained)

### MEDIUM · vigia/pipeline/pipeline.py
- Agent: `bug_investigator`
- Status: `PLAUSIBLE HYPOTHESIS`
- Description: The parser call `bundle_dict = json.load(f)` at vigia/pipeline/pipeline.py:1328 has no nearby exception handling, so malformed input may escape as an opaque failure.
- Reasoning: Observed construct matches; induction was undetermined: Target module could not be loaded in its package context: TypeError: function() argument 'code' must be code, not str
- Source commit: unavailable (source evidence retained)

### MEDIUM · vigia/pipeline/vigia_integration_bridge.py
- Agent: `bug_investigator`
- Status: `PLAUSIBLE HYPOTHESIS`
- Description: The parser call `sealed_dict = json.loads(result["bundle_json"])` at vigia/pipeline/vigia_integration_bridge.py:1189 has no nearby exception handling, so malformed input may escape as an opaque failure.
- Reasoning: Observed construct matches; induction was undetermined: Target module could not be loaded in its package context: TypeError: function() argument 'code' must be code, not str
- Source commit: unavailable (source evidence retained)

### MEDIUM · vigia/pipeline/vigia_integration_bridge.py
- Agent: `bug_investigator`
- Status: `PLAUSIBLE HYPOTHESIS`
- Description: The parser call `case = json.load(f)` at vigia/pipeline/vigia_integration_bridge.py:1299 has no nearby exception handling, so malformed input may escape as an opaque failure.
- Reasoning: Observed construct matches; induction was undetermined: Target module could not be loaded in its package context: TypeError: function() argument 'code' must be code, not str
- Source commit: unavailable (source evidence retained)

### MEDIUM · vigia/sift/disk_forensics.py
- Agent: `bug_investigator`
- Status: `PLAUSIBLE HYPOTHESIS`
- Description: The parser call `entries = self._parse(json.loads(parsed_json or "{}").get("entries", []))` at vigia/sift/disk_forensics.py:131 has no nearby exception handling, so malformed input may escape as an opaque failure.
- Reasoning: Observed construct matches; induction was undetermined: Target module could not be loaded in its package context: TypeError: function() argument 'code' must be code, not str
- Source commit: unavailable (source evidence retained)

### MEDIUM · vigia/sift/event_log_correlator.py
- Agent: `bug_investigator`
- Status: `PLAUSIBLE HYPOTHESIS`
- Description: The parser call `tree = ET.parse(xml_path)` at vigia/sift/event_log_correlator.py:187 has no nearby exception handling, so malformed input may escape as an opaque failure.
- Reasoning: Observed construct matches; induction was undetermined: Target module could not be loaded in its package context: TypeError: function() argument 'code' must be code, not str
- Source commit: unavailable (source evidence retained)

### MEDIUM · vigia/sift/registry_timeline_reconstructor.py
- Agent: `bug_investigator`
- Status: `PLAUSIBLE HYPOTHESIS`
- Description: The dynamic command invocation `result = subprocess.run(` at vigia/sift/registry_timeline_reconstructor.py:189 may pass attacker-controlled arguments without an enclosing failure boundary.
- Reasoning: Observed construct matches; induction was undetermined: Target module could not be loaded in its package context: TypeError: function() argument 'code' must be code, not str
- Source commit: unavailable (source evidence retained)

### MEDIUM · vigia/sift/sift_orchestrator.py
- Agent: `bug_investigator`
- Status: `PLAUSIBLE HYPOTHESIS`
- Description: The parser call `mft_bytes = json.dumps(json.loads(mft_json), sort_keys=True, separators=(",", ":")).encode()` at vigia/sift/sift_orchestrator.py:507 has no nearby exception handling, so malformed input may escape as an opaque failure.
- Reasoning: Observed construct matches; induction was undetermined: Target module could not be loaded in its package context: TypeError: function() argument 'code' must be code, not str
- Source commit: unavailable (source evidence retained)

### MEDIUM · vigia/tools/adversarial_nlp.py
- Agent: `bug_investigator`
- Status: `PLAUSIBLE HYPOTHESIS`
- Description: The parser call `return json.load(f)` at vigia/tools/adversarial_nlp.py:177 has no nearby exception handling, so malformed input may escape as an opaque failure.
- Reasoning: Observed construct matches; induction was undetermined: Target module could not be loaded in its package context: TypeError: function() argument 'code' must be code, not str
- Source commit: unavailable (source evidence retained)

### MEDIUM · vigia/sift/memory_forensics.py
- Agent: `security_auditor`
- Status: `CODE FACT`
- Description: parameter reaches os.path operation without proven normalization
- Reasoning: AST detector emitted this observation: path-traversal.
- Source commit: unavailable (source evidence retained)

### MEDIUM · vigia/sift/memory_forensics.py
- Agent: `security_auditor`
- Status: `CODE FACT`
- Description: parameter reaches os.path operation without proven normalization
- Reasoning: AST detector emitted this observation: path-traversal.
- Source commit: unavailable (source evidence retained)

### MEDIUM · vigia/sift/memory_forensics.py
- Agent: `security_auditor`
- Status: `CODE FACT`
- Description: parameter reaches os.path operation without proven normalization
- Reasoning: AST detector emitted this observation: path-traversal.
- Source commit: unavailable (source evidence retained)

### MEDIUM · vigia/sift/browser_forensics.py
- Agent: `security_auditor`
- Status: `CODE FACT`
- Description: unsafe SQL interpolation reaches execute() without parameter binding
- Reasoning: AST detector emitted this observation: sql-injection.
- Source commit: unavailable (source evidence retained)

### MEDIUM · vigia/sift/_sql_utils.py
- Agent: `security_auditor`
- Status: `CODE FACT`
- Description: parameter reaches os.path operation without proven normalization
- Reasoning: AST detector emitted this observation: path-traversal.
- Source commit: unavailable (source evidence retained)

### MEDIUM · vigia/sift/_sql_utils.py
- Agent: `security_auditor`
- Status: `CODE FACT`
- Description: parameter reaches os.path operation without proven normalization
- Reasoning: AST detector emitted this observation: path-traversal.
- Source commit: unavailable (source evidence retained)

### MEDIUM · vigia/sift/registry_timeline_reconstructor.py
- Agent: `security_auditor`
- Status: `CODE FACT`
- Description: parameter reaches os.path operation without proven normalization
- Reasoning: AST detector emitted this observation: path-traversal.
- Source commit: unavailable (source evidence retained)

### MEDIUM · vigia/sift/registry_timeline_reconstructor.py
- Agent: `security_auditor`
- Status: `CODE FACT`
- Description: parameter reaches os.path operation without proven normalization
- Reasoning: AST detector emitted this observation: path-traversal.
- Source commit: unavailable (source evidence retained)

### MEDIUM · vigia/security/security.py
- Agent: `security_auditor`
- Status: `CODE FACT`
- Description: parameter reaches open() without proven normalization
- Reasoning: AST detector emitted this observation: path-traversal.
- Source commit: unavailable (source evidence retained)

### MEDIUM · vigia/security/security.py
- Agent: `security_auditor`
- Status: `CODE FACT`
- Description: parameter reaches open() without proven normalization
- Reasoning: AST detector emitted this observation: path-traversal.
- Source commit: unavailable (source evidence retained)

### MEDIUM · vigia/security/security.py
- Agent: `security_auditor`
- Status: `CODE FACT`
- Description: parameter reaches open() without proven normalization
- Reasoning: AST detector emitted this observation: path-traversal.
- Source commit: unavailable (source evidence retained)

### MEDIUM · vigia/tools/adversarial_nlp.py
- Agent: `security_auditor`
- Status: `CODE FACT`
- Description: parameter reaches os.path operation without proven normalization
- Reasoning: AST detector emitted this observation: path-traversal.
- Source commit: unavailable (source evidence retained)

### MEDIUM · vigia/tools/adversarial_nlp.py
- Agent: `security_auditor`
- Status: `CODE FACT`
- Description: parameter reaches open() without proven normalization
- Reasoning: AST detector emitted this observation: path-traversal.
- Source commit: unavailable (source evidence retained)

### MEDIUM · vigia/tools/adversarial_nlp.py
- Agent: `security_auditor`
- Status: `CODE FACT`
- Description: parameter reaches os.path operation without proven normalization
- Reasoning: AST detector emitted this observation: path-traversal.
- Source commit: unavailable (source evidence retained)

### MEDIUM · vigia/tools/adversarial_nlp.py
- Agent: `security_auditor`
- Status: `CODE FACT`
- Description: parameter reaches os.path operation without proven normalization
- Reasoning: AST detector emitted this observation: path-traversal.
- Source commit: unavailable (source evidence retained)

### MEDIUM · vigia/tools/adversarial_nlp.py
- Agent: `security_auditor`
- Status: `CODE FACT`
- Description: parameter reaches os.path operation without proven normalization
- Reasoning: AST detector emitted this observation: path-traversal.
- Source commit: unavailable (source evidence retained)

### MEDIUM · vigia/tools/adversarial_nlp.py
- Agent: `security_auditor`
- Status: `CODE FACT`
- Description: parameter reaches os.path operation without proven normalization
- Reasoning: AST detector emitted this observation: path-traversal.
- Source commit: unavailable (source evidence retained)

### MEDIUM · vigia/tools/adversarial_nlp.py
- Agent: `security_auditor`
- Status: `CODE FACT`
- Description: parameter reaches open() without proven normalization
- Reasoning: AST detector emitted this observation: path-traversal.
- Source commit: unavailable (source evidence retained)

### MEDIUM · vigia/tools/adversarial_nlp.py
- Agent: `security_auditor`
- Status: `CODE FACT`
- Description: parameter reaches open() without proven normalization
- Reasoning: AST detector emitted this observation: path-traversal.
- Source commit: unavailable (source evidence retained)

### MEDIUM · vigia/tools/adversarial_nlp.py
- Agent: `security_auditor`
- Status: `CODE FACT`
- Description: parameter reaches open() without proven normalization
- Reasoning: AST detector emitted this observation: path-traversal.
- Source commit: unavailable (source evidence retained)

### MEDIUM · vigia/tools/mitre_mapping.py
- Agent: `security_auditor`
- Status: `CODE FACT`
- Description: non-empty credential-like string assigned to CREDENTIAL_ACCESS
- Reasoning: AST detector emitted this observation: hardcoded-credential.
- Source commit: unavailable (source evidence retained)

### MEDIUM · vigia/tools/visible_variables.py
- Agent: `security_auditor`
- Status: `CODE FACT`
- Description: non-empty credential-like string assigned to CREDENTIAL_ACCESS
- Reasoning: AST detector emitted this observation: hardcoded-credential.
- Source commit: unavailable (source evidence retained)

### MEDIUM · vigia/tools/document_integrity.py
- Agent: `security_auditor`
- Status: `CODE FACT`
- Description: parameter reaches os.path operation without proven normalization
- Reasoning: AST detector emitted this observation: path-traversal.
- Source commit: unavailable (source evidence retained)

### MEDIUM · vigia/tools/document_integrity.py
- Agent: `security_auditor`
- Status: `CODE FACT`
- Description: parameter reaches open() without proven normalization
- Reasoning: AST detector emitted this observation: path-traversal.
- Source commit: unavailable (source evidence retained)

### MEDIUM · vigia/tools/document_integrity.py
- Agent: `security_auditor`
- Status: `CODE FACT`
- Description: parameter reaches os.path operation without proven normalization
- Reasoning: AST detector emitted this observation: path-traversal.
- Source commit: unavailable (source evidence retained)

### MEDIUM · vigia/tools/document_integrity.py
- Agent: `security_auditor`
- Status: `CODE FACT`
- Description: parameter reaches os.path operation without proven normalization
- Reasoning: AST detector emitted this observation: path-traversal.
- Source commit: unavailable (source evidence retained)

### MEDIUM · vigia/tools/document_integrity.py
- Agent: `security_auditor`
- Status: `CODE FACT`
- Description: parameter reaches os.path operation without proven normalization
- Reasoning: AST detector emitted this observation: path-traversal.
- Source commit: unavailable (source evidence retained)

### MEDIUM · vigia/tools/document_integrity.py
- Agent: `security_auditor`
- Status: `CODE FACT`
- Description: parameter reaches open() without proven normalization
- Reasoning: AST detector emitted this observation: path-traversal.
- Source commit: unavailable (source evidence retained)

### MEDIUM · vigia/tools/forensic_db.py
- Agent: `security_auditor`
- Status: `CODE FACT`
- Description: parameter reaches os.path operation without proven normalization
- Reasoning: AST detector emitted this observation: path-traversal.
- Source commit: unavailable (source evidence retained)

### MEDIUM · vigia/tools/forensic_db.py
- Agent: `security_auditor`
- Status: `CODE FACT`
- Description: parameter reaches os.path operation without proven normalization
- Reasoning: AST detector emitted this observation: path-traversal.
- Source commit: unavailable (source evidence retained)

### MEDIUM · vigia/tools/forensic_db.py
- Agent: `security_auditor`
- Status: `CODE FACT`
- Description: parameter reaches os.path operation without proven normalization
- Reasoning: AST detector emitted this observation: path-traversal.
- Source commit: unavailable (source evidence retained)

### MEDIUM · vigia/tools/forensic_db.py
- Agent: `security_auditor`
- Status: `CODE FACT`
- Description: parameter reaches os.path operation without proven normalization
- Reasoning: AST detector emitted this observation: path-traversal.
- Source commit: unavailable (source evidence retained)

### MEDIUM · vigia/tools/forensic_db.py
- Agent: `security_auditor`
- Status: `CODE FACT`
- Description: parameter reaches os.path operation without proven normalization
- Reasoning: AST detector emitted this observation: path-traversal.
- Source commit: unavailable (source evidence retained)

### MEDIUM · vigia/tools/forensic_db.py
- Agent: `security_auditor`
- Status: `CODE FACT`
- Description: parameter reaches os.path operation without proven normalization
- Reasoning: AST detector emitted this observation: path-traversal.
- Source commit: unavailable (source evidence retained)

### MEDIUM · vigia/tools/forensic_db.py
- Agent: `security_auditor`
- Status: `CODE FACT`
- Description: parameter reaches os.path operation without proven normalization
- Reasoning: AST detector emitted this observation: path-traversal.
- Source commit: unavailable (source evidence retained)

### MEDIUM · vigia/tools/forensic_db.py
- Agent: `security_auditor`
- Status: `CODE FACT`
- Description: parameter reaches open() without proven normalization
- Reasoning: AST detector emitted this observation: path-traversal.
- Source commit: unavailable (source evidence retained)

### MEDIUM · vigia/tools/forensic_db.py
- Agent: `security_auditor`
- Status: `CODE FACT`
- Description: parameter reaches os.path operation without proven normalization
- Reasoning: AST detector emitted this observation: path-traversal.
- Source commit: unavailable (source evidence retained)

### MEDIUM · vigia/tools/forensic_db.py
- Agent: `security_auditor`
- Status: `CODE FACT`
- Description: parameter reaches os.path operation without proven normalization
- Reasoning: AST detector emitted this observation: path-traversal.
- Source commit: unavailable (source evidence retained)

### MEDIUM · vigia/tools/forensic_db.py
- Agent: `security_auditor`
- Status: `CODE FACT`
- Description: parameter reaches os.path operation without proven normalization
- Reasoning: AST detector emitted this observation: path-traversal.
- Source commit: unavailable (source evidence retained)

### MEDIUM · vigia/tools/forensic_db.py
- Agent: `security_auditor`
- Status: `CODE FACT`
- Description: parameter reaches os.path operation without proven normalization
- Reasoning: AST detector emitted this observation: path-traversal.
- Source commit: unavailable (source evidence retained)

### MEDIUM · vigia/tools/forensic_db.py
- Agent: `security_auditor`
- Status: `CODE FACT`
- Description: parameter reaches os.path operation without proven normalization
- Reasoning: AST detector emitted this observation: path-traversal.
- Source commit: unavailable (source evidence retained)

### MEDIUM · vigia/tools/forensic_db.py
- Agent: `security_auditor`
- Status: `CODE FACT`
- Description: parameter reaches os.path operation without proven normalization
- Reasoning: AST detector emitted this observation: path-traversal.
- Source commit: unavailable (source evidence retained)

### MEDIUM · vigia/tools/forensic_db.py
- Agent: `security_auditor`
- Status: `CODE FACT`
- Description: parameter reaches os.path operation without proven normalization
- Reasoning: AST detector emitted this observation: path-traversal.
- Source commit: unavailable (source evidence retained)

### MEDIUM · vigia/tools/forensic_db.py
- Agent: `security_auditor`
- Status: `CODE FACT`
- Description: parameter reaches os.path operation without proven normalization
- Reasoning: AST detector emitted this observation: path-traversal.
- Source commit: unavailable (source evidence retained)

### MEDIUM · vigia/tools/forensic_db.py
- Agent: `security_auditor`
- Status: `CODE FACT`
- Description: parameter reaches os.path operation without proven normalization
- Reasoning: AST detector emitted this observation: path-traversal.
- Source commit: unavailable (source evidence retained)

### MEDIUM · vigia/pipeline/pipeline.py
- Agent: `security_auditor`
- Status: `CODE FACT`
- Description: parameter reaches open() without proven normalization
- Reasoning: AST detector emitted this observation: path-traversal.
- Source commit: unavailable (source evidence retained)

### MEDIUM · vigia/pipeline/pipeline.py
- Agent: `security_auditor`
- Status: `CODE FACT`
- Description: parameter reaches open() without proven normalization
- Reasoning: AST detector emitted this observation: path-traversal.
- Source commit: unavailable (source evidence retained)

### MEDIUM · vigia/pipeline/vigia_integration_bridge.py
- Agent: `security_auditor`
- Status: `CODE FACT`
- Description: parameter reaches os.path operation without proven normalization
- Reasoning: AST detector emitted this observation: path-traversal.
- Source commit: unavailable (source evidence retained)

### MEDIUM · vigia/pipeline/vigia_integration_bridge.py
- Agent: `security_auditor`
- Status: `CODE FACT`
- Description: parameter reaches os.path operation without proven normalization
- Reasoning: AST detector emitted this observation: path-traversal.
- Source commit: unavailable (source evidence retained)

### MEDIUM · vigia/pipeline/vigia_integration_bridge.py
- Agent: `security_auditor`
- Status: `CODE FACT`
- Description: parameter reaches os.path operation without proven normalization
- Reasoning: AST detector emitted this observation: path-traversal.
- Source commit: unavailable (source evidence retained)

### MEDIUM · vigia/pipeline/vigia_integration_bridge.py
- Agent: `security_auditor`
- Status: `CODE FACT`
- Description: parameter reaches os.path operation without proven normalization
- Reasoning: AST detector emitted this observation: path-traversal.
- Source commit: unavailable (source evidence retained)

### MEDIUM · vigia/core/bundle_builder.py
- Agent: `security_auditor`
- Status: `CODE FACT`
- Description: parameter reaches os.path operation without proven normalization
- Reasoning: AST detector emitted this observation: path-traversal.
- Source commit: unavailable (source evidence retained)

### MEDIUM · vigia/core/bundle_builder.py
- Agent: `security_auditor`
- Status: `CODE FACT`
- Description: parameter reaches os.path operation without proven normalization
- Reasoning: AST detector emitted this observation: path-traversal.
- Source commit: unavailable (source evidence retained)

### MEDIUM · vigia/core/bundle_builder.py
- Agent: `security_auditor`
- Status: `CODE FACT`
- Description: parameter reaches open() without proven normalization
- Reasoning: AST detector emitted this observation: path-traversal.
- Source commit: unavailable (source evidence retained)

### MEDIUM · vigia/core/chain_of_custody.py
- Agent: `security_auditor`
- Status: `CODE FACT`
- Description: parameter reaches open() without proven normalization
- Reasoning: AST detector emitted this observation: path-traversal.
- Source commit: unavailable (source evidence retained)

### MEDIUM · vigia/core/lr_calibration.py
- Agent: `security_auditor`
- Status: `CODE FACT`
- Description: parameter reaches open() without proven normalization
- Reasoning: AST detector emitted this observation: path-traversal.
- Source commit: unavailable (source evidence retained)

### MEDIUM · vigia/core/lr_calibration.py
- Agent: `security_auditor`
- Status: `CODE FACT`
- Description: parameter reaches open() without proven normalization
- Reasoning: AST detector emitted this observation: path-traversal.
- Source commit: unavailable (source evidence retained)

### MEDIUM · vigia/core/execution_logger.py
- Agent: `security_auditor`
- Status: `CODE FACT`
- Description: parameter reaches os.path operation without proven normalization
- Reasoning: AST detector emitted this observation: path-traversal.
- Source commit: unavailable (source evidence retained)

### MEDIUM · vigia/core/execution_logger.py
- Agent: `security_auditor`
- Status: `CODE FACT`
- Description: parameter reaches open() without proven normalization
- Reasoning: AST detector emitted this observation: path-traversal.
- Source commit: unavailable (source evidence retained)

### MEDIUM · vigia/core/entanglement.py
- Agent: `security_auditor`
- Status: `CODE FACT`
- Description: parameter reaches open() without proven normalization
- Reasoning: AST detector emitted this observation: path-traversal.
- Source commit: unavailable (source evidence retained)

### MEDIUM · vigia/core/entanglement.py
- Agent: `security_auditor`
- Status: `CODE FACT`
- Description: parameter reaches open() without proven normalization
- Reasoning: AST detector emitted this observation: path-traversal.
- Source commit: unavailable (source evidence retained)

### MEDIUM · vigia/core/atomic_io.py
- Agent: `security_auditor`
- Status: `CODE FACT`
- Description: parameter reaches os.path operation without proven normalization
- Reasoning: AST detector emitted this observation: path-traversal.
- Source commit: unavailable (source evidence retained)

### MEDIUM · vigia/core/atomic_io.py
- Agent: `security_auditor`
- Status: `CODE FACT`
- Description: parameter reaches os.path operation without proven normalization
- Reasoning: AST detector emitted this observation: path-traversal.
- Source commit: unavailable (source evidence retained)

### MEDIUM · vigia/forensics/rfc3161_chain.py
- Agent: `security_auditor`
- Status: `CODE FACT`
- Description: parameter reaches open() without proven normalization
- Reasoning: AST detector emitted this observation: path-traversal.
- Source commit: unavailable (source evidence retained)

### MEDIUM · vigia/forensics/vision_audit.py
- Agent: `security_auditor`
- Status: `CODE FACT`
- Description: parameter reaches open() without proven normalization
- Reasoning: AST detector emitted this observation: path-traversal.
- Source commit: unavailable (source evidence retained)

### MEDIUM · vigia/forensics/vision_audit.py
- Agent: `security_auditor`
- Status: `CODE FACT`
- Description: parameter reaches open() without proven normalization
- Reasoning: AST detector emitted this observation: path-traversal.
- Source commit: unavailable (source evidence retained)

### MEDIUM · vigia/forensics/vision_audit.py
- Agent: `security_auditor`
- Status: `CODE FACT`
- Description: parameter reaches os.path operation without proven normalization
- Reasoning: AST detector emitted this observation: path-traversal.
- Source commit: unavailable (source evidence retained)

### MEDIUM · vigia_scorer.py
- Agent: `integrity_inspector`
- Status: `CODE FACT`
- Description: non-deterministic arithmetic in a decision-adjacent path
- Reasoning: AST detector emitted this observation: decision-adjacent-float.
- Source commit: unavailable (source evidence retained)

### MEDIUM · vigia_scorer.py
- Agent: `integrity_inspector`
- Status: `CODE FACT`
- Description: non-deterministic arithmetic in a decision-adjacent path
- Reasoning: AST detector emitted this observation: decision-adjacent-float.
- Source commit: unavailable (source evidence retained)

### MEDIUM · vigia_scorer.py
- Agent: `integrity_inspector`
- Status: `CODE FACT`
- Description: non-deterministic arithmetic in a decision-adjacent path
- Reasoning: AST detector emitted this observation: decision-adjacent-float.
- Source commit: unavailable (source evidence retained)

### MEDIUM · vigia_scorer.py
- Agent: `integrity_inspector`
- Status: `CODE FACT`
- Description: non-deterministic arithmetic in a decision-adjacent path
- Reasoning: AST detector emitted this observation: decision-adjacent-float.
- Source commit: unavailable (source evidence retained)

### MEDIUM · vigia_scorer.py
- Agent: `integrity_inspector`
- Status: `CODE FACT`
- Description: non-deterministic arithmetic in a decision-adjacent path
- Reasoning: AST detector emitted this observation: decision-adjacent-float.
- Source commit: unavailable (source evidence retained)

### MEDIUM · vigia/sift/sift_orchestrator.py
- Agent: `integrity_inspector`
- Status: `CODE FACT`
- Description: unversioned serialization
- Reasoning: AST detector emitted this observation: unversioned-serialization.
- Source commit: unavailable (source evidence retained)

### MEDIUM · vigia/security/security.py
- Agent: `integrity_inspector`
- Status: `CODE FACT`
- Description: unversioned serialization
- Reasoning: AST detector emitted this observation: unversioned-serialization.
- Source commit: unavailable (source evidence retained)

### MEDIUM · vigia/security/security.py
- Agent: `integrity_inspector`
- Status: `CODE FACT`
- Description: unversioned serialization
- Reasoning: AST detector emitted this observation: unversioned-serialization.
- Source commit: unavailable (source evidence retained)

### MEDIUM · vigia/security/security.py
- Agent: `integrity_inspector`
- Status: `CODE FACT`
- Description: unversioned serialization
- Reasoning: AST detector emitted this observation: unversioned-serialization.
- Source commit: unavailable (source evidence retained)

### MEDIUM · vigia/tools/signal_contract.py
- Agent: `integrity_inspector`
- Status: `CODE FACT`
- Description: non-deterministic arithmetic in a decision-adjacent path
- Reasoning: AST detector emitted this observation: decision-adjacent-float.
- Source commit: unavailable (source evidence retained)

### MEDIUM · vigia/tools/adversarial_nlp.py
- Agent: `integrity_inspector`
- Status: `CODE FACT`
- Description: floating-point division touches a money-shaped value; no explicit float() call, so it bypasses decision-adjacent-float
- Reasoning: AST detector emitted this observation: money-as-float.
- Source commit: unavailable (source evidence retained)

### MEDIUM · vigia/tools/adversarial_nlp.py
- Agent: `integrity_inspector`
- Status: `CODE FACT`
- Description: floating-point division touches a money-shaped value; no explicit float() call, so it bypasses decision-adjacent-float
- Reasoning: AST detector emitted this observation: money-as-float.
- Source commit: unavailable (source evidence retained)

### MEDIUM · vigia/tools/adversarial_nlp.py
- Agent: `integrity_inspector`
- Status: `CODE FACT`
- Description: floating-point division touches a money-shaped value; no explicit float() call, so it bypasses decision-adjacent-float
- Reasoning: AST detector emitted this observation: money-as-float.
- Source commit: unavailable (source evidence retained)

### MEDIUM · vigia/tools/adversarial_nlp.py
- Agent: `integrity_inspector`
- Status: `CODE FACT`
- Description: floating-point division touches a money-shaped value; no explicit float() call, so it bypasses decision-adjacent-float
- Reasoning: AST detector emitted this observation: money-as-float.
- Source commit: unavailable (source evidence retained)

### MEDIUM · vigia/tools/adversarial_nlp.py
- Agent: `integrity_inspector`
- Status: `CODE FACT`
- Description: floating-point division touches a money-shaped value; no explicit float() call, so it bypasses decision-adjacent-float
- Reasoning: AST detector emitted this observation: money-as-float.
- Source commit: unavailable (source evidence retained)

### MEDIUM · vigia/tools/adversarial_nlp.py
- Agent: `integrity_inspector`
- Status: `CODE FACT`
- Description: unversioned serialization
- Reasoning: AST detector emitted this observation: unversioned-serialization.
- Source commit: unavailable (source evidence retained)

### MEDIUM · vigia/tools/mitre_mapping.py
- Agent: `integrity_inspector`
- Status: `CODE FACT`
- Description: unversioned serialization
- Reasoning: AST detector emitted this observation: unversioned-serialization.
- Source commit: unavailable (source evidence retained)

### MEDIUM · vigia/tools/visible_variables.py
- Agent: `integrity_inspector`
- Status: `CODE FACT`
- Description: unversioned serialization
- Reasoning: AST detector emitted this observation: unversioned-serialization.
- Source commit: unavailable (source evidence retained)

### MEDIUM · vigia/tools/visible_variables.py
- Agent: `integrity_inspector`
- Status: `CODE FACT`
- Description: unversioned serialization
- Reasoning: AST detector emitted this observation: unversioned-serialization.
- Source commit: unavailable (source evidence retained)

### MEDIUM · vigia/tools/eml_gci.py
- Agent: `integrity_inspector`
- Status: `CODE FACT`
- Description: floating-point division touches a money-shaped value; no explicit float() call, so it bypasses decision-adjacent-float
- Reasoning: AST detector emitted this observation: money-as-float.
- Source commit: unavailable (source evidence retained)

### MEDIUM · vigia/tools/eml_gci.py
- Agent: `integrity_inspector`
- Status: `CODE FACT`
- Description: floating-point division touches a money-shaped value; no explicit float() call, so it bypasses decision-adjacent-float
- Reasoning: AST detector emitted this observation: money-as-float.
- Source commit: unavailable (source evidence retained)

### MEDIUM · vigia/tools/caie.py
- Agent: `integrity_inspector`
- Status: `CODE FACT`
- Description: non-deterministic arithmetic in a decision-adjacent path
- Reasoning: AST detector emitted this observation: decision-adjacent-float.
- Source commit: unavailable (source evidence retained)

### MEDIUM · vigia/tools/caie.py
- Agent: `integrity_inspector`
- Status: `CODE FACT`
- Description: floating-point division touches a money-shaped value; no explicit float() call, so it bypasses decision-adjacent-float
- Reasoning: AST detector emitted this observation: money-as-float.
- Source commit: unavailable (source evidence retained)

### MEDIUM · vigia/tools/caie.py
- Agent: `integrity_inspector`
- Status: `CODE FACT`
- Description: unversioned serialization
- Reasoning: AST detector emitted this observation: unversioned-serialization.
- Source commit: unavailable (source evidence retained)

### MEDIUM · vigia/pipeline/vigia_integration_bridge.py
- Agent: `integrity_inspector`
- Status: `CODE FACT`
- Description: non-deterministic arithmetic in a decision-adjacent path
- Reasoning: AST detector emitted this observation: decision-adjacent-float.
- Source commit: unavailable (source evidence retained)

### MEDIUM · vigia/pipeline/vigia_integration_bridge.py
- Agent: `integrity_inspector`
- Status: `CODE FACT`
- Description: floating-point division touches a money-shaped value; no explicit float() call, so it bypasses decision-adjacent-float
- Reasoning: AST detector emitted this observation: money-as-float.
- Source commit: unavailable (source evidence retained)

### MEDIUM · vigia/pipeline/vigia_integration_bridge.py
- Agent: `integrity_inspector`
- Status: `CODE FACT`
- Description: unversioned serialization
- Reasoning: AST detector emitted this observation: unversioned-serialization.
- Source commit: unavailable (source evidence retained)

### MEDIUM · vigia/pipeline/vigia_integration_bridge.py
- Agent: `integrity_inspector`
- Status: `CODE FACT`
- Description: unversioned serialization
- Reasoning: AST detector emitted this observation: unversioned-serialization.
- Source commit: unavailable (source evidence retained)

### MEDIUM · vigia/verdict/quadripartite.py
- Agent: `integrity_inspector`
- Status: `CODE FACT`
- Description: unversioned serialization
- Reasoning: AST detector emitted this observation: unversioned-serialization.
- Source commit: unavailable (source evidence retained)

### MEDIUM · vigia/core/bundle_builder.py
- Agent: `integrity_inspector`
- Status: `CODE FACT`
- Description: unversioned serialization
- Reasoning: AST detector emitted this observation: unversioned-serialization.
- Source commit: unavailable (source evidence retained)

### MEDIUM · vigia/core/lr_calibration.py
- Agent: `integrity_inspector`
- Status: `CODE FACT`
- Description: unversioned serialization
- Reasoning: AST detector emitted this observation: unversioned-serialization.
- Source commit: unavailable (source evidence retained)

### MEDIUM · vigia/core/ebs_v1.py
- Agent: `integrity_inspector`
- Status: `CODE FACT`
- Description: non-deterministic arithmetic in a decision-adjacent path
- Reasoning: AST detector emitted this observation: decision-adjacent-float.
- Source commit: unavailable (source evidence retained)

### MEDIUM · vigia/core/forensic_adapter.py
- Agent: `integrity_inspector`
- Status: `CODE FACT`
- Description: unversioned serialization
- Reasoning: AST detector emitted this observation: unversioned-serialization.
- Source commit: unavailable (source evidence retained)

### MEDIUM · vigia/core/trust_fusion.py
- Agent: `integrity_inspector`
- Status: `CODE FACT`
- Description: binary float literal assigned to a money-shaped value
- Reasoning: AST detector emitted this observation: money-as-float.
- Source commit: unavailable (source evidence retained)

### MEDIUM · vigia/core/trust_fusion.py
- Agent: `integrity_inspector`
- Status: `CODE FACT`
- Description: unversioned serialization
- Reasoning: AST detector emitted this observation: unversioned-serialization.
- Source commit: unavailable (source evidence retained)

### MEDIUM · vigia/core/execution_logger.py
- Agent: `integrity_inspector`
- Status: `CODE FACT`
- Description: unversioned serialization
- Reasoning: AST detector emitted this observation: unversioned-serialization.
- Source commit: unavailable (source evidence retained)

### MEDIUM · vigia/core/execution_logger.py
- Agent: `integrity_inspector`
- Status: `CODE FACT`
- Description: unversioned serialization
- Reasoning: AST detector emitted this observation: unversioned-serialization.
- Source commit: unavailable (source evidence retained)

### MEDIUM · vigia/core/graph_stability.py
- Agent: `integrity_inspector`
- Status: `CODE FACT`
- Description: floating-point division touches a money-shaped value; no explicit float() call, so it bypasses decision-adjacent-float
- Reasoning: AST detector emitted this observation: money-as-float.
- Source commit: unavailable (source evidence retained)

### MEDIUM · vigia/core/graph_stability.py
- Agent: `integrity_inspector`
- Status: `CODE FACT`
- Description: floating-point division touches a money-shaped value; no explicit float() call, so it bypasses decision-adjacent-float
- Reasoning: AST detector emitted this observation: money-as-float.
- Source commit: unavailable (source evidence retained)

### MEDIUM · vigia/core/peirceplanner_bounded.py
- Agent: `integrity_inspector`
- Status: `CODE FACT`
- Description: floating-point division touches a money-shaped value; no explicit float() call, so it bypasses decision-adjacent-float
- Reasoning: AST detector emitted this observation: money-as-float.
- Source commit: unavailable (source evidence retained)

### MEDIUM · vigia/core/peirceplanner_bounded.py
- Agent: `integrity_inspector`
- Status: `CODE FACT`
- Description: floating-point division touches a money-shaped value; no explicit float() call, so it bypasses decision-adjacent-float
- Reasoning: AST detector emitted this observation: money-as-float.
- Source commit: unavailable (source evidence retained)

### MEDIUM · vigia/core/peirceplanner_bounded.py
- Agent: `integrity_inspector`
- Status: `CODE FACT`
- Description: floating-point division touches a money-shaped value; no explicit float() call, so it bypasses decision-adjacent-float
- Reasoning: AST detector emitted this observation: money-as-float.
- Source commit: unavailable (source evidence retained)

### MEDIUM · vigia/inference/abductive_intent_engine.py
- Agent: `integrity_inspector`
- Status: `CODE FACT`
- Description: unversioned serialization
- Reasoning: AST detector emitted this observation: unversioned-serialization.
- Source commit: unavailable (source evidence retained)

### MEDIUM · vigia/forensics/rfc3161_chain.py
- Agent: `integrity_inspector`
- Status: `CODE FACT`
- Description: unversioned serialization
- Reasoning: AST detector emitted this observation: unversioned-serialization.
- Source commit: unavailable (source evidence retained)

### MEDIUM · vigia/forensics/rfc3161_chain.py
- Agent: `integrity_inspector`
- Status: `CODE FACT`
- Description: unversioned serialization
- Reasoning: AST detector emitted this observation: unversioned-serialization.
- Source commit: unavailable (source evidence retained)

### MEDIUM · vigia/forensics/vision_audit.py
- Agent: `integrity_inspector`
- Status: `CODE FACT`
- Description: binary float literal assigned to a money-shaped value
- Reasoning: AST detector emitted this observation: money-as-float.
- Source commit: unavailable (source evidence retained)

### LOW · vigia/core/audit_action.py
- Agent: `tamper-evident-audit-chain`
- Status: `PROTOCOL_GAP`
- Description: persistent audit/ledger append has no visible link to a previous entry hash
- Reasoning: A plain append-only record cannot detect deletion, insertion, or reordering after the fact.
- Source commit: unavailable (source evidence retained)

### LOW · vigia/core/audit_action.py
- Agent: `tamper-evident-audit-chain`
- Status: `PROTOCOL_GAP`
- Description: persistent audit/ledger append has no visible link to a previous entry hash
- Reasoning: A plain append-only record cannot detect deletion, insertion, or reordering after the fact.
- Source commit: unavailable (source evidence retained)

### LOW · vigia/core/audit_action.py
- Agent: `tamper-evident-audit-chain`
- Status: `PROTOCOL_GAP`
- Description: persistent audit/ledger append has no visible link to a previous entry hash
- Reasoning: A plain append-only record cannot detect deletion, insertion, or reordering after the fact.
- Source commit: unavailable (source evidence retained)

### LOW · vigia/core/bundle_builder.py
- Agent: `honest-degradation`
- Status: `PROTOCOL_GAP`
- Description: exception handler returns a plausible fallback without raising or marking degraded state
- Reasoning: A degraded-input handler is structurally silent, so callers cannot distinguish fallback data from verified data.
- Source commit: unavailable (source evidence retained)

### LOW · vigia/core/bundle_builder.py
- Agent: `honest-degradation`
- Status: `PROTOCOL_GAP`
- Description: exception handler returns a plausible fallback without raising or marking degraded state
- Reasoning: A degraded-input handler is structurally silent, so callers cannot distinguish fallback data from verified data.
- Source commit: unavailable (source evidence retained)

### LOW · vigia/core/bundle_builder.py
- Agent: `honest-degradation`
- Status: `PROTOCOL_GAP`
- Description: exception handler returns a plausible fallback without raising or marking degraded state
- Reasoning: A degraded-input handler is structurally silent, so callers cannot distinguish fallback data from verified data.
- Source commit: unavailable (source evidence retained)

### LOW · vigia/core/bundle_builder.py
- Agent: `tamper-evident-audit-chain`
- Status: `PROTOCOL_GAP`
- Description: persistent audit/ledger append has no visible link to a previous entry hash
- Reasoning: A plain append-only record cannot detect deletion, insertion, or reordering after the fact.
- Source commit: unavailable (source evidence retained)

### LOW · vigia/core/chain_of_custody.py
- Agent: `validate-at-the-boundary`
- Status: `PROTOCOL_GAP`
- Description: parameter `path` reaches a sensitive boundary call without an explicit raising validation
- Reasoning: validate-at-the-boundary applies because direct external input reaches a parser or filesystem call.
- Source commit: unavailable (source evidence retained)

### LOW · vigia/core/entanglement.py
- Agent: `sql-aggregation-not-materialization`
- Status: `PROTOCOL_GAP`
- Description: SQL execute occurs inside an application loop (potential N+1 query pattern)
- Reasoning: A batched query or preload should be considered before issuing one query per loop item.
- Source commit: unavailable (source evidence retained)

### LOW · vigia/core/entanglement.py
- Agent: `tamper-evident-audit-chain`
- Status: `PROTOCOL_GAP`
- Description: persistent audit/ledger append has no visible link to a previous entry hash
- Reasoning: A plain append-only record cannot detect deletion, insertion, or reordering after the fact.
- Source commit: unavailable (source evidence retained)

### LOW · vigia/core/entanglement.py
- Agent: `validate-at-the-boundary`
- Status: `PROTOCOL_GAP`
- Description: parameter `path` reaches a sensitive boundary call without an explicit raising validation
- Reasoning: validate-at-the-boundary applies because direct external input reaches a parser or filesystem call.
- Source commit: unavailable (source evidence retained)

### LOW · vigia/core/entanglement.py
- Agent: `validate-at-the-boundary`
- Status: `PROTOCOL_GAP`
- Description: parameter `path` reaches a sensitive boundary call without an explicit raising validation
- Reasoning: validate-at-the-boundary applies because direct external input reaches a parser or filesystem call.
- Source commit: unavailable (source evidence retained)

### LOW · vigia/core/forensic_adapter.py
- Agent: `honest-degradation`
- Status: `PROTOCOL_GAP`
- Description: exception handler drops an item in a loop; output silently reduced without degraded state
- Reasoning: A logged-and-continued degraded path can still produce a plausible partial result, so the caller cannot distinguish complete evaluation from discarded evidence.
- Source commit: unavailable (source evidence retained)

### LOW · vigia/core/graph_stability.py
- Agent: `tamper-evident-audit-chain`
- Status: `PROTOCOL_GAP`
- Description: persistent audit/ledger append has no visible link to a previous entry hash
- Reasoning: A plain append-only record cannot detect deletion, insertion, or reordering after the fact.
- Source commit: unavailable (source evidence retained)

### LOW · vigia/core/hash_chain.py
- Agent: `tamper-evident-audit-chain`
- Status: `PROTOCOL_GAP`
- Description: persistent audit/ledger append has no visible link to a previous entry hash
- Reasoning: A plain append-only record cannot detect deletion, insertion, or reordering after the fact.
- Source commit: unavailable (source evidence retained)

### LOW · vigia/core/lr_calibration.py
- Agent: `validate-at-the-boundary`
- Status: `PROTOCOL_GAP`
- Description: parameter `path` reaches a sensitive boundary call without an explicit raising validation
- Reasoning: validate-at-the-boundary applies because direct external input reaches a parser or filesystem call.
- Source commit: unavailable (source evidence retained)

### LOW · vigia/core/lr_calibration.py
- Agent: `validate-at-the-boundary`
- Status: `PROTOCOL_GAP`
- Description: parameter `path` reaches a sensitive boundary call without an explicit raising validation
- Reasoning: validate-at-the-boundary applies because direct external input reaches a parser or filesystem call.
- Source commit: unavailable (source evidence retained)

### LOW · vigia/core/trust_fusion.py
- Agent: `deterministic-core`
- Status: `PROTOCOL_GAP`
- Description: float or division result enters a payload that is later sealed
- Reasoning: Direct non-exact arithmetic is inside the deterministic serialization path.
- Source commit: unavailable (source evidence retained)

### LOW · vigia/forensics/rfc3161_chain.py
- Agent: `validate-at-the-boundary`
- Status: `PROTOCOL_GAP`
- Description: parameter `path` reaches a sensitive boundary call without an explicit raising validation
- Reasoning: validate-at-the-boundary applies because direct external input reaches a parser or filesystem call.
- Source commit: unavailable (source evidence retained)

### LOW · vigia/forensics/vision_audit.py
- Agent: `honest-degradation`
- Status: `PROTOCOL_GAP`
- Description: exception handler returns a plausible fallback without raising or marking degraded state
- Reasoning: A degraded-input handler is structurally silent, so callers cannot distinguish fallback data from verified data.
- Source commit: unavailable (source evidence retained)

### LOW · vigia/forensics/vision_audit.py
- Agent: `honest-degradation`
- Status: `PROTOCOL_GAP`
- Description: exception handler returns a plausible fallback without raising or marking degraded state
- Reasoning: A degraded-input handler is structurally silent, so callers cannot distinguish fallback data from verified data.
- Source commit: unavailable (source evidence retained)

### LOW · vigia/forensics/vision_audit.py
- Agent: `honest-degradation`
- Status: `PROTOCOL_GAP`
- Description: exception handler returns a plausible fallback without raising or marking degraded state
- Reasoning: A degraded-input handler is structurally silent, so callers cannot distinguish fallback data from verified data.
- Source commit: unavailable (source evidence retained)

### LOW · vigia/forensics/vision_audit.py
- Agent: `honest-degradation`
- Status: `PROTOCOL_GAP`
- Description: exception handler returns a plausible fallback without raising or marking degraded state
- Reasoning: A degraded-input handler is structurally silent, so callers cannot distinguish fallback data from verified data.
- Source commit: unavailable (source evidence retained)

### LOW · vigia/forensics/vision_audit.py
- Agent: `honest-degradation`
- Status: `PROTOCOL_GAP`
- Description: exception handler returns a plausible fallback without raising or marking degraded state
- Reasoning: A degraded-input handler is structurally silent, so callers cannot distinguish fallback data from verified data.
- Source commit: unavailable (source evidence retained)

### LOW · vigia/forensics/vision_audit.py
- Agent: `honest-degradation`
- Status: `PROTOCOL_GAP`
- Description: exception handler returns a plausible fallback without raising or marking degraded state
- Reasoning: A degraded-input handler is structurally silent, so callers cannot distinguish fallback data from verified data.
- Source commit: unavailable (source evidence retained)

### LOW · vigia/forensics/vision_audit.py
- Agent: `tamper-evident-audit-chain`
- Status: `PROTOCOL_GAP`
- Description: persistent audit/ledger append has no visible link to a previous entry hash
- Reasoning: A plain append-only record cannot detect deletion, insertion, or reordering after the fact.
- Source commit: unavailable (source evidence retained)

### LOW · vigia/forensics/vision_audit.py
- Agent: `tamper-evident-audit-chain`
- Status: `PROTOCOL_GAP`
- Description: persistent audit/ledger append has no visible link to a previous entry hash
- Reasoning: A plain append-only record cannot detect deletion, insertion, or reordering after the fact.
- Source commit: unavailable (source evidence retained)

### LOW · vigia/forensics/vision_audit.py
- Agent: `tamper-evident-audit-chain`
- Status: `PROTOCOL_GAP`
- Description: persistent audit/ledger append has no visible link to a previous entry hash
- Reasoning: A plain append-only record cannot detect deletion, insertion, or reordering after the fact.
- Source commit: unavailable (source evidence retained)

### LOW · vigia/forensics/vision_audit.py
- Agent: `tamper-evident-audit-chain`
- Status: `PROTOCOL_GAP`
- Description: persistent audit/ledger append has no visible link to a previous entry hash
- Reasoning: A plain append-only record cannot detect deletion, insertion, or reordering after the fact.
- Source commit: unavailable (source evidence retained)

### LOW · vigia/forensics/vision_audit.py
- Agent: `validate-at-the-boundary`
- Status: `PROTOCOL_GAP`
- Description: parameter `model_path` reaches a sensitive boundary call without an explicit raising validation
- Reasoning: validate-at-the-boundary applies because direct external input reaches a parser or filesystem call.
- Source commit: unavailable (source evidence retained)

### LOW · vigia/forensics/vision_audit.py
- Agent: `validate-at-the-boundary`
- Status: `PROTOCOL_GAP`
- Description: parameter `image_path` reaches a sensitive boundary call without an explicit raising validation
- Reasoning: validate-at-the-boundary applies because direct external input reaches a parser or filesystem call.
- Source commit: unavailable (source evidence retained)

### LOW · vigia/forensics/vision_audit.py
- Agent: `validate-at-the-boundary`
- Status: `PROTOCOL_GAP`
- Description: parameter `model_name` reaches a sensitive boundary call without an explicit raising validation
- Reasoning: validate-at-the-boundary applies because direct external input reaches a parser or filesystem call.
- Source commit: unavailable (source evidence retained)

### LOW · vigia/inference/abductive_reasoner.py
- Agent: `honest-degradation`
- Status: `PROTOCOL_GAP`
- Description: exception handler returns a plausible fallback without raising or marking degraded state
- Reasoning: A degraded-input handler is structurally silent, so callers cannot distinguish fallback data from verified data.
- Source commit: unavailable (source evidence retained)

### LOW · vigia/pipeline/pipeline.py
- Agent: `honest-degradation`
- Status: `PROTOCOL_GAP`
- Description: exception handler returns a plausible fallback without raising or marking degraded state
- Reasoning: A degraded-input handler is structurally silent, so callers cannot distinguish fallback data from verified data.
- Source commit: unavailable (source evidence retained)

### LOW · vigia/pipeline/pipeline.py
- Agent: `tamper-evident-audit-chain`
- Status: `PROTOCOL_GAP`
- Description: persistent audit/ledger append has no visible link to a previous entry hash
- Reasoning: A plain append-only record cannot detect deletion, insertion, or reordering after the fact.
- Source commit: unavailable (source evidence retained)

### LOW · vigia/pipeline/pipeline.py
- Agent: `validate-at-the-boundary`
- Status: `PROTOCOL_GAP`
- Description: parameter `bundle_path` reaches a sensitive boundary call without an explicit raising validation
- Reasoning: validate-at-the-boundary applies because direct external input reaches a parser or filesystem call.
- Source commit: unavailable (source evidence retained)

### LOW · vigia/pipeline/pipeline.py
- Agent: `validate-at-the-boundary`
- Status: `PROTOCOL_GAP`
- Description: parameter `bundle_path` reaches a sensitive boundary call without an explicit raising validation
- Reasoning: validate-at-the-boundary applies because direct external input reaches a parser or filesystem call.
- Source commit: unavailable (source evidence retained)

### LOW · vigia/pipeline/vigia_integration_bridge.py
- Agent: `honest-degradation`
- Status: `PROTOCOL_GAP`
- Description: exception handler returns a plausible fallback without raising or marking degraded state
- Reasoning: A degraded-input handler is structurally silent, so callers cannot distinguish fallback data from verified data.
- Source commit: unavailable (source evidence retained)

### LOW · vigia/pipeline/vigia_integration_bridge.py
- Agent: `tamper-evident-audit-chain`
- Status: `PROTOCOL_GAP`
- Description: persistent audit/ledger append has no visible link to a previous entry hash
- Reasoning: A plain append-only record cannot detect deletion, insertion, or reordering after the fact.
- Source commit: unavailable (source evidence retained)

### LOW · vigia/pipeline/vigia_integration_bridge.py
- Agent: `tamper-evident-audit-chain`
- Status: `PROTOCOL_GAP`
- Description: persistent audit/ledger append has no visible link to a previous entry hash
- Reasoning: A plain append-only record cannot detect deletion, insertion, or reordering after the fact.
- Source commit: unavailable (source evidence retained)

### LOW · vigia/pipeline/vigia_integration_bridge.py
- Agent: `tamper-evident-audit-chain`
- Status: `PROTOCOL_GAP`
- Description: persistent audit/ledger append has no visible link to a previous entry hash
- Reasoning: A plain append-only record cannot detect deletion, insertion, or reordering after the fact.
- Source commit: unavailable (source evidence retained)

### LOW · vigia/security/sandbox.py
- Agent: `tamper-evident-audit-chain`
- Status: `PROTOCOL_GAP`
- Description: persistent audit/ledger append has no visible link to a previous entry hash
- Reasoning: A plain append-only record cannot detect deletion, insertion, or reordering after the fact.
- Source commit: unavailable (source evidence retained)

### LOW · vigia/security/security.py
- Agent: `tamper-evident-audit-chain`
- Status: `PROTOCOL_GAP`
- Description: persistent audit/ledger append has no visible link to a previous entry hash
- Reasoning: A plain append-only record cannot detect deletion, insertion, or reordering after the fact.
- Source commit: unavailable (source evidence retained)

### LOW · vigia/security/security.py
- Agent: `tamper-evident-audit-chain`
- Status: `PROTOCOL_GAP`
- Description: persistent audit/ledger append has no visible link to a previous entry hash
- Reasoning: A plain append-only record cannot detect deletion, insertion, or reordering after the fact.
- Source commit: unavailable (source evidence retained)

### LOW · vigia/security/security.py
- Agent: `tamper-evident-audit-chain`
- Status: `PROTOCOL_GAP`
- Description: persistent audit/ledger append has no visible link to a previous entry hash
- Reasoning: A plain append-only record cannot detect deletion, insertion, or reordering after the fact.
- Source commit: unavailable (source evidence retained)

### LOW · vigia/sift/browser_forensics.py
- Agent: `sql-aggregation-not-materialization`
- Status: `PROTOCOL_GAP`
- Description: SQL execute occurs inside an application loop (potential N+1 query pattern)
- Reasoning: A batched query or preload should be considered before issuing one query per loop item.
- Source commit: unavailable (source evidence retained)

### LOW · vigia/sift/browser_forensics.py
- Agent: `sql-aggregation-not-materialization`
- Status: `PROTOCOL_GAP`
- Description: SQL execute occurs inside an application loop (potential N+1 query pattern)
- Reasoning: A batched query or preload should be considered before issuing one query per loop item.
- Source commit: unavailable (source evidence retained)

### LOW · vigia/sift/browser_forensics.py
- Agent: `sql-aggregation-not-materialization`
- Status: `PROTOCOL_GAP`
- Description: SQL execute occurs inside an application loop (potential N+1 query pattern)
- Reasoning: A batched query or preload should be considered before issuing one query per loop item.
- Source commit: unavailable (source evidence retained)

### LOW · vigia/sift/browser_forensics.py
- Agent: `sql-aggregation-not-materialization`
- Status: `PROTOCOL_GAP`
- Description: SQL execute occurs inside an application loop (potential N+1 query pattern)
- Reasoning: A batched query or preload should be considered before issuing one query per loop item.
- Source commit: unavailable (source evidence retained)

### LOW · vigia/sift/disk_forensics.py
- Agent: `honest-degradation`
- Status: `PROTOCOL_GAP`
- Description: exception handler drops an item in a loop; output silently reduced without degraded state
- Reasoning: A logged-and-continued degraded path can still produce a plausible partial result, so the caller cannot distinguish complete evaluation from discarded evidence.
- Source commit: unavailable (source evidence retained)

### LOW · vigia/sift/disk_forensics.py
- Agent: `honest-degradation`
- Status: `PROTOCOL_GAP`
- Description: exception handler drops an item in a loop; output silently reduced without degraded state
- Reasoning: A logged-and-continued degraded path can still produce a plausible partial result, so the caller cannot distinguish complete evaluation from discarded evidence.
- Source commit: unavailable (source evidence retained)

### LOW · vigia/sift/event_log_correlator.py
- Agent: `honest-degradation`
- Status: `PROTOCOL_GAP`
- Description: exception handler drops an item in a loop; output silently reduced without degraded state
- Reasoning: A logged-and-continued degraded path can still produce a plausible partial result, so the caller cannot distinguish complete evaluation from discarded evidence.
- Source commit: unavailable (source evidence retained)

### LOW · vigia/sift/event_log_correlator.py
- Agent: `tamper-evident-audit-chain`
- Status: `PROTOCOL_GAP`
- Description: persistent audit/ledger append has no visible link to a previous entry hash
- Reasoning: A plain append-only record cannot detect deletion, insertion, or reordering after the fact.
- Source commit: unavailable (source evidence retained)

### LOW · vigia/sift/event_log_correlator.py
- Agent: `tamper-evident-audit-chain`
- Status: `PROTOCOL_GAP`
- Description: persistent audit/ledger append has no visible link to a previous entry hash
- Reasoning: A plain append-only record cannot detect deletion, insertion, or reordering after the fact.
- Source commit: unavailable (source evidence retained)

### LOW · vigia/sift/event_log_correlator.py
- Agent: `tamper-evident-audit-chain`
- Status: `PROTOCOL_GAP`
- Description: persistent audit/ledger append has no visible link to a previous entry hash
- Reasoning: A plain append-only record cannot detect deletion, insertion, or reordering after the fact.
- Source commit: unavailable (source evidence retained)

### LOW · vigia/sift/event_log_correlator.py
- Agent: `tamper-evident-audit-chain`
- Status: `PROTOCOL_GAP`
- Description: persistent audit/ledger append has no visible link to a previous entry hash
- Reasoning: A plain append-only record cannot detect deletion, insertion, or reordering after the fact.
- Source commit: unavailable (source evidence retained)

### LOW · vigia/sift/event_log_correlator.py
- Agent: `validate-at-the-boundary`
- Status: `PROTOCOL_GAP`
- Description: parameter `xml_path` reaches a sensitive boundary call without an explicit raising validation
- Reasoning: validate-at-the-boundary applies because direct external input reaches a parser or filesystem call.
- Source commit: unavailable (source evidence retained)

### LOW · vigia/sift/fsevents_parser.py
- Agent: `honest-degradation`
- Status: `PROTOCOL_GAP`
- Description: exception handler returns a plausible fallback without raising or marking degraded state
- Reasoning: A degraded-input handler is structurally silent, so callers cannot distinguish fallback data from verified data.
- Source commit: unavailable (source evidence retained)

### LOW · vigia/sift/memory_forensics.py
- Agent: `honest-degradation`
- Status: `PROTOCOL_GAP`
- Description: exception handler returns a plausible fallback without raising or marking degraded state
- Reasoning: A degraded-input handler is structurally silent, so callers cannot distinguish fallback data from verified data.
- Source commit: unavailable (source evidence retained)

### LOW · vigia/sift/memory_forensics.py
- Agent: `honest-degradation`
- Status: `PROTOCOL_GAP`
- Description: exception handler drops an item in a loop; output silently reduced without degraded state
- Reasoning: A logged-and-continued degraded path can still produce a plausible partial result, so the caller cannot distinguish complete evaluation from discarded evidence.
- Source commit: unavailable (source evidence retained)

### LOW · vigia/sift/memory_forensics.py
- Agent: `honest-degradation`
- Status: `PROTOCOL_GAP`
- Description: exception handler drops an item in a loop; output silently reduced without degraded state
- Reasoning: A logged-and-continued degraded path can still produce a plausible partial result, so the caller cannot distinguish complete evaluation from discarded evidence.
- Source commit: unavailable (source evidence retained)

### LOW · vigia/sift/memory_forensics.py
- Agent: `honest-degradation`
- Status: `PROTOCOL_GAP`
- Description: exception handler drops an item in a loop; output silently reduced without degraded state
- Reasoning: A logged-and-continued degraded path can still produce a plausible partial result, so the caller cannot distinguish complete evaluation from discarded evidence.
- Source commit: unavailable (source evidence retained)

### LOW · vigia/sift/registry_timeline_reconstructor.py
- Agent: `honest-degradation`
- Status: `PROTOCOL_GAP`
- Description: exception handler returns a plausible fallback without raising or marking degraded state
- Reasoning: A degraded-input handler is structurally silent, so callers cannot distinguish fallback data from verified data.
- Source commit: unavailable (source evidence retained)

### LOW · vigia/sift/registry_timeline_reconstructor.py
- Agent: `honest-degradation`
- Status: `PROTOCOL_GAP`
- Description: exception handler drops an item in a loop; output silently reduced without degraded state
- Reasoning: A logged-and-continued degraded path can still produce a plausible partial result, so the caller cannot distinguish complete evaluation from discarded evidence.
- Source commit: unavailable (source evidence retained)

### LOW · vigia/sift/sift_orchestrator.py
- Agent: `honest-degradation`
- Status: `PROTOCOL_GAP`
- Description: exception handler returns a plausible fallback without raising or marking degraded state
- Reasoning: A degraded-input handler is structurally silent, so callers cannot distinguish fallback data from verified data.
- Source commit: unavailable (source evidence retained)

### LOW · vigia/sift/sift_orchestrator.py
- Agent: `validate-at-the-boundary`
- Status: `PROTOCOL_GAP`
- Description: parameter `mft_json` reaches a sensitive boundary call without an explicit raising validation
- Reasoning: validate-at-the-boundary applies because direct external input reaches a parser or filesystem call.
- Source commit: unavailable (source evidence retained)

### LOW · vigia/tools/adversarial_nlp.py
- Agent: `honest-degradation`
- Status: `PROTOCOL_GAP`
- Description: exception handler returns a plausible fallback without raising or marking degraded state
- Reasoning: A degraded-input handler is structurally silent, so callers cannot distinguish fallback data from verified data.
- Source commit: unavailable (source evidence retained)

### LOW · vigia/tools/adversarial_nlp.py
- Agent: `tamper-evident-audit-chain`
- Status: `PROTOCOL_GAP`
- Description: persistent audit/ledger append has no visible link to a previous entry hash
- Reasoning: A plain append-only record cannot detect deletion, insertion, or reordering after the fact.
- Source commit: unavailable (source evidence retained)

### LOW · vigia/tools/caie.py
- Agent: `honest-degradation`
- Status: `PROTOCOL_GAP`
- Description: exception handler returns a plausible fallback without raising or marking degraded state
- Reasoning: A degraded-input handler is structurally silent, so callers cannot distinguish fallback data from verified data.
- Source commit: unavailable (source evidence retained)

### LOW · vigia/tools/caie.py
- Agent: `honest-degradation`
- Status: `PROTOCOL_GAP`
- Description: exception handler returns a plausible fallback without raising or marking degraded state
- Reasoning: A degraded-input handler is structurally silent, so callers cannot distinguish fallback data from verified data.
- Source commit: unavailable (source evidence retained)

### LOW · vigia/tools/caie.py
- Agent: `honest-degradation`
- Status: `PROTOCOL_GAP`
- Description: exception handler returns a plausible fallback without raising or marking degraded state
- Reasoning: A degraded-input handler is structurally silent, so callers cannot distinguish fallback data from verified data.
- Source commit: unavailable (source evidence retained)

### LOW · vigia/tools/caie.py
- Agent: `honest-degradation`
- Status: `PROTOCOL_GAP`
- Description: exception handler returns a plausible fallback without raising or marking degraded state
- Reasoning: A degraded-input handler is structurally silent, so callers cannot distinguish fallback data from verified data.
- Source commit: unavailable (source evidence retained)

### LOW · vigia/tools/caie.py
- Agent: `tamper-evident-audit-chain`
- Status: `PROTOCOL_GAP`
- Description: persistent audit/ledger append has no visible link to a previous entry hash
- Reasoning: A plain append-only record cannot detect deletion, insertion, or reordering after the fact.
- Source commit: unavailable (source evidence retained)

### LOW · vigia/tools/caie.py
- Agent: `tamper-evident-audit-chain`
- Status: `PROTOCOL_GAP`
- Description: persistent audit/ledger append has no visible link to a previous entry hash
- Reasoning: A plain append-only record cannot detect deletion, insertion, or reordering after the fact.
- Source commit: unavailable (source evidence retained)

### LOW · vigia/tools/caie.py
- Agent: `tamper-evident-audit-chain`
- Status: `PROTOCOL_GAP`
- Description: persistent audit/ledger append has no visible link to a previous entry hash
- Reasoning: A plain append-only record cannot detect deletion, insertion, or reordering after the fact.
- Source commit: unavailable (source evidence retained)

### LOW · vigia/tools/document_integrity.py
- Agent: `honest-degradation`
- Status: `PROTOCOL_GAP`
- Description: exception handler returns a plausible fallback without raising or marking degraded state
- Reasoning: A degraded-input handler is structurally silent, so callers cannot distinguish fallback data from verified data.
- Source commit: unavailable (source evidence retained)

### LOW · vigia/tools/document_integrity.py
- Agent: `honest-degradation`
- Status: `PROTOCOL_GAP`
- Description: exception handler returns a plausible fallback without raising or marking degraded state
- Reasoning: A degraded-input handler is structurally silent, so callers cannot distinguish fallback data from verified data.
- Source commit: unavailable (source evidence retained)

### LOW · vigia/tools/document_integrity.py
- Agent: `tamper-evident-audit-chain`
- Status: `PROTOCOL_GAP`
- Description: persistent audit/ledger append has no visible link to a previous entry hash
- Reasoning: A plain append-only record cannot detect deletion, insertion, or reordering after the fact.
- Source commit: unavailable (source evidence retained)

### LOW · vigia/tools/document_integrity.py
- Agent: `validate-at-the-boundary`
- Status: `PROTOCOL_GAP`
- Description: parameter `path` reaches a sensitive boundary call without an explicit raising validation
- Reasoning: validate-at-the-boundary applies because direct external input reaches a parser or filesystem call.
- Source commit: unavailable (source evidence retained)

### LOW · vigia/tools/eml_gci.py
- Agent: `honest-degradation`
- Status: `PROTOCOL_GAP`
- Description: exception handler returns a plausible fallback without raising or marking degraded state
- Reasoning: A degraded-input handler is structurally silent, so callers cannot distinguish fallback data from verified data.
- Source commit: unavailable (source evidence retained)

### LOW · vigia/tools/forensic_db.py
- Agent: `tamper-evident-audit-chain`
- Status: `PROTOCOL_GAP`
- Description: persistent audit/ledger append has no visible link to a previous entry hash
- Reasoning: A plain append-only record cannot detect deletion, insertion, or reordering after the fact.
- Source commit: unavailable (source evidence retained)

### LOW · vigia/tools/forensic_db.py
- Agent: `tamper-evident-audit-chain`
- Status: `PROTOCOL_GAP`
- Description: persistent audit/ledger append has no visible link to a previous entry hash
- Reasoning: A plain append-only record cannot detect deletion, insertion, or reordering after the fact.
- Source commit: unavailable (source evidence retained)

### LOW · vigia/tools/forensic_db.py
- Agent: `tamper-evident-audit-chain`
- Status: `PROTOCOL_GAP`
- Description: persistent audit/ledger append has no visible link to a previous entry hash
- Reasoning: A plain append-only record cannot detect deletion, insertion, or reordering after the fact.
- Source commit: unavailable (source evidence retained)

### LOW · vigia/tools/forensic_db.py
- Agent: `tamper-evident-audit-chain`
- Status: `PROTOCOL_GAP`
- Description: persistent audit/ledger append has no visible link to a previous entry hash
- Reasoning: A plain append-only record cannot detect deletion, insertion, or reordering after the fact.
- Source commit: unavailable (source evidence retained)

### LOW · vigia/tools/paired_review.py
- Agent: `honest-degradation`
- Status: `PROTOCOL_GAP`
- Description: exception handler drops an item in a loop; output silently reduced without degraded state
- Reasoning: A logged-and-continued degraded path can still produce a plausible partial result, so the caller cannot distinguish complete evaluation from discarded evidence.
- Source commit: unavailable (source evidence retained)

### LOW · vigia/tools/visible_variables.py
- Agent: `honest-degradation`
- Status: `PROTOCOL_GAP`
- Description: exception handler returns a plausible fallback without raising or marking degraded state
- Reasoning: A degraded-input handler is structurally silent, so callers cannot distinguish fallback data from verified data.
- Source commit: unavailable (source evidence retained)

### LOW · vigia_scorer.py
- Agent: `honest-degradation`
- Status: `PROTOCOL_GAP`
- Description: exception handler drops an item in a loop; output silently reduced without degraded state
- Reasoning: A logged-and-continued degraded path can still produce a plausible partial result, so the caller cannot distinguish complete evaluation from discarded evidence.
- Source commit: unavailable (source evidence retained)

## Limitations

- Hypotheses require module 3 verification; parser candidates may receive isolated induction, while unsupported families remain AST-only.
- 176 discovered file(s) were skipped; see skipped_reasons for the exact paths and policy categories.
- 90 triaged module(s) were outside CONNECTED_ALIVE audit scope.
- 52 skill applicability result(s) were UNDETERMINED; no conclusion was inferred for them.
- 12 hypothesis/hypotheses survived structural verification without dynamic induction; they remain plausible hypotheses, not confirmed defects.
