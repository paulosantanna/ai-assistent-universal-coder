from __future__ import annotations

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..")))

from aeos.core.playbook_engine.playbook_contract_validator import PlaybookContractValidator


class TestPlaybookContractValidator:
    def setup_method(self):
        self.validator = PlaybookContractValidator(".")

    def test_validates_complete_playbook(self):
        result = self.validator.validate("project-analysis")
        assert result["valid"] is True
        assert result["contract"] is not None

    def test_validates_unknown_playbook(self):
        result = self.validator.validate("nonexistent-playbook")
        assert result["valid"] is False
        assert "Playbook not found in registry" in result["findings"]

    def test_validates_all_known_playbooks(self):
        known = ["project-analysis", "documentation-generation", "security-secrets-audit",
                 "code-change-proposal", "enterprise-project-onboarding"]
        for pid in known:
            result = self.validator.validate(pid)
            assert result["valid"] is True, f"Playbook {pid} should be valid: {result['findings']}"
