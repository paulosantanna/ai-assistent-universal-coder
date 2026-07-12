"""Honest scoring engine — no silent zeros, no PASS without evidence."""

from __future__ import annotations
from typing import Optional
from .models import AuditStatus, GateResult, AuditReport


def compute_score(gates: dict[str, GateResult]) -> dict:
    """Compute honest score based on executed gates only.
    
    Rules:
    - NOT_EXECUTED gates don't count as zero and don't contribute to PASS.
    - BLOCKED critical gates prevent global PASS.
    - Denominator = total_weight of all gates.
    - Numerator = sum of weights where status is PASS.
    - Score = None when critical coverage is insufficient.
    - Score 10.0 only when ALL critical gates are PASS with evidence.
    """
    total_weight = 0.0
    executed_weight = 0.0
    passed_weight = 0.0
    critical_not_executed = []
    critical_blocked = []
    critical_failed = []

    for gid, gate in gates.items():
        total_weight += gate.weight

        if gate.status == AuditStatus.PASS:
            executed_weight += gate.weight
            passed_weight += gate.weight
        elif gate.status == AuditStatus.FAIL:
            executed_weight += gate.weight
        elif gate.status == AuditStatus.BLOCKED:
            executed_weight += gate.weight
            if gate.critical:
                critical_blocked.append(gid)
        elif gate.status == AuditStatus.NOT_EXECUTED:
            if gate.critical:
                critical_not_executed.append(gid)

    coverage = round(executed_weight / total_weight, 2) if total_weight > 0 else 0.0

    # Determine score
    score: Optional[float] = None
    status = AuditStatus.PASS

    if critical_blocked:
        status = AuditStatus.BLOCKED
        score = None
    elif critical_not_executed:
        status = AuditStatus.BLOCKED
        score = None
    elif executed_weight == 0:
        status = AuditStatus.NOT_EXECUTED
        score = None
    else:
        if passed_weight == executed_weight:
            score = 10.0
            status = AuditStatus.PASS
        else:
            score = round(10.0 * passed_weight / executed_weight, 2)
            status = AuditStatus.FAIL if passed_weight < executed_weight else AuditStatus.PASS

    attempted_gates = sum(1 for g in gates.values() if g.status in (
        AuditStatus.PASS, AuditStatus.FAIL, AuditStatus.BLOCKED
    ))
    completed_gates = sum(1 for g in gates.values() if g.status in (
        AuditStatus.PASS, AuditStatus.FAIL
    ))
    blocked_gates = sum(1 for g in gates.values() if g.status == AuditStatus.BLOCKED)

    return {
        "status": status,
        "score": score,
        "coverage": coverage,
        "executed_gates": attempted_gates,
        "total_gates": len(gates),
        "attempted_gates": attempted_gates,
        "completed_gates": completed_gates,
        "blocked_gates": blocked_gates,
        "critical_not_executed": critical_not_executed,
        "critical_blocked": critical_blocked,
        "critical_failed": critical_failed,
        "executed_weight": executed_weight,
        "total_weight": total_weight,
    }
