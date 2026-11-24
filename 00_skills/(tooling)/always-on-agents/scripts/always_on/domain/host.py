"""The worker host is the window already open. The model is never guessed."""

from __future__ import annotations

from dataclasses import dataclass

ADAPTERS = frozenset({"cursor", "opencode"})


@dataclass(frozen=True)
class HostSession:
    host: str
    model: str


def detect_host(env: dict[str, str]) -> str:
    if env.get("CURSOR_AGENT") == "1":
        return "cursor"
    if any(key.startswith("OPENCODE") for key in env):
        return "opencode"
    return "unknown"


def require_model(model: str | None) -> str | None:
    text = (model or "").strip()
    return text or None
