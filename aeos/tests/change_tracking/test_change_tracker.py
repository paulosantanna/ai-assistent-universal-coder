from __future__ import annotations

import json

from aeos.core.change_tracking import ChangeTracker


def test_change_tracker_records_create_and_rollback_manifest(tmp_path):
    tracker = ChangeTracker("exec-test", tmp_path, "unit test")
    record = tracker.write_text(tmp_path / "README.md", "# Demo\n")
    outputs = tracker.write_manifests(tmp_path / ".aeos")

    assert record.action == "CREATE"
    assert record.after_sha256
    assert record.rollback["operation"] == "delete"
    manifest = json.loads((tmp_path / ".aeos" / "change-manifest.json").read_text(encoding="utf-8"))
    assert manifest["changes"][0]["relative_path"] == "README.md"
    assert outputs["rollback_summary"].endswith("rollback-plan.md")


def test_change_tracker_records_update_with_before_hash(tmp_path):
    target = tmp_path / "file.txt"
    target.write_text("before", encoding="utf-8")
    tracker = ChangeTracker("exec-test", tmp_path, "unit test")
    record = tracker.write_text(target, "after")

    assert record.action == "UPDATE"
    assert record.before_sha256
    assert record.after_sha256
    assert record.before_sha256 != record.after_sha256
    assert record.rollback["operation"] == "restore"


def test_change_tracker_rejects_outside_root(tmp_path):
    tracker = ChangeTracker("exec-test", tmp_path / "root", "unit test")
    try:
        tracker.write_text(tmp_path / "outside.txt", "bad")
    except ValueError as exc:
        assert "outside root" in str(exc)
    else:
        raise AssertionError("expected ValueError")
