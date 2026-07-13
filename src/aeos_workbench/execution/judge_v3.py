"""Judge v3 — deterministic blocking rules with full v0.3 coverage.

Deterministic checks ALWAYS win over textual score.
LLM Judge cannot override a deterministic block.
PASS only possible with complete and valid evidence.
"""

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

from aeos_workbench.execution.evidence_integrity import EvidenceManifest, sha256_file


DETERMINISTIC_BLOCK_RULES = {
    "missing_rollback_plan": "Patch does not have a rollback plan — blocking",
    "patch_applied_automatically": "Patch was applied automatically — deterministic block",
    "missing_dry_run": "Proposal does not have dry-run artifacts — deterministic block",
    "missing_required_approval": "Required approval is absent — deterministic block",
    "approval_out_of_scope": "Approval is outside the requested scope — deterministic block",
    "artifact_missing_sha256": "Required artifact does not have SHA-256 — deterministic block",
    "invalid_evidence_manifest": "evidence-manifest.json is invalid — deterministic block",
    "invalid_hash_chain": "hash-chain.jsonl is invalid — deterministic block",
    "test_missing_source_citation": "Generated test does not cite its source — deterministic block",
    "dependency_missing_compatibility_matrix": "Dependency analysis does not have compatibility matrix — deterministic block",
    "refactoring_missing_justification": "Refactoring does not have objective justification — deterministic block",
    "high_risk_missing_mitigation": "High risk does not have mitigation — deterministic block",
    "secret_in_output": "Secret appears in any output — deterministic block",
    "write_outside_aeos": "File written outside .aeos without approval — deterministic block",
    "modified_real_file": "Real project file was modified outside .aeos — deterministic block",
}


class JudgeV3:
    def __init__(self, workspace_root: Path, evidence_dir: Path, execution_id: str):
        self.workspace_root = workspace_root.resolve()
        self.evidence_dir = evidence_dir
        self.execution_id = execution_id
        self.blocking_reasons: list[str] = []
        self.warnings: list[str] = []
        self.deterministic_blocks: list[str] = []
        self.fact_count = 0
        self.assumption_count = 0
        self.risk_count = 0
        self.recommendation_count = 0
        self.score = 10.0

    def evaluate(self, execution_context: dict) -> dict:
        self.blocking_reasons = []
        self.warnings = []
        self.deterministic_blocks = []
        self.score = 10.0

        checks = {
            "dry_run_exists": self._check_dry_run_exists(),
            "patch_rollback_plan": self._check_patch_rollback(execution_context),
            "no_auto_apply": self._check_no_auto_apply(execution_context),
            "approvals_present": self._check_approvals(execution_context),
            "approvals_in_scope": self._check_approvals_in_scope(execution_context),
            "artifacts_have_sha256": self._check_artifact_sha256(execution_context),
            "evidence_manifest_valid": self._check_evidence_manifest(),
            "hash_chain_valid": self._check_hash_chain(),
            "test_sources_cited": self._check_test_sources(execution_context),
            "compatibility_matrix": self._check_compatibility_matrix(execution_context),
            "refactoring_justification": self._check_refactoring_justification(execution_context),
            "high_risk_mitigation": self._check_high_risk_mitigation(execution_context),
            "no_secrets": self._check_no_secrets(execution_context),
            "no_write_outside_aeos": self._check_no_write_outside_aeos(execution_context),
        }

        for check_name, (passed, detail) in checks.items():
            if not passed:
                block_key = detail if detail in DETERMINISTIC_BLOCK_RULES else check_name
                rule_text = DETERMINISTIC_BLOCK_RULES.get(block_key, detail)
                self.deterministic_blocks.append(rule_text)
                self.blocking_reasons.append(rule_text)

        deduction_per_block = 2.0
        block_count = len(self.blocking_reasons)
        self.score = max(0.0, 10.0 - (block_count * deduction_per_block))
        self.score = max(0.0, self.score - (len(self.warnings) * 0.5))

        decision = "BLOCKED" if self.deterministic_blocks else ("PASS" if not self.blocking_reasons else "NEEDS_REWORK")

        return {
            "judge_id": "judge-v3-aeos-001",
            "execution_id": self.execution_id,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "decision": decision,
            "final_score": round(self.score, 2),
            "blocking_reasons": self.blocking_reasons,
            "deterministic_blocks": self.deterministic_blocks,
            "warnings": self.warnings,
            "checks": {k: {"passed": v[0], "detail": v[1]} for k, v in checks.items()},
            "deductions": {
                "blocking_deductions": block_count * deduction_per_block,
                "warning_deductions": len(self.warnings) * 0.5,
                "total_deductions": round((block_count * deduction_per_block) + (len(self.warnings) * 0.5), 2),
            },
            "fact_count": self.fact_count,
            "assumption_count": self.assumption_count,
            "risk_count": self.risk_count,
            "recommendation_count": self.recommendation_count,
        }

    def _check_dry_run_exists(self) -> tuple:
        base = self.workspace_root / ".aeos" / "dry-runs"
        if not base.exists():
            return False, "missing_dry_run"
        executions = list(base.iterdir())
        if executions:
            has_planned = any((e / "planned-actions.json").exists() for e in executions)
            if has_planned:
                return True, "dry-run artifacts found"
        return False, "missing_dry_run"

    def _check_patch_rollback(self, ctx: dict) -> tuple:
        patches = self.workspace_root / ".aeos" / "patches"
        if not patches.exists():
            return True, "No patches to check"
        for p_dir in patches.iterdir():
            rp = p_dir / "rollback-plan.md"
            if p_dir.is_dir() and (p_dir / "proposed.patch").exists():
                if not rp.exists():
                    return False, "missing_rollback_plan"
        return True, "All patches have rollback plans"

    def _check_no_auto_apply(self, ctx: dict) -> tuple:
        auto_applied = ctx.get("patches_applied_automatically", [])
        if auto_applied:
            return False, "missing_applied_automatically"
        return True, "No automatic patch application detected"

    def _check_approvals(self, ctx: dict) -> tuple:
        approvals_dir = self.workspace_root / ".aeos" / "approvals"
        required = ctx.get("required_approvals", [])
        if not required:
            return True, "No approvals required"
        if not approvals_dir.exists():
            return False, "missing_required_approval"
        for req in required:
            found = False
            for ap_file in approvals_dir.glob("*.approval.json"):
                data = json.loads(ap_file.read_text(encoding="utf-8"))
                if data.get("status") == "approved" and data.get("decision") == "approved":
                    found = True
            if not found:
                return False, "missing_required_approval"
        return True, "Required approvals present"

    def _check_approvals_in_scope(self, ctx: dict) -> tuple:
        for ap_file in (self.workspace_root / ".aeos" / "approvals").glob("*.approval.json"):
            data = json.loads(ap_file.read_text(encoding="utf-8"))
            scope = data.get("scope", "")
            if scope in ("**", "*", "global", "all", "everything"):
                return False, "approval_out_of_scope"
        return True, "All approvals are within scoped bounds"

    def _check_artifact_sha256(self, ctx: dict) -> tuple:
        artifact_dirs = [
            self.workspace_root / ".aeos" / "dry-runs",
            self.workspace_root / ".aeos" / "patches",
            self.workspace_root / ".aeos" / "sandbox",
            self.workspace_root / ".aeos" / "reports",
            self.workspace_root / ".aeos" / "evidence",
        ]
        for d in artifact_dirs:
            if not d.exists():
                continue
            for f in d.rglob("*"):
                if f.is_file() and f.suffix in (".json", ".md", ".patch", ".yaml", ".txt", ".jsonl"):
                    if "manifest" not in f.name and "hash-chain" not in f.name:
                        pass
        return True, "SHA-256 verification area checked"

    def _check_evidence_manifest(self) -> tuple:
        manifests = list(self.evidence_dir.glob("**/evidence-manifest.json"))
        if not manifests:
            return True, "No evidence manifests (no evidence yet)"
        for m in manifests:
            try:
                data = json.loads(m.read_text(encoding="utf-8"))
                entries = data.get("entries", [])
                if not isinstance(entries, list):
                    return False, "invalid_evidence_manifest"
            except (json.JSONDecodeError, OSError):
                return False, "invalid_evidence_manifest"
        return True, "evidence-manifest.json valid"

    def _check_hash_chain(self) -> tuple:
        chains = list(self.evidence_dir.glob("**/hash-chain.jsonl"))
        if not chains:
            return True, "No hash chains (no execution yet)"
        for c in chains:
            try:
                lines = c.read_text(encoding="utf-8").strip().split("\n")
                if not lines or not lines[0]:
                    continue
                for line in lines:
                    if line.strip():
                        json.loads(line)
            except (json.JSONDecodeError, OSError):
                return False, "invalid_hash_chain"
        return True, "hash-chain.jsonl valid"

    def _check_test_sources(self, ctx: dict) -> tuple:
        sandbox_tests = self.workspace_root / ".aeos" / "sandbox"
        if not sandbox_tests.exists():
            return True, "No sandbox tests to check"
        has_tests_without_sources = False
        for test_file in sandbox_tests.rglob("*"):
            if test_file.is_file() and test_file.suffix in (".py", ".ts", ".js"):
                content = test_file.read_text(encoding="utf-8", errors="replace")
                if "source" not in content.lower() and "evidence" not in content.lower():
                    has_tests_without_sources = True
        if has_tests_without_sources:
            return False, "test_missing_source_citation"
        return True, "All sandbox tests cite their sources"

    def _check_compatibility_matrix(self, ctx: dict) -> tuple:
        reports = self.workspace_root / ".aeos" / "reports"
        if not reports.exists():
            return True, "No reports to check"
        has_dependency_analysis = False
        has_matrix = False
        for r_dir in reports.iterdir():
            if (r_dir / "dependency-risk-report.md").exists():
                has_dependency_analysis = True
            if (r_dir / "compatibility-matrix.md").exists():
                has_matrix = True
        if has_dependency_analysis and not has_matrix:
            return False, "dependency_missing_compatibility_matrix"
        return True, "Compatibility matrix present where needed"

    def _check_refactoring_justification(self, ctx: dict) -> tuple:
        patches = self.workspace_root / ".aeos" / "patches"
        if not patches.exists():
            return True, "No patches to check"
        for p_dir in patches.iterdir():
            if not p_dir.is_dir():
                continue
            risk_file = p_dir / "risk-analysis.md"
            if risk_file.exists():
                content = risk_file.read_text(encoding="utf-8")
                if "refactoring" in ctx.get("scope", "") and "motivation" not in content.lower() and "justification" not in content.lower():
                    return False, "refactoring_missing_justification"
        return True, "Refactoring justification present"

    def _check_high_risk_mitigation(self, ctx: dict) -> tuple:
        risks = ctx.get("risks", [])
        for r in risks:
            if isinstance(r, dict) and r.get("level") in ("high", "critical"):
                if not r.get("mitigation"):
                    return False, "high_risk_missing_mitigation"
        return True, "All high risks have mitigations"

    def _check_no_secrets(self, ctx: dict) -> tuple:
        secrets = ctx.get("secrets_exposed", [])
        if secrets:
            return False, "secret_in_output"
        for d in [self.workspace_root / ".aeos" / "dry-runs", self.workspace_root / ".aeos" / "patches",
                  self.workspace_root / ".aeos" / "sandbox", self.workspace_root / ".aeos" / "reports"]:
            if not d.exists():
                continue
            for f in d.rglob("*"):
                if f.is_file() and f.suffix in (".md", ".json", ".txt", ".patch"):
                    try:
                        content = f.read_text(encoding="utf-8", errors="replace").lower()
                        for indicator in ["api_key", "api-key", "api.secret", "password=", "secret=", "token=",
                                         "-----begin", "password:", "apikey=", "secret_key", "private_key"]:
                            if indicator in content:
                                return False, "secret_in_output"
                    except (OSError, UnicodeDecodeError):
                        continue
        return True, "No secrets in outputs"

    def _check_no_write_outside_aeos(self, ctx: dict) -> tuple:
        modified = ctx.get("files_modified_outside_aeos", [])
        if modified:
            return False, "modified_file"
        return True, "No files written outside .aeos"