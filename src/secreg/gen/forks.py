"""Build matched (control, manipulated) contrasts from a prefix (PLAN.md v2 Phase 5).

Owner: Alfonso (H3 v2: this file + configs/conditions.yaml + tests/test_forks.py).
v2 renames `make_forks` -> `make_contrasts`: every call now returns paired
(manipulated_fork, matched_control_fork) records sharing a `contrast_id`,
with an explicit `manipulation_check` (one declared factor per contrast;
`compound: true` if more than the declared factor actually changed). The GPU
owner only *runs* this on Phase 4 prefixes — never reimplements factor logic.
Not implemented yet; awaiting H3 v2 delivery (GATE 5).
"""

from __future__ import annotations

from typing import Any


def make_contrasts(
    prefix: dict, task: dict, conditions: list[str], tokenizer: Any, chat_template: Any
) -> list[tuple[dict, dict]]:
    raise NotImplementedError(
        "secreg.gen.forks.make_contrasts is owned by Alfonso (H3 v2, PLAN.md v2 Phase 5). "
        "Not yet delivered — see docs/STATUS.md."
    )
