"""Apply fork conditions to prefixes (PLAN.md Phase 5).

Owner: Alfonso (H3: this file + configs/conditions.yaml + tests/test_forks.py).
The GPU owner only *runs* make_forks on Phase 4 prefixes — never reimplements
condition logic. Not implemented yet; awaiting H3 delivery (GATE 5).
"""

from __future__ import annotations

from typing import Any


def make_forks(prefix: dict, task: dict, conditions: list[str], tokenizer: Any) -> list[dict]:
    raise NotImplementedError(
        "secreg.gen.forks.make_forks is owned by Alfonso (H3, PLAN.md Phase 5). "
        "Not yet delivered — see docs/STATUS.md."
    )
