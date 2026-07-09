"""
AEOS Negative Tests — validates all critical gates block prohibited operations.
"""

import json
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent / "src" / "src"))


def test_01_tool_router_module_loads():
    from aeos.core.tool_router.router import ToolRouter
    assert ToolRouter is not None
    print("[PASS 01] ToolRouter module loads")


def test_02_mcp_runtime_module_loads():
    from aeos.core.mcp_runtime.runtime import MCPRuntime
    assert MCPRuntime is not None
    print("[PASS 02] MCPRuntime module loads")


def test_03_mcp_registry_returns_none_for_unknown():
    from aeos.core.mcp_runtime.registry import MCPRegistry
    import yaml
    with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False, encoding="utf-8") as f:
        f.write("mcps: []\n")
        f.flush()
        reg = MCPRegistry(f.name)
        reg.load()
        assert reg.resolve("nonexistent") is None
    print("[PASS 03] MCP registry returns None for unknown MCP")


def test_04_evidence_store_integrity():
    from aeos.core.evidence.store import EvidenceStore
    with tempfile.TemporaryDirectory() as td:
        store = EvidenceStore(td)
        store.write_tool_call("test", {"request": "test"}, {"result": "ok"})
        integrity = store.verify_integrity("test", "tool-calls")
        assert integrity["passed"]
    print("[PASS 04] Evidence store integrity check passes")


def test_05_redactor_detects_aws_key():
    from aeos.core.redaction.redactor import Redactor
    r = Redactor()
    redacted, findings = r.redact("AKIA1234567890123456")
    assert len(findings) > 0
    assert "[REDACTED:" in redacted
    print("[PASS 05] Redactor detects and redacts AWS keys")


def test_06_redactor_detects_jwt():
    from aeos.core.redaction.redactor import Redactor
    r = Redactor()
    redacted, findings = r.redact("eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiIxIn0.test")
    assert len(findings) > 0
    print("[PASS 06] Redactor detects JWT tokens")


def test_07_approval_rejects_expired():
    from aeos.core.approval.advanced_approval import AdvancedApproval, ApprovalValidator
    from datetime import datetime, timedelta, UTC
    expired = AdvancedApproval(
        execution_id="t", action="patch.apply", scope=".aeos/patches/**",
        approved_by="u", reason="t",
        expires_at=(datetime.now(UTC) - timedelta(hours=1)).isoformat()
    )
    v = ApprovalValidator()
    assert not v.validate(expired).get("allowed", False)
    print("[PASS 07] Approval rejects expired approvals")


def test_08_approval_rejects_wildcard_scope():
    from aeos.core.approval.advanced_approval import AdvancedApproval, ApprovalValidator
    from datetime import datetime, timedelta, UTC
    a = AdvancedApproval(
        execution_id="t", action="any", scope="**",
        approved_by="u", reason="t",
        expires_at=(datetime.now(UTC) + timedelta(hours=1)).isoformat()
    )
    assert not ApprovalValidator().validate(a).get("allowed", False)
    print("[PASS 08] Approval rejects wildcard scope '**'")


def test_09_approval_rejects_empty_reason():
    from aeos.core.approval.advanced_approval import AdvancedApproval, ApprovalValidator
    from datetime import datetime, timedelta, UTC
    a = AdvancedApproval(
        execution_id="t", action="any", scope=".aeos/patches/**",
        approved_by="u", reason="",
        expires_at=(datetime.now(UTC) + timedelta(hours=1)).isoformat()
    )
    assert not ApprovalValidator().validate(a).get("allowed", False)
    print("[PASS 09] Approval rejects empty reason")


def test_10_pack_marketplace_blocks_direct_active():
    from aeos.core.pack_marketplace.marketplace import PackMarketplace
    m = PackMarketplace()
    assert not m.can_transition("quarantine", "active")
    assert not m.can_transition("rejected", "active")
    print("[PASS 10] Pack marketplace blocks direct quarantine->active")


def test_11_pack_marketplace_allows_quarantine_to_staging():
    from aeos.core.pack_marketplace.marketplace import PackMarketplace
    m = PackMarketplace()
    assert m.can_transition("quarantine", "staging")
    print("[PASS 11] Pack marketplace allows quarantine->staging")


def test_12_pack_marketplace_allows_staging_to_active():
    from aeos.core.pack_marketplace.marketplace import PackMarketplace
    m = PackMarketplace()
    assert m.can_transition("staging", "active")
    print("[PASS 12] Pack marketplace allows staging->active")


def test_13_conflict_detector_write_write():
    from aeos.core.parallel_execution.conflict_detector import ConflictDetector
    from aeos.core.parallel_execution.contracts import StepResourceSet
    cd = ConflictDetector()
    steps = [
        StepResourceSet(step_id="a", write_set=["x"]),
        StepResourceSet(step_id="b", write_set=["x"]),
    ]
    conflicts = cd.detect(steps)
    assert any(c.conflict_type == "WRITE_WRITE" for c in conflicts)
    print("[PASS 13] Conflict detector finds WRITE_WRITE")


def test_14_conflict_detector_read_write():
    from aeos.core.parallel_execution.conflict_detector import ConflictDetector
    from aeos.core.parallel_execution.contracts import StepResourceSet
    cd = ConflictDetector()
    steps = [
        StepResourceSet(step_id="a", write_set=["x"]),
        StepResourceSet(step_id="b", read_set=["x"]),
    ]
    conflicts = cd.detect(steps)
    assert any(c.conflict_type == "READ_WRITE" for c in conflicts)
    print("[PASS 14] Conflict detector finds READ_WRITE")


def test_15_evidence_cache_deterministic():
    from aeos.core.evidence_cache.cache_key import EvidenceCacheKeyBuilder
    b = EvidenceCacheKeyBuilder()
    k1 = b.build(aeos_version="1.2.0", config_hash="a", policy_hash="b", permission_hash="c",
                  playbook_id="p", playbook_version="1", skill_versions={}, lcp_versions={},
                  target_path="/t", file_hashes={}, command_inputs={})
    k2 = b.build(aeos_version="1.2.0", config_hash="a", policy_hash="b", permission_hash="c",
                  playbook_id="p", playbook_version="1", skill_versions={}, lcp_versions={},
                  target_path="/t", file_hashes={}, command_inputs={})
    assert k1 == k2
    print("[PASS 15] Evidence cache keys are deterministic")


def test_16_delegation_policy_blocks_unauthorized():
    from aeos.core.agent_runtime.delegation_policy import DelegationPolicyEngine
    engine = DelegationPolicyEngine({"delegation_policy": {"allowed": {"root": {"can_delegate_to": ["architect"]}}}})
    result = engine.can_delegate("root", "tester", {"risk_level": "low"})
    assert not result.get("allowed", False)
    print("[PASS 16] Delegation blocks unauthorized")


def test_17_delegation_policy_blocks_high_risk():
    from aeos.core.agent_runtime.delegation_policy import DelegationPolicyEngine
    engine = DelegationPolicyEngine({"delegation_policy": {"allowed": {"root": {"can_delegate_to": ["tester"]}}}})
    result = engine.can_delegate("root", "tester", {"risk_level": "high"})
    assert not result.get("allowed", False)
    print("[PASS 17] Delegation blocks high risk task")


def test_18_enterprise_judge_blocks_violations():
    from aeos.core.judge.engine import EnterpriseJudgeEngine
    engine = EnterpriseJudgeEngine({"min_score": 9.0})
    result = engine.evaluate({"missing_evidence": True, "hash_mismatch": True, "secret_exposed": True})
    assert result["decision"] == "BLOCKED"
    assert result["final_score"] < 9.0
    print(f"[PASS 18] Enterprise judge blocks violations (score: {result['final_score']})")


def test_19_enterprise_judge_passes_clean():
    from aeos.core.judge.engine import EnterpriseJudgeEngine
    engine = EnterpriseJudgeEngine({"min_score": 9.0})
    result = engine.evaluate({k: False for k in [
        "missing_evidence", "hash_mismatch", "secret_exposed", "tool_router_bypass",
        "policy_bypass", "permission_bypass", "wildcard_approval", "auto_merge_enabled",
        "auto_deploy_enabled", "critical_mcp_enabled_by_default", "pack_import_direct_to_active",
        "package_extract_without_verify", "agent_self_judging", "unsupported_factual_claim",
    ]})
    assert result["decision"] == "PASS"
    print(f"[PASS 19] Enterprise judge passes clean (score: {result['final_score']})")


def test_20_performance_budget_guard():
    from aeos.core.performance.performance_budget import PerformanceBudget, PerformanceBudgetGuard
    budget = PerformanceBudget(name="test", p50_seconds=30, p95_seconds=120)
    guard = PerformanceBudgetGuard()
    assert guard.evaluate(budget, 10)["status"] == "PASS"
    assert guard.evaluate(budget, 60)["status"] == "WARN"
    assert guard.evaluate(budget, 180)["status"] == "BREACHED"
    print("[PASS 20] Performance budget guard works")


def test_21_supply_chain_provenance():
    from aeos.core.supply_chain.provenance import ArtifactProvenance, ProvenanceValidator
    pv = ProvenanceValidator()
    assert pv.validate(ArtifactProvenance(artifact_path="/a", builder="b", source_ref="c", sha256="d"))["status"] == "PASS"
    assert pv.validate(ArtifactProvenance(artifact_path="", builder="", source_ref="", sha256=""))["status"] == "BLOCKED"
    print("[PASS 21] Supply chain provenance validation works")


def test_22_evaluation_runner():
    from aeos.core.evals.evaluation_runner import EvaluationRunner
    from aeos.core.evals.test_suites import ALL_SUITES
    runner = EvaluationRunner(ALL_SUITES)
    result = runner.run_suite("anti_hallucination")
    assert result.get("suite_id") == "anti_hallucination"
    print(f"[PASS 22] Evaluation runner: suite={result['suite_id']} score={result['score']}")


def test_23_profile_resolver():
    from aeos.core.profiles.profile_resolver import ProfileResolver
    resolver = ProfileResolver([{"id": "java", "indicators": ["pom.xml"]}])
    assert resolver.resolve(["pom.xml"]).get("id") == "java"
    print("[PASS 23] Profile resolver matches")


def test_24_profile_resolver_fallback():
    from aeos.core.profiles.profile_resolver import ProfileResolver
    resolver = ProfileResolver([{"id": "go", "indicators": ["go.mod"]}])
    assert resolver.resolve(["unknown.file"]).get("id") == "generic"
    print("[PASS 24] Profile resolver falls back to generic")


def test_25_blueprint_engine():
    from aeos.core.blueprints.blueprint_engine import BlueprintEngine
    with tempfile.TemporaryDirectory() as tmp:
        engine = BlueprintEngine(tmp)
        files = engine.generate_to_sandbox("exe", {"id": "bp", "generated_files": ["a.txt", "b.txt"]})
        assert len(files) == 2
    print("[PASS 25] Blueprint engine generates files")


def test_26_evidence_cache_store():
    from aeos.core.evidence_cache.cache_store import EvidenceCacheStore
    from aeos.core.evidence_cache.cache_key import stable_hash
    with tempfile.TemporaryDirectory() as tmp:
        store = EvidenceCacheStore(tmp)
        key = stable_hash({"test": "v"})
        store.put(key, {"data": "hello"})
        assert store.get(key) is not None
    print("[PASS 26] Evidence cache store/retrieve works")


def test_27_observability_observer():
    from aeos.core.observability.observer import AEOSObserver
    with tempfile.TemporaryDirectory() as tmp:
        obs = AEOSObserver(tmp, "test-obs")
        obs.log_event({"type": "test"})
        obs.write_metric({"token_usage": 100})
        from aeos.core.observability.reporter import ObservabilityReporter
        reporter = ObservabilityReporter(tmp)
        timeline = reporter.generate_timeline("test-obs")
        assert "Timeline" in timeline
        cost = reporter.generate_cost_report("test-obs")
        assert cost["token_usage"] == 100
    print("[PASS 27] Observability observer + reporter work")


def test_28_compliance_audit_exporter():
    from aeos.core.compliance.audit_exporter import AuditExporter
    with tempfile.TemporaryDirectory() as tmp:
        exporter = AuditExporter(tmp)
        path = exporter.export_jsonl("test-exec", [{"event": "test"}])
        assert Path(path).exists()
    print("[PASS 28] Compliance audit exporter works")


def test_29_production_readiness():
    from aeos.core.performance.readiness import ProductionReadinessChecker
    repo_root = Path(__file__).resolve().parent.parent.parent
    checker = ProductionReadinessChecker(repo_root)
    result = checker.check_all()
    assert result.get("total", 0) > 0
    print(f"[PASS 29] Production readiness: {result.get('pass_rate')}% ({result.get('score')}/{result.get('total')}) gates passing")


def test_30_agent_runtime_assigns_when_agent_not_registered():
    from aeos.core.agent_runtime.agent_runtime import AgentRuntime
    from aeos.core.agent_runtime.contracts import TaskDefinition

    class MockRegistry:
        def resolve(self, agent_id):
            return None

    class MockTraceStore:
        def write_event(self, execution_id, event):
            pass
    runtime = AgentRuntime(
        registry=MockRegistry(),
        delegation_policy=None,
        context_router=None,
        trace_store=MockTraceStore(),
        judge_gateway=None,
    )
    task = TaskDefinition(execution_id="t", assigned_agent="unknown", objective="x", scope={}, allowed_skills=[], required_evidence=[])
    result = runtime.assign_task(task)
    assert result.status == "BLOCKED"
    print("[PASS 30] Agent runtime blocks unregistered agent")


def test_31_stdlib_client_rejects_unlisted_mcp():
    from aeos.core.mcp_runtime.stdio_client_real import StdioMCPClient
    try:
        StdioMCPClient(mcp_id="malicious-mcp")
        assert False, "Must raise ValueError for unlisted MCP"
    except ValueError:
        print("[PASS 31] Stdio client rejects unlisted MCP")


def test_32_mcp_runtime_blocks_disabled():
    from aeos.core.mcp_runtime.runtime import MCPRuntime
    from aeos.core.mcp_runtime.registry import MCPRegistry
    with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False, encoding="utf-8") as f:
        f.write("mcps:\n  - id: test\n    type: mock\n    transport: stdio\n    config: ''\n    risk_level: critical\n    tools: []\n    capabilities: []\n    enabled: false\n")
        f.flush()
        reg = MCPRegistry(f.name)
        reg.load()
        runtime = MCPRuntime(reg)
        h = runtime.health("test")
        assert h.state == "STOPPED"
    print("[PASS 32] MCP runtime reports STOPPED for disabled MCP")


if __name__ == "__main__":
    tests = [
        test_01_tool_router_module_loads,
        test_02_mcp_runtime_module_loads,
        test_03_mcp_registry_returns_none_for_unknown,
        test_04_evidence_store_integrity,
        test_05_redactor_detects_aws_key,
        test_06_redactor_detects_jwt,
        test_07_approval_rejects_expired,
        test_08_approval_rejects_wildcard_scope,
        test_09_approval_rejects_empty_reason,
        test_10_pack_marketplace_blocks_direct_active,
        test_11_pack_marketplace_allows_quarantine_to_staging,
        test_12_pack_marketplace_allows_staging_to_active,
        test_13_conflict_detector_write_write,
        test_14_conflict_detector_read_write,
        test_15_evidence_cache_deterministic,
        test_16_delegation_policy_blocks_unauthorized,
        test_17_delegation_policy_blocks_high_risk,
        test_18_enterprise_judge_blocks_violations,
        test_19_enterprise_judge_passes_clean,
        test_20_performance_budget_guard,
        test_21_supply_chain_provenance,
        test_22_evaluation_runner,
        test_23_profile_resolver,
        test_24_profile_resolver_fallback,
        test_25_blueprint_engine,
        test_26_evidence_cache_store,
        test_27_observability_observer,
        test_28_compliance_audit_exporter,
        test_29_production_readiness,
        test_30_agent_runtime_assigns_when_agent_not_registered,
        test_31_stdlib_client_rejects_unlisted_mcp,
        test_32_mcp_runtime_blocks_disabled,
    ]