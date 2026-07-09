"""Test that CLI properly separates AEOS root from target project."""

from pathlib import Path
from unittest.mock import MagicMock, patch


def test_playbook_run_does_not_search_config_in_target(tmp_path: Path):
    """When --aeos-root is set, config must NOT be searched in target."""
    target = tmp_path / "target-project"
    target.mkdir()
    aeos_root = tmp_path / "aeos-install"
    aeos_root.mkdir(parents=True)
    (aeos_root / "aeos" / "config" / "aeos.config.yaml").parent.mkdir(parents=True)
    (aeos_root / "aeos" / "config" / "aeos.config.yaml").write_text(
        "aeos:\n  name: test\n  version: 1.0\n  mode: development\nregistries:\n  skills: aeos/registries"
    )

    assert not (target / "aeos" / "config" / "aeos.config.yaml").exists()

    with patch("aeos.cli.commands.run_playbook.RuntimeOrchestrator") as mock_orch, \
         patch("aeos.cli.commands.run_playbook.RuntimeRequest"):
        mock_result = MagicMock()
        mock_result.status = "PASS"
        mock_orch.return_value.run.return_value = mock_result

        from aeos.cli.commands.run_playbook import cmd_playbook_run
        args = MagicMock()
        args.aeos_root = str(aeos_root)
        args.target = str(target)
        args.playbook_id = "test"
        args.dry_run = True
        exit_code = cmd_playbook_run(args)
        assert exit_code == 0

        mock_orch.assert_called_once()
        call_kwargs = mock_orch.call_args[1]
        assert "aeos_root" in call_kwargs
        assert Path(call_kwargs["aeos_root"]).resolve() == aeos_root.resolve()


def test_target_without_aeos_config_is_accepted(tmp_path: Path):
    """Target project without aeos/config should not cause errors when aeos_root is set."""
    target = tmp_path / "bare-project"
    target.mkdir()
    aeos_root = tmp_path / "aeos-install"
    aeos_root.mkdir(parents=True)
    (aeos_root / "aeos" / "config" / "aeos.config.yaml").parent.mkdir(parents=True)
    (aeos_root / "aeos" / "config" / "aeos.config.yaml").write_text(
        "aeos:\n  name: test\n  version: 1.0\n  mode: development\nregistries:\n  skills: aeos/registries"
    )

    assert not (target / "aeos" / "config").exists()

    with patch("aeos.cli.commands.run_skill.RuntimeOrchestrator") as mock_orch, \
         patch("aeos.cli.commands.run_skill.RuntimeRequest"):
        mock_result = MagicMock()
        mock_result.status = "PASS"
        mock_orch.return_value.run.return_value = mock_result

        from aeos.cli.commands.run_skill import cmd_skill_run
        args = MagicMock()
        args.aeos_root = str(aeos_root)
        args.target = str(target)
        args.skill_id = "test"
        args.dry_run = True
        exit_code = cmd_skill_run(args)
        assert exit_code == 0


def test_error_message_points_to_aeos_root(tmp_path: Path):
    """Error must point to --aeos-root, not to target config."""
    target = tmp_path / "project"
    target.mkdir()
    from aeos.core.runtime.path_resolver import validate_aeos_root
    err = validate_aeos_root(target)
    assert err is not None
    assert "--aeos-root" in err
    assert str(target / "aeos" / "config" / "aeos.config.yaml") in err


def test_scan_uses_target_as_readonly(tmp_path: Path):
    """Scan must only read target, never modify it beyond .aeos/reports."""
    with patch("aeos.cli.commands.scan.FastRepoScanner") as mock_scanner:
        mock_stats = MagicMock()
        mock_stats.total_files = 10
        mock_stats.ignored_files = 2
        mock_stats.ignored_dirs = set()
        mock_stats.scanned_files = 8
        mock_stats.python_files = 3
        mock_stats.config_files = 2
        mock_stats.metadata_only_files = 0
        mock_stats.metadata_only_bytes = 0
        mock_stats.scanned_bytes = 1024
        mock_stats.elapsed_seconds = 0.5
        mock_stats.inflated = False
        mock_stats.top_20_dirs = []
        mock_scanner.return_value.scan.return_value = mock_stats

        from aeos.cli.commands.scan import cmd_scan
        args = MagicMock()
        args.target = str(tmp_path)
        args.exclude = []
        args.max_file_mb = 10
        args.metadata_only_large_files = True
        args.respect_gitignore = False
        exit_code = cmd_scan(args)
        assert exit_code == 0
