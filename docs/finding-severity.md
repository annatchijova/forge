# Finding severity contract

FORGE records four independent axes: `family`, `epistemic_level`,
`controllability`, and `exploitability`. Severity is a deterministic result of
those values in `forge/severity.py`; it is not evidence and does not alter the
epistemic level.

`ATTACKER_CONTROLLED` is required for HIGH or CRITICAL. In addition,
exploitability must be `PLAUSIBLE` or `CONFIRMED`. `INTERNAL_ONLY`,
`UNDETERMINED`, and an `OBSERVED_BOUNDARY` cap the finding at MEDIUM. This
keeps observed APIs and static boundary signals visible without presenting
them as confirmed exploits.
