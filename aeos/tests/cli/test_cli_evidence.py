import pytest
from pathlib import Path
from unittest.mock import MagicMock, patch


class TestCliEvidence:
    def test_evidence_list_empty(self, tmp_path: Path):
        from aeos.cli.commands.evidence import cmd_evidence_list
        args = MagicMock()
        args.target = str(tmp_path)
        exit_code = cmd_evidence_list(args)
        assert exit_code == 0

    def test_evidence_list_with_data(self, tmp_path: Path):
        evidence_dir = tmp_path / ".aeos" / "evidence" / "exec-001"
        evidence_dir.mkdir(parents=True, exist_ok=True)
        (evidence_dir / "runtime-request.jsonl").write_text("{}")
        from aeos.cli.commands.evidence import cmd_evidence_list
        args = MagicMock()
        args.target = str(tmp_path)
        exit_code = cmd_evidence_list(args)
        assert exit_code == 0

    def test_evidence_verify_missing(self, tmp_path: Path):
        from aeos.cli.commands.evidence import cmd_evidence_verify
        args = MagicMock()
        args.target = str(tmp_path)
        args.execution_id = "nonexistent"
        args.allow_partial = False
        args.execution_mode = "latest-any"
        exit_code = cmd_evidence_verify(args)
        assert exit_code == 2

    @patch("aeos.core.evidence.evidence_manifest.verify_staged_manifest")
    def test_evidence_verify_passes_with_manifest(self, mock_verify, tmp_path: Path):
        evidence_dir = tmp_path / ".aeos" / "evidence" / "exec-001"
        evidence_dir.mkdir(parents=True, exist_ok=True)
        (evidence_dir / "runtime-evidence-manifest.json").write_text('{"files": [], "manifest_sha256": "abc"}')
        (evidence_dir / "evidence-manifest.json").write_text('{"files": [], "manifest_sha256": "abc"}')
        (evidence_dir / "runtime-request.jsonl").write_text("{}")
        mock_verify.return_value = {"passed": True, "files_ok": 1, "file_errors": [], "stored_hash": "abc", "computed_hash": "abc"}
        from aeos.cli.commands.evidence import cmd_evidence_verify
        args = MagicMock()
        args.target = str(tmp_path)
        args.execution_id = "exec-001"
        args.allow_partial = False
        args.execution_mode = "latest-any"
        exit_code = cmd_evidence_verify(args)
        assert exit_code == 0

    @patch("aeos.core.evidence.evidence_manifest.verify_staged_manifest")
    def test_evidence_verify_blocks_without_final_manifest(self, mock_verify, tmp_path: Path):
        evidence_dir = tmp_path / ".aeos" / "evidence" / "exec-002"
        evidence_dir.mkdir(parents=True, exist_ok=True)
        (evidence_dir / "runtime-evidence-manifest.json").write_text('{"files": [], "manifest_sha256": "abc"}')
        (evidence_dir / "runtime-request.jsonl").write_text("{}")
        mock_verify.return_value = {"passed": True, "files_ok": 1, "file_errors": [], "stored_hash": "abc", "computed_hash": "abc"}
        from aeos.cli.commands.evidence import cmd_evidence_verify
        args = MagicMock()
        args.target = str(tmp_path)
        args.execution_id = "exec-002"
        args.allow_partial = False
        args.execution_mode = "latest-any"
        exit_code = cmd_evidence_verify(args)
        assert exit_code == 1

    @patch("aeos.core.evidence.evidence_manifest.verify_staged_manifest")
    def test_evidence_verify_review_with_allow_partial(self, mock_verify, tmp_path: Path):
        evidence_dir = tmp_path / ".aeos" / "evidence" / "exec-003"
        evidence_dir.mkdir(parents=True, exist_ok=True)
        (evidence_dir / "runtime-evidence-manifest.json").write_text('{"files": [], "manifest_sha256": "abc"}')
        (evidence_dir / "runtime-request.jsonl").write_text("{}")
        mock_verify.return_value = {"passed": True, "files_ok": 1, "file_errors": [], "stored_hash": "abc", "computed_hash": "abc"}
        from aeos.cli.commands.evidence import cmd_evidence_verify
        args = MagicMock()
        args.target = str(tmp_path)
        args.execution_id = "exec-003"
        args.allow_partial = True
        args.execution_mode = "latest-any"
        exit_code = cmd_evidence_verify(args)
        assert exit_code == 3
