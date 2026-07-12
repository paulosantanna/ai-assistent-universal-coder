"""AEOS Medical AI Audit V2 — Honest, evidence-based audit framework.

Compatible with legacy `from medical_research_mcp.audit import audit_repository`.
"""

from __future__ import annotations
import json
from pathlib import Path
from .models import (
    AuditStatus,
    EvidenceType,
    EvidenceItem,
    GateResult,
    AuditConfig,
    AuditReport,
    JudgeVerdict,
    CommandRecord,
)
from .orchestrator import run_audit
from .judge import judge_report, judge_gate
from .exclusions import DEFAULT_EXCLUSIONS, build_ignore_patterns

__all__ = [
    "AuditStatus",
    "EvidenceType",
    "EvidenceItem",
    "GateResult",
    "AuditConfig",
    "AuditReport",
    "JudgeVerdict",
    "CommandRecord",
    "run_audit",
    "judge_report",
    "judge_gate",
    "DEFAULT_EXCLUSIONS",
    "build_ignore_patterns",
    "audit_repository",
]


def audit_repository(
    repository: str,
    mode: str = "deep",
    timeout_seconds: int = 900,
    run_tests: bool = True,
    run_security: bool = True,
    run_dependency_audit: bool = True,
    read_only: bool = True,
    max_output_chars: int = 50000,
    verbosity: str = "normal",
    extra_exclusions: list[str] | None = None,
    output: str | None = None,
) -> AuditReport:
    """Unified audit entry point — works as both old facade and new V2 entry point.
    
    Args:
        repository: Path to the repository to audit
        mode: 'structural' (inventory only) or 'deep' (evidence-based)
        timeout_seconds: Maximum execution time
        run_tests: Whether to execute pytest
        run_security: Whether to run security scans
        run_dependency_audit: Whether to run dependency auditing
        read_only: If True, never modifies the audited repository
        max_output_chars: Maximum characters to capture from command output
        verbosity: 'summary', 'normal', or 'full'
        extra_exclusions: Additional exclusion patterns
        output: Path to write the detailed report JSON
    
    Returns:
        AuditReport with results
    """
    config = AuditConfig(
        repository=repository,
        mode=mode,
        timeout_seconds=timeout_seconds,
        run_tests=run_tests,
        run_security=run_security,
        run_dependency_audit=run_dependency_audit,
        read_only=read_only,
        max_output_chars=max_output_chars,
        verbosity=verbosity,
        extra_exclusions=extra_exclusions or [],
    )
    report = run_audit(config)

    if output:
        path = Path(output)
        path.parent.mkdir(parents=True, exist_ok=True)
        report.report_path = str(path.resolve())
        report_bytes = report.model_dump_json(indent=2).encode("utf-8")
        path.write_bytes(report_bytes)
        import hashlib
        report.report_sha256 = hashlib.sha256(report_bytes).hexdigest()

    return report


def cli() -> None:
    """Legacy CLI entry point (via entry_points in pyproject.toml)."""
    import argparse
    import sys

    parser = argparse.ArgumentParser(description="AEOS Medical AI Audit V2")
    parser.add_argument("repository", help="Path to the repository to audit")
    parser.add_argument("--mode", choices=["structural", "deep"], default="structural")
    parser.add_argument("--output", default=None, help="Path to write detailed report")
    parser.add_argument("--timeout", type=int, default=900)
    parser.add_argument("--no-tests", action="store_true")
    parser.add_argument("--no-security", action="store_true")
    parser.add_argument("--no-deps", action="store_true")
    parser.add_argument("--verbosity", choices=["summary", "normal", "full"], default="normal")
    args = parser.parse_args()

    report = audit_repository(
        repository=args.repository,
        mode=args.mode,
        timeout_seconds=args.timeout,
        run_tests=not args.no_tests,
        run_security=not args.no_security,
        run_dependency_audit=not args.no_deps,
        output=args.output,
        verbosity=args.verbosity,
    )

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
        "findings_count": len(report.findings),
    }
    sys.stdout.write(json.dumps(summary, indent=2) + "\n")
