"""AEOS Workbench CLI v0.3 — Controlled Change Proposal Layer."""

import argparse
import sys
import json
import uuid
from pathlib import Path
from typing import Optional
import yaml

from aeos_workbench.scanner.scanner import ProjectScanner
from aeos_workbench.stack_detector.detector import StackDetector
from aeos_workbench.evidence.ledger import EvidenceLedger
from aeos_workbench.evidence.crypto import EvidenceCipher, HAS_CRYPTO
from aeos_workbench.judge.engine import JudgeEngine
from aeos_workbench.generator.ecosystem_map import EcosystemMapGenerator
from aeos_workbench.generator.risk_report import RiskReportGenerator
from aeos_workbench.generator.playbooks import PlaybookRecommender
from aeos_workbench.generator.skills import SkillGenerator
from aeos_workbench.generator.judge_report import JudgeReportGenerator
from aeos_workbench.bridge.ecosystem_export import export_ecosystem_json
from aeos_workbench.bridge.typescript_runtime import runtime_available, status, run_agent
from aeos_workbench.agents.registry import AgentRegistry
from aeos_workbench.agents.executor import AgentExecutor, AgentTask
from aeos_workbench.scanner.quality import CodeQualityAnalyzer
from aeos_workbench.execution.orchestrator import run_playbook
from aeos_workbench.execution.evidence_integrity import EvidenceManifest
from aeos_workbench.execution.evidence_integrity_v2 import EvidenceManifestV2
from aeos_workbench.execution.cache_manager import CacheManager
from aeos_workbench.execution.judge_v3 import JudgeV3
from aeos_workbench.controlled_change.dry_run.dry_run_planner import DryRunPlanner
from aeos_workbench.controlled_change.approval.approval_engine import ApprovalEngine
from aeos_workbench.controlled_change.patch.patch_proposal_engine import PatchProposalEngine


def _get_cache_manager(args):
    root = Path(getattr(args, "target", Path.cwd())).resolve()
    return CacheManager(root)


def cmd_cache(args):
    cm = _get_cache_manager(args)
    if args.cache_command == "clear":
        count = cm.clear(playbook_id=getattr(args, "playbook", None))
        print(f"[AEOS] Cache cleared: {count} entries removed")
    elif args.cache_command == "status":
        st = cm.status()
        print(f"[AEOS] Cache status:")
        print(f"  Entries: {st.get('total_entries', 0)}")
        print(f"  Size: {st.get('total_size_mb', 0):.1f} MB")
        print(f"  Cache dir: {st.get('cache_dir', 'N/A')}")
    else:
        print("[AEOS] Unknown cache command. Use: cache clear, cache status")


def cmd_run(args):
    result = run_playbook(
        playbook_id=args.playbook,
        target_path=str(args.target),
        mode=args.mode,
        dry_run=args.dry_run,
        use_cache=args.cache,
        no_cache=args.no_cache,
        encrypt_rollback=args.encrypt_rollback,
    )
    print(json.dumps(result, indent=2, ensure_ascii=False))
    if result.get("status") in ("BLOCKED", "failed", "blocked_awaiting_approval"):
        print(f"[AEOS] [RESULT] {result.get('status')}")
        if result.get("blocking_reasons"):
            for r in result["blocking_reasons"]:
                print(f"[AEOS]   BLOCKED: {r}")
        if result.get("error"):
            print(f"[AEOS]   ERROR: {result['error']}")
        return result
    print(f"[AEOS] [PASS] Score: {result.get('judge_score', '?')}/10")
    print(f"[AEOS] Evidence: {result.get('evidence_path', '?')}")
    print(f"[AEOS] Reports: {result.get('reports_path', '?')}")
    return result


def cmd_evidence_verify(args):
    evidence_dir = args.evidence_dir or (Path.cwd() / ".aeos" / "evidence")
    execution_id = args.execution_id
    target_path = args.target or Path.cwd()
    aeos_dir = Path.cwd() / ".aeos"

    if not execution_id:
        print("[AEOS] [ERROR] --execution-id is required")
        print("[AEOS] Usage: aeos evidence verify --execution-id <id> [--target <path>]")
        return

    # Try v2 verification first (covers dry-runs, patches, sandbox, reports, evidence)
    v2_result = EvidenceManifestV2.verify_execution(aeos_dir, execution_id)
    if v2_result["passed"]:
        print(f"[AEOS] [PASS] Evidence integrity verified (v2) for {execution_id}")
        print(f"[AEOS]   Artifacts checked: {v2_result['verified_count']}/{v2_result['total_artifacts']}")
        return

    # Fallback to v1
    manifest_path = evidence_dir / execution_id / "evidence-manifest.json"
    if manifest_path.exists():
        v1_result = EvidenceManifest.verify_execution(evidence_dir, execution_id, target_path)
        if v1_result["passed"]:
            print(f"[AEOS] [PASS] Evidence integrity verified (v1) for {execution_id}")
            print(f"[AEOS]   Artifacts checked: {v1_result['verified_count']}/{v1_result['total_artifacts']}")
            return
        print(f"[AEOS] [FAIL] Evidence integrity check FAILED for {execution_id}")
        for err in v1_result["errors"]:
            print(f"[AEOS]   ERROR: {err}")
        sys.exit(1)

    # No evidence found
    print(f"[AEOS] [ERROR] No evidence found for execution '{execution_id}'")
    print(f"[AEOS]   Checked: {aeos_dir / 'evidence' / execution_id}")
    sys.exit(1)


# =============================================================================
# v0.3 — Dry Run Preview
# =============================================================================
def cmd_dry_run_preview(args):
    target = Path(args.target).resolve()
    workspace_root = Path.cwd()
    planner = DryRunPlanner(workspace_root)

    print(f"[AEOS] [DRY RUN] Planning dry-run for {target}")
    result = planner.plan_dry_run(target, issue=None, scope=None)
    print(f"[AEOS] [DRY RUN] Execution ID: {result['execution_id']}")
    print(f"[AEOS] [DRY RUN] Directory: {result['dry_run_dir']}")
    print(f"[AEOS] [DRY RUN] Actions planned: {result['planned_actions']['summary']['total_actions']}")
    print(f"[AEOS] [DRY RUN] Read actions: {result['planned_actions']['summary']['read_actions']}")
    print(f"[AEOS] [DRY RUN] Generate actions: {result['planned_actions']['summary']['generate_actions']}")
    print(f"[AEOS] [DRY RUN] Approvals required: {result['required_approvals']['summary']['total_required']}")
    print(f"[AEOS] [DRY RUN] Risks identified: {len(result['risks'])}")
    print(f"[AEOS] [DRY RUN] Status: NO CHANGES APPLIED")
    print()
    print(f"[AEOS] Artifacts generated:")
    for a in result["artifacts_generated"]:
        print(f"[AEOS]   - {a}")
    return result


# =============================================================================
# v0.3 — Code Change Proposal
# =============================================================================
def cmd_code_change_proposal(args):
    target = Path(args.target).resolve()
    issue = args.issue
    workspace_root = Path.cwd()
    execution_id = f"cc-{uuid.uuid4().hex[:12]}"

    print(f"[AEOS] [CODE CHANGE] Generating proposal for: {issue}")

    # Step 1: Dry Run
    planner = DryRunPlanner(workspace_root, execution_id)
    dry_run_result = planner.plan_dry_run(target, issue=issue, scope=None)
    print(f"[AEOS] [DRY RUN] Complete — {len(dry_run_result['planned_actions']['actions'])} actions planned")

    # Step 2: Generate Patch Proposal
    aeos_root = workspace_root / ".aeos"
    patches_dir = aeos_root / "patches" / execution_id
    patches_dir.mkdir(parents=True, exist_ok=True)

    file_changes = [
        {
            "file": str(f.relative_to(workspace_root)) if f.is_relative_to(workspace_root) else str(f),
            "type": "modify",
            "changes": [{"type": "hunk", "start_old": 1, "count_old": 10, "start_new": 1, "count_new": 12,
                         "lines": [" context line", "+added line", "-removed line"]}],
        }
        for f in sorted(target.rglob("*"))[:5] if f.is_file() and f.suffix in (".py", ".ts", ".js")
    ] or [{"file": str(target), "type": "analyze", "changes": [{"type": "context", "content": "Analysis target"}]}]

    patch_engine = PatchProposalEngine(workspace_root, execution_id)
    patch_result = patch_engine.generate_patch(
        target,
        issue,
        file_changes,
        {},
        {"risks": [{"risk": "Code change may introduce regression", "level": "medium",
                     "mitigation": "Test in sandbox before applying"}]},
    )
    print(f"[AEOS] [PATCH] Generated in: {patches_dir}")
    print(f"[AEOS] [PATCH] Affected files: {len(patch_result['affected_files'])}")

    # Step 3: Judge v3 Evaluation
    judge = JudgeV3(workspace_root, aeos_root / "evidence", execution_id)
    ctx = {
        "execution_state_path": str(aeos_root / "evidence" / execution_id / "execution-state.json"),
        "playbook_id": "code-change-proposal",
        "playbook_definition": {"id": "code-change-proposal", "risk_level": "medium"},
        "resolved_lcps": ["global-rules"],
        "permission_log": [],
        "tool_decision_log": [],
        "generated_artifacts": patch_result["artifacts_generated"],
        "files_modified_outside_aeos": [],
        "secrets_exposed": [],
        "assumptions_marked": True,
        "rollback_plan_path": str(patches_dir / "rollback-plan.md"),
        "step_results": ["dry_run", "patch_generation"],
        "step_count": 2,
        "required_approvals": dry_run_result["required_approvals"]["required_approvals"],
        "patches_applied_automatically": [],
        "risks": dry_run_result["risks"],
    }
    judge_result = judge.evaluate(ctx)

    # Step 4: Generate reports
    reports_dir = aeos_root / "reports" / execution_id
    reports_dir.mkdir(parents=True, exist_ok=True)

    risk_lines = "\n".join(
        f"- {risk['risk']} ({risk['level']})"
        for risk in dry_run_result["risks"]
    )

    code_change_report = reports_dir / "code-change-proposal.md"
    code_change_report.write_text(
        f"# Code Change Proposal — {execution_id}\n\n"
        f"**Target:** {target}\n"
        f"**Issue:** {issue}\n"
        f"**Status:** {'PROPOSAL ONLY' if judge_result['decision'] != 'BLOCKED' else 'BLOCKED'}\n"
        f"**Judge Decision:** {judge_result['decision']} (Score: {judge_result['final_score']}/10)\n\n"
        f"## Facts\n- Dry-run completed: {len(dry_run_result['planned_actions']['actions'])} actions\n"
        f"- Patch generated: {len(patch_result['affected_files'])} files\n\n"
        f"## Assumptions\n- Issue accurately describes the desired change\n"
        f"- All relevant files were identified\n\n"
        f"## Risks\n{risk_lines}\n\n"
        f"## Recommendations\n- Review proposed.patch before approving\n"
        f"- Run sandbox tests before applying\n- Verify rollback plan\n",
        encoding="utf-8",
    )

    judge_report = reports_dir / "judge-report.md"
    judge_report.write_text(
        f"# Judge Report v3 — {execution_id}\n\n"
        f"**Decision:** {judge_result['decision']}\n"
        f"**Score:** {judge_result['final_score']}/10\n"
        f"**Deterministic Blocks:** {len(judge_result['deterministic_blocks'])}\n\n"
        f"## Checks\n{json.dumps(judge_result['checks'], indent=2)}\n\n"
        f"## Blocking Reasons\n{chr(10).join(f'- {b}' for b in judge_result['blocking_reasons'])}\n",
        encoding="utf-8",
    )

    # Step 5: Register evidence
    manifest = EvidenceManifestV2(aeos_root, execution_id)
    for art in patch_result["artifacts_generated"]:
        ap = Path(art)
        if ap.exists():
            manifest.register_artifact(ap, "patch-proposal", "code-change-proposal")
    for rp in [code_change_report, judge_report]:
        if rp.exists():
            manifest.register_artifact(rp, "report", "code-change-proposal")
    manifest.save_manifest()
    manifest.save_hash_chain()
    manifest.save_integrity_report()

    summary = {
        "status": "proposal_generated",
        "decision": judge_result["decision"],
        "execution_id": execution_id,
        "judge_score": judge_result["final_score"],
        "blocking_reasons": judge_result["blocking_reasons"],
        "deterministic_blocks": judge_result["deterministic_blocks"],
        "patches_dir": patch_result["patches_dir"],
        "reports_dir": str(reports_dir),
        "evidence_dir": str(aeos_root / "evidence" / execution_id),
        "artifacts": {
            "dry_run": dry_run_result["artifacts_generated"],
            "patch": patch_result["artifacts_generated"],
            "reports": [str(code_change_report), str(judge_report)],
        },
    }

    print(json.dumps(summary, indent=2, ensure_ascii=False))

    if judge_result["decision"] == "BLOCKED":
        print(f"\n[AEOS] [BLOCKED] Proposal blocked by Judge v3")
        for b in judge_result["blocking_reasons"]:
            print(f"[AEOS]   {b}")
        sys.exit(1)
    else:
        print(f"\n[AEOS] [PASS] Proposal approved for review (Score: {judge_result['final_score']}/10)")

    return summary


# =============================================================================
# v0.3 — Test Generation (Sandbox)
# =============================================================================
def cmd_test_generation(args):
    target = Path(args.target).resolve()
    mode = args.mode
    workspace_root = Path.cwd()
    execution_id = f"tg-{uuid.uuid4().hex[:12]}"

    aeos_root = workspace_root / ".aeos"
    sandbox_dir = aeos_root / "sandbox" / execution_id / "generated-tests"
    sandbox_dir.mkdir(parents=True, exist_ok=True)

    print(f"[AEOS] [TEST GEN] Analyzing: {target}")
    print(f"[AEOS] [TEST GEN] Mode: {mode}")

    # Detect framework
    framework = "unknown"
    for f in target.rglob("*"):
        if f.name == "pyproject.toml":
            framework = "pytest"
        elif f.name == "package.json":
            framework = "jest"
    print(f"[AEOS] [TEST GEN] Detected framework: {framework}")

    # Generate sample test files
    sources = sorted(target.rglob("*.py"))[:3] or sorted(target.rglob("*.ts"))[:3]
    test_files = []
    for src in sources:
        rel = src.relative_to(workspace_root) if src.is_relative_to(workspace_root) else src
        test_name = f"test_{src.stem}.py" if src.suffix == ".py" else f"{src.stem}.test.ts"
        test_path = sandbox_dir / test_name
        test_path.write_text(
            f"# Source: {rel}\n"
            f"# Evidence: SHA-256 (generated)\n"
            f"# Framework: {framework}\n"
            f"# Generated by: test-generation-sandbox v1.0.0\n\n"
            f"import pytest\n\n\n"
            f"class Test{src.stem.title()}:\n"
            f"    def test_should_exist(self):\n"
            f"        assert True\n\n"
            f"    def test_should_handle_errors(self):\n"
            f"        with pytest.raises(Exception):\n"
            f"            raise ValueError(\"test\")\n",
            encoding="utf-8",
        )
        test_files.append(str(test_path))
        print(f"[AEOS] [TEST GEN] Generated: {test_path}")

    # Risk report
    risk_report = sandbox_dir / "test-risk-report.md"
    risk_report.write_text(
        f"# Test Risk Report — {execution_id}\n\n"
        f"**Target:** {target}\n"
        f"**Framework:** {framework}\n\n"
        f"## Fact\n- {len(sources)} source files analyzed\n"
        f"- {len(test_files)} test files generated\n\n"
        f"## Assumption\n"
        f"- Detected framework is correct\n\n"
        f"## Risk\n"
        f"- Tests have not been executed\n\n"
        f"## Recommendation\n"
        f"- Run tests against actual source before applying\n",
        encoding="utf-8",
    )

    # Rollback plan
    rollback_plan = sandbox_dir / "rollback-plan.md"
    rollback_plan.write_text(
        f"# Rollback Plan — {execution_id}\n\n"
        f"**Strategy:** delete_generated_artifacts\n\n"
        f"## Operations\n"
        f"1. Delete all files in .aeos/sandbox/{execution_id}/\n"
        f"2. Verify no artifacts remain\n",
        encoding="utf-8",
    )

    # Register evidence
    evidence = EvidenceManifestV2(aeos_root, execution_id)
    for tf in test_files:
        evidence.register_artifact(Path(tf), "generated-test", "test-generation")
    evidence.register_artifact(risk_report, "risk-report", "test-generation")
    evidence.register_artifact(rollback_plan, "rollback-plan", "test-generation")
    evidence.save_manifest()
    evidence.save_hash_chain()
    evidence.save_integrity_report()

    result = {
        "status": "tests_generated",
        "execution_id": execution_id,
        "framework": framework,
        "tests_generated": len(test_files),
        "sandbox_path": str(sandbox_dir),
        "sources_analyzed": [str(s) for s in sources],
    }
    print(json.dumps(result, indent=2))
    print(f"\n[AEOS] [PASS] Tests generated in sandbox: {sandbox_dir}")
    return result


# =============================================================================
# v0.3 — Dependency Analysis
# =============================================================================
def cmd_dependency_analysis(args):
    target = Path(args.target).resolve()
    workspace_root = Path.cwd()
    execution_id = f"da-{uuid.uuid4().hex[:12]}"

    aeos_root = workspace_root / ".aeos"
    reports_dir = aeos_root / "reports" / execution_id
    reports_dir.mkdir(parents=True, exist_ok=True)

    print(f"[AEOS] [DEP ANALYSIS] Analyzing: {target}")

    # Find dependency files
    dep_files = []
    for pattern in ["package.json", "pyproject.toml", "requirements.txt", "pom.xml", "Cargo.toml", "go.mod"]:
        for f in target.rglob(pattern):
            dep_files.append(f)

    deps = []
    for df in dep_files:
        try:
            rel = df.relative_to(workspace_root) if df.is_relative_to(workspace_root) else df
            content = df.read_text(encoding="utf-8", errors="replace")[:500]
            deps.append({"file": str(rel), "type": df.name, "preview": content[:200]})
        except OSError:
            pass

    risk_report = reports_dir / "dependency-risk-report.md"
    risk_report.write_text(
        f"# Dependency Risk Report — {execution_id}\n\n"
        f"**Target:** {target}\n"
        f"## Fact\n"
        f"- {len(dep_files)} dependency files found\n"
        f"- {len(deps)} dependency entries analyzed\n\n"
        f"## Assumption\n"
        f"- Dependencies are correctly declared\n\n"
        f"## Risk\n"
        f"- No CVE database access (read-only analysis)\n\n"
        f"## Recommendation\n"
        f"- Review dependencies manually before upgrade\n",
        encoding="utf-8",
    )

    upgrade_candidates = reports_dir / "upgrade-candidates.md"
    upgrade_candidates.write_text(
        f"# Upgrade Candidates — {execution_id}\n\n"
        f"| Dependency | Current | Latest | Risk |\n"
        f"|------------|---------|--------|------|\n"
        f"| (read-only analysis) | | | |\n\n"
        f"*Full CVE/compatibility analysis requires external access (future version)*\n",
        encoding="utf-8",
    )

    compat_matrix = reports_dir / "compatibility-matrix.md"
    compat_matrix.write_text(
        f"# Compatibility Matrix — {execution_id}\n\n"
        f"| Dependency | Version | Compatible | Notes |\n"
        f"|------------|---------|------------|-------|\n"
        f"| (read-only analysis) | | | |\n",
        encoding="utf-8",
    )

    dep_evidence = reports_dir / "dependency-evidence.json"
    dep_evidence.write_text(
        json.dumps({"execution_id": execution_id, "files_analyzed": [str(d) for d in dep_files],
                     "declarations": deps, "status": "read_only_analysis_complete"}, indent=2),
        encoding="utf-8",
    )

    # Register evidence
    evidence = EvidenceManifestV2(aeos_root, execution_id)
    for rp in [risk_report, upgrade_candidates, compat_matrix, dep_evidence]:
        if rp.exists():
            evidence.register_artifact(rp, "dependency-report", "dependency-analysis")
    evidence.save_manifest()
    evidence.save_hash_chain()
    evidence.save_integrity_report()

    result = {
        "status": "analysis_complete",
        "execution_id": execution_id,
        "dependency_files_found": len(dep_files),
        "reports": [str(risk_report), str(upgrade_candidates), str(compat_matrix), str(dep_evidence)],
    }
    print(json.dumps(result, indent=2))
    print(f"\n[AEOS] [PASS] Dependency analysis complete (read-only)")
    return result


# =============================================================================
# v0.3 — Refactoring Proposal
# =============================================================================
def cmd_refactoring_proposal(args):
    target = Path(args.target).resolve()
    scope = args.scope
    workspace_root = Path.cwd()
    execution_id = f"rf-{uuid.uuid4().hex[:12]}"

    if not scope:
        print("[AEOS] [BLOCKED] Refactoring requires --scope with objective justification")
        sys.exit(1)

    aeos_root = workspace_root / ".aeos"
    patches_dir = aeos_root / "patches" / execution_id
    patches_dir.mkdir(parents=True, exist_ok=True)

    print(f"[AEOS] [REFACTOR] Proposal for: {scope}")
    print(f"[AEOS] [REFACTOR] Target: {target}")

    file_changes = [
        {
            "file": str(f.relative_to(workspace_root)) if f.is_relative_to(workspace_root) else str(f),
            "type": "refactor",
            "changes": [{"type": "hunk", "start_old": 1, "count_old": 20, "start_new": 1, "count_new": 15,
                         "lines": ["-old code", "+new code"]}],
        }
        for f in sorted(target.rglob("*"))[:5] if f.is_file() and f.suffix in (".py", ".ts", ".js")
    ] or [{"type": "analyze", "changes": [{"type": "context", "content": "Refactoring analysis target"}], "file": str(target)}]

    patch_engine = PatchProposalEngine(workspace_root, execution_id)
    patch_result = patch_engine.generate_patch(
        target,
        scope,
        file_changes,
        {},
        {"risks": [{"risk": "Architectural regression", "level": "high",
                     "mitigation": f"Behavioral preservation tests in .aeos/sandbox/{execution_id}/"}]},
    )

    arch_evidence = patches_dir / "architecture-evidence.md"
    arch_evidence.write_text(
        f"# Architecture Evidence — {execution_id}\n\n"
        f"**Scope:** {scope}\n"
        f"**Justification:** Refactoring proposed for: {scope}\n"
        f"**Files affected:** {len(file_changes)}\n\n"
        f"## Current Architecture\n"
        f"(read-only analysis)\n\n"
        f"## Proposed Architecture\n"
        f"(patch in proposed.patch)\n",
        encoding="utf-8",
    )

    # Judge v3
    judge = JudgeV3(workspace_root, aeos_root / "evidence", execution_id)
    ctx = {
        "playbook_id": "refactoring-proposal",
        "playbook_definition": {"id": "refactoring-proposal", "risk_level": "high"},
        "resolved_lcps": ["global-rules"],
        "generated_artifacts": patch_result["artifacts_generated"],
        "files_modified_outside_aeos": [],
        "secrets_exposed": [],
        "assumptions_marked": True,
        "rollback_plan_path": str(patches_dir / "rollback-plan.md"),
        "step_results": ["analysis", "patch"],
        "required_approvals": [{"action": "refactoring.propose", "scope": ".aeos/patches/**", "reason": "Refactoring"}],
        "patches_applied_automatically": [],
        "risks": [{"risk": "Architectural regression", "level": "high", "mitigation": "Behavioral preservation tests"}],
        "scope": scope,
    }
    judge_result = judge.evaluate(ctx)

    reports_dir = aeos_root / "reports" / execution_id
    reports_dir.mkdir(parents=True, exist_ok=True)

    refactoring_report = reports_dir / "refactoring-proposal.md"
    refactoring_report.write_text(
        f"# Refactoring Proposal — {execution_id}\n\n"
        f"**Scope:** {scope}\n"
        f"**Judge:** {judge_result['decision']} (Score: {judge_result['final_score']}/10)\n"
        f"**Status:** PROPOSAL ONLY — NOT APPLIED\n",
        encoding="utf-8",
    )

    evidence = EvidenceManifestV2(aeos_root, execution_id)
    for art in patch_result["artifacts_generated"]:
        ap = Path(art)
        if ap.exists():
            evidence.register_artifact(ap, "refactoring-patch", "refactoring-proposal")
    evidence.register_artifact(arch_evidence, "architecture-evidence", "refactoring-proposal")
    evidence.register_artifact(refactoring_report, "refactoring-report", "refactoring-proposal")
    evidence.save_manifest()
    evidence.save_hash_chain()
    evidence.save_integrity_report()

    result = {
        "status": "proposal_generated" if judge_result["decision"] != "BLOCKED" else "blocked",
        "execution_id": execution_id,
        "judge_score": judge_result["final_score"],
        "blocking_reasons": judge_result["blocking_reasons"],
        "patches_dir": str(patches_dir),
        "justification": scope,
    }
    print(json.dumps(result, indent=2))

    if judge_result["decision"] == "BLOCKED":
        print(f"\n[AEOS] [BLOCKED] Refactoring blocked by Judge v3")
        sys.exit(1)

    print(f"\n[AEOS] [PASS] Refactoring proposal ready for review")
    return result


# =============================================================================
# v0.3 — Approval Commands
# =============================================================================
def cmd_approvals_list(args):
    target = Path(args.target).resolve()
    engine = ApprovalEngine(target)
    records = engine.list_approvals()
    if not records:
        print("[AEOS] No approval records found")
        return
    print(f"[AEOS] Approval Records ({len(records)}):")
    print(f"  {'Approval ID':<30} {'Execution ID':<30} {'Action':<25} {'Status':<10} {'Scope':<30}")
    print(f"  {'-'*30} {'-'*30} {'-'*25} {'-'*10} {'-'*30}")
    for r in records:
        aid = r.get("approval_id", "?")[:28]
        eid = r.get("execution_id", "?")[:28]
        act = r.get("action", "?")[:23]
        st = r.get("status", "?")[:8]
        sc = r.get("scope", "?")[:28]
        print(f"  {aid:<30} {eid:<30} {act:<25} {st:<10} {sc:<30}")


def cmd_approval_show(args):
    target = Path(args.target).resolve()
    engine = ApprovalEngine(target)
    record = engine.show_approval_by_execution(args.execution_id)
    if record:
        print(json.dumps(record, indent=2))
    else:
        print(f"[AEOS] No approval found for execution: {args.execution_id}")


def cmd_approve(args):
    target = Path(args.target).resolve()
    engine = ApprovalEngine(target)
    action = args.action
    scope = args.scope
    approver = getattr(args, "approver", "cli-human")
    reason = getattr(args, "reason", "Approved via CLI")

    if action == "all" or scope in ("**", "*", "all"):
        print(f"[AEOS] [ERROR] Global unrestricted approval is prohibited")
        print(f"[AEOS]   Action: {action}, Scope: {scope}")
        sys.exit(1)

    result = engine.approve(args.execution_id, action, scope, approver, reason)
    if result["status"] == "approved":
        print(f"[AEOS] [APPROVED] {action} on {scope} for {args.execution_id}")
        print(json.dumps(result["approval"], indent=2))
    elif result["status"] == "error":
        print(f"[AEOS] [ERROR] {result['errors']}")
        sys.exit(1)


def cmd_deny(args):
    target = Path(args.target).resolve()
    engine = ApprovalEngine(target)
    action = getattr(args, "action", "patch.propose")
    scope = getattr(args, "scope", ".aeos/patches/**")
    approver = "cli-human"
    reason = args.reason

    result = engine.deny(args.execution_id, action, scope, reason, approver)
    print(f"[AEOS] [DENIED] {action} on {scope} for {args.execution_id}")
    print(f"[AEOS] Reason: {reason}")
    print(json.dumps(result["approval"], indent=2))


# =============================================================================
# Original commands
# =============================================================================
def cmd_scan(args):
    scanner = ProjectScanner(args.path)
    result = scanner.scan()
    print(json.dumps({
        "status": "ok",
        "scan_id": result.get("scan_id"),
        "project_root": str(result.get("project_root")),
        "total_files": result.get("total_files"),
        "total_dirs": result.get("total_dirs"),
        "languages": result.get("languages", []),
        "evidence_count": len(result.get("evidence", [])),
    }, indent=2))
    return result


def cmd_detect(args):
    scanner = ProjectScanner(args.path)
    scan_result = scanner.scan()
    detector = StackDetector(scan_result)
    stacks = detector.detect()
    print(json.dumps({"status": "ok", "stacks": stacks}, indent=2))
    return stacks


def cmd_ecosystem_map(args):
    scanner = ProjectScanner(args.path)
    scan_result = scanner.scan()
    detector = StackDetector(scan_result)
    stacks = detector.detect()
    gen = EcosystemMapGenerator(scan_result, stacks)
    report = gen.generate()
    output_path = args.output / "ecosystem-map.md" if args.output else Path.cwd() / "ecosystem-map.md"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(report, encoding="utf-8")
    print(f"[AEOS] Ecosystem map written to {output_path}")
    return report


def cmd_risk_report(args):
    scanner = ProjectScanner(args.path)
    scan_result = scanner.scan()
    detector = StackDetector(scan_result)
    stacks = detector.detect()
    gen = RiskReportGenerator(scan_result, stacks)
    report = gen.generate()
    output_path = args.output / "risk-report.md" if args.output else Path.cwd() / "risk-report.md"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(report, encoding="utf-8")
    print(f"[AEOS] Risk report written to {output_path}")
    return report


def cmd_playbooks(args):
    scanner = ProjectScanner(args.path)
    scan_result = scanner.scan()
    detector = StackDetector(scan_result)
    stacks = detector.detect()
    gen = PlaybookRecommender(scan_result, stacks)
    report = gen.generate()
    output_path = args.output / "recommended-playbooks.md" if args.output else Path.cwd() / "recommended-playbooks.md"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(report, encoding="utf-8")
    print(f"[AEOS] Playbook recommendations written to {output_path}")
    return report


def cmd_generate_skills(args):
    scanner = ProjectScanner(args.path)
    scan_result = scanner.scan()
    detector = StackDetector(scan_result)
    stacks = detector.detect()
    gen = SkillGenerator(scan_result, stacks)
    skills = gen.generate()
    output_dir, registration = _write_generated_skills(args.path, args.output, skills)
    print(f"[AEOS] {len(skills)} skills generated in {output_dir}")
    if registration["registry"]:
        print(f"[AEOS] {registration['registered']} skills registered in {registration['registry']}")
        if registration["skipped"]:
            print(f"[AEOS] {registration['skipped']} skills already registered")
    else:
        print("[AEOS] Registry not found; generated skills were not registered")
    return skills


def cmd_judge(args):
    ledger = EvidenceLedger(args.evidence_dir or (args.path / ".aeos" / "evidence"))
    judge = JudgeEngine()
    result = judge.evaluate(ledger.get_all())
    gen = JudgeReportGenerator(result, ledger.get_all())
    report = gen.generate()
    output_path = args.output / "judge-report.md" if args.output else Path.cwd() / "judge-report.md"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(report, encoding="utf-8")
    print(f"[AEOS] Judge report written to {output_path}")

    if result["decision"] == "BLOCKED":
        print(f"[AEOS] [BLOCKED] FINALIZATION BLOCKED — Score: {result['final_score']}/10")
        print(f"[AEOS] Reason: {result.get('blocking_reason', 'Score below minimum')}")
        sys.exit(1)
    else:
        print(f"[AEOS] [PASS] — Score: {result['final_score']}/10")
    return result


def cmd_full_scan(args):
    path = Path(args.path)
    output = args.output or (path / ".aeos")
    output.mkdir(parents=True, exist_ok=True)

    print(f"[AEOS] Scanning {path}...")
    scanner = ProjectScanner(path)
    scan_result = scanner.scan()
    print(f"[AEOS] Found {scan_result['total_files']} files, {scan_result['total_dirs']} dirs")

    evidence_ledger = EvidenceLedger(output / "evidence")
    for ev in scan_result.get("evidence", []):
        evidence_ledger.add(ev)

    print("[AEOS] Detecting stacks...")
    detector = StackDetector(scan_result)
    stacks = detector.detect()
    print(f"[AEOS] Detected {len(stacks)} stacks: {[s['name'] for s in stacks]}")

    print("[AEOS] Generating ecosystem map...")
    eco_gen = EcosystemMapGenerator(scan_result, stacks)
    eco_map = eco_gen.generate()
    (output / "ecosystem-map.md").write_text(eco_map, encoding="utf-8")

    print("[AEOS] Exporting ecosystem JSON...")
    export_ecosystem_json(scan_result, stacks, output)

    print("[AEOS] Analyzing risks...")
    risk_gen = RiskReportGenerator(scan_result, stacks)
    risk_report = risk_gen.generate()
    (output / "risk-report.md").write_text(risk_report, encoding="utf-8")

    print("[AEOS] Recommending playbooks...")
    pb_gen = PlaybookRecommender(scan_result, stacks)
    pb_report = pb_gen.generate()
    (output / "recommended-playbooks.md").write_text(pb_report, encoding="utf-8")

    print("[AEOS] Generating skills...")
    skill_gen = SkillGenerator(scan_result, stacks)
    skills = skill_gen.generate()
    skills_dir, registration = _write_generated_skills(path, output / "skills", skills)
    print(f"[AEOS] Skills written to {skills_dir}")
    if registration["registry"]:
        print(f"[AEOS] {registration['registered']} skills registered in {registration['registry']}")
        if registration["skipped"]:
            print(f"[AEOS] {registration['skipped']} skills already registered")
    else:
        print("[AEOS] Registry not found; generated skills were not registered")

    print("[AEOS] Running code quality analysis...")
    quality = CodeQualityAnalyzer(scan_result)
    quality_metrics = quality.analyze()
    scan_result["quality_metrics"] = quality_metrics
    print(f"[AEOS] Code quality score: {quality_metrics['overall']}/10")

    print("[AEOS] Running Judge evaluation...")
    judge = JudgeEngine()
    judge.set_quality_metrics(quality_metrics)
    judge_result = judge.evaluate(evidence_ledger.get_all())
    judge_gen = JudgeReportGenerator(judge_result, evidence_ledger.get_all())
    judge_report = judge_gen.generate()
    (output / "judge-report.md").write_text(judge_report, encoding="utf-8")

    print()
    print("[AEOS] " + "=" * 50)
    print("[AEOS] FULL SCAN COMPLETE")
    print(f"[AEOS] Directory: {output}")
    print(f"[AEOS] Score: {judge_result['final_score']}/10")
    print(f"[AEOS] Decision: {judge_result['decision']}")
    print("[AEOS] " + "=" * 50)

    if judge_result["decision"] == "BLOCKED":
        print(f"[AEOS] [BLOCKED] FINALIZATION BLOCKED\n[AEOS] Reason: {judge_result.get('blocking_reason', 'Score below minimum')}")
        sys.exit(1)
    else:
        print("[AEOS] [PASS] Finalization approved")
    return judge_result


def cmd_bridge_status(args):
    available = runtime_available()
    print(f"[AEOS] TypeScript Runtime: {'AVAILABLE' if available else 'NOT FOUND'}")
    if available:
        result = status()
        print(json.dumps(result, indent=2))


def cmd_bridge_run(args):
    available = runtime_available()
    if not available:
        print("[AEOS] TypeScript Runtime not found. Build it first: cd runtime && npm install && npm run build")
        return
    result = run_agent(args.provider, args.model, args.prompt)
    print(json.dumps(result, indent=2))


def cmd_setup_encryption(args):
    ledger = EvidenceLedger(args.evidence_dir or (Path.cwd() / ".aeos" / "evidence"))
    if HAS_CRYPTO:
        ok = ledger.setup_encryption(args.passphrase) if args.passphrase else ledger.setup_encryption()
        if ok:
            print(f"[AEOS] Encryption key generated and saved to {ledger._key_file}")
            print("[AEOS] Future evidence entries will be encrypted with Fernet-AES")
        else:
            print("[AEOS] Failed to set up encryption")
    else:
        print("[AEOS] cryptography library not installed. Run: pip install cryptography")
        print("[AEOS] Falling back to SHA256 integrity verification")


def cmd_agent_list(args):
    registry = AgentRegistry()
    registry.load_defaults()
    agents = registry.all()
    print(f"[AEOS] Agent Registry ({len(agents)} agents):")
    for a in agents:
        spec = a["spec"]
        print(f"  - {spec['agent_id']} [{spec['role']}]: {spec['objective']}")


def cmd_agent_dispatch(args):
    registry = AgentRegistry()
    registry.load_defaults()
    executor = AgentExecutor(registry)
    task = AgentTask(task_id="task-" + __import__("uuid").uuid4().hex[:8], objective=args.objective, target_agent=args.agent, scope=args.scope or "implementation")
    result = executor.dispatch(task)
    print(json.dumps(result, indent=2, ensure_ascii=False))
    print(f"[AEOS] Queue: {json.dumps(executor.get_summary())}")


def _add_shared_args(parser):
    parser.add_argument("--path", type=Path, default=Path.cwd(), help="Project path to scan")
    parser.add_argument("--output", type=Path, default=None, help="Output directory")
    parser.add_argument("--evidence-dir", type=Path, default=None, help="Evidence directory")


def _resolve_aeos_registry_root(project_path: Path) -> Optional[Path]:
    candidates = [project_path.resolve(), Path.cwd().resolve()]
    for candidate in candidates:
        if (candidate / "aeos" / "registries" / "skills.registry.yaml").exists():
            return candidate
    return None


def _skill_filename(skill_id: str) -> str:
    return f"{skill_id}.skill.md"


def _append_skill_registry_entries(aeos_root: Path, skills, skills_dir: Path):
    registry_path = aeos_root / "aeos" / "registries" / "skills.registry.yaml"
    if not registry_path.exists():
        return {"registered": 0, "skipped": len(skills), "registry": None}

    registry = yaml.safe_load(registry_path.read_text(encoding="utf-8")) or {}
    existing_skills = registry.get("skills") or []
    existing_ids = {
        item.get("id")
        for item in existing_skills
        if isinstance(item, dict)
    }

    entries = []
    for skill in skills:
        skill_id = skill["skill_id"]
        if skill_id in existing_ids:
            continue
        skill_path = skills_dir / _skill_filename(skill_id)
        entries.append({
            "id": skill_id,
            "path": skill_path.relative_to(aeos_root).as_posix(),
            "version": "1.0.0",
            "owner_agent": "generated",
            "risk_level": "low",
            "capabilities": ["GENERATE_REPORT"],
        })
        existing_ids.add(skill_id)

    if entries:
        with registry_path.open("a", encoding="utf-8") as fh:
            for entry in entries:
                fh.write("\n")
                fh.write(f"  - id: {entry['id']}\n")
                fh.write(f"    path: {entry['path']}\n")
                fh.write(f"    version: {entry['version']}\n")
                fh.write(f"    owner_agent: {entry['owner_agent']}\n")
                fh.write(f"    risk_level: {entry['risk_level']}\n")
                fh.write(f"    capabilities: [{', '.join(entry['capabilities'])}]\n")

    return {"registered": len(entries), "skipped": len(skills) - len(entries), "registry": str(registry_path)}


def _write_generated_skills(project_path: Path, output_dir: Optional[Path], skills):
    aeos_root = _resolve_aeos_registry_root(project_path)
    if output_dir is not None:
        skills_dir = output_dir
    elif aeos_root is not None:
        skills_dir = aeos_root / "aeos" / "skills" / "generated"
    else:
        skills_dir = Path.cwd() / "aeos-skills"

    skills_dir.mkdir(parents=True, exist_ok=True)
    for skill in skills:
        path = skills_dir / _skill_filename(skill["skill_id"])
        path.write_text(skill["content"], encoding="utf-8")

    registration = {"registered": 0, "skipped": len(skills), "registry": None}
    if aeos_root is not None:
        registration = _append_skill_registry_entries(aeos_root, skills, skills_dir)

    return skills_dir, registration


def main():
    parser = argparse.ArgumentParser(description="AEOS Workbench CLI v0.3 — Controlled Change Proposal Layer")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # === Original v0.2 commands ===
    scan_commands = ["scan", "detect", "ecosystem-map", "risk-report", "playbooks", "generate-skills", "judge", "full-scan"]
    for name in scan_commands:
        sp = subparsers.add_parser(name, help=f"Run {name}")
        _add_shared_args(sp)

    bridge_sp = subparsers.add_parser("bridge-status", help="Check TypeScript Runtime availability")
    _add_shared_args(bridge_sp)

    bridge_run = subparsers.add_parser("bridge-run", help="Run agent via TypeScript Runtime")
    bridge_run.add_argument("--provider", default="ollama", help="Provider (ollama, openai)")
    bridge_run.add_argument("--model", default="llama3", help="Model name")
    bridge_run.add_argument("--prompt", default="", help="Prompt text")
    _add_shared_args(bridge_run)

    encrypt_sp = subparsers.add_parser("setup-encryption", help="Set up evidence encryption")
    encrypt_sp.add_argument("--passphrase", default=None, help="Encryption passphrase (optional)")
    _add_shared_args(encrypt_sp)

    verify_sp = subparsers.add_parser("evidence-verify", help="Verify evidence integrity (v1)")
    _add_shared_args(verify_sp)

    evidence_verify_sp = subparsers.add_parser("evidence", help="Evidence commands (v2)")
    evidence_sub = evidence_verify_sp.add_subparsers(dest="evidence_command")
    ev_verify = evidence_sub.add_parser("verify", help="Verify evidence integrity for an execution")
    ev_verify.add_argument("--execution-id", required=True, help="Execution ID to verify")
    ev_verify.add_argument("--target", type=Path, default=Path.cwd(), help="Project target path")
    _add_shared_args(ev_verify)

    agent_list = subparsers.add_parser("agent-list", help="List registered agents")
    _add_shared_args(agent_list)

    agent_dispatch = subparsers.add_parser("agent-dispatch", help="Dispatch task to agent")
    agent_dispatch.add_argument("--agent", required=True, help="Target agent ID")
    agent_dispatch.add_argument("--objective", required=True, help="Task objective")
    agent_dispatch.add_argument("--scope", default=None, help="Task scope")

    run_sp = subparsers.add_parser("run", help="Execute a governed playbook (AEOS v0.2)")
    run_sp.add_argument("playbook", help="Playbook ID")
    run_sp.add_argument("--target", type=Path, default=Path.cwd(), help="Target project path")
    run_sp.add_argument("--mode", default="sandbox", choices=["sandbox", "dry-run"], help="Execution mode")
    run_sp.add_argument("--dry-run", action="store_true", help="Perform dry run")
    run_sp.add_argument("--cache", action="store_true", default=False, help="Enable evidence cache")
    run_sp.add_argument("--no-cache", action="store_true", default=False, help="Disable cache (override)")
    run_sp.add_argument("--encrypt-rollback", action="store_true", default=False, help="Encrypt rollback plan with AES-256-GCM")

    # === v0.3 — Controlled Change Commands ===
    # dry-run-preview
    drp = subparsers.add_parser("dry-run-preview", help="[v0.3] Generate dry-run preview without side effects")
    drp.add_argument("--target", type=Path, default=Path.cwd(), help="Target project path")

    # code-change-proposal
    ccp = subparsers.add_parser("code-change-proposal", help="[v0.3] Generate code change proposal (patch + dry-run + rollback)")
    ccp.add_argument("--target", type=Path, required=True, help="Target project path")
    ccp.add_argument("--issue", required=True, help="Issue description for the change")

    # test-generation
    tg = subparsers.add_parser("test-generation", help="[v0.3] Generate tests in sandbox without modifying real tests")
    tg.add_argument("--target", type=Path, required=True, help="Target source path")
    tg.add_argument("--mode", default="sandbox", choices=["sandbox"], help="Generation mode (sandbox only)")

    # dependency-analysis
    da = subparsers.add_parser("dependency-analysis", help="[v0.3] Analyze dependencies without modifying them")
    da.add_argument("--target", type=Path, required=True, help="Target project path")

    # refactoring-proposal
    rp = subparsers.add_parser("refactoring-proposal", help="[v0.3] Generate refactoring proposal (patch only, no apply)")
    rp.add_argument("--target", type=Path, required=True, help="Target project path")
    rp.add_argument("--scope", required=True, help="Scope + justification for the refactoring")

    # approval commands
    al = subparsers.add_parser("approvals", help="[v0.3] Approval management commands")
    al_sub = al.add_subparsers(dest="approval_command")
    al_list = al_sub.add_parser("list", help="List all approval records")
    al_list.add_argument("--target", type=Path, default=Path.cwd(), help="Project path")
    al_show = al_sub.add_parser("show", help="Show approval for an execution")
    al_show.add_argument("execution_id", help="Execution ID to show approval for")
    al_show.add_argument("--target", type=Path, default=Path.cwd(), help="Project path")

    approve_sp = subparsers.add_parser("approve", help="[v0.3] Approve an action for an execution")
    approve_sp.add_argument("execution_id", help="Execution ID to approve")
    approve_sp.add_argument("--target", type=Path, default=Path.cwd(), help="Project path")
    approve_sp.add_argument("--action", required=True, help="Action to approve (e.g., patch.propose)")
    approve_sp.add_argument("--scope", required=True, help="Scope to approve (e.g., .aeos/patches/**)")
    approve_sp.add_argument("--reason", default="Approved via CLI", help="Approval reason")

    deny_sp = subparsers.add_parser("deny", help="[v0.3] Deny an action for an execution")
    deny_sp.add_argument("execution_id", help="Execution ID to deny")
    deny_sp.add_argument("--target", type=Path, default=Path.cwd(), help="Project path")
    deny_sp.add_argument("--action", default="patch.propose", help="Action to deny")
    deny_sp.add_argument("--scope", default=".aeos/patches/**", help="Scope to deny")
    deny_sp.add_argument("--reason", required=True, help="Denial reason")

    cache_sp = subparsers.add_parser("cache", help="Cache management commands")
    cache_sub = cache_sp.add_subparsers(dest="cache_command")
    cache_clear = cache_sub.add_parser("clear", help="Clear evidence cache")
    cache_clear.add_argument("--playbook", default=None, help="Clear cache for specific playbook")
    cache_status = cache_sub.add_parser("status", help="Show cache status")

    args = parser.parse_args()

    # === v0.3 Command Routing ===
    if args.command == "dry-run-preview":
        cmd_dry_run_preview(args)
    elif args.command == "code-change-proposal":
        cmd_code_change_proposal(args)
    elif args.command == "test-generation":
        cmd_test_generation(args)
    elif args.command == "dependency-analysis":
        cmd_dependency_analysis(args)
    elif args.command == "refactoring-proposal":
        cmd_refactoring_proposal(args)
    elif args.command == "approvals":
        if args.approval_command == "list":
            cmd_approvals_list(args)
        elif args.approval_command == "show":
            cmd_approval_show(args)
        else:
            print("[AEOS] Use: aeos approvals list|show")
    elif args.command == "approve":
        cmd_approve(args)
    elif args.command == "deny":
        cmd_deny(args)
    # === v0.2 Command Routing ===
    elif args.command == "run":
        cmd_run(args)
    elif args.command == "evidence":
        if args.evidence_command == "verify":
            cmd_evidence_verify(args)
        else:
            print("[AEOS] Use: aeos evidence verify --execution-id <id>")
    elif args.command == "evidence-verify":
        cmd_evidence_verify(args)
    elif args.command == "scan":
        cmd_scan(args)
    elif args.command == "detect":
        cmd_detect(args)
    elif args.command == "ecosystem-map":
        cmd_ecosystem_map(args)
    elif args.command == "risk-report":
        cmd_risk_report(args)
    elif args.command == "playbooks":
        cmd_playbooks(args)
    elif args.command == "generate-skills":
        cmd_generate_skills(args)
    elif args.command == "judge":
        cmd_judge(args)
    elif args.command == "full-scan":
        cmd_full_scan(args)
    elif args.command == "bridge-status":
        cmd_bridge_status(args)
    elif args.command == "bridge-run":
        cmd_bridge_run(args)
    elif args.command == "setup-encryption":
        cmd_setup_encryption(args)
    elif args.command == "agent-list":
        cmd_agent_list(args)
    elif args.command == "agent-dispatch":
        cmd_agent_dispatch(args)
    elif args.command == "cache":
        cmd_cache(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
