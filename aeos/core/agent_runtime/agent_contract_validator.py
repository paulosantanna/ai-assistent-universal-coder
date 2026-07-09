from __future__ import annotations

from typing import Any

from aeos.core.agent_runtime.agent_loader import AgentLoader


class AgentContractValidator:
    def __init__(self, workspace_root: str = "."):
        self.loader = AgentLoader(workspace_root)

    def validate(self, agent_id: str) -> dict[str, Any]:
        findings: list[str] = []
        warnings: list[str] = []
        contract = self.loader.load_agent_contract(agent_id)

        if contract is None:
            return {
                "valid": False,
                "agent_id": agent_id,
                "findings": ["Agent not found in registry"],
                "warnings": [],
                "contract": None,
            }

        if not contract.id:
            findings.append("Missing agent id")

        if not contract.role:
            findings.append("Missing role")

        if not contract.responsibilities:
            findings.append("No responsibilities defined")

        if not contract.allowed_actions:
            findings.append("No allowed actions defined")

        if not contract.capabilities:
            warnings.append("No capabilities specified")

        if not isinstance(contract.delegation_policy, dict):
            findings.append("delegation_policy must be a dict")

        if contract.delegation_policy:
            allowed_map = contract.delegation_policy.get("allowed", {})
            if contract.id in allowed_map:
                can_delegate_to = allowed_map[contract.id].get("can_delegate_to", [])
                if contract.id in can_delegate_to:
                    findings.append("Agent cannot delegate to itself")

        if not self.loader.agent_file_exists(agent_id):
            findings.append(f"Agent file not found at path: {contract.path}")

        return {
            "valid": len(findings) == 0,
            "agent_id": agent_id,
            "findings": findings,
            "warnings": warnings,
            "contract": contract.to_dict() if contract else None,
        }
