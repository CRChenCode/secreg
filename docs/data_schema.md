# Data Schema Reference

Canonical source of truth, mirrored in `src/secreg/schemas.py` (pydantic models) and
`PLAN.md` §2. **Any field change must update both files, bump `schema_version`, and
go through a PR reviewed by both owners (PLAN.md Agent Behavior Constraints #7).**

Current `schema_version`: `1.0` (all record types).

| Record | File | Produced by | Pydantic model |
|---|---|---|---|
| Task | `tasks.jsonl` (H1) | Alfonso | `secreg.schemas.Task` |
| Prefix | `prefix.jsonl` | GPU owner (Phase 4) | `secreg.schemas.Prefix` |
| Fork | `fork.jsonl` | Alfonso's `make_forks`, run by GPU owner | `secreg.schemas.Fork` |
| Sample | `sample.jsonl` | GPU owner (raw, H4); labels added by Alfonso (H5) | `secreg.schemas.Sample` |
| Pair | `pair.jsonl` | Alfonso (H5) | `secreg.schemas.Pair` |

See `PLAN.md` §2 "Canonical schemas" for the field-by-field JSON examples, and
`PLAN_alfonso.md` §4 for every Parquet table's columns and tensor layouts
(pilot_summary, fork_stats, delta_p, attn_to_spans, routing, dlogit, probe_eval,
patching/steering results, interventions_summary).

## Validating a record

```python
from secreg.schemas import Task
Task.model_validate(record_dict)  # raises pydantic.ValidationError on mismatch
```

## Handoff verification

Every handoff folder carries a `MANIFEST.json` (see `src/secreg/utils/manifest.py`).
Consumers run:

```bash
python -m secreg.utils.verify_handoff <dir>
```

before reading any handoff, and never modify a handoff folder in place
(PLAN_alfonso.md §3.2).
