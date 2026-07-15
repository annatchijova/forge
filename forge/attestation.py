"""Process-local provenance attestation for FORGE-generated manifests."""
from __future__ import annotations

import hashlib
import hmac
import secrets
from typing import Any

from forge.canonical import canonical_json

_KEY = secrets.token_bytes(32)


def _payload(manifest: dict[str, Any]) -> bytes:
    unsigned = dict(manifest)
    unsigned.pop("source_attestation", None)
    return canonical_json(unsigned).encode("utf-8")


def attest_manifest(manifest: dict[str, Any]) -> str:
    """Create an in-process token proving Runtime generated this manifest."""
    return hmac.new(_KEY, _payload(manifest), hashlib.sha256).hexdigest()


def verify_manifest_attestation(manifest: dict[str, Any]) -> bool:
    token = manifest.get("source_attestation")
    if not isinstance(token, str) or not token:
        return False
    expected = attest_manifest(manifest)
    return hmac.compare_digest(token, expected)

