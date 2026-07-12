"""CLI entry point for Medical AI Audit V2.

Usage:
  py -3 -m medical_research_mcp.audit <repository> [--mode deep] [--output report.json]
"""

from __future__ import annotations
import argparse
import json
import sys
from pathlib import Path
from . import audit_repository


def main() -> None:
    parser = argparse.ArgumentParser(
        description="AEOS Medical AI Audit V2 — Honest, evidence-based audit"
    )
    parser.add_argument("repository", help="Path to the repository to audit")
    parser.add_argument("--mode", choices=["structural", "deep"], default="structural",
                        help="Audit mode: structural (inventory only) or deep (evidence-based)")
    parser.add_argument("--output", default=None, help="Path to write detailed report JSON")
    parser.add_argument("--timeout", type=int, default=900, help="Timeout in seconds")
    parser.add_argument("--no-tests", action="store_true", help="Skip test execution")
    parser.add_argument("--no-security", action="store_true", help="Skip security scan")
    parser.add_argument("--no-deps", action="store_true", help="Skip dependency audit")
    parser.add_argument("--verbosity", choices=["summary", "normal", "full"], default="normal",
                        help="Output verbosity level")
    parser.add_argument("--max-output", type=int, default=50000, help="Max output chars per command")

    args = parser.parse_args()

    repo_path = Path(args.repository).resolve()
    if not repo_path.is_dir():
        print(f"Error: Repository path not found: {args.repository}", file=sys.stderr)
        sys.exit(1)

    report = audit_repository(
        repository=str(repo_path),
        mode=args.mode,
        timeout_seconds=args.timeout,
        run_tests=not args.no_tests,
        run_security=not args.no_security,
        run_dependency_audit=not args.no_deps,
        read_only=True,
        max_output_chars=args.max_output,
        verbosity=args.verbosity,
        output=args.output,
    )

    # Print executive summary to stdout
    summary = {
        "target": report.target,
        "mode": report.mode,
        "status": report.status.value,
        "score": report.score,
        "coverage": report.coverage,
        "executed_gates": report.executed_gates,
        "total_gates": report.total_gates,
        "attempted_gates": report.attempted_gates,
        "completed_gates": report.completed_gates,
        "blocked_gates": report.blocked_gates,
        "critical_not_executed": report.critical_not_executed,
        "critical_blocked": report.critical_blocked,
        "executive_summary": report.executive_summary,
        "report_path": report.report_path,
        "report_sha256": report.report_sha256,
        "findings_count": len(report.findings),
    }
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
