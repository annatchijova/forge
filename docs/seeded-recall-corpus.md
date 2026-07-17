# Seeded recall corpus

FORGE measures detector recall on intentionally seeded defects, not by
re-running only on carefully maintained repositories.  The measured unit is
the exact finding identity `(family, path, line)` emitted by the relevant
agent.  Severity is a secondary assertion; it never substitutes for locating
the seeded defect.

Run it from the repository root:

```bash
python3 -m forge.recall --corpus tests/corpus
```

The corpus manifest contains three distinct kinds of case:

| Kind | Contract | Included in recall denominator? |
|---|---|---|
| `positive` | Its exact identity must be emitted. | Yes |
| `benign_twin` | The specified family must emit nothing for that fixture. A hit is a precision regression. | No |
| `out_of_scope` | A real defect class FORGE does not currently model; it is recorded with its observed result. | Never |

`detection_mode: induction` and `both` enable the existing isolated induction
harness. Static cases remain static: they do not acquire a confirmation claim
merely because a harness exists for another family.

The current gate is `recall >= 0.90` for every represented modeled family and
zero hits on benign twins. The result is deterministic for a given commit and
manifest, so the JSON emitted by the command can be stored alongside any
benchmark run and compared across commits.

## Scope is not a cleanliness certificate

The out-of-scope fixtures deliberately include business-logic exception
swallowing, `None`/index errors, state-machine errors, races, IDOR,
misused API returns, type errors, and resource leaks. They are not false
negatives in this measurement because FORGE does not claim to model those
families today.

Consequently, `COMPLETE_NO_FINDINGS` always means no surviving finding within
the declared source and detector scope. It never means “this repository has no
bugs.” A future detector family may promote an out-of-scope fixture into a
positive only alongside an explicit scope and contract change.
