"""Executable functional + security oracles (v2).

Owner: Alfonso (PLAN.md v2 Phase 2 / PLAN_alfonso.md v2 H1). Not implemented
yet — structural placeholder so the rest of the codebase can import the
contract. Do not implement oracle logic from the GPU-owner side; consume H1
v2 once delivered (src/secreg/oracles/*, configs/cwes.yaml, data/tasks/tasks.jsonl,
data/tasks/splits.json).

v2 changes from v1: `code` may be a single file or a repo-state dict (for
multi-file tasks / agent format); the return shape uses a 5-way `outcome`
enum instead of a boolean `secure` (untestable/refusal/nonfunctional are
never collapsed into "secure"); `regression_eligible` is NOT computed here —
`label_shards` derives it from fork metadata (task invariant scope +
legitimate_change_spec), since regression eligibility depends on context the
oracle itself does not see.
"""

from __future__ import annotations

from typing import Any, Literal, TypedDict

Outcome = Literal[
    "functional_secure", "functional_insecure", "nonfunctional", "refusal", "untestable"
]


class OracleResult(TypedDict):
    func_pass: bool | None
    security_test_pass: bool | None  # None when not testable
    outcome: Outcome
    details: dict[str, Any]
    runtime_s: float
    error: str | None
    test_version: str


def evaluate(task_id: str, code: str | dict[str, str], timeout_s: float = 10.0) -> OracleResult:
    """Contract defined in PLAN.md v2 §3 / PLAN_alfonso.md v2 H1. Awaiting H1 v2 handoff."""
    raise NotImplementedError(
        "secreg.oracles.evaluate is owned by Alfonso (H1 v2, PLAN.md v2 Phase 2). "
        "Not yet delivered — see docs/STATUS.md."
    )
