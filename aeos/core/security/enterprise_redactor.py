import re

PATTERNS = [
    re.compile(r"AKIA[0-9A-Z]{16}"),
    re.compile(r"eyJ[a-zA-Z0-9_-]+\\.[a-zA-Z0-9_-]+\\.[a-zA-Z0-9_-]+"),
    re.compile(r"-----BEGIN (RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    re.compile(r"(?i)(api[_-]?key|token|secret)\\s*[:=]\\s*['\\\"][^'\\\"]+['\\\"]"),
]

class EnterpriseRedactor:
    def redact(self, text: str) -> tuple[str, list[str]]:
        findings = []
        redacted = text
        for idx, pattern in enumerate(PATTERNS):
            if pattern.search(redacted):
                findings.append(f"pattern_{idx}")
                redacted = pattern.sub("[REDACTED]", redacted)
        return redacted, findings
