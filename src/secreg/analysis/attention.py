"""Descriptive attention statistics (PLAN.md v2 Phase 8 task 3 / Phase 10 task 5).

Owner: GPU owner. v2 is explicit that attention mass is a *descriptive*
signal only — never call it causal; a controlled perturbation (patching /
ablation in secreg.analysis.patching) is required to support any causal
claim about attention-to-vulnerable-code. Writes `attn_descriptive.parquet`.
Not implemented yet; awaiting H5 and a working GPU environment.
"""

from __future__ import annotations


def attention_to_spans(state_id: str, spans: list[dict]) -> dict:
    raise NotImplementedError(
        "secreg.analysis.attention: awaiting H5 and a working GPU environment."
    )
