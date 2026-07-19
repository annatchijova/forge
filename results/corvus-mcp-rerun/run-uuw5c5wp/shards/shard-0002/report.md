# FORGE audit report

Repository: `/home/labestiadevigia/corvus-cronos-bridge`
Seal: **VERIFIED**
Findings: **3** · Discarded hypotheses: **0**
Finding-set digest: `4037e25766a51a4d5938ec91373f4dc51414803a87f76e1355e2074489d73468`
Eligible source coverage: **69/71 (97.2%)**
Discovery accounting: **69/683 discovered files**
Audit disposition: **ABSTAIN_INSUFFICIENT_SCOPE**

## Repository profile

- Modules: 21 (3 connected)
- Domains: audit_or_ledger, determinism_sensitive, input_boundary, serialization_or_persistence
- Audit duration: 1.982749 seconds

## Findings

### MEDIUM · tests/test_qwen_agent.py
- Agent: `bug_investigator`
- Status: `PLAUSIBLE HYPOTHESIS`
- Description: The parser call `data = json.loads(msg["content"])` at tests/test_qwen_agent.py:132 has no nearby exception handling, so malformed input may escape as an opaque failure.
- Reasoning: Observed construct matches, but induction only established that an error path is reachable: Malformed input reached an opaque AttributeError, but the exception did not originate at the hypothesized parser call. Evidence: tests/test_qwen_agent.py:132: AttributeError: module 'tests.test_qwen_agent' has no attribute '__call__'
- Source commit: `892d166eef137851f45f77c8fa6407e6f1ae1ad0`

### MEDIUM · tests/test_redteam_nightly.py
- Agent: `bug_investigator`
- Status: `PLAUSIBLE HYPOTHESIS`
- Description: The dynamic command invocation `proc = subprocess.run(` at tests/test_redteam_nightly.py:107 may pass attacker-controlled arguments without an enclosing failure boundary.
- Reasoning: Observed construct matches, but induction only established that an error path is reachable: Malformed input reached an opaque AttributeError, but the exception did not originate at the hypothesized parser call. Evidence: tests/test_redteam_nightly.py:107: AttributeError: module 'tests.test_redteam_nightly' has no attribute 'test_refuses_without_api_key'
- Source commit: `de3b2b1c9c2c246c7aa126e12973e8082ade2642`

### MEDIUM · tests/test_qwen_agent.py
- Agent: `integrity_inspector`
- Status: `CODE FACT`
- Description: unversioned serialization
- Reasoning: AST detector emitted this observation: unversioned-serialization.
- Source commit: `892d166eef137851f45f77c8fa6407e6f1ae1ad0`

## Limitations

- Hypotheses require module 3 verification; parser candidates may receive isolated induction, while unsupported families remain AST-only.
- 614 discovered file(s) were skipped; see skipped_reasons for the exact paths and policy categories.
- 18 triaged module(s) were outside CONNECTED_ALIVE audit scope.
- 2 skill applicability result(s) were UNDETERMINED; no conclusion was inferred for them.
- 2 hypothesis/hypotheses survived structural verification without dynamic induction; they remain plausible hypotheses, not confirmed defects.
