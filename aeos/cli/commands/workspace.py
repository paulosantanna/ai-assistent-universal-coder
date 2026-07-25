"""Comandos mínimos e locais do AEOS Workspace OS."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from aeos.core.workspace.kernel import WorkspaceKernel
from aeos.core.workspace.store import WorkspaceStore

MAX_PLAN_BYTES = 1_048_576


def _print_json(value: dict[str, Any]) -> None:
    print(json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")))


def cmd_workspace_plan(args: Any) -> int:
    spec_path = Path(args.spec).resolve()
    if not spec_path.is_file():
        raise ValueError("workspace plan spec does not exist")
    if spec_path.stat().st_size > MAX_PLAN_BYTES:
        raise ValueError("workspace plan spec exceeds 1 MiB")
    try:
        document = json.loads(spec_path.read_text(encoding="utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        raise ValueError(f"invalid workspace plan JSON: {error}") from error
    kernel = WorkspaceKernel(WorkspaceStore(Path(args.target)))
    _print_json(kernel.plan(document))
    return 0


def cmd_workspace_status(args: Any) -> int:
    store = WorkspaceStore(Path(args.target), create=False, read_only=True)
    _print_json(WorkspaceKernel(store).status(args.execution_id))
    return 0
