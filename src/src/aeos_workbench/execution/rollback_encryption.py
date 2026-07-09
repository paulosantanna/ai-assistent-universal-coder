"""Rollback Encryption — AES-256-GCM for rollback-plan.json, Fernet fallback."""

import base64
import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

HAS_CRYPTO = False
try:
    from cryptography.fernet import Fernet
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM
    HAS_CRYPTO = True
except ImportError:
    AESGCM = None
    Fernet = None


def _generate_key() -> bytes:
    if AESGCM:
        return AESGCM.generate_key(bit_length=256)
    if Fernet:
        return Fernet.generate_key()
    return os.urandom(32)


def _aesgcm_encrypt(key: bytes, plaintext: bytes) -> tuple[bytes, bytes, bytes]:
    aesgcm = AESGCM(key)
    nonce = os.urandom(12)
    ciphertext = aesgcm.encrypt(nonce, plaintext, None)
    return ciphertext, nonce, b""


def _aesgcm_decrypt(key: bytes, ciphertext: bytes, nonce: bytes, tag: bytes) -> bytes:
    aesgcm = AESGCM(key)
    return aesgcm.decrypt(nonce, ciphertext, None)


def _fernet_encrypt(key: bytes, plaintext: bytes) -> tuple[bytes, bytes, bytes]:
    f = Fernet(key)
    token = f.encrypt(plaintext)
    return token, b"", b""


def _fernet_decrypt(key: bytes, ciphertext: bytes, nonce: bytes, tag: bytes) -> bytes:
    f = Fernet(key)
    return f.decrypt(ciphertext)


KEY_DIR_NAME = "keys"


class RollbackEncryption:
    def __init__(self, workspace_root: Path):
        self.workspace_root = workspace_root.resolve()
        self.aeos_dir = self.workspace_root / ".aeos"
        self.key_dir = self.aeos_dir / KEY_DIR_NAME
        self.key_dir.mkdir(parents=True, exist_ok=True)
        self._key: Optional[bytes] = None

    @property
    def available(self) -> bool:
        return HAS_CRYPTO

    def generate_execution_key(self, execution_id: str) -> bytes:
        key = _generate_key()
        self._write_key(execution_id, key)
        self._key = key
        return key

    def _write_key(self, execution_id: str, key: bytes):
        path = self.key_dir / f"{execution_id}.key"
        path.write_bytes(key)

    def _read_key(self, execution_id: str) -> Optional[bytes]:
        path = self.key_dir / f"{execution_id}.key"
        if path.exists():
            return path.read_bytes()
        return None

    def load_key(self, execution_id: str) -> Optional[bytes]:
        self._key = self._read_key(execution_id)
        return self._key

    def encrypt_rollback(self, rollback_data: dict) -> dict:
        if not HAS_CRYPTO:
            return rollback_data

        execution_id = rollback_data.get("execution_id", "unknown")
        key = self.generate_execution_key(execution_id)

        operations_plain = json.dumps(rollback_data.get("operations", [])).encode("utf-8")

        if AESGCM:
            ciphertext, nonce, tag = _aesgcm_encrypt(key, operations_plain)
            algorithm = "AES-256-GCM"
        elif Fernet:
            ciphertext, nonce, tag = _fernet_encrypt(key, operations_plain)
            algorithm = "Fernet-AES"
        else:
            return rollback_data

        result = {
            "execution_id": rollback_data["execution_id"],
            "generated_at": rollback_data.get("generated_at", datetime.now(timezone.utc).isoformat()),
            "strategy": rollback_data.get("strategy", "sandbox_cleanup"),
            "encryption": {
                "algorithm": algorithm,
                "nonce": base64.b64encode(nonce).decode("ascii") if nonce else "",
                "tag": base64.b64encode(tag).decode("ascii") if tag else "",
            },
            "operations_encrypted": base64.b64encode(ciphertext).decode("ascii"),
            "summary": rollback_data.get("summary", {}),
        }
        return result

    def decrypt_rollback(self, encrypted_data: dict) -> dict:
        if not HAS_CRYPTO:
            return encrypted_data

        execution_id = encrypted_data.get("execution_id", "unknown")
        key = self._read_key(execution_id)
        if not key:
            raise ValueError(f"Rollback key not found for execution {execution_id}")

        enc = encrypted_data.get("encryption", {})
        algorithm = enc.get("algorithm", "AES-256-GCM")
        nonce = base64.b64decode(enc.get("nonce", "")) if enc.get("nonce") else b""
        tag = base64.b64decode(enc.get("tag", "")) if enc.get("tag") else b""
        ciphertext = base64.b64decode(encrypted_data.get("operations_encrypted", ""))

        if algorithm == "AES-256-GCM" and AESGCM:
            plaintext = _aesgcm_decrypt(key, ciphertext, nonce, tag)
        elif algorithm == "Fernet-AES" and Fernet:
            plaintext = _aesgcm_decrypt(key, ciphertext, nonce, tag)
        else:
            raise ValueError(f"Unsupported algorithm: {algorithm}")

        operations = json.loads(plaintext.decode("utf-8"))
        return {
            "execution_id": encrypted_data["execution_id"],
            "generated_at": encrypted_data.get("generated_at", ""),
            "strategy": encrypted_data.get("strategy", ""),
            "encryption": enc,
            "operations": operations,
            "summary": encrypted_data.get("summary", {}),
        }

    def compute_key(self, passphrase: str) -> bytes:
        import hashlib
        raw = hashlib.sha256(passphrase.encode("utf-8")).digest()
        if AESGCM:
            key = raw[:32]
        elif Fernet:
            key = base64.urlsafe_b64encode(raw[:32])
        else:
            key = raw[:32]
        return key