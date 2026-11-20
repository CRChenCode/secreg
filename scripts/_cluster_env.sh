#!/bin/bash
# Sourced by slurm/_template.sbatch and interactive sessions. Exports cache
# paths onto scratch per PLAN.md section 1 rule 3 — never let these default
# onto $HOME.

export SCRATCH_ROOT="${SCRATCH_ROOT:-/scratch/jhu/yyao69/cchen343/secreg}"
export HF_HOME="${HF_HOME:-${SCRATCH_ROOT}/hf}"
export VLLM_CACHE_ROOT="${VLLM_CACHE_ROOT:-${SCRATCH_ROOT}/vllm_cache}"
export TRITON_CACHE_DIR="${TRITON_CACHE_DIR:-${SCRATCH_ROOT}/triton_cache}"
export TORCH_HOME="${TORCH_HOME:-${SCRATCH_ROOT}/torch_home}"
export SECREG_LOGS="${SECREG_LOGS:-${SCRATCH_ROOT}/logs}"

mkdir -p "$HF_HOME" "$VLLM_CACHE_ROOT" "$TRITON_CACHE_DIR" "$TORCH_HOME" "$SECREG_LOGS"
