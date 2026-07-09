from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Literal
from uuid import uuid4
from time import time

AgentState = Literal[
    "REGISTERED", "AVAILABLE", "ASSIGNED", "RUNNING", "WAITING_CONTEXT",
    "WAITING_TOOL_RESULT", "WAITING_APPROVAL", "COMPLETED", "BLOCKED",
    "FAILED", "ESCALATED"
]

TaskStatus = Literal[
    "PENDING", "READY", "ASSIGNED", "RUNNING", "WAITING_CONTEXT",
    "WAITING_TOOL_RESULT", "WAITING_APPROVAL", "COMPLETED", "BLOCKED",
    "FAILED", "ESCALATED"
]

@dataclass(frozen=True)
class AgentMessage:
    execution_id: str
    task_id: str
    from_agent: str
    message_type: str
    payload: Dict[str, Any]
    to_agent: Optional[str] = None
    parent_message_id: Optional[str] = None
    context_refs: List[str] = field(default_factory=list)
    evidence_refs: List[str] = field(default_factory=list)
    risk_level: str = "low"
    requires_ack: bool = True
    message_id: str = field(default_factory=lambda: str(uuid4()))
    created_at_epoch: float = field(default_factory=time)

@dataclass
class TaskDefinition:
    execution_id: str
    assigned_agent: str
    objective: str
    scope: Dict[str, Any]
    allowed_skills: List[str]
    required_evidence: List[str]
    task_id: str = field(default_factory=lambda: str(uuid4()))
    parent_task_id: Optional[str] = None
    allowed_capabilities: List[str] = field(default_factory=list)
    allowed_mcps: List[str] = field(default_factory=list)
    required_lcps: List[str] = field(default_factory=list)
    required_context: List[str] = field(default_factory=list)
    forbidden_actions: List[str] = field(default_factory=list)
    quality_gates: List[str] = field(default_factory=list)
    escalation_rules: List[str] = field(default_factory=list)
    status: TaskStatus = "PENDING"

@dataclass
class TaskResult:
    execution_id: str
    task_id: str
    agent_id: str
    status: TaskStatus
    facts: List[Dict[str, Any]] = field(default_factory=list)
    assumptions: List[Dict[str, Any]] = field(default_factory=list)
    risks: List[Dict[str, Any]] = field(default_factory=list)
    recommendations: List[Dict[str, Any]] = field(default_factory=list)
    evidence_refs: List[str] = field(default_factory=list)
    blocking_conditions: List[str] = field(default_factory=list)
