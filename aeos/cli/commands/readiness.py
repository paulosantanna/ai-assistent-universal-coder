from pathlib import Path


def cmd_readiness_run(args) -> int:
    from aeos.cli.main import get_workspace_root, resolve_aeos_root
    workspace = get_workspace_root(args)
    aeos_root = resolve_aeos_root(args)
    from aeos.core.runtime.path_resolver import validate_aeos_root
    explicit = getattr(args, "aeos_root", None)
    if isinstance(explicit, str) and explicit:
        err = validate_aeos_root(aeos_root)
        if err:
            print(f"Error: {err}", file=__import__("sys").stderr)
            return 2

    try:
        from aeos.core.runtime.runtime_orchestrator import RuntimeOrchestrator
        orchestrator = RuntimeOrchestrator(
            workspace_root=str(workspace),
            aeos_root=str(aeos_root),
            target_path=str(workspace),
        )
        orchestrator.initialize()
        result = orchestrator.run_readiness_audit()
        status = getattr(result, "status", "PASS")
        score = getattr(result, "overall_score", 1.0)
        print(f"Readiness: {status} (score: {score:.4f})")
        from aeos.cli.commands.run_skill import _status_to_exit
        if hasattr(status, "value"):
            return _status_to_exit(status.value)
        return _status_to_exit(str(status))
    except Exception as e:
        print(f"Error running readiness audit: {e}", file=__import__("sys").stderr)
        return 2
