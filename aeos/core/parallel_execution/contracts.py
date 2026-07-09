from dataclasses import dataclass, field
from typing import List, Dict, Literal

ConflictType = Literal[
    "WRITE_WRITE",
    "READ_WRITE",
    "TOOL_SIDE_EFFECT",
    "APPROVAL_SCOPE",
    "RESOURCE_LOCK",
    "EVIDENCE_CHAIN",
    "AGENT_AUTHORITY",
]

@dataclass
class StepResourceSet:
    step_id: str
    read_set: List[str] = field(default_factory=list)
    write_set: List[str] = field(default_factory=list)
    tool_side_effects: List[str] = field(default_factory=list)
    locks: List[str] = field(default_factory=list)

@dataclass
class StepConflict:
    conflict_id: str
    conflict_type: ConflictType
    step_a: str
    step_b: str
    decision: str
    reason: str
    evidence_refs: List[str] = field(default_factory=list)
