# Status

Updated: 2026-11-20

**Plan version: v2.0** (research-design rewrite received 2026-11-20; see
`docs/decisions.md` for the full diff summary). Status per `PLAN.md` v2 header:
**PROPOSED** — do not launch large-scale Phase 6 or Phases 7-11 until the
v2 research-design gates are approved. No full-run GPU submission before GATE 10.

## Phases (v2 numbering)

| Phase | Status | Notes |
|---|---|---|
| 0 Cluster recon | **Partial, not re-confirmed against v2 wording** | Facts in `docs/cluster.md` already satisfy v2's added caveats (don't assume node types/scratch path — we verified both directly). GPU-specific checks (nvidia-smi, compute-node internet, unshare on a compute node) still blocked on the Skipjack outage; test job **1987143** still queued on `l40s` as of last check. |
| 1 Repo, reproducibility, schema | **In progress — GATE 1 (schema freeze) pending** | Repo skeleton, `pyproject.toml`, pre-commit, SLURM template, `configs/models.yaml` done (v1 pass). v2 schema migration done as infra prep: `src/secreg/schemas.py`, `docs/data_schema.md`, `configs/{conditions,cwes}.yaml` rewritten to v2; `src/secreg/stats.py` (Wilson CI + hierarchical bootstrap) and `src/secreg/utils/identity.py` (`state_id`, identification rule) added; the two GATE-1-mandated unit tests pass (`tests/test_stats.py`). 11/11 tests pass, ruff clean, both locally and (pre-v2) on the Skipjack login node — **the v2 code has not yet been re-synced/re-tested on Skipjack**. Not done: `[gpu]` extra install, model downloads, GPU smoke test (need a GPU node). |
| 2 Tasks & oracles | Not started | Alfonso-owned (H1 v2). v2 narrows the pilot to CWE-89 + CWE-22, 5-10 tasks each, before any wider CWE set. |
| 3-12 | Not started | Held per v2 stage gates; Phase 6 full-scale and Phases 7-11 require GATE 6A/10 first. |

## Open handoffs

None yet (H1 v2 not started).

## Blockers

- **Skipjack cluster outage** (observed 2026-11-20, ~12:50-14:55 local, last checked
  still ongoing): essentially all compute nodes across every GPU partition are
  `DOWN+NOT_RESPONDING`. Not account-specific. No ETA from this side.
- **GATE 1 (schema freeze) not yet approved by the user.** The v2 schema rewrite
  (`src/secreg/schemas.py`, `docs/data_schema.md`, conditions/cwes configs, the two
  mandated unit tests) is drafted and passing, but per `PLAN.md` v2 §2 this needs
  explicit sign-off before any v2 handoff (H1 v2 onward) is produced.

## Next steps

1. Get explicit user sign-off on GATE 1 (schema freeze) for the v2 schema rewrite.
2. Re-sync the updated repo to Skipjack and re-run the test suite there (last sync
   predates the v2 revision).
3. Once Skipjack nodes recover: finish the remaining Phase 0 v2 verification items,
   then Phase 1 GPU tasks (env install, model downloads, GPU smoke test).
4. Decide with the user how/when to start Phase 2 (Alfonso-owned: CWE-89/CWE-22
   pilot tasks and oracles) given there is currently only one executing agent.
