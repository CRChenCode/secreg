"""vLLM wrapper: batched sampling with fixed seeds, recorded as a `decoding_id` (v2).

Owner: GPU owner (PLAN.md v2 Phase 1 task onward). Not implemented yet —
depends on Phase 1 environment setup completing on a GPU node, which is
blocked on the Skipjack outage recorded in docs/cluster.md.
"""

from __future__ import annotations


def sample(
    model_id: str,
    model_revision: str,
    prompts: list[list[dict[str, str]]],
    n: int,
    temperature: float,
    seeds: list[int] | None = None,
    max_tokens: int = 2048,
) -> list[list[dict]]:
    raise NotImplementedError(
        "secreg.gen.engine.sample: Phase 1 vLLM smoke test has not run yet "
        "(blocked on Skipjack node outage — see docs/cluster.md)."
    )
