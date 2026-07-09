from __future__ import annotations

from pathlib import Path
from typing import Optional

import yaml

from aeos.core.permissions.permission_models import PermissionConfig, RoleCapabilityMapping


class CapabilityLoader:
    def __init__(self, workspace_root: str = "."):
        self.workspace_root = Path(workspace_root).resolve()
        self.config: Optional[PermissionConfig] = None
        self._known_capabilities: set[str] = set()

    def load(self, permissions_path: str = "aeos/config/permissions.yaml") -> PermissionConfig:
        full = self.workspace_root / permissions_path
        if not full.exists():
            raise FileNotFoundError(f"Permissions file not found: {full}")

        with open(full, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)

        default_mode = data.get("default", "deny")
        roles_raw = data.get("roles", {})
        approval_actions = data.get("approval_required", [])

        roles_map: dict[str, RoleCapabilityMapping] = {}
        for role_name, role_data in roles_raw.items():
            caps = role_data.get("capabilities", [])
            roles_map[role_name] = RoleCapabilityMapping(role=role_name, capabilities=caps)

        self.config = PermissionConfig(
            default=default_mode,
            roles=roles_map,
            approval_required_actions=approval_actions,
        )
        return self.config

    def load_capabilities_list(self, capabilities_path: str = "aeos/config/capabilities.yaml") -> set[str]:
        full = self.workspace_root / capabilities_path
        if not full.exists():
            return set()
        with open(full, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
        caps = data.get("capabilities", []) if data else []
        self._known_capabilities = set(caps)
        return self._known_capabilities

    def is_known_capability(self, capability: str) -> bool:
        return capability in self._known_capabilities

    def get_role_capabilities(self, role: str) -> list[str]:
        if not self.config:
            return []
        mapping = self.config.roles.get(role)
        if not mapping:
            return []
        return mapping.capabilities
