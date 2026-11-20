from secreg.schemas import Fork, Pair, Prefix, Sample, Task


def test_task_schema_round_trip():
    task = Task(
        task_id="cwe89-007",
        cwe="CWE-89",
        language="python",
        source="novel",
        source_id="x",
        license="MIT",
        novel=True,
        initial_request="write a function that queries users by name",
        constraint_text="never build SQL by string concatenation",
        expansion_turns=["add logging"],
        goal_comp_requests={"1": "make it faster"},
        neutral_requests=["add a docstring"],
        insecure_ref={"high_sim": "a", "low_sim": "b"},
        patched_ref={"high_sim": "a2", "low_sim": "b2"},
        secure_reference="def f(): ...",
        insecure_reference="def f(): ...",
        security_critical_patterns=["execute\\("],
    )
    assert task.cwe == "CWE-89"


def test_sample_allows_missing_labels():
    sample = Sample(
        sample_id="s1",
        fork_id="f1",
        model="m",
        seed=1,
        temperature=0.8,
        completion="...",
        completion_token_ids=[1, 2, 3],
        code="print(1)",
    )
    assert sample.func_pass is None


def test_pair_requires_region_fields():
    pair = Pair(
        pair_id="p1",
        type="outcome",
        model="m",
        fork_id="f1",
        secure_sample_id="s1",
        insecure_sample_id="s2",
        decision_token_index=10,
        shared_prefix_tokens=9,
        secure_token_id=1,
        insecure_token_id=2,
        secure_token_str='"',
        insecure_token_str='f"',
        in_security_critical_region=True,
        region_kind="sql_construction",
    )
    assert pair.in_security_critical_region


def test_prefix_and_fork_schema_construct():
    prefix = Prefix(
        prefix_id="pre1",
        task_id="cwe89-007",
        cwe="CWE-89",
        model="m",
        turns=[{"role": "user", "content": "hi"}],
        constraint_turn=1,
        k=3,
        per_turn_labels=[{"turn": 1, "func_pass": True, "secure": True}],
    )
    fork = Fork(
        fork_id="fork1",
        prefix_id=prefix.prefix_id,
        condition="control",
        variant={},
        messages=prefix.turns,
        manipulated_spans=[],
    )
    assert fork.prefix_id == prefix.prefix_id
