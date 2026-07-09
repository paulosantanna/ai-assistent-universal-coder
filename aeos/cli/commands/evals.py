from pathlib import Path


def cmd_evals_run(args) -> int:
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
    suite_id = getattr(args, "suite", "all")

    orchestrator = None
    try:
        from aeos.core.runtime.runtime_orchestrator import RuntimeOrchestrator
        orchestrator = RuntimeOrchestrator(
            workspace_root=str(workspace),
            aeos_root=str(aeos_root),
            target_path=str(workspace),
        )
        orchestrator.initialize()
    except Exception as e:
        print(f"Error initializing orchestrator: {e}", file=__import__("sys").stderr)
        return 2

    try:
        if suite_id == "all":
            result = orchestrator.run_with_evals("all")
        else:
            result = orchestrator.run_with_evals(suite_id)
        score = getattr(result, "overall_score", getattr(result, "score", 0))
        passed = getattr(result, "passed", 0)
        total = getattr(result, "total_cases", 0)
        print(f"Evals: {passed}/{total} passed (score: {score:.4f})")
        from aeos.cli.commands.run_skill import _status_to_exit
        return _status_to_exit(getattr(result, "status", "PASS").value if hasattr(result, "status") else "PASS")
    except Exception as e:
        print(f"Error running evals: {e}", file=__import__("sys").stderr)
        return 2
