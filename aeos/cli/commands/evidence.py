from pathlib import Path
from aeos.core.evidence.execution_resolver import resolve_execution, format_resolved, RESOLVE_LATEST_COMPLETE

MANIFEST_NAMES = [
    "runtime-evidence-manifest.json",
    "eval-evidence-manifest.json",
    "judge-evidence-manifest.json",
    "readiness-evidence-manifest.json",
    "evidence-manifest.json",
]


def cmd_evidence_list(args) -> int:
    from aeos.cli.main import resolve_target_path
    target_path = resolve_target_path(args)
    evidence_dir = target_path / ".aeos" / "evidence"
    if not evidence_dir.exists():
        print("No evidence directory found")
        return 0
    exec_dirs = sorted(
        [d for d in evidence_dir.iterdir() if d.is_dir()],
        key=lambda d: d.stat().st_mtime, reverse=True,
    )
    print("Execution IDs:")
    for d in exec_dirs:
        files = list(d.iterdir())
        manifest = d / "evidence-manifest.json"
        has_manifest = " [manifest]" if manifest.exists() else ""
        print(f"  - {d.name} ({len(files)} files{has_manifest})")
    if not exec_dirs:
        print("  (none)")
    return 0


def _check_manifest(mf: Path) -> tuple[str, str]:
    """Returns (label, status). status is PASS/FAIL/SKIP."""
    name = mf.name
    if not mf.exists():
        return name, "SKIP"
    try:
        from aeos.core.evidence.evidence_manifest import verify_staged_manifest
        result = verify_staged_manifest(mf)
        if result.get("passed"):
            return name, "PASS"
        errors = result.get("file_errors", [])
        return name, f"FAIL ({'; '.join(errors)})"
    except Exception as e:
        return name, f"FAIL ({e})"


def cmd_evidence_verify(args) -> int:
    from aeos.cli.main import resolve_target_path, get_execution_id
    target_path = resolve_target_path(args)
    mode = getattr(args, "execution_mode", RESOLVE_LATEST_COMPLETE)

    raw_eid = getattr(args, "execution_id", "latest")
    if raw_eid == "latest":
        execution_id, execution_dir = resolve_execution(target_path, mode=mode)
    else:
        execution_id = raw_eid
        execution_dir = target_path / ".aeos" / "evidence" / execution_id

    print(format_resolved(execution_id, execution_dir))

    if execution_id == "unknown":
        print("ERROR: No matching execution found")
        return 2

    execution_dir_resolved = target_path / ".aeos" / "evidence" / execution_id
    if not execution_dir_resolved.exists():
        print(f"Execution directory not found: {execution_dir_resolved}")
        return 2

    allow_partial = getattr(args, "allow_partial", False)

    results: list[tuple[str, str]] = []
    for name in MANIFEST_NAMES:
        mf = execution_dir_resolved / name
        label, status = _check_manifest(mf)
        results.append((label, status))
        print(f"  {label}: {status}")

    has_final_manifest = (execution_dir_resolved / "evidence-manifest.json").exists()

    skips = sum(1 for _, s in results if s == "SKIP")
    fails = sum(1 for _, s in results if not s.startswith("PASS") and s != "SKIP")

    if has_final_manifest and fails == 0:
        print("Evidence verification: PASS")
        return 0

    if skips == 5:
        if allow_partial:
            print("Evidence verification: REVIEW (no manifests found, --allow-partial)")
            return 3
        print("Evidence verification: BLOCKED (no manifests found)")
        return 1

    if not has_final_manifest and not allow_partial:
        print("Evidence verification: BLOCKED (evidence-manifest.json not found)")
        return 1

    if fails > 0:
        print("Evidence verification: FAIL")
        return 1

    if allow_partial:
        print("Evidence verification: REVIEW (partial, --allow-partial)")
        return 3

    print("Evidence verification: PASS")
    return 0


def cmd_evidence_report(args) -> int:
    from aeos.cli.main import resolve_target_path, get_execution_id
    target_path = resolve_target_path(args)
    execution_id = get_execution_id(args)
    execution_dir = target_path / ".aeos" / "evidence" / execution_id
    if not execution_dir.exists():
        print(f"Execution directory not found: {execution_dir}", file=__import__("sys").stderr)
        return 2
    try:
        files = list(execution_dir.iterdir())
        manifests = [f.name for f in files if f.name.endswith("-manifest.json")]
        line = ["# AEOS Evidence Report", "", f"- **Execution ID**: {execution_id}", f"- **Directory**: {execution_dir}", f"- **Total Files**: {len(files)}", "", "## Manifests", ""]
        for m in manifests:
            line.append(f"- {m}")
        line.extend(["", "## Files", ""])
        for f in sorted(files):
            if f.is_file():
                line.append(f"- {f.name} ({f.stat().st_size} bytes)")
        report = "\n".join(line)
        report_dir = target_path / ".aeos" / "reports"
        report_dir.mkdir(parents=True, exist_ok=True)
        report_path = report_dir / f"evidence-report-{execution_id}.md"
        report_path.write_text(report, encoding="utf-8")
        print(report)
        print(f"Report saved: {report_path}")
        return 0
    except Exception as e:
        print(f"Evidence report error: {e}", file=__import__("sys").stderr)
        return 2
