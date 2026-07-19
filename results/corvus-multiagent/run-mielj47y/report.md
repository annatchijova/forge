# Forge canonical multi-agent audit

## Status

**ABSTAINED.** The canonical set preserves external Codex hypotheses and native Forge observations; no static candidate is promoted to confirmed without induction.

Finding-set digest: `3eb856e520601bf496f6894e5099bdc0e1cad2dbd7f3bcf4ebc01cb9f2c8828a`
External Codex records: 3
Native Forge records: 73
Canonical assembly attestation: `EPHEMERAL_UNVERIFIABLE`.
External analytical provenance: `UNATTESTED`.

## Findings by source layer

### codex_external

- `codex_external:SM-1` — **UNDETERMINED** — Token-absent deployment may expose /analyze and /chat without token authentication.
- `codex_external:CR-1` — **UNDETERMINED** — Static transactional design may prevent partial persistence of closed CRONOS traces.
- `codex_external:AR-1` — **UNDETERMINED** — A generic prompt instruction outside known sanitizer markers may influence narration without altering the sealed verdict.

### forge_native

- `forge_native:0` — **PLAUSIBLE HYPOTHESIS** — The parser call `bundle = json.load(fh)` at corvus/corvus/verdict/bundle.py:96 has no nearby exception handling, so malformed input may escape as an opaque failure.
- `forge_native:1` — **PLAUSIBLE HYPOTHESIS** — The parser call `bundle = json.load(fh)` at corvus/tests/test_regressions.py:353 has no nearby exception handling, so malformed input may escape as an opaque failure.
- `forge_native:2` — **PLAUSIBLE HYPOTHESIS** — The parser call `payload=json.loads(r[1]),` at cronos/cronos/store.py:217 has no nearby exception handling, so malformed input may escape as an opaque failure.
- `forge_native:3` — **PLAUSIBLE HYPOTHESIS** — The parser call `contradictions = json.loads(contradictions_json) if contradictions_json else []` at cronos/cronos/store.py:225 has no nearby exception handling, so malformed input may escape as an opaque failure.
- `forge_native:4` — **PLAUSIBLE HYPOTHESIS** — The parser call `conf_warnings = json.loads(conf_warnings_json) if conf_warnings_json else []` at cronos/cronos/store.py:226 has no nearby exception handling, so malformed input may escape as an opaque failure.
- `forge_native:5` — **PLAUSIBLE HYPOTHESIS** — The parser call `return [{"kind": r[0], "payload": json.loads(r[1])} for r in rows]` at tests/test_full_integration.py:237 has no nearby exception handling, so malformed input may escape as an opaque failure.
- `forge_native:6` — **PLAUSIBLE HYPOTHESIS** — The parser call `data = json.loads(msg["content"])` at tests/test_qwen_agent.py:132 has no nearby exception handling, so malformed input may escape as an opaque failure.
- `forge_native:7` — **PLAUSIBLE HYPOTHESIS** — The dynamic command invocation `proc = subprocess.run(` at tests/test_redteam_nightly.py:107 may pass attacker-controlled arguments without an enclosing failure boundary.
- `forge_native:8` — **CODE FACT** — parameter reaches os.path operation without proven normalization
- `forge_native:9` — **CODE FACT** — parameter reaches os.path operation without proven normalization
- `forge_native:10` — **CODE FACT** — parameter reaches os.path operation without proven normalization
- `forge_native:11` — **CODE FACT** — parameter reaches os.path operation without proven normalization
- `forge_native:12` — **CODE FACT** — parameter reaches os.path operation without proven normalization
- `forge_native:13` — **CODE FACT** — parameter reaches os.path operation without proven normalization
- `forge_native:14` — **CODE FACT** — parameter reaches os.path operation without proven normalization
- `forge_native:15` — **CODE FACT** — non-empty credential-like string stored under 'X-API-Token'
- `forge_native:16` — **CODE FACT** — non-empty credential-like string stored under 'X-API-Token'
- `forge_native:17` — **CODE FACT** — parameter reaches os.path operation without proven normalization
- `forge_native:18` — **CODE FACT** — parameter reaches os.path operation without proven normalization
- `forge_native:19` — **CODE FACT** — parameter reaches os.path operation without proven normalization
- `forge_native:20` — **CODE FACT** — parameter reaches os.path operation without proven normalization
- `forge_native:21` — **CODE FACT** — parameter reaches os.path operation without proven normalization
- `forge_native:22` — **CODE FACT** — parameter reaches os.path operation without proven normalization
- `forge_native:23` — **CODE FACT** — parameter reaches os.path operation without proven normalization
- `forge_native:24` — **CODE FACT** — parameter reaches os.path operation without proven normalization
- `forge_native:25` — **CODE FACT** — parameter reaches os.path operation without proven normalization
- `forge_native:26` — **CODE FACT** — parameter reaches open() without proven normalization
- `forge_native:27` — **CODE FACT** — parameter reaches open() without proven normalization
- `forge_native:28` — **CODE FACT** — parameter reaches os.path operation without proven normalization
- `forge_native:29` — **CODE FACT** — parameter reaches os.path operation without proven normalization
- `forge_native:30` — **CODE FACT** — parameter reaches open() without proven normalization
- `forge_native:31` — **CODE FACT** — parameter reaches open() without proven normalization
- `forge_native:32` — **CODE FACT** — unversioned serialization
- `forge_native:33` — **CODE FACT** — unversioned serialization
- `forge_native:34` — **CODE FACT** — unversioned serialization
- `forge_native:35` — **CODE FACT** — unversioned serialization
- `forge_native:36` — **CODE FACT** — unversioned serialization
- `forge_native:37` — **CODE FACT** — unversioned serialization
- `forge_native:38` — **CODE FACT** — unversioned serialization
- `forge_native:39` — **CODE FACT** — unversioned serialization
- `forge_native:40` — **CODE FACT** — unversioned serialization
- `forge_native:41` — **CODE FACT** — unversioned serialization
- `forge_native:42` — **CODE FACT** — unversioned serialization
- `forge_native:43` — **CODE FACT** — unversioned serialization
- `forge_native:44` — **PROTOCOL_GAP** — exception handler returns a plausible fallback without raising or marking degraded state
- `forge_native:45` — **PROTOCOL_GAP** — persistent audit/ledger append has no visible link to a previous entry hash
- `forge_native:46` — **PROTOCOL_GAP** — related SQL mutations occur without a visible transaction boundary
- `forge_native:47` — **PROTOCOL_GAP** — exception handler returns a plausible fallback without raising or marking degraded state
- `forge_native:48` — **PROTOCOL_GAP** — persistent audit/ledger append has no visible link to a previous entry hash
- `forge_native:49` — **PROTOCOL_GAP** — parameter `path` reaches a sensitive boundary call without an explicit raising validation
- `forge_native:50` — **PROTOCOL_GAP** — persistent audit/ledger append has no visible link to a previous entry hash
- `forge_native:51` — **PROTOCOL_GAP** — persistent audit/ledger append has no visible link to a previous entry hash
- `forge_native:52` — **PROTOCOL_GAP** — persistent audit/ledger append has no visible link to a previous entry hash
- `forge_native:53` — **PROTOCOL_GAP** — SQL execute occurs inside an application loop (potential N+1 query pattern)
- `forge_native:54` — **PROTOCOL_GAP** — SQL execute occurs inside an application loop (potential N+1 query pattern)
- `forge_native:55` — **PROTOCOL_GAP** — persistent audit/ledger append has no visible link to a previous entry hash
- `forge_native:56` — **PROTOCOL_GAP** — persistent audit/ledger append has no visible link to a previous entry hash
- `forge_native:57` — **PROTOCOL_GAP** — SQL execute occurs inside an application loop (potential N+1 query pattern)
- `forge_native:58` — **PROTOCOL_GAP** — persistent audit/ledger append has no visible link to a previous entry hash
- `forge_native:59` — **PROTOCOL_GAP** — persistent audit/ledger append has no visible link to a previous entry hash
- `forge_native:60` — **PROTOCOL_GAP** — persistent audit/ledger append has no visible link to a previous entry hash
- `forge_native:61` — **PROTOCOL_GAP** — persistent audit/ledger append has no visible link to a previous entry hash
- `forge_native:62` — **PROTOCOL_GAP** — persistent audit/ledger append has no visible link to a previous entry hash
- `forge_native:63` — **PROTOCOL_GAP** — persistent audit/ledger append has no visible link to a previous entry hash
- `forge_native:64` — **PROTOCOL_GAP** — persistent audit/ledger append has no visible link to a previous entry hash
- `forge_native:65` — **PROTOCOL_GAP** — persistent audit/ledger append has no visible link to a previous entry hash
- `forge_native:66` — **PROTOCOL_GAP** — persistent audit/ledger append has no visible link to a previous entry hash
- `forge_native:67` — **PROTOCOL_GAP** — persistent audit/ledger append has no visible link to a previous entry hash
- `forge_native:68` — **PROTOCOL_GAP** — persistent audit/ledger append has no visible link to a previous entry hash
- `forge_native:69` — **PROTOCOL_GAP** — persistent audit/ledger append has no visible link to a previous entry hash
- `forge_native:70` — **PROTOCOL_GAP** — persistent audit/ledger append has no visible link to a previous entry hash
- `forge_native:71` — **PROTOCOL_GAP** — persistent audit/ledger append has no visible link to a previous entry hash
- `forge_native:72` — **PROTOCOL_GAP** — persistent audit/ledger append has no visible link to a previous entry hash

## Integrity and independence

- External agent independence: `INDEPENDENCE_VERIFIED`.
- Canonical finding set: sealed in `verification-manifest.canonical.sealed.json`.
- The canonical seal includes the updated external-agent audit trace.
- Assembly attestation and analytical provenance are separate claims.
- The seal proves artifact integrity, not finding correctness or an external layer's analytical provenance.
