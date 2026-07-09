from dataclasses import dataclass, field
from typing import Dict, List
from uuid import uuid4

@dataclass
class PackRecord:
    package_id: str
    package_type: str
    state: str
    source_path: str
    manifest: Dict
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)

@dataclass
class PackPromotionRequest:
    pack_id: str
    from_state: str
    to_state: str
    reason: str
    requested_by: str
    request_id: str = field(default_factory=lambda: str(uuid4()))
