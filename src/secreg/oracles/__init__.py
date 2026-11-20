"""Executable functional + security oracles.

Owner: Alfonso (PLAN.md Phase 2 / PLAN_alfonso.md H1). Not implemented yet —
this is a structural placeholder so the rest of the codebase can import the
contract. Do not implement oracle logic from the GPU-owner side; consume H1
once delivered (src/secreg/oracles/*, configs/cwes.yaml, data/tasks/tasks.jsonl).
"""

from __future__ import annotations

from typing import Any, TypedDict


class OracleResult(TypedDict):
    func_pass: bool
    secure: bool
    func_details: dict[str, Any]
    security_details: dict[str, Any]
    semgrep_findings: list[dict[str, Any]]
    error: str | None
    runtime_s: float


def evaluate(task_id: str, code: str, timeout_s: float = 10.0) -> OracleResult:
    """Contract defined in PLAN.md Phase 2 / PLAN_alfonso.md H1. Awaiting H1 handoff."""
    raise NotImplementedError(
        "secreg.oracles.evaluate is owned by Alfonso (H1, PLAN.md Phase 2). "
        "Not yet delivered — see docs/STATUS.md."
    )
