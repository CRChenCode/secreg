"""Valid on-policy prefix construction (PLAN.md v2 Phase 4).

Owner: GPU owner. Consumes H1 v2 (secreg.oracles.evaluate) in-loop to filter
each turn — do not reimplement oracle logic here. Each turn must record the
actual agent output/repo state (`repo_state_hash`, `invariant_valid`,
`active_constraint_set`) — v2 forbids inferring a "secure prefix" without
storing the real state (PLAN.md v2 §2 migration table: "avoids fictional or
stale secure prefixes"). Not implemented yet: depends on H1 v2 (Alfonso, not
yet delivered) and a working vLLM engine (secreg.gen.engine).
"""

from __future__ import annotations


def build_prefixes(
    model_id: str, model_revision: str, task_ids: list[str], k: int = 3, m: int = 3
) -> list[dict]:
    raise NotImplementedError(
        "secreg.gen.prefixes.build_prefixes: awaiting H1 v2 (oracle library + "
        "tasks.jsonl + splits.json) and a working sampling engine. See docs/STATUS.md."
    )
