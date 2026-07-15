"""Specialized deterministic workers used by the FORGE orchestrator.

These are local workers today. An eventual MCP adapter can expose the same
contracts without changing the evidence model.
"""

AGENT_ROLES = (
    "archaeologist", "bug_investigator", "security_auditor",
    "integrity_inspector", "patch_reviewer", "report_composer",
)
