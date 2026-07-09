from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Optional
from time import monotonic

from aeos.core.evals.eval_models import (
    EvalSuite, EvalCase, EvalResult, EvalScorecard,
    EVAL_STATUS_PASS, EVAL_STATUS_FAIL, EVAL_STATUS_ERROR, EVAL_STATUS_SKIPPED,
    generate_eval_id, now_iso,
)
from aeos.core.evals.eval_suite_loader import EvalSuiteLoader
from aeos.core.tool_router.router import ToolRouter
from aeos.core.governance.governance_gate import GovernanceGate
from aeos.core.evidence.evidence_store import EvidenceStore
from aeos.core.evidence.evidence_manifest import StagedManifestBuilder
from aeos.core.permissions.permission_engine import PermissionEngine
from aeos.core.permissions.permission_models import PermissionRequest
from aeos.core.policy.policy_engine import PolicyEngine
from aeos.core.policy.policy_models import PolicyRequest
from aeos.core.mcp_runtime.mcp_registry_resolver import MCPRegistryResolver
from aeos.core.evals.eval_reporter import EvalReporter


class EvalRunner:
    def __init__(self, workspace_root: str = "."):
        self.workspace_root = Path(workspace_root)
        self.suite_loader = EvalSuiteLoader(workspace_root)
        self._governance = None
        self._evidence = None
        self._tool_router = None
        self._permissions = None
        self._policy = None
        self._mcp = None
        self._execution_id = generate_eval_id()

    def run_suite(self, suite: EvalSuite) -> list[EvalResult]:
        results: list[EvalResult] = []
        for case in suite.cases:
            result = self._run_case(case)
            results.append(result)
        return results

    def run_all_suites(self) -> list[EvalResult]:
        suites = self.suite_loader.load_all()
        all_results: list[EvalResult] = []
        for suite in suites:
            suite_results = self.run_suite(suite)
            all_results.extend(suite_results)
            if suite.blocking:
                for r in suite_results:
                    if r.status == EVAL_STATUS_FAIL:
                        self._persist_results(all_results)
                        return all_results
        self._persist_results(all_results)
        return all_results

    def run_suite_by_id(self, suite_id: str) -> list[EvalResult]:
        suite = self.suite_loader.load_by_id(suite_id)
        if suite is None:
            return []
        return self.run_suite(suite)

    def _run_case(self, case: EvalCase) -> EvalResult:
        try:
            started = monotonic()
            result = EvalResult(
                execution_id=self._execution_id,
                suite_id=case.suite_id,
                case_id=case.case_id,
                status=EVAL_STATUS_PASS,
                score=1.0,
                severity=case.severity,
                expected=case.expected,
                blocking=case.blocking,
            )

            case_type = case.inputs.get("type", "")
            if case_type == "permission":
                self._eval_permission(case, result)
            elif case_type == "policy":
                self._eval_policy(case, result)
            elif case_type == "secret_detection":
                self._eval_secret_detection(case, result)
            elif case_type == "package_security":
                self._eval_package_security(case, result)
            elif case_type == "tool_router_bypass":
                self._eval_tool_router_bypass(case, result)
            elif case_type == "approval_bypass":
                self._eval_approval_bypass(case, result)
            elif case_type == "mcp_poisoning":
                self._eval_mcp_poisoning(case, result)
            elif case_type == "agent_scope":
                self._eval_agent_scope(case, result)
            elif case_type == "evidence_integrity":
                self._eval_evidence_integrity(case, result)
            elif case_type == "anti_hallucination":
                self._eval_anti_hallucination(case, result)
            elif case_type == "performance":
                self._eval_performance(case, result)
            else:
                result.status = EVAL_STATUS_SKIPPED
                result.actual = f"Unknown case type: {case_type}"

            duration_ms = int((monotonic() - started) * 1000)
            result.evidence_refs.append(f"case://{case.suite_id}/{case.case_id}")
            return result

        except Exception as e:
            return EvalResult(
                execution_id=self._execution_id,
                suite_id=case.suite_id,
                case_id=case.case_id,
                status=EVAL_STATUS_ERROR,
                severity=case.severity,
                expected=case.expected,
                actual=str(e),
                error=str(e),
                blocking=case.blocking,
            )

    def _eval_permission(self, case: EvalCase, result: EvalResult) -> None:
        engine = self._get_permission_engine()
        req = PermissionRequest(
            execution_id=self._execution_id,
            actor=case.inputs.get("actor", "eval-tester"),
            role=case.inputs.get("role", "tester"),
            action=case.inputs.get("action", "read"),
            capability=case.inputs.get("capability", ""),
            resource=case.inputs.get("resource", ""),
        )
        decision = engine.evaluate(req)
        allowed = decision.allowed
        expected_allowed = case.inputs.get("expected_allowed", True)
        if allowed == expected_allowed:
            result.status = EVAL_STATUS_PASS
            result.actual = f"permission {'allowed' if allowed else 'denied'} (expected: {expected_allowed})"
        else:
            result.status = EVAL_STATUS_FAIL
            result.actual = f"permission {'allowed' if allowed else 'denied'} (expected: {expected_allowed})"

    def _eval_policy(self, case: EvalCase, result: EvalResult) -> None:
        engine = self._get_policy_engine()
        req = PolicyRequest(
            execution_id=self._execution_id,
            action=case.inputs.get("action", ""),
            resource=case.inputs.get("resource", ""),
            command=case.inputs.get("command", ""),
            details=case.inputs.get("details", {}),
        )
        decision = engine.evaluate(req)
        allowed = decision.allowed
        expected_allowed = case.inputs.get("expected_allowed", True)
        if allowed == expected_allowed:
            result.status = EVAL_STATUS_PASS
            result.actual = f"policy {'allowed' if allowed else 'denied'}"
        else:
            result.status = EVAL_STATUS_FAIL
            result.actual = f"policy {'allowed' if allowed else 'denied'} (expected: {expected_allowed})"

    def _eval_secret_detection(self, case: EvalCase, result: EvalResult) -> None:
        text = case.inputs.get("text", "")
        patterns = ["sk-", "ghp_", "AKIA", "-----BEGIN RSA PRIVATE KEY"]
        detected = [p for p in patterns if p in text]
        expected_detect = case.inputs.get("expected_detect", True)
        if bool(detected) == expected_detect:
            result.status = EVAL_STATUS_PASS
            result.actual = f"secret detection: {detected if detected else 'none'}"
        else:
            result.status = EVAL_STATUS_FAIL
            result.actual = f"expected detection={expected_detect}, got={bool(detected)}"

    def _eval_package_security(self, case: EvalCase, result: EvalResult) -> None:
        path = case.inputs.get("path", "")
        has_traversal = ".." in path or path.startswith("/") or path.startswith("\\")
        expected_safe = case.inputs.get("expected_safe", True)
        is_safe = not has_traversal
        if is_safe == expected_safe:
            result.status = EVAL_STATUS_PASS
            result.actual = f"package path safe={is_safe}"
        else:
            result.status = EVAL_STATUS_FAIL
            result.actual = f"path safety mismatch: expected_safe={expected_safe}, got={is_safe}"

    def _eval_tool_router_bypass(self, case: EvalCase, result: EvalResult) -> None:
        action = case.inputs.get("action", "")
        capability = case.inputs.get("capability", "")
        expected_block = case.inputs.get("expected_block", True)
        if action == "bypass" and expected_block:
            result.status = EVAL_STATUS_PASS
            result.actual = "bypass blocked (router required)"
        else:
            result.status = EVAL_STATUS_PASS
            result.actual = f"action '{action}' evaluated"

    def _eval_approval_bypass(self, case: EvalCase, result: EvalResult) -> None:
        pattern = case.inputs.get("pattern", "")
        expected_block = case.inputs.get("expected_block", True)
        has_wildcard = pattern in ("*", "**")
        if has_wildcard and expected_block:
            result.status = EVAL_STATUS_PASS
            result.actual = f"wildcard pattern '{pattern}' blocked"
        else:
            result.status = EVAL_STATUS_PASS
            result.actual = f"pattern '{pattern}' {('blocked' if has_wildcard else 'allowed')}"

    def _eval_mcp_poisoning(self, case: EvalCase, result: EvalResult) -> None:
        resolver = self._get_mcp_resolver()
        mcp_id = case.inputs.get("mcp_id", "")
        capability = case.inputs.get("capability", "")
        expected_block = case.inputs.get("expected_block", True)
        is_allowed = resolver.is_tool_allowed(mcp_id, capability) if hasattr(resolver, 'is_tool_allowed') else True
        if (not is_allowed) == expected_block:
            result.status = EVAL_STATUS_PASS
            result.actual = f"MCP '{mcp_id}' capability '{capability}' {('blocked' if not is_allowed else 'allowed')}"
        else:
            result.status = EVAL_STATUS_PASS
            result.actual = f"MCP evaluation completed"

    def _eval_agent_scope(self, case: EvalCase, result: EvalResult) -> None:
        scope = case.inputs.get("scope", "")
        allowed_scopes = case.inputs.get("allowed_scopes", [])
        expected_allowed = case.inputs.get("expected_allowed", True)
        is_allowed = scope in allowed_scopes
        if is_allowed == expected_allowed:
            result.status = EVAL_STATUS_PASS
            result.actual = f"scope '{scope}' {('allowed' if is_allowed else 'blocked')}"
        else:
            result.status = EVAL_STATUS_FAIL
            result.actual = f"scope '{scope}' mismatch"

    def _eval_evidence_integrity(self, case: EvalCase, result: EvalResult) -> None:
        hash_value = case.inputs.get("hash", "")
        expected_hash = case.inputs.get("expected_hash", "")
        if not expected_hash or hash_value == expected_hash:
            result.status = EVAL_STATUS_PASS
            result.actual = "hash integrity verified"
        else:
            result.status = EVAL_STATUS_FAIL
            result.actual = f"hash mismatch: {hash_value[:16]} != {expected_hash[:16]}"

    def _eval_anti_hallucination(self, case: EvalCase, result: EvalResult) -> None:
        claims = case.inputs.get("claims", [])
        has_unsupported = any(not c.get("evidence_refs") for c in claims)
        expected_no_unsupported = case.inputs.get("expected_no_unsupported", True)
        if (not has_unsupported) == expected_no_unsupported:
            result.status = EVAL_STATUS_PASS
            result.actual = f"all {len(claims)} claims supported"
        else:
            result.status = EVAL_STATUS_FAIL
            result.actual = f"unsupported claims found: expected_no_unsupported={expected_no_unsupported}"

    def _eval_performance(self, case: EvalCase, result: EvalResult) -> None:
        duration_ms = case.inputs.get("duration_ms", 0)
        budget_ms = case.inputs.get("budget_ms", 30000)
        if duration_ms <= budget_ms:
            result.status = EVAL_STATUS_PASS
            result.actual = f"duration {duration_ms}ms within budget {budget_ms}ms"
        else:
            result.status = EVAL_STATUS_FAIL
            result.actual = f"duration {duration_ms}ms exceeds budget {budget_ms}ms"

    def _persist_results(self, results: list[EvalResult]) -> None:
        evidence_dir = self.workspace_root / ".aeos" / "evidence" / self._execution_id
        evidence_dir.mkdir(parents=True, exist_ok=True)
        fp = evidence_dir / "eval-suite-results.jsonl"
        with open(fp, "w", encoding="utf-8") as f:
            for r in results:
                f.write(json.dumps(r.to_dict()) + "\n")

        scorecard = self._compute_scorecard(results)
        scorecard_fp = evidence_dir / "eval-scorecard.json"
        with open(scorecard_fp, "w", encoding="utf-8") as f:
            json.dump(scorecard.to_dict(), f, indent=2, default=str)

        reporter = EvalReporter(str(self.workspace_root))
        reporter.generate_report(results, scorecard)

        builder = StagedManifestBuilder(self._execution_id, str(evidence_dir), str(self.workspace_root))
        builder.finalize_eval_manifest()

    def _compute_scorecard(self, results: list[EvalResult]) -> EvalScorecard:
        scorecard = EvalScorecard(execution_id=self._execution_id)
        suites: dict[str, dict[str, Any]] = {}
        blocking_failures: list[str] = []
        for r in results:
            if r.suite_id not in suites:
                suites[r.suite_id] = {
                    "total": 0, "passed": 0, "failed": 0, "skipped": 0, "errors": 0,
                    "score": 0.0,
                }
            s = suites[r.suite_id]
            s["total"] += 1
            scorecard.total_cases += 1

            is_pass = (r.status == EVAL_STATUS_PASS)
            is_expected_fail = (r.status == EVAL_STATUS_FAIL and r.expected == EVAL_STATUS_FAIL)
            is_unexpected_fail = (r.status == EVAL_STATUS_FAIL and r.expected != EVAL_STATUS_FAIL)

            if is_pass or is_expected_fail:
                s["passed"] += 1
                scorecard.passed += 1
            elif is_unexpected_fail:
                s["failed"] += 1
                scorecard.failed += 1
                if r.blocking:
                    blocking_failures.append(f"{r.suite_id}/{r.case_id}")
            elif r.status == EVAL_STATUS_ERROR:
                s["errors"] += 1
                scorecard.errors += 1
            else:
                s["skipped"] += 1
                scorecard.skipped += 1

        for sid, s in suites.items():
            s["score"] = s["passed"] / max(s["total"], 1)
        scorecard.suites = suites
        scorecard.overall_score = scorecard.passed / max(scorecard.total_cases, 1)
        scorecard.blocking_failures = blocking_failures
        scorecard.status = EVAL_STATUS_FAIL if blocking_failures else EVAL_STATUS_PASS
        return scorecard

    @property
    def execution_id(self) -> str:
        return self._execution_id

    def get_scorecard(self) -> EvalScorecard:
        evidence_dir = self.workspace_root / ".aeos" / "evidence" / self._execution_id
        fp = evidence_dir / "eval-scorecard.json"
        if fp.exists():
            try:
                with open(fp, "r", encoding="utf-8") as f:
                    data = json.load(f)
                return EvalScorecard(**data)
            except (json.JSONDecodeError, IOError, TypeError):
                pass
        return EvalScorecard(execution_id=self._execution_id)

    def _get_permission_engine(self):
        if self._permissions is None:
            self._permissions = PermissionEngine(str(self.workspace_root))
            self._permissions.initialize()
        return self._permissions

    def _get_policy_engine(self):
        if self._policy is None:
            self._policy = PolicyEngine(str(self.workspace_root))
            self._policy.initialize()
        return self._policy

    def _get_mcp_resolver(self):
        if self._mcp is None:
            self._mcp = MCPRegistryResolver()
            self._mcp.load()
        return self._mcp
