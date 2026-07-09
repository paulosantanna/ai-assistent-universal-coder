from __future__ import annotations

from typing import Any


class DelegationPolicyEngine:
    def __init__(self, policy: dict[str, Any]):
        self.policy = policy or {}

    def can_delegate(self, parent_agent: str, child_agent: str, task: dict[str, Any]) -> dict[str, Any]:
        allowed_map = self.policy.get("allowed", {})
        parent_rules = allowed_map.get(parent_agent, {})
        allowed_children = parent_rules.get("can_delegate_to", [])
        denied_children = parent_rules.get("cannot_delegate_to", [])

        if child_agent in denied_children:
            return {"allowed": False, "reason": "child_explicitly_denied"}

        if child_agent not in allowed_children:
            return {"allowed": False, "reason": "child_not_allowlisted"}

        if task.get("risk_level") in ("high", "critical"):
            return {
                "allowed": False,
                "reason": "high_or_critical_risk_requires_escalation",
                "escalation_required": True,
            }

        return {"allowed": True, "reason": "delegation_allowed"}

    def can_self_judge(self, agent_id: str) -> dict[str, Any]:
        return {"allowed": False, "reason": "self_judging_is_forbidden"}
