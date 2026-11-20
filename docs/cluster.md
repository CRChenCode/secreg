# Phase 0 — Cluster Reconnaissance (JHU ARCH Skipjack)

Status: **PARTIAL — blocked on a cluster-wide node outage.** See "Blocker" below.
Machine-readable facts are in `configs/cluster.yaml`.

## Access
- `ssh cchen343@login.arch.jhu.edu` (key-based, already configured as SSH host `skipjack`).
- SLURM account: `yyao69_super`. QOS: `jhu` (MaxTRESPU `gres/gpu=16` — i.e. at most 16 GPUs in flight at once under this QOS).
- Other QOS exist on the cluster (`jhu2` gres/gpu=32, `jhu4` gres/gpu=64, `a100_condo`, `h200_condo`, …) but `sacctmgr show assoc user=cchen343` only lists `yyao69_super / (any partition) / jhu` — we are not associated with the higher-GPU QOS or any condo QOS. If more concurrent GPU budget is needed later, the PI must request it from ARCH.

## Partitions / node types
| node-type | SLURM partition | gres string | nodes | default walltime |
|---|---|---|---|---|
| l40s | `l40s` | `gpu:l40s:8` | 8 | 3-00:00:00 |
| a100 | `a100` | `gpu:a100:8` | 13 | 3-00:00:00 |
| h100 | `h100` | `gpu:h100:4` | 32 | 3-00:00:00 |
| h200 | `h200` | `gpu:h200:4` | 6 | 3-00:00:00 |
| rtx6000 | `rtx6000` | `gpu:rtx_pro_6000:4` or `:8` | 3 | 3-00:00:00 |
| b200 / b300 | `b200` / `b300` | `gpu:b200:8` / `gpu:b300:8` | 16 / 17 | 3-00:00:00 |
| interactive_gpu | `interactive_gpu` | `gpu:2g.20gb:24` (MIG slices) | 2 | 4:00:00 |

GPU request syntax: `--gres=gpu:<n>` (and, per-type, `--gres=gpu:<type>:<n>`) is accepted by the scheduler — confirmed from the submitted test job's `TresPerNode=gres/gpu:1`. `--gpus` was not tested; no need to, since `--gres` works.

## Storage
- Home: `/home/jhu/cchen343`, mounted via weka (`wekafs1/homejhu`), 94G total / 11G used shared across the whole `/weka/home/jhu` tree — **code and configs only**, per plan.
- Scratch: `/scratch/jhu/yyao69` is the PI-level directory (owned by user/group `yyao69`). Created `scratch_root = /scratch/jhu/yyao69/cchen343/secreg` for this project (with a `logs/` subdir). Whole-cluster scratch fs is 4.5P, 9% used — no near-term pressure.
- `/projects` not checked (not needed yet; mounts on demand per plan, do not `ls` it directly).

## Software environment
- No `apptainer` / `singularity` anywhere in the Lmod tree (`module spider` finds neither) → **sandbox backend must be `subprocess+unshare`**, not Apptainer, contradicting nothing in the plan (it's listed as the fallback) but ruling out the "preferred" containerized option.
- `unshare` binary exists on the login node (`/usr/bin/unshare`); `unshare -rn true` itself has **not** been verified on a compute node yet (outage — see below).
- No `uv` module; install it under `$HOME/.local` via pip or the official installer (both need internet, confirmed reachable from the login node). `anaconda3/2024.02-1` is available as a conda fallback if `uv` setup is awkward on compute nodes.
- Python versions available as modules: 3.8.6, 3.9.15, 3.11.9, 3.13.13. Will target 3.11 unless a dependency forces otherwise.
- Login-node internet: confirmed (`huggingface.co` → 200, `pypi.org` → 200). **Compute-node internet is unverified** (see blocker).

## Blocker: cluster-wide outage at recon time (2026-11-20, ~12:50–14:55 local)
`sinfo -N -l` shows essentially the entire cluster — every GPU partition (`l40s`, `a100`, `h100`, `h200`, `rtx6000`, `b200`, `b300`, `interactive_gpu`) and most CPU nodes — in state `down*`/`DOWN+NOT_RESPONDING`, with `Reason=Not responding [slurm@2026-11-20T12:50:4x]` on every node checked. Only 4 CPU nodes (`ccl129/141/178/184`, partition `low`) show `idle`, and only 1 job cluster-wide was in state `R` (running) at the time I queried. The job queue (`squeue`) has hundreds of pending jobs from many different users/accounts stuck on `ReqNodeNotAvail` — this is not specific to our account, QOS, or job; it looks like a fabric/slurmd-communication incident affecting the whole scheduler fleet, starting a couple of hours before this recon.

I submitted the required 5-minute GPU test job anyway (`sbatch logs/test_gpu.sbatch`, job **1987143**, partition `l40s`, requests `--gres=gpu:1`, 4 CPUs, 16G mem, 5 min walltime) — it is queued (`PD`, reason `ReqNodeNotAvail`) and will run automatically once `l40s` nodes come back; its log will land at `logs/secreg-recon-1987143.out`. I did not escalate to ARCH support — that's a call for the human (PI/user) to make, since it may already be a known, tracked incident.

**Consequently, these Phase 0 acceptance-criteria items are still open:**
- `nvidia-smi` works on a compute node
- compute-node internet access (huggingface.co / pypi.org)
- `/tmp` and `$TMPDIR` size on a compute node
- `unshare -rn true` and `apptainer exec ...` behavior on a compute node (apptainer is already confirmed absent via modules, so this will just double-check `unshare`)

## Sandbox approach (provisional, pending the above)
`subprocess+unshare` is the only sandbox backend available on Skipjack (no Apptainer). This matches the plan's documented fallback, so Phase 2's `sandbox.py` should implement that backend first for the cluster side, with `docker` for Alfonso's local machine.

## Next steps
Everything above that isn't marked "unverified" is final — GATE 0 can be answered now for the account/partition/storage/software facts. The GPU-specific smoke-test facts need the cluster to recover (or an ARCH status check). Recommend: proceed with Phase 1 repo-skeleton work now (no GPU required), and let job 1987143 complete in the background to close out the remaining Phase 0 items.
