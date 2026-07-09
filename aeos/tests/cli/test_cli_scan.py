import pytest
from pathlib import Path
from unittest.mock import patch, MagicMock


class TestCliScan:
    def test_scan_runs(self, tmp_path: Path):
        from aeos.cli.commands.scan import cmd_scan
        args = MagicMock()
        args.target = str(tmp_path)
        args.exclude = []
        args.max_file_mb = 10
        args.metadata_only_large_files = True
        args.respect_gitignore = False
        exit_code = cmd_scan(args)
        assert exit_code == 0

    def test_scan_target_not_found(self, tmp_path: Path):
        from aeos.cli.commands.scan import cmd_scan
        args = MagicMock()
        args.target = str(tmp_path / "nonexistent")
        args.exclude = []
        args.max_file_mb = 10
        args.metadata_only_large_files = True
        args.respect_gitignore = False
        exit_code = cmd_scan(args)
        assert exit_code == 2

    def test_scan_counts_files(self, tmp_path: Path):
        (tmp_path / "main.py").write_text("x = 1")
        (tmp_path / "cfg.yaml").write_text("key: val")
        (tmp_path / "cfg.json").write_text("{}")
        (tmp_path / "README.md").write_text("# docs")

        from aeos.cli.commands.scan import cmd_scan
        args = MagicMock()
        args.target = str(tmp_path)
        args.exclude = []
        args.max_file_mb = 10
        args.metadata_only_large_files = True
        args.respect_gitignore = False
        exit_code = cmd_scan(args)
        assert exit_code == 0

    def test_scan_excludes(self, tmp_path: Path):
        (tmp_path / "main.py").write_text("x = 1")
        nm = tmp_path / "node_modules" / "pkg"
        nm.mkdir(parents=True)
        (nm / "index.js").write_text("js")

        from aeos.cli.commands.scan import cmd_scan
        args = MagicMock()
        args.target = str(tmp_path)
        args.exclude = ["node_modules"]
        args.max_file_mb = 10
        args.metadata_only_large_files = True
        args.respect_gitignore = False
        exit_code = cmd_scan(args)
        assert exit_code == 0

    def test_scan_generates_report(self, tmp_path: Path):
        (tmp_path / "main.py").write_text("x = 1")
        (tmp_path / ".aeos" / "reports").mkdir(parents=True)

        from aeos.cli.commands.scan import cmd_scan
        args = MagicMock()
        args.target = str(tmp_path)
        args.exclude = []
        args.max_file_mb = 10
        args.metadata_only_large_files = True
        args.respect_gitignore = False
        cmd_scan(args)

        reports = list((tmp_path / ".aeos" / "reports").glob("scan-report-*.md"))
        assert len(reports) > 0
        content = reports[0].read_text()
        assert "AEOS Scan Report" in content

    def test_scan_respects_gitignore_flag(self, tmp_path: Path):
        (tmp_path / ".gitignore").write_text("*.secret")
        (tmp_path / "main.py").write_text("x = 1")
        (tmp_path / "data.secret").write_text("sensitive")

        from aeos.cli.commands.scan import cmd_scan
        args = MagicMock()
        args.target = str(tmp_path)
        args.exclude = []
        args.max_file_mb = 10
        args.metadata_only_large_files = True
        args.respect_gitignore = True
        exit_code = cmd_scan(args)
        assert exit_code == 0

    def test_scan_shows_inflated(self, tmp_path: Path):
        for i in range(400):
            (tmp_path / f"file{i}.py").write_text("x")

        from aeos.cli.commands.scan import cmd_scan
        args = MagicMock()
        args.target = str(tmp_path)
        args.exclude = []
        args.max_file_mb = 10
        args.metadata_only_large_files = True
        args.respect_gitignore = False
        exit_code = cmd_scan(args)
        assert exit_code == 0

    def test_scan_with_custom_max_file_mb(self, tmp_path: Path):
        (tmp_path / "main.py").write_text("x = 1")

        from aeos.cli.commands.scan import cmd_scan
        args = MagicMock()
        args.target = str(tmp_path)
        args.exclude = []
        args.max_file_mb = 50
        args.metadata_only_large_files = True
        args.respect_gitignore = False
        exit_code = cmd_scan(args)
        assert exit_code == 0
