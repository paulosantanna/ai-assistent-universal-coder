"""Independent Judge — validates evidence integrity and score honesty.

The Judge does NOT edit the main implementation.
It can: maintain, reduce, invalidate, or block.
It CANNOT: increase scores or promote status.
"""

from __future__ import annotations
from datetime import datetime, timezone
from typing import Optional
from .models import AuditStatus, AuditReport, GateResult, JudgeVerdict, EvidenceType


def _ev_attr(ev, attr: str):
    """Get attribute from dict-like or object-like evidence."""
    if isinstance(ev, dict):
        return ev.get(attr, "")
    return getattr(ev, attr, "")


def _check_evidence_integrity(gate: GateResult) -> list[str]:
    issues = []
    for ev in gate.evidence:
        ev_sha = _ev_attr(ev, "sha256")
        ev_type = _ev_attr(ev, "type")
        ev_source = _ev_attr(ev, "source")
        ev_summary = _ev_attr(ev, "summary")
        if not ev_sha and ev_type in {EvidenceType.FILE_HASH.value, EvidenceType.COMMAND_OUTPUT.value, EvidenceType.TEST_REPORT.value}:
            issues.append(f"Evidence missing SHA-256: {ev_source}")
        if not ev_source:
            issues.append(f"Evidence missing source reference")
        if not ev_summary:
            issues.append(f"Evidence missing summary: {ev_source}")
    return issues


def _check_score_consistency(gate: GateResult) -> list[str]:
    issues = []
    if gate.status == AuditStatus.PASS:
        if not gate.evidence:
            issues.append(f"Gate '{gate.id}' is PASS but has no evidence")
        if gate.score is None:
            issues.append(f"Gate '{gate.id}' is PASS but score is None")
        elif gate.score != 10.0:
            issues.append(f"Gate '{gate.id}' is PASS but score ({gate.score}) != 10.0")
    if gate.status == AuditStatus.FAIL and gate.score is None:
        issues.append(f"Gate '{gate.id}' is FAIL but score is None (should be numeric)")
    if gate.status == AuditStatus.BLOCKED and gate.score is not None:
        issues.append(f"Gate '{gate.id}' is BLOCKED but has score {gate.score} (should be None)")
    if gate.status == AuditStatus.NOT_EXECUTED and gate.score is not None:
        issues.append(f"Gate '{gate.id}' is NOT_EXECUTED but has score {gate.score} (should be None)")
    return issues


def _check_contradictions(gate: GateResult) -> list[str]:
    issues = []
    if gate.status == AuditStatus.PASS and gate.findings:
        blocking_findings = [f for f in gate.findings if any(kw in f.lower() for kw in {"fail", "error", "missing", "block", "issue"})]
        if blocking_findings:
            issues.append(f"Gate '{gate.id}' is PASS but has negative findings: {blocking_findings[:3]}")
    return issues


def _check_reproducibility(gate: GateResult) -> list[str]:
    issues = []
    if gate.status in (AuditStatus.PASS, AuditStatus.FAIL) and not gate.commands:
        if gate.status == AuditStatus.PASS:
            issues.append(f"Gate '{gate.id}' has no commands recorded — result may not be reproducible")
    return issues


def judge_gate(gate: GateResult) -> Optional[GateResult]:
    """Judge a single gate result. Returns corrected gate or None if unchanged."""
    issues = []
    issues.extend(_check_evidence_integrity(gate))
    issues.extend(_check_score_consistency(gate))
    issues.extend(_check_contradictions(gate))
    issues.extend(_check_reproducibility(gate))

    if not issues:
        return None

    corrected = gate.model_copy(deep=True)
    downgraded = False

    # Downgrade PASS without evidence to FAIL
    if gate.status == AuditStatus.PASS and not gate.evidence:
        corrected.status = AuditStatus.FAIL
        corrected.score = 0.0
        corrected.findings.append("JUDGE: Downgraded from PASS to FAIL — no evidence provided")
        downgraded = True

    # Downgrade PASS with contradictory findings
    if gate.status == AuditStatus.PASS and any("fail" in f.lower() or "error" in f.lower() for f in gate.findings):
        corrected.status = AuditStatus.FAIL
        corrected.score = min(corrected.score or 10.0, 5.0)
        corrected.findings.append("JUDGE: Score reduced — contradictions between status and findings")
        downgraded = True

    # Invalidate BLOCKED that was promoted to PASS
    if gate.status == AuditStatus.PASS and any("block" in f.lower() for f in gate.findings):
        corrected.status = AuditStatus.BLOCKED
        corrected.score = None
        corrected.findings.append("JUDGE: Invalidated PASS — findings indicate blocked state")
        downgraded = True

    # Downgrade PASS with evidence integrity issues
    if gate.status == AuditStatus.PASS:
        ev_issues = _check_evidence_integrity(gate)
        if ev_issues:
            has_hash_issues = any("SHA-256" in e for e in ev_issues)
            if has_hash_issues:
                corrected.status = AuditStatus.FAIL
                corrected.score = min(corrected.score or 10.0, 5.0)
                corrected.findings.append(f"JUDGE: Downgraded — evidence integrity issues: {'; '.join(ev_issues[:3])}")
                downgraded = True

    if downgraded:
        return corrected
    return None


def judge_report(report: AuditReport) -> JudgeVerdict:
    """Perform independent review of the entire audit report.
    
    The Judge validates evidence, score consistency, and contradictions.
    It produces a verdict but does NOT modify the report directly.
    """
    reasons = []
    evidence_issues = []
    score_issues = []
    contradiction_issues = []
    adjusted_score = report.score
    adjusted_status = report.status

    for gid, gate in report.gates.items():
        ev_issues = _check_evidence_integrity(gate)
        sc_issues = _check_score_consistency(gate)
        ct_issues = _check_contradictions(gate)

        evidence_issues.extend(f"{gid}: {e}" for e in ev_issues)
        score_issues.extend(f"{gid}: {e}" for e in sc_issues)
        contradiction_issues.extend(f"{gid}: {e}" for e in ct_issues)

    if evidence_issues:
        reasons.append(f"Evidence issues found: {len(evidence_issues)}")
    if score_issues:
        reasons.append(f"Score consistency issues: {len(score_issues)}")
    if contradiction_issues:
        reasons.append(f"Status contradictions: {len(contradiction_issues)}")

    # Determine if the report needs adjustment
    needs_adjustment = bool(evidence_issues or score_issues or contradiction_issues)

    if needs_adjustment:
        # Check if score should be invalidated
        if report.score == 10.0 and (evidence_issues or score_issues):
            adjusted_score = None
            adjusted_status = AuditStatus.BLOCKED
            reasons.append("Score 10.0 rejected — evidence or score issues found")
        elif report.score is not None and score_issues:
            adjusted_score = min(report.score, 5.0) if report.score else None
            if adjusted_score is not None and adjusted_score < report.score:
                reasons.append(f"Score reduced from {report.score} to {adjusted_score} due to score issues")

    accepted = not needs_adjustment

    return JudgeVerdict(
        accepted=accepted,
        original_score=report.score,
        adjusted_score=adjusted_score,
        original_status=report.status,
        adjusted_status=adjusted_status,
        reasons=reasons,
        evidence_issues=evidence_issues[:20],
        score_issues=score_issues[:20],
        contradiction_issues=contradiction_issues[:20],
    )
