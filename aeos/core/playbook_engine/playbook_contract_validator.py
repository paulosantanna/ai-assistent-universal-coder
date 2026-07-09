from __future__ import annotations

from typing import Any

from aeos.core.playbook_engine.playbook_loader import PlaybookLoader


class PlaybookContractValidator:
    def __init__(self, workspace_root: str = "."):
        self.loader = PlaybookLoader(workspace_root)

    def validate(self, playbook_id: str) -> dict[str, Any]:
        findings: list[str] = []
        warnings: list[str] = []
        contract = self.loader.load_playbook_contract(playbook_id)

        if contract is None:
            return {
                "valid": False,
                "playbook_id": playbook_id,
                "findings": ["Playbook not found in registry"],
                "warnings": [],
                "contract": None,
            }

        if not contract.id:
            findings.append("Missing playbook id")

        if not contract.objective:
            findings.append("Missing objective")

        if not contract.required_skills and not contract.steps:
            findings.append("No required skills and no steps defined")

        if not contract.blocking_conditions:
            warnings.append("No blocking conditions defined")

        if not contract.outputs:
            warnings.append("No outputs defined")

        if not contract.required_agents:
            warnings.append("No required agents specified")

        if not self.loader.playbook_file_exists(playbook_id):
            findings.append(f"Playbook file not found at path: {contract.path}")

        return {
            "valid": len(findings) == 0,
            "playbook_id": playbook_id,
            "findings": findings,
            "warnings": warnings,
            "contract": contract.to_dict() if contract else None,
        }
