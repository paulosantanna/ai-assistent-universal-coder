from __future__ import annotations

import json
import sys

from aeos.core.runtime.runtime_models import RuntimeRequest
from aeos.core.runtime.runtime_orchestrator import RuntimeOrchestrator


def cmd_workflow_plan(args) -> int:
    from aeos.cli.main import resolve_aeos_root, resolve_target_path

    aeos_root = resolve_aeos_root(args)
    target_path = resolve_target_path(args)
    orchestrator = RuntimeOrchestrator(
        workspace_root=str(target_path),
        aeos_root=str(aeos_root),
        target_path=str(target_path),
    )
    orchestrator.initialize()

    request = RuntimeRequest(
        execution_id=getattr(args, "execution_id", "") or "",
        run_type="workflow",
        entity_id=args.workflow_id,
        actor="cli-user",
        role="operator",
        target_path=str(target_path),
        dry_run=True,
        approval_id=getattr(args, "approval_id", None),
        input={
            "objective": args.objective,
            "workflow_id": args.workflow_id,
            "risk_level": args.risk_level,
            "required_paths": _json_list(getattr(args, "required_paths", "[]")),
            "evidence_refs": _json_list(getattr(args, "evidence_refs", "[]")),
            "create_dataset_candidate": not getattr(args, "no_dataset_candidate", False),
        },
    )
    result = orchestrator.run_workflow(request)
    print(json.dumps(result.to_dict(), indent=2, ensure_ascii=True))
    return _status_to_exit(result.status)


def _json_list(raw: str) -> list[str]:
    try:
        value = json.loads(raw)
    except json.JSONDecodeError as exc:
        print(f"Invalid JSON list: {raw}", file=sys.stderr)
        raise SystemExit(2) from exc
    if not isinstance(value, list) or not all(isinstance(item, str) for item in value):
        print("Expected a JSON list of strings", file=sys.stderr)
        raise SystemExit(2)
    return value


def _status_to_exit(status: str) -> int:
    mapping = {"PASS": 0, "BLOCKED": 1, "ERROR": 2, "REVIEW": 3, "WAITING_APPROVAL": 4}
    return mapping.get(status, 2)

