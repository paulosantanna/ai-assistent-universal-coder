"""Evidence encryption module - Fernet-based symmetric encryption with integrity verification.

Provides optional encryption for evidence at rest.
If cryptography is not installed, falls back to SHA256 integrity only.
"""

import hashlib
import json
import os
import base64

HAS_CRYPTO = False
try:
    from cryptography.fernet import Fernet
    from cryptography.hazmat.primitives import hashes
    from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

    HAS_CRYPTO = True
except ImportError:
    pass


def generate_key():
    if HAS_CRYPTO:
        return Fernet.generate_key().decode("utf-8")
    return None


def derive_key_from_passphrase(passphrase, salt=None):
    if not HAS_CRYPTO:
        return None
    if salt is None:
        salt = b"aeos-evidence-salt-v1"
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=600000,
    )
    key = base64.urlsafe_b64encode(kdf.derive(passphrase.encode("utf-8")))
    return key.decode("utf-8")


class EvidenceCipher:
    def __init__(self, key=None):
        self.key = key
        self._fernet = None
        if key and HAS_CRYPTO:
            try:
                self._fernet = Fernet(key.encode("utf-8") if isinstance(key, str) else key)
            except Exception:
                self._fernet = None

    @classmethod
    def auto(cls):
        key = os.environ.get("AEOS_EVIDENCE_KEY")
        if key:
            return cls(key)
        return cls()

    @property
    def available(self):
        return self._fernet is not None

    def encrypt(self, data):
        payload = json.dumps(data, ensure_ascii=False, sort_keys=True).encode("utf-8")
        digest = hashlib.sha256(payload).hexdigest()

        if self._fernet:
            encrypted = self._fernet.encrypt(payload)
            return {
                "_aeos_cipher": "fernet",
                "_aeos_data": encrypted.decode("utf-8"),
                "_aeos_hash": digest,
                "_aeos_version": 1,
            }
        else:
            return {
                "_aeos_cipher": "plain",
                "_aeos_data": data,
                "_aeos_hash": digest,
                "_aeos_version": 1,
            }

    def decrypt(self, envelope):
        if envelope.get("_aeos_cipher") == "fernet":
            if not self._fernet:
                raise ValueError("Encrypted evidence requires AEOS_EVIDENCE_KEY or cryptography library")
            encrypted = envelope["_aeos_data"].encode("utf-8")
            decrypted = self._fernet.decrypt(encrypted)
            data = json.loads(decrypted.decode("utf-8"))
            digest = hashlib.sha256(decrypted).hexdigest()
            if digest != envelope.get("_aeos_hash", ""):
                raise ValueError("Evidence integrity check FAILED: hash mismatch")
            return data
        elif envelope.get("_aeos_cipher") == "plain":
            data = envelope["_aeos_data"]
            payload = json.dumps(data, ensure_ascii=False, sort_keys=True).encode("utf-8")
            digest = hashlib.sha256(payload).hexdigest()
            if digest != envelope.get("_aeos_hash", ""):
                raise ValueError("Evidence integrity check FAILED: hash mismatch")
            return data
        return envelope

    def hash_only(self, data):
        payload = json.dumps(data, ensure_ascii=False, sort_keys=True).encode("utf-8")
        return hashlib.sha256(payload).hexdigest()
