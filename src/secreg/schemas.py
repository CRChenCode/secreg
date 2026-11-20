"""Canonical record schemas (pydantic). Source of truth: PLAN.md section 2 and
docs/data_schema.md — keep those two in sync with this file. Bump
`schema_version` on any field change (PLAN.md Agent Behavior Constraints #7).
"""

from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, ConfigDict

SCHEMA_VERSION = "1.0"


class ChatTurn(BaseModel):
    model_config = ConfigDict(extra="forbid")
    role: str
    content: str


class InsecureRef(BaseModel):
    model_config = ConfigDict(extra="forbid")
    high_sim: str
    low_sim: str


class Task(BaseModel):
    """tasks.jsonl — H1, owned by Alfonso."""

    model_config = ConfigDict(extra="forbid")
    task_id: str
    cwe: str
    language: str
    source: Literal["seccodeplt", "cweval", "novel"]
    source_id: str
    license: str
    novel: bool
    initial_request: str
    constraint_text: str
    expansion_turns: list[str]
    goal_comp_requests: dict[str, str]
    neutral_requests: list[str]
    insecure_ref: InsecureRef
    patched_ref: InsecureRef
    secure_reference: str
    insecure_reference: str
    security_critical_patterns: list[str]


class PerTurnLabel(BaseModel):
    model_config = ConfigDict(extra="forbid")
    turn: int
    func_pass: bool
    secure: bool


class Prefix(BaseModel):
    """prefix.jsonl — produced by the GPU owner, Phase 4."""

    model_config = ConfigDict(extra="forbid")
    prefix_id: str
    task_id: str
    cwe: str
    model: str
    turns: list[ChatTurn]
    constraint_turn: int
    k: int
    per_turn_labels: list[PerTurnLabel]


class ManipulatedSpan(BaseModel):
    model_config = ConfigDict(extra="forbid")
    turn: int
    char_start: int
    char_end: int
    kind: Literal["constraint", "filler", "insecure_ref", "goal_request", "summary", "code"]


class Fork(BaseModel):
    """fork.jsonl — produced by Alfonso's make_forks, run by the GPU owner."""

    model_config = ConfigDict(extra="forbid")
    fork_id: str
    prefix_id: str
    condition: str
    variant: dict[str, Any]
    messages: list[ChatTurn]
    control_of: str | None = None
    manipulated_spans: list[ManipulatedSpan]


class Sample(BaseModel):
    """sample.jsonl — raw from the GPU owner (H4); labels added by Alfonso (H5).

    Label fields are optional because raw shards omit them entirely.
    """

    model_config = ConfigDict(extra="forbid")
    sample_id: str
    fork_id: str
    model: str
    seed: int
    temperature: float
    completion: str
    completion_token_ids: list[int]
    code: str
    func_pass: bool | None = None
    secure: bool | None = None
    oracle_details: dict[str, Any] | None = None
    semgrep_findings: list[dict[str, Any]] | None = None


class Pair(BaseModel):
    """pair.jsonl — H5, Alfonso."""

    model_config = ConfigDict(extra="forbid")
    pair_id: str
    type: Literal["outcome", "condition"]
    model: str
    fork_id: str
    secure_sample_id: str
    insecure_sample_id: str
    decision_token_index: int
    shared_prefix_tokens: int
    secure_token_id: int
    insecure_token_id: int
    secure_token_str: str
    insecure_token_str: str
    in_security_critical_region: bool
    region_kind: Literal["sql_construction", "file_path", "subprocess", "credential"] | None = None


RECORD_MODELS: dict[str, type[BaseModel]] = {
    "tasks": Task,
    "prefix": Prefix,
    "fork": Fork,
    "sample": Sample,
    "pair": Pair,
}
