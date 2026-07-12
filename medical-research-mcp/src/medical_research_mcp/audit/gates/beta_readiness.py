"""Gate 15: Beta Readiness — consolidates previous gates without repeating surface scanners."""

from __future__ import annotations
from datetime import datetime, timezone
from ..models import GateResult, AuditStatus


def check_beta_readiness(gates: dict[str, GateResult]) -> GateResult:
    """Gate 15: Consolidate all gate results into a beta readiness verdict.
    
    Does NOT repeat surface scans — relies on previous gate results.
    Blocks readiness if ANY critical gate is FAIL, BLOCKED, or NOT_EXECUTED.
    """
    gate = GateResult(
        id="beta_readiness",
        title="Beta Readiness",
        critical=True,
        weight=1.0,
        started_at=datetime.now(timezone.utc).isoformat(),
    )
    statuses = {gid: g.status for gid, g in gates.items() if g.id != "beta_readiness"}
    
    critical_failures = []
    critical_blocked = []
    critical_not_executed = []
    
    for gid, g in gates.items():
        if g.id == "beta_readiness":
            continue
        if not g.critical:
            continue
        if g.status == AuditStatus.FAIL:
            critical_failures.append(g.id)
        elif g.status == AuditStatus.BLOCKED:
            critical_blocked.append(g.id)
        elif g.status == AuditStatus.NOT_EXECUTED:
            critical_not_executed.append(g.id)
    
    gate.metrics["total_critical_gates"] = len([g for g in gates.values() if g.critical and g.id != "beta_readiness"])
    gate.metrics["critical_failures"] = len(critical_failures)
    gate.metrics["critical_blocked"] = len(critical_blocked)
    gate.metrics["critical_not_executed"] = len(critical_not_executed)
    
    if critical_failures:
        gate.findings.append(f"Critical gates failing: {', '.join(critical_failures)}")
    if critical_blocked:
        gate.findings.append(f"Critical gates blocked: {', '.join(critical_blocked)}")
    if critical_not_executed:
        gate.findings.append(f"Critical gates not executed: {', '.join(critical_not_executed)}")
    
    all_blockers = critical_failures + critical_blocked + critical_not_executed
    if all_blockers:
        gate.status = AuditStatus.BLOCKED
        gate.score = None
        gate.blocked_by = all_blockers
        gate.remediation = [
            f"Resolve critical gate failures: {', '.join(critical_failures)}" if critical_failures else "",
            f"Unblock critical gates: {', '.join(critical_blocked)}" if critical_blocked else "",
            f"Execute critical gates: {', '.join(critical_not_executed)}" if critical_not_executed else "",
        ]
        gate.remediation = [r for r in gate.remediation if r]
    else:
        gate.status = AuditStatus.PASS
        gate.score = 10.0
        gate.findings.append("All critical gates passed — beta readiness confirmed")
    
    gate.finished_at = datetime.now(timezone.utc).isoformat()
    gate.duration_ms = (
        datetime.fromisoformat(gate.finished_at).timestamp()
        - datetime.fromisoformat(gate.started_at).timestamp()
    ) * 1000
    return gate
