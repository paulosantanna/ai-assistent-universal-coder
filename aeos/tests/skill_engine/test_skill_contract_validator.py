from __future__ import annotations

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..")))

from aeos.core.skill_engine.skill_contract_validator import SkillContractValidator


class TestSkillContractValidator:
    def setup_method(self):
        self.validator = SkillContractValidator(".")

    def test_validates_complete_skill(self):
        result = self.validator.validate("repo-scanner")
        assert result["valid"] is True
        assert result["contract"] is not None

    def test_validates_unknown_skill(self):
        result = self.validator.validate("nonexistent-skill")
        assert result["valid"] is False
        assert "Skill not found in registry" in result["findings"]

    def test_validates_all_known_skills(self):
        known = ["repo-scanner", "architecture-mapper", "documentation", "security-audit",
                 "test-generation", "code-analyzer", "patch-planner", "dependency-analyzer",
                 "packaging"]
        for skill_id in known:
            result = self.validator.validate(skill_id)
            assert result["valid"] is True, f"Skill {skill_id} should be valid: {result['findings']}"
