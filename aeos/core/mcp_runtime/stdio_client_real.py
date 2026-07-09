"""Real stdio MCP client — runs allowlisted commands with timeout and isolation."""

import subprocess
import json
import shlex
from pathlib import Path
from .contracts import MCPInvokeResult
from .commands import get_command


class StdioMCPClient:
    def __init__(self, mcp_id: str, cwd: str | Path | None = None, timeout_seconds: int = 30):
        self.mcp_id = mcp_id
        self.cwd = Path(cwd) if cwd else None
        self.timeout_seconds = timeout_seconds
        self._cmd_def = get_command(mcp_id)
        if self._cmd_def is None:
            raise ValueError(f"MCP '{mcp_id}' is not in the allowlist")

    def call(self, method: str, params: dict) -> MCPInvokeResult:
        command = [self._cmd_def.command] + list(self._cmd_def.args)
        payload = json.dumps({"method": method, "params": params})

        try:
            proc = subprocess.run(
                command,
                input=payload,
                capture_output=True,
                text=True,
                cwd=self.cwd,
                timeout=self._cmd_def.timeout_seconds,
            )
        except subprocess.TimeoutExpired:
            return MCPInvokeResult(status="timeout", errors=["subprocess timed out"])
        except FileNotFoundError:
            return MCPInvokeResult(status="failed", errors=[f"command not found: {command[0]}"])

        if proc.returncode != 0:
            return MCPInvokeResult(
                status="failed",
                errors=[f"exit code {proc.returncode}", proc.stderr[:500]],
            )

        try:
            result = json.loads(proc.stdout)
            return MCPInvokeResult(status="success", output=result)
        except json.JSONDecodeError:
            return MCPInvokeResult(status="failed", errors=["invalid JSON output"])

    def health(self) -> dict:
        return {"id": self.mcp_id, "state": "READY", "note": "config-driven stdio client"}