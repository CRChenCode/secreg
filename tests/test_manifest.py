from secreg.utils.manifest import build_manifest, read_manifest
from secreg.utils.verify_handoff import verify_handoff


def test_build_and_verify_handoff(tmp_path):
    (tmp_path / "shard-0000.jsonl").write_text('{"a": 1}\n{"a": 2}\n')
    build_manifest(
        tmp_path,
        handoff_id="H-test-v2",
        producer="gpu-owner",
        consumer="alfonso",
        schema_version="2.0",
    )
    manifest = read_manifest(tmp_path)
    assert manifest["files"][0]["records"] == 2
    assert verify_handoff(tmp_path) == []


def test_verify_handoff_detects_tamper(tmp_path):
    (tmp_path / "shard-0000.jsonl").write_text('{"a": 1}\n')
    build_manifest(
        tmp_path,
        handoff_id="H-test-v2",
        producer="gpu-owner",
        consumer="alfonso",
        schema_version="2.0",
    )
    (tmp_path / "shard-0000.jsonl").write_text('{"a": 999}\n')
    problems = verify_handoff(tmp_path)
    assert problems and "sha256 mismatch" in problems[0]
