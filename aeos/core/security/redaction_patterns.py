REDACTION_PATTERNS = {
    "aws_access_key": r"AKIA[0-9A-Z]{16}",
    "jwt": r"eyJ[a-zA-Z0-9_-]+\.[a-zA-Z0-9_-]+\.[a-zA-Z0-9_-]+",
    "private_key": r"-----BEGIN (RSA |EC |OPENSSH )?PRIVATE KEY-----",
    "generic_api_key": r"(?i)(api[_-]?key|token|secret)\s*[:=]\s*['\"][^'\"]+['\"]",
}
