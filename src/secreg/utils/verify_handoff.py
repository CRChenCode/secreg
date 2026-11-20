"""Verify a handoff folder before use (PLAN_alfonso.md section 3.2 rule 1).

Usage: python -m secreg.utils.verify_handoff <dir>
Exits non-zero and prints every mismatch if verification fails. Consumers must
run this before reading a handoff and must never modify a handoff in place.
"""

from __future__ import annotations

import sys
from pathlib import Path

from secreg.utils.hashing import sha256_file
from secreg.utils.manifest import read_manifest


def verify_handoff(directory: str | Path) -> list[str]:
    """Returns a list of problem descriptions; empty list means verification passed."""
    directory = Path(directory)
    problems: list[str] = []
    try:
        manifest = read_manifest(directory)
    except FileNotFoundError as e:
        return [str(e)]

    for entry in manifest.get("files", []):
        path = directory / entry["path"]
        if not path.exists():
            problems.append(f"missing file listed in manifest: {entry['path']}")
            continue
        actual = sha256_file(path)
        if actual != entry["sha256"]:
            problems.append(
                f"sha256 mismatch for {entry['path']}: manifest={entry['sha256']} actual={actual}"
            )
    return problems


def main(argv: list[str] | None = None) -> int:
    argv = argv if argv is not None else sys.argv[1:]
    if len(argv) != 1:
        print("usage: python -m secreg.utils.verify_handoff <dir>", file=sys.stderr)
        return 2
    problems = verify_handoff(argv[0])
    if problems:
        print(f"FAILED verification for {argv[0]}:", file=sys.stderr)
        for p in problems:
            print(f"  - {p}", file=sys.stderr)
        return 1
    print(f"OK: {argv[0]} verified against MANIFEST.json")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
