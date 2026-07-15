"""Specialized deterministic workers used by the FORGE orchestrator.

These are local workers today. An eventual MCP adapter can expose the same
contracts without changing the evidence model.
"""

AGENT_ROLES = (
    "triage",
    "abduction",
    "adversarial_verification",
    "numeric_ml_review",
    "sealing",
    "reporting",
)
