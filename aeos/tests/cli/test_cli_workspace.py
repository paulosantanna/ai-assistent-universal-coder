from __future__ import annotations

import json
from pathlib import Path
from types import SimpleNamespace

import pytest

from aeos.cli.commands.workspace import cmd_workspace_plan, cmd_workspace_status
from aeos.cli.main import main
from aeos.core.workspace.store import WorkspaceStoreError


def write_plan(path: Path) -> None:
    path.write_text(
        json.dumps(
            {
                "execution_id": "cli-run",
                "hard_token_limit": 20,
                "tasks": [
                    {"task_id": "task-a", "hard_token_limit": 20}
                ],
            }
        ),
        encoding="utf-8",
    )


def test_cli_plan_and_read_only_status(tmp_path: Path, capsys) -> None:
    spec = tmp_path / "plan.json"
    write_plan(spec)
    args = SimpleNamespace(spec=str(spec), target=str(tmp_path))
    assert cmd_workspace_plan(args) == 0
    planned = json.loads(capsys.readouterr().out)
    assert planned["ready_task_ids"] == ["task-a"]

    database = tmp_path / ".aeos" / "workspace" / "workspace-v1.sqlite3"
    before = database.stat().st_mtime_ns
    status_args = SimpleNamespace(execution_id="cli-run", target=str(tmp_path))
    assert cmd_workspace_status(status_args) == 0
    assert json.loads(capsys.readouterr().out)["execution_id"] == "cli-run"
    assert database.stat().st_mtime_ns == before


def test_cli_status_missing_does_not_create_state(tmp_path: Path) -> None:
    args = SimpleNamespace(execution_id="missing", target=str(tmp_path))
    with pytest.raises(WorkspaceStoreError):
        cmd_workspace_status(args)
    assert not (tmp_path / ".aeos").exists()


def test_cli_rejects_invalid_json_without_state(tmp_path: Path) -> None:
    spec = tmp_path / "plan.json"
    spec.write_text("{invalid", encoding="utf-8")
    args = SimpleNamespace(spec=str(spec), target=str(tmp_path))
    with pytest.raises(ValueError, match="invalid workspace plan JSON"):
        cmd_workspace_plan(args)
    assert not (tmp_path / ".aeos").exists()


def test_main_parser_routes_workspace_and_preserves_version(
    tmp_path: Path, monkeypatch, capsys
) -> None:
    spec = tmp_path / "plan.json"
    write_plan(spec)
    monkeypatch.setattr(
        "sys.argv",
        [
            "aeos",
            "workspace",
            "plan",
            "--spec",
            str(spec),
            "--target",
            str(tmp_path),
        ],
    )
    with pytest.raises(SystemExit) as planned:
        main()
    assert planned.value.code == 0
    assert json.loads(capsys.readouterr().out)["execution_id"] == "cli-run"

    monkeypatch.setattr("sys.argv", ["aeos", "version"])
    with pytest.raises(SystemExit) as versioned:
        main()
    assert versioned.value.code == 0
    assert capsys.readouterr().out.strip() == "AEOS Chief Staff v1.0.0"
