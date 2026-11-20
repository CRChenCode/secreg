"""Candidate security-decision regions and anchored comparisons (PLAN.md v2 Phase 7, REDESIGNED).

Renamed from `decision_token.py` (v1) — v2 explicitly removes the v1 "≥70%
of pairs diverge in a security-critical region" acceptance criterion and
reframes the first divergent token as a *candidate*, not an assumed decision
point (PLAN.md v2 §0 identification rule; §7).

Owner split:
- Alfonso: AST/region annotation (`regions.jsonl`) and authoring decision-
  region fixtures (H5b v2, `fixture.jsonl`) — CPU only.
- GPU owner: teacher-forced Δlogit / sequence-logprob at each fixture's
  `continuation_prefix`, within each fork of a context pair (this module).

Not implemented yet; awaiting H5 (context pairs) and H5b (fixtures).
"""

from __future__ import annotations


def score_fixture(fixture: dict, fork_id: str, model_id: str) -> dict:
    """GPU-owner step: teacher-force `fixture.continuation_prefix` after
    `fork_id`'s prompt and compute Δlogit (single_token_dlogit) or the
    conditional sequence log-prob difference (sequence_logprob), per
    `fixture.scoring`. Writes into `fixture_scores.parquet` (H6 v2).
    """
    raise NotImplementedError(
        "secreg.analysis.candidate_regions.score_fixture: awaiting H5/H5b (PLAN.md v2 Phase 7)."
    )
