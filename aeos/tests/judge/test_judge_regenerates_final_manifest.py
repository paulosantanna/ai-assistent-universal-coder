from __future__ import annotations

import json
import hashlib
from pathlib import Path
from unittest.mock import patch, MagicMock

import pytest

from aeos.core.judge.judge_engine import JudgeEngine
from aeos.core.evidence.evidence_manifest import (
    StagedManifestBuilder,
    is_finalized,
    FINALIZED_MARKER,
)


@pytest.fixture
def workspace(tmp_path) -> Path:
    return tmp_path


def create_evidence(workspace: Path, exec_id: str):
    ed = workspace / ".aeos" / "evidence" / exec_id
    ed.mkdir(parents=True, exist_ok=True)

    (ed / "judge-input.json").write_text('{"execution_id":"' + exec_id + '","target_path":"."}')
    (ed / "judge-result.json").write_text('{"execution_id":"' + exec_id + '","status":"PASS","score":0.95}')
    (ed / "judge-scorecard.json").write_text('{"execution_id":"' + exec_id + '","score":1.0,"categories":{}}')
    (ed / "runtime-request.jsonl").write_text('{"action":"test"}\n')

    builder = StagedManifestBuilder(exec_id, str(ed), str(workspace))
    builder.finalize_runtime_manifest()
    return ed


def test_judge_engine_finalizes_judge_and_final_manifest(workspace):
    exec_id = "test-judge-regen-001"
    ed = create_evidence(workspace, exec_id)

    engine = JudgeEngine(workspace_root=str(workspace))

    engine._finalize_judge_manifest(exec_id)

    jem_path = ed / "judge-evidence-manifest.json"
    assert jem_path.exists(), "Judge evidence manifest should exist"

    em_path = ed / "evidence-manifest.json"
    assert em_path.exists(), "Final evidence manifest should exist after judge finalize"

    assert is_finalized(ed), "Evidence should be marked as finalized"

    with open(em_path) as f:
        em = json.load(f)
    jem_entries = [fe for fe in em["files"] if "judge-evidence-manifest" in fe.get("path", "")]
    assert jem_entries, "Final manifest must reference judge-evidence-manifest.json"


def test_judge_regen_updates_stale_final_manifest(workspace):
    exec_id = "test-stale-regen-001"
    ed = create_evidence(workspace, exec_id)

    engine = JudgeEngine(workspace_root=str(workspace))
    engine._finalize_judge_manifest(exec_id)

    jem_path = ed / "judge-evidence-manifest.json"
    original_jem_hash = hashlib.sha256(jem_path.read_bytes()).hexdigest()

    em_path = ed / "evidence-manifest.json"
    with open(em_path) as f:
        em_before = json.load(f)
    jem_entry_before = [fe for fe in em_before["files"]
                        if "judge-evidence-manifest" in fe.get("path", "")][0]
    assert jem_entry_before["sha256"] == original_jem_hash, \
        "Hash in final manifest should match on-disk hash"

    (ed / "judge-result.json").write_text(
        '{"execution_id":"' + exec_id + '","status":"PASS","score":0.99,"blocking_rules":[]}'
    )

    engine._finalize_judge_manifest(exec_id)

    new_jem_hash = hashlib.sha256(jem_path.read_bytes()).hexdigest()
    assert new_jem_hash != original_jem_hash, "Judge manifest hash should change after re-run"

    with open(em_path) as f:
        em_after = json.load(f)
    jem_entry_after = [fe for fe in em_after["files"]
                       if "judge-evidence-manifest" in fe.get("path", "")][0]
    assert jem_entry_after["sha256"] == new_jem_hash, \
        "Regenerated final manifest must reflect updated judge manifest hash"

    assert is_finalized(ed), "Should stay finalized after re-run"
