"""Shared statistics: Wilson intervals, hierarchical (clustered) bootstrap,
and paired contrast effects.

PLAN.md v2 §2 requires bootstrapping by task (not by generation): "bootstrap
tasks first, prefixes nested within tasks, samples nested within forks. Do
not treat 20 samples from one fork as 20 independent tasks." This module is
Alfonso's week-1 infra item (PLAN_alfonso.md v2 §5.1) and is exercised by the
GATE-1-mandated clustered-bootstrap unit test (tests/test_stats.py).
"""

from __future__ import annotations

import math
from collections.abc import Callable, Sequence
from dataclasses import dataclass

import numpy as np


def wilson_ci(successes: int, n: int, confidence: float = 0.95) -> tuple[float, float]:
    """Wilson score interval for a binomial proportion. Stable at small n and
    at p near 0 or 1, unlike the normal approximation.
    """
    if n == 0:
        return (0.0, 0.0)
    z = {0.90: 1.645, 0.95: 1.96, 0.99: 2.576}.get(confidence)
    if z is None:
        raise ValueError(f"unsupported confidence level: {confidence}")
    p = successes / n
    denom = 1 + z**2 / n
    center = p + z**2 / (2 * n)
    margin = z * math.sqrt(p * (1 - p) / n + z**2 / (4 * n**2))
    return ((center - margin) / denom, (center + margin) / denom)


@dataclass(frozen=True)
class ClusterKeys:
    """Column names identifying each nesting level, outermost first.

    E.g. ("task_id", "prefix_id", "fork_id") for the design in PLAN.md v2 §6:
    tasks -> prefixes nested in tasks -> samples nested in forks.
    """

    levels: tuple[str, ...]


def _resample_nested(
    rows: Sequence[dict], levels: tuple[str, ...], rng: np.random.Generator
) -> list[dict]:
    """Resample `rows` by cluster, recursively, outermost level first.

    At each level, resample (with replacement) the distinct keys seen at that
    level, then recurse into each chosen cluster's rows for the next level.
    The innermost level's rows are returned as-is (no row-level resampling —
    PLAN.md v2 explicitly nests samples within forks, it does not resample
    individual non-clustered rows).
    """
    if not levels:
        return list(rows)
    level = levels[0]
    groups: dict = {}
    for row in rows:
        groups.setdefault(row[level], []).append(row)
    keys = list(groups.keys())
    chosen_keys = rng.choice(keys, size=len(keys), replace=True)
    out: list[dict] = []
    for key in chosen_keys:
        out.extend(_resample_nested(groups[key], levels[1:], rng))
    return out


def hierarchical_bootstrap_ci(
    rows: Sequence[dict],
    cluster_levels: Sequence[str],
    statistic_fn: Callable[[Sequence[dict]], float],
    n_boot: int = 2000,
    confidence: float = 0.95,
    seed: int = 0,
) -> tuple[float, float, float]:
    """Hierarchical (multi-level cluster) bootstrap CI.

    Returns (point_estimate, ci_low, ci_high). `statistic_fn` computes the
    quantity of interest (e.g. P(functional AND secure)) from a list of row
    dicts; `cluster_levels` are column names from outermost to innermost
    (e.g. ["task_id", "prefix_id", "fork_id"]).
    """
    point = statistic_fn(rows)
    rng = np.random.default_rng(seed)
    levels = tuple(cluster_levels)
    boot_stats = np.empty(n_boot)
    for i in range(n_boot):
        resampled = _resample_nested(rows, levels, rng)
        boot_stats[i] = statistic_fn(resampled)
    alpha = 1 - confidence
    lo, hi = np.quantile(boot_stats, [alpha / 2, 1 - alpha / 2])
    return (point, float(lo), float(hi))


def paired_contrast_effect(
    condition_rows: Sequence[dict],
    control_rows: Sequence[dict],
    cluster_levels: Sequence[str],
    statistic_fn: Callable[[Sequence[dict]], float],
    n_boot: int = 2000,
    confidence: float = 0.95,
    seed: int = 0,
) -> tuple[float, float, float]:
    """effect = risk(condition) - risk(control), with a hierarchical-bootstrap CI
    on the paired difference (PLAN.md v2 §0 "Condition effect").
    """
    rng = np.random.default_rng(seed)
    levels = tuple(cluster_levels)
    point = statistic_fn(condition_rows) - statistic_fn(control_rows)
    boot_diffs = np.empty(n_boot)
    for i in range(n_boot):
        r_cond = _resample_nested(condition_rows, levels, rng)
        r_ctrl = _resample_nested(control_rows, levels, rng)
        boot_diffs[i] = statistic_fn(r_cond) - statistic_fn(r_ctrl)
    alpha = 1 - confidence
    lo, hi = np.quantile(boot_diffs, [alpha / 2, 1 - alpha / 2])
    return (point, float(lo), float(hi))


def flat_bootstrap_ci(
    rows: Sequence[dict],
    statistic_fn: Callable[[Sequence[dict]], float],
    n_boot: int = 2000,
    confidence: float = 0.95,
    seed: int = 0,
) -> tuple[float, float, float]:
    """Naive row-level bootstrap, ignoring clustering. Exists only as the
    "wrong" comparison in tests/test_stats.py — never use this for a reported
    result (PLAN.md v2 §0: "Do not treat 20 samples from one fork as 20
    independent tasks").
    """
    point = statistic_fn(rows)
    rng = np.random.default_rng(seed)
    n = len(rows)
    boot_stats = np.empty(n_boot)
    for i in range(n_boot):
        idx = rng.integers(0, n, size=n)
        boot_stats[i] = statistic_fn([rows[j] for j in idx])
    alpha = 1 - confidence
    lo, hi = np.quantile(boot_stats, [alpha / 2, 1 - alpha / 2])
    return (point, float(lo), float(hi))
