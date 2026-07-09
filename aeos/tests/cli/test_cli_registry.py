import pytest
from pathlib import Path
from unittest.mock import MagicMock, patch


class TestCliRegistry:
    def test_registry_validate_runs(self, tmp_path: Path):
        reg_dir = tmp_path / ".aeos" / "registries"
        reg_dir.mkdir(parents=True, exist_ok=True)
        (reg_dir / "skills.yaml").write_text("skills: {}")
        from aeos.cli.commands.registry import cmd_registry_validate
        args = MagicMock()
        args.target = str(tmp_path)
        exit_code = cmd_registry_validate(args)
        assert exit_code in (0, 1)

    def test_registry_list_skills(self, tmp_path: Path):
        reg_dir = tmp_path / ".aeos" / "registries"
        reg_dir.mkdir(parents=True, exist_ok=True)
        (reg_dir / "skills.yaml").write_text("skills: {}")
        from aeos.cli.commands.registry import cmd_registry_list
        args = MagicMock()
        args.target = str(tmp_path)
        args.entity = "skills"
        exit_code = cmd_registry_list(args)
        assert exit_code == 0

    def test_registry_list_empty(self, tmp_path: Path):
        reg_dir = tmp_path / ".aeos" / "registries"
        reg_dir.mkdir(parents=True, exist_ok=True)
        from aeos.cli.commands.registry import cmd_registry_list
        args = MagicMock()
        args.target = str(tmp_path)
        args.entity = "playbooks"
        exit_code = cmd_registry_list(args)
        assert exit_code == 0
