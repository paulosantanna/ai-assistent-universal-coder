from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import yaml

from aeos.core.evidence.evidence_store import EvidenceStore

from .context_planner import ContextPlanner
from .model_router import ModelRouter
from .training_data_curator import TrainingDataCurator
from .workflow_models import WorkflowPlan, WorkflowResult


class WorkflowKernel:
    def __init__(
        self,
        workspace_root: str = ".",
        aeos_root: str | None = None,
        evidence_store: EvidenceStore | None = None,
    ):
        self.workspace_root = Path(workspace_root).resolve()
        self.aeos_root = Path(aeos_root).resolve() if aeos_root else self.workspace_root
        self.evidence_store = evidence_store or EvidenceStore()
        self.context_planner = ContextPlanner(str(self.workspace_root), self.evidence_store)
        self.model_router = ModelRouter(str(self.workspace_root), str(self.aeos_root), self.evidence_store)
        self.training_data_curator = TrainingDataCurator(str(self.workspace_root), self.evidence_store)
        self.config = self._load_config()

    def plan_and_record(
        self,
        *,
        execution_id: str,
        objective: str,
        workflow_id: str | None = None,
        risk_level: str | None = None,
        target_path: str = ".",
        required_paths: list[str] | None = None,
        evidence_refs: list[str] | None = None,
        approval_id: str | None = None,
        tests_passed: bool = False,
        judge_status: str | None = None,
        eval_score: float | None = None,
        create_dataset_candidate: bool = True,
    ) -> WorkflowResult:
        workflow_id = workflow_id or self.config.get("default_workflow", "bug_fix")
        workflow = self.config["workflows"].get(workflow_id)
        if workflow is None:
            workflow_id = self.config.get("default_workflow", "bug_fix")
            workflow = self.config["workflows"][workflow_id]

        risk = risk_level or workflow.get("risk_default", "medium")
        context_pack = self.context_planner.build_context_pack(
            execution_id=execution_id,
            objective=objective,
            target_path=target_path,
            required_paths=required_paths,
            evidence_refs=evidence_refs,
        )

        decisions = []
        for stage in workflow.get("model_stages", []):
            decisions.append(
                self.model_router.decide(
                    execution_id=execution_id,
                    stage=stage,
                    risk_level=risk,
                    estimated_input_tokens=context_pack.estimated_tokens,
                    approval_id=approval_id,
                    deterministic_available=stage in {"search", "diff", "lint", "typecheck", "tests", "static_scan"},
                )
            )

        blocking = list(context_pack.blocking_conditions)
        for decision in decisions:
            if decision.status in {"BLOCKED", "WAITING_APPROVAL"}:
                blocking.extend(decision.blocking_conditions)

        plan = WorkflowPlan(
            execution_id=execution_id,
            workflow_id=workflow_id,
            objective=objective,
            risk_level=risk,
            stages=list(workflow.get("stages", [])),
            model_stages=list(workflow.get("model_stages", [])),
            context_pack_ref=f".aeos/evidence/{execution_id}/context-pack.json",
            model_decision_refs=[f".aeos/evidence/{execution_id}/model-routing-decisions.jsonl"],
            gates=self.config.get("gates", {}),
            status="BLOCKED" if blocking else "PASS",
            blocking_conditions=blocking,
        )

        dataset_candidates = []
        if create_dataset_candidate:
            dataset_type = "positive" if tests_passed and judge_status not in {"BLOCKED", "ERROR"} else "negative"
            dataset_candidates.append(
                self.training_data_curator.curate(
                    execution_id=execution_id,
                    dataset_type=dataset_type,
                    prompt=objective,
                    completion=json.dumps(plan.to_dict(), ensure_ascii=False),
                    source_refs=[plan.context_pack_ref, *plan.model_decision_refs, *(evidence_refs or [])],
                    tests_passed=tests_passed,
                    judge_status=judge_status,
                    eval_score=eval_score,
                )
            )

        status = "BLOCKED" if blocking else "PASS"
        result = WorkflowResult(
            execution_id=execution_id,
            workflow_id=workflow_id,
            status=status,
            plan=plan,
            context_pack=context_pack,
            model_decisions=decisions,
            dataset_candidates=dataset_candidates,
            evidence_refs=[
                f".aeos/evidence/{execution_id}/context-pack.json",
                f".aeos/evidence/{execution_id}/model-routing-decisions.jsonl",
            ],
            blocking_conditions=blocking,
        )
        self._persist_plan(plan)
        self.evidence_store.store_record(execution_id, "workflow-plan", plan.to_dict())
        self.evidence_store.store_record(execution_id, "workflow-result", result.to_dict())
        return result

    def _load_config(self) -> dict[str, Any]:
        path = self.aeos_root / "aeos" / "config" / "workflow-kernel.config.yaml"
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
        return data["workflow_kernel"]

    def _persist_plan(self, plan: WorkflowPlan) -> str:
        base = self.workspace_root / ".aeos" / "evidence" / plan.execution_id
        base.mkdir(parents=True, exist_ok=True)
        path = base / "workflow-plan.json"
        path.write_text(json.dumps(plan.to_dict(), indent=2, ensure_ascii=False), encoding="utf-8")
        return str(path)
