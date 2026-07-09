from __future__ import annotations

import json
import os
from pathlib import Path

import pytest

from aeos.core.evidence.evidence_manifest import (
    StagedManifestBuilder,
    EvidenceManifestGenerator,
    compute_manifest_hash,
    verify_staged_manifest,
    STAGE_RUNTIME,
    STAGE_EVAL,
    STAGE_JUDGE,
    STAGE_READINESS,
    STAGE_FINAL,
    STAGE_FILENAMES,
)
from aeos.core.evidence.hash_utils import sha256, sha256_file


@pytest.fixture
def evidence_dir(tmp_path) -> Path:
    return tmp_path / ".aeos" / "evidence"


def create_stage_file(evidence_dir: Path, execution_id: str, filename: str, content: str = "test"):
    fp = evidence_dir / execution_id / filename
    fp.parent.mkdir(parents=True, exist_ok=True)
    fp.write_text(content)
    return fp


def test_runtime_manifest_generated(evidence_dir):
    exec_id = "test-runtime-001"
    create_stage_file(evidence_dir, exec_id, "runtime-request.jsonl", '{"action":"test"}\n')
    create_stage_file(evidence_dir, exec_id, "tool_result.jsonl", '{"result":"ok"}\n')
    create_stage_file(evidence_dir, exec_id, "hash-chain.jsonl", '{"index":0,"sha256":"abc"}\n')

    builder = StagedManifestBuilder(exec_id, str(evidence_dir / exec_id))
    out = builder.finalize_runtime_manifest()
    assert Path(out).exists()

    with open(out, "r") as f:
        manifest = json.load(f)
    assert manifest["execution_id"] == exec_id
    assert manifest["manifest_sha256"] != ""
    assert len(manifest["files"]) >= 2

    computed = compute_manifest_hash(manifest)
    assert computed == manifest["manifest_sha256"], "Staged manifest hash should self-verify"


def test_eval_manifest_generated(evidence_dir):
    exec_id = "test-eval-001"
    create_stage_file(evidence_dir, exec_id, "eval-suite-results.jsonl", '{"case":"test"}\n')
    create_stage_file(evidence_dir, exec_id, "eval-scorecard.json", '{"overall_score":0.95}\n')

    builder = StagedManifestBuilder(exec_id, str(evidence_dir / exec_id))
    out = builder.finalize_eval_manifest()
    assert Path(out).exists()

    with open(out, "r") as f:
        manifest = json.load(f)
    computed = compute_manifest_hash(manifest)
    assert computed == manifest["manifest_sha256"]


def test_judge_manifest_generated(evidence_dir):
    exec_id = "test-judge-001"
    create_stage_file(evidence_dir, exec_id, "judge-input.json", '{"input":"test"}')
    create_stage_file(evidence_dir, exec_id, "judge-result.json", '{"status":"PASS"}')
    create_stage_file(evidence_dir, exec_id, "judge-scorecard.json", '{"score":1.0}')

    builder = StagedManifestBuilder(exec_id, str(evidence_dir / exec_id))
    out = builder.finalize_judge_manifest()
    assert Path(out).exists()

    with open(out, "r") as f:
        manifest = json.load(f)
    computed = compute_manifest_hash(manifest)
    assert computed == manifest["manifest_sha256"]


def test_readiness_manifest_generated(evidence_dir):
    exec_id = "test-readiness-001"
    create_stage_file(evidence_dir, exec_id, "production-readiness-scorecard.json", '{"score":0.95}')

    builder = StagedManifestBuilder(exec_id, str(evidence_dir / exec_id))
    out = builder.finalize_readiness_manifest()
    assert Path(out).exists()

    with open(out, "r") as f:
        manifest = json.load(f)
    computed = compute_manifest_hash(manifest)
    assert computed == manifest["manifest_sha256"]


def test_final_manifest_excludes_self(evidence_dir):
    """Stage E manifest must NOT include itself."""
    exec_id = "test-final-001"
    create_stage_file(evidence_dir, exec_id, "runtime-request.jsonl", '{"action":"test"}\n')
    create_stage_file(evidence_dir, exec_id, "tool_result.jsonl", '{"result":"ok"}\n')

    builder = StagedManifestBuilder(exec_id, str(evidence_dir / exec_id))
    builder.finalize_runtime_manifest()
    builder.finalize_evidence_manifest()

    final_fp = evidence_dir / exec_id / STAGE_FILENAMES[STAGE_FINAL]
    assert final_fp.exists()

    with open(final_fp, "r") as f:
        manifest = json.load(f)

    final_name = STAGE_FILENAMES[STAGE_FINAL]
    file_paths = [fe["path"] for fe in manifest["files"]]
    assert final_name not in [Path(p).name for p in file_paths], \
        f"Final manifest {final_name} must not include itself in files list"


def test_staged_manifest_does_not_include_other_stages(evidence_dir):
    """Stage A manifest should only include runtime files, not judge/eval files."""
    exec_id = "test-isolation-001"
    create_stage_file(evidence_dir, exec_id, "runtime-request.jsonl", '{"action":"test"}\n')
    create_stage_file(evidence_dir, exec_id, "judge-result.json", '{"status":"PASS"}')

    builder = StagedManifestBuilder(exec_id, str(evidence_dir / exec_id))
    out = builder.finalize_runtime_manifest()

    with open(out, "r") as f:
        manifest = json.load(f)
    file_paths = [fe["path"] for fe in manifest["files"]]
    assert not any("judge-result" in p for p in file_paths), \
        "Runtime manifest should not include judge files"


def test_partial_manifest_can_be_regenerated(evidence_dir):
    """Partial manifest should be replaceable by regenerating."""
    exec_id = "test-regenerate-001"
    create_stage_file(evidence_dir, exec_id, "runtime-request.jsonl", '{"action":"first"}\n')

    builder = StagedManifestBuilder(exec_id, str(evidence_dir / exec_id))
    out1 = builder.finalize_runtime_manifest()

    create_stage_file(evidence_dir, exec_id, "tool_result.jsonl", '{"result":"second"}\n')

    out2 = builder.finalize_runtime_manifest()

    with open(out2, "r") as f:
        manifest2 = json.load(f)
    assert len(manifest2["files"]) >= 2, "Regenerated manifest should include new files"


def test_hash_chain_in_runtime_manifest(evidence_dir):
    exec_id = "test-hashchain-001"
    create_stage_file(evidence_dir, exec_id, "runtime-request.jsonl", '{"action":"test"}\n')
    create_stage_file(evidence_dir, exec_id, "hash-chain.jsonl",
                      '{"index":0,"sha256":"abc","previous_sha256":"000"}\n')

    builder = StagedManifestBuilder(exec_id, str(evidence_dir / exec_id))
    out = builder.finalize_runtime_manifest()

    with open(out, "r") as f:
        manifest = json.load(f)
    file_paths = [fe["path"] for fe in manifest["files"]]
    assert any("hash-chain" in p for p in file_paths), \
        "Runtime manifest should include hash-chain.jsonl"


def test_final_manifest_verifies_all_stages(evidence_dir):
    """Final manifest should include references to all staged manifests."""
    exec_id = "test-allstages-001"
    create_stage_file(evidence_dir, exec_id, "runtime-request.jsonl", '{"action":"test"}\n')

    builder = StagedManifestBuilder(exec_id, str(evidence_dir / exec_id))
    builder.finalize_runtime_manifest()
    builder.finalize_evidence_manifest()

    final_fp = evidence_dir / exec_id / STAGE_FILENAMES[STAGE_FINAL]
    with open(final_fp, "r") as f:
        manifest = json.load(f)

    file_paths = [fe["path"] for fe in manifest["files"]]
    assert any("runtime-evidence-manifest" in p for p in file_paths), \
        "Final manifest must reference runtime-evidence-manifest.json"
