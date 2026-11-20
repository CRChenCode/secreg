# Data Schema Reference — v2

Canonical source of truth, mirrored in `src/secreg/schemas.py` (pydantic models),
`PLAN.md` v2 §2 (migration table), and `PLAN_alfonso.md` v2 §4 (field-by-field
JSON examples). **Any field change must update all three, bump `schema_version`,
and go through a PR reviewed by both owners** (PLAN.md v2 §13).

Current `schema_version`: **`2.0`**. v1 payloads are rejected, never coerced
(`PLAN_alfonso.md` v2 §3.3 rule 3) — every model below uses `extra="forbid"`
so a missing or renamed required v2 field raises a `pydantic.ValidationError`
instead of silently validating a v1-shaped record.

## Key identification rule (governs H6/H7/H8 — PLAN.md v2 §0)

Two completions with the same exact token prefix have **identical hidden
states** immediately before the first divergent token, regardless of which
token is later sampled. Consequently:
- `outcome_pairs.jsonl` (below) carries **no activation/state fields** — it
  exists only for code-region localization, never to contrast pre-divergence
  states.
- Cached activations are keyed by `state_id` (`secreg.utils.identity.state_id`),
  a pure function of `(model_revision, tokens up to and including this
  position, anchor_kind)` — never of anything sampled after that position.
  `tests/test_stats.py::test_identification_rule_shared_prefix_same_state_id`
  enforces this mechanically.

## Record types

| Record | File | Produced by | Pydantic model |
|---|---|---|---|
| Task | `tasks.jsonl` (H1 v2) | Alfonso | `secreg.schemas.Task` |
| Prefix | `prefix.jsonl` | GPU owner (Phase 4) | `secreg.schemas.Prefix` |
| Fork | `fork.jsonl` | Alfonso's `make_contrasts` (H3 v2), run by GPU owner | `secreg.schemas.Fork` |
| Sample (raw) | `sample.jsonl` (H4 v2) | GPU owner | `secreg.schemas.Sample` |
| Labeled sample | `samples_labeled/*.jsonl` (H5 v2) | Alfonso | `secreg.schemas.LabeledSample` |
| Context pair | `context_pairs.jsonl` (H5 v2) | Alfonso | `secreg.schemas.ContextPair` |
| Outcome pair | `outcome_pairs.jsonl` (H5 v2) | Alfonso | `secreg.schemas.OutcomePair` |
| Region | `regions.jsonl` (H5 v2) | Alfonso | `secreg.schemas.Region` |
| Fixture | H5b v2 (new) | Alfonso | `secreg.schemas.Fixture` |

**Context pairs vs. outcome pairs** (do not conflate): a context pair
`(control_fork, manipulated_fork)` is the *primary causal unit* — it compares
two distinct prompts and is what Phase 8/10 cache and patch. An outcome pair
`(secure_sample, insecure_sample)` compares two completions sampled from the
*same* fork; per the identification rule, their activations before the first
divergent token are provably identical, so an outcome pair can only localize
candidate code regions — it must never back a probe or a patch.

See `PLAN.md` v2 §2 "Mandatory v2 schema migration" for the full rationale per
field, and `PLAN_alfonso.md` v2 §4 for every Parquet table's columns
(`pilot_summary`, `fork_stats`, `contrast_effects`, `fixture_scores`,
`attn_descriptive`, `moe_routing`, `evidence_A`, `patching_results`,
`direction_results`, `evidence_matrix`, `interventions_summary`) and the H6 v2
safetensors layout (keyed by `state_id`, see above).

## Validating a record

```python
from secreg.schemas import Task
Task.model_validate(record_dict)  # raises pydantic.ValidationError on a v1-shaped or malformed record
```

## Statistics

`secreg.stats` implements Wilson intervals and the **hierarchical
(task → prefix → sample) bootstrap** PLAN.md v2 §2 requires in place of a flat,
unclustered bootstrap. `tests/test_stats.py` demonstrates the clustered
interval is substantially wider than a naive one under task-correlated data —
the exact failure mode the plan forbids ("do not treat 20 samples from one
fork as 20 independent tasks").

## Handoff verification

Every handoff folder carries a `MANIFEST.json` (v2 shape: adds `model`,
`decoding`, `oracle_test_version`, `split_version`, `env`, `provenance` —
see `PLAN_alfonso.md` v2 §3.2). Consumers run:

```bash
python -m secreg.utils.verify_handoff <dir>
```

before reading any handoff, and never modify a handoff folder in place.
`schema_version` must be `2.x`; a `1.x` manifest should be treated as
incompatible, not auto-upgraded.
