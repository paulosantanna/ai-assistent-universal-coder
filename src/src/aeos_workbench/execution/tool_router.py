"""Tool Router — routes all tool calls through permission checks, MCP integration, and logs decisions."""

import subprocess
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

APPROVAL_REQUIRED_ACTIONS = {
    "filesystem.delete",
    "filesystem.write_outside_sandbox",
    "git.commit",
    "git.push",
    "git.merge",
    "shell.run",
    "secrets.read",
    "deploy.run",
    "database.schema_change",
}

BLOCKED_ACTIONS = {
    "shell.destructive",
    "filesystem.delete",
    "deploy.production",
    "secrets.expose",
    "browser.login_automation",
    "auth.bypass",
    "audit.hide",
    "cookies.persist",
    "tokens.store",
}

MCP_READ_ONLY_ACTIONS = {
    "filesystem.read_file": {"mcp": "filesystem-readonly", "capability": "READ_FILES", "timeout": 30},
    "filesystem.list_directory": {"mcp": "filesystem-readonly", "capability": "LIST_DIRECTORIES", "timeout": 30},
    "filesystem.file_exists": {"mcp": "filesystem-readonly", "capability": "READ_FILES", "timeout": 15},
    "git.status": {"mcp": "git-readonly", "capability": "GIT_STATUS", "timeout": 15},
    "git.diff": {"mcp": "git-readonly", "capability": "GIT_DIFF", "timeout": 30},
    "git.log": {"mcp": "git-readonly", "capability": "GIT_LOG", "timeout": 15},
    "git.branch_list": {"mcp": "git-readonly", "capability": "GIT_STATUS", "timeout": 15},
}

MCP_WRITE_SECURITY = {
    "filesystem.write": {"allowed": True, "sandbox_required": True, "approval": False},
    "git.commit": {"allowed": False, "reason": "Git write is blocked in read-only mode"},
    "git.push": {"allowed": False, "reason": "Git write is blocked in read-only mode"},
    "git.merge": {"allowed": False, "reason": "Git write is blocked in read-only mode"},
    "git.branch_create": {"allowed": False, "reason": "Git write is blocked in read-only mode"},
    "shell.run": {"allowed": False, "reason": "Shell execution is blocked in this phase"},
    "secrets.read": {"allowed": False, "reason": "Secrets MCP is blocked in this phase"},
}

REDACTION_PATTERNS = [
    (r'(?i)(password|secret|token|key|credential)[=:]\s*\S+', "***REDACTED***"),
    (r'AKIA[0-9A-Z]{16}', "***REDACTED-AWS-KEY***"),
    (r'sk-[a-zA-Z0-9]{20,}', "***REDACTED-API-KEY***"),
    (r'-----BEGIN\s+(RSA\s+)?PRIVATE\s+KEY-----.*?-----END\s+(RSA\s+)?PRIVATE\s+KEY-----', "***REDACTED-PRIVATE-KEY***"),
]


def _redact_content(content: str) -> str:
    import re
    result = content
    for pattern, replacement in REDACTION_PATTERNS:
        result = re.sub(pattern, replacement, result, flags=re.DOTALL)
    return result


class ToolRouter:
    def __init__(self, sandbox_writer, approval_gateway, execution_id: str, workspace_root: Optional[Path] = None):
        self.sandbox_writer = sandbox_writer
        self.approval_gateway = approval_gateway
        self.execution_id = execution_id
        self.workspace_root = workspace_root or Path.cwd()
        self.decision_log: list[dict] = []
        self.mcp_call_log: list[dict] = []

    def authorize(
        self,
        action: str,
        actor: str = "system",
        context: Optional[dict] = None,
    ) -> dict:
        context = context or {}
        decision = self._evaluate(action, context)
        self.decision_log.append({
            "action": action,
            "actor": actor,
            "decision": decision["decision"],
            "reason": decision.get("reason", ""),
            "requires_approval": decision.get("requires_approval", False),
            "timestamp": datetime.now(timezone.utc).isoformat(),
        })
        return decision

    def _evaluate(self, action: str, context: dict) -> dict:
        import re

        if action in BLOCKED_ACTIONS:
            return {
                "decision": "deny",
                "reason": f"Action '{action}' is permanently blocked by Tool Router",
                "requires_approval": False,
                "blocked": True,
            }

        if action == "filesystem.write":
            target = context.get("target_path")
            if target and not self.sandbox_writer.is_within_allowed_aeos(target):
                return {
                    "decision": "deny",
                    "reason": f"Write to {target} is outside .aeos directory. "
                              f"Requires approval 'filesystem.write_outside_sandbox'",
                    "requires_approval": True,
                    "requires_action": "filesystem.write_outside_sandbox",
                    "blocked": False,
                }
            return {"decision": "allow", "reason": "Write within .aeos", "requires_approval": False}

        if action in APPROVAL_REQUIRED_ACTIONS:
            return {
                "decision": "pending_approval",
                "reason": f"Action '{action}' requires human approval",
                "requires_approval": True,
                "requires_action": action,
                "blocked": False,
            }

        if action in MCP_READ_ONLY_ACTIONS:
            mcp_config = MCP_READ_ONLY_ACTIONS[action]
            return {
                "decision": "allow",
                "reason": f"MCP read-only allowed: {action} via {mcp_config['mcp']}",
                "requires_approval": False,
                "mcp": mcp_config["mcp"],
                "capability": mcp_config["capability"],
                "timeout": mcp_config["timeout"],
            }

        if action in MCP_WRITE_SECURITY:
            sec = MCP_WRITE_SECURITY[action]
            if not sec["allowed"]:
                return {"decision": "deny", "reason": sec["reason"], "requires_approval": False, "blocked": True}
            return {"decision": "allow", "reason": "MCP write allowed", "requires_approval": sec.get("approval", False)}

        return {"decision": "allow", "reason": "Default allow", "requires_approval": False}

    def call_mcp(self, action: str, params: dict) -> dict:
        decision = self._evaluate(action, {})

        if decision.get("decision") == "deny":
            self.mcp_call_log.append({
                "action": action,
                "decision": "denied",
                "reason": decision.get("reason", ""),
                "timestamp": datetime.now(timezone.utc).isoformat(),
            })
            return {"error": decision.get("reason", "Action denied")}

        if decision.get("decision") not in ("allow",):
            self.mcp_call_log.append({
                "action": action,
                "decision": "blocked",
                "reason": "No permission granted",
                "timestamp": datetime.now(timezone.utc).isoformat(),
            })
            return {"error": "No permission granted"}

        mcp_config = MCP_READ_ONLY_ACTIONS.get(action, {})
        timeout = mcp_config.get("timeout", 30)
        capability = mcp_config.get("capability", "UNKNOWN")

        start_time = time.time()
        try:
            if action == "filesystem.read_file":
                file_path = params.get("path", "")
                full_path = self.workspace_root / file_path
                if not full_path.exists():
                    raise FileNotFoundError(f"File not found: {full_path}")
                content = full_path.read_text(encoding="utf-8", errors="replace")
                redacted = _redact_content(content)
                elapsed = time.time() - start_time
                self.mcp_call_log.append({
                    "action": action,
                    "decision": "allowed",
                    "capability": capability,
                    "params": {"path": file_path},
                    "elapsed_seconds": round(elapsed, 2),
                    "output_size_bytes": len(redacted),
                    "redacted": True,
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                })
                return {"content": redacted, "size": len(redacted)}

            elif action == "filesystem.list_directory":
                dir_path = params.get("path", "")
                full_path = self.workspace_root / dir_path
                if not full_path.exists():
                    raise FileNotFoundError(f"Directory not found: {full_path}")
                entries = [{"name": p.name, "type": "file" if p.is_file() else "dir", "size": p.stat().st_size if p.is_file() else 0} for p in sorted(full_path.iterdir())]
                elapsed = time.time() - start_time
                self.mcp_call_log.append({
                    "action": action,
                    "decision": "allowed",
                    "capability": capability,
                    "params": {"path": dir_path},
                    "elapsed_seconds": round(elapsed, 2),
                    "entry_count": len(entries),
                    "redacted": False,
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                })
                return {"entries": entries, "count": len(entries)}

            elif action == "filesystem.file_exists":
                file_path = params.get("path", "")
                full_path = self.workspace_root / file_path
                exists = full_path.exists()
                elapsed = time.time() - start_time
                self.mcp_call_log.append({
                    "action": action,
                    "decision": "allowed",
                    "capability": capability,
                    "params": {"path": file_path},
                    "elapsed_seconds": round(elapsed, 2),
                    "redacted": False,
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                })
                return {"exists": exists}

            elif action.startswith("git."):
                import subprocess
                git_cmd = {"status": ["git", "status", "--short"], "diff": ["git", "diff", "--stat"], "log": ["git", "log", "--oneline", "-10"], "branch_list": ["git", "branch"]}
                cmd = git_cmd.get(action.split(".")[-1])
                if not cmd:
                    return {"error": f"Unknown git action: {action}"}

                result = subprocess.run(cmd, capture_output=True, text=True, cwd=str(self.workspace_root), timeout=timeout)
                redacted_stdout = _redact_content(result.stdout)
                elapsed = time.time() - start_time
                self.mcp_call_log.append({
                    "action": action,
                    "decision": "allowed",
                    "capability": capability,
                    "elapsed_seconds": round(elapsed, 2),
                    "output_size_bytes": len(redacted_stdout),
                    "redacted": True,
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                })
                return {"stdout": redacted_stdout, "stderr": result.stderr, "returncode": result.returncode}

        except Exception as e:
            elapsed = time.time() - start_time
            self.mcp_call_log.append({
                "action": action,
                "decision": "error",
                "error": str(e),
                "elapsed_seconds": round(elapsed, 2),
                "timestamp": datetime.now(timezone.utc).isoformat(),
            })
            return {"error": str(e)}

        return {"error": f"Unknown MCP action: {action}"}

    def check_approval_before_execute(self, action: str, context: Optional[dict] = None) -> dict:
        decision = self._evaluate(action, context or {})
        if decision.get("requires_approval"):
            approval_data = self.approval_gateway.check_approval(self.execution_id)
            if not approval_data or approval_data.get("status") != "approved":
                return {
                    "decision": "blocked_waiting_approval",
                    "reason": f"Action '{action}' requires approval. "
                              f"Create approval file at .aeos/approvals/{self.execution_id}.approval.yaml",
                    "approval_required": True,
                }
            return {
                "decision": "allow",
                "reason": f"Action '{action}' approved by {approval_data.get('decided_by', 'human')}",
                "approval_required": True,
            }
        return decision

    def check_write_target(self, target_path: Path) -> dict:
        try:
            self.sandbox_writer.validate_write_target(target_path.absolute())
            return {"decision": "allow", "reason": "Write target is within allowed area"}
        except PermissionError as e:
            return {"decision": "deny", "reason": str(e), "requires_approval": True}

    def get_decision_log(self) -> list[dict]:
        return self.decision_log

    def get_mcp_call_log(self) -> list[dict]:
        return self.mcp_call_log