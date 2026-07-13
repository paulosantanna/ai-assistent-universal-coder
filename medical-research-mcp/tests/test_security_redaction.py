from pathlib import Path

from medical_research_mcp.audit.gates.security import check_security


def test_security_gate_redacts_secret_values_from_evidence(tmp_path: Path) -> None:
    (tmp_path / "config.py").write_text(
        'API_KEY = "sk-1234567890abcdef"\nPASSWORD = "super-secret"\n',
        encoding="utf-8",
    )

    result = check_security(str(tmp_path))

    summaries = " ".join(str(item.get("summary", "")) for item in result.evidence)
    assert "sk-1234567890abcdef" not in summaries
    assert "super-secret" not in summaries
    assert "***REDACTED***" in summaries
