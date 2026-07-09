"""AEOS Redactor — output redaction for secrets and sensitive data."""

import re
from typing import Any


SECRET_PATTERNS = [
    (re.compile(r"AKIA[0-9A-Z]{16}"), "aws_access_key"),
    (re.compile(r"eyJ[a-zA-Z0-9_-]+\.[a-zA-Z0-9_-]+\.[a-zA-Z0-9_-]+"), "jwt_token"),
    (re.compile(r"-----BEGIN (RSA |EC |OPENSSH )?PRIVATE KEY-----"), "private_key"),
    (re.compile(r"(?i)(api[_-]?key|token|secret|password)\s*[:=]\s*['\"][^'\"]+['\"]"), "generic_credential"),
    (re.compile(r"(?i)ghp_[a-zA-Z0-9]{36}"), "github_token"),
    (re.compile(r"(?i)gho_[a-zA-Z0-9]{36}"), "github_oauth"),
    (re.compile(r"(?i)ghu_[a-zA-Z0-9]{36}"), "github_user_token"),
    (re.compile(r"(?i)ghr_[a-zA-Z0-9]{76}"), "github_refresh_token"),
    (re.compile(r"(?i)ghs_[a-zA-Z0-9]{36}"), "github_server_token"),
    (re.compile(r"sk-[a-zA-Z0-9]{20,}"), "openai_key"),
]


class Redactor:
    def __init__(self, patterns: list = None):
        self.patterns = patterns or SECRET_PATTERNS

    def redact(self, data: Any, redact_strings: bool = True) -> tuple[Any, list[str]]:
        if isinstance(data, str):
            return self._redact_string(data)
        if isinstance(data, dict):
            findings = []
            redacted = {}
            for k, v in data.items():
                rv, f = self.redact(v, redact_strings)
                redacted[k] = rv
                findings.extend(f)
            return redacted, findings
        if isinstance(data, list):
            findings = []
            redacted = []
            for item in data:
                ri, f = self.redact(item, redact_strings)
                redacted.append(ri)
                findings.extend(f)
            return redacted, findings
        return data, []

    def _redact_string(self, text: str) -> tuple[str, list[str]]:
        findings = []
        for pattern, label in self.patterns:
            if pattern.search(text):
                findings.append(label)
                text = pattern.sub(f"[REDACTED:{label}]", text)
        return text, findings

    def contains_secret(self, text: str) -> bool:
        for pattern, _ in self.patterns:
            if pattern.search(text):
                return True
        return False