from __future__ import annotations

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..")))

from aeos.core.playbook_engine.playbook_loader import PlaybookLoader
from aeos.core.playbook_engine.playbook_registry_resolver import PlaybookRegistryResolver


class TestPlaybookLoader:
    def setup_method(self):
        self.loader = PlaybookLoader(".")

    def test_loader_loads_consolidated_playbooks(self):
        resolver = PlaybookRegistryResolver(".")
        registry = resolver.load()
        assert len(registry) > 0, "Should load at least one playbook"

    def test_loader_resolves_known_playbook(self):
        contract = self.loader.load_playbook_contract("project-analysis")
        assert contract is not None
        assert contract.id == "project-analysis"
        assert contract.objective != ""
        assert len(contract.steps) > 0

    def test_loader_resolves_unknown_playbook(self):
        contract = self.loader.load_playbook_contract("nonexistent-playbook")
        assert contract is None

    def test_playbook_file_exists_for_known(self):
        exists = self.loader.playbook_file_exists("project-analysis")
        assert exists is True

    def test_list_available_playbooks(self):
        playbooks = self.loader.list_available_playbooks()
        assert len(playbooks) > 0
        assert "project-analysis" in playbooks

    def test_enterprise_playbook_loaded(self):
        contract = self.loader.load_playbook_contract("enterprise-project-onboarding")
        assert contract is not None
        assert contract.id == "enterprise-project-onboarding"
        assert "repo-scanner" in contract.required_skills
