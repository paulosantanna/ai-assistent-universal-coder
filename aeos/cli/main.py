import sys
import os
import argparse
from pathlib import Path
from aeos.core.evidence.execution_resolver import (
    resolve_execution,
    format_resolved,
    RESOLVE_LATEST_COMPLETE,
    RESOLVE_LATEST_JUDGE,
    RESOLVE_LATEST_RUNTIME,
    RESOLVE_LATEST_ANY,
)


def main():
    parser = argparse.ArgumentParser(
        prog="aeos",
        description="AEOS Chief Staff - AI Engineering Operations Suite",
    )
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    def add_aeos_root(sp) -> None:
        sp.add_argument("--aeos-root", default=None, help="AEOS root directory (default: auto-detect from CWD)")
        return sp

    # init
    init_parser = subparsers.add_parser("init", help="Initialize AEOS workspace")
    init_parser.set_defaults(func="cmd_init")

    # doctor
    doctor_parser = subparsers.add_parser("doctor", help="Run system diagnostics")
    add_aeos_root(doctor_parser)
    doctor_parser.set_defaults(func="cmd_doctor")

    # scan
    scan_parser = subparsers.add_parser("scan", help="Scan target for analysis")
    scan_parser.add_argument("--target", default=".", help="Target directory to scan")
    scan_parser.add_argument("--exclude", action="append", default=[], help="Additional exclude pattern (repeatable)")
    scan_parser.add_argument("--max-file-mb", type=int, default=10, help="Max file size in MB before metadata-only (default: 10)")
    scan_parser.add_argument("--no-metadata-only", dest="metadata_only_large_files", action="store_false", help="Do not separate large files as metadata-only")
    scan_parser.add_argument("--respect-gitignore", action="store_true", help="Respect .gitignore patterns")
    scan_parser.set_defaults(func="cmd_scan")

    # skill
    skill_parser = subparsers.add_parser("skill", help="Skill commands")
    skill_sub = skill_parser.add_subparsers(dest="skill_command")
    skill_run = skill_sub.add_parser("run", help="Run a skill")
    add_aeos_root(skill_run)
    skill_run.add_argument("skill_id", help="Skill identifier")
    skill_run.add_argument("--target", default=".", help="Target directory")
    skill_run.add_argument("--dry-run", action="store_true", help="Dry run mode")
    skill_run.set_defaults(func="cmd_skill_run")

    # playbook
    playbook_parser = subparsers.add_parser("playbook", help="Playbook commands")
    playbook_sub = playbook_parser.add_subparsers(dest="playbook_command")
    playbook_run = playbook_sub.add_parser("run", help="Run a playbook")
    add_aeos_root(playbook_run)
    playbook_run.add_argument("playbook_id", help="Playbook identifier")
    playbook_run.add_argument("--target", default=".", help="Target directory")
    playbook_run.add_argument("--dry-run", action="store_true", help="Dry run mode")
    playbook_run.set_defaults(func="cmd_playbook_run")

    # agent
    agent_parser = subparsers.add_parser("agent", help="Agent commands")
    agent_sub = agent_parser.add_subparsers(dest="agent_command")
    agent_run = agent_sub.add_parser("run", help="Run an agent task")
    add_aeos_root(agent_run)
    agent_run.add_argument("agent_id", help="Agent identifier")
    agent_run.add_argument("--objective", required=True, help="Agent objective")
    agent_run.add_argument("--target", default=".", help="Target directory")
    agent_run.add_argument("--dry-run", action="store_true", help="Dry run mode")
    agent_run.set_defaults(func="cmd_agent_run")

    # judge
    judge_parser = subparsers.add_parser("judge", help="Judge commands")
    judge_sub = judge_parser.add_subparsers(dest="judge_command")
    judge_run = judge_sub.add_parser("run", help="Run judge evaluation")
    add_aeos_root(judge_run)
    judge_run.add_argument("--execution-id", default="latest", help="Execution ID")
    judge_run.set_defaults(func="cmd_judge_run")

    # evals
    evals_parser = subparsers.add_parser("evals", help="Eval commands")
    evals_sub = evals_parser.add_subparsers(dest="evals_command")
    evals_run = evals_sub.add_parser("run", help="Run eval suites")
    evals_run.add_argument("--suite", default="all", help="Suite ID or 'all'")
    evals_run.set_defaults(func="cmd_evals_run")

    # readiness
    readiness_parser = subparsers.add_parser("readiness", help="Readiness commands")
    readiness_sub = readiness_parser.add_subparsers(dest="readiness_command")
    readiness_run = readiness_sub.add_parser("run", help="Run readiness audit")
    readiness_run.set_defaults(func="cmd_readiness_run")

    # package
    package_parser = subparsers.add_parser("package", help="Package commands")
    package_sub = package_parser.add_subparsers(dest="package_command")
    pkg_create = package_sub.add_parser("create", help="Create execution package")
    pkg_create.add_argument("--execution-id", default="latest", help="Execution ID")
    pkg_create.set_defaults(func="cmd_package_create")
    pkg_verify = package_sub.add_parser("verify", help="Verify package")
    pkg_verify.add_argument("--path", required=True, help="Path to package ZIP")
    pkg_verify.set_defaults(func="cmd_package_verify")

    # registry
    registry_parser = subparsers.add_parser("registry", help="Registry commands")
    registry_sub = registry_parser.add_subparsers(dest="registry_command")
    registry_validate = registry_sub.add_parser("validate", help="Validate registry")
    registry_validate.set_defaults(func="cmd_registry_validate")
    rl = registry_sub.add_parser("list", help="List registry entities")
    rl.add_argument("entity", nargs="?", default="all",
                    choices=["skills", "playbooks", "agents", "mcps", "lcps", "all"],
                    help="Entity type to list")
    rl.set_defaults(func="cmd_registry_list")

    # evidence
    evidence_parser = subparsers.add_parser("evidence", help="Evidence commands")
    evidence_sub = evidence_parser.add_subparsers(dest="evidence_command")
    ev_list = evidence_sub.add_parser("list", help="List evidence")
    ev_list.set_defaults(func="cmd_evidence_list")
    ev_verify = evidence_sub.add_parser("verify", help="Verify evidence")
    ev_verify.add_argument("--execution-id", default="latest", help="Execution ID")
    ev_verify.add_argument("--allow-partial", action="store_true", help="Allow partial (missing manifest) without blocking")
    ev_verify.add_argument("--execution-mode", default=RESOLVE_LATEST_COMPLETE,
                           choices=[RESOLVE_LATEST_ANY, RESOLVE_LATEST_COMPLETE, RESOLVE_LATEST_JUDGE, RESOLVE_LATEST_RUNTIME],
                           help="How to resolve 'latest' execution")
    ev_verify.set_defaults(func="cmd_evidence_verify")
    ev_report = evidence_sub.add_parser("report", help="Evidence report")
    ev_report.add_argument("--execution-id", default="latest", help="Execution ID")
    ev_report.set_defaults(func="cmd_evidence_report")

    # version
    version_parser = subparsers.add_parser("version", help="Show version")
    version_parser.set_defaults(func="cmd_version")

    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        sys.exit(2)

    func_name = args.func
    handler = getattr(sys.modules[__name__], func_name, None)
    if handler:
        try:
            exit_code = handler(args)
            sys.exit(exit_code if exit_code is not None else 0)
        except Exception as e:
            print(f"Error: {e}", file=sys.stderr)
            sys.exit(2)
    else:
        print(f"Unknown command: {func_name}", file=sys.stderr)
        sys.exit(2)


def get_workspace_root(args) -> Path:
    target = getattr(args, "target", ".")
    return Path(target).resolve()


def resolve_aeos_root(args) -> Path:
    explicit = getattr(args, "aeos_root", None)
    if isinstance(explicit, str) and explicit:
        return Path(explicit).resolve()
    env_root = os.environ.get("AEOS_ROOT", "")
    if env_root:
        return Path(env_root).resolve()
    target = get_workspace_root(args)
    from aeos.core.runtime.path_resolver import _autodetect_aeos_root
    detected = _autodetect_aeos_root()
    if detected != Path.cwd().resolve():
        return detected
    return target


def resolve_target_path(args) -> Path:
    return get_workspace_root(args)


def get_execution_id(args) -> str:
    eid = getattr(args, "execution_id", "latest")
    if eid != "latest":
        return eid
    mode = getattr(args, "execution_mode", RESOLVE_LATEST_COMPLETE)
    eid_resolved, _ = resolve_execution(get_workspace_root(args), mode=mode)
    return eid_resolved


def resolve_latest_execution(workspace_root: Path, mode: str = RESOLVE_LATEST_COMPLETE) -> str:
    eid, _ = resolve_execution(workspace_root, mode=mode)
    return eid


# Command handlers - each returns an exit code

from aeos.cli.commands.init import cmd_init
from aeos.cli.commands.doctor import cmd_doctor
from aeos.cli.commands.scan import cmd_scan
from aeos.cli.commands.run_skill import cmd_skill_run
from aeos.cli.commands.run_playbook import cmd_playbook_run
from aeos.cli.commands.run_agent import cmd_agent_run
from aeos.cli.commands.judge import cmd_judge_run
from aeos.cli.commands.evals import cmd_evals_run
from aeos.cli.commands.readiness import cmd_readiness_run
from aeos.cli.commands.package import cmd_package_create, cmd_package_verify
from aeos.cli.commands.registry import cmd_registry_validate, cmd_registry_list
from aeos.cli.commands.evidence import cmd_evidence_list, cmd_evidence_verify, cmd_evidence_report
from aeos.cli.commands.version import cmd_version


if __name__ == "__main__":
    main()
