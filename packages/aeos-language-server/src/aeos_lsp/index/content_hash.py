from __future__ import annotations

import hashlib
from pathlib import Path
from typing import Any


def hash_content(content: str) -> str:
    return hashlib.sha256(content.encode("utf-8")).hexdigest()


def hash_file(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while True:
            chunk = f.read(65536)
            if not chunk:
                break
            h.update(chunk)
    return h.hexdigest()


def hash_document(uri: str, content: str) -> str:
    h = hashlib.sha256()
    h.update(uri.encode("utf-8"))
    h.update(b"\x00")
    h.update(content.encode("utf-8"))
    return h.hexdigest()


def hash_ast(ast: Any) -> str:
    h = hashlib.sha256()
    _hash_object(ast, h)
    return h.hexdigest()


def _hash_object(obj: Any, h: hashlib._Hash) -> None:
    if obj is None:
        h.update(b"n")
    elif isinstance(obj, bool):
        h.update(b"b" + str(obj).encode())
    elif isinstance(obj, (int, float)):
        h.update(b"i" + str(obj).encode())
    elif isinstance(obj, str):
        h.update(b"s" + obj.encode("utf-8"))
    elif isinstance(obj, bytes):
        h.update(b"x" + obj)
    elif isinstance(obj, (list, tuple)):
        h.update(b"l")
        for item in obj:
            _hash_object(item, h)
        h.update(b"e")
    elif isinstance(obj, dict):
        h.update(b"d")
        for k in sorted(obj.keys(), key=str):
            _hash_object(k, h)
            _hash_object(obj[k], h)
        h.update(b"e")
    elif hasattr(obj, "__dataclass_fields__"):
        h.update(b"o" + type(obj).__name__.encode())
        fields = sorted(obj.__dataclass_fields__.keys())
        for fname in fields:
            _hash_object(fname, h)
            _hash_object(getattr(obj, fname), h)
        h.update(b"e")
    else:
        h.update(b"u" + str(obj).encode("utf-8"))


def compare_hashes(old_hash: str, new_hash: str) -> bool:
    if not old_hash or not new_hash:
        return False
    return old_hash == new_hash
