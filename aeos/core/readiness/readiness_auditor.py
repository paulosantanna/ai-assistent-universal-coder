from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Optional

from aeos.core.readiness.readiness_models import (
    ReadinessResult, ReadinessScorecard,
    READINESS_PASS, READINESS_BLOCKED, READINESS_REVIEW, READINESS_ERROR,
    generate_readiness_id, now_iso,
)
from aeos.core.evidence.evidence_manifest import verify_staged_manifest, STAGE_FILENAMES
from aeos.core.evidence.execution_resolver import RESOLVE_LATEST_COMPLETE, resolve_execution


READINESS_CATEGORIES = [
    "architecture",
    "registry_integrity",
    "permission_policy_governance",
    "evidence_integrity",
    "tool_router_mcp",
    "skill_playbook_agent_runtime",
    "judge_layer",
    "eval_harness",
    "security",
    "package_supply_chain",
    "observability",
    "performance",
    "tests",
    "documentation",
    "runbooks",
    "production_safety",
]

CATEGORY_WEIGHTS = {
    "architecture": 0.05,
    "registry_integrity": 0.05,
    "permission_policy_governance": 0.08,
    "evidence_integrity": 0.08,
    "tool_router_mcp": 0.05,
    "skill_playbook_agent_runtime": 0.05,
    "judge_layer": 0.15,
    "eval_harness": 0.15,
    "security": 0.08,
    "package_supply_chain": 0.04,
    "observability": 0.03,
    "performance": 0.03,
    "tests": 0.06,
    "documentation": 0.02,
    "runbooks": 0.02,
    "production_safety": 0.06,
}


class ReadinessAuditor:
    def __init__(self, workspace_root: str = "."):
        self.workspace_root = Path(workspace_root)
        self._execution_id = generate_readiness_id()
        self._category_scores: dict[str, float] = {}
        self._category_details: dict[str, dict[str, Any]] = {}
        self._critical_blockers: list[dict[str, Any]] = []
        self._high_risks: list[dict[str, Any]] = []
        self._medium_risks: list[dict[str, Any]] = []
        self._recommendations: list[str] = []
        self._evidence_refs: list[str] = []
        self._gate_results: dict[str, Any] = {}
        self._resolved_execution_dir: Optional[Path] = None

    def audit(self) -> ReadinessResult:
        self._reset()
        self._resolve_consistent_execution()
        self._check_architecture()
        self._check_registry_integrity()
        self._check_permission_policy_governance()
        self._check_evidence_integrity()
        self._check_tool_router_mcp()
        self._check_skill_playbook_agent_runtime()
        self._check_judge_layer()
        self._check_eval_harness()
        self._check_security()
        self._check_package_supply_chain()
        self._check_observability()
        self._check_performance()
        self._check_tests()
        self._check_documentation()
        self._check_runbooks()
        self._check_production_safety()
        self._run_mandatory_gates()

        overall_score = self._compute_overall_score()
        status = self._determine_status(overall_score)

        return ReadinessResult(
            execution_id=self._execution_id,
            status=status,
            overall_score=overall_score,
            categories=dict(self._category_scores),
            critical_blockers=[b["description"] for b in self._critical_blockers],
            high_risks=[r["description"] for r in self._high_risks],
            medium_risks=[r["description"] for r in self._medium_risks],
            recommendations=list(self._recommendations),
            evidence_refs=list(self._evidence_refs),
            timestamp=now_iso(),
        )

    def get_scorecard(self) -> ReadinessScorecard:
        return ReadinessScorecard(
            execution_id=self._execution_id,
            status=self._determine_status(self._compute_overall_score()),
            overall_score=self._compute_overall_score(),
            categories=dict(self._category_scores),
            category_details=dict(self._category_details),
            critical_blockers=list(self._critical_blockers),
            high_risks=list(self._high_risks),
            medium_risks=list(self._medium_risks),
        )

    def get_execution_id(self) -> str:
        return self._execution_id

    def _reset(self) -> None:
        self._category_scores.clear()
        self._category_details.clear()
        self._critical_blockers.clear()
        self._high_risks.clear()
        self._medium_risks.clear()
        self._recommendations.clear()
        self._evidence_refs.clear()
        self._gate_results.clear()

    def _score_category(self, category: str, score: float, checks: list[dict]) -> None:
        self._category_scores[category] = score
        self._category_details[category] = {
            "score": score,
            "checks": checks,
        }
        for check in checks:
            severity = check.get("severity", "medium")
            desc = check.get("description", "")
            if severity == "critical" and not check.get("passed", True):
                self._critical_blockers.append(check)
            elif severity == "high" and not check.get("passed", True):
                self._high_risks.append(check)
            elif severity == "medium" and not check.get("passed", True):
                self._medium_risks.append(check)

    def _check_presence(self, path: Path, label: str, severity: str = "high") -> dict:
        exists = path.exists()
        return {
            "description": f"{label}: {'found' if exists else 'MISSING'}",
            "passed": exists,
            "severity": severity,
            "path": str(path),
        }

    def _load_json_file(self, path: Path) -> Optional[dict]:
        if path.exists():
            try:
                return json.loads(path.read_text(encoding="utf-8"))
            except (json.JSONDecodeError, IOError):
                pass
        return None

    def _normalize_jsonl_record(self, record: dict[str, Any]) -> dict[str, Any]:
        content = record.get("content")
        if not isinstance(content, dict):
            return record
        normalized = dict(content)
        for key in ("record_id", "record_type", "timestamp", "sha256"):
            if key in record and key not in normalized:
                normalized[key] = record[key]
        return normalized

    def _load_jsonl_first(self, path: Path) -> Optional[dict]:
        if path.exists():
            try:
                lines = path.read_text(encoding="utf-8").strip().splitlines()
                if lines:
                    return self._normalize_jsonl_record(json.loads(lines[0]))
            except (json.JSONDecodeError, IOError):
                pass
        return None

    def _resolve_consistent_execution(self) -> None:
        evidence_root = self.workspace_root / ".aeos" / "evidence"
        if evidence_root.exists():
            dirs = sorted([d for d in evidence_root.iterdir() if d.is_dir()], key=lambda d: d.stat().st_mtime, reverse=True)
            runtime_names = ("runtime-result.jsonl", "runtime_results.jsonl", "runtime_result.jsonl")
            for directory in dirs:
                runtime_fp = next((directory / name for name in runtime_names if (directory / name).exists()), None)
                judge_fp = directory / "judge-result.json"
                eval_fp = directory / "eval-scorecard.json"
                if runtime_fp and judge_fp.exists() and eval_fp.exists():
                    runtime_data = self._load_jsonl_first(runtime_fp) or {}
                    judge_data = self._load_json_file(judge_fp) or {}
                    eval_data = self._load_json_file(eval_fp) or {}
                    eval_score = float(eval_data.get("overall_score", 0.0) or 0.0)
                    if runtime_data.get("status") == "PASS" and judge_data.get("status") == "PASS" and eval_score >= 0.95:
                        self._resolved_execution_dir = directory
                        return

        _, execution_dir = resolve_execution(self.workspace_root, RESOLVE_LATEST_COMPLETE)
        if execution_dir.name != "evidence" and execution_dir.exists():
            self._resolved_execution_dir = execution_dir
        else:
            self._resolved_execution_dir = None

    def _find_latest_evidence(self, filename: str) -> Optional[Path]:
        return self._find_latest_evidence_any([filename])

    def _find_latest_evidence_any(self, filenames: list[str], *, consistent_execution: bool = False) -> Optional[Path]:
        if consistent_execution and self._resolved_execution_dir is not None:
            for filename in filenames:
                fp = self._resolved_execution_dir / filename
                if fp.exists():
                    return fp
            return None

        evidence_root = self.workspace_root / ".aeos" / "evidence"
        if not evidence_root.exists():
            return None
        dirs = sorted([d for d in evidence_root.iterdir() if d.is_dir()], key=lambda d: d.stat().st_mtime, reverse=True)
        for d in dirs:
            for filename in filenames:
                fp = d / filename
                if fp.exists():
                    return fp
        return None

    def _check_architecture(self) -> None:
        checks = []
        core_dir = self.workspace_root / "aeos" / "core"
        checks.append(self._check_presence(core_dir / "runtime", "Runtime module", "critical"))
        checks.append(self._check_presence(core_dir / "judge", "Judge module", "critical"))
        checks.append(self._check_presence(core_dir / "evals", "Evals module", "critical"))
        checks.append(self._check_presence(core_dir / "readiness", "Readiness module", "critical"))
        checks.append(self._check_presence(core_dir / "skill_engine", "Skill Engine", "high"))
        checks.append(self._check_presence(core_dir / "playbook_engine", "Playbook Engine", "high"))
        checks.append(self._check_presence(core_dir / "agent_runtime", "Agent Runtime", "high"))
        checks.append(self._check_presence(core_dir / "tool_router", "Tool Router", "high"))
        checks.append(self._check_presence(core_dir / "governance", "Governance Gate", "high"))
        checks.append(self._check_presence(core_dir / "evidence", "Evidence Store", "high"))
        passed = sum(1 for c in checks if c["passed"])
        score = passed / max(len(checks), 1)
        self._score_category("architecture", score, checks)

    def _check_registry_integrity(self) -> None:
        checks = []
        derived_dir = self.workspace_root / ".aeos" / "derived" / "registries"
        checks.append(self._check_presence(derived_dir / "skills.consolidated.yaml", "Skills registry", "high"))
        checks.append(self._check_presence(derived_dir / "playbooks.consolidated.yaml", "Playbooks registry", "high"))
        checks.append(self._check_presence(derived_dir / "agents.consolidated.yaml", "Agents registry", "high"))

        manifest = self._load_json_file(derived_dir / "registry-merge-manifest.json")
        if manifest:
            failed = int(manifest.get("fragments_failed", 0) or 0)
            checks.append({
                "description": f"Registry merge manifest: fragments_failed={failed}",
                "passed": failed == 0,
                "severity": "critical",
                "path": str(derived_dir / "registry-merge-manifest.json"),
            })
            self._evidence_refs.append(str(derived_dir / "registry-merge-manifest.json"))
        else:
            checks.append({
                "description": "Registry merge manifest missing",
                "passed": False,
                "severity": "critical",
            })

        registry_evidence = self.workspace_root / ".aeos" / "evidence" / "registry-loader"
        orphans = self._load_json_file(registry_evidence / "orphans.json")
        if isinstance(orphans, list):
            critical_orphans = [o for o in orphans if o.get("severity") == "critical"]
            checks.append({
                "description": f"Registry critical orphans: {len(critical_orphans)}",
                "passed": len(critical_orphans) == 0,
                "severity": "critical",
                "path": str(registry_evidence / "orphans.json"),
            })
            self._evidence_refs.append(str(registry_evidence / "orphans.json"))
        else:
            checks.append({
                "description": "Registry orphan evidence missing",
                "passed": False,
                "severity": "critical",
            })

        cross = self._load_json_file(registry_evidence / "cross-dependency-validation.json")
        if isinstance(cross, dict):
            errors = []
            for findings in cross.values():
                if isinstance(findings, list):
                    errors.extend(f for f in findings if f.get("severity") == "error")
            checks.append({
                "description": f"Registry cross-dependency errors: {len(errors)}",
                "passed": len(errors) == 0,
                "severity": "critical",
                "path": str(registry_evidence / "cross-dependency-validation.json"),
            })
            self._evidence_refs.append(str(registry_evidence / "cross-dependency-validation.json"))
        else:
            checks.append({
                "description": "Registry cross-dependency evidence missing",
                "passed": False,
                "severity": "critical",
            })

        if derived_dir.exists():
            self._evidence_refs.append(str(derived_dir))
        passed = sum(1 for c in checks if c["passed"])
        score = passed / max(len(checks), 1)
        self._score_category("registry_integrity", score, checks)

    def _check_permission_policy_governance(self) -> None:
        checks = []
        config_dir = self.workspace_root / "aeos" / "config"
        checks.append(self._check_presence(config_dir / "permissions.yaml", "Permissions config", "critical"))
        checks.append(self._check_presence(config_dir / "policies.yaml", "Policies config", "critical"))
        checks.append(self._check_presence(config_dir / "aeos.config.yaml", "AEOS config", "high"))
        perm_dir = self.workspace_root / "aeos" / "core" / "permissions"
        pol_dir = self.workspace_root / "aeos" / "core" / "policy"
        gov_dir = self.workspace_root / "aeos" / "core" / "governance"
        checks.append(self._check_presence(perm_dir / "permission_engine.py", "PermissionEngine", "high"))
        checks.append(self._check_presence(pol_dir / "policy_engine.py", "PolicyEngine", "high"))
        checks.append(self._check_presence(gov_dir / "governance_gate.py", "GovernanceGate", "high"))
        passed = sum(1 for c in checks if c["passed"])
        score = passed / max(len(checks), 1)
        self._score_category("permission_policy_governance", score, checks)

    def _check_evidence_integrity(self) -> None:
        checks = []
        ev_dir = self.workspace_root / "aeos" / "core" / "evidence"
        checks.append(self._check_presence(ev_dir / "evidence_store.py", "EvidenceStore", "critical"))
        checks.append(self._check_presence(ev_dir / "evidence_reporter.py", "EvidenceReporter", "high"))
        evidence_root = self.workspace_root / ".aeos" / "evidence"
        if evidence_root.exists():
            exec_dirs = [d for d in evidence_root.iterdir() if d.is_dir()]
            checks.append({
                "description": f"Evidence directories: {len(exec_dirs)} executions",
                "passed": len(exec_dirs) > 0,
                "severity": "medium",
            })
            self._evidence_refs.append(str(evidence_root))
        passed = sum(1 for c in checks if c["passed"])
        score = passed / max(len(checks), 1)
        self._score_category("evidence_integrity", score, checks)

    def _check_tool_router_mcp(self) -> None:
        checks = []
        tr_dir = self.workspace_root / "aeos" / "core" / "tool_router"
        mcp_dir = self.workspace_root / "aeos" / "core" / "mcp_runtime"
        checks.append(self._check_presence(tr_dir / "router.py", "ToolRouter", "critical"))
        checks.append(self._check_presence(mcp_dir / "mcp_registry_resolver.py", "MCPRegistryResolver", "critical"))
        checks.append(self._check_presence(tr_dir / "tool_models.py", "Tool models", "high"))
        config_dir = self.workspace_root / "aeos" / "config"
        checks.append(self._check_presence(config_dir / "tool-router.config.yaml", "Tool router config", "high"))
        checks.append(self._check_presence(config_dir / "mcp-tools.allowlist.yaml", "MCP allowlist", "critical"))
        passed = sum(1 for c in checks if c["passed"])
        score = passed / max(len(checks), 1)
        self._score_category("tool_router_mcp", score, checks)

    def _check_skill_playbook_agent_runtime(self) -> None:
        checks = []
        checks.append(self._check_presence(self.workspace_root / "aeos" / "core" / "skill_engine" / "skill_executor.py", "SkillExecutor", "high"))
        checks.append(self._check_presence(self.workspace_root / "aeos" / "core" / "playbook_engine" / "playbook_executor.py", "PlaybookExecutor", "high"))
        checks.append(self._check_presence(self.workspace_root / "aeos" / "core" / "agent_runtime" / "agent_runtime.py", "AgentRuntime", "high"))
        checks.append(self._check_presence(self.workspace_root / "aeos" / "core" / "runtime" / "runtime_orchestrator.py", "RuntimeOrchestrator", "critical"))
        passed = sum(1 for c in checks if c["passed"])
        score = passed / max(len(checks), 1)
        self._score_category("skill_playbook_agent_runtime", score, checks)

    def _check_judge_layer(self) -> None:
        checks = []
        judge_dir = self.workspace_root / "aeos" / "core" / "judge"
        checks.append(self._check_presence(judge_dir / "judge_engine.py", "JudgeEngine", "critical"))
        checks.append(self._check_presence(judge_dir / "deterministic_judge.py", "DeterministicJudge", "critical"))
        checks.append(self._check_presence(judge_dir / "judge_models.py", "Judge models", "high"))
        checks.append(self._check_presence(judge_dir / "judge_blocking_rules.py", "Blocking rules", "high"))
        checks.append(self._check_presence(judge_dir / "judge_input_builder.py", "Input builder", "high"))
        checks.append(self._check_presence(judge_dir / "judge_scorecard.py", "Scorecard generator", "high"))
        checks.append(self._check_presence(judge_dir / "judge_reporter.py", "Judge reporter", "high"))

        judge_data: Optional[dict] = None
        judge_fp = self._find_latest_evidence_any(["judge-result.json"], consistent_execution=True)
        if judge_fp:
            judge_data = self._load_json_file(judge_fp)
            if judge_data:
                jstatus = judge_data.get("status", "")
                jscore = judge_data.get("score", 0.0)
                checks.append({
                    "description": f"Judge result: status={jstatus}, score={jscore:.4f}",
                    "passed": jstatus == "PASS",
                    "severity": "critical",
                })
                self._evidence_refs.append(str(judge_fp))
            else:
                checks.append({"description": "Judge result file is corrupted", "passed": False, "severity": "critical"})
        else:
            checks.append({"description": "No judge-result.json found — Judge may not have run", "passed": False, "severity": "critical"})

        passed = sum(1 for c in checks if c["passed"])
        score = passed / max(len(checks), 1)

        if judge_data and judge_data.get("status") == "BLOCKED":
            score = min(score, 0.3)

        self._score_category("judge_layer", score, checks)

    def _check_eval_harness(self) -> None:
        checks = []
        evals_dir = self.workspace_root / "aeos" / "core" / "evals"
        checks.append(self._check_presence(evals_dir / "eval_runner.py", "EvalRunner", "critical"))
        checks.append(self._check_presence(evals_dir / "eval_suite_loader.py", "EvalSuiteLoader", "high"))
        checks.append(self._check_presence(evals_dir / "eval_models.py", "Eval models", "high"))
        checks.append(self._check_presence(evals_dir / "eval_scorecard.py", "Eval scorecard", "high"))

        suites_dir = self.workspace_root / "aeos" / "evals"
        if suites_dir.exists():
            suite_dirs = [d for d in suites_dir.iterdir() if d.is_dir()]
            checks.append({
                "description": f"Eval suites: {len(suite_dirs)} found",
                "passed": len(suite_dirs) >= 2,
                "severity": "medium",
            })
            for sd in suite_dirs:
                if (sd / "suite.yaml").exists():
                    self._evidence_refs.append(str(sd / "suite.yaml"))
        else:
            checks.append({"description": "Eval suites directory missing", "passed": False, "severity": "high"})

        eval_data: Optional[dict] = None
        eval_fp = self._find_latest_evidence_any(["eval-scorecard.json"], consistent_execution=True)
        if eval_fp:
            eval_data = self._load_json_file(eval_fp)
            if eval_data:
                escore = eval_data.get("overall_score", 0.0)
                epassed = eval_data.get("passed", 0)
                etotal = eval_data.get("total_cases", 0)
                checks.append({
                    "description": f"Eval scorecard: {epassed}/{etotal} passed score={escore:.4f}",
                    "passed": escore >= 0.95,
                    "severity": "critical",
                })
                self._evidence_refs.append(str(eval_fp))
            else:
                checks.append({"description": "Eval scorecard file is corrupted", "passed": False, "severity": "critical"})
        else:
            checks.append({"description": "No eval-scorecard.json found — Evals may not have run", "passed": False, "severity": "critical"})

        passed = sum(1 for c in checks if c["passed"])
        score = passed / max(len(checks), 1)

        if eval_data is not None:
            escore = eval_data.get("overall_score", 0.0)
            score = min(score, escore)
            if escore < 0.5:
                score = min(score, 0.2)

        self._score_category("eval_harness", score, checks)

    def _check_security(self) -> None:
        checks = []
        config_dir = self.workspace_root / "aeos" / "config"
        checks.append(self._check_presence(config_dir / "security-hardening.config.yaml", "Security hardening config", "critical"))
        checks.append(self._check_presence(config_dir / "enterprise-security.config.yaml", "Enterprise security config", "critical"))
        package_fp = self._find_latest_evidence("package-verify-result.json")
        checks.append({
            "description": "Security/package adversarial smoke evidence found" if package_fp else "Security/package adversarial smoke evidence missing",
            "passed": package_fp is not None,
            "severity": "high",
            "path": str(package_fp) if package_fp else "",
        })
        if package_fp:
            self._evidence_refs.append(str(package_fp))
        passed = sum(1 for c in checks if c["passed"])
        score = passed / max(len(checks), 1)
        if self._critical_blockers:
            security_blockers = [b for b in self._critical_blockers if "security" in b.get("description", "").lower() or "mcp" in b.get("description", "").lower()]
            if security_blockers:
                score = min(score, 0.5)
        self._score_category("security", score, checks)

    def _check_package_supply_chain(self) -> None:
        checks = []
        pkg_fp = self._find_latest_evidence("package-verify-result.json")
        pkg_data = self._load_json_file(pkg_fp) if pkg_fp else None
        checks.append(self._check_presence(self.workspace_root / "aeos" / "core" / "packaging" / "package_verifier.py", "Package verifier", "critical"))
        if pkg_data:
            status = pkg_data.get("status", "UNKNOWN")
            checks.append({
                "description": f"Package smoke result: status={status}",
                "passed": status == "PASS",
                "severity": "critical",
                "path": str(pkg_fp),
            })
            self._evidence_refs.append(str(pkg_fp))
        else:
            checks.append({
                "description": "Package verification execution evidence missing",
                "passed": False,
                "severity": "critical",
            })
        passed = sum(1 for c in checks if c["passed"])
        score = passed / max(len(checks), 1)
        self._score_category("package_supply_chain", score, checks)

    def _check_observability(self) -> None:
        checks = []
        obs_dir = self.workspace_root / "aeos" / "core" / "observability"
        checks.append(self._check_presence(obs_dir, "Observability module", "medium"))
        config_dir = self.workspace_root / "aeos" / "config"
        checks.append(self._check_presence(config_dir / "observability.config.yaml", "Observability config", "medium"))
        runtime_fp = self._find_latest_evidence_any(["runtime-result.jsonl", "runtime_results.jsonl", "runtime_result.jsonl"], consistent_execution=True)
        checks.append({
            "description": "Runtime evidence available for observability review" if runtime_fp else "Runtime evidence missing for observability review",
            "passed": runtime_fp is not None,
            "severity": "high",
            "path": str(runtime_fp) if runtime_fp else "",
        })
        passed = sum(1 for c in checks if c["passed"])
        score = passed / max(len(checks), 1)
        self._score_category("observability", score, checks)

    def _check_performance(self) -> None:
        checks = []
        config_dir = self.workspace_root / "aeos" / "config"
        checks.append(self._check_presence(config_dir / "performance-budgets.yaml", "Performance budgets", "medium"))
        perf_dir = self.workspace_root / "aeos" / "core" / "performance"
        checks.append(self._check_presence(perf_dir, "Performance module", "medium"))
        passed = sum(1 for c in checks if c["passed"])
        score = passed / max(len(checks), 1)
        self._score_category("performance", score, checks)

    def _check_tests(self) -> None:
        checks = []
        tests_dir = self.workspace_root / "aeos" / "tests"
        checks.append(self._check_presence(tests_dir / "judge", "Judge tests", "high"))
        checks.append(self._check_presence(tests_dir / "evals", "Eval tests", "high"))
        checks.append(self._check_presence(tests_dir / "readiness", "Readiness tests", "high"))
        checks.append(self._check_presence(tests_dir / "runtime", "Runtime tests", "high"))
        verification_fp = self._find_latest_evidence("verification-result.json")
        verification_data = self._load_json_file(verification_fp) if verification_fp else None
        if verification_data:
            status = verification_data.get("status", "UNKNOWN")
            checks.append({
                "description": f"Verification suite result: status={status}, suite={verification_data.get('suite', 'unknown')}",
                "passed": status == "PASS",
                "severity": "critical",
                "path": str(verification_fp),
            })
            self._evidence_refs.append(str(verification_fp))
        else:
            checks.append({
                "description": "Verification suite execution evidence missing",
                "passed": False,
                "severity": "critical",
            })
        passed = sum(1 for c in checks if c["passed"])
        score = passed / max(len(checks), 1)
        self._score_category("tests", score, checks)

    def _check_documentation(self) -> None:
        checks = []
        checks.append(self._check_presence(self.workspace_root / "README.md", "README", "medium"))
        checks.append(self._check_presence(self.workspace_root / "aeos" / "tests" / "README_TEST_PLAN_v1.md", "Test plan", "medium"))
        passed = sum(1 for c in checks if c["passed"])
        score = passed / max(len(checks), 1)
        self._score_category("documentation", score, checks)

    def _check_runbooks(self) -> None:
        checks = []
        docs = [
            self.workspace_root / "README.md",
            self.workspace_root / "aeos" / "AEOS-GUIDE.md",
            self.workspace_root / "aeos" / "tests" / "README_TEST_PLAN_v1.md",
        ]
        for doc in docs:
            checks.append(self._check_presence(doc, f"Runbook source {doc.name}", "medium"))
        passed = sum(1 for c in checks if c["passed"])
        score = passed / max(len(checks), 1)
        self._score_category("runbooks", score, checks)

    def _check_production_safety(self) -> None:
        checks = []
        config_dir = self.workspace_root / "aeos" / "config"
        checks.append(self._check_presence(config_dir / "production-enterprise.config.yaml", "Production config", "critical"))
        checks.append(self._check_presence(config_dir / "v1-release-gates.yaml", "Release gates", "critical"))
        checks.append(self._check_presence(config_dir / "enterprise-ci-gates.yaml", "CI gates", "high"))
        reports_dir = self.workspace_root / ".aeos" / "reports"
        if reports_dir.exists():
            report_count = len(list(reports_dir.rglob("*.md")))
            checks.append({
                "description": f"Reports generated: {report_count}",
                "passed": report_count > 0,
                "severity": "medium",
            })
            self._evidence_refs.append(str(reports_dir))
        passed = sum(1 for c in checks if c["passed"])
        score = passed / max(len(checks), 1)
        self._score_category("production_safety", score, checks)

    def _run_mandatory_gates(self) -> None:
        gate_checks: list[dict] = []

        # Gate 1: Judge Status Gate
        judge_fp = self._find_latest_evidence_any(["judge-result.json"], consistent_execution=True)
        if judge_fp:
            judge_data = self._load_json_file(judge_fp)
            if judge_data:
                jstatus = judge_data.get("status", "")
                jscore = judge_data.get("score", 0.0)
                jblocking = judge_data.get("blocking_rules", [])
                self._gate_results["judge_status"] = {"status": jstatus, "score": jscore, "blocking_rules": jblocking}
                if jstatus == "BLOCKED":
                    gate_checks.append({
                        "description": f"Judge is BLOCKED (score={jscore:.4f}, blocking_rules={jblocking})",
                        "passed": False, "severity": "critical",
                    })
                elif jstatus == "REVIEW":
                    gate_checks.append({
                        "description": f"Judge is REVIEW (score={jscore:.4f})",
                        "passed": False, "severity": "high",
                    })
                else:
                    gate_checks.append({
                        "description": f"Judge passed (status={jstatus}, score={jscore:.4f})",
                        "passed": True, "severity": "critical",
                    })
            else:
                gate_checks.append({"description": "Judge result corrupted", "passed": False, "severity": "critical"})
        else:
            gate_checks.append({"description": "Judge result not found", "passed": False, "severity": "critical"})

        # Gate 2: Runtime Status Gate
        runtime_fp = self._find_latest_evidence_any(["runtime-result.jsonl", "runtime_results.jsonl", "runtime_result.jsonl"], consistent_execution=True)
        if runtime_fp:
            runtime_data = self._load_jsonl_first(runtime_fp)
            if runtime_data:
                rstatus = runtime_data.get("status", "UNKNOWN")
                self._gate_results["runtime_status"] = {"status": rstatus, "path": str(runtime_fp)}
                if rstatus in ("BLOCKED", "ERROR"):
                    gate_checks.append({
                        "description": f"Runtime is {rstatus}",
                        "passed": False, "severity": "critical",
                    })
                elif rstatus == "REVIEW":
                    gate_checks.append({
                        "description": "Runtime is REVIEW",
                        "passed": False, "severity": "high",
                    })
                elif rstatus == "PASS":
                    gate_checks.append({
                        "description": f"Runtime passed (status={rstatus})",
                        "passed": True, "severity": "critical",
                    })
                else:
                    gate_checks.append({
                        "description": f"Runtime status is unknown ({rstatus})",
                        "passed": False, "severity": "critical",
                    })
                self._evidence_refs.append(str(runtime_fp))
            else:
                gate_checks.append({"description": "Runtime result file corrupted", "passed": False, "severity": "critical"})
        else:
            gate_checks.append({"description": "Runtime result not found", "passed": False, "severity": "critical"})

        # Gate 3: Eval Score Gate
        eval_fp = self._find_latest_evidence_any(["eval-scorecard.json"], consistent_execution=True)
        if eval_fp:
            eval_data = self._load_json_file(eval_fp)
            if eval_data:
                escore = eval_data.get("overall_score", 0.0)
                epassed = eval_data.get("passed", 0)
                etotal = eval_data.get("total_cases", 0)
                self._gate_results["eval_score"] = {"score": escore, "passed": epassed, "total": etotal}
                if escore < 0.95:
                    gate_checks.append({
                        "description": f"Eval score {escore:.4f} below 0.95 ({epassed}/{etotal} passed)",
                        "passed": False, "severity": "critical",
                    })
                else:
                    gate_checks.append({
                        "description": f"Eval score {escore:.4f} meets 0.95 ({epassed}/{etotal} passed)",
                        "passed": True, "severity": "critical",
                    })
            else:
                gate_checks.append({"description": "Eval scorecard corrupted", "passed": False, "severity": "critical"})
        else:
            gate_checks.append({"description": "Eval scorecard not found", "passed": False, "severity": "critical"})

        # Gate 4: Evidence Manifest Gate (check all staged manifests)
        evidence_root = self.workspace_root / ".aeos" / "evidence"
        staged_manifests = ["runtime-evidence-manifest.json", "eval-evidence-manifest.json",
                            "judge-evidence-manifest.json", "readiness-evidence-manifest.json",
                            "evidence-manifest.json"]

        staged_results = {}
        for sm in staged_manifests:
            sm_fp = self._find_latest_evidence(sm)
            if sm_fp:
                sm_result = verify_staged_manifest(sm_fp)
                staged_results[sm] = sm_result
                if sm_result["passed"]:
                    gate_checks.append({
                        "description": f"Manifest '{sm}' verified ({sm_result['files_ok']} files)",
                        "passed": True, "severity": "critical",
                    })
                else:
                    for err in sm_result["file_errors"]:
                        gate_checks.append({
                            "description": f"Manifest '{sm}' FAILED: {err}",
                            "passed": False, "severity": "critical",
                        })
            else:
                gate_checks.append({
                    "description": f"Manifest '{sm}' NOT found",
                    "passed": False, "severity": "critical",
                })

        self._gate_results["staged_manifests"] = staged_results

        # Gate 5: Critical Blockers Gate
        if self._critical_blockers:
            descs = [b["description"] for b in self._critical_blockers]
            self._gate_results["critical_blockers"] = descs
            gate_checks.append({
                "description": f"Critical blockers: {len(descs)} total — {descs}",
                "passed": False, "severity": "critical",
            })
        else:
            gate_checks.append({"description": "No critical blockers", "passed": True, "severity": "critical"})

        # Gate 6: Report Existence Gate
        reports_dir = self.workspace_root / ".aeos" / "reports"
        for expected_report in ["judge-report.md", "evaluation-harness-report.md", "production-readiness-report.md"]:
            found = False
            if reports_dir.exists():
                for rdir in reports_dir.iterdir():
                    if rdir.is_dir() and (rdir / expected_report).exists():
                        found = True
                        break
            gate_checks.append({
                "description": f"Report '{expected_report}' {'found' if found else 'MISSING'}",
                "passed": found, "severity": "high",
            })

        for gc in gate_checks:
            severity = gc.get("severity", "critical")
            if not gc.get("passed", True):
                if severity == "critical":
                    self._critical_blockers.append(gc)
                elif severity == "high":
                    self._high_risks.append(gc)
                elif severity == "medium":
                    self._medium_risks.append(gc)

    def _compute_overall_score(self) -> float:
        if not self._category_scores:
            return 0.0
        weighted_sum = 0.0
        weight_total = 0.0
        for cat, score in self._category_scores.items():
            w = CATEGORY_WEIGHTS.get(cat, 0.02)
            weighted_sum += score * w
            weight_total += w
        if weight_total == 0:
            return 0.0
        score = weighted_sum / weight_total
        if self._critical_blockers:
            score = min(score, 0.5)
            critical_count = len(self._critical_blockers)
            score = max(0.1, score - (critical_count * 0.05))
        return max(0.0, min(1.0, score))

    def _determine_status(self, overall_score: float) -> str:
        if self._critical_blockers:
            return READINESS_BLOCKED
        if overall_score >= 0.95:
            return READINESS_PASS
        if overall_score >= 0.80:
            return READINESS_REVIEW
        return READINESS_BLOCKED
