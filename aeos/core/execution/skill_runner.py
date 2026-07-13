from __future__ import annotations

from pathlib import Path
from time import monotonic
from typing import Any

from aeos.core.evidence.evidence_manifest import StagedManifestBuilder
from aeos.core.evidence.evidence_store import EvidenceStore
from aeos.core.execution.execution_models import ExecutionRequest, ExecutionResult
from aeos.core.execution.skill_resolver import SkillResolver
from aeos.core.skill_engine.skill_executor import SkillExecutor
from aeos.core.skill_engine.skill_models import SkillRequest


class SkillRunner:
    """Runtime-facing skill runner with explicit dry-run semantics."""

    def __init__(self, aeos_root: str = ".", workspace_root: str = "."):
        self.aeos_root = Path(aeos_root).resolve()
        self.workspace_root = Path(workspace_root).resolve()
        self.resolver = SkillResolver(str(self.aeos_root))
        self.evidence_store = EvidenceStore(str(self.workspace_root / ".aeos" / "evidence"))

    def run(self, request: ExecutionRequest) -> ExecutionResult:
        started = monotonic()
        if request.run_type != "skill":
            return self._result(
                request,
                "ERROR",
                started,
                error=f"SkillRunner only supports run_type='skill', got '{request.run_type}'",
            )

        self.evidence_store.store_record(request.execution_id, "runtime-request", request.to_dict())

        resolved = self.resolver.resolve(request.entity_id)
        if resolved is None:
            return self._result(
                request,
                "BLOCKED",
                started,
                blocking_conditions=[f"Skill '{request.entity_id}' not found in registry"],
            )

        self.evidence_store.store_record(
            request.execution_id,
            "skill-contract-validation",
            resolved.validation,
        )

        if not resolved.validation.get("valid", False):
            return self._result(
                request,
                "BLOCKED",
                started,
                result={"skill": resolved.to_dict()},
                blocking_conditions=list(resolved.validation.get("findings", [])),
            )

        missing_inputs = self._missing_inputs(resolved.contract.required_inputs, request.input)
        if missing_inputs:
            return self._result(
                request,
                "BLOCKED",
                started,
                result={"skill": resolved.to_dict()},
                blocking_conditions=[f"Missing required input: {name}" for name in missing_inputs],
            )

        if request.dry_run:
            return self._dry_run(request, resolved, started)

        executor = SkillExecutor(
            workspace_root=str(self.aeos_root),
            evidence_store=self.evidence_store,
        )
        skill_request = SkillRequest(
            execution_id=request.execution_id,
            skill_id=request.entity_id,
            actor=request.actor,
            role=request.role,
            input=request.input,
            approval_id=request.approval_id,
        )
        skill_result = executor.execute(skill_request)
        return self._result(
            request,
            skill_result.status,
            started,
            mode="execute",
            result=skill_result.to_dict(),
            evidence_refs=list(skill_result.evidence_refs),
            blocking_conditions=list(skill_result.blocking_conditions),
            error=skill_result.error,
        )

    def _dry_run(self, request: ExecutionRequest, resolved: Any, started: float) -> ExecutionResult:
        return self._result(
            request,
            "PASS",
            started,
            result={
                "skill": resolved.to_dict(),
                "planned_actions": list(resolved.contract.allowed_actions),
                "required_evidence": [
                    "runtime-request.jsonl",
                    "skill-contract-validation.jsonl",
                    "skill-result.jsonl",
                    "runtime-result.jsonl",
                    "runtime-evidence-manifest.json",
                ],
            },
            facts=[
                {
                    "claim": f"Skill '{request.entity_id}' resolved and validated",
                    "evidence_ref": "skill-contract-validation.jsonl",
                },
                {
                    "claim": "Dry-run did not execute external tools or mutate target files",
                    "evidence_ref": "runtime-request.jsonl",
                },
            ],
            risks=[
                {
                    "risk": "Dry-run validates contract and execution plan only; live tool behavior is not exercised.",
                    "evidence_ref": "runtime-request.jsonl",
                }
            ],
        )

    def _missing_inputs(self, required: list[str], supplied: dict[str, Any]) -> list[str]:
        return [name for name in required if name not in supplied or supplied.get(name) in (None, "")]

    def _result(
        self,
        request: ExecutionRequest,
        status: str,
        started: float,
        mode: str | None = None,
        result: dict[str, Any] | None = None,
        facts: list[dict[str, Any]] | None = None,
        risks: list[dict[str, Any]] | None = None,
        evidence_refs: list[str] | None = None,
        blocking_conditions: list[str] | None = None,
        error: str | None = None,
    ) -> ExecutionResult:
        execution_result = ExecutionResult(
            execution_id=request.execution_id,
            run_type=request.run_type,
            entity_id=request.entity_id,
            status=status,
            mode=mode or ("dry-run" if request.dry_run else "execute"),
            result=result or {},
            facts=facts or [],
            risks=risks or [],
            evidence_refs=evidence_refs or [],
            blocking_conditions=blocking_conditions or [],
            duration_ms=int((monotonic() - started) * 1000),
            error=error,
        )
        self.evidence_store.store_record(request.execution_id, "skill-result", execution_result.to_dict())
        self.evidence_store.store_record(request.execution_id, "runtime-result", execution_result.to_dict())
        manifest = self._generate_runtime_manifest(request.execution_id)
        execution_result.evidence_refs.append(manifest)
        return execution_result

    def _generate_runtime_manifest(self, execution_id: str) -> str:
        evidence_dir = self.workspace_root / ".aeos" / "evidence" / execution_id
        builder = StagedManifestBuilder(execution_id, str(evidence_dir), str(self.workspace_root))
        return builder.finalize_runtime_manifest()
