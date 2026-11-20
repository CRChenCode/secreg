#!/bin/bash
# Template SLURM job for secreg. Copy into a phase-specific .sbatch and fill
# in PARTITION/GRES/TIME/the python module to run. Reads account/scratch root
# from configs/cluster.yaml via scripts/_cluster_env.sh.
#
# Usage: sbatch slurm/pilot_baseline.sbatch  (or any script derived from this one)

#SBATCH --job-name=secreg-job
#SBATCH --account=yyao69_super
#SBATCH --qos=jhu
#SBATCH --partition=l40s           # override per job: l40s | a100 | h100 | h100-NVL=h100 | h200
#SBATCH --gres=gpu:1
#SBATCH --cpus-per-task=8
#SBATCH --mem=64G
#SBATCH --time=04:00:00            # keep <= 80% of the partition's wall-time limit (PLAN.md rule 5)
#SBATCH --output=/scratch/jhu/yyao69/cchen343/secreg/logs/%x-%j.out

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
source "${REPO_ROOT}/scripts/_cluster_env.sh"

echo "[secreg] job ${SLURM_JOB_ID} on $(hostname), partition ${SLURM_JOB_PARTITION:-unknown}"
nvidia-smi || true

# Activate environment (uv-managed venv on scratch; falls back to module-loaded conda).
if [ -f "${SCRATCH_ROOT}/venv/bin/activate" ]; then
    source "${SCRATCH_ROOT}/venv/bin/activate"
else
    module load anaconda3/2024.02-1
    conda activate secreg
fi

cd "${REPO_ROOT}"

# Replace the next line with the actual entry point for this job.
srun python -m secreg."$@"
