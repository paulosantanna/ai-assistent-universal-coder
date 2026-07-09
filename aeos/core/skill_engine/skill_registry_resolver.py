from __future__ import annotations

from pathlib import Path
from typing import Any, Optional

import yaml


class SkillRegistryResolver:
    def __init__(self, workspace_root: str = "."):
        self.workspace_root = Path(workspace_root)
        self._registry: dict[str, dict[str, Any]] = {}

    def load(self) -> dict[str, dict[str, Any]]:
        paths = [
            self.workspace_root / ".aeos" / "derived" / "registries" / "skills.consolidated.yaml",
            self.workspace_root / "aeos" / "registries" / "skills.registry.yaml",
        ]
        for p in paths:
            if p.exists():
                with open(p, "r", encoding="utf-8") as f:
                    data = yaml.safe_load(f) or {}
                entries = data.get("skills", [])
                for entry in entries:
                    eid = entry.get("id")
                    if eid:
                        self._registry[eid] = entry
                return self._registry
        return self._registry

    def resolve(self, skill_id: str) -> Optional[dict[str, Any]]:
        if not self._registry:
            self.load()
        return self._registry.get(skill_id)

    def list_skills(self) -> list[str]:
        return list(self._registry.keys())

    def get_skill_path(self, skill_id: str) -> Optional[str]:
        entry = self.resolve(skill_id)
        if entry:
            return entry.get("path")
        return None

    def get_owner_agent(self, skill_id: str) -> Optional[str]:
        entry = self.resolve(skill_id)
        if entry:
            return entry.get("owner_agent")
        return None

    def get_capabilities(self, skill_id: str) -> list[str]:
        entry = self.resolve(skill_id)
        if entry:
            return entry.get("capabilities", [])
        return []
