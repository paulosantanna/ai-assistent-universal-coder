"""Judge v2 — validates execution completeness, evidence integrity, sandbox isolation, and safety."""

from datetime import datetime, timezone
from pathlib import Path
from enum import Enum
from typing import Optional

from aeos_workbench.execution.evidence_integrity import EvidenceManifest


class JudgeDecision(str, Enum):
    PASS = "PASS"
    BLOCKED = "BLOCKED"


AUTO_BLOCK_RULES = {
    "secret_exposed": "Secret exposed in output",
    "write_outside_sandbox": "Write outside sandbox without approval",
    "missing_evidence": "Required evidence missing",
    "destructive_change": "Destructive change without approval",
    "invented_architecture": "Architecture invented without evidence",
    "missing_execution_state": "execution-state.json not found",
    "missing_rollback_plan": "rollback-plan.json not found",
    "missing_step_results": "No step results generated",
    "missing_lcp_resolution": "LCPs were not resolved",
    "missing_permission_check": "Permissions were not evaluated",
    "no_artifacts_generated": "No sandbox artifacts generated",
    "assumptions_not_marked": "Assumptions were not marked",
    "modified_real_files": "Files outside .aeos were modified",
    "missing_evidence_manifest": "evidence-manifest.json not found",
    "missing_hash_chain": "hash-chain.jsonl not found",
    "evidence_hash_mismatch": "Artifact hash mismatch — evidence was tampered",
    "missing_required_artifact": "Required artifact missing",
    "evidence_altered_after_execution": "Evidence was altered after execution",
}


class JudgeV2:
    def __init__(self, workspace_root: Path, evidence_dir: Path, execution_id: str):
        self.workspace_root = workspace_root.resolve()
        self.evidence_dir = evidence_dir
        self.execution_id = execution_id
        self.blocking_reasons: list[str] = []
        self.warnings: list[str] = []
        self.score = 10.0

    def evaluate(self, execution_context: dict) -> dict:
        self.blocking_reasons = []
        self.warnings = []
        self.score = 10.0

        checks = {
            "execution_state_exists": self._check_execution_state(execution_context),
            "playbook_resolved": self._check_playbook_resolved(execution_context),
            "lcps_loaded": self._check_lcps_loaded(execution_context),
            "permissions_evaluated": self._check_permissions_evaluated(execution_context),
            "tool_calls_registered": self._check_tool_calls_registered(execution_context),
            "artifacts_generated": self._check_artifacts_generated(execution_context),
            "no_external_files_changed": self._check_no_external_files_changed(execution_context),
            "no_secrets_exposed": self._check_no_secrets_exposed(execution_context),
            "assumptions_marked": self._check_assumptions_marked(execution_context),
            "rollback_plan_exists": self._check_rollback_plan_exists(execution_context),
            "step_results_exist": self._check_step_results_exist(execution_context),
            "evidence_manifest_exists": self._check_evidence_manifest_exists(),
            "hash_chain_exists": self._check_hash_chain_exists(),
            "artifact_hashes_valid": self._check_artifact_hashes_valid(execution_context),
        }

        for check_name, (passed, detail) in checks.items():
            if not passed:
                if detail in AUTO_BLOCK_RULES:
                    self.blocking_reasons.append(AUTO_BLOCK_RULES[detail])
                else:
                    self.blocking_reasons.append(detail)

        deduction_per_block = 2.0
        block_count = len(self.blocking_reasons)
        self.score = max(0.0, 10.0 - (block_count * deduction_per_block))

        warning_deduction = 0.5
        self.score = max(0.0, self.score - (len(self.warnings) * warning_deduction))

        decision = JudgeDecision.BLOCKED if self.blocking_reasons else JudgeDecision.PASS

        return {
            "judge_id": "judge-v2-aeos-001",
            "execution_id": self.execution_id,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "decision": decision.value,
            "final_score": round(self.score, 2),
            "blocking_reasons": self.blocking_reasons,
            "warnings": self.warnings,
            "checks": {k: {"passed": v[0], "detail": v[1]} for k, v in checks.items()},
            "deductions": {
                "blocking_deductions": block_count * deduction_per_block,
                "warning_deductions": len(self.warnings) * warning_deduction,
                "total_deductions": round((block_count * deduction_per_block) + (len(self.warnings) * warning_deduction), 2),
            },
        }

    def _check_execution_state(self, ctx: dict) -> tuple:
        path = ctx.get("execution_state_path")
        if path and Path(path).exists():
            return True, "execution-state.json exists"
        return False, "missing_execution_state"

    def _check_playbook_resolved(self, ctx: dict) -> tuple:
        if ctx.get("playbook_id") and ctx.get("playbook_definition"):
            return True, "Playbook was resolved"
        return False, "Playbook not resolved"

    def _check_lcps_loaded(self, ctx: dict) -> tuple:
        lcps = ctx.get("resolved_lcps", [])
        if lcps:
            return True, f"LCPs loaded: {', '.join(lcps[:3])}"
        return False, "missing_lcp_resolution"

    def _check_permissions_evaluated(self, ctx: dict) -> tuple:
        log = ctx.get("permission_log", [])
        if log:
            return True, f"{len(log)} permission decisions recorded"
        return False, "missing_permission_check"

    def _check_tool_calls_registered(self, ctx: dict) -> tuple:
        log = ctx.get("tool_decision_log", [])
        if log:
            return True, f"{len(log)} tool calls registered"
        return False, "No tool calls registered"

    def _check_artifacts_generated(self, ctx: dict) -> tuple:
        artifacts = ctx.get("generated_artifacts", [])
        if artifacts:
            return True, f"{len(artifacts)} artifacts generated"
        return False, "no_artifacts_generated"

    def _check_no_external_files_changed(self, ctx: dict) -> tuple:
        modified = ctx.get("files_modified_outside_aeos", [])
        if modified:
            return False, f"Modified files outside .aeos: {modified}"
        return True, "No files outside .aeos were modified"

    def _check_no_secrets_exposed(self, ctx: dict) -> tuple:
        secrets = ctx.get("secrets_exposed", [])
        if secrets:
            return False, "secret_exposed"
        return True, "No secrets exposed"

    def _check_assumptions_marked(self, ctx: dict) -> tuple:
        if ctx.get("assumptions_marked", False):
            return True, "Assumptions were marked"
        return False, "assumptions_not_marked"

    def _check_rollback_plan_exists(self, ctx: dict) -> tuple:
        if ctx.get("rollback_plan_path") and Path(ctx["rollback_plan_path"]).exists():
            return True, "rollback-plan.json exists"
        return False, "missing_rollback_plan"

    def _check_step_results_exist(self, ctx: dict) -> tuple:
        steps = ctx.get("step_results", [])
        if steps:
            return True, f"{len(steps)} step results generated"
        return False, "missing_step_results"

    def _check_evidence_manifest_exists(self) -> tuple:
        path = self.evidence_dir / self.execution_id / "evidence-manifest.json"
        if path.exists():
            return True, "evidence-manifest.json exists"
        return False, "missing_evidence_manifest"

    def _check_hash_chain_exists(self) -> tuple:
        path = self.evidence_dir / self.execution_id / "hash-chain.jsonl"
        if path.exists():
            return True, "hash-chain.jsonl exists"
        return False, "missing_hash_chain"

    def _check_artifact_hashes_valid(self, ctx: dict) -> tuple:
        manifest_path = self.evidence_dir / self.execution_id / "evidence-manifest.json"
        if not manifest_path.exists():
            return True, "No manifest to validate"

        result = EvidenceManifest.verify_execution(
            self.evidence_dir, self.execution_id, self.workspace_root
        )

        if not result["passed"]:
            details = "; ".join(result["errors"][:3])
            return False, f"evidence_hash_mismatch: {details}" if result["errors"] else (False, "evidence_altered_after_execution")

        return True, f"All {result['verified_count']} artifact hashes verified"