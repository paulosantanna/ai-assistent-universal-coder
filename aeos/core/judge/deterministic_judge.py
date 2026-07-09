from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any, Optional

from aeos.core.judge.judge_models import JudgeInput, JudgeFinding, JudgeResult, JudgeStatus, JUDGE_STATUS_PASS, JUDGE_STATUS_BLOCKED, JUDGE_STATUS_ERROR, JUDGE_STATUS_REVIEW, now_iso
from aeos.core.judge.judge_blocking_rules import CRITICAL_RULES, HIGH_RULES, is_critical
from aeos.core.evidence.evidence_manifest import compute_manifest_hash, STAGE_FILENAMES


class DeterministicJudge:
    def __init__(self, workspace_root: str = "."):
        self.workspace_root = Path(workspace_root)
        self._findings: list[JudgeFinding] = []
        self._blocking_rules: list[str] = []
        self._warnings: list[str] = []
        self._facts_validated: list[str] = []
        self._claims_rejected: list[str] = []
        self._missing_evidence: list[str] = []
        self._security_findings: list[str] = []
        self._policy_findings: list[str] = []
        self._permission_findings: list[str] = []
        self._performance_findings: list[str] = []
        self._recommendations: list[str] = []
        self._evidence_refs: list[str] = []

    def evaluate(self, judge_input: JudgeInput) -> JudgeResult:
        self._reset()
        self._check_evidence_manifest(judge_input)
        self._check_permissions(judge_input)
        self._check_policy(judge_input)
        self._check_governance(judge_input)
        self._check_tool_results(judge_input)
        self._check_skill_results(judge_input)
        self._check_playbook_results(judge_input)
        self._check_agent_results(judge_input)
        self._check_runtime_results(judge_input)
        self._check_claims(judge_input)
        self._check_approvals(judge_input)
        self._check_packages(judge_input)
        self._check_security(judge_input)
        self._check_performance(judge_input)

        score = self._compute_score()
        status = self._determine_status(score)

        return JudgeResult(
            execution_id=judge_input.execution_id,
            status=status,
            score=score,
            blocking_rules=self._blocking_rules,
            warnings=self._warnings,
            facts_validated=self._facts_validated,
            claims_rejected=self._claims_rejected,
            missing_evidence=self._missing_evidence,
            security_findings=self._security_findings,
            policy_findings=self._policy_findings,
            permission_findings=self._permission_findings,
            performance_findings=self._performance_findings,
            recommendations=self._recommendations,
            evidence_refs=self._evidence_refs,
            timestamp=now_iso(),
        )

    def has_critical_blockers(self) -> bool:
        return any(is_critical(r) for r in self._blocking_rules)

    def get_findings(self) -> list[JudgeFinding]:
        return self._findings

    def _reset(self) -> None:
        self._findings.clear()
        self._blocking_rules.clear()
        self._warnings.clear()
        self._facts_validated.clear()
        self._claims_rejected.clear()
        self._missing_evidence.clear()
        self._security_findings.clear()
        self._policy_findings.clear()
        self._permission_findings.clear()
        self._performance_findings.clear()
        self._recommendations.clear()
        self._evidence_refs.clear()

    def _add_finding(self, rule_id: str, status: str, detail: str = "", evidence_ref: str = "") -> None:
        self._findings.append(JudgeFinding(
            rule_id=rule_id, status=status, detail=detail, evidence_ref=evidence_ref,
        ))
        if status == "FAIL":
            if is_critical(rule_id):
                self._blocking_rules.append(rule_id)
            self._warnings.append(f"{rule_id}: {detail}")

    def _check_evidence_manifest(self, ji: JudgeInput) -> None:
        """Check evidence manifest integrity using same hash algo as generator.
        
        Uses compute_manifest_hash() which serializes WITHOUT manifest_sha256
        to match how the generator computed the hash — avoiding the self-referential
        hash bug where the file-on-disk hash never matches because it includes
        its own manifest_sha256 field.
        """
        if not ji.evidence_manifest_path:
            self._add_finding("missing_evidence_manifest", "FAIL", "No evidence manifest path provided")
            self._missing_evidence.append("evidence-manifest.json")
            return
        manifest_path = Path(ji.evidence_manifest_path)
        if not manifest_path.exists():
            self._add_finding("missing_evidence_manifest", "FAIL", f"Evidence manifest not found at {manifest_path}")
            self._missing_evidence.append(str(manifest_path))
            return
        try:
            with open(manifest_path, "r") as f:
                manifest = json.load(f)
            self._facts_validated.append(f"evidence-manifest loaded: {manifest.get('total_records', 0)} records")

            stored_hash = manifest.get("manifest_sha256", "")
            if stored_hash:
                computed = compute_manifest_hash(manifest)
                if computed != stored_hash:
                    self._add_finding("manifest_hash_mismatch", "FAIL",
                                      f"Hash mismatch: stored={stored_hash}, computed={computed}",
                                      evidence_ref=str(manifest_path))
                else:
                    self._facts_validated.append(f"manifest SHA256 verified: {computed[:16]}...")

            manifest_dir = manifest_path.parent
            for fe in manifest.get("files", []):
                fpath = fe.get("path", "")
                if Path(fpath).is_absolute():
                    full_path = Path(fpath)
                else:
                    full_path = (self.workspace_root / fpath)
                    if not full_path.exists():
                        full_path = manifest_dir / fpath
                if not full_path.exists():
                    self._add_finding("missing_evidence_manifest", "FAIL",
                                      f"Referenced file missing: {fpath}",
                                      evidence_ref=str(manifest_path))
                    self._missing_evidence.append(fpath)
                    continue
                expected_hash = fe.get("sha256", "")
                if expected_hash:
                    actual_hash = self._compute_file_hash(full_path)
                    if actual_hash != expected_hash:
                        self._add_finding("manifest_hash_mismatch", "FAIL",
                                          f"File hash mismatch: {fpath} (stored={expected_hash[:16]}..., actual={actual_hash[:16]}...)",
                                          evidence_ref=str(full_path))

            self._evidence_refs.append(str(manifest_path))
        except (json.JSONDecodeError, IOError) as e:
            self._add_finding("missing_evidence_manifest", "FAIL", f"Cannot read manifest: {e}")

    def _check_permissions(self, ji: JudgeInput) -> None:
        for dec in ji.permission_decisions:
            ref = dec.get("decision_id", "")
            status = dec.get("status", "")
            if status == "DENY":
                self._add_finding("permission_denied", "FAIL",
                                  f"Permission denied: {dec.get('action', '?')} for {dec.get('actor', '?')}",
                                  evidence_ref=ref)
                self._permission_findings.append(f"DENY: {dec.get('action', '?')}")
            elif status == "ALLOW":
                self._facts_validated.append(f"permission allowed: {dec.get('action', '?')}")
            if ref:
                self._evidence_refs.append(ref)

    def _check_policy(self, ji: JudgeInput) -> None:
        for dec in ji.policy_decisions:
            ref = dec.get("decision_id", "")
            status = dec.get("status", "")
            if status == "DENY":
                self._add_finding("policy_denied", "FAIL",
                                  f"Policy denied: {dec.get('action', '?')} - {dec.get('reason', '?')}",
                                  evidence_ref=ref)
                self._policy_findings.append(f"DENY: {dec.get('reason', '?')}")
            elif status == "ALLOW":
                self._facts_validated.append(f"policy allowed: {dec.get('action', '?')}")
            if ref:
                self._evidence_refs.append(ref)

    def _check_governance(self, ji: JudgeInput) -> None:
        for dec in ji.governance_decisions:
            ref = dec.get("decision_id", "")
            status = dec.get("status", "")
            if status in ("BLOCKED", "WAITING_APPROVAL"):
                reasons = dec.get("blocking_reasons", [])
                self._add_finding("governance_blocked", "FAIL",
                                  f"Governance blocked: {reasons}",
                                  evidence_ref=ref)
            elif status == "PASS":
                self._facts_validated.append("governance gate passed")
            if ref:
                self._evidence_refs.append(ref)

    def _check_tool_results(self, ji: JudgeInput) -> None:
        for tr in ji.tool_results:
            ref = tr.get("decision_id", "") or tr.get("result_id", "")
            status = tr.get("status", "")
            tool_id = tr.get("tool_id", "?")
            if status == "BLOCKED":
                self._add_finding("tool_router_bypass", "FAIL",
                                  f"Tool blocked: {tool_id} - {tr.get('error', '')}",
                                  evidence_ref=ref)
            elif status == "ERROR":
                self._add_finding("runtime_error", "FAIL",
                                  f"Tool error: {tool_id} - {tr.get('error', '')}",
                                  evidence_ref=ref)
            else:
                self._facts_validated.append(f"tool {tool_id} completed: {status}")

            output = tr.get("output", {})
            if isinstance(output, dict):
                self._check_secret_exposure(output, ref)
            if ref:
                self._evidence_refs.append(ref)

    def _check_skill_results(self, ji: JudgeInput) -> None:
        for sr in ji.skill_results:
            ref = sr.get("request_id", "")
            status = sr.get("status", "")
            if status in ("BLOCKED", "ERROR"):
                bcs = sr.get("blocking_conditions", [])
                self._add_finding("skill_blocked" if status == "BLOCKED" else "runtime_error", "FAIL",
                                  f"Skill {sr.get('skill_id', '?')}: {status} - {bcs}",
                                  evidence_ref=ref)
            elif status == "PASS":
                self._facts_validated.append(f"skill {sr.get('skill_id', '?')} passed")
            if ref:
                self._evidence_refs.append(ref)

    def _check_playbook_results(self, ji: JudgeInput) -> None:
        for pr in ji.playbook_results:
            ref = pr.get("request_id", "")
            status = pr.get("status", "")
            if status in ("BLOCKED", "ERROR"):
                bcs = pr.get("blocking_conditions", [])
                self._add_finding("playbook_blocked" if status == "BLOCKED" else "runtime_error", "FAIL",
                                  f"Playbook {pr.get('playbook_id', '?')}: {status} - {bcs}",
                                  evidence_ref=ref)
            elif status == "PASS":
                self._facts_validated.append(f"playbook {pr.get('playbook_id', '?')} passed")
            if ref:
                self._evidence_refs.append(ref)

    def _check_agent_results(self, ji: JudgeInput) -> None:
        for ar in ji.agent_results:
            ref = ar.get("task_id", "")
            status = ar.get("status", "")
            if status in ("BLOCKED", "ERROR"):
                bcs = ar.get("blocking_conditions", [])
                self._add_finding("agent_blocked" if status == "BLOCKED" else "runtime_error", "FAIL",
                                  f"Agent {ar.get('agent_id', '?')}: {status} - {bcs}",
                                  evidence_ref=ref)
            elif status == "PASS":
                self._facts_validated.append(f"agent {ar.get('agent_id', '?')} passed")
            if ref:
                self._evidence_refs.append(ref)

    def _check_runtime_results(self, ji: JudgeInput) -> None:
        for rr in ji.runtime_results:
            ref = rr.get("execution_id", "")
            status = rr.get("status", "")
            bcs = rr.get("blocking_conditions", [])
            if status in ("BLOCKED", "ERROR"):
                self._add_finding("runtime_error", "FAIL",
                                  f"Runtime {rr.get('run_type', '?')}: {status} - {bcs}",
                                  evidence_ref=ref)
            if bcs:
                for bc in bcs:
                    self._warnings.append(f"runtime blocking condition: {bc}")
            if ref:
                self._evidence_refs.append(ref)
            self._facts_validated.append(f"runtime {rr.get('run_type', '?')} status: {status}")

    def _check_claims(self, ji: JudgeInput) -> None:
        for claim in ji.claims:
            claim_text = claim.get("claim", "")
            has_evidence = bool(claim.get("evidence_refs"))
            if not has_evidence:
                self._add_finding("unsupported_claim", "FAIL",
                                  f"Claim without evidence: {claim_text[:100]}")
                self._claims_rejected.append(claim_text[:100])
            else:
                self._facts_validated.append(f"claim supported: {claim_text[:50]}")

    def _check_approvals(self, ji: JudgeInput) -> None:
        for apr in ji.approval_refs:
            ref = apr.get("approval_id", "")
            status = apr.get("status", "")
            pattern = apr.get("pattern", "")
            expires_at = apr.get("expires_at", "")

            if status == "MISSING":
                self._add_finding("approval_missing", "FAIL", f"Missing approval", evidence_ref=ref)
            if pattern == "*" or pattern == "**":
                self._add_finding("approval_wildcard", "FAIL",
                                  f"Wildcard approval pattern: {pattern}", evidence_ref=ref)
            if expires_at:
                try:
                    from datetime import datetime, timezone
                    expiry = datetime.fromisoformat(expires_at)
                    if expiry < datetime.now(timezone.utc):
                        self._add_finding("approval_expired", "FAIL",
                                          f"Approval expired at {expires_at}", evidence_ref=ref)
                except (ValueError, TypeError):
                    pass
            if ref:
                self._evidence_refs.append(ref)

    def _check_packages(self, ji: JudgeInput) -> None:
        for pkg in ji.package_refs:
            ref = pkg.get("package_id", "") or pkg.get("path", "")
            verified = pkg.get("verified", False)
            has_traversal = pkg.get("path_traversal_detected", False)
            has_absolute = pkg.get("absolute_path_detected", False)

            if not verified:
                self._add_finding("package_verify_failed", "FAIL",
                                  f"Package not verified: {pkg.get('path', '?')}", evidence_ref=ref)
            if has_traversal:
                self._add_finding("path_traversal_detected", "FAIL",
                                  f"Path traversal in package: {pkg.get('path', '?')}", evidence_ref=ref)
            if has_absolute:
                self._add_finding("path_traversal_detected", "FAIL",
                                  f"Absolute path in package: {pkg.get('path', '?')}", evidence_ref=ref)
            if ref:
                self._evidence_refs.append(ref)

    def _check_security(self, ji: JudgeInput) -> None:
        for tool_result in ji.tool_results:
            output = tool_result.get("output", {})
            if isinstance(output, dict):
                self._check_secret_exposure(output, tool_result.get("result_id", ""))
            error = tool_result.get("error", "")
            if error and ("AI" in error or "sk-" in error or "ghp_" in error):
                self._add_finding("secret_exposed", "FAIL",
                                  f"Potential secret in error: {error[:80]}",
                                  evidence_ref=tool_result.get("result_id", ""))

    def _check_secret_exposure(self, output: dict, ref: str) -> None:
        output_str = json.dumps(output)
        secret_patterns = ["sk-", "ghp_", "gho_", "ghu_", "ghs_", "AKIA", "-----BEGIN"]
        for pattern in secret_patterns:
            if pattern in output_str:
                self._add_finding("secret_exposed", "FAIL",
                                  f"Secret pattern '{pattern}' found in output",
                                  evidence_ref=ref)
                self._security_findings.append(f"secret pattern '{pattern}' in output")
                break

        write_scope = output.get("write_path", "") or output.get("target", "")
        if write_scope and ".." in str(write_scope):
            self._add_finding("write_outside_allowed_scope", "FAIL",
                              f"Write path traversal: {write_scope}", evidence_ref=ref)

    def _check_performance(self, ji: JudgeInput) -> None:
        if not ji.runtime_results:
            self._add_finding("performance_budget_unreported", "FAIL",
                              "No runtime results to evaluate performance")
            return
        for rr in ji.runtime_results:
            duration = rr.get("duration_ms", 0)
            if duration > 30000:
                self._add_finding("performance_budget_breached_without_justification", "FAIL",
                                  f"Execution took {duration}ms (budget: 30000ms)",
                                  evidence_ref=rr.get("execution_id", ""))
                self._performance_findings.append(f"duration {duration}ms > 30000ms")

    def _compute_score(self) -> float:
        total = len(self._findings)
        if total == 0:
            return 1.0
        failures = sum(1 for f in self._findings if f.status == "FAIL")
        critical_failures = sum(1 for f in self._findings if f.status == "FAIL" and is_critical(f.rule_id))
        if critical_failures > 0:
            return max(0.0, 1.0 - (critical_failures * 0.2) - (failures * 0.05))
        return max(0.0, 1.0 - (failures * 0.05))

    def _determine_status(self, score: float) -> JudgeStatus:
        if self.has_critical_blockers():
            return JUDGE_STATUS_BLOCKED
        if score >= 0.95:
            return JUDGE_STATUS_PASS
        if score >= 0.80:
            return JUDGE_STATUS_REVIEW
        return JUDGE_STATUS_BLOCKED

    @staticmethod
    def _compute_file_hash(path: Path) -> str:
        sha = hashlib.sha256()
        with open(path, "rb") as f:
            for chunk in iter(lambda: f.read(65536), b""):
                sha.update(chunk)
        return sha.hexdigest()
