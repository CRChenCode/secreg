"""RQ3 interventions and baselines (PLAN.md Phase 11).

Common interface: apply(messages, model_client) -> generation, where
model_client has an `api` backend (Alfonso) and a `vllm` backend (GPU owner).
Not implemented yet; awaiting H7 (diagnosis-driven dispatch) and earlier phases.
"""

from __future__ import annotations

from typing import Protocol


class ModelClient(Protocol):
    def generate(self, messages: list[dict], **kwargs) -> dict: ...


def apply(messages: list[dict], model_client: ModelClient) -> dict:
    raise NotImplementedError("secreg.interventions.apply: no intervention implemented yet.")
