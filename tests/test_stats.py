"""The two unit tests PLAN.md v2 §2 requires before GATE 1:

(i) deterministic hidden-state equality on identical token prefixes before
    sample divergence (the "key identification rule", PLAN.md v2 §0);
(ii) bootstrapping by task rather than unclustered generation.
"""

from __future__ import annotations

import numpy as np

from secreg.stats import flat_bootstrap_ci, hierarchical_bootstrap_ci, wilson_ci
from secreg.utils.identity import state_id


def test_identification_rule_shared_prefix_same_state_id():
    shared_prefix = [1, 2, 3, 4, 5]
    secure_continuation = shared_prefix + [100, 101]
    insecure_continuation = shared_prefix + [200, 201, 202]

    # The state at the position right before divergence is a function of the
    # shared prefix only — it must not depend on what each branch sampled next.
    id_secure_branch = state_id("rev1", secure_continuation[: len(shared_prefix)], "pre_decision")
    id_insecure_branch = state_id(
        "rev1", insecure_continuation[: len(shared_prefix)], "pre_decision"
    )
    assert id_secure_branch == id_insecure_branch

    # Including even one post-divergence token must change the id — state_id
    # is keyed strictly by "tokens up to and including this position", so it
    # is mechanically impossible to assign the divergent continuations the
    # same id past the shared prefix.
    id_after_divergence_secure = state_id(
        "rev1", secure_continuation[: len(shared_prefix) + 1], "pre_decision"
    )
    assert id_after_divergence_secure != id_secure_branch

    # A different model revision must never collide with another revision's state.
    id_other_revision = state_id("rev2", shared_prefix, "pre_decision")
    assert id_other_revision != id_secure_branch


def test_wilson_ci_contains_point_estimate_and_widens_at_small_n():
    point = 7 / 10
    lo_small, hi_small = wilson_ci(7, 10)
    assert lo_small <= point <= hi_small
    lo_large, hi_large = wilson_ci(700, 1000)
    assert (hi_small - lo_small) > (hi_large - lo_large)


def _make_clustered_rows(
    n_tasks: int, prefixes_per_task: int, samples_per_prefix: int, seed: int
) -> list[dict]:
    """Synthetic data with strong *task-level* correlation: each task gets its
    own latent risk, and all its samples inherit it almost deterministically.
    A flat (row-level) bootstrap ignores this and understates uncertainty; a
    hierarchical bootstrap resampling tasks first should not.
    """
    rng = np.random.default_rng(seed)
    rows = []
    for t in range(n_tasks):
        task_risk = rng.beta(2, 2)  # one risk level per task, shared by all its rows
        for p in range(prefixes_per_task):
            for s in range(samples_per_prefix):
                outcome = rng.random() < task_risk
                rows.append(
                    {
                        "task_id": f"task{t}",
                        "prefix_id": f"task{t}-pre{p}",
                        "sample_id": f"task{t}-pre{p}-s{s}",
                        "secure": bool(outcome),
                    }
                )
    return rows


def _p_secure(rows) -> float:
    if not rows:
        return 0.0
    return sum(1 for r in rows if r["secure"]) / len(rows)


def test_clustered_bootstrap_is_wider_than_flat_bootstrap_under_task_correlation():
    rows = _make_clustered_rows(n_tasks=8, prefixes_per_task=3, samples_per_prefix=20, seed=42)

    _, flat_lo, flat_hi = flat_bootstrap_ci(rows, _p_secure, n_boot=1000, seed=1)
    _, clustered_lo, clustered_hi = hierarchical_bootstrap_ci(
        rows, ["task_id", "prefix_id", "sample_id"], _p_secure, n_boot=1000, seed=1
    )

    flat_width = flat_hi - flat_lo
    clustered_width = clustered_hi - clustered_lo

    # With only 8 independent task-level risk draws (vs. 480 rows), a bootstrap
    # that resamples tasks first must reflect that small effective sample size
    # and come out noticeably wider than one that treats every row as
    # independent — exactly the failure mode PLAN.md v2 §2 forbids ("do not
    # treat 20 samples from one fork as 20 independent tasks").
    assert clustered_width > flat_width * 1.5
