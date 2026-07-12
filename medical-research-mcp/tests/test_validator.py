from medical_research_mcp.expert_validator import validate_10_0
from medical_research_mcp.models import ValidationCriterion


def test_accepts_only_full_evidenced_pass() -> None:
    criteria = [
        ValidationCriterion(id="A", name="architecture", weight=1, passed=True, evidence=["ADR-001"]),
        ValidationCriterion(id="B", name="tests", weight=1, passed=True, evidence=["pytest-pass"]),
    ]
    report = validate_10_0(criteria)
    assert report.accepted
    assert report.score == 10.0


def test_rejects_missing_evidence_even_when_marked_passed() -> None:
    criteria = [
        ValidationCriterion(id="A", name="tests", weight=1, passed=True, evidence=[]),
    ]
    report = validate_10_0(criteria)
    assert not report.accepted
    assert report.score == 0.0


def test_rejects_any_mandatory_failure() -> None:
    criteria = [
        ValidationCriterion(id="A", name="architecture", weight=1, passed=True, evidence=["ADR"]),
        ValidationCriterion(id="B", name="security", weight=1, passed=False, evidence=["scan"], reason="critical"),
    ]
    report = validate_10_0(criteria)
    assert not report.accepted
    assert report.score == 5.0
    assert report.blocking_reasons
