"""Causal mechanism experiments (PLAN.md v2 Phase 10, REDESIGNED).

Owner: GPU owner (patching hierarchy: sham controls -> matched-anchor
patching -> reverse patch -> direction interventions -> source-specific
tests -> full-generation validation), using H7 v2 directions for the
direction-intervention step. Produces H8 v2 (`patching_results.parquet`,
`direction_results.parquet`, raw resampled generations). Start at one
model x one CWE x one manipulation before expanding (PLAN.md v2 §10).
Recovery is reported only when `|D|` clears a pre-registered minimum and
sign is interpretable; values outside [0,1] are expected and must not be
clipped. Not implemented yet; awaiting H5/H6/H7 v2.
"""

from __future__ import annotations


def patch_state(
    context_pair: dict,
    fixture: dict,
    layer: int,
    component: str,
    # "forward" | "reverse" | "sham_same_state" | "sham_random_layer" | "sham_unrelated_context"
    direction: str,
) -> dict:
    raise NotImplementedError(
        "secreg.analysis.patching: awaiting H5/H6/H7 v2 (PLAN.md v2 Phase 10)."
    )
