"""Direction construction and steering (PLAN.md v2 Phase 10 direction interventions, Phase 11).

Owner: GPU owner, using H7 v2 probe/diff-of-means directions (constraint-
related, insecure-source-related, and random/control directions). Avoid
selecting the intervention layer on the untouched test split. Not
implemented yet; awaiting H7 v2.
"""

from __future__ import annotations


def steer(state: dict, direction_source: str, layer: int, strength: float) -> dict:
    raise NotImplementedError("secreg.analysis.steering: awaiting H7 v2 (PLAN.md v2 Phase 10/11).")
