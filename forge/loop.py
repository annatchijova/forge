"""Patch-proposal loop with FORGE as the sole resolution authority."""
from __future__ import annotations

import json
import shutil
import subprocess
import tempfile
import time
from pathlib import Path
from typing import Any, Sequence

from forge.comparison import compare_runs
from forge.git_refs import resolve_ref
from forge.runtime import Runtime

STATES = (
    "AUDITED", "PATCH_PROPOSED", "PATCH_APPLIED_TEMPORARILY", "TESTED",
    "REAUDITED", "CONVERGED", "STILL_PRESENT",
    "ABSTAIN_NO_PROPOSAL", "ABSTAIN_PROVIDER_UNAVAILABLE", "FAILED",
)


def _git(repo: Path, *args: str, check: bool = True) -> subprocess.CompletedProcess:
    return subprocess.run(["git", "-C", str(repo), *args], text=True,
                          stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                          check=check)


def _transition(trace: list[dict[str, Any]], state: str, **payload: Any) -> None:
    trace.append({"sequence": len(trace), "state": state, "timestamp": time.time(), **payload})


def _test(worktree: Path, command: Sequence[str] | None, timeout: int) -> dict[str, Any]:
    if not command:
        return {"status": "NOT_REQUESTED", "passed": None, "command": []}
    try:
        result = subprocess.run(list(command), cwd=worktree, text=True,
                                stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                                timeout=timeout, check=False)
        return {"status": "PASSED" if result.returncode == 0 else "FAILED",
                "passed": result.returncode == 0, "returncode": result.returncode,
                "command": list(command), "output": result.stdout[-12000:]}
    except subprocess.TimeoutExpired as exc:
        return {"status": "TIMEOUT", "passed": False, "command": list(command),
                "output": str(exc)}


def _apply_patch(worktree: Path, patch: str) -> dict[str, Any]:
    if not patch.strip():
        return {"applied": False, "status": "EMPTY_PATCH", "output": "patch is empty"}
    checked = subprocess.run(["git", "-C", str(worktree), "apply", "--check", "-"],
                             input=patch, text=True, stdout=subprocess.PIPE,
                             stderr=subprocess.STDOUT, check=False)
    if checked.returncode != 0:
        return {"applied": False, "status": "REJECTED", "output": checked.stdout[-12000:]}
    applied = subprocess.run(["git", "-C", str(worktree), "apply", "--whitespace=nowarn", "-"],
                             input=patch, text=True, stdout=subprocess.PIPE,
                             stderr=subprocess.STDOUT, check=False)
    return {"applied": applied.returncode == 0,
            "status": "APPLIED" if applied.returncode == 0 else "FAILED",
            "output": applied.stdout[-12000:]}


def run_loop(repo: str | Path, ref: str, output_dir: str | Path,
             proposal_provider: str = "deterministic", patches: Sequence[str] | None = None,
             max_iterations: int = 3, max_connected: int = 100,
             test_command: Sequence[str] | None = None, test_timeout: int = 120) -> dict[str, Any]:
    """Run a bounded proposal/test/re-audit loop without modifying the source repo.

    ``deterministic`` and ``human`` are credit-free. A supplied patch is always
    treated as a proposal; only the subsequent FORGE re-audit can resolve a
    finding. ``llm`` is intentionally a provider boundary and abstains until a
    model adapter is explicitly installed.
    """
    if max_iterations < 1:
        raise ValueError("max_iterations must be positive")
    if proposal_provider not in {"deterministic", "human", "llm"}:
        raise ValueError("proposal_provider must be deterministic, human, or llm")
    repository = Path(repo).resolve()
    if not repository.is_dir():
        raise ValueError(f"repository path is not a directory: {repo}")
    commit = resolve_ref(repository, ref)
    destination = Path(output_dir).resolve()
    destination.mkdir(parents=True, exist_ok=True)
    trace: list[dict[str, Any]] = []
    patches = tuple(patches or ())
    runtime = Runtime(max_connected=max_connected)
    initial = runtime.audit_ref(repository, ref, destination / "initial")
    _transition(trace, "AUDITED", ref=ref, commit=commit, findings=initial.findings,
                sealed=initial.artifacts.get("sealed"))

    result: dict[str, Any] = {
        "loop_schema_version": "1.0",
        "repository": str(repository), "ref": ref, "commit": commit,
        "proposal_provider": proposal_provider, "max_iterations": max_iterations,
        "status": "CONVERGED" if initial.findings == 0 else None,
        "iterations": [], "initial_run": initial.artifacts,
        "authority": "FORGE",
    }
    if initial.findings == 0:
        _transition(trace, "CONVERGED", reason="initial audit has no findings")
        result["trace"] = trace
        result["trace_artifact"] = str(destination / "loop-trace.json")
        result["report_artifact"] = str(destination / "loop-report.json")
        (destination / "loop-trace.json").write_text(json.dumps(trace, indent=2) + "\n")
        (destination / "loop-report.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
        return result

    worktree_container = Path(tempfile.mkdtemp(prefix="forge-loop-"))
    worktree = worktree_container / "worktree"
    try:
        _git(repository, "worktree", "add", "--detach", str(worktree), commit)
        for number in range(1, max_iterations + 1):
            if proposal_provider == "llm":
                _transition(trace, "ABSTAIN_PROVIDER_UNAVAILABLE", iteration=number,
                            reason="no LLM proposal adapter is configured")
                result["status"] = "ABSTAIN_PROVIDER_UNAVAILABLE"
                break
            patch = patches[number - 1] if number <= len(patches) else ""
            if not patch:
                _transition(trace, "ABSTAIN_NO_PROPOSAL", iteration=number,
                            reason="no deterministic or human patch proposal supplied")
                result["status"] = "ABSTAIN_NO_PROPOSAL"
                break
            _transition(trace, "PATCH_PROPOSED", iteration=number,
                        provider=proposal_provider, patch_sha256=__import__("hashlib").sha256(patch.encode()).hexdigest())
            application = _apply_patch(worktree, patch)
            if not application["applied"]:
                _transition(trace, "FAILED", iteration=number, phase="patch", **application)
                result["status"] = "FAILED"
                result["iterations"].append({"iteration": number, "patch": application})
                break
            _transition(trace, "PATCH_APPLIED_TEMPORARILY", iteration=number)
            tests = _test(worktree, test_command, test_timeout)
            _transition(trace, "TESTED", iteration=number, **tests)
            if tests["passed"] is False:
                result["iterations"].append({"iteration": number, "patch": application, "tests": tests})
                _transition(trace, "STILL_PRESENT", iteration=number, reason="tests failed")
                result["status"] = "STILL_PRESENT"
                break
            audit = runtime.audit(worktree, destination / f"iteration-{number}")
            delta = compare_runs(destination / "initial", destination / f"iteration-{number}")
            _transition(trace, "REAUDITED", iteration=number, findings=audit.findings,
                        resolved=len(delta["resolved"]), new=len(delta["new"]),
                        unchanged=len(delta["unchanged"]))
            iteration = {"iteration": number, "patch": application, "tests": tests,
                         "audit": audit.artifacts, "delta": delta}
            result["iterations"].append(iteration)
            if not delta["new"] and not delta["unchanged"]:
                _transition(trace, "CONVERGED", iteration=number,
                            reason="all initial findings resolved and no new findings")
                result["status"] = "CONVERGED"
                break
            _transition(trace, "STILL_PRESENT", iteration=number,
                        reason="FORGE still reports unresolved or new findings")
            result["status"] = "STILL_PRESENT"
        else:
            result["status"] = "STILL_PRESENT"
    finally:
        _git(repository, "worktree", "remove", "--force", str(worktree), check=False)
        shutil.rmtree(worktree_container, ignore_errors=True)
    result["trace"] = trace
    (destination / "loop-trace.json").write_text(json.dumps(trace, indent=2) + "\n")
    result["trace_artifact"] = str(destination / "loop-trace.json")
    result["report_artifact"] = str(destination / "loop-report.json")
    (destination / "loop-report.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    return result


__all__ = ("STATES", "run_loop")
