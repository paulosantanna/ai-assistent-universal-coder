from pathlib import Path

from aeos.core.playbook_engine.playbook_contract_validator import PlaybookContractValidator
from aeos.core.skill_engine.skill_contract_validator import SkillContractValidator


MANTIS_SKILLS = ["mantis-architecture", "mantis-calibrate", "mantis-chain", "mantis-critic", "mantis-dedupe", "mantis-history", "mantis-meta-agent", "mantis-patch", "mantis-pipeline-adapter", "mantis-plan", "mantis-reflect", "mantis-report", "mantis-reproduce", "mantis-researcher", "mantis-review", "mantis-structural-index", "mantis-summarize", "mantis-threat-model"]


def test_mantis_skills_are_registered_and_have_original_contracts():
    workspace = Path(__file__).resolve().parents[3]
    validator = SkillContractValidator(str(workspace))
    for skill_id in MANTIS_SKILLS:
        result = validator.validate(skill_id)
        assert result["valid"] is True, (skill_id, result["findings"])
        original = workspace / "skills" / "mantis" / skill_id / "references" / "ORIGINAL_SKILL.md"
        assert original.exists(), skill_id


def test_mantis_playbook_is_registered():
    workspace = Path(__file__).resolve().parents[3]
    result = PlaybookContractValidator(str(workspace)).validate("mantis")
    assert result["valid"] is True, result["findings"]
    assert "mantis-review" in result["contract"]["required_skills"]
