# FORGE audit report

Repository: `/home/labestiadevigia/corvus-cronos-bridge`
Seal: **VERIFIED**
Findings: **73** · Discarded hypotheses: **1**
Finding-set digest: `b49d398ca881eb2bf44cb277f282528d34da1d746b80ad39cc6f742359a4483f`
Eligible source coverage: **69/71 (97.2%)**
Discovery accounting: **69/683 discovered files**
Audit disposition: **ABSTAIN_INSUFFICIENT_SCOPE**

## Repository profile

- Modules: 71 (53 connected)
- Domains: audit_or_ledger, cryptographic, determinism_sensitive, input_boundary, serialization_or_persistence
- Audit duration: 8.69841 seconds

## Findings

### MEDIUM · corvus/corvus/verdict/bundle.py
- Agent: `bug_investigator`
- Status: `PLAUSIBLE HYPOTHESIS`
- Description: The parser call `bundle = json.load(fh)` at corvus/corvus/verdict/bundle.py:96 has no nearby exception handling, so malformed input may escape as an opaque failure.
- Reasoning: Observed construct matches; induction was undetermined: Target module could not be loaded in its package context: ModuleNotFoundError: No module named 'corvus.models'
- Source commit: `13075d0bb42adc84052f3e0e78a28b970775f910`

### MEDIUM · corvus/tests/test_regressions.py
- Agent: `bug_investigator`
- Status: `PLAUSIBLE HYPOTHESIS`
- Description: The parser call `bundle = json.load(fh)` at corvus/tests/test_regressions.py:353 has no nearby exception handling, so malformed input may escape as an opaque failure.
- Reasoning: Observed construct matches; induction was undetermined: Target module could not be loaded in its package context: ModuleNotFoundError: No module named 'corvus.analysis'
- Source commit: `13075d0bb42adc84052f3e0e78a28b970775f910`

### MEDIUM · cronos/cronos/store.py
- Agent: `bug_investigator`
- Status: `PLAUSIBLE HYPOTHESIS`
- Description: The parser call `payload=json.loads(r[1]),` at cronos/cronos/store.py:217 has no nearby exception handling, so malformed input may escape as an opaque failure.
- Reasoning: Observed construct matches; induction was undetermined: Target module could not be loaded in its package context: ImportError: attempted relative import with no known parent package
- Source commit: `13075d0bb42adc84052f3e0e78a28b970775f910`

### MEDIUM · cronos/cronos/store.py
- Agent: `bug_investigator`
- Status: `PLAUSIBLE HYPOTHESIS`
- Description: The parser call `contradictions = json.loads(contradictions_json) if contradictions_json else []` at cronos/cronos/store.py:225 has no nearby exception handling, so malformed input may escape as an opaque failure.
- Reasoning: Observed construct matches; induction was undetermined: Target module could not be loaded in its package context: ImportError: attempted relative import with no known parent package
- Source commit: `13075d0bb42adc84052f3e0e78a28b970775f910`

### MEDIUM · cronos/cronos/store.py
- Agent: `bug_investigator`
- Status: `PLAUSIBLE HYPOTHESIS`
- Description: The parser call `conf_warnings = json.loads(conf_warnings_json) if conf_warnings_json else []` at cronos/cronos/store.py:226 has no nearby exception handling, so malformed input may escape as an opaque failure.
- Reasoning: Observed construct matches; induction was undetermined: Target module could not be loaded in its package context: ImportError: attempted relative import with no known parent package
- Source commit: `13075d0bb42adc84052f3e0e78a28b970775f910`

### MEDIUM · tests/test_full_integration.py
- Agent: `bug_investigator`
- Status: `PLAUSIBLE HYPOTHESIS`
- Description: The parser call `return [{"kind": r[0], "payload": json.loads(r[1])} for r in rows]` at tests/test_full_integration.py:237 has no nearby exception handling, so malformed input may escape as an opaque failure.
- Reasoning: Observed construct matches, but induction only established that an error path is reachable: Malformed input reached an opaque AttributeError, but the exception did not originate at the hypothesized parser call. Evidence: tests/test_full_integration.py:237: AttributeError: module 'tests.test_full_integration' has no attribute '_steps_for'
- Source commit: `8a18d8f9bfa57ee2f7eb698b97a708869994c1ca`

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

### MEDIUM · tests/test_bridge.py
- Agent: `security_auditor`
- Status: `CODE FACT`
- Description: parameter reaches os.path operation without proven normalization
- Reasoning: AST detector emitted this observation: path-traversal.
- Source commit: unavailable (source evidence retained)

### MEDIUM · tests/test_bridge.py
- Agent: `security_auditor`
- Status: `CODE FACT`
- Description: parameter reaches os.path operation without proven normalization
- Reasoning: AST detector emitted this observation: path-traversal.
- Source commit: unavailable (source evidence retained)

### MEDIUM · tests/test_bridge.py
- Agent: `security_auditor`
- Status: `CODE FACT`
- Description: parameter reaches os.path operation without proven normalization
- Reasoning: AST detector emitted this observation: path-traversal.
- Source commit: unavailable (source evidence retained)

### MEDIUM · tests/test_bridge.py
- Agent: `security_auditor`
- Status: `CODE FACT`
- Description: parameter reaches os.path operation without proven normalization
- Reasoning: AST detector emitted this observation: path-traversal.
- Source commit: unavailable (source evidence retained)

### MEDIUM · tests/test_bridge.py
- Agent: `security_auditor`
- Status: `CODE FACT`
- Description: parameter reaches os.path operation without proven normalization
- Reasoning: AST detector emitted this observation: path-traversal.
- Source commit: unavailable (source evidence retained)

### MEDIUM · tests/test_bridge.py
- Agent: `security_auditor`
- Status: `CODE FACT`
- Description: parameter reaches os.path operation without proven normalization
- Reasoning: AST detector emitted this observation: path-traversal.
- Source commit: unavailable (source evidence retained)

### MEDIUM · tests/test_bridge.py
- Agent: `security_auditor`
- Status: `CODE FACT`
- Description: parameter reaches os.path operation without proven normalization
- Reasoning: AST detector emitted this observation: path-traversal.
- Source commit: unavailable (source evidence retained)

### MEDIUM · tests/test_api_server.py
- Agent: `security_auditor`
- Status: `CODE FACT`
- Description: non-empty credential-like string stored under 'X-API-Token'
- Reasoning: AST detector emitted this observation: hardcoded-credential.
- Source commit: `e8b913d471ab33b9a8429df771dce283872a24c9`

### MEDIUM · tests/test_api_server.py
- Agent: `security_auditor`
- Status: `CODE FACT`
- Description: non-empty credential-like string stored under 'X-API-Token'
- Reasoning: AST detector emitted this observation: hardcoded-credential.
- Source commit: `e8b913d471ab33b9a8429df771dce283872a24c9`

### MEDIUM · tests/test_api_server.py
- Agent: `security_auditor`
- Status: `CODE FACT`
- Description: parameter reaches os.path operation without proven normalization
- Reasoning: AST detector emitted this observation: path-traversal.
- Source commit: unavailable (source evidence retained)

### MEDIUM · tests/test_api_server.py
- Agent: `security_auditor`
- Status: `CODE FACT`
- Description: parameter reaches os.path operation without proven normalization
- Reasoning: AST detector emitted this observation: path-traversal.
- Source commit: unavailable (source evidence retained)

### MEDIUM · tests/test_full_integration.py
- Agent: `security_auditor`
- Status: `CODE FACT`
- Description: parameter reaches os.path operation without proven normalization
- Reasoning: AST detector emitted this observation: path-traversal.
- Source commit: unavailable (source evidence retained)

### MEDIUM · tests/test_full_integration.py
- Agent: `security_auditor`
- Status: `CODE FACT`
- Description: parameter reaches os.path operation without proven normalization
- Reasoning: AST detector emitted this observation: path-traversal.
- Source commit: unavailable (source evidence retained)

### MEDIUM · tests/test_full_integration.py
- Agent: `security_auditor`
- Status: `CODE FACT`
- Description: parameter reaches os.path operation without proven normalization
- Reasoning: AST detector emitted this observation: path-traversal.
- Source commit: unavailable (source evidence retained)

### MEDIUM · tests/test_full_integration.py
- Agent: `security_auditor`
- Status: `CODE FACT`
- Description: parameter reaches os.path operation without proven normalization
- Reasoning: AST detector emitted this observation: path-traversal.
- Source commit: unavailable (source evidence retained)

### MEDIUM · corvus_cronos/bridge.py
- Agent: `security_auditor`
- Status: `CODE FACT`
- Description: parameter reaches os.path operation without proven normalization
- Reasoning: AST detector emitted this observation: path-traversal.
- Source commit: unavailable (source evidence retained)

### MEDIUM · corvus_cronos/bridge.py
- Agent: `security_auditor`
- Status: `CODE FACT`
- Description: parameter reaches os.path operation without proven normalization
- Reasoning: AST detector emitted this observation: path-traversal.
- Source commit: unavailable (source evidence retained)

### MEDIUM · corvus/tests/test_regressions.py
- Agent: `security_auditor`
- Status: `CODE FACT`
- Description: parameter reaches os.path operation without proven normalization
- Reasoning: AST detector emitted this observation: path-traversal.
- Source commit: unavailable (source evidence retained)

### MEDIUM · corvus/tests/test_regressions.py
- Agent: `security_auditor`
- Status: `CODE FACT`
- Description: parameter reaches open() without proven normalization
- Reasoning: AST detector emitted this observation: path-traversal.
- Source commit: unavailable (source evidence retained)

### MEDIUM · corvus/tests/test_regressions.py
- Agent: `security_auditor`
- Status: `CODE FACT`
- Description: parameter reaches open() without proven normalization
- Reasoning: AST detector emitted this observation: path-traversal.
- Source commit: unavailable (source evidence retained)

### MEDIUM · corvus/corvus/memory/engine.py
- Agent: `security_auditor`
- Status: `CODE FACT`
- Description: parameter reaches os.path operation without proven normalization
- Reasoning: AST detector emitted this observation: path-traversal.
- Source commit: unavailable (source evidence retained)

### MEDIUM · corvus/corvus/verdict/bundle.py
- Agent: `security_auditor`
- Status: `CODE FACT`
- Description: parameter reaches os.path operation without proven normalization
- Reasoning: AST detector emitted this observation: path-traversal.
- Source commit: unavailable (source evidence retained)

### MEDIUM · corvus/corvus/verdict/bundle.py
- Agent: `security_auditor`
- Status: `CODE FACT`
- Description: parameter reaches open() without proven normalization
- Reasoning: AST detector emitted this observation: path-traversal.
- Source commit: unavailable (source evidence retained)

### MEDIUM · corvus/corvus/verdict/bundle.py
- Agent: `security_auditor`
- Status: `CODE FACT`
- Description: parameter reaches open() without proven normalization
- Reasoning: AST detector emitted this observation: path-traversal.
- Source commit: unavailable (source evidence retained)

### MEDIUM · tests/test_qwen_agent.py
- Agent: `integrity_inspector`
- Status: `CODE FACT`
- Description: unversioned serialization
- Reasoning: AST detector emitted this observation: unversioned-serialization.
- Source commit: `892d166eef137851f45f77c8fa6407e6f1ae1ad0`

### MEDIUM · corvus_cronos/qwen_agent.py
- Agent: `integrity_inspector`
- Status: `CODE FACT`
- Description: unversioned serialization
- Reasoning: AST detector emitted this observation: unversioned-serialization.
- Source commit: `892d166eef137851f45f77c8fa6407e6f1ae1ad0`

### MEDIUM · corvus_cronos/bridge.py
- Agent: `integrity_inspector`
- Status: `CODE FACT`
- Description: unversioned serialization
- Reasoning: AST detector emitted this observation: unversioned-serialization.
- Source commit: `8a18d8f9bfa57ee2f7eb698b97a708869994c1ca`

### MEDIUM · scripts/redteam_nightly.py
- Agent: `integrity_inspector`
- Status: `CODE FACT`
- Description: unversioned serialization
- Reasoning: AST detector emitted this observation: unversioned-serialization.
- Source commit: `de3b2b1c9c2c246c7aa126e12973e8082ade2642`

### MEDIUM · cronos/cronos/store.py
- Agent: `integrity_inspector`
- Status: `CODE FACT`
- Description: unversioned serialization
- Reasoning: AST detector emitted this observation: unversioned-serialization.
- Source commit: `13075d0bb42adc84052f3e0e78a28b970775f910`

### MEDIUM · cronos/cronos/chain.py
- Agent: `integrity_inspector`
- Status: `CODE FACT`
- Description: unversioned serialization
- Reasoning: AST detector emitted this observation: unversioned-serialization.
- Source commit: `13075d0bb42adc84052f3e0e78a28b970775f910`

### MEDIUM · cronos/cronos/chain.py
- Agent: `integrity_inspector`
- Status: `CODE FACT`
- Description: unversioned serialization
- Reasoning: AST detector emitted this observation: unversioned-serialization.
- Source commit: `13075d0bb42adc84052f3e0e78a28b970775f910`

### MEDIUM · cronos/tests/test_chain.py
- Agent: `integrity_inspector`
- Status: `CODE FACT`
- Description: unversioned serialization
- Reasoning: AST detector emitted this observation: unversioned-serialization.
- Source commit: `13075d0bb42adc84052f3e0e78a28b970775f910`

### MEDIUM · cronos/tests/test_chain.py
- Agent: `integrity_inspector`
- Status: `CODE FACT`
- Description: unversioned serialization
- Reasoning: AST detector emitted this observation: unversioned-serialization.
- Source commit: `13075d0bb42adc84052f3e0e78a28b970775f910`

### MEDIUM · corvus/tests/test_regressions.py
- Agent: `integrity_inspector`
- Status: `CODE FACT`
- Description: unversioned serialization
- Reasoning: AST detector emitted this observation: unversioned-serialization.
- Source commit: `13075d0bb42adc84052f3e0e78a28b970775f910`

### MEDIUM · corvus/corvus/memory/audit.py
- Agent: `integrity_inspector`
- Status: `CODE FACT`
- Description: unversioned serialization
- Reasoning: AST detector emitted this observation: unversioned-serialization.
- Source commit: `13075d0bb42adc84052f3e0e78a28b970775f910`

### MEDIUM · corvus/corvus/verdict/bundle.py
- Agent: `integrity_inspector`
- Status: `CODE FACT`
- Description: unversioned serialization
- Reasoning: AST detector emitted this observation: unversioned-serialization.
- Source commit: `13075d0bb42adc84052f3e0e78a28b970775f910`

### LOW · corvus/corvus/analysis/__init__.py
- Agent: `honest-degradation`
- Status: `PROTOCOL_GAP`
- Description: exception handler returns a plausible fallback without raising or marking degraded state
- Reasoning: A degraded-input handler is structurally silent, so callers cannot distinguish fallback data from verified data.
- Source commit: `13075d0bb42adc84052f3e0e78a28b970775f910`

### LOW · corvus/corvus/memory/consolidator.py
- Agent: `tamper-evident-audit-chain`
- Status: `PROTOCOL_GAP`
- Description: persistent audit/ledger append has no visible link to a previous entry hash
- Reasoning: A plain append-only record cannot detect deletion, insertion, or reordering after the fact.
- Source commit: `13075d0bb42adc84052f3e0e78a28b970775f910`

### LOW · corvus/corvus/memory/engine.py
- Agent: `atomic-state-mutation`
- Status: `PROTOCOL_GAP`
- Description: related SQL mutations occur without a visible transaction boundary
- Reasoning: A crash between related writes can leave persistent state only partially mutated.
- Source commit: `13075d0bb42adc84052f3e0e78a28b970775f910`

### LOW · corvus/corvus/memory/engine.py
- Agent: `honest-degradation`
- Status: `PROTOCOL_GAP`
- Description: exception handler returns a plausible fallback without raising or marking degraded state
- Reasoning: A degraded-input handler is structurally silent, so callers cannot distinguish fallback data from verified data.
- Source commit: `13075d0bb42adc84052f3e0e78a28b970775f910`

### LOW · corvus/corvus/memory/engine.py
- Agent: `tamper-evident-audit-chain`
- Status: `PROTOCOL_GAP`
- Description: persistent audit/ledger append has no visible link to a previous entry hash
- Reasoning: A plain append-only record cannot detect deletion, insertion, or reordering after the fact.
- Source commit: `13075d0bb42adc84052f3e0e78a28b970775f910`

### LOW · corvus/corvus/verdict/bundle.py
- Agent: `validate-at-the-boundary`
- Status: `PROTOCOL_GAP`
- Description: parameter `path` reaches a sensitive boundary call without an explicit raising validation
- Reasoning: validate-at-the-boundary applies because direct external input reaches a parser or filesystem call.
- Source commit: `13075d0bb42adc84052f3e0e78a28b970775f910`

### LOW · corvus/tests/test_memory.py
- Agent: `tamper-evident-audit-chain`
- Status: `PROTOCOL_GAP`
- Description: persistent audit/ledger append has no visible link to a previous entry hash
- Reasoning: A plain append-only record cannot detect deletion, insertion, or reordering after the fact.
- Source commit: `13075d0bb42adc84052f3e0e78a28b970775f910`

### LOW · corvus/tests/test_memory.py
- Agent: `tamper-evident-audit-chain`
- Status: `PROTOCOL_GAP`
- Description: persistent audit/ledger append has no visible link to a previous entry hash
- Reasoning: A plain append-only record cannot detect deletion, insertion, or reordering after the fact.
- Source commit: `13075d0bb42adc84052f3e0e78a28b970775f910`

### LOW · corvus_cronos/bridge.py
- Agent: `tamper-evident-audit-chain`
- Status: `PROTOCOL_GAP`
- Description: persistent audit/ledger append has no visible link to a previous entry hash
- Reasoning: A plain append-only record cannot detect deletion, insertion, or reordering after the fact.
- Source commit: `92e7f24a2c9a485c135b0f78a8d4fe8b4c5d999c`

### LOW · corvus_cronos/qwen_agent.py
- Agent: `sql-aggregation-not-materialization`
- Status: `PROTOCOL_GAP`
- Description: SQL execute occurs inside an application loop (potential N+1 query pattern)
- Reasoning: A batched query or preload should be considered before issuing one query per loop item.
- Source commit: `892d166eef137851f45f77c8fa6407e6f1ae1ad0`

### LOW · corvus_cronos/qwen_agent.py
- Agent: `sql-aggregation-not-materialization`
- Status: `PROTOCOL_GAP`
- Description: SQL execute occurs inside an application loop (potential N+1 query pattern)
- Reasoning: A batched query or preload should be considered before issuing one query per loop item.
- Source commit: `892d166eef137851f45f77c8fa6407e6f1ae1ad0`

### LOW · cronos/cronos/chain.py
- Agent: `tamper-evident-audit-chain`
- Status: `PROTOCOL_GAP`
- Description: persistent audit/ledger append has no visible link to a previous entry hash
- Reasoning: A plain append-only record cannot detect deletion, insertion, or reordering after the fact.
- Source commit: `13075d0bb42adc84052f3e0e78a28b970775f910`

### LOW · cronos/cronos/chain.py
- Agent: `tamper-evident-audit-chain`
- Status: `PROTOCOL_GAP`
- Description: persistent audit/ledger append has no visible link to a previous entry hash
- Reasoning: A plain append-only record cannot detect deletion, insertion, or reordering after the fact.
- Source commit: `13075d0bb42adc84052f3e0e78a28b970775f910`

### LOW · cronos/cronos/store.py
- Agent: `sql-aggregation-not-materialization`
- Status: `PROTOCOL_GAP`
- Description: SQL execute occurs inside an application loop (potential N+1 query pattern)
- Reasoning: A batched query or preload should be considered before issuing one query per loop item.
- Source commit: `13075d0bb42adc84052f3e0e78a28b970775f910`

### LOW · cronos/cronos/store.py
- Agent: `tamper-evident-audit-chain`
- Status: `PROTOCOL_GAP`
- Description: persistent audit/ledger append has no visible link to a previous entry hash
- Reasoning: A plain append-only record cannot detect deletion, insertion, or reordering after the fact.
- Source commit: `13075d0bb42adc84052f3e0e78a28b970775f910`

### LOW · cronos/cronos/tracer.py
- Agent: `tamper-evident-audit-chain`
- Status: `PROTOCOL_GAP`
- Description: persistent audit/ledger append has no visible link to a previous entry hash
- Reasoning: A plain append-only record cannot detect deletion, insertion, or reordering after the fact.
- Source commit: `13075d0bb42adc84052f3e0e78a28b970775f910`

### LOW · cronos/slack/output.py
- Agent: `tamper-evident-audit-chain`
- Status: `PROTOCOL_GAP`
- Description: persistent audit/ledger append has no visible link to a previous entry hash
- Reasoning: A plain append-only record cannot detect deletion, insertion, or reordering after the fact.
- Source commit: `13075d0bb42adc84052f3e0e78a28b970775f910`

### LOW · cronos/tests/test_chain.py
- Agent: `tamper-evident-audit-chain`
- Status: `PROTOCOL_GAP`
- Description: persistent audit/ledger append has no visible link to a previous entry hash
- Reasoning: A plain append-only record cannot detect deletion, insertion, or reordering after the fact.
- Source commit: `13075d0bb42adc84052f3e0e78a28b970775f910`

### LOW · cronos/tests/test_chain.py
- Agent: `tamper-evident-audit-chain`
- Status: `PROTOCOL_GAP`
- Description: persistent audit/ledger append has no visible link to a previous entry hash
- Reasoning: A plain append-only record cannot detect deletion, insertion, or reordering after the fact.
- Source commit: `13075d0bb42adc84052f3e0e78a28b970775f910`

### LOW · cronos/tests/test_chain.py
- Agent: `tamper-evident-audit-chain`
- Status: `PROTOCOL_GAP`
- Description: persistent audit/ledger append has no visible link to a previous entry hash
- Reasoning: A plain append-only record cannot detect deletion, insertion, or reordering after the fact.
- Source commit: `13075d0bb42adc84052f3e0e78a28b970775f910`

### LOW · cronos/tests/test_chain.py
- Agent: `tamper-evident-audit-chain`
- Status: `PROTOCOL_GAP`
- Description: persistent audit/ledger append has no visible link to a previous entry hash
- Reasoning: A plain append-only record cannot detect deletion, insertion, or reordering after the fact.
- Source commit: `13075d0bb42adc84052f3e0e78a28b970775f910`

### LOW · cronos/tests/test_chain.py
- Agent: `tamper-evident-audit-chain`
- Status: `PROTOCOL_GAP`
- Description: persistent audit/ledger append has no visible link to a previous entry hash
- Reasoning: A plain append-only record cannot detect deletion, insertion, or reordering after the fact.
- Source commit: `13075d0bb42adc84052f3e0e78a28b970775f910`

### LOW · cronos/tests/test_chain.py
- Agent: `tamper-evident-audit-chain`
- Status: `PROTOCOL_GAP`
- Description: persistent audit/ledger append has no visible link to a previous entry hash
- Reasoning: A plain append-only record cannot detect deletion, insertion, or reordering after the fact.
- Source commit: `13075d0bb42adc84052f3e0e78a28b970775f910`

### LOW · cronos/tests/test_chain.py
- Agent: `tamper-evident-audit-chain`
- Status: `PROTOCOL_GAP`
- Description: persistent audit/ledger append has no visible link to a previous entry hash
- Reasoning: A plain append-only record cannot detect deletion, insertion, or reordering after the fact.
- Source commit: `13075d0bb42adc84052f3e0e78a28b970775f910`

### LOW · cronos/tests/test_store.py
- Agent: `tamper-evident-audit-chain`
- Status: `PROTOCOL_GAP`
- Description: persistent audit/ledger append has no visible link to a previous entry hash
- Reasoning: A plain append-only record cannot detect deletion, insertion, or reordering after the fact.
- Source commit: `13075d0bb42adc84052f3e0e78a28b970775f910`

### LOW · scripts/redteam_nightly.py
- Agent: `tamper-evident-audit-chain`
- Status: `PROTOCOL_GAP`
- Description: persistent audit/ledger append has no visible link to a previous entry hash
- Reasoning: A plain append-only record cannot detect deletion, insertion, or reordering after the fact.
- Source commit: `de3b2b1c9c2c246c7aa126e12973e8082ade2642`

### LOW · tests/test_bridge.py
- Agent: `tamper-evident-audit-chain`
- Status: `PROTOCOL_GAP`
- Description: persistent audit/ledger append has no visible link to a previous entry hash
- Reasoning: A plain append-only record cannot detect deletion, insertion, or reordering after the fact.
- Source commit: `8a18d8f9bfa57ee2f7eb698b97a708869994c1ca`

### LOW · tests/test_bridge.py
- Agent: `tamper-evident-audit-chain`
- Status: `PROTOCOL_GAP`
- Description: persistent audit/ledger append has no visible link to a previous entry hash
- Reasoning: A plain append-only record cannot detect deletion, insertion, or reordering after the fact.
- Source commit: `92e7f24a2c9a485c135b0f78a8d4fe8b4c5d999c`

### LOW · tests/test_bridge.py
- Agent: `tamper-evident-audit-chain`
- Status: `PROTOCOL_GAP`
- Description: persistent audit/ledger append has no visible link to a previous entry hash
- Reasoning: A plain append-only record cannot detect deletion, insertion, or reordering after the fact.
- Source commit: `92e7f24a2c9a485c135b0f78a8d4fe8b4c5d999c`

## Limitations

- Hypotheses require module 3 verification; parser candidates may receive isolated induction, while unsupported families remain AST-only.
- 614 discovered file(s) were skipped; see skipped_reasons for the exact paths and policy categories.
- 18 triaged module(s) were outside CONNECTED_ALIVE audit scope.
- 46 skill applicability result(s) were UNDETERMINED; no conclusion was inferred for them.
- 8 hypothesis/hypotheses survived structural verification without dynamic induction; they remain plausible hypotheses, not confirmed defects.
