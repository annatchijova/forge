# Precision corpus gate

`tests/corpus` measures detector outputs as exact finding identities:
`(family, path relative to corpus case, line)`. A family match on the wrong
line is both a false positive and a false negative. `by_family` remains only
as an aggregate, family-presence view for trend reading.

The initial committed floor is **precision >= 0.95** and **recall >= 0.90** on
the global exact-finding score. Run it from the repository root:

```bash
python3 -m forge.precision --corpus tests/corpus --min-precision 0.95 --min-recall 0.90
```

Changing either floor requires an explicit review of the corpus contract; it
must not be weakened as a side effect of detector changes.
