from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Optional

from aeos.core.evidence.evidence_models import HashChainLink, generate_record_id, now_iso
from aeos.core.evidence.hash_utils import sha256


class EvidenceStore:
    def __init__(self, output_dir: str = ".aeos/evidence"):
        self.output_dir = Path(output_dir)
        self._hash_chain: list[HashChainLink] = []
        self._last_hash: str = "0" * 64

    def store_record(self, execution_id: str, record_type: str, content: dict[str, Any]) -> str:
        return self.store_records(execution_id, record_type, [content])[0]

    def store_records(self, execution_id: str, record_type: str, contents: list[dict[str, Any]]) -> list[str]:
        if not contents:
            return []

        base = self.output_dir / execution_id
        base.mkdir(parents=True, exist_ok=True)
        fp = self._record_path(base, record_type)
        record_ids: list[str] = []

        with open(fp, "a", encoding="utf-8") as f:
            for content in contents:
                record, chain_link = self._build_record(execution_id, record_type, content)
                f.write(json.dumps(record, ensure_ascii=False) + "\n")
                record_ids.append(record["record_id"])
                self._hash_chain.append(chain_link)

        self._write_hash_chain(base)

        return record_ids

    def _build_record(
        self,
        execution_id: str,
        record_type: str,
        content: dict[str, Any],
    ) -> tuple[dict[str, Any], HashChainLink]:
        record_id = generate_record_id()
        ts = now_iso()

        record = {
            "record_id": record_id,
            "execution_id": execution_id,
            "record_type": record_type,
            "content": content,
            "timestamp": ts,
        }
        record_hash = sha256(record)

        record["sha256"] = record_hash

        chain_link = HashChainLink(
            index=len(self._hash_chain),
            record_type=record_type,
            sha256=record_hash,
            previous_sha256=self._last_hash,
            timestamp=ts,
        )
        self._last_hash = record_hash
        return record, chain_link

    def store_decisions(
        self, execution_id: str, record_type: str, decisions: list[Any]
    ) -> list[str]:
        contents = []
        for d in decisions:
            if hasattr(d, "to_dict"):
                content = d.to_dict()
            else:
                content = d
            contents.append(content)
        return self.store_records(execution_id, record_type, contents)

    def _record_path(self, base: Path, record_type: str) -> Path:
        if record_type in ("permission_decision", "policy_decision", "audit", "tool_call"):
            return base / f"{record_type}s.jsonl"
        return base / f"{record_type}.jsonl"

    def _write_hash_chain(self, base: Path) -> None:
        fp = base / "hash-chain.jsonl"
        with open(fp, "w", encoding="utf-8") as f:
            for link in self._hash_chain:
                f.write(json.dumps(link.to_dict(), ensure_ascii=False) + "\n")

    def get_hash_chain(self) -> list[HashChainLink]:
        return list(self._hash_chain)

    def verify_hash_chain(self, execution_id: str) -> dict[str, Any]:
        base = self.output_dir / execution_id
        fp = base / "hash-chain.jsonl"
        if not fp.exists():
            return {"passed": False, "reason": "hash_chain_not_found"}

        errors = []
        previous = "0" * 64
        with open(fp, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    link = json.loads(line)
                    if link.get("previous_sha256") != previous:
                        errors.append(f"Hash chain broken at index {link.get('index')}")
                    previous = link.get("sha256", "")
                except json.JSONDecodeError:
                    errors.append("Invalid JSON in hash chain")

        return {"passed": len(errors) == 0, "errors": errors, "links": len(self._hash_chain)}
