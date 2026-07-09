"""AEOS Core Scanner — scans for evidence integrity, secrets, and config drift."""

import hashlib
import json
from pathlib import Path


class CoreScanner:
    def __init__(self, target_root: str | Path):
        self.target_root = Path(target_root)

    def scan_evidence_integrity(self, execution_id: str = None) -> list[dict]:
        evidence_dir = self.target_root / ".aeos" / "evidence"
        if not evidence_dir.exists():
            return []
        issues = []
        for exec_dir in evidence_dir.iterdir():
            if exec_dir.is_dir():
                for log_file in exec_dir.glob("*.jsonl"):
                    issues.extend(self._check_jsonl_integrity(log_file))
        return issues

    def _check_jsonl_integrity(self, path: Path) -> list[dict]:
        issues = []
        with path.open("r", encoding="utf-8") as f:
            for line_no, line in enumerate(f, 1):
                line = line.strip()
                if not line:
                    continue
                try:
                    record = json.loads(line)
                    stored_hash = record.pop("_sha256", None)
                    if stored_hash:
                        recalc = hashlib.sha256(
                            json.dumps(record, sort_keys=True, ensure_ascii=False).encode("utf-8")
                        ).hexdigest()
                        if stored_hash != recalc:
                            issues.append({"file": str(path), "line": line_no, "issue": "hash_mismatch"})
                except json.JSONDecodeError:
                    issues.append({"file": str(path), "line": line_no, "issue": "invalid_json"})
        return issues

    def scan_secrets_in_output(self, root: str | Path = None) -> list[dict]:
        from aeos.core.redaction.redactor import SECRET_PATTERNS
        target = Path(root) if root else self.target_root
        findings = []
        for f in target.rglob("*.jsonl"):
            try:
                content = f.read_text(encoding="utf-8", errors="replace")
                for pattern, label in SECRETS_PATTERNS:
                    if pattern.search(content):
                        findings.append({"file": str(f), "pattern": label})
            except (OSError, PermissionError):
                pass
        return findings