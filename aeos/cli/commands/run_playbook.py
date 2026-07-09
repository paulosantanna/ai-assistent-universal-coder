from pathlib import Path
from aeos.core.runtime.runtime_orchestrator import RuntimeOrchestrator
from aeos.core.runtime.runtime_models import RuntimeRequest
from aeos.cli.commands.run_skill import _status_to_exit


def cmd_playbook_run(args) -> int:
    from aeos.cli.main import resolve_aeos_root, resolve_target_path
    aeos_root = resolve_aeos_root(args)
    target_path = resolve_target_path(args)
    from aeos.core.runtime.path_resolver import validate_aeos_root
    explicit = getattr(args, "aeos_root", None)
    if isinstance(explicit, str) and explicit:
        err = validate_aeos_root(aeos_root)
        if err:
            print(f"Error: {err}", file=__import__("sys").stderr)
            return 2
    orchestrator = RuntimeOrchestrator(
        workspace_root=str(target_path),
        aeos_root=str(aeos_root),
        target_path=str(target_path),
    )
    orchestrator.initialize()

    request = RuntimeRequest(
        execution_id="",
        run_type="playbook",
        entity_id=args.playbook_id,
        input={"playbook_id": args.playbook_id, "target": str(target_path)},
        target_path=str(target_path),
        dry_run=getattr(args, "dry_run", False),
        actor="cli-user",
        role="operator",
    )
    result = orchestrator.run(request)
    print(f"Playbook run result: {result.status}")
    return _status_to_exit(result.status)
