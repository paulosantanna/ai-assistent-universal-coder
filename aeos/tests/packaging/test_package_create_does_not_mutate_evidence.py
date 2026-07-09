from __future__ import annotations

import hashlib
from pathlib import Path

import pytest

from aeos.core.evidence.evidence_manifest import (
    StagedManifestBuilder,
    mark_finalized,
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


def test_package_create_does_not_modify_evidence(workspace):
    exec_id = "test-pkg-nomut-001"
    ed = create_evidence(workspace, exec_id)

    file_hashes_before = {}
    for f in ed.rglob("*"):
        if f.is_file():
            file_hashes_before[str(f.relative_to(ed))] = hashlib.sha256(f.read_bytes()).hexdigest()

    builder = PackageBuilder(workspace_root=str(workspace))
    request = PackageBuildRequest(execution_id=exec_id)
    result = builder.create_package(request)

    assert result.status != PackageStatus.FAILED, f"Package creation failed: {result.error}"
    assert result.package_path, "Package path should be set"

    file_hashes_after = {}
    for f in ed.rglob("*"):
        if f.is_file():
            file_hashes_after[str(f.relative_to(ed))] = hashlib.sha256(f.read_bytes()).hexdigest()

    assert file_hashes_before == file_hashes_after, \
        "Package creation must not modify any evidence files"

    assert result.package_path.startswith(str(workspace / ".aeos" / "packages")), \
        "Package should be written to .aeos/packages/, not evidence"


def test_package_create_fails_without_finalized_marker(workspace):
    exec_id = "test-pkg-nofinal-001"
    ed = create_evidence(workspace, exec_id)

    marker = ed / ".finalized"
    if marker.exists():
        marker.unlink()

    builder = PackageBuilder(workspace_root=str(workspace))
    request = PackageBuildRequest(execution_id=exec_id)
    result = builder.create_package(request)

    assert result.status == PackageStatus.FAILED, \
        "Package should FAIL if evidence is not finalized"
    assert "not finalized" in result.error.lower(), \
        "Error must mention not finalized"
    assert ".finalized" in result.error, \
        "Error must mention .finalized marker"
