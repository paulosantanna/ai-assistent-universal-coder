import pytest
from pathlib import Path
from unittest.mock import MagicMock, patch, PropertyMock


class TestCliRuntimeCommands:
    @patch("aeos.cli.commands.run_skill.RuntimeOrchestrator")
    @patch("aeos.cli.commands.run_skill.RuntimeRequest")
    def test_skill_run_dry_run(self, mock_rr, mock_orch, tmp_path: Path):
        mock_result = MagicMock()
        mock_result.status = "PASS"
        mock_orch.return_value.run.return_value = mock_result
        from aeos.cli.commands.run_skill import cmd_skill_run
        args = MagicMock()
        args.target = str(tmp_path)
        args.skill_id = "test-skill"
        args.dry_run = True
        exit_code = cmd_skill_run(args)
        assert exit_code == 0

    @patch("aeos.cli.commands.run_playbook.RuntimeOrchestrator")
    @patch("aeos.cli.commands.run_playbook.RuntimeRequest")
    def test_playbook_run_dry_run(self, mock_rr, mock_orch, tmp_path: Path):
        mock_result = MagicMock()
        mock_result.status = "PASS"
        mock_orch.return_value.run.return_value = mock_result
        from aeos.cli.commands.run_playbook import cmd_playbook_run
        args = MagicMock()
        args.target = str(tmp_path)
        args.playbook_id = "test-playbook"
        args.dry_run = True
        exit_code = cmd_playbook_run(args)
        assert exit_code == 0

    @patch("aeos.cli.commands.run_agent.RuntimeOrchestrator")
    @patch("aeos.cli.commands.run_agent.RuntimeRequest")
    def test_agent_run_dry_run(self, mock_rr, mock_orch, tmp_path: Path):
        mock_result = MagicMock()
        mock_result.status = "PASS"
        mock_orch.return_value.run.return_value = mock_result
        from aeos.cli.commands.run_agent import cmd_agent_run
        args = MagicMock()
        args.target = str(tmp_path)
        args.agent_id = "test-agent"
        args.objective = "test objective"
        args.dry_run = True
        exit_code = cmd_agent_run(args)
        assert exit_code == 0

    def test_status_to_exit(self):
        from aeos.cli.commands.run_skill import _status_to_exit
        assert _status_to_exit("PASS") == 0
        assert _status_to_exit("BLOCKED") == 1
        assert _status_to_exit("ERROR") == 2
        assert _status_to_exit("REVIEW") == 3
        assert _status_to_exit("WAITING_APPROVAL") == 4
        assert _status_to_exit("UNKNOWN") == 2
