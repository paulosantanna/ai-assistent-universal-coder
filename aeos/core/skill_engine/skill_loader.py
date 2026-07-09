from __future__ import annotations

from pathlib import Path
from typing import Optional

import yaml

from aeos.core.skill_engine.skill_models import SkillContract
from aeos.core.skill_engine.skill_registry_resolver import SkillRegistryResolver


class SkillLoader:
    def __init__(self, workspace_root: str = "."):
        self.workspace_root = Path(workspace_root)
        self.resolver = SkillRegistryResolver(workspace_root)

    def load_skill_contract(self, skill_id: str) -> Optional[SkillContract]:
        registry = self.resolver.load()
        entry = registry.get(skill_id)
        if not entry:
            return None

        skill_path = entry.get("path", "")
        full_path = self.workspace_root / skill_path if skill_path else None

        mission = entry.get("mission", "")
        allowed_actions = entry.get("allowed_actions", [])
        forbidden_actions = entry.get("forbidden_actions", [])
        required_inputs = entry.get("required_inputs", [])
        output_schema = entry.get("output_schema", {})
        quality_gates = entry.get("quality_gates", [])
        stop_conditions = entry.get("stop_conditions", [])
        owner_agent = entry.get("owner_agent", "")
        capabilities = entry.get("capabilities", [])
        risk_level = entry.get("risk_level", "low")

        return SkillContract(
            id=skill_id,
            mission=mission,
            allowed_actions=allowed_actions,
            forbidden_actions=forbidden_actions,
            required_inputs=required_inputs,
            output_schema=output_schema,
            quality_gates=quality_gates,
            stop_conditions=stop_conditions,
            owner_agent=owner_agent,
            capabilities=capabilities,
            risk_level=risk_level,
            path=str(full_path) if full_path else "",
        )

    def skill_file_exists(self, skill_id: str) -> bool:
        path = self.resolver.get_skill_path(skill_id)
        if not path:
            return False
        full_path = self.workspace_root / path
        return full_path.exists()

    def list_available_skills(self) -> list[str]:
        self.resolver.load()
        return self.resolver.list_skills()
