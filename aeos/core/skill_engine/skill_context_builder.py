from __future__ import annotations

from typing import Any

from aeos.core.skill_engine.skill_models import SkillRequest, SkillContract


class SkillContextBuilder:
    def build(self, request: SkillRequest, contract: SkillContract) -> dict[str, Any]:
        return {
            "execution_id": request.execution_id,
            "skill_id": request.skill_id,
            "actor": request.actor,
            "role": request.role,
            "input": request.input,
            "contract": contract.to_dict() if contract else {},
            "allowed_actions": contract.allowed_actions if contract else [],
            "forbidden_actions": contract.forbidden_actions if contract else [],
            "quality_gates": contract.quality_gates if contract else [],
            "stop_conditions": contract.stop_conditions if contract else [],
            "capabilities": contract.capabilities if contract else [],
            "risk_level": contract.risk_level if contract else "low",
            "context_refs": request.context_refs,
            "evidence_refs": request.evidence_refs,
            "approval_id": request.approval_id,
        }
