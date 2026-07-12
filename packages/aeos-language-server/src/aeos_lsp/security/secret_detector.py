from __future__ import annotations

import logging
import math
import re
from dataclasses import dataclass, field
from typing import Any

logger = logging.getLogger(__name__)


@dataclass
class SecretMatch:
    type: str
    value_preview: str
    line: int
    column: int
    end_column: int
    confidence: float
    context: str = ""
    entropy: float = 0.0

    def to_dict(self) -> dict[str, Any]:
        return {
            "type": self.type,
            "value_preview": self.value_preview,
            "line": self.line,
            "column": self.column,
            "end_column": self.end_column,
            "confidence": self.confidence,
            "context": self.context[:100],
            "entropy": self.entropy,
        }


_REGEX_PATTERNS: list[tuple[str, re.Pattern[str], float]] = [
    ("GitHub Token", re.compile(r"(?:ghp_|gho_|ghu_|ghs_|ghr_)[a-zA-Z0-9]{36,}"), 0.95),
    ("GitLab Token", re.compile(r"glpat-[a-zA-Z0-9\-]{20,}"), 0.95),
    ("AWS Access Key", re.compile(r"(?:AKIA|ASIA)[0-9A-Z]{16}"), 0.9),
    ("AWS Secret Key", re.compile(r"(?i)aws[_-]?secret[_-]?access[_-]?key\s*[=:]\s*['\"]?[a-zA-Z0-9+/=]{40}"), 0.9),
    ("Azure Connection String", re.compile(r"DefaultEndpointsProtocol=https;AccountName=[^;]+;AccountKey=[^;]+"), 0.85),
    ("Stripe Live Key", re.compile(r"(?:sk_live_|pk_live_)[a-zA-Z0-9]{24,}"), 0.95),
    ("Stripe Test Key", re.compile(r"(?:sk_test_|pk_test_)[a-zA-Z0-9]{24,}"), 0.85),
    ("Slack Bot Token", re.compile(r"xoxb-[a-zA-Z0-9\-]{50,}"), 0.95),
    ("Slack Webhook URL", re.compile(r"https://hooks\.slack\.com/services/[a-zA-Z0-9/]{40,}"), 0.9),
    ("Discord Bot Token", re.compile(r"[a-zA-Z0-9_\-]{24}\.[a-zA-Z0-9_\-]{6}\.[a-zA-Z0-9_\-]{27}"), 0.9),
    ("Twilio SID", re.compile(r"AC[a-zA-Z0-9]{32}"), 0.85),
    ("JWT Token", re.compile(r"eyJ[a-zA-Z0-9_\-+=/]+\.[a-zA-Z0-9_\-+=/]+\.[a-zA-Z0-9_\-+=/]+"), 0.8),
    ("PEM Private Key", re.compile(r"-----BEGIN\s+(?:RSA\s+)?PRIVATE\s+KEY-----"), 0.95),
    ("SSH Private Key", re.compile(r"-----BEGIN\s+OPENSSH\s+PRIVATE\s+KEY-----"), 0.95),
    ("PGP Private Key", re.compile(r"-----BEGIN\s+PGP\s+PRIVATE\s+KEY\s+BLOCK-----"), 0.95),
    ("Heroku API Key", re.compile(r"(?i)heroku[_-]?api[_-]?key\s*[=:]\s*['\"]?[a-zA-Z0-9\-]{20,}"), 0.85),
    ("Google OAuth", re.compile(r"\d{12,20}-[a-zA-Z0-9_]{32,}\.apps\.googleusercontent\.com"), 0.85),
    ("Generic API Key", re.compile(r"(?i)(?:api[_-]?key|apikey)\s*[=:]\s*['\"]?([a-zA-Z0-9_\-+=/]{16,64})['\"]?"), 0.7),
    ("Password Assignment", re.compile(r"(?i)(?:password|passwd|pwd)\s*[=:]\s*['\"]?([^\s'\"&;<>]{4,100})['\"]?"), 0.6),
    ("Database Connection String", re.compile(r"(?i)(?:postgres(?:ql)?|mysql|mongodb|redis|rediss)\+?:\/\/[^\s@]+@"), 0.85),
    ("SQLite Path", re.compile(r"(?i)sqlite[_:]?.*?path\s*=\s*['\"]?[a-zA-Z0-9_\-./\\]+\.(?:db|sqlite|sqlite3)"), 0.5),
    ("Firebase URL", re.compile(r"https://[a-zA-Z0-9\-]+\.firebaseio\.com"), 0.7),
    ("Private npm Token", re.compile(r"(?i)//registry\.npmjs\.org/:_authToken=[a-zA-Z0-9\-]{36,}"), 0.9),
    ("Docker Config Auth", re.compile(r"(?i)\"auth\":\s*\"[a-zA-Z0-9+=/]{50,}\""), 0.7),
]

_HIGH_ENTROPY_THRESHOLD = 4.5


def _shannon_entropy(data: str) -> float:
    if not data:
        return 0.0
    entropy = 0.0
    length = len(data)
    for char in set(data):
        count = data.count(char)
        if count > 0:
            p = count / length
            entropy -= p * math.log2(p)
    return entropy


class SecretDetector:
    def __init__(
        self,
        patterns: list[tuple[str, re.Pattern[str], float]] | None = None,
        enable_entropy_detection: bool = True,
        entropy_threshold: float = _HIGH_ENTROPY_THRESHOLD,
        min_secret_length: int = 8,
    ) -> None:
        self._patterns = patterns or _REGEX_PATTERNS
        self._enable_entropy = enable_entropy_detection
        self._entropy_threshold = entropy_threshold
        self._min_secret_length = min_secret_length

    def detect(self, text: str, context_lines: int = 1) -> list[SecretMatch]:
        if not text:
            return []

        matches: list[SecretMatch] = []
        seen_spans: set[tuple[int, int, int]] = set()

        lines = text.split("\n")

        for secret_type, pattern, base_confidence in self._patterns:
            for match in pattern.finditer(text):
                start = match.start()
                end = match.end()

                line_no, col = self._position_from_offset(text, start)
                end_line, end_col = self._position_from_offset(text, end)

                span_key = (line_no, col, end_col)
                if span_key in seen_spans:
                    continue
                seen_spans.add(span_key)

                value = match.group(0)
                value_preview = value[:40] + "..." if len(value) > 40 else value

                entropy = _shannon_entropy(value) if self._enable_entropy else 0.0

                confidence = base_confidence
                if self._enable_entropy and entropy < 3.0:
                    confidence *= 0.8
                elif self._enable_entropy and entropy > self._entropy_threshold:
                    confidence = min(1.0, confidence * 1.1)

                context = self._extract_context(lines, line_no - 1, context_lines)

                matches.append(SecretMatch(
                    type=secret_type,
                    value_preview=value_preview,
                    line=line_no,
                    column=col,
                    end_column=end_col,
                    confidence=round(confidence, 3),
                    context=context,
                    entropy=round(entropy, 2),
                ))

        if self._enable_entropy:
            matches.extend(self._detect_by_entropy(text, lines, context_lines, seen_spans))

        matches.sort(key=lambda m: (-m.confidence, m.line, m.column))
        return matches

    def detect_high_confidence(self, text: str, min_confidence: float = 0.8) -> list[SecretMatch]:
        return [m for m in self.detect(text) if m.confidence >= min_confidence]

    def has_secrets(self, text: str, min_confidence: float = 0.7) -> bool:
        return any(m.confidence >= min_confidence for m in self.detect(text))

    def detect_by_type(self, text: str, secret_type: str) -> list[SecretMatch]:
        return [
            m for m in self.detect(text)
            if m.type.lower() == secret_type.lower()
        ]

    def _detect_by_entropy(
        self,
        text: str,
        lines: list[str],
        context_lines: int,
        seen_spans: set[tuple[int, int, int]],
    ) -> list[SecretMatch]:
        entropy_matches: list[SecretMatch] = []

        long_token_pattern = re.compile(r'\b[a-zA-Z0-9_\-+=/]{20,80}\b')
        for match in long_token_pattern.finditer(text):
            value = match.group(0)

            if len(value) < self._min_secret_length:
                continue

            entropy = _shannon_entropy(value)
            if entropy < self._entropy_threshold:
                continue

            start = match.start()
            end = match.end()
            line_no, col = self._position_from_offset(text, start)
            end_line, end_col = self._position_from_offset(text, end)

            span_key = (line_no, col, end_col)
            if span_key in seen_spans:
                continue
            seen_spans.add(span_key)

            if self._is_likely_secret(value):
                context = self._extract_context(lines, line_no - 1, context_lines)
                entropy_matches.append(SecretMatch(
                    type="High-Entropy String",
                    value_preview=value[:40] + "..." if len(value) > 40 else value,
                    line=line_no,
                    column=col,
                    end_column=end_col,
                    confidence=min(0.85, 0.5 + (entropy - 4.0) * 0.1),
                    context=context,
                    entropy=round(entropy, 2),
                ))

        return entropy_matches

    def _is_likely_secret(self, value: str) -> bool:
        if value.startswith(("-----BEGIN", "-----END")):
            return True
        if "--" in value or ".." in value:
            return False
        if value.isdigit():
            return False
        if value.lower() in ("true", "false", "none", "null", "yes", "no"):
            return False
        return True

    def _extract_context(self, lines: list[str], line_idx: int, context_lines: int) -> str:
        start = max(0, line_idx - context_lines)
        end = min(len(lines), line_idx + context_lines + 1)
        context_parts = []
        for i in range(start, end):
            prefix = ">" if i == line_idx else " "
            context_parts.append(f"{prefix} {lines[i]}")
        return "\n".join(context_parts)

    @staticmethod
    def _position_from_offset(text: str, offset: int) -> tuple[int, int]:
        if offset >= len(text):
            return (0, 0)
        line = text[:offset].count("\n")
        last_newline = text[:offset].rfind("\n")
        col = offset - last_newline - 1 if last_newline >= 0 else offset
        return (line + 1, col)

    def add_pattern(self, secret_type: str, pattern: re.Pattern[str], confidence: float = 0.7) -> None:
        self._patterns.append((secret_type, pattern, confidence))
        logger.debug("Added detection pattern: %s", secret_type)

    def list_patterns(self) -> list[str]:
        return [name for name, _, _ in self._patterns]

    def __repr__(self) -> str:
        return f"SecretDetector(patterns={len(self._patterns)}, entropy={self._enable_entropy})"
