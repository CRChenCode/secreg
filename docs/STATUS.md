# Status

Updated: 2026-11-20

## Phases

| Phase | Status | Notes |
|---|---|---|
| 0 Cluster recon | **Partial** | Account/storage/software facts confirmed (`docs/cluster.md`). GPU-specific checks blocked on a cluster-wide Skipjack outage; test job **1987143** queued on `l40s`, will complete once nodes recover. |
| 1 Repo & env | **In progress** | Repo skeleton, `pyproject.toml`, pre-commit, SLURM template, `configs/models.yaml` (4 model IDs verified on HF) done. Repo rsynced to `/home/jhu/cchen343/secreg` on Skipjack; CPU-only dev venv built at `/scratch/jhu/yyao69/cchen343/secreg/venv` (`uv sync --extra dev`); `pytest` (6/6) and `ruff check` pass both locally and on the Skipjack login node. Not done: `[gpu]` extra install (torch/vllm/nnsight — needs a GPU node to pick the right CUDA wheel), model downloads, GPU smoke test. |
| 2 Tasks & oracles | Not started | Alfonso-owned (PLAN.md Phase 2 / H1). |
| 3–12 | Not started | — |

## Open handoffs

None yet (H1 not started).

## Blockers

- **Skipjack cluster outage** (observed 2026-11-20, ~12:50–14:55 local): essentially
  all compute nodes across every GPU partition (l40s, a100, h100, h200, rtx6000,
  b200, b300, interactive_gpu) are `DOWN+NOT_RESPONDING`. Not account-specific —
  hundreds of other users' jobs are stuck the same way. No ETA known from this side.
  Decision: proceed with non-GPU Phase 1 work in the meantime (`docs/decisions.md`).

## Next steps

1. Once Skipjack nodes recover: check job 1987143's log, finish Phase 0 GATE 0
   verification items, then run Phase 1 tasks 2–5 (env install, SLURM template
   test, model downloads, GPU smoke test).
2. Decide (with the user) how/when to start Phase 2 (Alfonso-owned: seed tasks
   and oracles) given there is currently only one executing agent.
