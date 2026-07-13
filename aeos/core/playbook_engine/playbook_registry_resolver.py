from __future__ import annotations

from pathlib import Path
from typing import Any, Optional

import yaml


class PlaybookRegistryResolver:
    def __init__(self, workspace_root: str = "."):
        self.workspace_root = Path(workspace_root)
        self._registry: dict[str, dict[str, Any]] = {}

    def load(self) -> dict[str, dict[str, Any]]:
        paths = [
            self.workspace_root / ".aeos" / "derived" / "registries" / "playbooks.consolidated.yaml",
            self.workspace_root / "aeos" / "registries" / "playbooks.registry.yaml",
            self.workspace_root / "aeos" / "registries" / "enterprise-playbooks.registry.yaml",
            self.workspace_root / "aeos" / "registries" / "playbooks.v0_6.additions.yaml",
            self.workspace_root / "aeos" / "registries" / "playbooks.v0_7.additions.yaml",
            self.workspace_root / "aeos" / "registries" / "playbooks.v0_8_to_v1_0.additions.yaml",
            self.workspace_root / "aeos" / "registries" / "playbooks.v1_1_enterprise.additions.yaml",
        ]
        for p in paths:
            if not p.exists():
                continue
            with open(p, "r", encoding="utf-8-sig") as f:
                data = yaml.safe_load(f) or {}
            entries = data.get("playbooks", [])
            for entry in entries:
                eid = entry.get("id")
                if eid and eid not in self._registry:
                    self._registry[eid] = entry
        return self._registry

    def resolve(self, playbook_id: str) -> Optional[dict[str, Any]]:
        if not self._registry:
            self.load()
        return self._registry.get(playbook_id)

    def list_playbooks(self) -> list[str]:
        return list(self._registry.keys())

    def get_playbook_path(self, playbook_id: str) -> Optional[str]:
        entry = self.resolve(playbook_id)
        if entry:
            return entry.get("path")
        return None

    def get_required_skills(self, playbook_id: str) -> list[str]:
        entry = self.resolve(playbook_id)
        if entry:
            return entry.get("required_skills", [])
        return []

    def get_required_agents(self, playbook_id: str) -> list[str]:
        entry = self.resolve(playbook_id)
        if entry:
            return entry.get("required_agents", [])
        return []

    def get_required_lcps(self, playbook_id: str) -> list[str]:
        entry = self.resolve(playbook_id)
        if entry:
            return entry.get("required_lcps", [])
        return []

    def get_allowed_mcps(self, playbook_id: str) -> list[str]:
        entry = self.resolve(playbook_id)
        if entry:
            return entry.get("allowed_mcps", [])
        return []
