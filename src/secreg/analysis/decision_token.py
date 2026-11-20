"""Locate the secure/insecure divergence token t* (PLAN.md Phase 7).

Steps 1-2 (find t*, filter by security-critical region) are Alfonso's, CPU/
tokenizer only, shipped inside H5 pairs.jsonl. Step 3 (teacher-force to
compute Δlogit) is the GPU owner's, shipped inside H6 dlogit.parquet. Not
implemented yet; awaiting H5.
"""

from __future__ import annotations


def validate_decision_token(pair: dict, model_id: str) -> dict:
    """GPU-owner step 3: teacher-force and compute Δlogit. Awaiting H5."""
    raise NotImplementedError("secreg.analysis.decision_token: awaiting H5 (PLAN.md Phase 7).")
