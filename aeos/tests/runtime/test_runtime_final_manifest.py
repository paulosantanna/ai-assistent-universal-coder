from __future__ import annotations

import json
from pathlib import Path

import pytest

from aeos.core.evidence.evidence_manifest import (
    StagedManifestBuilder,
    EvidenceManifestGenerator,
    verify_staged_manifest,
    compute_manifest_hash,
    STAGE_RUNTIME,
    STAGE_FINAL,
    STAGE_FILENAMES,
)
from aeos.core.evidence.hash_utils import sha256_file


@pytest.fixture
def evidence_dir(tmp_path) -> Path:
    return tmp_path / ".aeos" / "evidence"


def create_file(evidence_dir: Path, exec_id: str, name: str, content: str = "test"):
    fp = evidence_dir / exec_id / name
    fp.parent.mkdir(parents=True, exist_ok=True)
    fp.write_text(content)
    return fp


def test_runtime_final_manifest_generated_after_all_writes(evidence_dir):
    """Runtime manifest should be generated after all runtime evidence files are written."""
    exec_id = "test-runtime-final-001"
    create_file(evidence_dir, exec_id, "runtime-request.jsonl", '{"action":"run"}\n')
    create_file(evidence_dir, exec_id, "runtime-result.jsonl", '{"status":"PASS"}\n')
    create_file(evidence_dir, exec_id, "tool_decision.jsonl", '{"tool":"read"}\n')
    create_file(evidence_dir, exec_id, "tool_result.jsonl", '{"result":"data"}\n')
    create_file(evidence_dir, exec_id, "skill-result.jsonl", '{"skill":"scan"}\n')
    create_file(evidence_dir, exec_id, "hash-chain.jsonl", '{"index":0,"sha256":"abc"}\n')

    builder = StagedManifestBuilder(exec_id, str(evidence_dir / exec_id))
    out = builder.finalize_runtime_manifest()

    with open(out, "r") as f:
        manifest = json.load(f)

    file_names = [Path(fe["path"]).name for fe in manifest["files"]]
    assert "runtime-request.jsonl" in file_names, \
        f"Should include runtime-request.jsonl: got {file_names}"
    assert "runtime-result.jsonl" in file_names
    assert "hash-chain.jsonl" in file_names
    assert len(manifest["files"]) >= 5, \
        f"Runtime manifest should include 5+ files: got {len(manifest['files'])}"


def test_runtime_manifest_verifies_after_finalization(evidence_dir):
    """Runtime manifest should pass verify after all runtime files are written."""
    exec_id = "test-runtime-verify-001"
    create_file(evidence_dir, exec_id, "runtime-request.jsonl", '{"action":"test"}\n')
    create_file(evidence_dir, exec_id, "hash-chain.jsonl", '{"index":0,"sha256":"abc"}\n')

    builder = StagedManifestBuilder(exec_id, str(evidence_dir / exec_id))
    builder.finalize_runtime_manifest()

    result = builder.verify_manifest(STAGE_RUNTIME)
    assert result["passed"], f"Runtime manifest verify should pass: {result['file_errors']}"
    assert result["files_ok"] >= 2


def test_runtime_manifest_detects_post_finalize_tampering(evidence_dir):
    """Runtime manifest verify should detect file changes after finalization."""
    exec_id = "test-runtime-tamper-001"
    rf = create_file(evidence_dir, exec_id, "runtime-request.jsonl", '{"action":"original"}\n')

    builder = StagedManifestBuilder(exec_id, str(evidence_dir / exec_id))
    builder.finalize_runtime_manifest()

    rf.write_text('{"action":"TAMPERED"}\n')

    result = builder.verify_manifest(STAGE_RUNTIME)
    assert not result["passed"], "Verify should detect post-finalize file tampering"
    assert any("hash mismatch" in err.lower() for err in result["file_errors"])


def test_runtime_manifest_is_deterministic(evidence_dir):
    """Same files should produce same manifest hash."""
    exec_id = "test-runtime-det-001"
    create_file(evidence_dir, exec_id, "runtime-request.jsonl", '{"action":"deterministic"}\n')
    create_file(evidence_dir, exec_id, "tool_result.jsonl", '{"result":"same"}\n')

    builder = StagedManifestBuilder(exec_id, str(evidence_dir / exec_id))
    p1 = builder.finalize_runtime_manifest()

    clean_dir = evidence_dir / exec_id
    for f in clean_dir.iterdir():
        f.unlink()

    create_file(evidence_dir, exec_id, "runtime-request.jsonl", '{"action":"deterministic"}\n')
    create_file(evidence_dir, exec_id, "tool_result.jsonl", '{"result":"same"}\n')

    builder2 = StagedManifestBuilder(exec_id, str(evidence_dir / exec_id))
    p2 = builder2.finalize_runtime_manifest()

    with open(p1, "r") as f:
        m1 = json.load(f)
    with open(p2, "r") as f:
        m2 = json.load(f)

    assert m1["manifest_sha256"] == m2["manifest_sha256"], \
        "Same input files must produce same manifest hash"


def test_full_pipeline_manifest_chain(evidence_dir):
    """Test A-E lifecycle in sequence for a full pipeline execution."""
    exec_id = "test-pipeline-001"
    create_file(evidence_dir, exec_id, "runtime-request.jsonl", '{"action":"pipeline"}\n')
    create_file(evidence_dir, exec_id, "tool_result.jsonl", '{"result":"ok"}\n')
    create_file(evidence_dir, exec_id, "hash-chain.jsonl", '{"index":0}\n')

    builder = StagedManifestBuilder(exec_id, str(evidence_dir / exec_id))

    a = builder.finalize_runtime_manifest()
    assert Path(a).exists()
    assert verify_staged_manifest(Path(a))["passed"]

    create_file(evidence_dir, exec_id, "eval-suite-results.jsonl", '{"case":"pass"}\n')
    create_file(evidence_dir, exec_id, "eval-scorecard.json", '{"score":0.95}\n')
    b = builder.finalize_eval_manifest()
    assert Path(b).exists()
    assert verify_staged_manifest(Path(b))["passed"]

    create_file(evidence_dir, exec_id, "judge-input.json", '{"input":"ok"}')
    create_file(evidence_dir, exec_id, "judge-result.json", '{"status":"PASS"}')
    create_file(evidence_dir, exec_id, "judge-scorecard.json", '{"score":1.0}')
    c = builder.finalize_judge_manifest()
    assert Path(c).exists()
    assert verify_staged_manifest(Path(c))["passed"]

    create_file(evidence_dir, exec_id, "production-readiness-scorecard.json", '{"score":0.95}')
    d = builder.finalize_readiness_manifest()
    assert Path(d).exists()
    assert verify_staged_manifest(Path(d))["passed"]

    e = builder.finalize_evidence_manifest()
    assert Path(e).exists()
    assert verify_staged_manifest(Path(e))["passed"]

    all_ok = builder.verify_all_manifests()
    assert all_ok["passed"], f"Full pipeline manifest chain should verify: {all_ok}"
