from pathlib import Path
from aeos.core.runtime.runtime_orchestrator import RuntimeOrchestrator
from aeos.core.runtime.runtime_models import RuntimeRequest


def cmd_skill_run(args) -> int:
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
        run_type="skill",
        entity_id=args.skill_id,
        input={"skill_id": args.skill_id, "target": str(target_path)},
        target_path=str(target_path),
        dry_run=getattr(args, "dry_run", False),
        actor="cli-user",
        role="operator",
    )
    result = orchestrator.run(request)
    print(f"Skill run result: {result.status}")
    return _status_to_exit(result.status)


def _status_to_exit(status: str) -> int:
    mapping = {"PASS": 0, "BLOCKED": 1, "ERROR": 2, "REVIEW": 3, "WAITING_APPROVAL": 4}
    return mapping.get(status, 2)
