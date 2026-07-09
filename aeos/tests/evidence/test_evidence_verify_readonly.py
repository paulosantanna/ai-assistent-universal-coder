from __future__ import annotations

import json
import hashlib
from pathlib import Path

import pytest

from aeos.core.evidence.evidence_manifest import (
    StagedManifestBuilder,
    verify_staged_manifest,
)
from aeos.core.evidence.hash_utils import sha256_file


@pytest.fixture
def evidence_dir(tmp_path) -> Path:
    return tmp_path / ".aeos" / "evidence"


def create_file(evidence_dir: Path, exec_id: str, filename: str, content: str = "test"):
    fp = evidence_dir / exec_id / filename
    fp.parent.mkdir(parents=True, exist_ok=True)
    fp.write_text(content)
    return fp


def test_evidence_verify_does_not_modify_files(evidence_dir):
    exec_id = "test-readonly-001"
    ed = evidence_dir / exec_id

    create_file(ed, exec_id, "runtime-request.jsonl", '{"action":"test"}')

    builder = StagedManifestBuilder(exec_id, str(ed))
    builder.finalize_runtime_manifest()

    runtime_manifest = ed / "runtime-evidence-manifest.json"
    hash_before = hashlib.sha256(runtime_manifest.read_bytes()).hexdigest()
    mtime_before = runtime_manifest.stat().st_mtime_ns

    ws = evidence_dir.parent.parent
    result = verify_staged_manifest(runtime_manifest, ws)
    assert result.get("passed"), "Verify should pass on clean manifest"

    hash_after = hashlib.sha256(runtime_manifest.read_bytes()).hexdigest()
    mtime_after = runtime_manifest.stat().st_mtime_ns

    assert hash_before == hash_after, "Verify must not modify manifest content"
    assert mtime_before == mtime_after, "Verify must not modify manifest timestamp"


def test_evidence_verify_does_not_create_new_files(evidence_dir):
    exec_id = "test-nocreate-001"
    ed = evidence_dir / exec_id

    create_file(ed, exec_id, "runtime-request.jsonl", '{"action":"test"}')

    builder = StagedManifestBuilder(exec_id, str(ed))
    builder.finalize_runtime_manifest()

    files_before = set(f.name for f in ed.iterdir() if f.is_file())

    ws = evidence_dir.parent.parent
    verify_staged_manifest(ed / "runtime-evidence-manifest.json", ws)

    files_after = set(f.name for f in ed.iterdir() if f.is_file())

    assert files_before == files_after, \
        "Verify must not create or delete any files in evidence directory"
