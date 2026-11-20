"""Activation caching via nnsight / HF forward hooks (PLAN.md Phase 8).

Owner: GPU owner. Consumes H5. Not implemented yet; awaiting H5 and Phase 1
GPU smoke test (blocked on the Skipjack outage — see docs/cluster.md).
"""

from __future__ import annotations


def cache_activations(samples: list[dict], model_id: str, positions: list[str]) -> None:
    raise NotImplementedError("secreg.analysis.cache: awaiting H5 and a working GPU environment.")
