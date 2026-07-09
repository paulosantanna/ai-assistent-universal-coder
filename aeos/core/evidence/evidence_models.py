from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Optional


@dataclass
class EvidenceRecord:
    record_id: str
    execution_id: str
    record_type: str
    content: dict[str, Any]
    sha256: str
    timestamp: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "record_id": self.record_id,
            "execution_id": self.execution_id,
            "record_type": self.record_type,
            "content": self.content,
            "sha256": self.sha256,
            "timestamp": self.timestamp,
        }


@dataclass
class EvidenceManifest:
    execution_id: str
    generated_at: str
    files: list[dict[str, Any]] = field(default_factory=list)
    total_records: int = 0
    manifest_sha256: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "execution_id": self.execution_id,
            "generated_at": self.generated_at,
            "files": self.files,
            "total_records": self.total_records,
            "manifest_sha256": self.manifest_sha256,
        }


@dataclass
class HashChainLink:
    index: int
    record_type: str
    sha256: str
    previous_sha256: str
    timestamp: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "index": self.index,
            "record_type": self.record_type,
            "sha256": self.sha256,
            "previous_sha256": self.previous_sha256,
            "timestamp": self.timestamp,
        }


@dataclass
class AuditEntry:
    entry_id: str
    execution_id: str
    action: str
    actor: str
    status: str
    detail: str
    timestamp: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "entry_id": self.entry_id,
            "execution_id": self.execution_id,
            "action": self.action,
            "actor": self.actor,
            "status": self.status,
            "detail": self.detail,
            "timestamp": self.timestamp,
        }


def generate_record_id() -> str:
    import uuid
    return f"ev-{uuid.uuid4().hex[:12]}"


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()
