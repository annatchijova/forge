"""Runtime source fingerprint - detects a long-running process serving stale code.

A CLI invocation (`python3 -m forge audit ...`) always re-imports from disk,
so it is always current. A long-running server (`forge.mcp_server`,
`forge.cronos_mcp_server`, `forge.loop_mcp`) keeps whatever was on disk at
process start loaded in memory for its entire lifetime: a source fix applied
after the server started is real on disk and invisible to that process until
it restarts, with nothing in its responses distinguishing "the fix does not
work" from "this process has not loaded the fix yet."

RUNTIME_FINGERPRINT is computed once, at import time, from the path, mtime,
and size of every .py file under this package - not a manually maintained
version string (which stays the same across ordinary commits), so it changes
automatically the moment the process is restarted after any source change,
with zero versioning discipline required from anyone.
"""
from __future__ import annotations

import hashlib
import time
from pathlib import Path

_PACKAGE_ROOT = Path(__file__).resolve().parent


def _compute_fingerprint(root: Path) -> str:
    entries = sorted(
        (str(path.relative_to(root)), path.stat().st_mtime_ns, path.stat().st_size)
        for path in root.rglob("*.py")
    )
    return hashlib.sha256(repr(entries).encode("utf-8")).hexdigest()[:16]


RUNTIME_FINGERPRINT: str = _compute_fingerprint(_PACKAGE_ROOT)
# int, not float: this can flow into sealed/canonicalized payloads
# (forge/canonical.py forbids floats there entirely - deterministic-core).
PROCESS_IMPORTED_AT_EPOCH: int = int(time.time())

__all__ = ("RUNTIME_FINGERPRINT", "PROCESS_IMPORTED_AT_EPOCH")
