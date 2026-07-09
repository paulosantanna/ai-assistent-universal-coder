from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Literal
from uuid import uuid4
from time import time

ToolStatus = Literal["success", "blocked", "failed", "timeout"]

@dataclass(frozen=True)
class ToolCallRequest:
    execution_id: str
    agent_id: str
    skill_id: str
    playbook_id: str
    mcp_id: str
    tool_name: str
    action: str
    capability: str
    input: Dict[str, Any]
    risk_level: str = "low"
    requires_approval: bool = False
    approval_id: Optional[str] = None
    request_id: str = field(default_factory=lambda: str(uuid4()))
    created_at_epoch: float = field(default_factory=time)

@dataclass
class ToolCallResult:
    request_id: str
    status: ToolStatus
    output: Dict[str, Any] = field(default_factory=dict)
    redacted: bool = True
    evidence_refs: List[str] = field(default_factory=list)
    duration_ms: int = 0
    permission_decision: Dict[str, Any] = field(default_factory=dict)
    policy_decision: Dict[str, Any] = field(default_factory=dict)
    errors: List[str] = field(default_factory=list)
