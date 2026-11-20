"""RQ3 intervention study with independent evaluation (PLAN.md v2 Phase 11, REDESIGNED).

Common interface: apply(messages, model_client) -> generation, where
model_client has an `api` backend (Alfonso) and a `vllm` backend (GPU owner).
v2 adds explicit non-diagnostic comparators that must be beaten before any
"mechanism-informed" claim: (8) best single targeted method applied
universally, (9) shuffled/random dispatch at matched cost, (10) oracle
diagnosis dispatch (upper bound only, never deployable), (11) predicted
diagnosis dispatch (frozen pre-generation, evaluated on held-out tasks). A
risk predictor alone does not identify which mechanism causes a failure —
label an undispatched risk-gated method "risk-gated universal intervention",
not mechanism-specific. Not implemented yet; awaiting H7 v2 and earlier phases.
"""

from __future__ import annotations

from typing import Protocol


class ModelClient(Protocol):
    def generate(self, messages: list[dict], **kwargs) -> dict: ...


def apply(messages: list[dict], model_client: ModelClient) -> dict:
    raise NotImplementedError("secreg.interventions.apply: no intervention implemented yet.")
