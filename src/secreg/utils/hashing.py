"""Content hashing for record ids, config hashes, and MANIFEST.json sha256 fields."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any


def sha256_file(path: str | Path, chunk_size: int = 1 << 20) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(chunk_size), b""):
            h.update(chunk)
    return h.hexdigest()


def content_hash(obj: Any, length: int = 16) -> str:
    """Deterministic short hash of a JSON-serializable object, used for record ids."""
    payload = json.dumps(obj, sort_keys=True, default=str).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()[:length]


def config_hash(config: dict) -> str:
    return content_hash(config, length=12)
