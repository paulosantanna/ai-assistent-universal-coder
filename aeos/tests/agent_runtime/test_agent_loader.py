from __future__ import annotations

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..")))

from aeos.core.agent_runtime.agent_loader import AgentLoader, AgentRegistryResolver


class TestAgentLoader:
    def setup_method(self):
        self.loader = AgentLoader(".")

    def test_loader_loads_consolidated_agents(self):
        resolver = AgentRegistryResolver(".")
        registry = resolver.load()
        assert len(registry) > 0, "Should load at least one agent"

    def test_loader_resolves_known_agent(self):
        contract = self.loader.load_agent_contract("root")
        assert contract is not None
        assert contract.id == "root"
        assert contract.role == "root"
        assert len(contract.responsibilities) > 0
        assert len(contract.allowed_actions) > 0
        assert len(contract.capabilities) > 0

    def test_loader_resolves_unknown_agent(self):
        contract = self.loader.load_agent_contract("nonexistent-agent")
        assert contract is None

    def test_agent_file_exists_for_known(self):
        exists = self.loader.agent_file_exists("root")
        assert exists is True

    def test_list_available_agents(self):
        agents = self.loader.list_available_agents()
        assert len(agents) > 0
        assert "root" in agents
        assert "architect" in agents
        assert "judge" in agents

    def test_all_known_agents_have_contracts(self):
        known = ["root", "architect", "coder", "tester", "security", "documenter", "judge", "planner", "devops"]
        for agent_id in known:
            contract = self.loader.load_agent_contract(agent_id)
            assert contract is not None, f"Agent {agent_id} should be loadable"
            assert contract.is_valid(), f"Contract for {agent_id} should be valid"
