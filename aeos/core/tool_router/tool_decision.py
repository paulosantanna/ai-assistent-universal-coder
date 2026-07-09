from __future__ import annotations

from aeos.core.tool_router.tool_models import ToolDecision, generate_decision_id, generate_timestamp


def make_decision(
    execution_id: str,
    request_id: str,
    tool_id: str,
    action: str,
    status: str,
    permission_allowed: bool,
    policy_allowed: bool,
    governance_status: str,
    reason: str,
    permission_decision_id: str = "",
    policy_decision_id: str = "",
    evidence_refs: list[str] | None = None,
) -> ToolDecision:
    return ToolDecision(
        decision_id=generate_decision_id(),
        execution_id=execution_id,
        request_id=request_id,
        tool_id=tool_id,
        action=action,
        status=status,
        permission_allowed=permission_allowed,
        policy_allowed=policy_allowed,
        governance_status=governance_status,
        reason=reason,
        permission_decision_id=permission_decision_id,
        policy_decision_id=policy_decision_id,
        evidence_refs=evidence_refs or [],
        timestamp=generate_timestamp(),
    )
