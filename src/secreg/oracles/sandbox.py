"""Isolated execution of generated code.

Owner: Alfonso (PLAN.md Phase 2 task 6 / PLAN_alfonso.md H1). Two backends are
specified: `docker` (Alfonso's local machine) and `subprocess+unshare` (Skipjack
has no Apptainer — confirmed in docs/cluster.md — so this is the only cluster
backend). Not implemented yet.
"""

from __future__ import annotations


def run_sandboxed(code: str, backend: str, timeout_s: float = 10.0) -> dict:
    raise NotImplementedError(
        "secreg.oracles.sandbox is owned by Alfonso (PLAN.md Phase 2 task 6). "
        "Cluster backend must be 'subprocess+unshare' (no Apptainer on Skipjack)."
    )
