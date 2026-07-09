from __future__ import annotations

import hashlib
import json
from pathlib import Path

import pytest

from aeos.core.evidence.evidence_manifest import (
    StagedManifestBuilder,
    verify_staged_manifest,
)
from aeos.core.packaging.package_builder import PackageBuilder
from aeos.core.packaging.package_models import PackageBuildRequest, PackageStatus


@pytest.fixture
def workspace(tmp_path) -> Path:
    return tmp_path


def create_evidence(workspace: Path, exec_id: str) -> Path:
    ed = workspace / ".aeos" / "evidence" / exec_id
    ed.mkdir(parents=True, exist_ok=True)

    (ed / "runtime-request.jsonl").write_text('{"action":"test"}\n')
    (ed / "judge-input.json").write_text('{"input":"test"}')
    (ed / "judge-result.json").write_text('{"status":"PASS","score":0.95}')
    (ed / "judge-scorecard.json").write_text('{"score":1.0}')

    builder = StagedManifestBuilder(exec_id, str(ed), str(workspace))
    builder.finalize_runtime_manifest()
    builder.finalize_judge_manifest()
    builder.finalize_evidence_manifest()

    return ed


def test_verify_pass_then_package_verify_again_pass(workspace):
    exec_id = "test-verify-pkg-verify-001"
    ed = create_evidence(workspace, exec_id)

    ws_path = workspace
    verify_result_1 = verify_staged_manifest(ed / "evidence-manifest.json", ws_path)
    assert verify_result_1.get("passed"), \
        f"Verify before package should PASS, got: {verify_result_1.get('file_errors', [])}"

    builder = PackageBuilder(workspace_root=str(workspace))
    request = PackageBuildRequest(execution_id=exec_id)
    result = builder.create_package(request)
    assert result.status != PackageStatus.FAILED, f"Package creation failed: {result.error}"

    verify_result_2 = verify_staged_manifest(ed / "evidence-manifest.json", ws_path)
    assert verify_result_2.get("passed"), \
        f"Verify after package should still PASS, got: {verify_result_2.get('file_errors', [])}"

    assert verify_result_1["stored_hash"] == verify_result_2["stored_hash"], \
        "evidence-manifest.json must not change after package create"
    assert verify_result_1["computed_hash"] == verify_result_2["computed_hash"], \
        "evidence-manifest.json hash must not change after package create"


def test_hash_mismatch_still_detected_after_package(workspace):
    exec_id = "test-hashfail-pkg-001"
    ed = create_evidence(workspace, exec_id)

    ws_path = workspace

    builder = PackageBuilder(workspace_root=str(workspace))
    request = PackageBuildRequest(execution_id=exec_id)
    result = builder.create_package(request)
    assert result.status != PackageStatus.FAILED

    verify_ok = verify_staged_manifest(ed / "evidence-manifest.json", ws_path)
    assert verify_ok.get("passed"), "Verify should pass before corruption"

    jem = ed / "judge-evidence-manifest.json"
    content = json.loads(jem.read_text())
    content["manifest_sha256"] = "0000000000000000000000000000000000000000000000000000000000000000"
    jem.write_text(json.dumps(content, indent=2))

    verify_fail = verify_staged_manifest(ed / "evidence-manifest.json", ws_path)
    assert not verify_fail.get("passed"), \
        "Verify should FAIL after judge-evidence-manifest.json mutation"
    assert any("hash mismatch" in e.lower() for e in verify_fail.get("file_errors", [])), \
        f"Must report hash mismatch error, got: {verify_fail.get('file_errors', [])}"
