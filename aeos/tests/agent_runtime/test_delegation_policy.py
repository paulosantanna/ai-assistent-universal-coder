from __future__ import annotations

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..")))

from aeos.core.agent_runtime.delegation_policy import DelegationPolicyEngine


class TestDelegationPolicy:
    def setup_method(self):
        self.policy = {
            "allowed": {
                "root": {"can_delegate_to": ["architect", "coder", "judge"], "cannot_delegate_to": []},
                "architect": {"can_delegate_to": ["coder"], "cannot_delegate_to": []},
                "judge": {"can_delegate_to": [], "cannot_delegate_to": []},
            }
        }
        self.engine = DelegationPolicyEngine(self.policy)

    def test_can_delegate_allowed(self):
        result = self.engine.can_delegate("root", "architect", {"risk_level": "low"})
        assert result["allowed"] is True

    def test_cannot_delegate_to_unknown_agent(self):
        result = self.engine.can_delegate("root", "nonexistent", {"risk_level": "low"})
        assert result["allowed"] is False
        assert "child_not_allowlisted" in result["reason"]

    def test_cannot_delegate_from_agent_without_rules(self):
        result = self.engine.can_delegate("judge", "architect", {"risk_level": "low"})
        assert result["allowed"] is False

    def test_blocked_for_high_risk(self):
        result = self.engine.can_delegate("root", "architect", {"risk_level": "high"})
        assert result["allowed"] is False
        assert result.get("escalation_required") is True

    def test_blocked_for_critical_risk(self):
        result = self.engine.can_delegate("root", "architect", {"risk_level": "critical"})
        assert result["allowed"] is False
        assert result.get("escalation_required") is True

    def test_self_judging_blocked(self):
        result = self.engine.can_self_judge("judge")
        assert result["allowed"] is False
        assert "self_judging_is_forbidden" in result["reason"]

    def test_agent_cannot_delegate_to_denied(self):
        result = self.engine.can_delegate("root", "judge", {"risk_level": "low"})
        assert result["allowed"] is not False  # judge is in allowed list

    def test_empty_policy_denies(self):
        engine = DelegationPolicyEngine({})
        result = engine.can_delegate("root", "architect", {})
        assert result["allowed"] is False
