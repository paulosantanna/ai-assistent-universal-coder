from __future__ import annotations

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..")))

from aeos.core.agent_runtime.agent_contract_validator import AgentContractValidator


class TestAgentContractValidator:
    def setup_method(self):
        self.validator = AgentContractValidator(".")

    def test_validates_complete_agent(self):
        result = self.validator.validate("root")
        assert result["valid"] is True
        assert result["contract"] is not None

    def test_validates_unknown_agent(self):
        result = self.validator.validate("nonexistent-agent")
        assert result["valid"] is False
        assert "Agent not found in registry" in result["findings"]

    def test_validates_all_known_agents(self):
        known = ["root", "architect", "coder", "tester", "security", "documenter", "judge", "planner", "devops"]
        for agent_id in known:
            result = self.validator.validate(agent_id)
            assert result["valid"] is True, f"Agent {agent_id} should be valid: {result['findings']}"

    def test_validates_self_delegation_not_allowed(self):
        # root should not be able to delegate to itself
        result = self.validator.validate("root")
        assert result["valid"] is True
        contract_dict = result["contract"]
        if contract_dict:
            allowed_map = contract_dict.get("delegation_policy", {}).get("allowed", {})
            agent_id = contract_dict.get("id", "")
            if agent_id in allowed_map:
                can_delegate_to = allowed_map[agent_id].get("can_delegate_to", [])
                assert agent_id not in can_delegate_to, "Agent should not delegate to itself"
