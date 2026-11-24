"""Billing is a domain rule. A priced family cannot be reclassified as free."""

from __future__ import annotations

from dataclasses import dataclass

PAID_GENERATION_LIMIT = 3
PAID_MARKERS = (
    "grok",
    "claude",
    "opus",
    "sonnet",
    "haiku",
    "codex",
    "gpt",
    "gemini",
    "glm",
    "o1",
    "o3",
    "o4",
)
ACCEPTED_ANSWERS = frozenset({"sim", "yes", "aprovo"})


def _normalized(model: str) -> str:
    return (model or "").strip().lower()


def is_ollama(value: str) -> bool:
    text = _normalized(value)
    return "ollama" in text or ":11434" in text


def is_priced_family(model: str) -> bool:
    text = _normalized(model)
    return any(marker in text for marker in PAID_MARKERS)


def classify(model: str, allowlist: set[str]) -> str:
    """Return paid, free, unknown or forbidden.

    unknown is not free. The caller treats unknown like paid.
    A priced marker wins over the allowlist.
    """
    if is_ollama(model):
        return "forbidden"
    if is_priced_family(model):
        return "paid"
    key = _normalized(model)
    allowed = {_normalized(item) for item in allowlist}
    if key and key in allowed:
        return "free"
    return "unknown"


def accepts_answer(answer: str) -> bool:
    return (answer or "").strip().lower() in ACCEPTED_ANSWERS


@dataclass(frozen=True)
class BillingDecision:
    model: str
    kind: str
    limit: int | None
    asks: bool

    @staticmethod
    def for_model(model: str, allowlist: set[str]) -> "BillingDecision":
        kind = classify(model, allowlist)
        if kind == "free":
            return BillingDecision(model, kind, None, False)
        if kind == "forbidden":
            return BillingDecision(model, kind, 0, False)
        return BillingDecision(model, kind, PAID_GENERATION_LIMIT, True)
