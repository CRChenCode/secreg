"""Probes, risk model, and accessibility evidence (PLAN.md v2 Phase 9, REDESIGNED, RQ"A").

Owner: Alfonso (full; CPU is sufficient). Consumes H6 v2. Produces H7 v2,
frozen at GATE 9. Splits (train/calibration/test) must be fixed on
`data/tasks/splits.json` *before* any probe feature exists; this module must
never assign different outcome labels to the same pre-divergence `state_id`
(the identification rule forbids outcome probes on outcome_pairs). Required:
constraint-accessibility probes, the fork-level risk-propensity model, cross-
condition generalization, text/metadata-only baselines, early-warning
metrics. No H-loss/H-readout/H-override ground-truth labels are produced
here — only continuous accessibility evidence (`evidence_A.parquet`); causal
I/C come from Phase 10, not from this module. Not implemented yet; awaiting H6.
"""

from __future__ import annotations


def train_probe(states: dict, labels: list[int], probe_name: str, splits: dict) -> dict:
    raise NotImplementedError(
        "secreg.analysis.probes is owned by Alfonso (H7 v2, PLAN.md v2 Phase 9). "
        "Not yet delivered — see docs/STATUS.md."
    )
