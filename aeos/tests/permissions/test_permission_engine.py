from __future__ import annotations

from pathlib import Path

import pytest

from aeos.core.permissions.permission_engine import PermissionEngine
from aeos.core.permissions.permission_models import PermissionRequest


@pytest.fixture
def workspace_root() -> Path:
    return Path(__file__).resolve().parent.parent.parent.parent


@pytest.fixture
def engine(workspace_root) -> PermissionEngine:
    e = PermissionEngine(str(workspace_root))
    e.initialize()
    return e


def test_deny_all_default(engine: PermissionEngine):
    req = PermissionRequest(
        execution_id="test-001", actor="ghost", role="",
        action="test", capability="READ_FILES", resource=""
    )
    d = engine.evaluate(req)
    assert not d.allowed
    assert "no role" in d.reason.lower()


def test_role_without_capability_deny(engine: PermissionEngine):
    req = PermissionRequest(
        execution_id="test-002", actor="tester", role="tester",
        action="test", capability="MAP_ARCHITECTURE", resource=""
    )
    d = engine.evaluate(req)
    assert not d.allowed
    assert "does not have" in d.reason.lower()


def test_capability_inexistente_deny(engine: PermissionEngine):
    req = PermissionRequest(
        execution_id="test-003", actor="coder", role="coder",
        action="test", capability="NONEXISTENT_CAP", resource=""
    )
    d = engine.evaluate(req)
    assert not d.allowed
    assert "does not exist" in d.reason.lower()


def test_capability_exists_allows(engine: PermissionEngine):
    req = PermissionRequest(
        execution_id="test-004", actor="coder", role="coder",
        action="write_file", capability="WRITE_SANDBOX_FILES",
        resource=".aeos/sandbox/test.txt"
    )
    d = engine.evaluate(req)
    assert d.allowed


def test_action_approval_required(engine: PermissionEngine):
    req = PermissionRequest(
        execution_id="test-005", actor="coder", role="coder",
        action="shell.run", capability="WRITE_SANDBOX_FILES",
        resource=".aeos/sandbox/test.txt"
    )
    d = engine.evaluate(req)
    assert d.allowed
    assert d.requires_approval


def test_role_inexistente_deny(engine: PermissionEngine):
    req = PermissionRequest(
        execution_id="test-006", actor="ghost", role="nonexistent-role",
        action="test", capability="READ_FILES", resource=""
    )
    d = engine.evaluate(req)
    assert not d.allowed
    assert "does not exist" in d.reason.lower()


def test_no_capability_specified_deny(engine: PermissionEngine):
    req = PermissionRequest(
        execution_id="test-007", actor="coder", role="coder",
        action="test", capability="", resource=""
    )
    d = engine.evaluate(req)
    assert not d.allowed
    assert "no capability" in d.reason.lower()


def test_decision_has_required_fields(engine: PermissionEngine):
    req = PermissionRequest(
        execution_id="test-008", actor="root", role="root",
        action="test", capability="GENERATE_REPORT", resource="report.md"
    )
    d = engine.evaluate(req)
    assert d.decision_id.startswith("pd-")
    assert d.execution_id == "test-008"
    assert d.actor == "root"
    assert d.role == "root"
    assert d.action == "test"
    assert d.capability == "GENERATE_REPORT"
    assert d.resource == "report.md"
    assert d.timestamp is not None
