"""AEOS MCP Runtime — real invocation layer with allowlist, timeout, and health checks."""

from typing import Any
from .contracts import MCPHealth, MCPInvokeResult
from .registry import MCPRegistry
from .stdio_client_real import StdioMCPClient


class MCPRuntime:
    def __init__(self, registry: MCPRegistry, default_timeout_seconds: int = 30):
        self.registry = registry
        self.default_timeout_seconds = default_timeout_seconds

    def health(self, mcp_id: str) -> MCPHealth:
        mcp = self.registry.resolve(mcp_id)
        if not mcp:
            return MCPHealth(id=mcp_id, state="FAILED", errors=["mcp_not_registered"])
        if not getattr(mcp, "enabled", True):
            return MCPHealth(id=mcp_id, state="STOPPED", errors=["mcp_disabled"])
        return MCPHealth(
            id=mcp_id,
            state="READY",
            capabilities=getattr(mcp, "capabilities", []),
            tools=getattr(mcp, "tools", []),
        )

    def invoke(self, request) -> dict:
        mcp = self.registry.resolve(request.mcp_id)
        if not mcp:
            return {"status": "blocked", "errors": ["mcp_not_registered"]}
        if not getattr(mcp, "enabled", True):
            return {"status": "blocked", "errors": ["mcp_disabled"]}
        if not self.registry.is_tool_allowed(request.mcp_id, request.tool_name):
            return {"status": "blocked", "errors": ["tool_not_allowlisted"]}

        try:
            client = StdioMCPClient(
                mcp_id=request.mcp_id,
                timeout_seconds=self.default_timeout_seconds,
            )
            result = client.call(request.tool_name, dict(request.input))
            return {
                "mcp_id": request.mcp_id,
                "tool_name": request.tool_name,
                "status": result.status,
                "output": result.output,
                "errors": result.errors,
            }
        except ValueError as exc:
            return {"status": "blocked", "errors": [str(exc)]}