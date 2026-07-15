"""Deterministic source snapshot hashing for repository chain of custody."""
from __future__ import annotations

import hashlib
from pathlib import Path
from typing import Iterable


def snapshot_sha256(root: str | Path, paths: Iterable[Path]) -> str:
    """Hash relative paths and bytes in stable order before audit output exists."""
    base = Path(root).resolve()
    digest = hashlib.sha256()
    for path in sorted((Path(item) for item in paths), key=lambda item: str(item.relative_to(base))):
        relative = path.relative_to(base).as_posix().encode("utf-8")
        digest.update(len(relative).to_bytes(8, "big"))
        digest.update(relative)
        try:
            payload = path.read_bytes()
        except (OSError, UnicodeError) as exc:
            marker = f"UNREADABLE:{type(exc).__name__}".encode("utf-8")
            digest.update(len(marker).to_bytes(8, "big")); digest.update(marker)
            continue
        digest.update(len(payload).to_bytes(8, "big"))
        digest.update(payload)
    return digest.hexdigest()
