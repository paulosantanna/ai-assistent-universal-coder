import pytest
import sys
from pathlib import Path
from unittest.mock import patch, MagicMock


class TestCliDoctor:
    def test_doctor_runs(self, tmp_path: Path):
        (tmp_path / ".aeos" / "config").mkdir(parents=True, exist_ok=True)
        (tmp_path / ".aeos" / "registries").mkdir(parents=True, exist_ok=True)
        (tmp_path / ".aeos" / "evidence").mkdir(parents=True, exist_ok=True)
        (tmp_path / ".aeos" / "reports").mkdir(parents=True, exist_ok=True)
        (tmp_path / ".aeos" / "config" / "permissions.yaml").write_text("permissions: []")
        (tmp_path / ".aeos" / "config" / "policies.yaml").write_text("policies: []")
        (tmp_path / ".aeos" / "registries" / "skills.yaml").write_text("skills: {}")
        (tmp_path / "pytest.ini").write_text("[pytest]\n")

        sys.path.insert(0, str(tmp_path))
        try:
            from aeos.cli.commands.doctor import cmd_doctor
            args = MagicMock()
            args.target = str(tmp_path)
            args.aeos_root = str(tmp_path)
            exit_code = cmd_doctor(args)
            assert exit_code in (0, 3)
        finally:
            sys.path.pop(0)

    def test_doctor_fails_without_aeos_dir(self, tmp_path: Path):
        from aeos.cli.commands.doctor import cmd_doctor
        args = MagicMock()
        args.target = str(tmp_path)
        args.aeos_root = str(tmp_path)
        exit_code = cmd_doctor(args)
        assert exit_code == 1

    def test_doctor_generates_report(self, tmp_path: Path):
        (tmp_path / ".aeos" / "config").mkdir(parents=True, exist_ok=True)
        (tmp_path / ".aeos" / "registries").mkdir(parents=True, exist_ok=True)
        (tmp_path / ".aeos" / "evidence").mkdir(parents=True, exist_ok=True)
        (tmp_path / ".aeos" / "reports").mkdir(parents=True, exist_ok=True)
        from aeos.cli.commands.doctor import cmd_doctor
        args = MagicMock()
        args.target = str(tmp_path)
        args.aeos_root = str(tmp_path)
        cmd_doctor(args)
        report_path = tmp_path / ".aeos" / "reports" / "doctor-report.md"
        assert report_path.exists()
        content = report_path.read_text()
        assert "AEOS Doctor Report" in content
