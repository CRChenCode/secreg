# Decision Log

Every 🛑 GATE outcome is appended here: date, options considered, choice, rationale.

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
