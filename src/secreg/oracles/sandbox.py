"""Isolated execution of generated code. `code` may be a single file or a
repo-state dict (v2 oracle contract, PLAN_alfonso.md v2 H1).

Owner: Alfonso (PLAN.md v2 Phase 2 task 5 / PLAN_alfonso.md v2 H1). Two
backends are specified: `docker` (Alfonso's local machine) and
`subprocess+unshare` (Skipjack has no Apptainer — confirmed in
docs/cluster.md — so this is the only cluster backend so far; `unshare`
itself is still unverified on a compute node due to the outage — PLAN.md v2
§1 task 4 explicitly warns not to assume it works). Not implemented yet.
"""

from __future__ import annotations


def run_sandboxed(code: str, backend: str, timeout_s: float = 10.0) -> dict:
    raise NotImplementedError(
        "secreg.oracles.sandbox is owned by Alfonso (PLAN.md Phase 2 task 6). "
        "Cluster backend must be 'subprocess+unshare' (no Apptainer on Skipjack)."
    )
