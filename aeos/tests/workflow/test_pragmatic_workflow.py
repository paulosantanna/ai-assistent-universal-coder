from __future__ import annotations

from pathlib import Path

from aeos.core.evidence.evidence_store import EvidenceStore
from aeos.core.runtime.runtime_models import RuntimeRequest, generate_execution_id
from aeos.core.runtime.runtime_orchestrator import RuntimeOrchestrator
from aeos.core.workflow.context_planner import ContextPlanner
from aeos.core.workflow.model_router import ModelRouter
from aeos.core.workflow.training_data_curator import TrainingDataCurator
from aeos.core.workflow.workflow_kernel import WorkflowKernel


REPO_ROOT = Path(__file__).resolve().parents[3]


def _evidence_store(root: Path) -> EvidenceStore:
    return EvidenceStore(str(root / ".aeos" / "evidence"))


def test_context_planner_redacts_preview_and_persists_pack(tmp_path: Path) -> None:
    target = tmp_path / "project"
    target.mkdir()
    (target / "config.txt").write_text('api_key="secret-value"\nnormal=true\n', encoding="utf-8")

    planner = ContextPlanner(str(target), evidence_store=_evidence_store(target))
    pack = planner.build_context_pack(
        execution_id="exec-context",
        objective="plan context",
        target_path=".",
        required_paths=["config.txt"],
    )

    assert pack.status == "PASS"
    assert pack.files[0].redaction_findings == ["generic_credential"]
    assert "secret-value" not in pack.files[0].preview
    assert (target / ".aeos" / "evidence" / "exec-context" / "context-pack.json").exists()


def test_context_planner_blocks_path_outside_workspace(tmp_path: Path) -> None:
    planner = ContextPlanner(str(tmp_path), evidence_store=_evidence_store(tmp_path))
    pack = planner.build_context_pack(
        execution_id="exec-outside",
        objective="plan context",
        target_path=".",
        required_paths=[str(REPO_ROOT / "AGENT.md")],
    )

    assert pack.files == []
    assert pack.excluded_files[0].reason == "path_outside_workspace"


def test_model_router_uses_free_profile_for_low_risk_paid_stage(tmp_path: Path) -> None:
    router = ModelRouter(str(tmp_path), str(REPO_ROOT), evidence_store=_evidence_store(tmp_path))
    decision = router.decide(
        execution_id="exec-router-low",
        stage="focused_patch",
        risk_level="low",
        estimated_input_tokens=1000,
    )

    assert decision.status == "PASS"
    assert decision.profile == "free_local"
    assert decision.paid is False


def test_model_router_requires_approval_for_high_risk_paid_stage(tmp_path: Path) -> None:
    router = ModelRouter(str(tmp_path), str(REPO_ROOT), evidence_store=_evidence_store(tmp_path))
    decision = router.decide(
        execution_id="exec-router-high",
        stage="architecture_decision",
        risk_level="high",
        estimated_input_tokens=1000,
    )

    assert decision.status == "WAITING_APPROVAL"
    assert decision.profile == "paid_strong"
    assert decision.paid is True
    assert decision.blocking_conditions == ["paid_model_requires_approval"]


def test_training_data_curator_rejects_unsafe_positive_candidate(tmp_path: Path) -> None:
    curator = TrainingDataCurator(str(tmp_path), evidence_store=_evidence_store(tmp_path))
    candidate = curator.curate(
        execution_id="exec-dataset",
        dataset_type="positive",
        prompt='token="secret"\n',
        completion="patch",
        source_refs=[".aeos/evidence/exec-dataset/context-pack.json"],
        tests_passed=False,
        judge_status="PASS",
    )

    assert candidate.status == "REJECTED"
    assert "positive_example_requires_passing_tests" in candidate.blocking_conditions
    assert "secret" not in candidate.prompt


def test_workflow_kernel_creates_plan_model_decisions_and_dataset_candidate(tmp_path: Path) -> None:
    (tmp_path / "AGENT.md").write_text("agent contract\n", encoding="utf-8")
    kernel = WorkflowKernel(str(tmp_path), str(REPO_ROOT), evidence_store=_evidence_store(tmp_path))

    result = kernel.plan_and_record(
        execution_id="exec-workflow",
        workflow_id="bug_fix",
        objective="Fix low risk bug",
        risk_level="low",
        tests_passed=True,
        judge_status="PASS",
    )

    assert result.status == "PASS"
    assert result.context_pack.files
    assert [decision.paid for decision in result.model_decisions] == [False, False, False]
    assert result.dataset_candidates[0].status == "ACCEPTED"
    assert (tmp_path / ".aeos" / "evidence" / "exec-workflow" / "workflow-plan.json").exists()


def test_runtime_orchestrator_runs_workflow(tmp_path: Path) -> None:
    (tmp_path / "AGENT.md").write_text("agent contract\n", encoding="utf-8")
    orchestrator = RuntimeOrchestrator(
        workspace_root=str(tmp_path),
        aeos_root=str(REPO_ROOT),
        target_path=str(tmp_path),
    )
    orchestrator.initialize()
    request = RuntimeRequest(
        execution_id=generate_execution_id(),
        run_type="workflow",
        entity_id="bug_fix",
        actor="tester",
        role="tester",
        target_path=str(tmp_path),
        input={
            "objective": "Fix low risk bug",
            "risk_level": "low",
            "tests_passed": True,
            "judge_status": "PASS",
        },
    )

    result = orchestrator.run(request)

    assert result.status == "PASS"
    assert result.run_type == "workflow"
    assert result.result["dataset_candidates"][0]["status"] == "ACCEPTED"
