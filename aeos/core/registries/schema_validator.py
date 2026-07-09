from __future__ import annotations

from pathlib import Path
from typing import Optional

import yaml

from aeos.core.registries.registry_models import (
    ConsolidatedRegistry,
    SchemaValidationResult,
)


class SchemaValidator:
    def __init__(self, workspace_root: str = "."):
        self.workspace_root = Path(workspace_root).resolve()
        self._capabilities: set[str] = set()

    def load_capabilities(self, capabilities_path: str = "aeos/config/capabilities.yaml") -> set[str]:
        full_path = self.workspace_root / capabilities_path
        if not full_path.exists():
            return set()
        with open(full_path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
        caps = data.get("capabilities", []) if data else []
        self._capabilities = set(caps)
        return self._capabilities

    def validate(self, registry: ConsolidatedRegistry) -> SchemaValidationResult:
        result = SchemaValidationResult(valid=True)

        for agent_id, agent in registry.agents.items():
            if not agent_id:
                result.errors.append("Agent entry with empty id")
                result.valid = False

        for skill_id, skill in registry.skills.items():
            if not skill_id:
                result.errors.append("Skill entry with empty id")
                result.valid = False
            if self._capabilities:
                unknown = [c for c in skill.capabilities if c not in self._capabilities]
                for cap in unknown:
                    result.warnings.append(f"Skill '{skill_id}' references unknown capability '{cap}'")
                    result.unknown_capabilities.add(cap)

        for playbook_id, playbook in registry.playbooks.items():
            if not playbook_id:
                result.errors.append("Playbook entry with empty id")
                result.valid = False

        for mcp_id, mcp in registry.mcps.items():
            if not mcp_id:
                result.errors.append("MCP entry with empty id")
                result.valid = False
            if self._capabilities:
                unknown = [c for c in mcp.capabilities if c not in self._capabilities]
                for cap in unknown:
                    result.warnings.append(f"MCP '{mcp_id}' references unknown capability '{cap}'")
                    result.unknown_capabilities.add(cap)

        for lcp_id, lcp in registry.lcps.items():
            if not lcp_id:
                result.errors.append("LCP entry with empty id")
                result.valid = False

        return result
