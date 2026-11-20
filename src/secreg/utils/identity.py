"""Encodes the key identification rule (PLAN.md v2 §0):

"For an autoregressive model in deterministic evaluation, two completions
with the same exact token prefix have identical hidden states immediately
before the first divergent token, regardless of which token is later
sampled."

`state_id` is the only sanctioned way to key a cached activation (H6 v2:
`manifest.jsonl` keys by `state_id`). It is a pure function of (model
revision, the token ids *up to and including* `token_index`, and the anchor
kind) — never of anything that depends on tokens sampled *after*
`token_index`. That makes it mechanically impossible for two branches
sharing a prefix to be assigned different state_ids at a shared position,
which is what tests/test_stats.py::test_identification_rule_shared_prefix
checks.
"""

from __future__ import annotations

from secreg.utils.hashing import content_hash


def prompt_token_hash(token_ids: list[int], model_revision: str) -> str:
    return content_hash({"model_revision": model_revision, "token_ids": token_ids}, length=24)


def state_id(model_revision: str, token_ids_up_to_index: list[int], anchor_kind: str) -> str:
    """Deterministic id for a cached activation state.

    `token_ids_up_to_index` must be sliced to end at (and include) the
    position being cached — never pass the full completion. Two sequences
    that agree on every token up to that index, however they continue, must
    yield the same state_id: that's the identification rule above.
    """
    return content_hash(
        {
            "model_revision": model_revision,
            "shared_prefix": token_ids_up_to_index,
            "anchor_kind": anchor_kind,
        },
        length=24,
    )
