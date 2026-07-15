# FORGE agent contracts

These role cards define the first local agent set. They are intentionally
framework-neutral so a later MCP transport can expose the same inputs and
outputs.

| Agent | Responsibility | Output |
|---|---|---|
| `triage` | classify repository modules and scope | `TriageManifest` |
| `abduction` | propose concrete, falsifiable hypotheses | `HypothesesManifest` |
| `adversarial_verification` | test structural benign explanations | `VerificationManifest` |
| `numeric_ml_review` | inspect float, exact-arithmetic, model, data and boundary claims | bounded annotations; never invented severity |
| `sealing` | canonicalize and chain the verification evidence | sealed manifest |
| `reporting` | render observations, inferences, discarded candidates and scope limits | self-contained HTML |

The first five deterministic pipeline stages are implemented by
`forge.orchestrator`; `numeric_ml_review` is currently a role contract awaiting
its dedicated detector. The orchestrator stops at a configurable scope guard,
and agents may not mutate the audited repository.

Every agent must preserve the distinction between observation, abductive
hypothesis, deductive falsifier, and inductive conclusion. A transport layer or
LLM may propose text later, but it cannot promote a hypothesis into a finding or
alter evidence already sealed.
