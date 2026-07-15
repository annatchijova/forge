# FORGE

Forensic Repository Governance Engine.

## Development

Run all commands (`pytest`, `python3 -m forge`, and Git operations) from the
repository root: `/home/labestiadevigia/forge`. Running from a parent directory
can pick up unrelated files and produce misleading test or audit results. This
happened during the Kimi audit verification step.

## Shared skills

The versioned `skills-gpt/` directory contains the project's shared engineering
and audit policies. Future specialized agents and the multi-agent orchestrator
will use these documents as common operating context rather than inventing
separate standards.

The collection is designed for repository analysis across conventional code,
floating-point decision logic, and ML systems. It keeps observation, inference,
and judgment separate; uses Peircean abduction to propose explanations,
deduction to derive testable consequences, and induction only for claims backed
by repeated evidence. Deterministic sealing and exact arithmetic are preferred
where results become evidence; floats and probabilistic ML outputs remain
explicitly bounded, labeled, and tested at their boundary conditions.

The orchestrator and MCP are planned integrations, not implemented components
of the current module set.
