from __future__ import annotations

from pathlib import Path
from typing import Optional

import yaml

from aeos.core.agent_runtime.agent_models import AgentContract


class AgentRegistryResolver:
    def __init__(self, workspace_root: str = "."):
        self.workspace_root = Path(workspace_root)
        self._registry: dict[str, dict] = {}

    def load(self) -> dict[str, dict]:
        paths = [
            self.workspace_root / ".aeos" / "derived" / "registries" / "agents.consolidated.yaml",
            self.workspace_root / "aeos" / "registries" / "agents.registry.yaml",
        ]
        for p in paths:
            if p.exists():
                with open(p, "r", encoding="utf-8") as f:
                    data = yaml.safe_load(f) or {}
                entries = data.get("agents", [])
                for entry in entries:
                    eid = entry.get("id")
                    if eid:
                        self._registry[eid] = entry
                return self._registry
        return self._registry

    def resolve(self, agent_id: str) -> Optional[dict]:
        if not self._registry:
            self.load()
        return self._registry.get(agent_id)

    def list_agents(self) -> list[str]:
        return list(self._registry.keys())

    def get_agent_path(self, agent_id: str) -> Optional[str]:
        entry = self.resolve(agent_id)
        if entry:
            return entry.get("path")
        return None


class AgentLoader:
    def __init__(self, workspace_root: str = "."):
        self.workspace_root = Path(workspace_root)
        self.resolver = AgentRegistryResolver(workspace_root)

    def load_agent_contract(self, agent_id: str) -> Optional[AgentContract]:
        registry = self.resolver.load()
        entry = registry.get(agent_id)
        if not entry:
            return None

        agent_path = entry.get("path", "")
        full_path = self.workspace_root / agent_path if agent_path else None

        delegation_policy = entry.get("delegation_policy", {})
        if not isinstance(delegation_policy, dict):
            delegation_policy = {}

        return AgentContract(
            id=agent_id,
            role=entry.get("role", ""),
            responsibilities=entry.get("responsibilities", []),
            allowed_actions=entry.get("allowed_actions", []),
            forbidden_actions=entry.get("forbidden_actions", []),
            capabilities=entry.get("capabilities", []),
            delegation_policy=delegation_policy,
            output_schema=entry.get("output_schema", {}),
            stop_conditions=entry.get("stop_conditions", []),
            path=str(full_path) if full_path else "",
        )

    def agent_file_exists(self, agent_id: str) -> bool:
        path = self.resolver.get_agent_path(agent_id)
        if not path:
            return False
        full_path = self.workspace_root / path
        return full_path.exists()

    def list_available_agents(self) -> list[str]:
        self.resolver.load()
        return self.resolver.list_agents()
