from __future__ import annotations

import json
import os
import tempfile
from pathlib import Path

import pytest

from aeos.core.judge.deterministic_judge import DeterministicJudge
from aeos.core.judge.judge_models import (
    JudgeInput, JudgeResult,
    JUDGE_STATUS_PASS, JUDGE_STATUS_BLOCKED,
)
from aeos.core.evidence.evidence_manifest import (
    StagedManifestBuilder,
    compute_manifest_hash,
    verify_staged_manifest,
    STAGE_FILENAMES,
)
from aeos.core.evidence.hash_utils import sha256_file


@pytest.fixture
def tmp_workspace(tmp_path) -> Path:
    return tmp_path


def make_valid_manifest(evidence_dir: Path, execution_id: str) -> str:
    """Create a valid evidence-manifest.json that will pass Judge verification."""
    evidence_dir.mkdir(parents=True, exist_ok=True)

    runtime_file = evidence_dir / "runtime-request.jsonl"
    runtime_file.write_text('{"action":"test"}\n')

    builder = StagedManifestBuilder(execution_id, str(evidence_dir))
    return builder.finalize_runtime_manifest()


def test_judge_does_not_block_on_valid_manifest(tmp_workspace):
    """Judge must NOT report manifest_hash_mismatch for a correctly generated manifest."""
    exec_id = "test-judge-manifest-001"
    evidence_dir = tmp_workspace / ".aeos" / "evidence" / exec_id
    manifest_path = make_valid_manifest(evidence_dir, exec_id)

    judge = DeterministicJudge(str(tmp_workspace))
    ji = JudgeInput(
        execution_id=exec_id,
        evidence_manifest_path=manifest_path,
        permission_decisions=[
            {"decision_id": "pd-001", "status": "ALLOW", "action": "read", "actor": "tester"},
        ],
        policy_decisions=[
            {"decision_id": "pl-001", "status": "ALLOW", "action": "read"},
        ],
        tool_results=[
            {"tool_id": "fs", "status": "PASS", "output": {"content": "ok"}, "result_id": "tr-001"},
        ],
        skill_results=[
            {"skill_id": "s1", "status": "PASS", "request_id": "sr-001"},
        ],
        runtime_results=[
            {"execution_id": exec_id, "run_type": "skill", "status": "PASS", "duration_ms": 100},
        ],
    )
    result = judge.evaluate(ji)
    assert "manifest_hash_mismatch" not in result.blocking_rules, \
        f"Judge must NOT report manifest_hash_mismatch for valid manifest: {result.blocking_rules}"
    assert result.status == JUDGE_STATUS_PASS, \
        f"Judge should PASS with clean input and valid manifest: {result.status}"


def test_judge_detects_tampered_file_after_manifest(tmp_workspace):
    """Judge should detect file hash mismatch when a file is tampered AFTER manifest."""
    exec_id = "test-judge-tamper-001"
    evidence_dir = tmp_workspace / ".aeos" / "evidence" / exec_id
    manifest_path = make_valid_manifest(evidence_dir, exec_id)

    tampered_file = evidence_dir / "runtime-request.jsonl"
    tampered_file.write_text('{"action":"TAMPERED"}\n')

    judge = DeterministicJudge(str(tmp_workspace))
    ji = JudgeInput(
        execution_id=exec_id,
        evidence_manifest_path=manifest_path,
    )
    result = judge.evaluate(ji)
    assert "manifest_hash_mismatch" in result.blocking_rules, \
        "Judge should detect hash mismatch after tampering"
    assert result.status == JUDGE_STATUS_BLOCKED


def test_judge_does_not_check_output_it_will_write(tmp_workspace):
    """Judge manifest should only reference files that exist BEFORE Judge runs.
    
    Judge writes judge-result.json, judge-scorecard.json, judge-report.md.
    These should NOT be in the input manifest that Judge checks.
    """
    exec_id = "test-judge-self-001"
    evidence_dir = tmp_workspace / ".aeos" / "evidence" / exec_id
    manifest_path = make_valid_manifest(evidence_dir, exec_id)

    judge = DeterministicJudge(str(tmp_workspace))
    ji = JudgeInput(
        execution_id=exec_id,
        evidence_manifest_path=manifest_path,
    )
    result = judge.evaluate(ji)

    assert "manifest_hash_mismatch" not in result.blocking_rules, \
        "Judge must not fail due to files it will write (judge-result.json etc.)"
    for w in result.warnings:
        assert "judge-result" not in w, \
            f"Judge should not warn about judge-result: {w}"


def test_judge_validates_staged_manifests(tmp_workspace):
    """Judge should verify a staged runtime manifest correctly."""
    exec_id = "test-judge-staged-001"
    evidence_dir = tmp_workspace / ".aeos" / "evidence" / exec_id
    manifest_path = make_valid_manifest(evidence_dir, exec_id)

    staged_fp = evidence_dir / STAGE_FILENAMES["runtime"]
    assert staged_fp.exists(), "Staged runtime manifest should exist"

    result = verify_staged_manifest(staged_fp)
    assert result["passed"], f"Staged manifest verify should pass: {result['file_errors']}"


def test_judge_hash_computation_matches_generator(tmp_workspace):
    """The hash computed by Judge should match what the generator stored."""
    exec_id = "test-judge-hash-001"
    evidence_dir = tmp_workspace / ".aeos" / "evidence" / exec_id
    manifest_path = make_valid_manifest(evidence_dir, exec_id)

    with open(manifest_path, "r") as f:
        manifest = json.load(f)

    stored = manifest["manifest_sha256"]
    computed = compute_manifest_hash(manifest)
    assert stored == computed, \
        "Judge's hash computation must match generator's stored hash"
