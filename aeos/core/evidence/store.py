"""AEOS Evidence Store — persists all execution evidence with hash integrity."""

import json
import hashlib
from pathlib import Path
from datetime import datetime, UTC


class EvidenceStore:
    def __init__(self, target_root: str):
        self.target_root = Path(target_root)

    def _base(self, execution_id: str) -> Path:
        p = self.target_root / ".aeos" / "evidence" / execution_id
        p.mkdir(parents=True, exist_ok=True)
        return p

    def _append_jsonl(self, path: Path, record: dict):
        record["_timestamp"] = datetime.now(UTC).isoformat()
        record["_sha256"] = hashlib.sha256(
            json.dumps(record, sort_keys=True, ensure_ascii=False).encode("utf-8")
        ).hexdigest()
        with path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(record, ensure_ascii=False) + "\n")

    def write_tool_call(self, execution_id: str, request: dict, result: dict):
        base = self._base(execution_id)
        self._append_jsonl(base / "tool-calls.jsonl", {"type": "tool_call", "request": request, "result": result})

    def write_mcp_call(self, execution_id: str, mcp_id: str, method: str, params: dict, result: dict):
        base = self._base(execution_id)
        self._append_jsonl(base / "mcp-calls.jsonl", {"type": "mcp_call", "mcp_id": mcp_id, "method": method, "params": params, "result": result})

    def write_permission_decision(self, execution_id: str, request: dict, decision: dict):
        base = self._base(execution_id)
        self._append_jsonl(base / "permission-decisions.jsonl", {"type": "permission_decision", "request": request, "decision": decision})

    def write_policy_decision(self, execution_id: str, request: dict, decision: dict):
        base = self._base(execution_id)
        self._append_jsonl(base / "policy-decisions.jsonl", {"type": "policy_decision", "request": request, "decision": decision})

    def verify_integrity(self, execution_id: str, log_type: str) -> dict:
        base = self._base(execution_id)
        path = base / f"{log_type}.jsonl"
        if not path.exists():
            return {"passed": False, "reason": "file_not_found"}
        errors = []
        total = 0
        with path.open("r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                total += 1
                try:
                    record = json.loads(line)
                    stored_hash = record.pop("_sha256", None)
                    if stored_hash:
                        recalc = hashlib.sha256(
                            json.dumps(record, sort_keys=True, ensure_ascii=False).encode("utf-8")
                        ).hexdigest()
                        if stored_hash != recalc:
                            errors.append(f"line_{total}: hash_mismatch")
                except json.JSONDecodeError:
                    errors.append(f"line_{total}: invalid_json")
        return {"passed": len(errors) == 0, "total": total, "errors": errors}

    def read_log(self, execution_id: str, log_type: str) -> list[dict]:
        base = self._base(execution_id)
        path = base / f"{log_type}.jsonl"
        if not path.exists():
            return []
        records = []
        with path.open("r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line:
                    records.append(json.loads(line))
        return records