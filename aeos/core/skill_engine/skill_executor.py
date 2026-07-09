from __future__ import annotations

from pathlib import Path
from time import monotonic
from typing import Any, Optional

from aeos.core.skill_engine.skill_models import (
    SkillRequest,
    SkillResult,
    SkillContract,
    now_iso,
)
from aeos.core.skill_engine.skill_loader import SkillLoader
from aeos.core.skill_engine.skill_contract_validator import SkillContractValidator
from aeos.core.skill_engine.skill_context_builder import SkillContextBuilder
from aeos.core.skill_engine.skill_result_validator import SkillResultValidator
from aeos.core.skill_engine.skill_reporter import SkillReporter
from aeos.core.tool_router.router import ToolRouter
from aeos.core.tool_router.tool_models import ToolRequest
from aeos.core.governance.governance_gate import GovernanceGate
from aeos.core.governance.governance_models import GovernanceRequest
from aeos.core.evidence.evidence_store import EvidenceStore


class SkillExecutor:
    def __init__(
        self,
        workspace_root: str = ".",
        tool_router: Optional[ToolRouter] = None,
        governance_gate: Optional[GovernanceGate] = None,
        evidence_store: Optional[EvidenceStore] = None,
    ):
        self.workspace_root = Path(workspace_root)
        self.loader = SkillLoader(workspace_root)
        self.contract_validator = SkillContractValidator(workspace_root)
        self.context_builder = SkillContextBuilder()
        self.result_validator = SkillResultValidator()
        self.reporter = SkillReporter(workspace_root)
        self.tool_router = tool_router
        self.governance_gate = governance_gate
        self.evidence_store = evidence_store or EvidenceStore()

    def execute(self, request: SkillRequest) -> SkillResult:
        started = monotonic()
        execution_id = request.execution_id

        contract = self.loader.load_skill_contract(request.skill_id)

        if contract is None:
            result = SkillResult(
                execution_id=execution_id,
                skill_id=request.skill_id,
                status="BLOCKED",
                blocking_conditions=[f"Skill '{request.skill_id}' not found in registry"],
                duration_ms=int((monotonic() - started) * 1000),
            )
            self.evidence_store.store_record(execution_id, "skill-result", result.to_dict())
            self.reporter.generate_report(execution_id, request, result)
            return result

        validation = self.contract_validator.validate(request.skill_id)
        self.evidence_store.store_record(execution_id, "skill-contract-validation", validation)

        if not validation["valid"]:
            result = SkillResult(
                execution_id=execution_id,
                skill_id=request.skill_id,
                status="BLOCKED",
                blocking_conditions=validation["findings"],
                duration_ms=int((monotonic() - started) * 1000),
            )
            self.evidence_store.store_record(execution_id, "skill-result", result.to_dict())
            self.reporter.generate_report(execution_id, request, result)
            return result

        contract_path = contract.path or self.loader.resolver.get_skill_path(request.skill_id)
        if contract_path:
            fp = self.workspace_root / contract_path
            if not fp.exists():
                result = SkillResult(
                    execution_id=execution_id,
                    skill_id=request.skill_id,
                    status="BLOCKED",
                    blocking_conditions=[f"Skill file does not exist: {fp}"],
                    duration_ms=int((monotonic() - started) * 1000),
                )
                self.evidence_store.store_record(execution_id, "skill-result", result.to_dict())
                self.reporter.generate_report(execution_id, request, result)
                return result

        context = self.context_builder.build(request, contract)

        if self.governance_gate:
            gov_req = GovernanceRequest(
                execution_id=execution_id,
                action="skill.execute",
                actor=request.actor,
                role=request.role,
                capability=contract.capabilities[0] if contract.capabilities else "",
                resource=f"skill:{request.skill_id}",
            )
            gov_result = self.governance_gate.evaluate(gov_req)
            if gov_result.status in ("BLOCKED", "WAITING_APPROVAL"):
                result = SkillResult(
                    execution_id=execution_id,
                    skill_id=request.skill_id,
                    status=gov_result.status,
                    blocking_conditions=[gov_result.blocking_reason],
                    evidence_refs=gov_result.evidence_refs,
                    duration_ms=int((monotonic() - started) * 1000),
                )
                self.evidence_store.store_record(execution_id, "skill-result", result.to_dict())
                self.reporter.generate_report(execution_id, request, result)
                return result

        tool_results: list[dict[str, Any]] = []
        evidence_refs: list[str] = []

        if self.tool_router and contract:
            if "filesystem.read" in contract.allowed_actions:
                tr = ToolRequest(
                    execution_id=execution_id,
                    actor=request.actor,
                    role=request.role,
                    tool_id="filesystem-readonly",
                    action="filesystem.read",
                    capability=contract.capabilities[0] if contract.capabilities else "READ_FILES",
                    resource=request.input.get("target_path", "."),
                )
                tr_result = self.tool_router.route(tr)
                tool_results.append(tr_result.to_dict())
                evidence_refs.extend(tr_result.evidence_refs)

            if "filesystem.exists" in contract.allowed_actions:
                tr = ToolRequest(
                    execution_id=execution_id,
                    actor=request.actor,
                    role=request.role,
                    tool_id="filesystem-readonly",
                    action="filesystem.exists",
                    capability=contract.capabilities[0] if contract.capabilities else "READ_FILES",
                    resource=request.input.get("target_path", "."),
                )
                tr_result = self.tool_router.route(tr)
                tool_results.append(tr_result.to_dict())
                evidence_refs.extend(tr_result.evidence_refs)

            if "filesystem.write_sandbox" in contract.allowed_actions:
                tr = ToolRequest(
                    execution_id=execution_id,
                    actor=request.actor,
                    role=request.role,
                    tool_id="filesystem-write-sandbox",
                    action="filesystem.write_sandbox",
                    capability="WRITE_SANDBOX_FILES",
                    resource=f"{execution_id}/skill-output.json",
                    input={"content": {"execution_id": execution_id, "skill_id": request.skill_id}},
                )
                tr_result = self.tool_router.route(tr)
                tool_results.append(tr_result.to_dict())
                evidence_refs.extend(tr_result.evidence_refs)

            if "package.verify" in contract.allowed_actions:
                tr = ToolRequest(
                    execution_id=execution_id,
                    actor=request.actor,
                    role=request.role,
                    tool_id="package-local",
                    action="package.verify",
                    capability="PACKAGE_VERIFY",
                    resource="",
                )
                tr_result = self.tool_router.route(tr)
                tool_results.append(tr_result.to_dict())
                evidence_refs.extend(tr_result.evidence_refs)

        has_blocking = any(
            r.get("status") in ("BLOCKED", "ERROR") for r in tool_results
        )

        result = SkillResult(
            execution_id=execution_id,
            skill_id=request.skill_id,
            status="BLOCKED" if has_blocking else "PASS",
            facts=[
                {"claim": f"Skill {request.skill_id} executed", "evidence": str(evidence_refs) if evidence_refs else ""},
            ],
            assumptions=[
                {"assumption": "Skill execution used governed tool router", "evidence_ref": str(evidence_refs) if evidence_refs else ""},
            ],
            risks=[
                {"risk": "Execution may have blocking conditions", "evidence_ref": str(evidence_refs) if evidence_refs else ""},
            ] if has_blocking else [],
            recommendations=[
                {"recommendation": "Review tool results for detailed output", "reason": "Tool results contain execution details"},
            ],
            tool_results=tool_results,
            evidence_refs=evidence_refs,
            blocking_conditions=(
                [r.get("error", "Tool blocked") for r in tool_results if r.get("status") in ("BLOCKED", "ERROR")]
            ) if has_blocking else [],
            duration_ms=int((monotonic() - started) * 1000),
        )

        self.evidence_store.store_record(execution_id, "skill-result", result.to_dict())
        self.reporter.generate_report(execution_id, request, result)
        return result
