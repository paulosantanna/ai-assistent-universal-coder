"""Execution Orchestrator — ties all v0.2.1 components together for governed playbook execution."""

import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

import yaml

from aeos_workbench.execution.state_machine import ExecutionStateMachine, ExecutionState
from aeos_workbench.execution.approval_gateway import ApprovalGateway
from aeos_workbench.execution.sandbox_writer import SandboxWriter
from aeos_workbench.execution.rollback_manager import RollbackManager
from aeos_workbench.execution.lcp_resolver import LCPResolver
from aeos_workbench.execution.playbook_step_engine import PlaybookStepEngine
from aeos_workbench.execution.skill_quality_gates import SkillQualityGates
from aeos_workbench.execution.tool_router import ToolRouter
from aeos_workbench.execution.judge_v2 import JudgeV2, JudgeDecision
from aeos_workbench.execution.report_generator import ReportGenerator
from aeos_workbench.execution.documentation_playbook import DocumentationPlaybook
from aeos_workbench.execution.evidence_integrity import EvidenceManifest
from aeos_workbench.execution.cache_manager import CacheManager
from aeos_workbench.execution.rollback_encryption import RollbackEncryption


class ExecutionOrchestrator:
    def __init__(
        self,
        workspace_root: Path,
        mode: str = "sandbox",
        use_cache: bool = False,
        encrypt_rollback: bool = False,
        no_cache: bool = False,
    ):
        self.workspace_root = workspace_root.resolve()
        self.mode = mode
        self.use_cache = use_cache and not no_cache
        self.encrypt_rollback = encrypt_rollback
        self.execution_id = f"ex-{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S')}-{__import__('uuid').uuid4().hex[:6]}"

        self.aeos_dir = self.workspace_root / ".aeos"
        self.evidence_dir = self.aeos_dir / "evidence"
        self.sandbox_dir = self.aeos_dir / "sandbox"
        self.approvals_dir = self.aeos_dir / "approvals"
        self.reports_dir = self.aeos_dir / "reports"

        for d in [self.evidence_dir, self.sandbox_dir, self.approvals_dir, self.reports_dir]:
            d.mkdir(parents=True, exist_ok=True)

        self.state_machine = ExecutionStateMachine(self.execution_id)
        self.approval_gateway = ApprovalGateway(self.approvals_dir)
        self.sandbox_writer = SandboxWriter(self.workspace_root, self.execution_id)
        self.rollback_encryption = RollbackEncryption(self.workspace_root) if encrypt_rollback else None
        self.rollback_manager = RollbackManager(
            self.evidence_dir,
            self.execution_id,
            encryption=self.rollback_encryption,
            workspace_root=self.workspace_root,
        )
        self.cache_manager = CacheManager(self.workspace_root) if use_cache else None
        self.step_engine = PlaybookStepEngine(self.evidence_dir, self.execution_id)
        self.tool_router = ToolRouter(self.sandbox_writer, self.approval_gateway, self.execution_id, self.workspace_root)
        self.report_generator = ReportGenerator(self.reports_dir, self.execution_id)
        self.judge = JudgeV2(self.workspace_root, self.evidence_dir, self.execution_id)
        self.skill_gates = SkillQualityGates()
        self.evidence_manifest = EvidenceManifest(self.evidence_dir, self.execution_id)

        self.lcp_resolver = LCPResolver(
            self.workspace_root,
            self.workspace_root / "aeos" / "registries" / "lcps.registry.yaml",
        )

        self.playbook_definition: Optional[dict] = None
        self.resolved_lcps: dict = {}
        self.generated_artifacts: list[dict] = []
        self.risks: list[str] = []
        self.assumptions_marked = False
        self._cache_hit = False

    def run(self, playbook_id: str, target_path: Path, dry_run: bool = False) -> dict:
        try:
            self.state_machine.transition(ExecutionState.VALIDATING_CONFIG, "Starting validation")
            self._validate_config()

            self.state_machine.transition(ExecutionState.RESOLVING_PLAYBOOK, f"Resolving playbook: {playbook_id}")
            self._resolve_playbook(playbook_id)

            self.state_machine.transition(ExecutionState.RESOLVING_CONTEXT, "Resolving LCPs")
            self._resolve_context()

            self.state_machine.transition(ExecutionState.CHECKING_PERMISSIONS, "Checking permissions")
            self._check_permissions()

            self.state_machine.transition(ExecutionState.DRY_RUN, "Performing dry run")
            self._dry_run(target_path)

            if dry_run or self.mode == "dry-run":
                self.state_machine.transition(ExecutionState.PASSED, "Dry run completed — no actual execution")
                self.state_machine.save(self.evidence_dir)
                return {"status": "dry_run", "execution_id": self.execution_id}

            requires_approval = self._check_approval_needed(playbook_id)
            if requires_approval:
                self.state_machine.transition(ExecutionState.WAITING_APPROVAL, "Waiting for human approval")
                self.approval_gateway.create_approval_request(self.execution_id, f"playbook.{playbook_id}", {"playbook_id": playbook_id, "target": str(target_path)})
                approved = self.approval_gateway.is_approved(self.execution_id)
                if not approved:
                    print(f"[AEOS] Approval needed for playbook '{playbook_id}'")
                    print(f"[AEOS] Create: .aeos/approvals/{self.execution_id}.approval.yaml")
                    print(f"[AEOS] Set status: 'approved', decision: 'approved'")
                    self.state_machine.transition(ExecutionState.BLOCKED, "Awaiting approval — execution blocked")
                    self.state_machine.save(self.evidence_dir)
                    return {"status": "blocked_awaiting_approval", "execution_id": self.execution_id,
                            "message": f"Create .aeos/approvals/{self.execution_id}.approval.yaml to approve"}

            self.state_machine.transition(ExecutionState.EXECUTING, "Executing playbook")

            cache_key = None
            if self.cache_manager:
                cache_key = self._build_cache_key(playbook_id, target_path)
                cached = self.cache_manager.get(cache_key, playbook_id)
                if cached:
                    print(f"[AEOS] [CACHE] Cache hit for {playbook_id}: {len(cached['artifacts'])} artifacts restored")
                    execution_result = {"generated_artifacts": cached["artifacts"], "risks": [], "cached": True}
                    self._cache_hit = True
                else:
                    print(f"[AEOS] [CACHE] Cache miss for {playbook_id}")

            if not self._cache_hit:
                execution_result = self._execute_playbook(playbook_id, target_path)

            self.state_machine.transition(ExecutionState.COLLECTING_EVIDENCE, "Collecting evidence")
            self._collect_evidence(execution_result)

            self.state_machine.save(self.evidence_dir)
            self.rollback_manager.save(encrypt=self.encrypt_rollback)
            for step in self.step_engine.steps:
                self.step_engine.save_step(step)

            self._register_evidence_integrity(execution_result)

            if self.cache_manager and not execution_result.get("cached"):
                source_files = []
                if execution_result.get("files_analyzed"):
                    source_files = [self.workspace_root / f for f in execution_result["files_analyzed"]]
                self.cache_manager.set(
                    cache_key,
                    playbook_id,
                    source_files,
                    self.generated_artifacts,
                    playbook_risk_level=self.playbook_definition.get("risk_level", "low") if self.playbook_definition else "low",
                )

            self.state_machine.transition(ExecutionState.JUDGING, "Running Judge v2")
            judge_result = self._run_judge()

            if judge_result["decision"] == JudgeDecision.PASS.value:
                self.state_machine.transition(ExecutionState.PASSED, f"All checks passed — score: {judge_result['final_score']}/10")
            else:
                self.state_machine.transition(ExecutionState.BLOCKED, f"Blocked by Judge: {', '.join(judge_result.get('blocking_reasons', []))}")

            self.state_machine.save(self.evidence_dir)

            self._register_evidence_integrity(execution_result)

            self._generate_reports(judge_result, execution_result)

            result = {
                "status": judge_result["decision"],
                "execution_id": self.execution_id,
                "judge_score": judge_result["final_score"],
                "judge_decision": judge_result["decision"],
                "blocking_reasons": judge_result.get("blocking_reasons", []),
                "generated_artifacts": self.generated_artifacts,
                "evidence_path": str(self.evidence_dir / self.execution_id),
                "sandbox_path": str(self.sandbox_dir / self.execution_id),
                "reports_path": str(self.reports_dir / self.execution_id),
            }
            if self.cache_manager:
                result["cache_hit"] = self._cache_hit
            if self.rollback_encryption:
                result["rollback_encrypted"] = self.encrypt_rollback and self.rollback_encryption.available
            return result

        except Exception as e:
            import traceback
            tb = traceback.format_exc()
            print(f"[AEOS] [ERROR] {e}\n{tb}", file=__import__('sys').stderr)
            try:
                self.state_machine.transition(ExecutionState.FAILED, f"Error: {e}")
                self.state_machine.save(self.evidence_dir)
                self.rollback_manager.save()
            except Exception:
                pass
            return {"status": "failed", "execution_id": self.execution_id, "error": str(e)}

    def _build_cache_key(self, playbook_id: str, target_path: Path) -> str:
        pb_version = "1.0.0"
        skill_versions = {}
        if self.playbook_definition:
            pb_version = self.playbook_definition.get("version", "1.0.0")
            for skill_id in self.playbook_definition.get("required_skills", []):
                skill_versions[skill_id] = "1.0.0"
        return self.cache_manager.build_cache_key(
            playbook_id, pb_version, skill_versions, target_path
        ) if self.cache_manager else ""

    def _validate_config(self):
        config_path = self.workspace_root / "aeos" / "config" / "aeos.config.yaml"
        if not config_path.exists():
            raise FileNotFoundError(f"AEOS config not found: {config_path}")
        with open(config_path, encoding="utf-8") as f:
            cfg = yaml.safe_load(f)
        if not cfg or "aeos" not in cfg:
            raise ValueError("Invalid AEOS config: missing 'aeos' key")
        self.state_machine.metadata["config_version"] = cfg.get("aeos", {}).get("version", "unknown")

    def _resolve_playbook(self, playbook_id: str):
        registry_path = self.workspace_root / "aeos" / "registries" / "playbooks.registry.yaml"
        if not registry_path.exists():
            raise FileNotFoundError(f"Playbook registry not found: {registry_path}")
        with open(registry_path, encoding="utf-8") as f:
            registry = yaml.safe_load(f)
        for pb in registry.get("playbooks", []):
            if pb["id"] == playbook_id:
                self.playbook_definition = pb
                return
        raise ValueError(f"Playbook '{playbook_id}' not found in registry")

    def _resolve_context(self):
        stack_ids = None
        if self.playbook_definition:
            stack_ids = self.playbook_definition.get("required_lcps", [])
        self.resolved_lcps = self.lcp_resolver.resolve_for(
            self.playbook_definition.get("id", "unknown") if self.playbook_definition else "unknown", stack_ids)

    def _check_permissions(self):
        if not self.playbook_definition:
            return
        for agent in self.playbook_definition.get("required_agents", []):
            self.tool_router.authorize(f"agent.{agent}", actor=agent)

    def _check_approval_needed(self, playbook_id: str) -> bool:
        risk_map = {"low": 0, "medium": 1, "high": 2, "critical": 3}
        pb_risk = risk_map.get(self.playbook_definition.get("risk_level", "low"), 0) if self.playbook_definition else 0
        return pb_risk >= 2

    def _dry_run(self, target_path: Path):
        print(f"[AEOS] [DRY RUN] Would execute playbook: {self.playbook_definition.get('id', '?')}")
        print(f"[AEOS] [DRY RUN] Target: {target_path}")
        print(f"[AEOS] [DRY RUN] Sandbox: {self.sandbox_dir / self.execution_id}")
        print(f"[AEOS] [DRY RUN] LCPs: {list(self.resolved_lcps.get('resolved_lcps', []))}")
        print(f"[AEOS] [DRY RUN] No files were written.")

    def _execute_playbook(self, playbook_id: str, target_path: Path) -> dict:
        if playbook_id == "documentation-generation":
            from aeos_workbench.execution.documentation_playbook import DocumentationPlaybook
            playbook = DocumentationPlaybook(self.sandbox_writer, self.rollback_manager, self.step_engine, self.execution_id)
            result = playbook.execute(target_path)
        elif playbook_id == "security-secrets-audit":
            from aeos_workbench.execution.secrets_audit_playbook import SecretsAuditPlaybook
            playbook = SecretsAuditPlaybook(self.sandbox_writer, self.rollback_manager, self.step_engine, self.execution_id, self.reports_dir, self.evidence_dir)
            result = playbook.execute(target_path)
        elif playbook_id == "devcontainer-generation":
            from aeos_workbench.execution.devcontainer_playbook import DevcontainerPlaybook
            playbook = DevcontainerPlaybook(self.sandbox_writer, self.rollback_manager, self.step_engine, self.execution_id)
            result = playbook.execute(target_path)
        elif playbook_id == "test-recovery":
            from aeos_workbench.execution.test_recovery_playbook import TestRecoveryPlaybook
            playbook = TestRecoveryPlaybook(self.sandbox_writer, self.rollback_manager, self.step_engine, self.execution_id, self.reports_dir)
            result = playbook.execute(target_path)
        else:
            raise ValueError(f"Playbook '{playbook_id}' execution not implemented in v0.2.1")

        self.generated_artifacts = result.get("generated_artifacts", [])
        self.risks = result.get("risks", [])
        self.assumptions_marked = True
        return result

    def _collect_evidence(self, execution_result: dict):
        self.tool_router.authorize("evidence.collect", actor="system", context={"execution_id": self.execution_id})

    def _register_evidence_integrity(self, execution_result: dict):
        for art in self.generated_artifacts:
            ap = Path(art["path"])
            if ap.exists():
                self.evidence_manifest.register_artifact(
                    artifact_path=ap,
                    artifact_type=art.get("type", "unknown"),
                    producer_step="execution",
                )

        esp = self.evidence_dir / self.execution_id / "execution-state.json"
        if esp.exists():
            self.evidence_manifest.register_artifact(esp, "execution-state", "state-machine")

        rp = self.evidence_dir / self.execution_id / "rollback-plan.json"
        if rp.exists():
            self.evidence_manifest.register_artifact(rp, "rollback-plan", "rollback-manager")

        for step in self.step_engine.steps:
            sp = self.step_engine.save_step(step)
            if sp and sp.exists():
                self.evidence_manifest.register_artifact(sp, "step-result", f"step-engine-{step.get('step_id', 'unknown')}")

        self.evidence_manifest.save_manifest()
        self.evidence_manifest.save_hash_chain()
        self.evidence_manifest.save_integrity_report()

    def _run_judge(self) -> dict:
        steps = self.step_engine.steps
        permission_log = self.tool_router.get_decision_log()

        ctx = {
            "execution_state_path": str(self.evidence_dir / self.execution_id / "execution-state.json"),
            "playbook_id": self.playbook_definition.get("id") if self.playbook_definition else None,
            "playbook_definition": self.playbook_definition,
            "resolved_lcps": self.resolved_lcps.get("resolved_lcps", []),
            "permission_log": permission_log,
            "tool_decision_log": permission_log,
            "generated_artifacts": [a["path"] for a in self.generated_artifacts],
            "files_modified_outside_aeos": [],
            "secrets_exposed": [],
            "assumptions_marked": self.assumptions_marked,
            "rollback_plan_path": str(self.evidence_dir / self.execution_id / "rollback-plan.json"),
            "step_results": [s["step_id"] for s in steps],
            "step_count": len(steps),
        }
        return self.judge.evaluate(ctx)

    def _generate_reports(self, judge_result: dict, execution_result: dict):
        perm_log = self.tool_router.get_decision_log()

        execution_context = {
            "execution_id": self.execution_id,
            "playbook_id": self.playbook_definition.get("id") if self.playbook_definition else "?",
            "target_path": str(self.workspace_root),
            "mode": self.mode,
            "final_state": self.state_machine.state.value,
            "state_history": self.state_machine.history,
            "step_summary": self.step_engine.get_summary(),
            "permission_log": perm_log,
            "generated_artifacts": [a["path"] for a in self.generated_artifacts],
            "risks": self.risks,
        }

        self.report_generator.generate_execution_summary(execution_context)
        self.report_generator.generate_judge_report(judge_result)
        self.report_generator.generate_artifacts_index(self.generated_artifacts)


def run_playbook(
    playbook_id: str,
    target_path: str = ".",
    mode: str = "sandbox",
    dry_run: bool = False,
    use_cache: bool = False,
    no_cache: bool = False,
    encrypt_rollback: bool = False,
) -> dict:
    workspace = Path(target_path).resolve()
    orchestrator = ExecutionOrchestrator(
        workspace,
        mode=mode,
        use_cache=use_cache,
        no_cache=no_cache,
        encrypt_rollback=encrypt_rollback,
    )
    return orchestrator.run(playbook_id, workspace, dry_run=dry_run)