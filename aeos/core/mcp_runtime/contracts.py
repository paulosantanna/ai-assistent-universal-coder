from dataclasses import dataclass, field
from typing import Any, Dict, List, Literal, Optional

MCPState = Literal["UNINITIALIZED", "STARTING", "READY", "DEGRADED", "FAILED", "STOPPING", "STOPPED"]

@dataclass
class MCPDefinition:
    id: str
    type: str
    transport: str
    config_path: str
    risk_level: str
    capabilities: List[str]
    tools: List[str]
    enabled: bool = True
    approval_required: bool = False

@dataclass
class MCPHealth:
    id: str
    state: MCPState
    version: str = "unknown"
    capabilities: List[str] = field(default_factory=list)
    tools: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)

@dataclass
class MCPInvokeResult:
    status: str
    output: Dict[str, Any] = field(default_factory=dict)
    errors: List[str] = field(default_factory=list)
