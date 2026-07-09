from __future__ import annotations

from aeos.core.governance.governance_models import (
    GOV_STATUS_BLOCKED,
    GOV_STATUS_PASS,
    GOV_STATUS_WAITING_APPROVAL,
    GovernanceRequest,
    GovernanceResult,
    now_iso,
)
from aeos.core.permissions.permission_engine import PermissionEngine
from aeos.core.permissions.permission_models import PermissionRequest
from aeos.core.policy.policy_engine import PolicyEngine
from aeos.core.policy.policy_models import PolicyRequest


class GovernanceGate:
    def __init__(self, workspace_root: str = "."):
        self.workspace_root = workspace_root
        self.permission_engine = PermissionEngine(workspace_root)
        self.policy_engine = PolicyEngine(workspace_root)
        self.results: list[GovernanceResult] = []

    def initialize(self) -> None:
        self.permission_engine.initialize()
        self.policy_engine.initialize()

    def evaluate(self, request: GovernanceRequest) -> GovernanceResult:
        perm_req = PermissionRequest(
            execution_id=request.execution_id,
            actor=request.actor,
            role=request.role,
            action=request.action,
            capability=request.capability,
            resource=request.resource,
        )
        perm_decision = self.permission_engine.evaluate(perm_req)

        pol_req = PolicyRequest(
            execution_id=request.execution_id,
            action=request.action,
            resource=request.resource,
            command=request.command,
            branch=request.branch,
            details=request.details,
        )
        pol_decision = self.policy_engine.evaluate(pol_req)

        blocking_reasons: list[str] = []
        evidence_refs: list[str] = []

        evidence_refs.append(perm_decision.decision_id)
        evidence_refs.append(pol_decision.decision_id)

        if not perm_decision.allowed:
            blocking_reasons.append(f"Permission denied: {perm_decision.reason}")

        if not pol_decision.allowed:
            blocking_reasons.append(f"Policy denied: {pol_decision.reason}")

        requires_approval = perm_decision.requires_approval
        approval_present = request.approval_present

        if requires_approval and not approval_present:
            blocking_reasons.append("Action requires approval but no approval is present")

        if len(blocking_reasons) > 0:
            has_security_block = not perm_decision.allowed or not pol_decision.allowed
            if has_security_block:
                status = GOV_STATUS_BLOCKED
            elif requires_approval and not approval_present:
                status = GOV_STATUS_WAITING_APPROVAL
            else:
                status = GOV_STATUS_BLOCKED
        else:
            status = GOV_STATUS_PASS

        result = GovernanceResult(
            execution_id=request.execution_id,
            action=request.action,
            status=status,
            permission_allowed=perm_decision.allowed,
            policy_allowed=pol_decision.allowed,
            requires_approval=requires_approval,
            approval_present=approval_present,
            blocking_reasons=blocking_reasons,
            evidence_refs=evidence_refs,
            timestamp=now_iso(),
            permission_decision_id=perm_decision.decision_id,
            policy_decision_id=pol_decision.decision_id,
        )

        self.results.append(result)
        return result
