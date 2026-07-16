# Engineering philosophy

FORGE is built around one principle:

> **Engineering should optimize for correctness before confidence.**

Every repository audit follows the Peircean reasoning loop:

```
Observation
      │
      ▼
Abduction
(generate hypotheses)
      │
      ▼
Deduction
(design falsification tests)
      │
      ▼
Induction
(earn only bounded conclusions)
```

A plausible pattern is never promoted into a defect merely because it looks
convincing. Evidence remains separate from inference throughout the entire
pipeline: every finding carries an explicit epistemic level from the
red-team-auditing vocabulary — **CODE FACT** for a directly observed AST
match, **PLAUSIBLE HYPOTHESIS** for an unexecuted abduction, **CONFIRMED BY
INDUCTION** for a reproduced prediction, **FALSIFIED** for a refuted one —
and that level is never invented or conflated with the OBSERVED / INFERRED /
OPINION category field it sits next to.

## Design principles

* Deterministic decision path
* No hidden reasoning promotion
* Evidence precedes conclusions
* Hypotheses remain auditable
* `ABSTAIN` is a valid outcome
* Honest degradation over false certainty
* Canonical, typed serialization
* Bit-for-bit reproducibility of the seal
* Minimal, read-only repository interaction
* Security-first engineering
