"""Canonical record schemas — v2.

Source of truth: PLAN.md v2 §2 (migration table) and PLAN_alfonso.md v2 §4
(field-by-field JSON examples). Keep all three in sync; bump
`SCHEMA_VERSION` on any field change and update `docs/data_schema.md` in the
same PR (PLAN.md v2 §13, "no silent schema change").

v1 is NOT compatible with v2 (PLAN_alfonso.md v2 §3.3 rule 3): a v1 payload
must be rejected, never coerced. These models intentionally use `extra="forbid"`
so a missing or renamed required field raises instead of silently validating.
"""

from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, ConfigDict

SCHEMA_VERSION = "2.0"

Outcome = Literal[
    "functional_secure", "functional_insecure", "nonfunctional", "refusal", "untestable"
]
Factor = Literal[
    "control",
    "goal_comp",
    "insecure_ref",
    "ctx_omit",
    "ctx_delete",
    "ctx_distance",
    "implicit_only",
]


class ChatTurn(BaseModel):
    model_config = ConfigDict(extra="forbid")
    role: str
    content: str


class InsecureRef(BaseModel):
    model_config = ConfigDict(extra="forbid")
    high_sim: str
    low_sim: str


class RefMatchChecks(BaseModel):
    model_config = ConfigDict(extra="forbid")
    length_ratio: float
    api_equivalent: bool
    diff_lines_security_only: bool


class Provenance(BaseModel):
    model_config = ConfigDict(extra="forbid")
    source: Literal["seccodeplt", "cweval", "novel"]
    source_id: str
    license: str
    novel: bool
    transformations: list[str] = []
    drafted_by: Literal["human", "llm"]
    reviewed_by: str
    reviewed_at: str


class LegitimateChangeSpec(BaseModel):
    model_config = ConfigDict(extra="forbid")
    turn_kind: Literal["expansion", "goal_comp", "neutral"]
    may_revise_invariant: bool


class Task(BaseModel):
    """tasks.jsonl — H1 v2, owned by Alfonso."""

    model_config = ConfigDict(extra="forbid")
    task_id: str
    cwe: str
    language: str
    initial_request: str
    constraint_text: str
    security_invariant: str
    invariant_scope: dict[str, list[str]]
    legitimate_change_spec: list[LegitimateChangeSpec]
    constraint_active_after_compaction: bool
    expansion_turns: list[str]
    neutral_requests: list[str]
    goal_comp_requests: dict[str, str]
    goal_comp_validation: dict[str, dict[str, Any]]
    insecure_ref: InsecureRef
    patched_ref: InsecureRef
    ref_match_checks: RefMatchChecks
    secure_reference: str
    insecure_reference: str
    security_critical_patterns: list[str]
    oracle_status: Literal["validated", "rejected", "pending"]
    func_and_security_tests_version: str
    provenance: Provenance


class PerTurnLabel(BaseModel):
    model_config = ConfigDict(extra="forbid")
    turn: int
    func_pass: bool
    secure: bool
    repo_state_hash: str
    invariant_valid: bool
    active_constraint_set: list[str]
    turn_label_status: Literal["validated", "pending", "excluded"]


class Prefix(BaseModel):
    """prefix.jsonl v2 — GPU owner, Phase 4."""

    model_config = ConfigDict(extra="forbid")
    prefix_id: str
    task_id: str
    cwe: str
    model: str
    model_revision: str
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


class ManipulationCheck(BaseModel):
    model_config = ConfigDict(extra="forbid")
    token_count_delta_vs_control: int
    securely_satisfiable: bool
    diff_summary: str
    reviewer: str
    reviewer_judgment: Literal["pass", "fail", "compound"]
    notes: str = ""


class Fork(BaseModel):
    """fork.jsonl v2 — Alfonso's make_contrasts (H3 v2), run by the GPU owner."""

    model_config = ConfigDict(extra="forbid")
    fork_id: str
    prefix_id: str
    task_id: str
    contrast_id: str
    matched_control_fork_id: str | None  # null on control forks
    factor: Factor
    variant: dict[str, Any]
    compound: bool
    messages: list[ChatTurn]
    manipulated_spans: list[ManipulatedSpan]
    semantic_anchor_ids: list[str]
    active_constraint_set: list[str]
    invariant_applies: bool
    prompt_token_hash: str
    prompt_token_count: int
    manipulation_check: ManipulationCheck


class Sample(BaseModel):
    """sample.jsonl v2 — raw from the GPU owner (H4); no label fields here."""

    model_config = ConfigDict(extra="forbid")
    sample_id: str
    fork_id: str
    model: str
    model_revision: str
    seed: int
    decoding_id: str
    completion: str
    completion_token_ids: list[int]
    finish_reason: str
    generation_status: Literal["ok", "error", "truncated"]
    code: str | dict[str, str]
    final_repo_state_hash: str
    oracle_eval_target: Literal["file", "repo_state"]


class OracleResult(BaseModel):
    """Return shape of secreg.oracles.evaluate (H1 v2 contract)."""

    model_config = ConfigDict(extra="forbid")
    func_pass: bool | None
    security_test_pass: bool | None
    outcome: Outcome
    details: dict[str, Any]
    runtime_s: float
    error: str | None
    test_version: str


class LabeledSample(Sample):
    """H5 v2: Sample fields + oracle result + regression_eligible."""

    model_config = ConfigDict(extra="forbid")
    outcome: Outcome
    details: dict[str, Any]
    test_version: str
    regression_eligible: bool


class ContextPair(BaseModel):
    """context_pairs.jsonl — H5 v2. The primary causal-comparison unit."""

    model_config = ConfigDict(extra="forbid")
    context_pair_id: str
    contrast_id: str
    task_id: str
    prefix_id: str
    control_fork_id: str
    manipulated_fork_id: str
    model: str
    split: Literal["train", "calibration", "test"]
    effect_estimate: float
    effect_ci: tuple[float, float]
    eligible_for_mechanism: bool
    selection_reason: str


class OutcomePair(BaseModel):
    """outcome_pairs.jsonl — H5 v2. Localization/illustration ONLY.

    The identification rule (PLAN.md v2 §0) forbids using these to contrast
    pre-divergence hidden states: two completions sharing an exact token
    prefix have identical hidden states before the first divergent token,
    regardless of which token is later sampled. Never train an outcome
    probe or patch "secure into insecure" at the shared prefix position
    using these records.
    """

    model_config = ConfigDict(extra="forbid")
    outcome_pair_id: str
    fork_id: str
    secure_sample_id: str
    insecure_sample_id: str
    first_divergence_index: int
    shared_prefix_tokens: int


class Region(BaseModel):
    """regions.jsonl — H5 v2. The first divergent token is a candidate only."""

    model_config = ConfigDict(extra="forbid")
    region_id: str
    sample_id: str
    region_kind: str
    token_span: tuple[int, int]
    ast_span: dict[str, Any]
    reliability: Literal["high", "low"]
    invariant_ref: str
    candidate_anchor: str
    alignment_method: Literal["ast", "regex", "manual"]
    valid_comparison: bool
    decision_token_role: Literal["candidate", "non_security", "unknown"]


class TokenizationCheck(BaseModel):
    model_config = ConfigDict(extra="forbid")
    secure_ids: list[int]
    insecure_ids: list[int]
    single_token: bool
    first_token_distinct: bool


class Fixture(BaseModel):
    """H5b v2 — decision-region fixtures (Alfonso → GPU). New in v2."""

    model_config = ConfigDict(extra="forbid")
    fixture_id: str
    context_pair_id: str
    task_id: str
    continuation_prefix: str
    secure_alternative: str
    insecure_alternative: str
    functional_equivalence_check: Literal["pass", "fail"]
    tokenization: dict[str, TokenizationCheck]  # keyed by model id
    scoring: Literal["single_token_dlogit", "sequence_logprob"]
    status: Literal["supported", "unsupported"]
    unsupported_reason: str | None


RECORD_MODELS: dict[str, type[BaseModel]] = {
    "tasks": Task,
    "prefix": Prefix,
    "fork": Fork,
    "sample": Sample,
    "labeled_sample": LabeledSample,
    "context_pair": ContextPair,
    "outcome_pair": OutcomePair,
    "region": Region,
    "fixture": Fixture,
}
