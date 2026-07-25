"""Detecção fail-closed de campos sensíveis antes da persistência."""

from __future__ import annotations

import re
from collections.abc import Mapping, Sequence
from typing import Any


_SENSITIVE_SEGMENTS = {
    "secret",
    "password",
    "passwd",
    "passphrase",
    "credential",
    "credentials",
    "authorization",
}
_SENSITIVE_ASSIGNMENT = re.compile(
    r"(?i)(password|passwd|passphrase|secret|api[_-]?key|access[_-]?token|"
    r"refresh[_-]?token|authorization|private[_-]?key|session[_-]?cookie)\s*[:=]"
)
_BEARER = re.compile(r"(?i)\bbearer\s+[A-Za-z0-9._~+/=-]{8,}")
_PRIVATE_KEY = re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----")


def normalize_key(key: str) -> str:
    camel_split = re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", key)
    return re.sub(r"[^a-z0-9]+", "_", camel_split.casefold()).strip("_")


def is_sensitive_key(key: str) -> bool:
    normalized = normalize_key(key)
    segments = set(normalized.split("_"))
    return (
        bool(segments.intersection(_SENSITIVE_SEGMENTS))
        or normalized == "token"
        or normalized.endswith("_token")
        or normalized == "cookie"
        or normalized.endswith("_cookie")
        or normalized.endswith("api_key")
        or normalized.endswith("private_key")
        or normalized.endswith("access_key")
    )


def assert_safe_text(value: str, field: str) -> None:
    if (
        _SENSITIVE_ASSIGNMENT.search(value)
        or _BEARER.search(value)
        or _PRIVATE_KEY.search(value)
    ):
        raise ValueError(f"sensitive value detected in {field}")


def assert_safe_payload(value: Any, field: str = "payload") -> None:
    if isinstance(value, Mapping):
        for key, nested in value.items():
            text_key = str(key)
            if is_sensitive_key(text_key):
                raise ValueError(f"sensitive key detected in {field}")
            assert_safe_payload(nested, f"{field}.{text_key}")
    elif isinstance(value, Sequence) and not isinstance(value, (str, bytes)):
        for index, nested in enumerate(value):
            assert_safe_payload(nested, f"{field}[{index}]")
    elif isinstance(value, str):
        assert_safe_text(value, field)
