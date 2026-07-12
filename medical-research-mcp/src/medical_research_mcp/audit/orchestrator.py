"""Audit orchestrator — structural and deep modes with proper lifecycle."""

from __future__ import annotations
import asyncio
import hashlib
import json
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .models import AuditConfig, AuditReport, AuditStatus, GateResult
from .scoring import compute_score
from .judge import judge_gate, judge_report
from .exclusions import build_ignore_patterns
from .gates import (
    check_repository_hygiene,
    check_architecture,
    check_imports,
    check_tests,
    check_rag,
    check_training,
    check_continual_learning,
    check_simulation,
    check_security,
    check_dependencies,
    check_privacy,
    check_governance,
    check_observability,
    check_documentation,
    check_beta_readiness,
)


GATE_REGISTRY: dict[str, Any] = {
    "repository_hygiene": check_repository_hygiene,
    "architecture": check_architecture,
    "imports_and_compilation": check_imports,
    "test_execution": check_tests,
    "rag_quality": check_rag,
    "training_pipeline": check_training,
    "continual_learning": check_continual_learning,
    "simulation": check_simulation,
    "security": check_security,
    "dependency_security": check_dependencies,
    "privacy": check_privacy,
    "governance": check_governance,
    "observability": check_observability,
    "documentation": check_documentation,
    "beta_readiness": check_beta_readiness,
}

STRUCTURAL_GATES: list[str] = [
    "repository_hygiene",
    "architecture",
    "rag_quality",
    "training_pipeline",
    "continual_learning",
    "simulation",
    "security",
    "privacy",
    "governance",
    "observability",
    "documentation",
]

ASYNC_GATES: set[str] = {"imports_and_compilation", "test_execution", "dependency_security"}


def _build_executive_summary(report: AuditReport) -> str:
    parts = [
        f"Audit mode: {report.mode}",
        f"Status: {report.status.value}",
    ]
    if report.mode == "structural":
        parts.append("STRUCTURAL MODE: Inventory only. No quality scores, no readiness claims. DISCOVERY_COMPLETED.")
    if report.score is not None:
        parts.append(f"Score: {report.score}/10")
    if report.coverage is not None:
        parts.append(f"Coverage: {report.coverage:.0%}")
    parts.append(f"Gates: {report.attempted_gates} attempted, {report.completed_gates} completed, {report.blocked_gates} blocked, {report.total_gates} total")
    if report.critical_not_executed:
        parts.append(f"Critical NOT_EXECUTED: {', '.join(report.critical_not_executed)}")
    if report.critical_blocked:
        parts.append(f"Critical BLOCKED: {', '.join(report.critical_blocked)}")
    if report.findings:
        parts.append(f"Key findings: {len(report.findings)}")
    return " | ".join(parts)


def _run_structural(config: AuditConfig) -> AuditReport:
    """Structural mode: fast inventory only — no scores, no readiness claims.
    
    Uses a SINGLE fast file scan to avoid 15x full-tree iteration on large repos.
    """
    started = datetime.now(timezone.utc)
    root = Path(config.repository).resolve()
    gates_result: dict[str, GateResult] = {}

    # Single fast inventory pass
    py_files = 0
    md_files = 0
    test_dirs = 0
    config_files = 0
    total_files = 0

    if root.is_dir():
        for p in root.rglob("*"):
            if not p.is_file():
                continue
            rel = str(p.relative_to(root)).replace("\\", "/")
            from .exclusions import should_ignore
            if should_ignore(rel):
                continue
            total_files += 1
            if p.suffix == ".py":
                py_files += 1
            if p.suffix == ".md":
                md_files += 1
            if p.suffix in {".yaml", ".yml", ".toml", ".json"}:
                config_files += 1
        test_dir = root / "tests"
        test_dirs = 1 if test_dir.is_dir() else 0

    # Create minimal gate results from inventory
    for gid in STRUCTURAL_GATES:
        gate = GateResult(
            id=gid,
            title=gid.replace("_", " ").title(),
            status=AuditStatus.NOT_APPLICABLE,
            score=None,
            started_at=started.isoformat(),
            finished_at=datetime.now(timezone.utc).isoformat(),
        )
        gate.metrics["structural_inventory"] = {
            "total_files": total_files,
            "python_files": py_files,
            "documentation_files": md_files,
            "config_files": config_files,
            "has_tests_directory": bool(test_dirs),
        }
        gates_result[gid] = gate

    finished = datetime.now(timezone.utc)
    duration_ms = (finished.timestamp() - started.timestamp()) * 1000

    all_findings = []
    for g in gates_result.values():
        all_findings.extend(g.findings)

    report = AuditReport(
        target=str(root),
        mode="structural",
        started_at=started.isoformat(),
        finished_at=finished.isoformat(),
        duration_ms=duration_ms,
        status=AuditStatus.NOT_EXECUTED,
        score=None,
        coverage=0.0,
        executed_gates=0,
        total_gates=len(GATE_REGISTRY),
        critical_not_executed=[],
        gates=gates_result,
        executive_summary="STRUCTURAL MODE: Inventory only. No quality scores, no readiness claims. DISCOVERY_COMPLETED.",
        findings=["STRUCTURAL MODE: This is an inventory scan, not a readiness assessment. No gates were executed."],
        limitations=[
            "Structural mode does not execute any tests or validate functionality",
            "No quality scores are produced in structural mode",
            "File presence does not imply feature completeness",
            "Run --mode deep for actual evidence-based audit",
        ],
    )
    report.executive_summary = _build_executive_summary(report)
    return report


async def _run_deep(config: AuditConfig) -> AuditReport:
    """Deep mode: execute real gates, collect evidence, produce honest scores."""
    started = datetime.now(timezone.utc)
    root = Path(config.repository).resolve()

    ignore_patterns = build_ignore_patterns(config.extra_exclusions)
    gates_result: dict[str, GateResult] = {}
    timeout = config.timeout_seconds
    max_out = config.max_output_chars

    # Run sync gates first
    sync_gates = [gid for gid in GATE_REGISTRY if gid not in ASYNC_GATES and gid != "beta_readiness"]
    for gid in sync_gates:
        fn = GATE_REGISTRY.get(gid)
        if fn is None:
            continue
        try:
            if gid == "security":
                result = fn(config.repository, run_scan=config.run_security, max_output_chars=max_out)
            else:
                result = fn(config.repository)
            # Apply judge to each gate
            judged = judge_gate(result)
            gates_result[gid] = judged if judged else result
        except Exception as e:
            gates_result[gid] = GateResult(
                id=gid,
                title=gid.replace("_", " ").title(),
                status=AuditStatus.BLOCKED,
                score=None,
                findings=[f"Gate execution error: {e}"],
                critical=True,
            )

    # Run async gates
    for gid in ASYNC_GATES:
        fn = GATE_REGISTRY.get(gid)
        if fn is None:
            continue
        try:
            kwargs = {"repository": config.repository, "max_output_chars": max_out}
            if gid == "test_execution":
                kwargs["timeout_seconds"] = min(timeout, 300)
            if gid == "dependency_security":
                kwargs["run_audit"] = config.run_dependency_audit

            import inspect
            if inspect.iscoroutinefunction(fn):
                result = await fn(**kwargs)
            else:
                result = fn(**kwargs)

            judged = judge_gate(result)
            gates_result[gid] = judged if judged else result
        except Exception as e:
            gates_result[gid] = GateResult(
                id=gid,
                title=gid.replace("_", " ").title(),
                status=AuditStatus.BLOCKED,
                score=None,
                findings=[f"Gate execution error: {e}"],
                critical=True,
            )

    # Beta readiness — consolidate
    gates_result["beta_readiness"] = check_beta_readiness(gates_result)

    # Compute honest score
    score_info = compute_score(gates_result)

    all_findings = []
    for g in gates_result.values():
        all_findings.extend(g.findings)

    finished = datetime.now(timezone.utc)
    duration_ms = (finished.timestamp() - started.timestamp()) * 1000

    report = AuditReport(
        target=str(root),
        mode="deep",
        started_at=started.isoformat(),
        finished_at=finished.isoformat(),
        duration_ms=duration_ms,
        status=score_info["status"],
        score=score_info["score"],
        coverage=score_info["coverage"],
        executed_gates=score_info["executed_gates"],
        total_gates=score_info["total_gates"],
        attempted_gates=score_info["attempted_gates"],
        completed_gates=score_info["completed_gates"],
        blocked_gates=score_info["blocked_gates"],
        critical_not_executed=score_info.get("critical_not_executed", []),
        critical_blocked=score_info.get("critical_blocked", []),
        gates=gates_result,
        findings=all_findings[:50],
        limitations=[
            "Deep audit executes real commands but does not run training or long simulations",
            "Evidence is based on static analysis and test execution",
            "Security audit uses git grep and static patterns — not a full penetration test",
            "Clinical readiness requires domain expert review beyond automated gates",
        ],
    )

    # Run Judge on the full report
    verdict = judge_report(report)
    if not verdict.accepted:
        report.findings.append(f"JUDGE: {'; '.join(verdict.reasons)}")
        if verdict.adjusted_score is not None and verdict.adjusted_score != report.score:
            report.score = verdict.adjusted_score
        if verdict.adjusted_status is not None and verdict.adjusted_status != report.status:
            report.status = verdict.adjusted_status
        if verdict.evidence_issues:
            report.limitations.extend(verdict.evidence_issues[:5])
        if verdict.score_issues:
            report.findings.extend(verdict.score_issues[:5])

    report.executive_summary = _build_executive_summary(report)
    return report


def run_audit(config: AuditConfig) -> AuditReport:
    """Main entry point — dispatches to structural or deep mode."""
    if config.mode == "structural":
        return _run_structural(config)
    elif config.mode == "deep":
        return asyncio.run(_run_deep(config))
    else:
        raise ValueError(f"Unknown audit mode: {config.mode}. Use 'structural' or 'deep'.")
