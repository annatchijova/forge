"""Single, typed, deterministic serializer for sealed FORGE data."""
from __future__ import annotations

import json
from dataclasses import asdict, is_dataclass
from typing import Any

CANONICALIZE_VERSION = "1"


def _typed(value: Any) -> Any:
    if value is None:
        return {"type": "null"}
    if isinstance(value, bool):
        return {"type": "bool", "value": value}
    if isinstance(value, int):
        return {"type": "int", "value": str(value)}
    if isinstance(value, float):
        raise TypeError("floats are not allowed in sealed payloads")
    if isinstance(value, str):
        return {"type": "str", "value": value}
    if is_dataclass(value):
        return _typed(asdict(value))
    if isinstance(value, dict):
        return {"type": "dict", "value": {str(k): _typed(value[k]) for k in sorted(value, key=str)}}
    if isinstance(value, (list, tuple)):
        return {"type": "list", "value": [_typed(item) for item in value]}
    raise TypeError(f"unsupported sealed value: {type(value).__name__}")


def canonical_json(value: Any) -> str:
    return json.dumps(_typed(value), ensure_ascii=False, sort_keys=True, separators=(",", ":"))
