"""FastMCP transport for the existing FORGE pipeline.

The tool functions are ordinary Python functions as well, which keeps fixture
tests independent of a running MCP client. They never write to an audited
repository; audit output is placed in a temporary directory outside it.
"""
from __future__ import annotations
import json
import tempfile
from dataclasses import asdict
from pathlib import Path
from typing import Any

from mcp.server.fastmcp import FastMCP

from forge.runtime import Runtime
from forge.sealing import verify_sealed
from forge.agents.patch_reviewer import review as review_patch_impl

mcp = FastMCP("forge")
runtime = Runtime()

def _error(code: str, message: str, **extra: Any) -> dict[str, Any]:
    return {"ok": False, "error": {"code": code, "message": message, **extra}}

@mcp.tool()
def audit_repository(path: str, max_connected: int = 100, output_dir: str | None = None) -> dict[str, Any]:
    root = Path(path).expanduser()
    if not root.exists(): return _error("not_found", f"repository path does not exist: {path}")
    if not root.is_dir(): return _error("not_directory", f"repository path is not a directory: {path}")
    try:
        if output_dir is None:
            output = Path(tempfile.mkdtemp(prefix="forge-mcp-"))
        else:
            output_root = Path(output_dir).expanduser()
            output_root.mkdir(parents=True, exist_ok=True)
            output = Path(tempfile.mkdtemp(prefix="run-", dir=output_root))
        result = runtime.audit(root, output, max_connected).to_dict()
        result["report_html_path"] = result["artifacts"]["report"]; result["ok"] = True
        return result
    except (OSError, ValueError, RuntimeError) as exc:
        return _error("audit_failed", str(exc))

@mcp.tool()
def get_coverage(run_output_dir: str) -> dict[str, Any]:
    path = Path(run_output_dir) / "coverage-report.json"
    try:
        if not path.is_file(): return _error("missing_artifact", f"coverage artifact not found: {path}")
        return {"ok": True, **json.loads(path.read_text(encoding="utf-8"))}
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        return _error("malformed_artifact", f"could not read coverage artifact: {exc}")

@mcp.tool()
def get_findings(run_output_dir: str, agent: str | None = None) -> list | dict:
    path = Path(run_output_dir) / "verification-manifest.sealed.json"
    allowed = {"bug_investigator", "security_auditor", "integrity_inspector"}
    if agent is not None and agent not in allowed: return _error("invalid_agent", f"unsupported agent filter: {agent}")
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        if not isinstance(data.get("chain"), list): return _error("malformed_artifact", "sealed manifest has no chain list")
        return runtime.get_findings(run_output_dir, agent)
    except FileNotFoundError: return _error("missing_artifact", f"sealed manifest not found: {path}")
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc: return _error("malformed_artifact", f"could not read sealed manifest: {exc}")

@mcp.tool()
def verify_seal(sealed_path: str) -> dict[str, Any]:
    try:
        return runtime.verify_findings(sealed_path)
    except FileNotFoundError: return _error("not_found", f"sealed manifest not found: {sealed_path}")
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc: return _error("malformed_artifact", f"could not verify sealed manifest: {exc}")

@mcp.tool()
def triage_repository(path: str) -> dict[str, Any]:
    root = Path(path).expanduser()
    if not root.is_dir(): return _error("invalid_repository", f"repository path is not a directory: {path}")
    try:
        manifest = runtime.triage_repository(root)
        return {"ok": True, "manifest": manifest.to_dict()}
    except (OSError, ValueError) as exc: return _error("triage_failed", str(exc))

@mcp.tool()
def infer_module_domains(path: str) -> dict[str, Any]:
    root = Path(path).expanduser()
    if not root.is_dir(): return _error("invalid_repository", f"repository path is not a directory: {path}")
    try:
        hypotheses = runtime.infer_module_domains(root)
        return {"ok": True, "hypotheses": [{"module_path": h.module_path, "domains": h.domains, "confidence": {"numerator": h.confidence.numerator, "denominator": h.confidence.denominator}, "evidence": [item.__dict__ for item in h.evidence], "alternatives": h.alternatives} for h in hypotheses]}
    except (OSError, ValueError) as exc: return _error("domain_inference_failed", str(exc))

@mcp.tool()
def list_available_skills() -> dict[str, Any]:
    try: return {"ok": True, "skills": list(runtime.list_available_skills())}
    except (OSError, ValueError, json.JSONDecodeError) as exc: return _error("skill_loading_failed", str(exc))

@mcp.tool()
def run_skill(path: str, skill: str | None = None) -> dict[str, Any]:
    root = Path(path).expanduser()
    if not root.is_dir(): return _error("invalid_repository", f"repository path is not a directory: {path}")
    try: return {"ok": True, **runtime.run_skill(root, skill).to_dict()}
    except (OSError, ValueError) as exc: return _error("skill_run_failed", str(exc))

@mcp.tool()
def repository_summary(path: str) -> dict[str, Any]:
    root = Path(path).expanduser()
    if not root.is_dir(): return _error("invalid_repository", f"repository path is not a directory: {path}")
    try: return {"ok": True, **runtime.repository_summary(root)}
    except (OSError, ValueError) as exc: return _error("summary_failed", str(exc))

@mcp.tool()
def generate_report(sealed_path: str, mode: str = "standard", output: str | None = None) -> dict[str, Any]:
    try: return {"ok": True, "path": str(runtime.generate_report(sealed_path, mode, output))}
    except (OSError, ValueError, json.JSONDecodeError) as exc: return _error("report_failed", str(exc))

@mcp.tool()
def seal_results(verification_path: str, output: str | None = None) -> dict[str, Any]:
    try: return {"ok": True, "path": str(runtime.seal_results(verification_path, output))}
    except (OSError, ValueError, KeyError, json.JSONDecodeError) as exc: return _error("seal_failed", str(exc))

@mcp.tool()
def review_patch(unified_diff: str, intent: str, before: str = "", after: str = "") -> dict[str, Any]:
    try:
        result = asdict(review_patch_impl(unified_diff, intent, before, after))
        result["ratio"] = {"numerator": result["ratio"].numerator, "denominator": result["ratio"].denominator}
        return result
    except (SyntaxError, ValueError) as exc: return _error("invalid_patch", str(exc))

if __name__ == "__main__":
    mcp.run()
