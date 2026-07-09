from __future__ import annotations

from typing import Optional

from aeos.core.skill_engine.skill_models import SkillContract
from aeos.core.skill_engine.skill_loader import SkillLoader


class SkillContractValidator:
    def __init__(self, workspace_root: str = "."):
        self.loader = SkillLoader(workspace_root)

    def validate(self, skill_id: str) -> dict[str, any]:
        findings: list[str] = []
        warnings: list[str] = []
        contract = self.loader.load_skill_contract(skill_id)

        if contract is None:
            return {
                "valid": False,
                "skill_id": skill_id,
                "findings": ["Skill not found in registry"],
                "warnings": [],
                "contract": None,
            }

        if not contract.id:
            findings.append("Missing skill id")

        if not contract.mission:
            findings.append("Missing mission")

        if not contract.allowed_actions:
            findings.append("No allowed actions defined")

        if not isinstance(contract.required_inputs, list):
            findings.append("required_inputs must be a list")

        if not isinstance(contract.output_schema, dict):
            findings.append("output_schema must be a dict")

        if not contract.quality_gates:
            findings.append("No quality gates defined")

        if not contract.stop_conditions:
            findings.append("No stop conditions defined")

        if not contract.owner_agent:
            warnings.append("No owner_agent specified")

        if not contract.capabilities:
            warnings.append("No capabilities specified")

        if not self.loader.skill_file_exists(skill_id):
            findings.append(f"Skill file not found at path: {contract.path}")

        return {
            "valid": len(findings) == 0,
            "skill_id": skill_id,
            "findings": findings,
            "warnings": warnings,
            "contract": contract.to_dict() if contract else None,
        }
