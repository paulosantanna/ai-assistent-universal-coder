from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Optional


@dataclass
class PolicyRequest:
    execution_id: str
    action: str
    resource: str = ""
    command: str = ""
    branch: str = ""
    details: dict[str, Any] = field(default_factory=dict)


class PolicySeverity:
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


@dataclass
class PolicyDecision:
    decision_id: str
    execution_id: str
    action: str
    resource: str
    allowed: bool
    severity: str
    reason: str
    matched_policy: str
    timestamp: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "decision_id": self.decision_id,
            "execution_id": self.execution_id,
            "action": self.action,
            "resource": self.resource,
            "allowed": self.allowed,
            "severity": self.severity,
            "reason": self.reason,
            "matched_policy": self.matched_policy,
            "timestamp": self.timestamp,
        }


@dataclass
class PolicyConfig:
    protected_branches: list[str] = field(default_factory=lambda: ["main", "master", "develop"])
    allow_write_paths: list[str] = field(default_factory=lambda: [
        ".aeos/sandbox/**", ".aeos/reports/**", ".aeos/evidence/**",
        ".aeos/patches/**", ".aeos/packages/**",
    ])
    block_delete_without_approval: bool = True
    block_merge_always: bool = True
    block_force_push_always: bool = True
    block_commit_without_approval: bool = True
    block_push_without_approval: bool = True
    shell_allowlist: list[str] = field(default_factory=list)
    block_unlisted_shell: bool = True
    block_destructive_shell_patterns: list[str] = field(default_factory=list)
    block_secret_output: bool = True
    block_secret_package: bool = True
    block_secret_logging: bool = True
    require_package_manifest: bool = True
    require_package_sha256: bool = True
    block_package_path_traversal: bool = True
    block_package_absolute_paths: bool = True
    block_package_symlinks: bool = True
    block_package_zip_bomb: bool = True
    block_auto_merge: bool = True
    block_auto_deploy: bool = True
    block_wildcard_approval: bool = True
    block_unrestricted_shell: bool = True
    block_raw_secret_persistence: bool = True
    block_direct_active_pack_import: bool = True
    block_critical_mcp_default_enabled: bool = True
    block_unverified_package_extract: bool = True


def generate_policy_decision_id() -> str:
    import uuid
    return f"pd-{uuid.uuid4().hex[:12]}"


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()
