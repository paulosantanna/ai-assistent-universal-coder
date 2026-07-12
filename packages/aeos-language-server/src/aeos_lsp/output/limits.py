from __future__ import annotations

import logging
from typing import Any

from lsprotocol.types import Diagnostic

logger = logging.getLogger(__name__)

_DEFAULT_MAX_OUTPUT_BYTES = 1_048_576
_DEFAULT_MAX_OUTPUT_CHARS = 1_048_576
_DEFAULT_MAX_DIAGNOSTICS = 500
_DEFAULT_MAX_LINES = 10_000


class OutputLimiter:
    def __init__(
        self,
        max_bytes: int = _DEFAULT_MAX_OUTPUT_BYTES,
        max_chars: int = _DEFAULT_MAX_OUTPUT_CHARS,
        max_diagnostics: int = _DEFAULT_MAX_DIAGNOSTICS,
        max_lines: int = _DEFAULT_MAX_LINES,
    ) -> None:
        self._max_bytes = max_bytes
        self._max_chars = max_chars
        self._max_diagnostics = max_diagnostics
        self._max_lines = max_lines

    def update_config(self, max_chars: int | None = None, max_diagnostics: int | None = None) -> None:
        if max_chars is not None:
            self._max_chars = max_chars
        if max_diagnostics is not None:
            self._max_diagnostics = max_diagnostics

    def limit_text(self, text: str) -> str:
        if not text:
            return text

        if len(text) > self._max_chars:
            text = text[: self._max_chars]
            logger.debug("Text truncated to %d characters", self._max_chars)

        byte_count = len(text.encode("utf-8"))
        if byte_count > self._max_bytes:
            ratio = self._max_bytes / byte_count
            new_len = int(len(text) * ratio * 0.95)
            text = text[:new_len]
            logger.debug("Text truncated to %d bytes", self._max_bytes)

        lines = text.split("\n")
        if len(lines) > self._max_lines:
            lines = lines[: self._max_lines]
            text = "\n".join(lines)
            logger.debug("Text truncated to %d lines", self._max_lines)

        return text

    def limit_diagnostics(self, diagnostics: list[Diagnostic]) -> list[Diagnostic]:
        if len(diagnostics) > self._max_diagnostics:
            logger.debug(
                "Diagnostics limited from %d to %d",
                len(diagnostics), self._max_diagnostics,
            )
            return diagnostics[: self._max_diagnostics]
        return diagnostics

    def limit_bytes(self, data: bytes) -> bytes:
        if len(data) > self._max_bytes:
            logger.debug("Output truncated from %d to %d bytes", len(data), self._max_bytes)
            return data[: self._max_bytes]
        return data

    def count_tokens(self, text: str) -> int:
        if not text:
            return 0
        clean = text.encode("utf-8", errors="replace").decode("utf-8")
        return int(len(clean) * 0.27)

    def count_bytes(self, text: str) -> int:
        return len(text.encode("utf-8", errors="replace"))

    def estimate_output_size(self, text: str) -> dict[str, Any]:
        byte_count = self.count_bytes(text)
        char_count = len(text)
        line_count = text.count("\n") + 1
        token_estimate = self.count_tokens(text)

        within_limits = (
            byte_count <= self._max_bytes
            and char_count <= self._max_chars
            and line_count <= self._max_lines
        )

        return {
            "bytes": byte_count,
            "chars": char_count,
            "lines": line_count,
            "estimated_tokens": token_estimate,
            "max_bytes": self._max_bytes,
            "max_chars": self._max_chars,
            "max_lines": self._max_lines,
            "within_limits": within_limits,
        }

    def __repr__(self) -> str:
        return (
            f"OutputLimiter(max_bytes={self._max_bytes}, "
            f"max_chars={self._max_chars}, "
            f"max_diagnostics={self._max_diagnostics})"
        )
