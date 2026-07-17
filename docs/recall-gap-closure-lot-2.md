# Recall-gap closure — lot 2

**Date:** 2026-07-18  
**Status:** SQL cluster closed; command cluster pending

Lot 2 reuses the shared, source-ordered unsafe-origin snapshots introduced by
the path-flow consolidation. The graph is computed once per function and is
parameterized by family policy; sinks decide which argument position is
dangerous.

## SQL injection

The SQL detector now inspects only argument zero of `execute`, `executemany`,
and `executescript`: the SQL expression, never the parameter tuple/dict. This
separation is essential because bound values are the safe channel.

It detects unsafe parameter origins through concatenation, percent formatting,
`.format`, f-strings, and local aliases when they reach that expression. It
does not infer an injection merely because a parameter occurs in a bound-value
tuple or as a key selecting a constant query from a mapping.

| Measure | Before SQL cluster | After SQL cluster |
|---|---:|---:|
| SQL variants | 2/4 | 4/4 |
| Overall variants | 23/36 | 25/36 |
| Benign-twin false positives | 0 | 0 |
| Precision corpus | 1.0 | 1.0 |

The two closed gaps are `str.format` and a one-hop query alias. The already
detected concat and percent-interpolation forms are retained as mechanism-
checked positives. Each requires `sql`, `execute`, and `interpolation` in the
finding description, so an incidental family match cannot inflate recall.

The SQL implementation is committed atomically with this record. The command
cluster will update it separately; `shell=<variable>` is explicitly outside
that change because it requires constant propagation policy.
