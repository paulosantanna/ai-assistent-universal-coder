from __future__ import annotations

from pathlib import Path

import pytest

from aeos.core.governance.governance_gate import GovernanceGate
from aeos.core.governance.governance_models import (
    GOV_STATUS_BLOCKED,
    GOV_STATUS_PASS,
    GOV_STATUS_WAITING_APPROVAL,
    GovernanceRequest,
)
from aeos.core.governance.governance_reporter import GovernanceReporter


@pytest.fixture
def workspace_root() -> Path:
    return Path(__file__).resolve().parent.parent.parent.parent


@pytest.fixture
def gate(workspace_root) -> GovernanceGate:
    g = GovernanceGate(str(workspace_root))
    g.initialize()
    return g


def test_gate_blocked_permission_denied(gate: GovernanceGate):
    req = GovernanceRequest(
        execution_id="gt001", action="filesystem.delete",
        actor="coder", role="coder", capability="DEPLOY",
        resource="src/main.py"
    )
    result = gate.evaluate(req)
    assert result.status == GOV_STATUS_BLOCKED
    assert not result.permission_allowed
    assert len(result.blocking_reasons) > 0


def test_gate_blocked_policy_denied(gate: GovernanceGate):
    req = GovernanceRequest(
        execution_id="gt002", action="git.merge",
        actor="coder", role="coder", capability="WRITE_SANDBOX_FILES",
        resource=""
    )
    result = gate.evaluate(req)
    assert result.status == GOV_STATUS_BLOCKED
    assert not result.policy_allowed


def test_gate_waiting_approval(gate: GovernanceGate):
    req = GovernanceRequest(
        execution_id="gt003", action="secrets.read",
        actor="tester", role="tester", capability="READ_FILES",
        resource=".env", approval_present=False,
    )
    result = gate.evaluate(req)
    assert result.status == GOV_STATUS_WAITING_APPROVAL
    assert result.requires_approval
    assert not result.approval_present


def test_gate_pass(gate: GovernanceGate):
    req = GovernanceRequest(
        execution_id="gt004", action="reports.generate",
        actor="root", role="root", capability="GENERATE_REPORT",
        resource=".aeos/reports/test.md",
    )
    result = gate.evaluate(req)
    assert result.status == GOV_STATUS_PASS
    assert result.permission_allowed
    assert result.policy_allowed


def test_gate_evidence_refs_populated(gate: GovernanceGate):
    req = GovernanceRequest(
        execution_id="gt005", action="reports.generate",
        actor="root", role="root", capability="GENERATE_REPORT",
        resource=".aeos/reports/test.md",
    )
    result = gate.evaluate(req)
    assert len(result.evidence_refs) == 2
    assert all(ref.startswith("pd-") for ref in result.evidence_refs)


def test_gate_blocking_reason_permission(gate: GovernanceGate):
    req = GovernanceRequest(
        execution_id="gt006", action="filesystem.delete",
        actor="coder", role="coder", capability="DEPLOY",
        resource="src/main.py"
    )
    result = gate.evaluate(req)
    assert any("Permission denied" in r for r in result.blocking_reasons)


def test_gate_blocking_reason_policy(gate: GovernanceGate):
    req = GovernanceRequest(
        execution_id="gt007", action="git.merge",
        actor="coder", role="coder", capability="WRITE_SANDBOX_FILES",
        resource=""
    )
    result = gate.evaluate(req)
    assert any("Policy denied" in r for r in result.blocking_reasons)


def test_gate_reporter_generates_report(workspace_root, gate: GovernanceGate, tmp_path):
    req = GovernanceRequest(
        execution_id="gt008", action="reports.generate",
        actor="root", role="root", capability="GENERATE_REPORT",
        resource=".aeos/reports/test.md",
    )
    result = gate.evaluate(req)

    reporter = GovernanceReporter(str(tmp_path / ".aeos" / "reports"))
    report_path = reporter.write_governance_report("gt008", gate.results)
    assert Path(report_path).exists()

    with open(report_path, "r") as f:
        content = f.read()
    assert "PASS" in content
    assert "gt008" in content


def test_gate_result_to_dict(gate: GovernanceGate):
    req = GovernanceRequest(
        execution_id="gt009", action="reports.generate",
        actor="root", role="root", capability="GENERATE_REPORT",
        resource="report.md",
    )
    result = gate.evaluate(req)
    d = result.to_dict()
    assert d["execution_id"] == "gt009"
    assert "status" in d
    assert "permission_allowed" in d
    assert "policy_allowed" in d
    assert "blocking_reasons" in d
    assert "evidence_refs" in d
