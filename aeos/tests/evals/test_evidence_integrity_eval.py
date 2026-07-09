from __future__ import annotations

import json
from pathlib import Path

import pytest

from aeos.core.evidence.evidence_manifest import (
    StagedManifestBuilder,
    verify_staged_manifest,
    compute_manifest_hash,
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


def test_hash_mismatch_detected_on_tampered_file(evidence_dir):
    """Real hash mismatch should be detected when file content changes after finalization."""
    exec_id = "test-eval-realmismatch-001"
    test_file = create_file(evidence_dir, exec_id, "runtime-request.jsonl", '{"action":"original"}\n')

    builder = StagedManifestBuilder(exec_id, str(evidence_dir / exec_id))
    builder.finalize_runtime_manifest()

    test_file.write_text('{"action":"MODIFIED"}\n')

    result = verify_staged_manifest(evidence_dir / exec_id / STAGE_FILENAMES["runtime"])
    assert not result["passed"], "Should detect real hash mismatch after modification"
    file_errors = " ".join(result["file_errors"]).lower()
    assert "hash mismatch" in file_errors, \
        f"Should report hash mismatch: {result['file_errors']}"


def test_no_hash_mismatch_when_files_unchanged(evidence_dir):
    """No hash mismatch when files remain unchanged after finalization."""
    exec_id = "test-eval-nomismatch-001"
    create_file(evidence_dir, exec_id, "runtime-request.jsonl", '{"action":"stable"}\n')

    builder = StagedManifestBuilder(exec_id, str(evidence_dir / exec_id))
    builder.finalize_runtime_manifest()

    result = verify_staged_manifest(evidence_dir / exec_id / STAGE_FILENAMES["runtime"])
    assert result["passed"], f"Should pass when files unchanged: {result['file_errors']}"


def test_hash_match_case_passes(evidence_dir):
    """When hash matches expected_hash, case passes (no mismatch)."""
    exec_id = "test-eval-match-001"
    create_file(evidence_dir, exec_id, "runtime-request.jsonl", '{"action":"test"}\n')

    builder = StagedManifestBuilder(exec_id, str(evidence_dir / exec_id))
    manifest_path = builder.finalize_runtime_manifest()

    with open(manifest_path, "r") as f:
        manifest = json.load(f)

    stored = manifest["manifest_sha256"]
    computed = compute_manifest_hash(manifest)
    assert stored == computed, "Hash should match when no tampering"


def test_hash_computation_reproducible(evidence_dir):
    """Same content should always produce same hash."""
    exec_id = "test-eval-repro-001"
    create_file(evidence_dir, exec_id, "runtime-request.jsonl", '{"action":"fixed"}\n')

    builder = StagedManifestBuilder(exec_id, str(evidence_dir / exec_id))
    p1 = builder.finalize_runtime_manifest()

    clean_dir = evidence_dir / exec_id
    for f in clean_dir.iterdir():
        f.unlink()

    create_file(evidence_dir, exec_id, "runtime-request.jsonl", '{"action":"fixed"}\n')

    builder2 = StagedManifestBuilder(exec_id, str(evidence_dir / exec_id))
    p2 = builder2.finalize_runtime_manifest()

    with open(p1, "r") as f:
        m1 = json.load(f)
    with open(p2, "r") as f:
        m2 = json.load(f)

    assert m1["manifest_sha256"] == m2["manifest_sha256"], \
        "Same content should produce same manifest hash"
