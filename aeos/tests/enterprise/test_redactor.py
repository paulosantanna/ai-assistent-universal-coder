from aeos.core.security.enterprise_redactor import EnterpriseRedactor

def test_redacts_api_key():
    redactor = EnterpriseRedactor()
    text, findings = redactor.redact("api_key='abc123'")
    assert "[REDACTED]" in text
    assert findings
