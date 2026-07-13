from __future__ import annotations

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..")))

from aeos.core.skill_engine.skill_loader import SkillLoader
from aeos.core.skill_engine.skill_registry_resolver import SkillRegistryResolver


class TestSkillLoader:
    def setup_method(self):
        self.loader = SkillLoader(".")

    def test_loader_loads_consolidated_skills(self):
        SkillRegistryResolver.clear_cache()
        resolver = SkillRegistryResolver(".")
        registry = resolver.load()
        assert len(registry) > 0, "Should load at least one skill"
        assert SkillRegistryResolver.cache_size() >= 1

    def test_registry_resolver_reuses_shared_cache(self):
        SkillRegistryResolver.clear_cache()
        first = SkillRegistryResolver(".")
        second = SkillRegistryResolver(".")

        first_registry = first.load()
        cache_size = SkillRegistryResolver.cache_size()
        second_registry = second.load()

        assert cache_size >= 1
        assert SkillRegistryResolver.cache_size() == cache_size
        assert first_registry.keys() == second_registry.keys()

    def test_loader_reuses_contract_instance(self):
        contract_a = self.loader.load_skill_contract("repo-scanner")
        contract_b = self.loader.load_skill_contract("repo-scanner")

        assert contract_a is contract_b

    def test_loader_resolves_known_skill(self):
        contract = self.loader.load_skill_contract("repo-scanner")
        assert contract is not None
        assert contract.id == "repo-scanner"
        assert contract.mission != ""
        assert len(contract.allowed_actions) > 0
        assert len(contract.quality_gates) > 0
        assert len(contract.stop_conditions) > 0

    def test_loader_resolves_unknown_skill(self):
        contract = self.loader.load_skill_contract("nonexistent-skill")
        assert contract is None

    def test_skill_file_exists_for_known_skill(self):
        exists = self.loader.skill_file_exists("repo-scanner")
        assert exists is True

    def test_skill_file_not_exists_for_unknown(self):
        exists = self.loader.skill_file_exists("nonexistent-skill")
        assert exists is False

    def test_list_available_skills(self):
        skills = self.loader.list_available_skills()
        assert len(skills) > 0
        assert "repo-scanner" in skills
        assert "architecture-mapper" in skills

    def test_loader_loads_all_known_skills(self):
        known = ["repo-scanner", "architecture-mapper", "documentation", "security-audit",
                 "test-generation", "code-analyzer", "patch-planner", "dependency-analyzer",
                 "packaging"]
        for skill_id in known:
            contract = self.loader.load_skill_contract(skill_id)
            assert contract is not None, f"Skill {skill_id} should be loadable"
            assert contract.is_valid(), f"Contract for {skill_id} should be valid"
