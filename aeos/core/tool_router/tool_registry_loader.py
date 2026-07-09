from __future__ import annotations

from pathlib import Path
from typing import Any, Optional

import yaml

from aeos.core.tool_router.tool_models import ToolRegistryConfig


class ToolRegistryLoader:
    def __init__(self, workspace_root: str = "."):
        self.workspace_root = Path(workspace_root)
        self.config: Optional[ToolRegistryConfig] = None

    def load(self) -> ToolRegistryConfig:
        findings: list[dict[str, Any]] = []
        loaded: list[str] = []

        mcps = self._load_mcp_registry(findings, loaded)
        mcp_runtime = self._load_mcp_runtime(findings, loaded)
        tool_router = self._load_tool_router_config(findings, loaded)
        allowlist = self._load_mcp_tools_allowlist(findings, loaded)

        config = ToolRegistryConfig(
            mcps=mcps,
            mcp_runtime_config=mcp_runtime,
            tool_router_config=tool_router,
            tool_allowlist=allowlist,
            findings=findings,
            loaded_files=loaded,
        )

        self._detect_unknown_capabilities(config, findings)
        self._detect_critical_mcp_enabled_default(config, findings)
        self._detect_unregistered_tools(config, findings)

        self.config = config
        return config

    def _load_yaml(self, path: Path, label: str, findings: list, loaded: list) -> dict:
        if path.exists():
            loaded.append(str(path))
            with open(path, "r", encoding="utf-8") as f:
                return yaml.safe_load(f) or {}
        findings.append({"type": "config_not_found", "label": label, "path": str(path)})
        return {}

    def _load_mcp_registry(self, findings: list, loaded: list) -> list[dict]:
        path = self.workspace_root / "aeos" / "registries" / "mcps.registry.yaml"
        data = self._load_yaml(path, "mcps.registry.yaml", findings, loaded)
        return data.get("mcps", [])

    def _load_mcp_runtime(self, findings: list, loaded: list) -> dict:
        path = self.workspace_root / "aeos" / "config" / "mcp.runtime.yaml"
        return self._load_yaml(path, "mcp.runtime.yaml", findings, loaded)

    def _load_tool_router_config(self, findings: list, loaded: list) -> dict:
        path = self.workspace_root / "aeos" / "config" / "tool-router.config.yaml"
        return self._load_yaml(path, "tool-router.config.yaml", findings, loaded)

    def _load_mcp_tools_allowlist(self, findings: list, loaded: list) -> dict[str, list[str]]:
        path = self.workspace_root / "aeos" / "config" / "mcp-tools.allowlist.yaml"
        data = self._load_yaml(path, "mcp-tools.allowlist.yaml", findings, loaded)
        return data.get("allowlist", {})

    def _detect_unknown_capabilities(self, config: ToolRegistryConfig, findings: list):
        caps_path = self.workspace_root / "aeos" / "config" / "capabilities.yaml"
        if not caps_path.exists():
            return
        with open(caps_path, "r", encoding="utf-8") as f:
            caps_data = yaml.safe_load(f) or {}
        known = set(caps_data.get("capabilities", []))
        for mcp in config.mcps:
            for cap in mcp.get("capabilities", []):
                if cap not in known:
                    findings.append({
                        "type": "unknown_capability",
                        "mcp_id": mcp.get("id"),
                        "capability": cap,
                        "severity": "high",
                    })

    def _detect_critical_mcp_enabled_default(self, config: ToolRegistryConfig, findings: list):
        for mcp in config.mcps:
            if mcp.get("risk_level") == "critical" and mcp.get("enabled", False):
                findings.append({
                    "type": "critical_mcp_enabled_default",
                    "mcp_id": mcp.get("id"),
                    "severity": "critical",
                })

    def _detect_unregistered_tools(self, config: ToolRegistryConfig, findings: list):
        for mcp in config.mcps:
            mcp_id = mcp.get("id", "")
            mcp_tools = set(mcp.get("tools", []))
            allowlisted = set(config.tool_allowlist.get(mcp_id, []))
            for tool in mcp_tools:
                if tool not in allowlisted:
                    findings.append({
                        "type": "tool_not_in_allowlist",
                        "mcp_id": mcp_id,
                        "tool": tool,
                        "severity": "medium",
                    })



