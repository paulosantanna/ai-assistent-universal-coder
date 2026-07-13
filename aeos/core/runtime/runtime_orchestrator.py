from __future__ import annotations

import json
import hashlib
import shutil
from pathlib import Path
from time import monotonic
from typing import Any, Optional

from aeos.core.runtime.execution_context import ExecutionContext
from aeos.core.runtime.runtime_models import (
    RuntimeRequest,
    RuntimeResult,
    now_iso,
)
from aeos.core.runtime.runtime_reporter import RuntimeReporter
from aeos.core.config.config_loader import ConfigLoader
from aeos.core.permissions.permission_engine import PermissionEngine
from aeos.core.permissions.permission_models import PermissionRequest
from aeos.core.policy.policy_engine import PolicyEngine
from aeos.core.policy.policy_models import PolicyRequest
from aeos.core.governance.governance_gate import GovernanceGate
from aeos.core.governance.governance_models import GovernanceRequest
from aeos.core.evidence.evidence_store import EvidenceStore
from aeos.core.evidence.evidence_reporter import EvidenceReporter
from aeos.core.evidence.evidence_manifest import StagedManifestBuilder
from aeos.core.tool_router.router import ToolRouter
from aeos.core.tool_router.tool_models import ToolRequest
from aeos.core.mcp_runtime.mcp_registry_resolver import MCPRegistryResolver
from aeos.core.skill_engine.skill_executor import SkillExecutor
from aeos.core.skill_engine.skill_models import SkillRequest
from aeos.core.playbook_engine.playbook_executor import PlaybookExecutor
from aeos.core.playbook_engine.playbook_models import PlaybookRequest
from aeos.core.agent_runtime.agent_runtime import AgentRuntime
from aeos.core.agent_runtime.agent_models import AgentTask, generate_task_id
from aeos.core.judge.judge_engine import JudgeEngine
from aeos.core.judge.judge_models import JUDGE_STATUS_PASS
from aeos.core.evals.eval_runner import EvalRunner
from aeos.core.readiness.production_gate import ProductionGate
from aeos.core.execution.execution_models import ExecutionRequest
from aeos.core.execution.skill_runner import SkillRunner


class RuntimeOrchestrator:
    def __init__(self, workspace_root: str = ".", aeos_root: Optional[str] = None, target_path: Optional[str] = None):
        self.workspace_root = Path(workspace_root).resolve()
        self.aeos_root = Path(aeos_root).resolve() if aeos_root else self.workspace_root
        self.target_path = Path(target_path).resolve() if target_path else self.workspace_root
        self.config_loader = ConfigLoader(workspace_root, aeos_root=str(self.aeos_root))
        self.permission_engine = PermissionEngine(str(self.aeos_root))
        self.policy_engine = PolicyEngine(str(self.aeos_root))
        self.governance_gate = GovernanceGate(str(self.aeos_root))
        self.evidence_store = EvidenceStore()
        self.evidence_reporter = EvidenceReporter()
        self.tool_router = ToolRouter(
            workspace_root=str(self.aeos_root),
            governance_gate=self.governance_gate,
            evidence_store=self.evidence_store,
        )
        self.mcp_resolver = MCPRegistryResolver()
        self.skill_executor = SkillExecutor(
            workspace_root=str(self.aeos_root),
            tool_router=self.tool_router,
            governance_gate=self.governance_gate,
            evidence_store=self.evidence_store,
        )
        self.playbook_executor = PlaybookExecutor(
            workspace_root=str(self.aeos_root),
            tool_router=self.tool_router,
            skill_executor=self.skill_executor,
            governance_gate=self.governance_gate,
            evidence_store=self.evidence_store,
        )
        self.agent_runtime = AgentRuntime(
            workspace_root=str(self.aeos_root),
            tool_router=self.tool_router,
            skill_executor=self.skill_executor,
            playbook_executor=self.playbook_executor,
            governance_gate=self.governance_gate,
            evidence_store=self.evidence_store,
        )
        self.reporter = RuntimeReporter(str(self.aeos_root))
        self._judge_engine: Optional[JudgeEngine] = None
        self._eval_runner: Optional[EvalRunner] = None
        self._production_gate: Optional[ProductionGate] = None

    def initialize(self) -> None:
        self.config_loader.load()
        self.permission_engine.initialize()
        self.policy_engine.initialize()
        self.governance_gate.initialize()
        self.tool_router.initialize()
        self.mcp_resolver.load()

    def run_skill(self, request: RuntimeRequest) -> RuntimeResult:
        started = monotonic()
        execution_id = request.execution_id

        if request.dry_run:
            runner = SkillRunner(aeos_root=str(self.aeos_root), workspace_root=str(self.workspace_root))
            execution_result = runner.run(
                ExecutionRequest(
                    execution_id=execution_id,
                    run_type="skill",
                    entity_id=request.entity_id,
                    actor=request.actor,
                    role=request.role,
                    input=request.input,
                    target_path=request.target_path,
                    dry_run=True,
                    approval_id=request.approval_id,
                )
            )
            result = RuntimeResult(
                execution_id=execution_id,
                run_type="skill",
                entity_id=request.entity_id,
                status=execution_result.status,
                result=execution_result.to_dict(),
                evidence_refs=list(execution_result.evidence_refs),
                blocking_conditions=list(execution_result.blocking_conditions),
                duration_ms=int((monotonic() - started) * 1000),
                error=execution_result.error,
            )
            self.reporter.generate_report(execution_id, request, result)
            return result

        self.evidence_store.store_record(execution_id, "runtime-request", request.to_dict())

        sr = SkillRequest(
            execution_id=execution_id,
            skill_id=request.entity_id,
            actor=request.actor,
            role=request.role,
            input=request.input,
            approval_id=request.approval_id,
        )
        skill_result = self.skill_executor.execute(sr)

        result = RuntimeResult(
            execution_id=execution_id,
            run_type="skill",
            entity_id=request.entity_id,
            status=skill_result.status,
            result=skill_result.to_dict(),
            evidence_refs=list(skill_result.evidence_refs),
            blocking_conditions=skill_result.blocking_conditions,
            duration_ms=int((monotonic() - started) * 1000),
        )

        self.evidence_store.store_record(execution_id, "runtime-result", result.to_dict())
        self.reporter.generate_report(execution_id, request, result)

        manifest = self._generate_evidence_manifest(execution_id)
        result.evidence_refs.append(manifest)
        return result

    def run_playbook(self, request: RuntimeRequest) -> RuntimeResult:
        started = monotonic()
        execution_id = request.execution_id

        self.evidence_store.store_record(execution_id, "runtime-request", request.to_dict())

        pr = PlaybookRequest(
            execution_id=execution_id,
            playbook_id=request.entity_id,
            actor=request.actor,
            role=request.role,
            target_path=request.target_path,
            input=request.input,
            approval_id=request.approval_id,
            dry_run=request.dry_run,
        )
        playbook_result = self.playbook_executor.execute(pr)

        result = RuntimeResult(
            execution_id=execution_id,
            run_type="playbook",
            entity_id=request.entity_id,
            status=playbook_result.status,
            result=playbook_result.to_dict(),
            evidence_refs=list(playbook_result.evidence_refs),
            blocking_conditions=playbook_result.blocking_conditions,
            duration_ms=int((monotonic() - started) * 1000),
        )

        self.evidence_store.store_record(execution_id, "runtime-result", result.to_dict())
        self.reporter.generate_report(execution_id, request, result)

        manifest = self._generate_evidence_manifest(execution_id)
        result.evidence_refs.append(manifest)
        return result

    def run_agent_task(self, request: RuntimeRequest) -> RuntimeResult:
        started = monotonic()
        execution_id = request.execution_id

        self.evidence_store.store_record(execution_id, "runtime-request", request.to_dict())

        task = AgentTask(
            execution_id=execution_id,
            task_id=generate_task_id(),
            agent_id=request.entity_id,
            actor=request.actor,
            role=request.role,
            objective=request.input.get("objective", f"Execute {request.entity_id}"),
            scope=request.input,
            approval_id=request.approval_id,
        )
        agent_result = self.agent_runtime.execute_task(task)

        result = RuntimeResult(
            execution_id=execution_id,
            run_type="agent",
            entity_id=request.entity_id,
            status=agent_result.status,
            result=agent_result.to_dict(),
            evidence_refs=list(agent_result.evidence_refs),
            blocking_conditions=agent_result.blocking_conditions,
            duration_ms=int((monotonic() - started) * 1000),
        )

        self.evidence_store.store_record(execution_id, "runtime-result", result.to_dict())
        self.reporter.generate_report(execution_id, request, result)

        manifest = self._generate_evidence_manifest(execution_id)
        result.evidence_refs.append(manifest)
        return result

    def run(self, request: RuntimeRequest) -> RuntimeResult:
        if request.run_type == "skill":
            return self.run_skill(request)
        elif request.run_type == "playbook":
            return self.run_playbook(request)
        elif request.run_type == "agent":
            return self.run_agent_task(request)
        else:
            return RuntimeResult(
                execution_id=request.execution_id,
                run_type=request.run_type,
                entity_id=request.entity_id,
                status="ERROR",
                error=f"Unknown run_type: {request.run_type}",
            )

    def _generate_evidence_manifest(self, execution_id: str) -> str:
        evidence_base = self.workspace_root / ".aeos" / "evidence" / execution_id
        builder = StagedManifestBuilder(execution_id, str(evidence_base), str(self.workspace_root))
        return builder.finalize_runtime_manifest()

    @property
    def judge_engine(self) -> JudgeEngine:
        if self._judge_engine is None:
            self._judge_engine = JudgeEngine(str(self.aeos_root))
        return self._judge_engine

    @property
    def eval_runner(self) -> EvalRunner:
        if self._eval_runner is None:
            self._eval_runner = EvalRunner(str(self.aeos_root))
        return self._eval_runner

    @property
    def production_gate(self) -> ProductionGate:
        if self._production_gate is None:
            self._production_gate = ProductionGate(str(self.aeos_root))
        return self._production_gate

    def run_with_judge(self, request: RuntimeRequest) -> tuple[RuntimeResult, Any]:
        runtime_result = self.run(request)
        judge_result = self.judge_engine.evaluate(request.execution_id, request.target_path)
        return runtime_result, judge_result

    def run_with_evals(self, suite_id: str = "") -> Any:
        if suite_id:
            return self.eval_runner.run_suite_by_id(suite_id)
        return self.eval_runner.run_all_suites()

    def run_readiness_audit(self) -> Any:
        return self.production_gate.evaluate()

    def run_full_pipeline(self, request: RuntimeRequest, run_evals: bool = True, run_readiness: bool = True) -> dict[str, Any]:
        runtime_result = self.run(request)
        result: dict[str, Any] = {
            "runtime_result": runtime_result,
            "judge_result": None,
            "eval_results": None,
            "readiness_result": None,
            "pipeline_status": runtime_result.status,
        }

        judge_result = self.judge_engine.evaluate(request.execution_id, request.target_path)
        result["judge_result"] = judge_result
        if judge_result.status != JUDGE_STATUS_PASS:
            result["pipeline_status"] = "BLOCKED"

        if run_evals:
            eval_results = self.eval_runner.run_all_suites()
            result["eval_results"] = eval_results
            scorecard = self.eval_runner.get_scorecard()
            if scorecard.blocking_failures:
                result["pipeline_status"] = "BLOCKED"
            self._sync_evidence(request.execution_id, self.eval_runner._execution_id)

        if run_readiness:
            readiness_result = self.production_gate.evaluate()
            result["readiness_result"] = readiness_result
            if self.production_gate.is_blocked(readiness_result):
                result["pipeline_status"] = "BLOCKED"
            self._sync_evidence(request.execution_id, readiness_result.execution_id)

        return result

    def _sync_evidence(self, target_execution_id: str, source_execution_id: str) -> None:
        import shutil
        source_dir = self.workspace_root / ".aeos" / "evidence" / source_execution_id
        target_dir = self.workspace_root / ".aeos" / "evidence" / target_execution_id
        source_reports = self.workspace_root / ".aeos" / "reports" / source_execution_id
        target_reports = self.workspace_root / ".aeos" / "reports" / target_execution_id
        if source_dir.exists():
            target_dir.mkdir(parents=True, exist_ok=True)
            for f in source_dir.iterdir():
                if f.is_file():
                    shutil.copy2(f, target_dir / f.name)
        if source_reports.exists():
            target_reports.mkdir(parents=True, exist_ok=True)
            for f in source_reports.iterdir():
                if f.is_file():
                    shutil.copy2(f, target_reports / f.name)
