"""Matched-state activation caching (PLAN.md v2 Phase 8, REDESIGNED).

Owner: GPU owner. Consumes H5/H5b v2. Produces H6 v2: states keyed by
`state_id` (see secreg.utils.identity.state_id — never a raw token index
across mismatched prompts), with `context_id`, `anchor_id`,
`anchor_kind: "prompt" | "teacher_forced_fixture"`, and explicit
`intervention_provenance`. `constraint_end` is null (never synthesized) when
the constraint is absent in that branch. Not implemented yet; awaiting H5/H5b
and Phase 1 GPU smoke test (blocked on the Skipjack outage — see docs/cluster.md).
"""

from __future__ import annotations


def cache_states(context_pairs: list[dict], fixtures: list[dict], model_id: str) -> None:
    raise NotImplementedError(
        "secreg.analysis.cache: awaiting H5/H5b and a working GPU environment."
    )
