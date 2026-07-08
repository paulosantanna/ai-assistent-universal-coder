"""Evidence Ledger - persists and retrieves evidence entries with optional encryption."""

import json
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

from aeos_workbench.evidence.crypto import EvidenceCipher, generate_key, HAS_CRYPTO


class EvidenceLedger:
    def __init__(self, storage_dir=None, cipher=None):
        self.storage_dir = Path(storage_dir) if storage_dir else Path.cwd() / ".aeos" / "evidence"
        self.storage_dir.mkdir(parents=True, exist_ok=True)
        self._entries_file = self.storage_dir / "evidence.jsonl"
        self._key_file = self.storage_dir / ".key"
        self._cache = None

        if cipher:
            self.cipher = cipher
        else:
            auto_cipher = EvidenceCipher.auto()
            if not auto_cipher.available and self._key_file.exists():
                stored_key = self._key_file.read_text().strip()
                auto_cipher = EvidenceCipher(stored_key)
            self.cipher = auto_cipher

    def add(self, entry):
        entry.setdefault("evidence_id", "evt-" + uuid.uuid4().hex[:12])
        entry.setdefault("timestamp", datetime.now(timezone.utc).isoformat())
        entry.setdefault("verified", False)

        envelope = self.cipher.encrypt(entry)

        with open(self._entries_file, "a", encoding="utf-8") as f:
            f.write(json.dumps(envelope, ensure_ascii=False) + "\n")

        if self._cache is not None:
            self._cache.append(entry)

        return entry

    def get_all(self):
        if self._cache is not None:
            return self._cache

        if not self._entries_file.exists():
            self._cache = []
            return self._cache

        entries = []
        with open(self._entries_file, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line:
                    try:
                        envelope = json.loads(line)
                        entry = self.cipher.decrypt(envelope)
                        entries.append(entry)
                    except (json.JSONDecodeError, ValueError) as e:
                        entries.append({
                            "evidence_id": "evt-corrupted",
                            "type": "error",
                            "claim": "Corrupted evidence entry: " + str(e),
                            "timestamp": datetime.now(timezone.utc).isoformat(),
                            "verified": False,
                        })

        self._cache = entries
        return entries

    def get_by_type(self, evidence_type):
        return [e for e in self.get_all() if e.get("type") == evidence_type]

    def get_by_id(self, evidence_id):
        for e in self.get_all():
            if e.get("evidence_id") == evidence_id:
                return e
        return None

    def count(self):
        return len(self.get_all())

    def clear(self):
        self._cache = None
        if self._entries_file.exists():
            self._entries_file.unlink()

    def export_json(self):
        return json.dumps(self.get_all(), indent=2, ensure_ascii=False)

    def has_type(self, evidence_type):
        return any(e.get("type") == evidence_type for e in self.get_all())

    def setup_encryption(self, passphrase=None):
        if passphrase:
            from aeos_workbench.evidence.crypto import derive_key_from_passphrase
            key = derive_key_from_passphrase(passphrase)
        else:
            key = generate_key()
        if key:
            self._key_file.write_text(key)
            self.cipher = EvidenceCipher(key)
            return True
        return HAS_CRYPTO

    @property
    def encryption_available(self):
        return self.cipher.available
