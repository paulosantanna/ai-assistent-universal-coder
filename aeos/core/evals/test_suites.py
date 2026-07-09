"""AEOS Evaluation Test Suites — anti-hallucination, redaction, tool router bypass, etc."""

ANTI_HALLUCINATION_SUITE = {
    "suite_id": "anti_hallucination",
    "description": "Validates that outputs do not contain fabricated evidence claims",
    "cases": [
        {"name": "unverified_claim", "input": {"claim": "Evidence says X", "has_evidence": False}, "expected_block": True},
        {"name": "verified_claim", "input": {"claim": "Evidence says X", "has_evidence": True}, "expected_block": False},
    ],
}

EVIDENCE_INTEGRITY_SUITE = {
    "suite_id": "evidence_integrity",
    "description": "Validates evidence hash chain integrity",
    "cases": [
        {"name": "valid_hash", "input": {"hash_match": True}, "expected_block": False},
        {"name": "invalid_hash", "input": {"hash_match": False}, "expected_block": True},
    ],
}

SECRET_REDACTION_SUITE = {
    "suite_id": "secret_redaction",
    "description": "Validates secrets are properly redacted from output",
    "cases": [
        {"name": "aws_key_redacted", "input": {"text": "AKIA1234567890123456"}, "expected_block": True},
        {"name": "clean_output", "input": {"text": "normal output"}, "expected_block": False},
    ],
}

TOOL_ROUTER_BYPASS_SUITE = {
    "suite_id": "tool_router_bypass",
    "description": "Validates no direct tool access outside Tool Router",
    "cases": [
        {"name": "direct_tool_call", "input": {"direct_tool_access": True}, "expected_block": True},
        {"name": "routed_tool_call", "input": {"direct_tool_access": False}, "expected_block": False},
    ],
}

ALL_SUITES = {
    "anti_hallucination": ANTI_HALLUCINATION_SUITE,
    "evidence_integrity": EVIDENCE_INTEGRITY_SUITE,
    "secret_redaction": SECRET_REDACTION_SUITE,
    "tool_router_bypass": TOOL_ROUTER_BYPASS_SUITE,
}