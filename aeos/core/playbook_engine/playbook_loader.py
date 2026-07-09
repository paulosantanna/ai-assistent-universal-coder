from __future__ import annotations

from pathlib import Path
from typing import Optional

from aeos.core.playbook_engine.playbook_models import PlaybookContract, PlaybookStep
from aeos.core.playbook_engine.playbook_registry_resolver import PlaybookRegistryResolver


class PlaybookLoader:
    def __init__(self, workspace_root: str = "."):
        self.workspace_root = Path(workspace_root)
        self.resolver = PlaybookRegistryResolver(workspace_root)

    def load_playbook_contract(self, playbook_id: str) -> Optional[PlaybookContract]:
        registry = self.resolver.load()
        entry = registry.get(playbook_id)
        if not entry:
            return None

        playbook_path = entry.get("path", "")
        full_path = self.workspace_root / playbook_path if playbook_path else None

        steps_data = entry.get("steps", [])
        steps = []
        for s in steps_data:
            steps.append(PlaybookStep(
                id=s.get("id", ""),
                skill=s.get("skill"),
                description=s.get("description", ""),
                depends_on=s.get("depends_on", []),
            ))

        return PlaybookContract(
            id=playbook_id,
            objective=entry.get("objective", ""),
            required_agents=entry.get("required_agents", []),
            required_skills=entry.get("required_skills", []),
            required_lcps=entry.get("required_lcps", []),
            allowed_mcps=entry.get("allowed_mcps", []),
            steps=steps,
            blocking_conditions=entry.get("blocking_conditions", []),
            outputs=entry.get("outputs", []),
            final_report_sections=entry.get("final_report_sections", []),
            risk_level=entry.get("risk_level", "low"),
            required_capabilities=entry.get("required_capabilities", []),
            path=str(full_path) if full_path else "",
        )

    def playbook_file_exists(self, playbook_id: str) -> bool:
        path = self.resolver.get_playbook_path(playbook_id)
        if not path:
            return False
        full_path = self.workspace_root / path
        return full_path.exists()

    def list_available_playbooks(self) -> list[str]:
        self.resolver.load()
        return self.resolver.list_playbooks()
