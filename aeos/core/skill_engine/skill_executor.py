from __future__ import annotations

import importlib.util
import tempfile
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
from aeos.core.chromatic import ChromaticOrchestrator
from aeos.core.change_tracking import ChangeTracker
from aeos.core.token_budget import TokenBudgetGovernor


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
        self.contract_validator = SkillContractValidator(workspace_root, loader=self.loader)
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

        if request.skill_id == "chromatic-mega-brain":
            result = self._execute_chromatic_megabrain(request, started)
            self.evidence_store.store_record(execution_id, "skill-result", result.to_dict())
            self.reporter.generate_report(execution_id, request, result)
            return result

        if request.skill_id == "token-budget-governor":
            result = self._execute_token_budget_governor(request, started)
            self.evidence_store.store_record(execution_id, "skill-result", result.to_dict())
            self.reporter.generate_report(execution_id, request, result)
            return result

        if request.skill_id == "universal-project-factory":
            result = self._execute_universal_project_factory(request, started)
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

    def _execute_token_budget_governor(self, request: SkillRequest, started: float) -> SkillResult:
        prompt_scope = str(request.input.get("prompt_scope", ""))
        provider = str(request.input.get("provider", "unknown"))
        requested_output_tokens = int(request.input.get("requested_output_tokens", 2000))
        task_priority = str(request.input.get("task_priority", "normal"))
        subagent_count = int(request.input.get("subagent_count", 0))

        governor = TokenBudgetGovernor()
        decision = governor.evaluate(prompt_scope, provider, requested_output_tokens, task_priority)
        subagent_budget = governor.subagent_budget(decision.limit, subagent_count) if subagent_count else 0
        record = {**decision.to_dict(), "subagent_budget": subagent_budget}
        record_id = self.evidence_store.store_record(request.execution_id, "token-budget-decision", record)

        return SkillResult(
            execution_id=request.execution_id,
            skill_id=request.skill_id,
            status=decision.status,
            facts=[
                {
                    "claim": f"Token budget evaluated for provider {decision.provider}",
                    "evidence": record_id,
                }
            ],
            assumptions=[
                {
                    "assumption": "Token count uses a conservative character-based estimate.",
                    "evidence_ref": record_id,
                }
            ],
            recommendations=[
                {"recommendation": item, "reason": "Token budget governance"}
                for item in decision.recommendations
            ],
            tool_results=[
                {
                    "tool_id": "token-budget-governor",
                    "status": decision.status,
                    "result": record,
                }
            ],
            evidence_refs=[record_id],
            blocking_conditions=list(decision.blocking_conditions),
            duration_ms=int((monotonic() - started) * 1000),
        )

    def _execute_universal_project_factory(self, request: SkillRequest, started: float) -> SkillResult:
        planner = self._load_universal_project_planner()

        project_name = str(request.input.get("project_name", ""))
        objective = str(request.input.get("objective", ""))
        architecture = str(request.input.get("architecture", "unspecified"))
        languages = request.input.get("languages", [])
        databases = request.input.get("databases", [])
        deployment_target = str(request.input.get("deployment_target", "cloud"))
        token_budget = request.input.get("token_budget", {})

        plan = planner.project_plan(objective, architecture, languages, databases, deployment_target)
        matrix = planner.stack_matrix(languages, databases)
        manifest = planner.scaffold_manifest(project_name, architecture, languages)
        package = planner.scaffold_package(project_name, objective, architecture, languages, databases, deployment_target)
        checklist = planner.production_checklist(architecture, deployment_target)
        sandbox_dir = self._resolve_sandbox_dir(request)
        change_tracker = ChangeTracker(
            request.execution_id,
            sandbox_dir,
            "universal-project-factory scaffold generation",
        )
        generated_files = self._write_scaffold_artifacts(
            sandbox_dir,
            package.get("artifacts", []),
            change_tracker,
        )
        trace_outputs = change_tracker.write_manifests(sandbox_dir / ".aeos" / "rollback")
        result_payload = {
            "project_plan": plan,
            "stack_matrix": matrix,
            "scaffold_manifest": manifest,
            "scaffold_package": package,
            "production_checklist": checklist,
            "token_budget": token_budget,
            "sandbox_dir": str(sandbox_dir),
            "generated_files": generated_files,
            "change_count": len(change_tracker.records),
            "change_manifest": trace_outputs["change_manifest"],
            "rollback_plan": trace_outputs["rollback_plan"],
            "rollback_summary": trace_outputs["rollback_summary"],
        }
        record_id = self.evidence_store.store_record(request.execution_id, "universal-project-plan", result_payload)
        trace_record_id = self.evidence_store.store_record(
            request.execution_id,
            "change-trace",
            {
                "execution_id": request.execution_id,
                "sandbox_dir": str(sandbox_dir),
                "change_count": len(change_tracker.records),
                **trace_outputs,
            },
        )
        blockers = (
            list(plan.get("blocking_conditions", []))
            + list(manifest.get("blocking_conditions", []))
            + list(package.get("blocking_conditions", []))
        )

        return SkillResult(
            execution_id=request.execution_id,
            skill_id=request.skill_id,
            status="BLOCKED" if blockers else "PASS",
            facts=[
                {
                    "claim": "Universal zero-to-production plan generated",
                    "evidence": record_id,
                },
                {
                    "claim": "Generated scaffold changes are tracked with rollback metadata",
                    "evidence": trace_record_id,
                }
            ],
            assumptions=[
                {
                    "assumption": "Generated scaffold is a sandbox manifest until explicitly approved for application.",
                    "evidence_ref": record_id,
                }
            ],
            recommendations=[
                {
                    "recommendation": "Run documentation, security, tests, packaging and production readiness gates before applying scaffold.",
                    "reason": "Zero-to-production workflow requires production gates.",
                },
                {
                    "recommendation": "Review change-manifest.json and rollback-plan.md before approving generated files.",
                    "reason": "Rollback traceability is required for governed changes.",
                }
            ],
            tool_results=[
                {
                    "tool_id": "universal-project",
                    "status": "BLOCKED" if blockers else "PASS",
                    "result": result_payload,
                }
            ],
            evidence_refs=[record_id, trace_record_id],
            blocking_conditions=blockers,
            duration_ms=int((monotonic() - started) * 1000),
        )

    def _load_universal_project_planner(self):
        planner_path = self.workspace_root / "universal-project-mcp" / "src" / "universal_project_mcp" / "planner.py"
        spec = importlib.util.spec_from_file_location("universal_project_planner", planner_path)
        if spec is None or spec.loader is None:
            raise RuntimeError(f"Cannot load universal project planner at {planner_path}")
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module

    def _resolve_sandbox_dir(self, request: SkillRequest) -> Path:
        requested = request.input.get("sandbox_root")
        if requested:
            root = Path(str(requested)).resolve()
            allowed_roots = [
                Path("/tmp").resolve(),
                Path(tempfile.gettempdir()).resolve(),
                (self.workspace_root / ".aeos" / "tmp").resolve(),
                (self.workspace_root / ".aeos" / "sandbox").resolve(),
            ]
            if not any(root == allowed or allowed in root.parents for allowed in allowed_roots):
                root = (self.workspace_root / ".aeos" / "sandbox" / request.execution_id).resolve()
        else:
            root = (self.workspace_root / ".aeos" / "sandbox" / request.execution_id).resolve()
        root.mkdir(parents=True, exist_ok=True)
        return root

    def _write_scaffold_artifacts(
        self,
        sandbox_dir: Path,
        artifacts: list[dict[str, str]],
        change_tracker: ChangeTracker,
    ) -> list[str]:
        generated: list[str] = []
        base = sandbox_dir.resolve()
        for artifact in artifacts:
            rel = str(artifact.get("path", "")).strip()
            if not rel or rel.startswith("/") or ".." in Path(rel).parts:
                continue
            target = (base / rel).resolve()
            if base != target and base not in target.parents:
                continue
            record = change_tracker.write_text(target, str(artifact.get("content", "")))
            generated.append(record.path)
        return generated

    def _execute_chromatic_megabrain(self, request: SkillRequest, started: float) -> SkillResult:
        objective = str(request.input.get("objective", request.input.get("problem", ""))).strip()
        decision_type = str(request.input.get("decision_type", "architecture")).strip() or "architecture"
        constraints = request.input.get("constraints", [])
        evidence_refs = request.input.get("evidence_refs", request.evidence_refs)
        max_colors = int(request.input.get("max_colors", 5))

        if not isinstance(constraints, list):
            constraints = [str(constraints)]
        if not isinstance(evidence_refs, list):
            evidence_refs = [str(evidence_refs)]

        run = ChromaticOrchestrator().create_run(
            objective=objective,
            decision_type=decision_type,
            constraints=[str(item) for item in constraints],
            evidence_refs=[str(item) for item in evidence_refs],
            max_colors=max_colors,
        )
        run_record_id = self.evidence_store.store_record(request.execution_id, "chromatic-run", run.to_dict())

        return SkillResult(
            execution_id=request.execution_id,
            skill_id=request.skill_id,
            status="BLOCKED" if run.blocking_conditions else "PASS",
            facts=[
                {
                    "claim": "Chromatic Mega Brain selected bounded cognitive perspectives",
                    "evidence": run_record_id,
                    "selected_colors": run.selected_colors,
                },
                {
                    "claim": "Chromatic run generated handoffs, decision matrix and quality gates",
                    "evidence": run_record_id,
                },
            ],
            assumptions=[
                {
                    "assumption": "Color handoffs are execution scaffolds; final domain claims still require inspected evidence.",
                    "evidence_ref": run_record_id,
                }
            ],
            risks=[
                {
                    "risk": "High-impact decisions can overfit incomplete evidence if Judge review is skipped.",
                    "evidence_ref": run_record_id,
                }
            ],
            recommendations=[
                {
                    "recommendation": "Use selected color handoffs before architecture, migration, security or cloud readiness decisions.",
                    "reason": "The run separates evidence, risks, implementation, constraints and knowledge before synthesis.",
                },
                {
                    "recommendation": "Route synthesized recommendation through Judge when any blocking condition, high risk or cloud decision exists.",
                    "reason": "Chromatic analysis is advisory until validated.",
                },
            ],
            tool_results=[
                {
                    "tool_id": "chromatic-mega-brain",
                    "status": "BLOCKED" if run.blocking_conditions else "PASS",
                    "result": run.to_dict(),
                }
            ],
            evidence_refs=[run_record_id],
            blocking_conditions=list(run.blocking_conditions),
            duration_ms=int((monotonic() - started) * 1000),
        )
