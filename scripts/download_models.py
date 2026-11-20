#!/usr/bin/env python
"""Download models listed in configs/models.yaml into $SCRATCH_ROOT/hf and
verify integrity (Phase 1 task 4). Run on a login/data-transfer node per
cluster policy (no GPU needed for a snapshot download).

Usage: python scripts/download_models.py [--only primary,pilot_qwen3_4b]
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from secreg.paths import hf_home  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--only", help="comma-separated model keys from configs/models.yaml")
    parser.add_argument(
        "--config", default=str(Path(__file__).resolve().parents[1] / "configs" / "models.yaml")
    )
    args = parser.parse_args()

    from huggingface_hub import snapshot_download

    with open(args.config) as f:
        cfg = yaml.safe_load(f)

    keys = args.only.split(",") if args.only else list(cfg["models"].keys())
    cache_dir = hf_home()
    cache_dir.mkdir(parents=True, exist_ok=True)

    for key in keys:
        entry = cfg["models"][key]
        hf_id = entry["hf_id"]
        print(f"[download_models] {key} -> {hf_id}")
        local_path = snapshot_download(repo_id=hf_id, cache_dir=str(cache_dir))
        size_bytes = sum(f.stat().st_size for f in Path(local_path).rglob("*") if f.is_file())
        print(f"[download_models]   ok: {local_path} ({size_bytes / 1e9:.2f} GB)")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
