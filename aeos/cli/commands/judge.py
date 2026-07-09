from pathlib import Path
from aeos.core.evidence.execution_resolver import resolve_execution, format_resolved, RESOLVE_LATEST_COMPLETE
from aeos.core.judge.judge_engine import JudgeEngine
from aeos.core.judge.judge_models import JUDGE_STATUS_PASS, JUDGE_STATUS_BLOCKED, JUDGE_STATUS_REVIEW, JUDGE_STATUS_ERROR


def cmd_judge_run(args) -> int:
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

    raw_eid = getattr(args, "execution_id", "latest")
    if raw_eid == "latest":
        execution_id, execution_dir = resolve_execution(target_path, mode=RESOLVE_LATEST_COMPLETE)
    else:
        execution_id = raw_eid
        execution_dir = target_path / ".aeos" / "evidence" / execution_id

    print(format_resolved(execution_id, execution_dir))

    if execution_id == "unknown":
        print("ERROR: No matching execution found for judge evaluation")
        return 2

    evidence_dir = target_path / ".aeos" / "evidence" / execution_id
    reports_dir = target_path / ".aeos" / "reports" / execution_id

    if not evidence_dir.exists():
        print(f"ERROR: Evidence directory not found: {evidence_dir}")
        print("  Judge requires a completed execution with evidence files.")
        return 2

    final_manifest = evidence_dir / "evidence-manifest.json"
    if not final_manifest.exists():
        print(f"ERROR: evidence-manifest.json not found at {final_manifest}")
        print("  Judge evaluation requires a finalized evidence manifest.")
        print("  Missing manifests:")
        for mname in ["runtime-evidence-manifest.json", "eval-evidence-manifest.json",
                       "judge-evidence-manifest.json", "readiness-evidence-manifest.json",
                       "evidence-manifest.json"]:
            mf = evidence_dir / mname
            print(f"    - {mname}: {'FOUND' if mf.exists() else 'MISSING'}")
        print("  Reason: missing_evidence_manifest")
        return 2

    judge_engine = JudgeEngine(workspace_root=str(aeos_root))
    result = judge_engine.evaluate(execution_id, target_path=str(target_path))

    print(f"Judge result: {result.status} (score: {result.score})")

    if result.status == JUDGE_STATUS_ERROR or result.status == JUDGE_STATUS_BLOCKED:
        if result.missing_evidence:
            print("  Missing evidence:")
            for me in result.missing_evidence:
                print(f"    - {me}")
        if result.blocking_rules:
            print("  Blocking rules:")
            for br in result.blocking_rules:
                print(f"    - {br}")
        if result.warnings:
            print("  Warnings:")
            for w in result.warnings:
                print(f"    - {w}")
        if result.recommendations:
            print("  Recommendations:")
            for r in result.recommendations[:5]:
                print(f"    - {r}")

    judge_report = reports_dir / "judge-report.md"
    if judge_report.exists():
        print(f"  Report: {judge_report}")

    from aeos.cli.commands.run_skill import _status_to_exit
    return _status_to_exit(result.status)
