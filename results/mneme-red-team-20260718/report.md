# FORGE audit report

Repository: `/home/labestiadevigia/mneme`
Seal: **VERIFIED**
Findings: **58** · Discarded hypotheses: **4**
Finding-set digest: `0430c43927e68f4dd42882d7022992e231f098e86ed728130361bf6ea7537671`
Eligible source coverage: **12/12 (100.0%)**
Discovery accounting: **12/138 discovered files**
Audit disposition: **ABSTAIN_INSUFFICIENT_SCOPE**

## Repository profile

- Modules: 12 (9 connected)
- Domains: audit_or_ledger, cryptographic, determinism_sensitive, input_boundary, serialization_or_persistence
- Audit duration: 5.483358 seconds

## Findings

### MEDIUM · mneme/bundle.py
- Agent: `bug_investigator`
- Status: `PLAUSIBLE HYPOTHESIS`
- Description: The parser call `sid = json.loads(pj).get("sweep_id")` at mneme/bundle.py:180 has no nearby exception handling, so malformed input may escape as an opaque failure.
- Reasoning: Observed construct matches, but induction only established that an error path is reachable: Malformed input reached an opaque AttributeError, but the exception did not originate at the hypothesized parser call. Evidence: mneme/bundle.py:180: AttributeError: 'str' object has no attribute 'execute' [target frames: /home/labestiadevigia/mneme/mneme/bundle.py:130]
- Source commit: `834e3271690218872225a489bf306957a5254c5f`

### MEDIUM · mneme/bundle.py
- Agent: `bug_investigator`
- Status: `PLAUSIBLE HYPOTHESIS`
- Description: The parser call `payload = json.loads(r["payload_json"])` at mneme/bundle.py:216 has no nearby exception handling, so malformed input may escape as an opaque failure.
- Reasoning: Observed construct matches, but induction only established that an error path is reachable: Malformed input reached an opaque TypeError, but the exception did not originate at the hypothesized parser call. Evidence: mneme/bundle.py:216: TypeError: string indices must be integers, not 'str' [target frames: /home/labestiadevigia/mneme/mneme/bundle.py:214]
- Source commit: `f9c41e1d302deb32d3ea548139960e1e59eec124`

### MEDIUM · mneme/field.py
- Agent: `bug_investigator`
- Status: `PLAUSIBLE HYPOTHESIS`
- Description: The parser call `other_claim = json.loads(pj).get("claim")` at mneme/field.py:212 has no nearby exception handling, so malformed input may escape as an opaque failure.
- Reasoning: Observed construct matches, but induction only established that an error path is reachable: Malformed input reached an opaque TypeError, but the exception did not originate at the hypothesized parser call. Evidence: mneme/field.py:212: TypeError: store() takes 1 positional argument but 7 were given
- Source commit: `f9c41e1d302deb32d3ea548139960e1e59eec124`

### MEDIUM · mneme/field.py
- Agent: `bug_investigator`
- Status: `PLAUSIBLE HYPOTHESIS`
- Description: The parser call `served = json.loads(served_json)["served"]` at mneme/field.py:461 has no nearby exception handling, so malformed input may escape as an opaque failure.
- Reasoning: Observed construct matches, but induction only established that an error path is reachable: Malformed input reached an opaque AttributeError, but the exception did not originate at the hypothesized parser call. Evidence: mneme/field.py:461: AttributeError: 'str' object has no attribute 'execute' [target frames: /home/labestiadevigia/mneme/mneme/field.py:454]
- Source commit: `e4388ac904914df7e6d64f08645227021a78042f`

### MEDIUM · tests/test_bundle_pure.py
- Agent: `bug_investigator`
- Status: `PLAUSIBLE HYPOTHESIS`
- Description: The parser call `pbody = json.loads(partial)["body"]` at tests/test_bundle_pure.py:134 has no nearby exception handling, so malformed input may escape as an opaque failure.
- Reasoning: Observed construct matches; induction was undetermined: No synchronous module-level function boundary was found.
- Source commit: `834e3271690218872225a489bf306957a5254c5f`

### MEDIUM · tests/test_bundle_pure.py
- Agent: `bug_investigator`
- Status: `PLAUSIBLE HYPOTHESIS`
- Description: The parser call `json.loads(honest)["body"]["excluded_sweeps"] == [])` at tests/test_bundle_pure.py:139 has no nearby exception handling, so malformed input may escape as an opaque failure.
- Reasoning: Observed construct matches; induction was undetermined: No synchronous module-level function boundary was found.
- Source commit: `834e3271690218872225a489bf306957a5254c5f`

### MEDIUM · tests/test_bundle_pure.py
- Agent: `bug_investigator`
- Status: `PLAUSIBLE HYPOTHESIS`
- Description: The parser call `tb = json.loads(bundle.export_bundle(cur4))` at tests/test_bundle_pure.py:191 has no nearby exception handling, so malformed input may escape as an opaque failure.
- Reasoning: Observed construct matches; induction was undetermined: No synchronous module-level function boundary was found.
- Source commit: `89360b63dca05d6caaf73e225490d4453af98002`

### MEDIUM · tests/test_bundle_pure.py
- Agent: `bug_investigator`
- Status: `PLAUSIBLE HYPOTHESIS`
- Description: The parser call `payload=json.loads(ch[1]["payload_json"]))` at tests/test_bundle_pure.py:199 has no nearby exception handling, so malformed input may escape as an opaque failure.
- Reasoning: Observed construct matches; induction was undetermined: No synchronous module-level function boundary was found.
- Source commit: `89360b63dca05d6caaf73e225490d4453af98002`

### MEDIUM · tests/test_bundle_pure.py
- Agent: `bug_investigator`
- Status: `PLAUSIBLE HYPOTHESIS`
- Description: The parser call `doc = json.loads(honest)` at tests/test_bundle_pure.py:209 has no nearby exception handling, so malformed input may escape as an opaque failure.
- Reasoning: Observed construct matches; induction was undetermined: No synchronous module-level function boundary was found.
- Source commit: `f9c41e1d302deb32d3ea548139960e1e59eec124`

### MEDIUM · tests/test_bundle_pure.py
- Agent: `bug_investigator`
- Status: `PLAUSIBLE HYPOTHESIS`
- Description: The parser call `t = json.loads(honest)` at tests/test_bundle_pure.py:211 has no nearby exception handling, so malformed input may escape as an opaque failure.
- Reasoning: Observed construct matches; induction was undetermined: No synchronous module-level function boundary was found.
- Source commit: `f9c41e1d302deb32d3ea548139960e1e59eec124`

### MEDIUM · tests/test_bundle_pure.py
- Agent: `bug_investigator`
- Status: `PLAUSIBLE HYPOTHESIS`
- Description: The parser call `t = json.loads(honest)` at tests/test_bundle_pure.py:215 has no nearby exception handling, so malformed input may escape as an opaque failure.
- Reasoning: Observed construct matches; induction was undetermined: No synchronous module-level function boundary was found.
- Source commit: `f9c41e1d302deb32d3ea548139960e1e59eec124`

### MEDIUM · tests/test_bundle_pure.py
- Agent: `bug_investigator`
- Status: `PLAUSIBLE HYPOTHESIS`
- Description: The parser call `t = json.loads(honest)` at tests/test_bundle_pure.py:221 has no nearby exception handling, so malformed input may escape as an opaque failure.
- Reasoning: Observed construct matches; induction was undetermined: No synchronous module-level function boundary was found.
- Source commit: `f9c41e1d302deb32d3ea548139960e1e59eec124`

### MEDIUM · tests/test_bundle_pure.py
- Agent: `bug_investigator`
- Status: `PLAUSIBLE HYPOTHESIS`
- Description: The parser call `t = json.loads(honest)` at tests/test_bundle_pure.py:227 has no nearby exception handling, so malformed input may escape as an opaque failure.
- Reasoning: Observed construct matches; induction was undetermined: No synchronous module-level function boundary was found.
- Source commit: `f9c41e1d302deb32d3ea548139960e1e59eec124`

### MEDIUM · tests/test_bundle_pure.py
- Agent: `bug_investigator`
- Status: `PLAUSIBLE HYPOTHESIS`
- Description: The parser call `t = json.loads(honest)` at tests/test_bundle_pure.py:235 has no nearby exception handling, so malformed input may escape as an opaque failure.
- Reasoning: Observed construct matches; induction was undetermined: No synchronous module-level function boundary was found.
- Source commit: `f9c41e1d302deb32d3ea548139960e1e59eec124`

### MEDIUM · tests/test_bundle_pure.py
- Agent: `bug_investigator`
- Status: `PLAUSIBLE HYPOTHESIS`
- Description: The parser call `t = json.loads(honest)` at tests/test_bundle_pure.py:243 has no nearby exception handling, so malformed input may escape as an opaque failure.
- Reasoning: Observed construct matches; induction was undetermined: No synchronous module-level function boundary was found.
- Source commit: `f9c41e1d302deb32d3ea548139960e1e59eec124`

### MEDIUM · tests/test_bundle_pure.py
- Agent: `bug_investigator`
- Status: `PLAUSIBLE HYPOTHESIS`
- Description: The parser call `t = json.loads(honest)` at tests/test_bundle_pure.py:251 has no nearby exception handling, so malformed input may escape as an opaque failure.
- Reasoning: Observed construct matches; induction was undetermined: No synchronous module-level function boundary was found.
- Source commit: `834e3271690218872225a489bf306957a5254c5f`

### MEDIUM · tests/test_bundle_pure.py
- Agent: `bug_investigator`
- Status: `PLAUSIBLE HYPOTHESIS`
- Description: The parser call `t = json.loads(partial)` at tests/test_bundle_pure.py:260 has no nearby exception handling, so malformed input may escape as an opaque failure.
- Reasoning: Observed construct matches; induction was undetermined: No synchronous module-level function boundary was found.
- Source commit: `834e3271690218872225a489bf306957a5254c5f`

### MEDIUM · tests/test_bundle_pure.py
- Agent: `bug_investigator`
- Status: `PLAUSIBLE HYPOTHESIS`
- Description: The parser call `t = json.loads(partial)` at tests/test_bundle_pure.py:268 has no nearby exception handling, so malformed input may escape as an opaque failure.
- Reasoning: Observed construct matches; induction was undetermined: No synchronous module-level function boundary was found.
- Source commit: `834e3271690218872225a489bf306957a5254c5f`

### MEDIUM · tests/test_bundle_pure.py
- Agent: `bug_investigator`
- Status: `PLAUSIBLE HYPOTHESIS`
- Description: The parser call `t = json.loads(honest)` at tests/test_bundle_pure.py:275 has no nearby exception handling, so malformed input may escape as an opaque failure.
- Reasoning: Observed construct matches; induction was undetermined: No synchronous module-level function boundary was found.
- Source commit: `834e3271690218872225a489bf306957a5254c5f`

### MEDIUM · tests/test_bundle_pure.py
- Agent: `bug_investigator`
- Status: `PLAUSIBLE HYPOTHESIS`
- Description: The parser call `t = json.loads(honest)` at tests/test_bundle_pure.py:283 has no nearby exception handling, so malformed input may escape as an opaque failure.
- Reasoning: Observed construct matches; induction was undetermined: No synchronous module-level function boundary was found.
- Source commit: `f9c41e1d302deb32d3ea548139960e1e59eec124`

### MEDIUM · tests/test_bundle_pure.py
- Agent: `bug_investigator`
- Status: `PLAUSIBLE HYPOTHESIS`
- Description: The parser call `t = json.loads(honest)` at tests/test_bundle_pure.py:294 has no nearby exception handling, so malformed input may escape as an opaque failure.
- Reasoning: Observed construct matches; induction was undetermined: No synchronous module-level function boundary was found.
- Source commit: `f9c41e1d302deb32d3ea548139960e1e59eec124`

### MEDIUM · tests/test_bundle_pure.py
- Agent: `bug_investigator`
- Status: `PLAUSIBLE HYPOTHESIS`
- Description: The dynamic command invocation `r = subprocess.run([sys.executable,` at tests/test_bundle_pure.py:307 may pass attacker-controlled arguments without an enclosing failure boundary.
- Reasoning: Observed construct matches; induction was undetermined: No synchronous module-level function boundary was found.
- Source commit: `f9c41e1d302deb32d3ea548139960e1e59eec124`

### MEDIUM · tests/test_bundle_pure.py
- Agent: `bug_investigator`
- Status: `PLAUSIBLE HYPOTHESIS`
- Description: The dynamic command invocation `r = subprocess.run([sys.executable,` at tests/test_bundle_pure.py:315 may pass attacker-controlled arguments without an enclosing failure boundary.
- Reasoning: Observed construct matches; induction was undetermined: No synchronous module-level function boundary was found.
- Source commit: `834e3271690218872225a489bf306957a5254c5f`

### MEDIUM · tests/test_bundle_pure.py
- Agent: `bug_investigator`
- Status: `PLAUSIBLE HYPOTHESIS`
- Description: The dynamic command invocation `r = subprocess.run([sys.executable,` at tests/test_bundle_pure.py:324 may pass attacker-controlled arguments without an enclosing failure boundary.
- Reasoning: Observed construct matches; induction was undetermined: No synchronous module-level function boundary was found.
- Source commit: `f9c41e1d302deb32d3ea548139960e1e59eec124`

### MEDIUM · tests/test_field_pure.py
- Agent: `bug_investigator`
- Status: `PLAUSIBLE HYPOTHESIS`
- Description: The parser call `and json.loads(last[1])["successor_memory_id"] == "mem-new", str(last))` at tests/test_field_pure.py:241 has no nearby exception handling, so malformed input may escape as an opaque failure.
- Reasoning: Observed construct matches; induction was undetermined: No synchronous module-level function boundary was found.
- Source commit: `e4388ac904914df7e6d64f08645227021a78042f`

### MEDIUM · tests/test_field_pure.py
- Agent: `bug_investigator`
- Status: `PLAUSIBLE HYPOTHESIS`
- Description: The parser call `json.loads(birth).get("supersedes") == "mem-old")` at tests/test_field_pure.py:245 has no nearby exception handling, so malformed input may escape as an opaque failure.
- Reasoning: Observed construct matches; induction was undetermined: No synchronous module-level function boundary was found.
- Source commit: `e4388ac904914df7e6d64f08645227021a78042f`

### MEDIUM · mneme/trust.py
- Agent: `security_auditor`
- Status: `CODE FACT`
- Description: unsafe SQL interpolation reaches execute() without parameter binding
- Reasoning: AST detector emitted this observation: sql-injection.
- Source commit: `f9c41e1d302deb32d3ea548139960e1e59eec124`

### MEDIUM · tests/test_custody_pure.py
- Agent: `integrity_inspector`
- Status: `CODE FACT`
- Description: unversioned serialization
- Reasoning: AST detector emitted this observation: unversioned-serialization.
- Source commit: `f9c41e1d302deb32d3ea548139960e1e59eec124`

### MEDIUM · tests/test_bundle_pure.py
- Agent: `integrity_inspector`
- Status: `CODE FACT`
- Description: unversioned serialization
- Reasoning: AST detector emitted this observation: unversioned-serialization.
- Source commit: `89360b63dca05d6caaf73e225490d4453af98002`

### MEDIUM · tests/test_bundle_pure.py
- Agent: `integrity_inspector`
- Status: `CODE FACT`
- Description: unversioned serialization
- Reasoning: AST detector emitted this observation: unversioned-serialization.
- Source commit: `f9c41e1d302deb32d3ea548139960e1e59eec124`

### MEDIUM · tests/test_bundle_pure.py
- Agent: `integrity_inspector`
- Status: `CODE FACT`
- Description: unversioned serialization
- Reasoning: AST detector emitted this observation: unversioned-serialization.
- Source commit: `f9c41e1d302deb32d3ea548139960e1e59eec124`

### MEDIUM · tests/test_bundle_pure.py
- Agent: `integrity_inspector`
- Status: `CODE FACT`
- Description: unversioned serialization
- Reasoning: AST detector emitted this observation: unversioned-serialization.
- Source commit: `f9c41e1d302deb32d3ea548139960e1e59eec124`

### MEDIUM · tests/test_bundle_pure.py
- Agent: `integrity_inspector`
- Status: `CODE FACT`
- Description: unversioned serialization
- Reasoning: AST detector emitted this observation: unversioned-serialization.
- Source commit: `f9c41e1d302deb32d3ea548139960e1e59eec124`

### MEDIUM · tests/test_bundle_pure.py
- Agent: `integrity_inspector`
- Status: `CODE FACT`
- Description: unversioned serialization
- Reasoning: AST detector emitted this observation: unversioned-serialization.
- Source commit: `f9c41e1d302deb32d3ea548139960e1e59eec124`

### MEDIUM · tests/test_bundle_pure.py
- Agent: `integrity_inspector`
- Status: `CODE FACT`
- Description: unversioned serialization
- Reasoning: AST detector emitted this observation: unversioned-serialization.
- Source commit: `f9c41e1d302deb32d3ea548139960e1e59eec124`

### MEDIUM · tests/test_bundle_pure.py
- Agent: `integrity_inspector`
- Status: `CODE FACT`
- Description: unversioned serialization
- Reasoning: AST detector emitted this observation: unversioned-serialization.
- Source commit: `834e3271690218872225a489bf306957a5254c5f`

### MEDIUM · tests/test_bundle_pure.py
- Agent: `integrity_inspector`
- Status: `CODE FACT`
- Description: unversioned serialization
- Reasoning: AST detector emitted this observation: unversioned-serialization.
- Source commit: `834e3271690218872225a489bf306957a5254c5f`

### MEDIUM · tests/test_bundle_pure.py
- Agent: `integrity_inspector`
- Status: `CODE FACT`
- Description: unversioned serialization
- Reasoning: AST detector emitted this observation: unversioned-serialization.
- Source commit: `834e3271690218872225a489bf306957a5254c5f`

### MEDIUM · tests/test_bundle_pure.py
- Agent: `integrity_inspector`
- Status: `CODE FACT`
- Description: unversioned serialization
- Reasoning: AST detector emitted this observation: unversioned-serialization.
- Source commit: `834e3271690218872225a489bf306957a5254c5f`

### MEDIUM · tests/test_bundle_pure.py
- Agent: `integrity_inspector`
- Status: `CODE FACT`
- Description: unversioned serialization
- Reasoning: AST detector emitted this observation: unversioned-serialization.
- Source commit: `f9c41e1d302deb32d3ea548139960e1e59eec124`

### MEDIUM · tests/test_bundle_pure.py
- Agent: `integrity_inspector`
- Status: `CODE FACT`
- Description: unversioned serialization
- Reasoning: AST detector emitted this observation: unversioned-serialization.
- Source commit: `f9c41e1d302deb32d3ea548139960e1e59eec124`

### MEDIUM · tests/test_bundle_pure.py
- Agent: `integrity_inspector`
- Status: `CODE FACT`
- Description: unversioned serialization
- Reasoning: AST detector emitted this observation: unversioned-serialization.
- Source commit: `f9c41e1d302deb32d3ea548139960e1e59eec124`

### LOW · mneme/bundle.py
- Agent: `sql-aggregation-not-materialization`
- Status: `PROTOCOL_GAP`
- Description: SQL execute occurs inside an application loop (potential N+1 query pattern)
- Reasoning: A batched query or preload should be considered before issuing one query per loop item.
- Source commit: `f9c41e1d302deb32d3ea548139960e1e59eec124`

### LOW · mneme/bundle.py
- Agent: `sql-aggregation-not-materialization`
- Status: `PROTOCOL_GAP`
- Description: SQL execute occurs inside an application loop (potential N+1 query pattern)
- Reasoning: A batched query or preload should be considered before issuing one query per loop item.
- Source commit: `f9c41e1d302deb32d3ea548139960e1e59eec124`

### LOW · mneme/bundle.py
- Agent: `tamper-evident-audit-chain`
- Status: `PROTOCOL_GAP`
- Description: persistent audit/ledger append has no visible link to a previous entry hash
- Reasoning: A plain append-only record cannot detect deletion, insertion, or reordering after the fact.
- Source commit: `f9c41e1d302deb32d3ea548139960e1e59eec124`

### LOW · mneme/bundle.py
- Agent: `validate-at-the-boundary`
- Status: `PROTOCOL_GAP`
- Description: parameter `bundle_json` reaches a sensitive boundary call without an explicit raising validation
- Reasoning: validate-at-the-boundary applies because direct external input reaches a parser or filesystem call.
- Source commit: `f9c41e1d302deb32d3ea548139960e1e59eec124`

### LOW · mneme/field.py
- Agent: `atomic-state-mutation`
- Status: `PROTOCOL_GAP`
- Description: related SQL mutations occur without a visible transaction boundary
- Reasoning: A crash between related writes can leave persistent state only partially mutated.
- Source commit: `f9c41e1d302deb32d3ea548139960e1e59eec124`

### LOW · mneme/field.py
- Agent: `sql-aggregation-not-materialization`
- Status: `PROTOCOL_GAP`
- Description: SQL execute occurs inside an application loop (potential N+1 query pattern)
- Reasoning: A batched query or preload should be considered before issuing one query per loop item.
- Source commit: `f9c41e1d302deb32d3ea548139960e1e59eec124`

### LOW · mneme/field.py
- Agent: `validate-at-the-boundary`
- Status: `PROTOCOL_GAP`
- Description: parameter `s` reaches a sensitive boundary call without an explicit raising validation
- Reasoning: validate-at-the-boundary applies because direct external input reaches a parser or filesystem call.
- Source commit: `f9c41e1d302deb32d3ea548139960e1e59eec124`

### LOW · mneme/trust.py
- Agent: `sql-aggregation-not-materialization`
- Status: `PROTOCOL_GAP`
- Description: SQL execute occurs inside an application loop (potential N+1 query pattern)
- Reasoning: A batched query or preload should be considered before issuing one query per loop item.
- Source commit: `f9c41e1d302deb32d3ea548139960e1e59eec124`

### LOW · mneme/trust.py
- Agent: `tamper-evident-audit-chain`
- Status: `PROTOCOL_GAP`
- Description: persistent audit/ledger append has no visible link to a previous entry hash
- Reasoning: A plain append-only record cannot detect deletion, insertion, or reordering after the fact.
- Source commit: `f9c41e1d302deb32d3ea548139960e1e59eec124`

### LOW · mneme/trust.py
- Agent: `tamper-evident-audit-chain`
- Status: `PROTOCOL_GAP`
- Description: persistent audit/ledger append has no visible link to a previous entry hash
- Reasoning: A plain append-only record cannot detect deletion, insertion, or reordering after the fact.
- Source commit: `e4388ac904914df7e6d64f08645227021a78042f`

### LOW · mneme/trust.py
- Agent: `tamper-evident-audit-chain`
- Status: `PROTOCOL_GAP`
- Description: persistent audit/ledger append has no visible link to a previous entry hash
- Reasoning: A plain append-only record cannot detect deletion, insertion, or reordering after the fact.
- Source commit: `f9c41e1d302deb32d3ea548139960e1e59eec124`

### LOW · mneme/trust.py
- Agent: `tamper-evident-audit-chain`
- Status: `PROTOCOL_GAP`
- Description: persistent audit/ledger append has no visible link to a previous entry hash
- Reasoning: A plain append-only record cannot detect deletion, insertion, or reordering after the fact.
- Source commit: `f9c41e1d302deb32d3ea548139960e1e59eec124`

### LOW · tests/test_bundle_pure.py
- Agent: `sql-aggregation-not-materialization`
- Status: `PROTOCOL_GAP`
- Description: SQL execute occurs inside an application loop (potential N+1 query pattern)
- Reasoning: A batched query or preload should be considered before issuing one query per loop item.
- Source commit: `f9c41e1d302deb32d3ea548139960e1e59eec124`

### LOW · tests/test_custody_pure.py
- Agent: `sql-aggregation-not-materialization`
- Status: `PROTOCOL_GAP`
- Description: SQL execute occurs inside an application loop (potential N+1 query pattern)
- Reasoning: A batched query or preload should be considered before issuing one query per loop item.
- Source commit: `f9c41e1d302deb32d3ea548139960e1e59eec124`

### LOW · tests/test_field_pure.py
- Agent: `sql-aggregation-not-materialization`
- Status: `PROTOCOL_GAP`
- Description: SQL execute occurs inside an application loop (potential N+1 query pattern)
- Reasoning: A batched query or preload should be considered before issuing one query per loop item.
- Source commit: `f9c41e1d302deb32d3ea548139960e1e59eec124`

### LOW · tests/test_field_pure.py
- Agent: `sql-aggregation-not-materialization`
- Status: `PROTOCOL_GAP`
- Description: SQL execute occurs inside an application loop (potential N+1 query pattern)
- Reasoning: A batched query or preload should be considered before issuing one query per loop item.
- Source commit: `f9c41e1d302deb32d3ea548139960e1e59eec124`

## Limitations

- Hypotheses require module 3 verification; parser candidates may receive isolated induction, while unsupported families remain AST-only.
- 126 discovered file(s) were skipped; see skipped_reasons for the exact paths and policy categories.
- 3 triaged module(s) were outside CONNECTED_ALIVE audit scope.
- 4 skill applicability result(s) were UNDETERMINED; no conclusion was inferred for them.
- 26 hypothesis/hypotheses survived structural verification without dynamic induction; they remain plausible hypotheses, not confirmed defects.
