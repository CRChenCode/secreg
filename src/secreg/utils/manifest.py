"""Build and read MANIFEST.json for handoff folders and output directories.

v2 format (PLAN_alfonso.md v2 section 3.2) adds `model`, `decoding`,
`oracle_test_version`, `split_version`, `env`, and `provenance` on top of the
base fields:
{
  "handoff_id": "...", "schema_version": "2.0", "producer": "gpu-owner" | "alfonso",
  "consumer": "...", "created_at": "...", "git_commit": "...", "config_hash": "...",
  "model": {...}, "decoding": {...}, "oracle_test_version": "...",
  "split_version": "...", "env": {...}, "provenance": {...},
  "files": [{"path", "records", "sha256"}], "notes": "..."
}
A `schema_version` that is not `2.x` should be treated as incompatible by
consumers, never auto-upgraded (PLAN_alfonso.md v2 section 3.3 rule 3).
"""

from __future__ import annotations

import json
import subprocess
from datetime import UTC, datetime
from pathlib import Path
from typing import Literal

from secreg.utils.hashing import sha256_file

MANIFEST_NAME = "MANIFEST.json"


def _git_commit() -> str:
    try:
        return (
            subprocess.check_output(["git", "rev-parse", "HEAD"], stderr=subprocess.DEVNULL)
            .decode()
            .strip()
        )
    except Exception:
        return "unknown"


def _count_jsonl_records(path: Path) -> int:
    if path.suffix != ".jsonl":
        return 0
    with open(path, "rb") as f:
        return sum(1 for _ in f)


def build_manifest(
    directory: str | Path,
    handoff_id: str,
    producer: Literal["gpu-owner", "alfonso"],
    consumer: str,
    schema_version: str,
    config_hash: str = "",
    notes: str = "",
    file_glob: str = "**/*",
    model: dict | None = None,
    decoding: dict | None = None,
    oracle_test_version: str | None = None,
    split_version: str | None = None,
    env: dict | None = None,
    provenance: dict | None = None,
) -> dict:
    directory = Path(directory)
    files = []
    for path in sorted(directory.glob(file_glob)):
        if path.is_dir() or path.name == MANIFEST_NAME:
            continue
        files.append(
            {
                "path": str(path.relative_to(directory)),
                "records": _count_jsonl_records(path),
                "sha256": sha256_file(path),
            }
        )
    manifest = {
        "handoff_id": handoff_id,
        "producer": producer,
        "consumer": consumer,
        "created_at": datetime.now(UTC).astimezone().isoformat(),
        "git_commit": _git_commit(),
        "config_hash": config_hash,
        "schema_version": schema_version,
        "model": model,
        "decoding": decoding,
        "oracle_test_version": oracle_test_version,
        "split_version": split_version,
        "env": env,
        "provenance": provenance,
        "files": files,
        "notes": notes,
    }
    with open(directory / MANIFEST_NAME, "w") as f:
        json.dump(manifest, f, indent=2)
    return manifest


def read_manifest(directory: str | Path) -> dict:
    directory = Path(directory)
    manifest_path = directory / MANIFEST_NAME
    if not manifest_path.exists():
        raise FileNotFoundError(f"No {MANIFEST_NAME} in {directory}")
    with open(manifest_path) as f:
        return json.load(f)
