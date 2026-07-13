import json
from pathlib import Path

from aeos_workbench.execution import orchestrator as orchestrator_module
from aeos_workbench.execution.rollback_manager import RollbackManager


def test_run_playbook_approves_same_execution(monkeypatch, tmp_path):
    class FakeApprovalGateway:
        def __init__(self):
            self.created = None
            self.resolved = None

        def create_approval_request(self, execution_id, action, context):
            self.created = (execution_id, action, context)

        def resolve(self, execution_id, decision, decided_by, reason):
            self.resolved = (execution_id, decision, decided_by, reason)

    class FakeOrchestrator:
        instance = None

        def __init__(self, workspace, **kwargs):
            self.execution_id = "ex-test"
            self.approval_gateway = FakeApprovalGateway()
            self.workspace = workspace
            FakeOrchestrator.instance = self

        def run(self, playbook_id, target, dry_run=False):
            return {
                "status": "PASS",
                "execution_id": self.execution_id,
                "playbook_id": playbook_id,
                "target": str(target),
            }

    monkeypatch.setattr(
        orchestrator_module, "ExecutionOrchestrator", FakeOrchestrator
    )
    monkeypatch.chdir(tmp_path)
    target = tmp_path / "target"
    target.mkdir()

    result = orchestrator_module.run_playbook(
        "critical-playbook", str(target), approvals=True
    )

    instance = FakeOrchestrator.instance
    assert result["execution_id"] == "ex-test"
    assert instance.approval_gateway.created == (
        "ex-test",
        "playbook.critical-playbook",
        {"playbook_id": "critical-playbook", "target": str(target)},
    )
    assert instance.approval_gateway.resolved[:3] == (
        "ex-test",
        "approved",
        "cli-human",
    )


def test_rollback_plan_uses_execution_id(tmp_path):
    manager = RollbackManager(tmp_path, "ex-test")

    path = manager.save()
    payload = json.loads(path.read_text(encoding="utf-8"))

    assert path == Path(tmp_path) / "ex-test" / "rollback-plan.json"
    assert payload["execution_id"] == "ex-test"
