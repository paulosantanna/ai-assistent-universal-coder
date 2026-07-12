from __future__ import annotations

import logging
import re
from typing import Any

logger = logging.getLogger(__name__)

_WHITESPACE_RE = re.compile(r"\s+")
_PUNCTUATION_RE = re.compile(r"[^\w\s]")
_CONTROL_CHARS_RE = re.compile(r"[\x00-\x08\x0b\x0c\x0e-\x1f]")

_AVG_TOKENS_PER_WORD = 1.33
_AVG_TOKENS_PER_CHAR = 0.27
_AVG_TOKENS_PER_CODE_CHAR = 0.33


def _estimate_token_count(text: str, profile: str = "general") -> int:
    if not text:
        return 0

    clean = _CONTROL_CHARS_RE.sub("", text)
    char_count = len(clean)

    if profile == "code":
        estimated = char_count * _AVG_TOKENS_PER_CODE_CHAR
    elif profile == "conversation":
        word_count = len(_WHITESPACE_RE.split(clean.strip()))
        punc_count = len(_PUNCTUATION_RE.findall(clean))
        estimated = (word_count * _AVG_TOKENS_PER_WORD) + (punc_count * 0.5)
    else:
        estimated = char_count * _AVG_TOKENS_PER_CHAR

    return max(1, int(round(estimated)))


def _count_tokens_by_model(text: str, model: str = "gpt-4") -> int:
    model_multipliers = {
        "gpt-4": 1.0,
        "gpt-4-turbo": 1.0,
        "gpt-3.5-turbo": 1.1,
        "claude-3-opus": 0.95,
        "claude-3-sonnet": 1.0,
        "claude-3-haiku": 1.05,
        "claude-2": 1.0,
        "gemini-pro": 1.0,
        "llama-3": 1.05,
        "mixtral": 1.1,
        "code-davinci-002": 1.2,
    }

    base = _estimate_token_count(text, "code")
    multiplier = model_multipliers.get(model.lower(), 1.0)
    return max(1, int(round(base * multiplier)))


def estimate_tokens(server: Any, args: dict[str, Any]) -> dict[str, Any]:
    uri = args.get("uri", "")
    text_arg = args.get("text", "")
    model = args.get("model", "gpt-4")
    profile = args.get("profile", "code")

    logger.info("Estimating tokens for %s (model=%s, profile=%s)", uri, model, profile)

    try:
        if not text_arg and uri:
            workspace = getattr(server, "workspace_manager", None)
            if workspace is not None:
                doc = workspace.document_store.get(uri) if hasattr(workspace, "document_store") else None
                if doc is not None:
                    text_arg = doc.text if hasattr(doc, "text") else ""

        if not text_arg:
            return {"error": "No text provided and document not found", "uri": uri}

        estimated = _count_tokens_by_model(text_arg, model)
        char_count = len(text_arg)
        word_count = len(_WHITESPACE_RE.split(text_arg.strip())) if text_arg.strip() else 0

        return {
            "uri": uri,
            "estimated_tokens": estimated,
            "char_count": char_count,
            "word_count": word_count,
            "model": model,
            "profile": profile,
            "detail": {
                "method": "estimated" if model in ("gpt-4", "claude-3-sonnet") else "approximate",
                "multiplier_applied": _count_tokens_by_model(text_arg, model) / max(1, _estimate_token_count(text_arg, profile)),
                "tiers": {
                    "tier_1k": estimated <= 1000,
                    "tier_4k": estimated <= 4000,
                    "tier_8k": estimated <= 8000,
                    "tier_16k": estimated <= 16000,
                    "tier_32k": estimated <= 32000,
                    "tier_64k": estimated <= 64000,
                    "tier_128k": estimated <= 128000,
                },
            },
        }
    except Exception as exc:
        logger.exception("Failed to estimate tokens for %s", uri)
        return {"error": str(exc), "uri": uri}
