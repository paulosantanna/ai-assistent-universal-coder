from dataclasses import dataclass, field
from typing import Dict, List, Optional
from uuid import uuid4
from datetime import datetime, UTC

@dataclass
class TraceSpan:
    execution_id: str
    name: str
    kind: str
    status: str = "ok"
    parent_span_id: Optional[str] = None
    span_id: str = field(default_factory=lambda: str(uuid4()))
    started_at: str = field(default_factory=lambda: datetime.now(UTC).isoformat())
    ended_at: Optional[str] = None
    duration_ms: Optional[int] = None
    evidence_refs: List[str] = field(default_factory=list)
    attributes: Dict = field(default_factory=dict)
