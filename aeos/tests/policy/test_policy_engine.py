from __future__ import annotations

from pathlib import Path

import pytest

from aeos.core.policy.policy_engine import PolicyEngine
from aeos.core.policy.policy_models import PolicyRequest, PolicySeverity


@pytest.fixture
def workspace_root() -> Path:
    return Path(__file__).resolve().parent.parent.parent.parent


@pytest.fixture
def engine(workspace_root) -> PolicyEngine:
    e = PolicyEngine(str(workspace_root))
    e.initialize()
    return e


def test_block_write_outside_sandbox(engine: PolicyEngine):
    req = PolicyRequest(execution_id="t001", action="filesystem.write", resource="src/main.py")
    d = engine.evaluate(req)
    assert not d.allowed
    assert "outside allowed" in d.reason.lower()


def test_allow_write_in_sandbox(engine: PolicyEngine):
    req = PolicyRequest(execution_id="t002", action="filesystem.write", resource=".aeos/sandbox/test.txt")
    d = engine.evaluate(req)
    assert d.allowed


def test_allow_write_in_reports(engine: PolicyEngine):
    req = PolicyRequest(execution_id="t003", action="filesystem.write", resource=".aeos/reports/report.md")
    d = engine.evaluate(req)
    assert d.allowed


def test_allow_write_in_evidence(engine: PolicyEngine):
    req = PolicyRequest(execution_id="t004", action="filesystem.write", resource=".aeos/evidence/ex001/record.jsonl")
    d = engine.evaluate(req)
    assert d.allowed


def test_block_git_merge(engine: PolicyEngine):
    req = PolicyRequest(execution_id="t005", action="git.merge")
    d = engine.evaluate(req)
    assert not d.allowed
    assert d.severity == PolicySeverity.CRITICAL


def test_block_git_force_push(engine: PolicyEngine):
    req = PolicyRequest(execution_id="t006", action="git.force_push")
    d = engine.evaluate(req)
    assert not d.allowed
    assert d.severity == PolicySeverity.CRITICAL


def test_block_shell_not_allowlisted(engine: PolicyEngine):
    req = PolicyRequest(execution_id="t007", action="shell.run", command="evil_script.sh")
    d = engine.evaluate(req)
    assert not d.allowed


def test_allow_shell_allowlisted(engine: PolicyEngine):
    req = PolicyRequest(execution_id="t008", action="shell.run", command="pytest")
    d = engine.evaluate(req)
    assert d.allowed


def test_block_destructive_shell_pattern(engine: PolicyEngine):
    req = PolicyRequest(execution_id="t009", action="shell.run", command="rm -rf /tmp")
    d = engine.evaluate(req)
    assert not d.allowed
    assert "destructive" in d.reason.lower()


def test_block_auto_merge(engine: PolicyEngine):
    req = PolicyRequest(execution_id="t010", action="auto_merge")
    d = engine.evaluate(req)
    assert not d.allowed


def test_block_auto_deploy(engine: PolicyEngine):
    req = PolicyRequest(execution_id="t011", action="auto_deploy")
    d = engine.evaluate(req)
    assert not d.allowed


def test_block_approval_wildcard(engine: PolicyEngine):
    req = PolicyRequest(execution_id="t012", action="approval.wildcard")
    d = engine.evaluate(req)
    assert not d.allowed


def test_block_package_extract_unverified(engine: PolicyEngine):
    req = PolicyRequest(
        execution_id="t013", action="package.extract",
        resource="pkg.zip", details={"verified": False}
    )
    d = engine.evaluate(req)
    assert not d.allowed


def test_allow_package_extract_verified(engine: PolicyEngine):
    req = PolicyRequest(
        execution_id="t014", action="package.extract",
        resource="pkg.zip", details={"verified": True}
    )
    d = engine.evaluate(req)
    assert d.allowed


def test_block_protected_branch_main(engine: PolicyEngine):
    req = PolicyRequest(execution_id="t015", action="branch.protected", branch="main")
    d = engine.evaluate(req)
    assert not d.allowed


def test_block_protected_branch_master(engine: PolicyEngine):
    req = PolicyRequest(execution_id="t016", action="branch.protected", branch="master")
    d = engine.evaluate(req)
    assert not d.allowed


def test_block_protected_branch_develop(engine: PolicyEngine):
    req = PolicyRequest(execution_id="t017", action="branch.protected", branch="develop")
    d = engine.evaluate(req)
    assert not d.allowed


def test_allow_non_protected_branch(engine: PolicyEngine):
    req = PolicyRequest(execution_id="t018", action="branch.protected", branch="feature/new")
    d = engine.evaluate(req)
    assert d.allowed


def test_block_secrets_output(engine: PolicyEngine):
    req = PolicyRequest(execution_id="t019", action="secrets.output")
    d = engine.evaluate(req)
    assert not d.allowed


def test_block_secret_persist(engine: PolicyEngine):
    req = PolicyRequest(execution_id="t020", action="secret.persist")
    d = engine.evaluate(req)
    assert not d.allowed


def test_block_direct_pack_import(engine: PolicyEngine):
    req = PolicyRequest(execution_id="t021", action="pack.import_direct")
    d = engine.evaluate(req)
    assert not d.allowed


def test_block_filesystem_delete(engine: PolicyEngine):
    req = PolicyRequest(execution_id="t022", action="filesystem.delete", resource="file.txt")
    d = engine.evaluate(req)
    assert not d.allowed
