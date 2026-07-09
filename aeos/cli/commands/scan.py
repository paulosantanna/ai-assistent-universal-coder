import sys
import json
import time
from pathlib import Path
from datetime import datetime, timezone

from aeos.core.scanner.fast_repo_scanner import FastRepoScanner
from aeos.core.scanner.exclusions import DEFAULT_EXCLUDE_PATTERNS


def _format_bytes(b: int) -> str:
    for unit in ("B", "KB", "MB", "GB"):
        if b < 1024:
            return f"{b:.1f} {unit}"
        b /= 1024
    return f"{b:.1f} TB"


def cmd_scan(args) -> int:
    from aeos.cli.main import resolve_target_path

    target = resolve_target_path(args)
    if not target.exists():
        print(f"Target not found: {target}", file=sys.stderr)
        return 2

    exclude = DEFAULT_EXCLUDE_PATTERNS
    if hasattr(args, "exclude") and args.exclude:
        exclude = list(exclude) + list(args.exclude)

    max_file_mb = getattr(args, "max_file_mb", 10)
    metadata_only_large_files = getattr(args, "metadata_only_large_files", True)
    respect_gitignore = getattr(args, "respect_gitignore", False)

    scanner = FastRepoScanner(
        root=target,
        exclude=exclude,
        max_file_mb=max_file_mb,
        metadata_only_large_files=metadata_only_large_files,
        respect_gitignore=respect_gitignore,
    )

    print(f"Scanning: {target}")
    print(f"  Exclude patterns: {len(scanner.exclude_patterns)}")
    if scanner.exclude_patterns:
        for p in sorted(scanner.exclude_patterns):
            print(f"    - {p}")
    print()

    stats = scanner.scan()

    print("--- Scan Results ---")
    print(f"  Files inspected:     {stats.total_files}")
    print(f"  Files ignored:       {stats.ignored_files}")
    print(f"  Directories ignored: {len(stats.ignored_dirs)}")
    if stats.ignored_dirs:
        for d in sorted(stats.ignored_dirs)[:10]:
            print(f"    - {d}/")
        if len(stats.ignored_dirs) > 10:
            print(f"    ... and {len(stats.ignored_dirs) - 10} more")
    print(f"  Files scanned:       {stats.scanned_files}")
    print(f"  Python files:        {stats.python_files}")
    print(f"  Config files:        {stats.config_files}")
    print(f"  Metadata-only files: {stats.metadata_only_files}")
    print(f"  Bytes read:          {_format_bytes(stats.scanned_bytes)}")
    print(f"  Execution time:      {stats.elapsed_seconds:.2f}s")
    print(f"  Inflated:            {'YES' if stats.inflated else 'NO'}")

    if stats.top_20_dirs:
        print()
        print("--- Top 20 Heaviest Directories ---")
        print(f"  {'Directory':<50} {'Files':>8} {'Size':>12}")
        for dirname, fcount, fbytes in stats.top_20_dirs:
            print(f"  {dirname:<50} {fcount:>8} {_format_bytes(fbytes):>12}")

    report = _generate_report(target, scanner.exclude_patterns, stats)

    reports_dir = target / ".aeos" / "reports"
    reports_dir.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    report_path = reports_dir / f"scan-report-{timestamp}.md"
    report_path.write_text(report, encoding="utf-8")
    print(f"\nReport: {report_path}")

    _store_evidence(target, stats)

    if stats.inflated:
        return 3
    return 0


def _generate_report(target: Path, exclude_patterns: list[str], stats) -> str:
    lines = ["# AEOS Scan Report", ""]
    lines.append(f"- **Target**: {target}")
    lines.append(f"- **Timestamp**: {datetime.now(timezone.utc).isoformat()}")
    lines.append(f"- **Duration**: {stats.elapsed_seconds:.2f}s")
    lines.append("")

    lines.append("## Exclusion Patterns")
    lines.append("")
    for p in sorted(exclude_patterns):
        lines.append(f"- `{p}`")
    lines.append("")

    lines.append("## Statistics")
    lines.append("")
    lines.append("| Metric | Value |")
    lines.append("|--------|-------|")
    lines.append(f"| Files inspected (before exclusion) | {stats.total_files} |")
    lines.append(f"| Files ignored by exclusion | {stats.ignored_files} |")
    lines.append(f"| Directories ignored | {len(stats.ignored_dirs)} |")
    lines.append(f"| Files scanned (after exclusion) | {stats.scanned_files} |")
    lines.append(f"| Python files | {stats.python_files} |")
    lines.append(f"| Config files (yaml/json) | {stats.config_files} |")
    lines.append(f"| Metadata-only files (large) | {stats.metadata_only_files} |")
    lines.append(f"| Bytes read | {stats.scanned_bytes} |")
    lines.append(f"| Formatted size | {_format_bytes(stats.scanned_bytes)} |")
    lines.append(f"| Execution time | {stats.elapsed_seconds:.2f}s |")
    lines.append(f"| Inflated | {'YES' if stats.inflated else 'NO'} |")
    lines.append("")

    if stats.top_20_dirs:
        lines.append("## Top 20 Heaviest Directories")
        lines.append("")
        lines.append("| Directory | Files | Size |")
        lines.append("|-----------|-------|------|")
        for dirname, fcount, fbytes in stats.top_20_dirs:
            lines.append(f"| {dirname} | {fcount} | {_format_bytes(fbytes)} |")
        lines.append("")

    verdict = "PASS" if not stats.inflated else "REVIEW"
    lines.append(f"## Verdict: {verdict}")
    lines.append("")
    if stats.inflated:
        lines.append("**Scan appears inflated.** Consider adding more exclusion patterns or increasing `--max-file-mb`.")
    else:
        lines.append("Scan results within expected range.")
    lines.append("")

    return "\n".join(lines)


def _store_evidence(target: Path, stats):
    try:
        from aeos.core.evidence.store import EvidenceStore
        store = EvidenceStore(str(target))
        exec_id = f"scan-{datetime.now(timezone.utc).strftime('%Y%m%d-%H%M%S')}"
        store.write_tool_call(exec_id, {"command": "scan"}, {
            "total_files": stats.total_files,
            "ignored_files": stats.ignored_files,
            "ignored_dirs": len(stats.ignored_dirs),
            "scanned_files": stats.scanned_files,
            "python_files": stats.python_files,
            "config_files": stats.config_files,
            "scanned_bytes": stats.scanned_bytes,
            "elapsed_seconds": round(stats.elapsed_seconds, 2),
            "inflated": stats.inflated,
        })
    except Exception:
        pass
