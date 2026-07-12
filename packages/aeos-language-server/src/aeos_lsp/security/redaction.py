from __future__ import annotations

import logging
import re
from typing import Any

logger = logging.getLogger(__name__)

_REDACTION_PLACEHOLDER = "***REDACTED***"

_SECRET_PATTERNS: list[tuple[str, re.Pattern[str], str]] = [
    ("api_key", re.compile(
        r"(?i)(?:api[_-]?key|apikey|api[_-]?secret)\s*[=:]\s*['\"]?([a-zA-Z0-9_\-+=/]{16,64})['\"]?"
    ), "***API-KEY-REDACTED***"),
    ("aws_access_key", re.compile(
        r"(?i)(?:aws[_-]?access[_-]?key[_-]?id|AKIA[0-9A-Z]{16})\b"
    ), "***AWS-KEY-REDACTED***"),
    ("aws_secret_key", re.compile(
        r"(?i)(?:aws[_-]?secret[_-]?access[_-]?key)\s*[=:]\s*['\"]?([a-zA-Z0-9+/=]{40})['\"]?"
    ), "***AWS-SECRET-REDACTED***"),
    ("github_token", re.compile(
        r"(?i)(?:ghp_|gho_|ghu_|ghs_|ghr_)[a-zA-Z0-9]{36,}"
    ), "***GITHUB-TOKEN-REDACTED***"),
    ("gitlab_token", re.compile(
        r"(?i)(?:glpat-)[a-zA-Z0-9\-]{20,}"
    ), "***GITLAB-TOKEN-REDACTED***"),
    ("bearer_token", re.compile(
        r"(?i)(?:Bearer\s+|token\s*[:=]\s*)[a-zA-Z0-9_\-+=/]{20,200}"
    ), "***TOKEN-REDACTED***"),
    ("password", re.compile(
        r"(?i)(?:password|passwd|pwd)\s*[=:]\s*['\"]?([^\s'\"&;<>]{4,100})['\"]?"
    ), "***PASSWORD-REDACTED***"),
    ("secret", re.compile(
        r"(?i)(?:secret|secret_key|secretkey|client_secret)\s*[=:]\s*['\"]?([a-zA-Z0-9_\-+=/]{8,})['\"]?"
    ), "***SECRET-REDACTED***"),
    ("private_key", re.compile(
        r"-----BEGIN\s+(?:RSA\s+)?PRIVATE\s+KEY-----[\s\S]*?-----END\s+(?:RSA\s+)?PRIVATE\s+KEY-----"
    ), "***PRIVATE-KEY-REDACTED***"),
    ("ssh_key", re.compile(
        r"(?i)(?:ssh-rsa\s+|ssh-ed25519\s+|ecdsa-sha2-nistp\d+\s+)[a-zA-Z0-9+/=]{100,}"
    ), "***SSH-KEY-REDACTED***"),
    ("jwt_token", re.compile(
        r"eyJ[a-zA-Z0-9_\-+=/]+\.[a-zA-Z0-9_\-+=/]+\.[a-zA-Z0-9_\-+=/]+"
    ), "***JWT-REDACTED***"),
    ("connection_string", re.compile(
        r"(?i)(?:connection\s*string|connstr|conn_string)\s*[=:]\s*['\"]?([^'\"]{20,200})['\"]?"
    ), "***CONNECTION-STRING-REDACTED***"),
    ("slack_token", re.compile(
        r"(?i)(?:xoxb-|xoxa-|xoxp-|xoxr-)[a-zA-Z0-9\-]{50,}"
    ), "***SLACK-TOKEN-REDACTED***"),
    ("discord_token", re.compile(
        r"[a-zA-Z0-9_\-]{24}\.[a-zA-Z0-9_\-]{6}\.[a-zA-Z0-9_\-]{27}"
    ), "***DISCORD-TOKEN-REDACTED***"),
    ("stripe_key", re.compile(
        r"(?i)(?:sk_live_|pk_live_|sk_test_|pk_test_)[a-zA-Z0-9]{24,}"
    ), "***STRIPE-KEY-REDACTED***"),
    ("twilio_sid", re.compile(
        r"(?i)AC[a-zA-Z0-9]{32}"
    ), "***TWILIO-SID-REDACTED***"),
    ("database_url", re.compile(
        r"(?i)(?:postgres(?:ql)?|mysql|mongodb|redis|rediss)\+?:\/\/[^\s]{10,}"
    ), "***DB-URL-REDACTED***"),
    ("generic_token", re.compile(
        r"(?i)(?:token|auth_token|accesstoken|refreshtoken)\s*[=:]\s*['\"]?([a-zA-Z0-9_\-]{8,128})['\"]?"
    ), "***TOKEN-REDACTED***"),
]


class RedactionEngine:
    def __init__(self, patterns: list[tuple[str, re.Pattern[str], str]] | None = None) -> None:
        self._patterns = patterns or _SECRET_PATTERNS

    def redact_text(self, text: str) -> str:
        if not text:
            return text
        result = text
        for name, pattern, replacement in self._patterns:
            result = pattern.sub(replacement, result)
        return result

    def redact_structured(self, data: Any, max_depth: int = 20) -> Any:
        if max_depth <= 0:
            return _REDACTION_PLACEHOLDER

        if isinstance(data, str):
            return self.redact_text(data)

        if isinstance(data, dict):
            return {
                key: self.redact_structured(value, max_depth - 1)
                for key, value in data.items()
            }

        if isinstance(data, list):
            return [self.redact_structured(item, max_depth - 1) for item in data]

        if isinstance(data, tuple):
            return tuple(self.redact_structured(item, max_depth - 1) for item in data)

        return data

    def contains_secret(self, text: str) -> bool:
        if not text:
            return False
        for name, pattern, _ in self._patterns:
            if pattern.search(text):
                return True
        return False

    def add_pattern(self, name: str, pattern: re.Pattern[str], replacement: str | None = None) -> None:
        repl = replacement or _REDACTION_PLACEHOLDER
        self._patterns.append((name, pattern, repl))
        logger.debug("Added redaction pattern: %s", name)

    def list_patterns(self) -> list[str]:
        return [name for name, _, _ in self._patterns]

    def __repr__(self) -> str:
        return f"RedactionEngine(patterns={len(self._patterns)})"
