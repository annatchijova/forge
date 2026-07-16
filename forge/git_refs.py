"""Read-only Git ref resolution and tree extraction helpers."""
from __future__ import annotations

import subprocess
import tarfile
from pathlib import Path


def _git(repo: str | Path, *args: str, stdout=subprocess.PIPE) -> subprocess.CompletedProcess:
    return subprocess.run(
        ["git", "-C", str(Path(repo).resolve()), *args],
        stdout=stdout,
        stderr=subprocess.PIPE,
        check=False,
        text=False,
    )


def resolve_ref(repo: str | Path, ref: str) -> str:
    """Resolve a Git ref to an object id without changing repository state."""
    if not ref or not ref.strip():
        raise ValueError("git ref must not be empty")
    # Trailing "--" marks end-of-options so a ref value shaped like a git
    # flag (e.g. "--upload-pack=...") is never parsed as one - matching
    # merge_base()/changed_files() below, which already guard with "--".
    # ("git rev-parse --verify" only accepts it after the revision, not
    # before, unlike merge-base/diff.)
    result = _git(repo, "rev-parse", "--verify", f"{ref}^{{commit}}", "--")
    if result.returncode != 0:
        detail = result.stderr.decode("utf-8", "replace").strip()
        raise ValueError(f"git ref not found: {ref}" + (f" ({detail})" if detail else ""))
    return result.stdout.decode("ascii", "strict").strip()


def merge_base(repo: str | Path, base_ref: str, head_ref: str) -> str:
    result = _git(repo, "merge-base", "--", base_ref, head_ref)
    if result.returncode != 0:
        detail = result.stderr.decode("utf-8", "replace").strip()
        raise ValueError(f"git refs have no merge-base: {base_ref}, {head_ref}" + (f" ({detail})" if detail else ""))
    return result.stdout.decode("ascii", "strict").strip()


def changed_files(repo: str | Path, base_ref: str, head_ref: str) -> tuple[str, ...]:
    base = merge_base(repo, base_ref, head_ref)
    result = _git(repo, "diff", "--name-only", "--diff-filter=ACDMRTUXB", "--", base, head_ref)
    if result.returncode != 0:
        detail = result.stderr.decode("utf-8", "replace").strip()
        raise ValueError(f"could not compute Git ref diff: {base_ref}, {head_ref}" + (f" ({detail})" if detail else ""))
    return tuple(sorted(line for line in result.stdout.decode("utf-8", "replace").splitlines() if line))


def archive_ref(repo: str | Path, ref: str, destination: str | Path) -> None:
    """Extract a committed ref tree into destination using ``git archive``."""
    target = Path(destination)
    target.mkdir(parents=True, exist_ok=True)
    # Trailing "--" marks end-of-options: `git archive` accepts flags like
    # --remote/--upload-pack that would run an arbitrary program in a
    # --remote invocation. `ref` reaches here from public entry points
    # (audit_ref/compare_refs), so a value shaped like a flag must never be
    # parsed as one, even though `-C <repo>` already keeps this local-only.
    result = _git(repo, "archive", ref, "--", stdout=subprocess.PIPE)
    if result.returncode != 0:
        detail = result.stderr.decode("utf-8", "replace").strip()
        raise ValueError(f"could not archive git ref: {ref}" + (f" ({detail})" if detail else ""))
    with tarfile.open(fileobj=__import__("io").BytesIO(result.stdout), mode="r:") as archive:
        members = archive.getmembers()
        for member in members:
            member_path = Path(member.name)
            if member_path.is_absolute() or ".." in member_path.parts:
                raise ValueError(f"unsafe path in git archive: {member.name}")
        # Extract one validated member at a time to remain compatible with
        # Python versions predating tarfile's ``filter=`` parameter while
        # retaining an explicit traversal check above.
        for member in members:
            try:
                archive.extract(member, target, filter="data")
            except TypeError:  # Python < 3.12
                archive.extract(member, target)
