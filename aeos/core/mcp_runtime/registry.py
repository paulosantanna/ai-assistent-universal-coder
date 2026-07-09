"""AEOS MCP Registry — resolves MCP definitions from registry YAML."""

from pathlib import Path
from typing import Any
from .contracts import MCPDefinition


class MCPRegistry:
    def __init__(self, registry_path: str | Path):
        self.registry_path = Path(registry_path)
        self._mcps: dict[str, MCPDefinition] = {}
        self._allowlist: dict[str, set[str]] = {}

    def load(self):
        import yaml
        if not self.registry_path.exists():
            raise FileNotFoundError(f"MCP registry not found: {self.registry_path}")
        raw = yaml.safe_load(self.registry_path.read_text(encoding="utf-8"))
        for entry in raw.get("mcps", []):
            mcp = MCPDefinition(
                id=entry["id"],
                type=entry.get("type", "unknown"),
                transport=entry.get("transport", "stdio"),
                config_path=entry.get("config", ""),
                risk_level=entry.get("risk_level", "low"),
                capabilities=entry.get("capabilities", []),
                tools=entry.get("tools", []),
                enabled=entry.get("enabled", True),
                approval_required=entry.get("approval_required", False),
            )
            self._mcps[mcp.id] = mcp
            self._allowlist[mcp.id] = set(entry.get("tools", []))

    def resolve(self, mcp_id: str) -> MCPDefinition | None:
        return self._mcps.get(mcp_id)

    def is_tool_allowed(self, mcp_id: str, tool_name: str) -> bool:
        allowed = self._allowlist.get(mcp_id)
        if allowed is None:
            return False
        return tool_name in allowed

    def list_enabled(self) -> list[dict[str, Any]]:
        result = []
        for mcp in self._mcps.values():
            if getattr(mcp, "enabled", True):
                result.append({"id": mcp.id, "type": mcp.type, "risk_level": mcp.risk_level, "tools": mcp.tools})
        return result