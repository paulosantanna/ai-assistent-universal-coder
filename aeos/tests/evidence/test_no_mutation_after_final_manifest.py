from __future__ import annotations

import json
import hashlib
from pathlib import Path

import pytest

from aeos.core.evidence.evidence_manifest import (
    StagedManifestBuilder,
    verify_staged_manifest,
    is_finalized,
    mark_finalized,
    unmark_finalized,
    FINALIZED_MARKER,
)


@pytest.fixture
def evidence_dir(tmp_path) -> Path:
    return tmp_path / ".aeos" / "evidence"


def create_file(evidence_dir: Path, exec_id: str, filename: str, content: str = "test"):
    fp = evidence_dir / exec_id / filename
    fp.parent.mkdir(parents=True, exist_ok=True)
    fp.write_text(content)
    return fp


def test_finalized_marker_created_after_final_manifest(evidence_dir):
    exec_id = "test-finalized-001"
    create_file(evidence_dir, exec_id, "runtime-request.jsonl", '{"action":"test"}')

    builder = StagedManifestBuilder(exec_id, str(evidence_dir / exec_id))
    builder.finalize_runtime_manifest()
    assert not is_finalized(evidence_dir / exec_id), \
        "Should NOT be finalized before final evidence manifest"

    builder.finalize_evidence_manifest()

    assert is_finalized(evidence_dir / exec_id), \
        "Should be finalized after final evidence manifest"
    assert (evidence_dir / exec_id / FINALIZED_MARKER).exists()


def test_no_mutation_after_final_manifest_detected(evidence_dir):
    exec_id = "test-nomutation-001"
    create_file(evidence_dir, exec_id, "runtime-request.jsonl", '{"action":"test"}')

    builder = StagedManifestBuilder(exec_id, str(evidence_dir / exec_id))
    builder.finalize_runtime_manifest()
    builder.finalize_evidence_manifest()

    jem_path = evidence_dir / exec_id / "judge-evidence-manifest.json"
    if jem_path.exists():
        original_hash = hashlib.sha256(jem_path.read_bytes()).hexdigest()

        jem_path.write_text('{"corrupted": true}')

        ws = evidence_dir.parent.parent
        result = verify_staged_manifest(evidence_dir / exec_id / "evidence-manifest.json", ws)
        assert not result.get("passed"), \
            "Verify should FAIL after judge-evidence-manifest.json mutation"
        file_errors = result.get("file_errors", [])
        assert any("hash mismatch" in e.lower() for e in file_errors), \
            f"Expected hash mismatch error, got: {file_errors}"

        jem_path.write_text('{"manifest_sha256":"0000","files":[],"execution_id":"x"}')
        result2 = verify_staged_manifest(jem_path, ws)
        assert not result2.get("passed"), \
            "Corrupted manifest should not verify"


def test_marker_respected_by_is_finalized(evidence_dir):
    exec_id = "test-marker-001"
    ed = evidence_dir / exec_id
    ed.mkdir(parents=True, exist_ok=True)

    assert not is_finalized(ed), "Fresh dir should not be finalized"

    mark_finalized(ed)
    assert is_finalized(ed), "Should be finalized after mark_finalized()"

    unmark_finalized(ed)
    assert not is_finalized(ed), "Should not be finalized after unmark_finalized()"


def test_judge_regen_updates_final_manifest(evidence_dir):
    exec_id = "test-regen-001"
    create_file(evidence_dir, exec_id, "judge-input.json", '{"input":"first"}')
    create_file(evidence_dir, exec_id, "judge-result.json", '{"status":"PASS"}')
    create_file(evidence_dir, exec_id, "judge-scorecard.json", '{"score":1.0}')

    builder = StagedManifestBuilder(exec_id, str(evidence_dir / exec_id))
    builder.finalize_judge_manifest()

    jem_path = evidence_dir / exec_id / "judge-evidence-manifest.json"
    orig_jem_hash = hashlib.sha256(jem_path.read_bytes()).hexdigest()

    builder.finalize_evidence_manifest()
    assert is_finalized(evidence_dir / exec_id)

    em_path = evidence_dir / exec_id / "evidence-manifest.json"
    with open(em_path) as f:
        em_before = json.load(f)
    jem_entry = [fe for fe in em_before["files"] if "judge-evidence-manifest" in fe.get("path", "")]
    assert jem_entry, "Final manifest must reference judge-evidence-manifest.json"
    orig_stored_hash = jem_entry[0]["sha256"]

    assert orig_stored_hash == orig_jem_hash, \
        "Final manifest must store correct hash of judge-evidence-manifest.json"

    create_file(evidence_dir, exec_id, "judge-result.json", '{"status":"PASS","score":0.99}')

    builder.finalize_judge_manifest()

    new_jem_hash = hashlib.sha256(jem_path.read_bytes()).hexdigest()
    assert new_jem_hash != orig_jem_hash, \
        "Judge-evidence-manifest hash should change after re-finalization"

    builder.finalize_evidence_manifest()

    with open(em_path) as f:
        em_after = json.load(f)
    new_stored_hash = [fe for fe in em_after["files"] if "judge-evidence-manifest" in fe.get("path", "")][0]["sha256"]

    assert new_stored_hash == new_jem_hash, \
        "regenerated final manifest must store updated judge-evidence-manifest hash"
