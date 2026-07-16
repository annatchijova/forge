# Hackathon build notes

FORGE is submitted in the **Developer Tools** track. The project was extended
with Codex using GPT-5.6, with product decisions centered on reproducibility,
evidence provenance, bounded execution, and judge-friendly outputs:

* Codex accelerated repository archaeology, test-driven hardening, report UX,
  and the benchmark/evidence-package workflow.
* GPT-5.6 was used as the implementation and review partner; deterministic
  detectors remain in the runtime, so model routing is recorded honestly and
  is never presented as evidence of a model call.
* The project separates observed findings, discarded hypotheses, optional
  recommendations, and applied code changes.

Before submission, provide the actual Codex `/feedback` Session ID for the
build thread in the submission form. FORGE does not fabricate or hard-code
that external identifier.

## Codex build-session evidence

Known Codex sessions used during the build:

* `019f65d2-230f-71d2-ab70-e8195fb8fae0`
* `019f6693-c5fa-75e1-bc61-3c7af5ab6cc0`
* `019f6706-b195-7981-b21a-a01f98a6f785`
* _Three additional session IDs pending retrieval from screenshots._
