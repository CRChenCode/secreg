# Decision Log

Every 🛑 GATE outcome is appended here: date, options considered, choice, rationale.

## 2026-11-20 — PLAN.md / PLAN_alfonso.md revised to v2.0 (research-design rewrite)

The user replaced both plan files with a v2.0 scientific-design revision. Summary of
what changed and what it invalidates from the v1 scaffolding built earlier today:

- **Mechanism labels downgraded.** H-loss/H-readout/H-override are no longer preset
  diagnoses; they are optional shorthand over three continuous evidence dimensions —
  accessibility (A), constraint causal influence (I), competing-source influence (C) —
  used only when evidence supports them. Default is `mixed/indeterminate`.
- **New non-negotiable identification rule** (PLAN.md v2 §0): two completions sharing
  an exact token prefix have identical hidden states before the first divergent token.
  This forbids training an outcome probe or patching "secure→insecure" at `t*-1` using
  `outcome_pairs.jsonl` — those are now explicitly localization-only. The primary causal
  unit is `context_pairs.jsonl` (control vs. manipulated *prompt*, not secure vs.
  insecure *sample*).
- **Scope tightened**: feasibility pilot first — 1 dense model, CWE-89 + CWE-22 only,
  5-10 tasks/CWE, 4 pilot conditions (control, goal_comp, insecure_ref, ctx_omit),
  20-40 context pairs for mechanism work. Phase 6 full-scale and Phases 7-11 are held
  until the pilot go/no-go questions (PLAN.md v2 §0) are answered at GATE 6A/10.
  **No full-run GPU submission before GATE 10.**
- **Every schema changed**: tasks.jsonl gains `security_invariant`,
  `legitimate_change_spec`, `provenance`, etc.; fork.jsonl gains `contrast_id`,
  `matched_control_fork_id`, `factor`, `manipulation_check`; pair.jsonl splits into
  `context_pairs.jsonl` and `outcome_pairs.jsonl`; a new H5b (decision-region fixtures)
  is added; H6 keys activations by `state_id`/`anchor_id` instead of
  `sample_id`/`position_name`. **v1 payloads are rejected, never coerced.**
  `schema_version` bumped 1.0 → 2.0 everywhere.

**Action taken** (as the "Shared"/Phase-1 infra owner, not as Alfonso's domain work):
rewrote `src/secreg/schemas.py` to v2 (pydantic, `extra="forbid"`, so a v1-shaped
record raises instead of silently validating), `docs/data_schema.md`,
`configs/conditions.yaml` and `configs/cwes.yaml` (pilot CWE-89/CWE-22 + v2 factor
names), renamed `analysis/decision_token.py` → `analysis/candidate_regions.py`,
`gen/forks.make_forks` → `gen/forks.make_contrasts`, and updated every stub module's
docstring/contract to the v2 shape. Added `src/secreg/stats.py` (Wilson CI +
hierarchical task→prefix→sample bootstrap) and `src/secreg/utils/identity.py`
(`state_id`, enforcing the identification rule), plus the two unit tests PLAN.md v2 §2
mandates before GATE 1 (`tests/test_stats.py`): identification-rule equality, and
clustered bootstrap being substantially wider than a naive flat bootstrap under
task-correlated data. All 11 tests pass; ruff clean.

**Not done, and explicitly held per the plan's own rule**: no Alfonso-owned domain
content (oracle logic, task authoring, fork/contrast logic, probes) was written or
guessed at — those stubs were only updated to the new v2 *contracts* (signatures,
docstrings), never given an implementation.

**Open**: this *is* GATE 1 (schema freeze) territory — PLAN.md v2 §2 says "GPU owner
and Alfonso review the migration table... before downstream implementation." The
schema/infra rewrite above is the pre-gate preparation; it still needs the user's
explicit sign-off before any real v2 handoff (H1 v2 onward) is produced. GATE 0 from
the v1 pass (cluster recon) is also not re-confirmed against the v2 Phase 0 wording
(which adds: don't assume node types beyond what's actually allocated, don't assume
`/scratch/jhu/<PI>` without checking — both already satisfied by the existing
`docs/cluster.md`, but the user has not formally signed off on it as a GATE).

## 2026-11-20 — GATE 0 (partial) — Cluster recon under outage

**Options**: (a) wait for the cluster to recover before doing anything; (b) proceed
with Phase 1 non-GPU repo/environment scaffolding now, letting the queued GPU test
job (1987143) complete in the background; (c) escalate to ARCH support first.

**Choice**: (b). Proceed with Phase 1 repo skeleton / environment scaffolding; leave
job 1987143 queued; defer the remaining Phase 0 GPU-specific verification (nvidia-smi,
compute-node internet, `/tmp`/`$TMPDIR` size, `unshare -rn` on a compute node) until
the cluster recovers.

**Rationale**: the outage (recon time 2026-11-20 ~12:50–14:55 local) affects every GPU
partition and most of the cluster, is not specific to this account, and nothing about
it is actionable from this side beyond waiting — but Phase 1's repo/environment tasks
(skeleton, pyproject.toml, SLURM templates, configs/models.yaml) need no GPU node and
can proceed in parallel without any research-design risk.

## 2026-11-20 — Role split with a single executing agent

**Options**: (a) one agent does both GPU-owner and Alfonso-owned work; (b) strictly
GPU-owner work only, stop and report whenever an Alfonso-owned handoff (H1, H3, H7,
etc.) would be needed; (c) scaffold shared infrastructure only for now, decide the
Alfonso-owned domain work (oracles, tasks, forks, probes) later.

**Choice**: (c), for now. Built the full repo skeleton, canonical schemas
(`src/secreg/schemas.py`), handoff/manifest utilities, SLURM templates, and
`configs/models.yaml`. Left every Alfonso-owned module (`oracles/`, `tasks/`,
`gen/forks.py`, `analysis/probes.py`, …) as an explicit `NotImplementedError`
stub naming the owning phase/handoff, per `PLAN.md` Agent Behavior Constraint #6
("do not implement Alfonso-owned components").

**Rationale**: Phase 2 (seed tasks & oracles) is explicitly "the most critical
engineering" in the plan and needs human-reviewed domain judgment (CWE selection,
constraint text, novel-task authoring) that shouldn't be fabricated wholesale by
an agent without a decision point. Revisit this entry once the user decides whether
to proceed with Alfonso's work directly.
