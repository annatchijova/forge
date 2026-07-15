# Security Audit — `forge` (working tree)
## Red Team Round 1–2
**Date:** 2026-07-15
**Method:** Abductive Engineering (A–D–I) + Red-Team Auditing
**Scope:** `forge/*.py` (~3551 lines): sealing/canonicalization, git ref handling
(`git_refs.py`, `loop.py`, `loop_mcp.py` — new/uncommitted, least-reviewed), the
MCP tool surface (`mcp_server.py`, `cronos_mcp_server.py`, `loop_mcp.py`), the
core decision path (`verification.py`, `induction.py`, `hypotheses.py`,
`disposition.py`, `contradictions.py`), report/seal rendering. Out of scope:
`forge/agents/*` heuristic scanners' detection accuracy, `tests/`, dependency
supply chain.
**Base:** branch `agent/improve-forge-audit-reporting` @ commit `c4b8a2d25cbbb9b33e48b77ea058a3284913fdce`
(working tree has uncommitted changes to `cli.py`, `mcp_server.py`, `runtime.py`
and untracked `git_refs.py`, `loop.py`, `loop_mcp.py` — audited as they sit on disk).
**Environment:** Python 3.12.3, git 2.43.0, Linux.
**Reproducible evidence:** commands below are copy-pasteable; run from repo root
with `sys.path.insert(0, '.')` in the Python one-liners.

> **Process note on this audit:** three attempts to delegate the investigation
> to a background subagent ("fork") returned near-instantly (0–1 tool calls,
> 2–55s) with text that closely mirrored the coordinator's own prior phrasing
> instead of genuine findings. Per this skill's own epistemic discipline, that
> output was treated as unverified and discarded rather than reported as
> real. All findings below were produced by direct inline reading and
> execution against the live repository — no delegated/unverified output is
> included.

## Threat model
- Attacker CAN: control the *contents* of a Git repository handed to FORGE for
  audit (branch names, ref names via low-level plumbing, commit messages, file
  contents, patch text); call any exposed MCP tool directly (`audit_repository`,
  `audit_ref`, `compare_refs`, `seal_results`, `loop_audit`, etc.) with
  attacker-chosen string/JSON arguments, as would an LLM agent orchestrating
  these tools or a lower-trust MCP client in a multi-tenant deployment.
- Attacker CANNOT: modify the `forge` source code itself; obtain the operator's
  filesystem/shell access outside what an MCP tool call grants; break SHA-256.
- Trust boundary tested: the boundary between "content of an audited repo /
  arguments to an MCP tool" (untrusted) and "the sealed verification manifest"
  (meant to be trustworthy evidence).

## Epistemic legend
CODE FACT · PLAUSIBLE HYPOTHESIS · CONFIRMED BY INDUCTION · FALSIFIED

## Executive summary
| ID | Severity | Level | Module | Finding |
|----|----------|-------|--------|---------|
| F1 | HIGH | CONFIRMED BY INDUCTION | `runtime.py:345` / MCP `seal_results` | Arbitrary caller-supplied JSON is sealed into a valid, `verify_sealed()`-passing chain with no check it came from a real audit run |
| F2 | LOW | CONFIRMED BY INDUCTION | `git_refs.py:38-44` / `runtime.py:318` | Unresolved ref strings reach `git merge-base`/`git diff` argv positions unsanitized (argument injection); demonstrated effect is a clean error, not RCE/write |
| F3 | MEDIUM | PLAUSIBLE HYPOTHESIS | `loop.py:109-112` | TOCTOU: temp dir created then deleted then recreated by `git worktree add`, a window for a local symlink race |
| F4 | INFO (threat-model) | CODE FACT | `loop_mcp.py:27,34,37` | `loop_audit` MCP tool runs a caller-supplied `test_command` as a real subprocess — by design, but undocumented as a capability grant |
| F5 | INFO (hygiene) | CODE FACT | `runtime.py:109-122,186` | `orchestrator_model`/`agent_models` params are recorded into the trace but not consumed by anything — no LLM call site exists anywhere in `forge/agents/*` yet |
| — | — | FALSIFIED | `git_refs.py:19-27,47-69` | `resolve_ref`/`archive_ref` are NOT vulnerable to the same argument-injection or RCE-via-`ext::` pattern (see Discarded vectors) |
| — | — | CONFIRMED BY INDUCTION (positive) | `canonical.py` | Canonicalization is order-independent, rejects floats, and distinguishes bool/int/str — deterministic-core invariant holds |
| — | — | CODE FACT (positive) | `verification.py`,`induction.py`,`hypotheses.py`,`disposition.py`,`contradictions.py`,`sealing.py` | Zero references to any LLM/model routing in the decision path — LLM-out-of-loop invariant holds trivially (no LLM integration exists yet) |

## Findings

### F1 — `seal_results` seals unattested content as if it were a genuine audit
**Severity:** HIGH  **Epistemic level:** CONFIRMED BY INDUCTION  **Bucket:** vulnerability (trust-boundary gap)

- **Surprise / expectation violated:** `DECISIONS.md:44-46` documents that only
  "a full-access attacker who can rewrite the entire report can forge a
  consistent replacement chain from scratch." That framing implies forgery
  requires filesystem-level access and hand-reimplementing the hash scheme.
  In fact `Runtime.seal_results()` (`runtime.py:345-351`), also exposed as the
  MCP tool `seal_results(verification_path, output)` (`mcp_server.py:228-235`),
  performs that "forgery" for the caller: it calls `load_json()` on any path,
  builds a `VerificationManifest` from whatever the JSON contains (only field
  presence/enum-membership is checked — `models.py:222-236` — not that the
  content originated from a real `Runtime.audit()` run), and writes a fully
  valid SHA-256 chain over it.
- **Abduction:** if provenance of the *input* to `seal_results` is never
  checked, a caller can hand it a hand-written manifest — no real repository
  scan, no real hypotheses, no real evidence — and receive back an artifact
  that is byte-for-byte structurally identical to (and passes the same
  verifier as) a genuine sealed FORGE report.
- **Deduction:** predict that a manifest with `root` pointing at a directory
  that was never audited, and a finding whose `evidence` says `"nowhere.py:1 /
  made up"`, will (a) be accepted by `seal_results` without error, and (b)
  report `ok: True` from `verify_sealed()`.
- **Induction — executed:**
  ```python
  from forge.runtime import Runtime
  fake = {
    "schema_version": "1", "forge_version": "fake-9.9.9", "hypotheses_schema_version": "1",
    "root": "/nonexistent/never-audited-repo", "generated_at_epoch": 0,
    "findings": [{
       "category": "OBSERVED", "epistemic_level": "CONFIRMED BY INDUCTION",
       "module_path": "totally/fabricated.py",
       "description": "Fabricated finding never produced by any real audit run",
       "evidence": [{"kind": "code", "source": "nowhere.py:1", "detail": "made up"}],
       "reasoning": "fabricated end to end", "agent": "security_auditor",
       "outcome": "OBSERVED", "severity": "CRITICAL", "provenance": []
    }],
    "discarded": [], "ast_verified_families": [], "ast_unverified_families": [],
    "induction": [], "repository_snapshot_sha256": "deadbeef"*8,
  }
  # ... written to /tmp/fake_verification.json ...
  target = Runtime().seal_results("/tmp/fake_verification.json", "/tmp/fake_verification.sealed.json")
  ```
  **Observed output:**
  ```
  sealed to /tmp/fake_verification.sealed.json
  chain length: 1
  verify_sealed result on fabricated manifest: {'ok': True, 'linkage_ok': True, 'integrity_ok': True, 'issues': []}
  ```
  Prediction held. Reproducible against commit `c4b8a2d25cbbb9b33e48b77ea058a3284913fdce`, Python 3.12.3, no external corpus needed (fixture inlined above).
- **Causal chain:**
  ```
  caller-controlled JSON file (no origin check)
      ↓ seal_results() / MCP tool "seal_results"
  load_json() + enum/field-presence validation only (no run linkage)
      ↓
  VerificationManifest built from arbitrary content
      ↓
  seal_manifest() computes a fully valid SHA-256 chain over it
      ↓
  verify_sealed() reports ok=True, integrity_ok=True (correctly — nothing was
  altered *after* this sealing), so a downstream consumer that treats "sealed"
  as "came from FORGE's audit pipeline" is misled
  ```
- **Precision note (per skill Part 7):** the seal mechanism itself is **not
  broken** — `verify_sealed` correctly proves the fabricated content wasn't
  altered after sealing. The defect is that **a wrong (fabricated) verdict can
  be sealed** through a sanctioned, low-friction entry point, not that sealing
  can be tampered with after the fact.
- **Threat-model precondition:** attacker needs only the ability to call
  `seal_results` (function or MCP tool) with a JSON file they control — no
  filesystem tampering of `forge`'s own files, no reimplementation of the hash
  chain, no elevated privilege. This is materially cheaper than the
  "full-access attacker" scenario `DECISIONS.md` already discloses, and the
  disclosure doesn't mention this specific, sanctioned code path.
- **Recommendation (record only, out of scope of this audit to fix):** either
  (a) have `seal_results` require/verify a linkage token that only
  `Runtime.audit()`/`audit_ref()`/`compare_refs()` can produce (e.g. an HMAC
  over the manifest computed at generation time with a key never exposed to
  callers), or (b) rename/document the tool explicitly as "attest whatever
  manifest you hand me" so downstream consumers never treat "sealed" alone as
  a provenance guarantee, and update `DECISIONS.md` to name this exact path.

### F2 — Unresolved ref strings reach `git merge-base`/`git diff` as raw argv (argument injection)
**Severity:** LOW (as demonstrated — capped by induction, see below)  **Epistemic level:** CONFIRMED BY INDUCTION  **Bucket:** vulnerability (defense-in-depth gap), NOT RCE

- **Surprise / expectation violated:** `resolve_ref()` (`git_refs.py:19-27`) is
  careful — it wraps the caller's `ref` in `f"{ref}^{{commit}}"` before passing
  it to `git rev-parse --verify`, which neutralizes leading-dash option
  injection (confirmed below). `changed_files()` (`git_refs.py:38-44`) is
  **not** equally careful: it passes `base_ref`/`head_ref` straight into `git
  merge-base` and (for `head_ref`) straight into `git diff`, with no `--`
  separator to stop option parsing. These are reachable directly from the
  exposed MCP tool `compare_refs(path, base_ref, head_ref, ...)`
  (`mcp_server.py:77-88` → `runtime.py:299-325` → `git_refs.py:318`).
- **Abduction:** a `head_ref`/`base_ref` value starting with `-` (e.g. an
  attacker-named branch on a repo being audited, created via `git update-ref`
  which bypasses the porcelain `git branch` name restrictions) will be parsed
  by git as an option rather than a revision, potentially achieving arbitrary
  file write (`git diff --output=<path>`) or worse.
- **Deduction:** predict `changed_files(repo, "master", "--output=/tmp/pwned_forge_argtest.txt")` writes `/tmp/pwned_forge_argtest.txt`.
- **Induction — executed:**
  ```bash
  git update-ref "refs/heads/--output=/tmp/pwned_forge_argtest.txt" <head-sha>   # succeeds — plumbing bypasses branch-name validation
  ```
  ```python
  from forge.git_refs import changed_files
  changed_files(repo, "master", "--output=/tmp/pwned_forge_argtest.txt")
  ```
  **Observed output:**
  ```
  EXC: ValueError git refs have no merge-base: master, --output=/tmp/pwned_forge_argtest.txt
  (error: unknown option `output=/tmp/pwned_forge_argtest.txt'
  usage: git merge-base [-a | --all] <commit> <commit>...  ...)
  no file created
  ```
  Prediction **falsified for the `--output` vector specifically**: `merge_base()`
  is called before the vulnerable `diff` call and fails cleanly, because `git
  merge-base` has no dangerous options (no arbitrary write/exec flags) — it
  only recognizes `--all/--octopus/--independent/--is-ancestor/--fork-point`,
  none of which write files or execute programs. So the injection is real
  (CODE FACT: the raw string does reach git's option parser) but its
  demonstrated blast radius through this call path is a clean `ValueError`,
  not file write or RCE.
- **`resolve_ref` — separately tested and FALSIFIED as an injection vector:**
  ```python
  resolve_ref(repo, "--output=/tmp/pwned2.txt")   # -> ValueError: git ref not found ... fatal: Needed a single revision
  resolve_ref(repo, "-o/tmp/pwned3")               # -> same clean failure
  resolve_ref(repo, "--upload-pack=touch /tmp/pwned4")  # -> same clean failure
  ```
  No file created in any case. The `^{commit}` suffix concatenation defangs
  this path.
- **Residual risk (not fully explored):** `merge_base()` is called with
  `base_ref` and `head_ref` in argv positions where a *non-erroring* flag
  (e.g. `--all`) could alter output semantics without erroring, or could cause
  the wrong pair of commits to be diffed if git's positional-arg resolution
  gets confused by a dash-prefixed ref — this could silently produce a wrong
  (not just failing) `changed_files` result. Not executed; capped at
  **PLAUSIBLE HYPOTHESIS** for that sub-case.
- **Threat-model precondition:** requires ref names on the *audited* repository
  to be attacker-influenced (e.g. forge run automatically against PR branch
  names in CI, where an external contributor names the branch) — plausible in
  a CI/MCP-orchestrated deployment, not applicable if the operator always types
  the ref by hand.
- **Recommendation (record only):** insert `"--"` before revision arguments in
  `merge_base()` and the `diff` call in `changed_files()`, matching the
  defense already implicit in `resolve_ref`'s suffix trick.

### F3 — TOCTOU window in `run_loop`'s worktree creation
**Severity:** MEDIUM  **Epistemic level:** PLAUSIBLE HYPOTHESIS (not executed — race not induced)  **Bucket:** vulnerability (local, narrow)

- **Surprise / expectation violated:** `loop.py:109-112`:
  ```python
  worktree = Path(tempfile.mkdtemp(prefix="forge-loop-"))
  try:
      shutil.rmtree(worktree)
      _git(repository, "worktree", "add", "--detach", str(worktree), commit)
  ```
  `mkdtemp` atomically creates a directory that is guaranteed not to already
  exist; the code immediately deletes it and then asks `git worktree add` to
  recreate a directory at that exact path. This is the textbook
  create-delete-recreate anti-pattern (equivalent to the long-deprecated
  `tempfile.mktemp()` unsafe behavior, done manually) — between the `rmtree`
  and the `git worktree add`, the uniqueness guarantee no longer holds.
- **Abduction:** on a multi-user host, another local process watching `/tmp`
  (e.g. via inotify) could race to create a symlink at the freed path before
  `git worktree add` writes there, potentially redirecting the worktree
  checkout to attacker-chosen location.
- **Deduction:** a tight-loop local race harness (one process spinning
  `mkdtemp`+`rmtree`, another racing to `ln -s` at the freed path) would show a
  nonzero win rate for the attacker within some window.
- **Induction:** **not run** — reliably demonstrating a timing race was judged
  disproportionate effort for this pass and was not executed; per this skill's
  rule, the finding is capped at PLAUSIBLE HYPOTHESIS, not claimed as confirmed.
- **Threat-model precondition:** requires a co-resident, unprivileged local
  attacker on the same host as the FORGE operator — not applicable to a
  single-user workstation, relevant to a shared/multi-tenant CI runner.
- **Recommendation (record only):** use `git worktree add` directly against a
  path from `mkdtemp()` without the intervening `rmtree` (git will refuse if
  the directory isn't empty, so either use a subdirectory that doesn't yet
  exist under the mkdtemp'd dir, or `os.rmdir` immediately before-and-atomic
  isn't achievable in POSIX — the standard fix is to let `git worktree add`
  target a *new* path component inside the still-existing mkdtemp directory).

### F4 — `loop_audit` MCP tool grants arbitrary command execution by design, undocumented as such
**Severity:** INFO (threat-model precondition, not a code defect)  **Epistemic level:** CODE FACT  **Bucket:** threat-model assumption

- `loop_mcp.py:24-38` exposes `loop_audit(path, ref, ..., test_command:
  list[str] | None, ...)`. `loop.py:33-45` (`_test`) runs
  `subprocess.run(list(command), cwd=worktree, ...)` with whatever argv the
  caller supplies — this is by-design test-suite execution (there is no way to
  verify a patch fixes a bug without running the repo's tests), not a bug. No
  shell is invoked (`shell=True` is never set anywhere in `git_refs.py` or
  `loop.py` — confirmed by grep), so this is exactly "run this program with
  these arguments," nothing more, nothing less.
- **Why it's called out anyway:** neither `loop_audit`'s docstring nor
  `mcp_server.py`'s module docstring states that any MCP caller who can invoke
  this tool is granted equivalent-to-shell code execution on the host running
  the MCP server (test_command is unconstrained — any program on `$PATH` with
  any arguments). In a deployment where the MCP server is reachable by a
  lower-trust caller (e.g., an LLM agent that itself decided to call this tool
  based on untrusted instructions embedded in analyzed content), this is the
  most powerful capability in the entire tool surface and is not flagged as
  such next to the others.
- **Recommendation (record only):** document this precondition explicitly next
  to the tool definition ("the caller must be as trusted as a local shell
  user"), and/or scope MCP server deployment so `loop_mcp` is never exposed to
  a lower-trust caller than `mcp_server.py`'s other tools.

### F5 — `orchestrator_model`/`agent_models` parameters are recorded but not wired to any LLM call
**Severity:** INFO (hygiene/precision)  **Epistemic level:** CODE FACT  **Bucket:** hygiene

- `mcp_server.py:29-32` (`audit_repository`) and `runtime.py:109-122` accept
  `orchestrator_model`/`agent_models`, store them on `ModelRouting`, and record
  `model_routing.to_dict()` into the audit trace (`runtime.py:186`) — but
  `grep -rn "self.model_routing\." forge/runtime.py` shows no other read site,
  and `grep -n "openai|anthropic|requests\.|httpx|completion" forge/agents/*.py`
  returns nothing: no LLM API integration exists anywhere in `forge/agents/*`
  yet (all scanners there are deterministic heuristic/AST code).
- This is good news for the LLM-out-of-loop invariant (there is currently
  nothing to be *in* the loop), but the exposed parameters could mislead an
  operator into believing a specific model is actively narrating or deciding —
  worth a docstring note that these are currently inert.

## Discarded (non-exploitable) vectors
| Vector | Result | Why it failed |
|---|---|---|
| `resolve_ref()` argument injection (`--output=`, `-o`, `--upload-pack=`) | FALSIFIED | `f"{ref}^{{commit}}"` suffix concatenation breaks any dash-prefixed option syntax before it reaches `rev-parse --verify`; git errors cleanly with "Needed a single revision" |
| `archive_ref()` RCE via crafted ref (e.g. `--remote=ext::sh -c ...`) | FALSIFIED (by code-path analysis + confirmed call site) | `archive_ref()` is only ever called with an already-resolved commit SHA (`runtime.py:282,285`: `commit = resolve_ref(...)` then `archive_ref(repository, commit, ...)`), never with the raw attacker-influenced ref string |
| `archive_ref()` path traversal via crafted tar member names | FALSIFIED (code fact) | `git_refs.py:56-68` explicitly checks `member_path.is_absolute()` and `".." in member_path.parts` before extracting, and uses `filter="data"` on Python ≥3.12 |
| Shell metacharacter injection (`;`, `` ` ``, `$()`) anywhere in `git_refs.py`/`loop.py` subprocess calls | FALSIFIED (code fact) | Every `subprocess.run` call in both files passes a list argv with `shell` unset (defaults to `False`); grep confirms zero `shell=True` occurrences in either file |
| `_apply_patch()` patch-content injection into `git apply` | FALSIFIED (code fact) | Patch text is passed via `input=patch` to stdin, not interpolated into argv or a shell string |
| Float/non-determinism in `canonical_json` (dict order, `1` vs `1.0` vs `"1"` vs `True`) | FALSIFIED — canonicalizer is correct | Executed: order-independent hash, `TypeError` raised on any `float`, bool/int/str produce distinct typed-tagged output |
| LLM influencing the sealed verdict (llm-out-of-the-loop invariant) | FALSIFIED — invariant holds | grep across `verification.py`, `induction.py`, `hypotheses.py`, `disposition.py`, `contradictions.py`, `sealing.py` for any model/LLM reference returns nothing; no LLM call site exists in `forge/agents/*` at all currently |

## Recommendations (out of scope of this change — record only)
1. Add provenance verification to `seal_results` (F1) — highest priority; this
   is the sharpest finding because it's reachable via a single sanctioned MCP
   call, cheaper than the "full-access attacker" scenario already disclosed in
   `DECISIONS.md`.
2. Insert `--` before revision arguments in `merge_base`/`diff` calls inside
   `changed_files()` (F2).
3. Remove the create-delete-recreate temp-directory pattern in `loop.py:109-111` (F3).
4. Document `test_command`'s full-code-execution capability explicitly on
   `loop_audit` (F4).
5. Either wire `orchestrator_model`/`agent_models` to a real integration or
   note in the docstring that they are currently inert (F5).

## Remediation status — 2026-07-15

The confirmed findings and the identified defense-in-depth gap were addressed
in the current working tree:

| ID | Status | Remediation |
|---|---|---|
| F1 | Fixed | `VerificationManifest` now carries a process-local HMAC source attestation. `seal_results` rejects manifests without a valid FORGE-generated attestation or with post-audit edits. The sealed manifest preserves the attestation. |
| F2 | Fixed | `merge-base` and `diff` now receive `--` before caller-controlled revision arguments, preventing option parsing at those boundaries. |
| F3 | Fixed | The loop creates a unique temporary parent and asks Git to create a new child worktree path; it no longer deletes and recreates the path returned by `mkdtemp`. Cleanup removes the Git worktree and its parent. |
| F4 | Documented | `loop_audit` now states that `test_command` executes programs with the MCP process's privileges. The tool must only be exposed to callers trusted with equivalent local-shell access. |
| F5 | Documented | `ModelRouting` explicitly states that model names are inert metadata until a model-backed adapter is installed; no model call is implied by trace metadata. |

The attestation is intentionally process-local. A manifest copied to a
different FORGE process cannot be re-sealed there; it must be produced by that
process's own audit runtime. This keeps the sanctioned seal entry point from
becoming a general-purpose attestation oracle while preserving the normal
`audit` → `verification-manifest` → `sealed manifest` path.

Regression coverage includes fabricated-manifest rejection, post-audit
tampering rejection, Git ref argument boundaries, temporary worktree cleanup,
and loop authority boundaries. Full suite result after remediation: **127
tests passed**.
