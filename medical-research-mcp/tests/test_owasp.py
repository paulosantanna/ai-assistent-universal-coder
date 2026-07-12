from medical_research_mcp.AI_OWASP import CONTROLS, security_checklist


def test_owasp_gate_requires_controls() -> None:
    result = security_checklist([])
    assert not result["passed"]


def test_owasp_gate_passes_with_all_declared_controls() -> None:
    enabled = [control for controls in CONTROLS.values() for control in controls]
    result = security_checklist(enabled)
    assert result["passed"]
