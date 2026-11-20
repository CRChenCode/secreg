"""Resolve project paths from configs/cluster.yaml and environment variables.

Precedence: explicit environment variable > configs/cluster.yaml > error.
Keeps the rest of the codebase free of hard-coded cluster paths (PLAN.md Section 1).
"""

from __future__ import annotations

import os
from functools import lru_cache
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parents[2]
CLUSTER_CONFIG_PATH = REPO_ROOT / "configs" / "cluster.yaml"


@lru_cache(maxsize=1)
def _cluster_config() -> dict:
    if not CLUSTER_CONFIG_PATH.exists():
        return {}
    with open(CLUSTER_CONFIG_PATH) as f:
        return yaml.safe_load(f) or {}


def scratch_root() -> Path:
    """Root for all large/generated artifacts. Never write these under home or git."""
    env = os.environ.get("SCRATCH_ROOT")
    if env:
        return Path(env)
    cfg = _cluster_config()
    path = cfg.get("slurm", {}).get("scratch_root")
    if not path:
        raise RuntimeError(
            "scratch_root not set: export SCRATCH_ROOT or fill "
            "configs/cluster.yaml slurm.scratch_root"
        )
    return Path(path)


def hf_home() -> Path:
    return Path(os.environ.get("HF_HOME", scratch_root() / "hf"))


def logs_dir() -> Path:
    return Path(os.environ.get("SECREG_LOGS", scratch_root() / "logs"))


def data_dir(*parts: str) -> Path:
    """A subdirectory under scratch for a given data stage, e.g. data_dir('prefixes')."""
    p = scratch_root() / "data"
    for part in parts:
        p = p / part
    return p


def handoff_dir(handoff_id: str) -> Path:
    return scratch_root() / "handoffs" / handoff_id
