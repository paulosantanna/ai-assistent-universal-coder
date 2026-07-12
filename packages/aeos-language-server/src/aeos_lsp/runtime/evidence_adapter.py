from __future__ import annotations

import hashlib
import json
import logging
import time
import uuid
from pathlib import Path
from typing import Any

from aeos_lsp.runtime.ports import EvidencePort, EvidenceRecord

logger = logging.getLogger(__name__)


class EvidenceAdapter(EvidencePort):
    def __init__(self, store_dir: str | Path | None = None) -> None:
        self._initialized = False
        self._records: dict[str, EvidenceRecord] = {}
        self._store_dir = Path(store_dir) if store_dir else None
        self._persist = store_dir is not None

    async def initialize(self, config: dict[str, Any] | None = None) -> None:
        self._initialized = True
        if config and "store_dir" in config:
            self._store_dir = Path(config["store_dir"])
            self._persist = True
        if self._persist and self._store_dir is not None:
            self._store_dir.mkdir(parents=True, exist_ok=True)
            self._load_persisted()
        logger.info("Evidence adapter initialized (persist=%s)", self._persist)

    async def shutdown(self) -> None:
        self._initialized = False
        self._records.clear()
        logger.info("Evidence adapter shut down")

    async def store(self, record: EvidenceRecord) -> str:
        if not record.evidence_id:
            record.evidence_id = str(uuid.uuid4())

        record.content_hash = hashlib.sha256(
            (record.content + record.timestamp).encode("utf-8")
        ).hexdigest()[:16]

        self._records[record.evidence_id] = record

        if self._persist and self._store_dir is not None:
            self._persist_record(record)

        logger.debug("Stored evidence: %s", record.evidence_id)
        return record.evidence_id

    async def retrieve(self, evidence_id: str) -> EvidenceRecord | None:
        return self._records.get(evidence_id)

    async def find(self, artifact_id: str) -> list[EvidenceRecord]:
        return [
            r for r in self._records.values()
            if r.artifact_id == artifact_id
        ]

    async def verify(self, evidence_id: str) -> bool:
        record = self._records.get(evidence_id)
        if record is None:
            return False
        expected_hash = hashlib.sha256(
            (record.content + record.timestamp).encode("utf-8")
        ).hexdigest()[:16]
        return record.content_hash == expected_hash

    async def health_check(self) -> dict[str, Any]:
        corrupted = 0
        for eid in list(self._records.keys()):
            if not await self.verify(eid):
                corrupted += 1
        return {
            "status": "ok" if self._initialized else "not_initialized",
            "record_count": len(self._records),
            "corrupted": corrupted,
            "persist_enabled": self._persist,
        }

    def _persist_record(self, record: EvidenceRecord) -> None:
        if self._store_dir is None:
            return
        file_path = self._store_dir / f"{record.evidence_id}.json"
        try:
            file_path.write_text(
                json.dumps({
                    "evidence_id": record.evidence_id,
                    "artifact_id": record.artifact_id,
                    "execution_id": record.execution_id,
                    "content_hash": record.content_hash,
                    "content": record.content,
                    "timestamp": record.timestamp,
                    "metadata": record.metadata,
                }, indent=2),
                encoding="utf-8",
            )
        except OSError as exc:
            logger.error("Failed to persist evidence %s: %s", record.evidence_id, exc)

    def _load_persisted(self) -> None:
        if self._store_dir is None or not self._store_dir.is_dir():
            return
        for f in self._store_dir.glob("*.json"):
            try:
                data = json.loads(f.read_text(encoding="utf-8"))
                record = EvidenceRecord(
                    evidence_id=data["evidence_id"],
                    artifact_id=data.get("artifact_id", ""),
                    execution_id=data.get("execution_id", ""),
                    content_hash=data.get("content_hash", ""),
                    content=data.get("content", ""),
                    timestamp=data.get("timestamp", ""),
                    metadata=data.get("metadata", {}),
                )
                self._records[record.evidence_id] = record
            except (json.JSONDecodeError, KeyError, OSError) as exc:
                logger.warning("Failed to load evidence file %s: %s", f, exc)
