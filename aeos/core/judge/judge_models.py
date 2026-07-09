from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Optional
from uuid import uuid4

JUDGE_STATUS_PASS = "PASS"
JUDGE_STATUS_BLOCKED = "BLOCKED"
JUDGE_STATUS_ERROR = "ERROR"
JUDGE_STATUS_REVIEW = "REVIEW"

JudgeStatus = str  # "PASS" | "BLOCKED" | "ERROR" | "REVIEW"


@dataclass
class JudgeInput:
    execution_id: str
    target_path: str = "."
    evidence_manifest_path: str = ""
    reports: list[dict[str, Any]] = field(default_factory=list)
    permission_decisions: list[dict[str, Any]] = field(default_factory=list)
    policy_decisions: list[dict[str, Any]] = field(default_factory=list)
    governance_decisions: list[dict[str, Any]] = field(default_factory=list)
    tool_results: list[dict[str, Any]] = field(default_factory=list)
    skill_results: list[dict[str, Any]] = field(default_factory=list)
    playbook_results: list[dict[str, Any]] = field(default_factory=list)
    agent_results: list[dict[str, Any]] = field(default_factory=list)
    runtime_results: list[dict[str, Any]] = field(default_factory=list)
    claims: list[dict[str, Any]] = field(default_factory=list)
    approval_refs: list[dict[str, Any]] = field(default_factory=list)
    package_refs: list[dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "execution_id": self.execution_id,
            "target_path": self.target_path,
            "evidence_manifest_path": self.evidence_manifest_path,
            "reports": self.reports,
            "permission_decisions": self.permission_decisions,
            "policy_decisions": self.policy_decisions,
            "governance_decisions": self.governance_decisions,
            "tool_results": self.tool_results,
            "skill_results": self.skill_results,
            "playbook_results": self.playbook_results,
            "agent_results": self.agent_results,
            "runtime_results": self.runtime_results,
            "claims": self.claims,
            "approval_refs": self.approval_refs,
            "package_refs": self.package_refs,
        }


@dataclass
class BlockingRule:
    rule_id: str
    severity: str  # "critical" | "high" | "medium" | "low"
    category: str
    description: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "rule_id": self.rule_id,
            "severity": self.severity,
            "category": self.category,
            "description": self.description,
        }


@dataclass
class JudgeFinding:
    rule_id: str
    status: str  # "PASS" | "FAIL" | "SKIPPED"
    detail: str = ""
    evidence_ref: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "rule_id": self.rule_id,
            "status": self.status,
            "detail": self.detail,
            "evidence_ref": self.evidence_ref,
        }


@dataclass
class JudgeResult:
    execution_id: str
    status: JudgeStatus
    score: float = 0.0
    blocking_rules: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    facts_validated: list[str] = field(default_factory=list)
    claims_rejected: list[str] = field(default_factory=list)
    missing_evidence: list[str] = field(default_factory=list)
    security_findings: list[str] = field(default_factory=list)
    policy_findings: list[str] = field(default_factory=list)
    permission_findings: list[str] = field(default_factory=list)
    performance_findings: list[str] = field(default_factory=list)
    recommendations: list[str] = field(default_factory=list)
    evidence_refs: list[str] = field(default_factory=list)
    timestamp: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "execution_id": self.execution_id,
            "status": self.status,
            "score": self.score,
            "blocking_rules": self.blocking_rules,
            "warnings": self.warnings,
            "facts_validated": self.facts_validated,
            "claims_rejected": self.claims_rejected,
            "missing_evidence": self.missing_evidence,
            "security_findings": self.security_findings,
            "policy_findings": self.policy_findings,
            "permission_findings": self.permission_findings,
            "performance_findings": self.performance_findings,
            "recommendations": self.recommendations,
            "evidence_refs": self.evidence_refs,
            "timestamp": self.timestamp,
        }


@dataclass
class JudgeScorecard:
    execution_id: str
    status: JudgeStatus
    overall_score: float = 0.0
    categories: dict[str, float] = field(default_factory=dict)
    findings: list[dict[str, Any]] = field(default_factory=list)
    critical_blockers: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "execution_id": self.execution_id,
            "status": self.status,
            "overall_score": self.overall_score,
            "categories": self.categories,
            "findings": self.findings,
            "critical_blockers": self.critical_blockers,
            "warnings": self.warnings,
        }


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def generate_judge_id() -> str:
    return f"judge-{uuid4().hex[:12]}"
