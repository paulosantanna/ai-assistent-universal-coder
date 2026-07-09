from __future__ import annotations

import json
from pathlib import Path

import pytest

from aeos.core.readiness.readiness_auditor import ReadinessAuditor
from aeos.core.readiness.production_gate import ProductionGate
from aeos.core.readiness.readiness_models import (
    READINESS_PASS, READINESS_BLOCKED,
)
from aeos.core.evidence.evidence_manifest import (
    StagedManifestBuilder,
    verify_staged_manifest,
    STAGE_FILENAMES,
)


@pytest.fixture
def workspace(tmp_path) -> Path:
    ws = tmp_path / "workspace"
    ws.mkdir(parents=True, exist_ok=True)
    (ws / "aeos" / "core").mkdir(parents=True, exist_ok=True)
    (ws / "aeos" / "config").mkdir(parents=True, exist_ok=True)
    (ws / ".aeos" / "evidence").mkdir(parents=True, exist_ok=True)
    (ws / ".aeos" / "reports").mkdir(parents=True, exist_ok=True)
    (ws / "aeos" / "tests").mkdir(parents=True, exist_ok=True)
    (ws / "aeos" / "evals").mkdir(parents=True, exist_ok=True)
    return ws


def create_module(ws: Path, *parts: str):
    fp = ws.joinpath(*parts)
    fp.parent.mkdir(parents=True, exist_ok=True)
    fp.write_text("# module")
    return fp


def make_judge_result(ws: Path, exec_id: str, status: str = "PASS", score: float = 1.0):
    evidence_dir = ws / ".aeos" / "evidence" / exec_id
    evidence_dir.mkdir(parents=True, exist_ok=True)
    fp = evidence_dir / "judge-result.json"
    fp.write_text(json.dumps({"execution_id": exec_id, "status": status, "score": score, "blocking_rules": []}))
    return fp


def make_runtime_result(ws: Path, exec_id: str, status: str = "PASS"):
    evidence_dir = ws / ".aeos" / "evidence" / exec_id
    evidence_dir.mkdir(parents=True, exist_ok=True)
    fp = evidence_dir / "runtime_result.jsonl"
    fp.write_text(json.dumps({"execution_id": exec_id, "status": status}) + "\n")
    return fp


def make_eval_scorecard(ws: Path, exec_id: str, score: float = 1.0):
    evidence_dir = ws / ".aeos" / "evidence" / exec_id
    evidence_dir.mkdir(parents=True, exist_ok=True)
    fp = evidence_dir / "eval-scorecard.json"
    fp.write_text(json.dumps({
        "execution_id": exec_id, "overall_score": score,
        "total_cases": 10, "passed": int(10 * score), "failed": 0,
        "errors": 0, "skipped": 0, "blocking_failures": [], "suites": {},
    }))
    return fp


def make_manifest(ws: Path, exec_id: str, manifest_name: str = "evidence-manifest.json"):
    evidence_dir = ws / ".aeos" / "evidence" / exec_id
    evidence_dir.mkdir(parents=True, exist_ok=True)
    test_file = evidence_dir / "dummy.jsonl"
    test_file.write_text('{"test":true}\n')

    builder = StagedManifestBuilder(exec_id, str(evidence_dir))
    if manifest_name == STAGE_FILENAMES["runtime"]:
        builder.finalize_runtime_manifest()
    elif manifest_name == STAGE_FILENAMES["eval"]:
        builder.finalize_eval_manifest()
    elif manifest_name == STAGE_FILENAMES["judge"]:
        builder.finalize_judge_manifest()
    elif manifest_name == STAGE_FILENAMES["readiness"]:
        builder.finalize_readiness_manifest()
    elif manifest_name == STAGE_FILENAMES["final"]:
        builder.finalize_runtime_manifest()
        if (evidence_dir / "eval-scorecard.json").exists():
            builder.finalize_eval_manifest()
        if (evidence_dir / "judge-result.json").exists():
            builder.finalize_judge_manifest()
        builder.finalize_readiness_manifest()
        builder.finalize_evidence_manifest()

    return evidence_dir / manifest_name


def test_readiness_blocks_when_final_manifest_invalid(workspace):
    """Readiness must BLOCKED when the final evidence-manifest.json has hash mismatch."""
    create_module(workspace, "aeos", "core", "runtime", "runtime_orchestrator.py")
    create_module(workspace, "aeos", "core", "judge", "judge_engine.py")
    create_module(workspace, "aeos", "core", "evals", "eval_runner.py")
    create_module(workspace, "aeos", "core", "readiness", "readiness_auditor.py")
    create_module(workspace, "aeos", "core", "skill_engine", "skill_executor.py")
    create_module(workspace, "aeos", "core", "playbook_engine", "playbook_executor.py")
    create_module(workspace, "aeos", "core", "agent_runtime", "agent_runtime.py")
    create_module(workspace, "aeos", "core", "tool_router", "router.py")
    create_module(workspace, "aeos", "core", "governance", "governance_gate.py")
    create_module(workspace, "aeos", "core", "evidence", "evidence_store.py")
    create_module(workspace, "aeos", "core", "mcp_runtime", "mcp_registry_resolver.py")
    create_module(workspace, "aeos", "core", "permissions", "permission_engine.py")
    create_module(workspace, "aeos", "core", "policy", "policy_engine.py")
    create_module(workspace, "aeos", "config", "permissions.yaml")
    create_module(workspace, "aeos", "config", "policies.yaml")
    create_module(workspace, "aeos", "config", "aeos.config.yaml")
    create_module(workspace, "aeos", "config", "tool-router.config.yaml")
    create_module(workspace, "aeos", "config", "mcp-tools.allowlist.yaml")
    create_module(workspace, "aeos", "config", "security-hardening.config.yaml")
    create_module(workspace, "aeos", "config", "enterprise-security.config.yaml")
    create_module(workspace, "aeos", "config", "production-enterprise.config.yaml")
    create_module(workspace, "aeos", "config", "v1-release-gates.yaml")
    create_module(workspace, "aeos", "config", "enterprise-ci-gates.yaml")
    create_module(workspace, "aeos", "config", "observability.config.yaml")
    create_module(workspace, "aeos", "config", "performance-budgets.yaml")
    create_module(workspace, "aeos", "core", "observability", "__init__.py")
    create_module(workspace, "aeos", "core", "performance", "__init__.py")
    create_module(workspace, "aeos", "evals", "suite.yaml")
    create_module(workspace, "aeos", "tests", "judge", "test_judge.py")
    create_module(workspace, "aeos", "tests", "evals", "test_eval.py")
    create_module(workspace, "aeos", "tests", "readiness", "test_readiness.py")
    create_module(workspace, "aeos", "tests", "runtime", "test_runtime.py")

    exec_id = "test-readiness-blocked-manifest-001"
    make_judge_result(workspace, exec_id, "PASS", 1.0)
    make_runtime_result(workspace, exec_id, "PASS")
    make_eval_scorecard(workspace, exec_id, 0.95)
    make_manifest(workspace, exec_id, STAGE_FILENAMES["runtime"])
    make_manifest(workspace, exec_id, STAGE_FILENAMES["judge"])
    make_manifest(workspace, exec_id, STAGE_FILENAMES["eval"])
    make_manifest(workspace, exec_id, STAGE_FILENAMES["readiness"])
    make_manifest(workspace, exec_id, STAGE_FILENAMES["final"])

    final_fp = workspace / ".aeos" / "evidence" / exec_id / STAGE_FILENAMES["final"]
    with open(final_fp, "r") as f:
        manifest = json.load(f)
    for fe in manifest.get("files", []):
        fpath = workspace / ".aeos" / "evidence" / exec_id / fe["path"]
        if fpath.exists():
            original = fpath.read_text()
            fpath.write_text(original + "\nTAMPERED")
            break

    auditor = ReadinessAuditor(str(workspace))
    result = auditor.audit()
    has_manifest_error = any("manifest" in b.lower() for b in result.critical_blockers)
    assert has_manifest_error or result.status == READINESS_BLOCKED, \
        "Readiness should be BLOCKED when staged manifest verification fails"


def test_readiness_passes_with_valid_staged_manifests(workspace):
    """Readiness must accept execution with all valid staged manifests."""
    create_module(workspace, "aeos", "core", "runtime", "runtime_orchestrator.py")
    create_module(workspace, "aeos", "core", "judge", "judge_engine.py")
    create_module(workspace, "aeos", "core", "judge", "deterministic_judge.py")
    create_module(workspace, "aeos", "core", "judge", "judge_models.py")
    create_module(workspace, "aeos", "core", "judge", "judge_blocking_rules.py")
    create_module(workspace, "aeos", "core", "judge", "judge_input_builder.py")
    create_module(workspace, "aeos", "core", "judge", "judge_scorecard.py")
    create_module(workspace, "aeos", "core", "judge", "judge_reporter.py")
    create_module(workspace, "aeos", "core", "evals", "eval_runner.py")
    create_module(workspace, "aeos", "core", "evals", "eval_suite_loader.py")
    create_module(workspace, "aeos", "core", "evals", "eval_models.py")
    create_module(workspace, "aeos", "core", "evals", "eval_scorecard.py")
    create_module(workspace, "aeos", "core", "readiness", "readiness_auditor.py")
    create_module(workspace, "aeos", "core", "readiness", "readiness_scorecard.py")
    create_module(workspace, "aeos", "core", "readiness", "readiness_reporter.py")
    create_module(workspace, "aeos", "core", "skill_engine", "skill_executor.py")
    create_module(workspace, "aeos", "core", "playbook_engine", "playbook_executor.py")
    create_module(workspace, "aeos", "core", "agent_runtime", "agent_runtime.py")
    create_module(workspace, "aeos", "core", "tool_router", "router.py")
    create_module(workspace, "aeos", "core", "tool_router", "tool_models.py")
    create_module(workspace, "aeos", "core", "governance", "governance_gate.py")
    create_module(workspace, "aeos", "core", "evidence", "evidence_store.py")
    create_module(workspace, "aeos", "core", "evidence", "evidence_reporter.py")
    create_module(workspace, "aeos", "core", "mcp_runtime", "mcp_registry_resolver.py")
    create_module(workspace, "aeos", "core", "permissions", "permission_engine.py")
    create_module(workspace, "aeos", "core", "policy", "policy_engine.py")
    create_module(workspace, "aeos", "config", "permissions.yaml")
    create_module(workspace, "aeos", "config", "policies.yaml")
    create_module(workspace, "aeos", "config", "aeos.config.yaml")
    create_module(workspace, "aeos", "config", "tool-router.config.yaml")
    create_module(workspace, "aeos", "config", "mcp-tools.allowlist.yaml")
    create_module(workspace, "aeos", "config", "security-hardening.config.yaml")
    create_module(workspace, "aeos", "config", "enterprise-security.config.yaml")
    create_module(workspace, "aeos", "config", "production-enterprise.config.yaml")
    create_module(workspace, "aeos", "config", "v1-release-gates.yaml")
    create_module(workspace, "aeos", "config", "enterprise-ci-gates.yaml")
    create_module(workspace, "aeos", "config", "observability.config.yaml")
    create_module(workspace, "aeos", "config", "performance-budgets.yaml")
    create_module(workspace, "aeos", "core", "observability", "__init__.py")
    create_module(workspace, "aeos", "core", "performance", "__init__.py")
    create_module(workspace, "aeos", "evals", "suite.yaml")
    create_module(workspace, "aeos", "tests", "judge", "test_judge.py")
    create_module(workspace, "aeos", "tests", "evals", "test_eval.py")
    create_module(workspace, "aeos", "tests", "readiness", "test_readiness.py")
    create_module(workspace, "aeos", "tests", "runtime", "test_runtime.py")

    exec_id = "test-readiness-pass-001"
    make_judge_result(workspace, exec_id, "PASS", 1.0)
    make_runtime_result(workspace, exec_id, "PASS")
    make_eval_scorecard(workspace, exec_id, 0.95)
    make_manifest(workspace, exec_id, STAGE_FILENAMES["runtime"])
    make_manifest(workspace, exec_id, STAGE_FILENAMES["judge"])
    make_manifest(workspace, exec_id, STAGE_FILENAMES["eval"])
    make_manifest(workspace, exec_id, STAGE_FILENAMES["readiness"])
    make_manifest(workspace, exec_id, STAGE_FILENAMES["final"])

    auditor = ReadinessAuditor(str(workspace))
    result = auditor.audit()
    assert result.status == READINESS_PASS or len(result.critical_blockers) == 0, \
        f"Readiness should be PASS with valid manifests: {result.status}, blockers={result.critical_blockers}"


def test_readiness_blocks_without_staged_manifests(workspace):
    """Readiness should BLOCK when staged manifests are missing."""
    create_module(workspace, "aeos", "core", "runtime", "runtime_orchestrator.py")
    create_module(workspace, "aeos", "core", "judge", "judge_engine.py")
    create_module(workspace, "aeos", "core", "evals", "eval_runner.py")
    create_module(workspace, "aeos", "core", "readiness", "readiness_auditor.py")
    create_module(workspace, "aeos", "core", "skill_engine", "skill_executor.py")
    create_module(workspace, "aeos", "core", "playbook_engine", "playbook_executor.py")
    create_module(workspace, "aeos", "core", "agent_runtime", "agent_runtime.py")
    create_module(workspace, "aeos", "core", "tool_router", "router.py")
    create_module(workspace, "aeos", "core", "governance", "governance_gate.py")
    create_module(workspace, "aeos", "core", "evidence", "evidence_store.py")
    create_module(workspace, "aeos", "core", "mcp_runtime", "mcp_registry_resolver.py")
    create_module(workspace, "aeos", "core", "permissions", "permission_engine.py")
    create_module(workspace, "aeos", "core", "policy", "policy_engine.py")
    create_module(workspace, "aeos", "config", "permissions.yaml")
    create_module(workspace, "aeos", "config", "policies.yaml")
    create_module(workspace, "aeos", "config", "aeos.config.yaml")
    create_module(workspace, "aeos", "config", "tool-router.config.yaml")
    create_module(workspace, "aeos", "config", "mcp-tools.allowlist.yaml")
    create_module(workspace, "aeos", "config", "security-hardening.config.yaml")
    create_module(workspace, "aeos", "config", "enterprise-security.config.yaml")
    create_module(workspace, "aeos", "config", "production-enterprise.config.yaml")
    create_module(workspace, "aeos", "config", "v1-release-gates.yaml")
    create_module(workspace, "aeos", "config", "enterprise-ci-gates.yaml")
    create_module(workspace, "aeos", "config", "observability.config.yaml")
    create_module(workspace, "aeos", "config", "performance-budgets.yaml")
    create_module(workspace, "aeos", "core", "observability", "__init__.py")
    create_module(workspace, "aeos", "core", "performance", "__init__.py")
    create_module(workspace, "aeos", "evals", "suite.yaml")
    create_module(workspace, "aeos", "tests", "judge", "test_judge.py")
    create_module(workspace, "aeos", "tests", "evals", "test_eval.py")
    create_module(workspace, "aeos", "tests", "readiness", "test_readiness.py")
    create_module(workspace, "aeos", "tests", "runtime", "test_runtime.py")

    exec_id = "test-readiness-nomanifest-001"
    make_judge_result(workspace, exec_id, "PASS", 1.0)
    make_runtime_result(workspace, exec_id, "PASS")
    make_eval_scorecard(workspace, exec_id, 1.0)

    auditor = ReadinessAuditor(str(workspace))
    result = auditor.audit()
    assert result.status == READINESS_BLOCKED, \
        "Readiness should be BLOCKED when staged manifests are completely missing"
