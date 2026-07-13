from __future__ import annotations

import json
from pathlib import Path

import pytest

from aeos.core.evidence.evidence_store import EvidenceStore
from aeos.core.evidence.evidence_manifest import EvidenceManifestGenerator
from aeos.core.evidence.evidence_reporter import EvidenceReporter
from aeos.core.evidence.audit_logger import AuditLogger
from aeos.core.evidence.hash_utils import sha256, sha256_file


@pytest.fixture
def evidence_dir(tmp_path) -> Path:
    return tmp_path / ".aeos" / "evidence"


def test_store_record_creates_file(evidence_dir):
    store = EvidenceStore(str(evidence_dir))
    rid = store.store_record("exec-001", "audit", {"action": "test"})
    assert rid is not None
    fp = evidence_dir / "exec-001" / "audits.jsonl"
    assert fp.exists()


def test_store_record_permission_decision(evidence_dir):
    store = EvidenceStore(str(evidence_dir))
    rid = store.store_record("exec-001", "permission_decision", {"allowed": False})
    assert rid is not None
    fp = evidence_dir / "exec-001" / "permission_decisions.jsonl"
    assert fp.exists()


def test_store_record_policy_decision(evidence_dir):
    store = EvidenceStore(str(evidence_dir))
    rid = store.store_record("exec-001", "policy_decision", {"allowed": True})
    assert rid is not None
    fp = evidence_dir / "exec-001" / "policy_decisions.jsonl"
    assert fp.exists()


def test_evidence_manifest_contains_sha256(evidence_dir):
    store = EvidenceStore(str(evidence_dir))
    store.store_record("exec-002", "audit", {"action": "create"})
    store.store_record("exec-002", "permission_decision", {"allowed": True})

    rep = EvidenceReporter(str(evidence_dir))
    manifest_path = rep.generate_manifest("exec-002", {"audit": 1, "permission_decision": 1})
    assert Path(manifest_path).exists()

    with open(manifest_path, "r") as f:
        manifest = json.load(f)

    assert manifest["execution_id"] == "exec-002"
    assert manifest["manifest_sha256"] != ""
    assert len(manifest["files"]) >= 1
    for file_entry in manifest["files"]:
        assert "sha256" in file_entry
        assert "path" in file_entry


def test_hash_chain_generated(evidence_dir):
    store = EvidenceStore(str(evidence_dir))
    store.store_record("exec-003", "audit", {"action": "first"})
    store.store_record("exec-003", "audit", {"action": "second"})

    chain = store.get_hash_chain()
    assert len(chain) == 2
    assert chain[0].previous_sha256 == "0" * 64
    assert chain[1].previous_sha256 == chain[0].sha256


def test_hash_chain_verify(evidence_dir):
    store = EvidenceStore(str(evidence_dir))
    store.store_record("exec-004", "audit", {"action": "test"})
    result = store.verify_hash_chain("exec-004")
    assert result["passed"] is True


def test_hash_utility():
    h = sha256("hello")
    assert len(h) == 64
    assert sha256({"a": 1}) == sha256({"a": 1})
    assert sha256({"a": 1}) != sha256({"a": 2})


def test_audit_logger_creates_file(evidence_dir):
    logger = AuditLogger(str(evidence_dir))
    entry = logger.log("exec-005", "test_action", "root", "PASS", "test detail")
    assert entry.entry_id.startswith("ev-")
    fp = evidence_dir / "exec-005" / "audit-log.jsonl"
    assert fp.exists()
    with open(fp, "r") as f:
        line = json.loads(f.readline())
    assert line["action"] == "test_action"
    assert line["actor"] == "root"


def test_evidence_manifest_generator(evidence_dir):
    log_dir = evidence_dir / "exec-006"
    log_dir.mkdir(parents=True, exist_ok=True)
    log_file = log_dir / "audits.jsonl"
    with open(log_file, "w") as f:
        for _ in range(5):
            f.write('{"test": true}\n')

    gen = EvidenceManifestGenerator("exec-006", str(evidence_dir))
    gen.add_file(str(log_file), record_count=5)
    out = gen.generate(str(log_dir / "evidence-manifest.json"))
    assert Path(out).exists()
    with open(out, "r") as f:
        manifest = json.load(f)
    assert manifest["total_records"] == 5


def test_multiple_records_same_file(evidence_dir):
    store = EvidenceStore(str(evidence_dir))
    store.store_record("exec-007", "audit", {"i": 1})
    store.store_record("exec-007", "audit", {"i": 2})
    store.store_record("exec-007", "audit", {"i": 3})

    fp = evidence_dir / "exec-007" / "audits.jsonl"
    count = sum(1 for _ in open(fp, "r"))
    assert count == 3


def test_store_records_batches_hash_chain(evidence_dir):
    store = EvidenceStore(str(evidence_dir))
    ids = store.store_records("exec-008", "audit", [{"i": 1}, {"i": 2}, {"i": 3}])

    assert len(ids) == 3
    assert len(store.get_hash_chain()) == 3
    result = store.verify_hash_chain("exec-008")
    assert result["passed"] is True
    fp = evidence_dir / "exec-008" / "audits.jsonl"
    assert sum(1 for _ in open(fp, "r")) == 3
