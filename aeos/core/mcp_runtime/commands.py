"""MCP commands registry — allowlisted commands for MCP tools."""

from dataclasses import dataclass, field
from typing import List, Optional


@dataclass(frozen=True)
class MCPCommandDef:
    mcp_id: str
    command: str
    args: List[str] = field(default_factory=list)
    cwd_override: Optional[str] = None
    env_keys: List[str] = field(default_factory=list)
    risk_level: str = "low"
    timeout_seconds: int = 30
    allow_network: bool = False


MCP_COMMAND_ALLOWLIST: dict[str, MCPCommandDef] = {
    "filesystem-readonly": MCPCommandDef(
        mcp_id="filesystem-readonly",
        command="python",
        args=["-m", "aeos_workbench.mcp_stdio.filesystem_readonly"],
        risk_level="low",
        timeout_seconds=30,
    ),
    "filesystem-write-sandbox": MCPCommandDef(
        mcp_id="filesystem-write-sandbox",
        command="python",
        args=["-m", "aeos_workbench.mcp_stdio.filesystem_write_sandbox"],
        risk_level="medium",
        timeout_seconds=60,
    ),
    "git-readonly": MCPCommandDef(
        mcp_id="git-readonly",
        command="python",
        args=["-m", "aeos_workbench.mcp_stdio.git_readonly"],
        risk_level="low",
        timeout_seconds=60,
    ),
    "test-runner-controlled": MCPCommandDef(
        mcp_id="test-runner-controlled",
        command="python",
        args=["-m", "aeos_workbench.mcp_stdio.test_runner_controlled"],
        risk_level="medium",
        timeout_seconds=300,
    ),
    "package-local": MCPCommandDef(
        mcp_id="package-local",
        command="python",
        args=["-m", "aeos_workbench.mcp_stdio.package_local"],
        risk_level="medium",
        timeout_seconds=120,
    ),
}


def get_command(mcp_id: str) -> MCPCommandDef | None:
    return MCP_COMMAND_ALLOWLIST.get(mcp_id)