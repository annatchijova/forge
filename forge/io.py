"""Named boundaries for reading JSON artifacts and persisted trace payloads."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any


class ForgeArtifactError(ValueError):
    """A present artifact could not be decoded as the expected JSON document."""


def parse_json(raw: str, source: str = "JSON input") -> Any:
    if not isinstance(raw, str):
        raise ForgeArtifactError(f"malformed {source}: expected text input")
    try:
        return json.loads(raw)
    except (json.JSONDecodeError, UnicodeDecodeError) as exc:
        raise ForgeArtifactError(f"malformed {source}: {exc}") from exc


def load_json(path: str | Path, source: str | None = None) -> Any:
    path = Path(path)
    return parse_json(path.read_text(encoding="utf-8"), source or str(path))
