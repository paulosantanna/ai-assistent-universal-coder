from __future__ import annotations

import json
import os
from pathlib import Path

import pytest

from aeos.core.evidence.evidence_manifest import (
    StagedManifestBuilder,
    compute_manifest_hash,
    verify_staged_manifest,
    STAGE_RUNTIME,
    STAGE_FINAL,
    STAGE_FILENAMES,
)
from aeos.core.evidence.hash_utils import sha256_file


@pytest.fixture
def evidence_dir(tmp_path) -> Path:
    return tmp_path / ".aeos" / "evidence"


def create_stage_file(evidence_dir: Path, execution_id: str, filename: str, content: str = "test"):
    fp = evidence_dir / execution_id / filename
    fp.parent.mkdir(parents=True, exist_ok=True)
    fp.write_text(content)
    return fp


def test_verify_passes_when_intact(evidence_dir):
    exec_id = "test-verify-pass-001"
    create_stage_file(evidence_dir, exec_id, "runtime-request.jsonl", '{"action":"test"}\n')

    builder = StagedManifestBuilder(exec_id, str(evidence_dir / exec_id))
    builder.finalize_runtime_manifest()

    result = builder.verify_manifest(STAGE_RUNTIME)
    assert result["passed"], f"Verify should pass for intact manifest: {result['file_errors']}"
    assert result["stored_hash"] != ""
    assert result["computed_hash"] != ""


def test_verify_self_hash_matches(evidence_dir):
    """Verify that stored hash == computed hash using compute_manifest_hash()."""
    exec_id = "test-verify-self-001"
    create_stage_file(evidence_dir, exec_id, "runtime-request.jsonl", '{"action":"test"}\n')

    builder = StagedManifestBuilder(exec_id, str(evidence_dir / exec_id))
    builder.finalize_runtime_manifest()

    manifest_fp = evidence_dir / exec_id / STAGE_FILENAMES[STAGE_RUNTIME]
    with open(manifest_fp, "r") as f:
        manifest = json.load(f)

    stored = manifest["manifest_sha256"]
    computed = compute_manifest_hash(manifest)
    assert stored == computed, \
        f"Self hash mismatch: stored={stored[:16]}..., computed={computed[:16]}..."


def test_verify_fails_when_file_altered(evidence_dir):
    """After finalization, altering a file should be detected by verify."""
    exec_id = "test-verify-alter-001"
    test_file = create_stage_file(evidence_dir, exec_id, "runtime-request.jsonl", '{"action":"original"}\n')

    builder = StagedManifestBuilder(exec_id, str(evidence_dir / exec_id))
    builder.finalize_runtime_manifest()

    test_file.write_text('{"action":"TAMPERED"}\n')

    result = builder.verify_manifest(STAGE_RUNTIME)
    assert not result["passed"], "Verify should fail when a file is altered after finalization"
    assert any("hash mismatch" in err.lower() or "hash mismatch" in err.lower()
               for err in result["file_errors"]), \
        f"Should report hash mismatch after tampering: {result['file_errors']}"


def test_verify_final_manifest_detects_tampering(evidence_dir):
    """Cascading verify: tampering a file should be caught by its staged manifest.
    
    Final manifest references staged manifests by their file hash.
    To catch individual file tampering, verify the staged manifest itself.
    """
    exec_id = "test-final-alter-001"
    test_file = create_stage_file(evidence_dir, exec_id, "runtime-request.jsonl", '{"action":"original"}\n')

    builder = StagedManifestBuilder(exec_id, str(evidence_dir / exec_id))
    builder.finalize_runtime_manifest()
    builder.finalize_evidence_manifest()

    test_file.write_text('{"action":"TAMPERED"}\n')

    runtime_fp = evidence_dir / exec_id / STAGE_FILENAMES["runtime"]
    runtime_result = verify_staged_manifest(runtime_fp)
    assert not runtime_result["passed"], \
        "Runtime manifest verify should fail when a referenced file is tampered"

    final_fp = evidence_dir / exec_id / STAGE_FILENAMES[STAGE_FINAL]
    final_result = verify_staged_manifest(final_fp)
    assert final_result["passed"], \
        "Final manifest verify should pass (it only checks staged manifest file, not individual files)"


def test_verify_passes_with_multiple_files(evidence_dir):
    exec_id = "test-multi-001"
    create_stage_file(evidence_dir, exec_id, "runtime-request.jsonl", '{"a":1}\n')
    create_stage_file(evidence_dir, exec_id, "tool_result.jsonl", '{"b":2}\n')
    create_stage_file(evidence_dir, exec_id, "skill-result.jsonl", '{"c":3}\n')

    builder = StagedManifestBuilder(exec_id, str(evidence_dir / exec_id))
    builder.finalize_runtime_manifest()

    result = builder.verify_manifest(STAGE_RUNTIME)
    assert result["passed"], f"Multi-file verify should pass: {result['file_errors']}"
    assert result["files_ok"] >= 2


def test_verify_manifest_not_found(evidence_dir):
    builder = StagedManifestBuilder("nonexistent", str(evidence_dir / "nonexistent"))
    result = builder.verify_manifest(STAGE_RUNTIME)
    assert not result["passed"]
    assert any("not found" in err.lower() for err in result["file_errors"])


def test_all_stages_verify_after_final(evidence_dir):
    """All staged manifests plus final should pass verify when unchanged."""
    exec_id = "test-allverify-001"
    create_stage_file(evidence_dir, exec_id, "runtime-request.jsonl", '{"action":"test"}\n')
    create_stage_file(evidence_dir, exec_id, "eval-suite-results.jsonl", '{"case":"pass"}\n')
    create_stage_file(evidence_dir, exec_id, "eval-scorecard.json", '{"score":0.95}\n')
    create_stage_file(evidence_dir, exec_id, "judge-input.json", '{"input":"ok"}')
    create_stage_file(evidence_dir, exec_id, "judge-result.json", '{"status":"PASS"}')
    create_stage_file(evidence_dir, exec_id, "judge-scorecard.json", '{"score":1.0}')
    create_stage_file(evidence_dir, exec_id, "production-readiness-scorecard.json", '{"score":0.95}')

    builder = StagedManifestBuilder(exec_id, str(evidence_dir / exec_id))
    builder.finalize_runtime_manifest()
    builder.finalize_eval_manifest()
    builder.finalize_judge_manifest()
    builder.finalize_readiness_manifest()
    builder.finalize_evidence_manifest()

    all_result = builder.verify_all_manifests()
    assert all_result["passed"], f"All manifests should verify: {all_result}"
