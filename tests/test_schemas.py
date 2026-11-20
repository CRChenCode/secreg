from secreg.schemas import ContextPair, Fork, OutcomePair, Prefix, Sample, Task


def _task_kwargs(**overrides):
    base = dict(
        task_id="cwe89-007",
        cwe="CWE-89",
        language="python",
        initial_request="write a function that queries users by name",
        constraint_text="never build SQL by string concatenation",
        security_invariant="All SQL values reaching the DB driver are parameter-bound.",
        invariant_scope={"functions": ["get_user"], "files": ["db.py"]},
        legitimate_change_spec=[{"turn_kind": "expansion", "may_revise_invariant": False}],
        constraint_active_after_compaction=True,
        expansion_turns=["add logging"],
        neutral_requests=["add a docstring"],
        goal_comp_requests={"1": "make it faster"},
        goal_comp_validation={"1": {"securely_satisfiable": True, "secure_cost_note": "n/a"}},
        insecure_ref={"high_sim": "a", "low_sim": "b"},
        patched_ref={"high_sim": "a2", "low_sim": "b2"},
        ref_match_checks={
            "length_ratio": 1.02,
            "api_equivalent": True,
            "diff_lines_security_only": True,
        },
        secure_reference="def f(): ...",
        insecure_reference="def f(): ...",
        security_critical_patterns=["execute\\("],
        oracle_status="validated",
        func_and_security_tests_version="2026-12-01.a",
        provenance={
            "source": "novel",
            "source_id": "x",
            "license": "MIT",
            "novel": True,
            "drafted_by": "human",
            "reviewed_by": "alfonso",
            "reviewed_at": "2026-12-01",
        },
    )
    base.update(overrides)
    return base


def test_task_v2_schema_round_trip():
    task = Task(**_task_kwargs())
    assert task.cwe == "CWE-89"
    assert task.oracle_status == "validated"


def test_task_rejects_v1_shape_missing_invariant():
    v1_style = _task_kwargs()
    del v1_style["security_invariant"]
    try:
        Task(**v1_style)
        raised = False
    except Exception:
        raised = True
    assert raised, "a v1-shaped task (missing security_invariant) must be rejected, not coerced"


def test_sample_v2_requires_no_label_fields():
    sample = Sample(
        sample_id="s1",
        fork_id="f1",
        model="m",
        model_revision="rev1",
        seed=1,
        decoding_id="d1",
        completion="...",
        completion_token_ids=[1, 2, 3],
        finish_reason="stop",
        generation_status="ok",
        code="print(1)",
        final_repo_state_hash="h1",
        oracle_eval_target="file",
    )
    assert sample.generation_status == "ok"


def test_outcome_pair_is_localization_only_by_construction():
    pair = OutcomePair(
        outcome_pair_id="op1",
        fork_id="f1",
        secure_sample_id="s1",
        insecure_sample_id="s2",
        first_divergence_index=412,
        shared_prefix_tokens=411,
    )
    # OutcomePair intentionally carries no activation/state fields — the
    # identification rule forbids using it to contrast pre-divergence states.
    assert not hasattr(pair, "activation") and not hasattr(pair, "hidden_state")


def test_context_pair_is_the_causal_unit():
    pair = ContextPair(
        context_pair_id="cp1",
        contrast_id="c1",
        task_id="cwe89-007",
        prefix_id="pre1",
        control_fork_id="fork_ctrl",
        manipulated_fork_id="fork_manip",
        model="m",
        split="train",
        effect_estimate=0.12,
        effect_ci=(0.03, 0.21),
        eligible_for_mechanism=True,
        selection_reason="significant effect in pilot",
    )
    assert pair.split == "train"


def test_prefix_and_fork_v2_schema_construct():
    prefix = Prefix(
        prefix_id="pre1",
        task_id="cwe89-007",
        cwe="CWE-89",
        model="m",
        model_revision="rev1",
        turns=[{"role": "user", "content": "hi"}],
        constraint_turn=1,
        k=3,
        per_turn_labels=[
            {
                "turn": 1,
                "func_pass": True,
                "secure": True,
                "repo_state_hash": "h0",
                "invariant_valid": True,
                "active_constraint_set": ["cwe89.param_binding"],
                "turn_label_status": "validated",
            }
        ],
    )
    fork = Fork(
        fork_id="fork_ctrl",
        prefix_id=prefix.prefix_id,
        task_id=prefix.task_id,
        contrast_id="c1",
        matched_control_fork_id=None,
        factor="control",
        variant={},
        compound=False,
        messages=prefix.turns,
        manipulated_spans=[],
        semantic_anchor_ids=["assistant_start"],
        active_constraint_set=["cwe89.param_binding"],
        invariant_applies=True,
        prompt_token_hash="hash1",
        prompt_token_count=100,
        manipulation_check={
            "token_count_delta_vs_control": 0,
            "securely_satisfiable": True,
            "diff_summary": "n/a (control fork)",
            "reviewer": "alfonso",
            "reviewer_judgment": "pass",
        },
    )
    assert fork.prefix_id == prefix.prefix_id
