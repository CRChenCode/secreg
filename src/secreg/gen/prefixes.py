"""On-policy prefix construction (PLAN.md Phase 4).

Owner: GPU owner. Consumes H1 (secreg.oracles.evaluate) in-loop to filter each
turn — do not reimplement oracle logic here. Not implemented yet: depends on
H1 (Alfonso, not yet delivered) and a working vLLM engine (secreg.gen.engine).
"""

from __future__ import annotations


def build_prefixes(model_id: str, task_ids: list[str], k: int = 3, m: int = 3) -> list[dict]:
    raise NotImplementedError(
        "secreg.gen.prefixes.build_prefixes: awaiting H1 (oracle library + tasks.jsonl) "
        "and a working sampling engine. See docs/STATUS.md."
    )
