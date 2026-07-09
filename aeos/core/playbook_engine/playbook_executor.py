from __future__ import annotations

from pathlib import Path
from time import monotonic
from typing import Any, Optional

from aeos.core.playbook_engine.playbook_models import (
    PlaybookRequest,
    PlaybookResult,
    PlaybookContract,
    PlaybookStep,
)
from aeos.core.playbook_engine.playbook_loader import PlaybookLoader
from aeos.core.playbook_engine.playbook_contract_validator import PlaybookContractValidator
from aeos.core.playbook_engine.playbook_planner import PlaybookPlanner
from aeos.core.playbook_engine.playbook_result_validator import PlaybookResultValidator
from aeos.core.playbook_engine.playbook_reporter import PlaybookReporter
from aeos.core.skill_engine.skill_executor import SkillExecutor
from aeos.core.skill_engine.skill_models import SkillRequest, SkillResult
from aeos.core.tool_router.router import ToolRouter
from aeos.core.tool_router.tool_models import ToolRequest
from aeos.core.governance.governance_gate import GovernanceGate
from aeos.core.evidence.evidence_store import EvidenceStore
from aeos.core.evidence.evidence_reporter import EvidenceReporter


class PlaybookExecutor:
    def __init__(
        self,
        workspace_root: str = ".",
        tool_router: Optional[ToolRouter] = None,
        skill_executor: Optional[SkillExecutor] = None,
        governance_gate: Optional[GovernanceGate] = None,
        evidence_store: Optional[EvidenceStore] = None,
    ):
        self.workspace_root = Path(workspace_root)
        self.loader = PlaybookLoader(workspace_root)
        self.contract_validator = PlaybookContractValidator(workspace_root)
        self.planner = PlaybookPlanner()
        self.result_validator = PlaybookResultValidator()
        self.reporter = PlaybookReporter(workspace_root)
        self.tool_router = tool_router
        self.skill_executor = skill_executor
        self.governance_gate = governance_gate
        self.evidence_store = evidence_store or EvidenceStore()
        self.evidence_reporter = EvidenceReporter()

    def execute(self, request: PlaybookRequest) -> PlaybookResult:
        started = monotonic()
        execution_id = request.execution_id

        contract = self.loader.load_playbook_contract(request.playbook_id)

        validation = self.contract_validator.validate(request.playbook_id)
        self.evidence_store.store_record(execution_id, "playbook-contract-validation", validation)

        if contract is None or not validation["valid"]:
            result = PlaybookResult(
                execution_id=execution_id,
                playbook_id=request.playbook_id,
                status="BLOCKED",
                blocking_conditions=validation.get("findings", ["Playbook not found"]),
                duration_ms=int((monotonic() - started) * 1000),
            )
            self.evidence_store.store_record(execution_id, "playbook-result", result.to_dict())
            self.reporter.generate_report(execution_id, request, result)
            return result

        contract_path = contract.path or self.loader.resolver.get_playbook_path(request.playbook_id)
        if contract_path:
            fp = self.workspace_root / contract_path
            if not fp.exists():
                result = PlaybookResult(
                    execution_id=execution_id,
                    playbook_id=request.playbook_id,
                    status="BLOCKED",
                    blocking_conditions=[f"Playbook file does not exist: {fp}"],
                    duration_ms=int((monotonic() - started) * 1000),
                )
                self.evidence_store.store_record(execution_id, "playbook-result", result.to_dict())
                self.reporter.generate_report(execution_id, request, result)
                return result

        from aeos.core.skill_engine.skill_registry_resolver import SkillRegistryResolver
        skill_resolver = SkillRegistryResolver(str(self.workspace_root))
        all_skills = skill_resolver.load().keys()
        plan = self.planner.plan(contract, all_skills)

        if not plan["valid"]:
            result = PlaybookResult(
                execution_id=execution_id,
                playbook_id=request.playbook_id,
                status="BLOCKED",
                blocking_conditions=plan.get("cycles", []) + plan.get("unresolved", []),
                duration_ms=int((monotonic() - started) * 1000),
            )
            self.evidence_store.store_record(execution_id, "playbook-result", result.to_dict())
            self.reporter.generate_report(execution_id, request, result)
            return result

        if contract and contract.required_skills:
            missing_skills = [s for s in contract.required_skills if s not in all_skills]
            if missing_skills:
                result = PlaybookResult(
                    execution_id=execution_id,
                    playbook_id=request.playbook_id,
                    status="BLOCKED",
                    blocking_conditions=[f"Required skills not available: {missing_skills}"],
                    duration_ms=int((monotonic() - started) * 1000),
                )
                self.evidence_store.store_record(execution_id, "playbook-result", result.to_dict())
                self.reporter.generate_report(execution_id, request, result)
                return result

        if request.dry_run:
            result = PlaybookResult(
                execution_id=execution_id,
                playbook_id=request.playbook_id,
                status="PASS",
                steps=plan.get("execution_order", []),
                facts=[
                    {"claim": "Dry-run completed successfully", "evidence": execution_id},
                ],
                assumptions=[
                    {"assumption": "Skills would execute in planned order", "evidence_ref": execution_id},
                ],
                duration_ms=int((monotonic() - started) * 1000),
            )
            self.evidence_store.store_record(execution_id, "playbook-result", result.to_dict())
            self.reporter.generate_report(execution_id, request, result)
            return result

        completed: set[str] = set()
        step_results: list[dict[str, Any]] = []
        skill_results_list: list[dict[str, Any]] = []
        tool_results_list: list[dict[str, Any]] = []
        all_evidence_refs: list[str] = []

        if not contract:
            result = PlaybookResult(
                execution_id=execution_id,
                playbook_id=request.playbook_id,
                status="ERROR",
                blocking_conditions=["Playbook contract not loaded"],
                duration_ms=int((monotonic() - started) * 1000),
            )
            self.evidence_store.store_record(execution_id, "playbook-result", result.to_dict())
            self.reporter.generate_report(execution_id, request, result)
            return result

        dag = self.planner.dag

        while True:
            ready = dag.ready_steps(completed) if dag else []
            if not ready:
                break

            for step in ready:
                step_start = monotonic()
                step_result: dict[str, Any] = {
                    "step_id": step.id,
                    "description": step.description,
                    "skill": step.skill,
                    "status": "PENDING",
                    "result": None,
                    "error": None,
                    "duration_ms": 0,
                }

                if step.skill and self.skill_executor:
                    sr = SkillRequest(
                        execution_id=execution_id,
                        skill_id=step.skill,
                        actor=request.actor,
                        role=request.role,
                        input=request.input,
                    )
                    skill_result = self.skill_executor.execute(sr)

                    if skill_result.status == "BLOCKED":
                        result = PlaybookResult(
                            execution_id=execution_id,
                            playbook_id=request.playbook_id,
                            status="BLOCKED",
                            steps=step_results + [{
                                "step_id": step.id, "description": step.description,
                                "skill": step.skill, "status": "BLOCKED",
                                "error": f"Skill {step.skill} blocked: {skill_result.blocking_conditions}",
                                "duration_ms": int((monotonic() - step_start) * 1000),
                            }],
                            skill_results=skill_results_list + [skill_result.to_dict()],
                            tool_results=tool_results_list,
                            blocking_conditions=[f"Skill '{step.skill}' returned BLOCKED"],
                            evidence_refs=all_evidence_refs,
                            duration_ms=int((monotonic() - started) * 1000),
                        )
                        self.evidence_store.store_record(execution_id, "playbook-result", result.to_dict())
                        self.reporter.generate_report(execution_id, request, result)
                        return result

                    skill_results_list.append(skill_result.to_dict())
                    all_evidence_refs.extend(skill_result.evidence_refs)
                    step_result["status"] = skill_result.status
                    step_result["result"] = skill_result.to_dict()
                else:
                    step_result["status"] = "PASS"

                step_result["duration_ms"] = int((monotonic() - step_start) * 1000)
                step_results.append(step_result)
                completed.add(step.id)

                self.evidence_store.store_record(execution_id, "playbook-step-result", step_result)

        # Verify no skill returned BLOCKED
        has_blocked_skill = any(
            sr.get("status") == "BLOCKED" for sr in skill_results_list
        )

        result = PlaybookResult(
            execution_id=execution_id,
            playbook_id=request.playbook_id,
            status="BLOCKED" if has_blocked_skill else "PASS",
            steps=step_results,
            skill_results=skill_results_list,
            tool_results=tool_results_list,
            facts=[
                {"claim": f"Playbook {request.playbook_id} completed", "evidence": execution_id},
            ],
            assumptions=[
                {"assumption": "All steps executed in DAG order", "evidence_ref": execution_id},
            ],
            risks=[
                {"risk": "Playbook steps may have partial results", "evidence_ref": execution_id},
            ] if has_blocked_skill else [],
            recommendations=[
                {"recommendation": "Review step results for detailed output", "reason": "Step results contain execution details"},
            ],
            evidence_refs=all_evidence_refs,
            blocking_conditions=["One or more skills returned BLOCKED"] if has_blocked_skill else [],
            duration_ms=int((monotonic() - started) * 1000),
        )

        self.evidence_store.store_record(execution_id, "playbook-result", result.to_dict())
        self.reporter.generate_report(execution_id, request, result)
        return result
