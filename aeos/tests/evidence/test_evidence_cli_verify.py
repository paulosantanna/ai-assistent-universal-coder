import pytest
from pathlib import Path
from unittest.mock import MagicMock, patch


@patch("aeos.core.evidence.evidence_manifest.verify_staged_manifest")
def test_evidence_verify_shows_resolved_path(mock_verify, tmp_path: Path, capsys):
    evidence_dir = tmp_path / ".aeos" / "evidence" / "exec-final"
    evidence_dir.mkdir(parents=True, exist_ok=True)
    (evidence_dir / "evidence-manifest.json").write_text('{"files": [], "manifest_sha256": "abc"}')
    (evidence_dir / "runtime-request.jsonl").write_text("{}")
    mock_verify.return_value = {"passed": True, "files_ok": 1, "file_errors": []}

    from aeos.cli.commands.evidence import cmd_evidence_verify
    args = MagicMock()
    args.target = str(tmp_path)
    args.execution_id = "exec-final"
    args.allow_partial = False
    args.execution_mode = "latest-any"
    exit_code = cmd_evidence_verify(args)
    captured = capsys.readouterr()
    assert "Resolved execution:" in captured.out
    assert "evidence-manifest.json: PASS" in captured.out
    assert exit_code == 0


@patch("aeos.core.evidence.evidence_manifest.verify_staged_manifest")
def test_evidence_verify_not_pass_when_all_skip(mock_verify, tmp_path: Path, capsys):
    evidence_dir = tmp_path / ".aeos" / "evidence" / "exec-empty"
    evidence_dir.mkdir(parents=True, exist_ok=True)
    mock_verify.return_value = {"passed": True, "files_ok": 0, "file_errors": []}

    from aeos.cli.commands.evidence import cmd_evidence_verify
    args = MagicMock()
    args.target = str(tmp_path)
    args.execution_id = "exec-empty"
    args.allow_partial = False
    args.execution_mode = "latest-any"
    exit_code = cmd_evidence_verify(args)
    captured = capsys.readouterr()
    assert "BLOCKED" in captured.out
    assert "PASS" not in captured.out
    assert exit_code == 1


@patch("aeos.core.evidence.evidence_manifest.verify_staged_manifest")
def test_evidence_verify_blocks_when_final_manifest_missing(mock_verify, tmp_path: Path, capsys):
    evidence_dir = tmp_path / ".aeos" / "evidence" / "exec-partial"
    evidence_dir.mkdir(parents=True, exist_ok=True)
    (evidence_dir / "runtime-evidence-manifest.json").write_text('{"files": []}')
    (evidence_dir / "runtime-request.jsonl").write_text("{}")
    mock_verify.return_value = {"passed": True, "files_ok": 1, "file_errors": []}

    from aeos.cli.commands.evidence import cmd_evidence_verify
    args = MagicMock()
    args.target = str(tmp_path)
    args.execution_id = "exec-partial"
    args.allow_partial = False
    args.execution_mode = "latest-any"
    exit_code = cmd_evidence_verify(args)
    captured = capsys.readouterr()
    assert "BLOCKED" in captured.out
    assert "evidence-manifest.json not found" in captured.out
    assert exit_code == 1


@patch("aeos.core.evidence.evidence_manifest.verify_staged_manifest")
def test_evidence_verify_allow_partial_returns_review(mock_verify, tmp_path: Path, capsys):
    evidence_dir = tmp_path / ".aeos" / "evidence" / "exec-partial"
    evidence_dir.mkdir(parents=True, exist_ok=True)
    (evidence_dir / "runtime-evidence-manifest.json").write_text('{"files": []}')
    (evidence_dir / "runtime-request.jsonl").write_text("{}")
    mock_verify.return_value = {"passed": True, "files_ok": 1, "file_errors": []}

    from aeos.cli.commands.evidence import cmd_evidence_verify
    args = MagicMock()
    args.target = str(tmp_path)
    args.execution_id = "exec-partial"
    args.allow_partial = True
    args.execution_mode = "latest-any"
    exit_code = cmd_evidence_verify(args)
    captured = capsys.readouterr()
    assert "REVIEW" in captured.out
    assert exit_code == 3
