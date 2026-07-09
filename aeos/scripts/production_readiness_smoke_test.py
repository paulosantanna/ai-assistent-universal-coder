#!/usr/bin/env python3
"""
AEOS Production Readiness Smoke Test.
Runs the full pipeline: Runtime -> Judge -> Evals -> Readiness Audit.

Usage: py -3 aeos/scripts/production_readiness_smoke_test.py

Exit codes:
  0 = PASS (all gates green)
  1 = BLOCKED (at least one gate failed)
  2 = ERROR (technical error)
  3 = REVIEW (at least one gate requires review)
"""

from __future__ import annotations

import sys
import os
import json
from pathlib import Path
from time import monotonic

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from aeos.core.runtime.runtime_orchestrator import RuntimeOrchestrator
from aeos.core.runtime.runtime_models import RuntimeRequest, generate_execution_id
from aeos.core.judge.judge_models import JUDGE_STATUS_PASS, JUDGE_STATUS_BLOCKED, JUDGE_STATUS_REVIEW
from aeos.core.readiness.readiness_models import READINESS_PASS, READINESS_BLOCKED, READINESS_REVIEW
from aeos.core.evidence.evidence_manifest import StagedManifestBuilder, compute_manifest_hash, STAGE_FILENAMES


def main():
    failures: list[str] = []
    overall_exit = 0

    print("=" * 60)
    print("AEOS Production Readiness Smoke Test")
    print("=" * 60)

    orchestrator = RuntimeOrchestrator(workspace_root=".")
    orchestrator.initialize()

    # Phase 1: Run skill through orchestrator
    print("\n[Phase 1] Running skill through orchestrator...")
    execution_id = generate_execution_id()
    req = RuntimeRequest(
        execution_id=execution_id,
        run_type="skill",
        entity_id="repo-scanner",
        actor="smoke-tester",
        role="architect",
        input={"target_path": "."},
        dry_run=True,
    )
    rt_result = orchestrator.run(req)
    print(f"  Runtime status: {rt_result.status}")
    if rt_result.status in ("BLOCKED", "ERROR"):
        failures.append(f"Runtime: {rt_result.status}")
    elif rt_result.status == "REVIEW":
        if overall_exit < 3:
            overall_exit = 3

    # Phase 2: Judge evaluation
    print("\n[Phase 2] Running Judge evaluation...")
    judge_result = orchestrator.judge_engine.evaluate(execution_id)
    print(f"  Judge status: {judge_result.status}")
    print(f"  Judge score: {judge_result.score:.4f}")
    print(f"  Blocking rules: {judge_result.blocking_rules}")
    if judge_result.blocking_rules:
        for rule in judge_result.blocking_rules:
            print(f"    - {rule}")

    if judge_result.status == JUDGE_STATUS_BLOCKED:
        failures.append(f"Judge: BLOCKED (score={judge_result.score:.4f}, rules={judge_result.blocking_rules})")
    elif judge_result.status == JUDGE_STATUS_REVIEW:
        if overall_exit < 3:
            overall_exit = 3
        failures.append(f"Judge: REVIEW (score={judge_result.score:.4f})")

    # Phase 3: Run evaluation harness
    print("\n[Phase 3] Running Evaluation Harness...")
    eval_results = orchestrator.eval_runner.run_all_suites()
    scorecard = orchestrator.eval_runner.get_scorecard()
    print(f"  Evals: {scorecard.passed}/{scorecard.total_cases} passed")
    print(f"  Overall score: {scorecard.overall_score:.4f}")
    print(f"  Blocking failures: {len(scorecard.blocking_failures)}")
    if scorecard.blocking_failures:
        for bf in scorecard.blocking_failures:
            print(f"    - {bf}")

    if scorecard.overall_score < 0.95:
        failures.append(f"Evals: score={scorecard.overall_score:.4f} below 0.95 threshold ({scorecard.passed}/{scorecard.total_cases} passed)")

    # Phase 5: Production Readiness Audit
    print("\n[Phase 5] Running Production Readiness Audit...")
    readiness_result = orchestrator.production_gate.evaluate()
    print(f"  Readiness status: {readiness_result.status}")
    print(f"  Overall score: {readiness_result.overall_score:.4f}")
    print(f"  Critical blockers: {len(readiness_result.critical_blockers)}")
    if readiness_result.critical_blockers:
        for cb in readiness_result.critical_blockers:
            print(f"    - {cb}")

    if readiness_result.status != READINESS_PASS:
        failures.append(f"Readiness: {readiness_result.status} (score={readiness_result.overall_score:.4f})")

    # Verify evidence files
    print("\n[Verification] Checking evidence files...")
    evidence_dir = Path(".aeos") / "evidence" / execution_id
    required_evidence = [
        "runtime-evidence-manifest.json",
        "judge-evidence-manifest.json",
        "judge-input.json",
        "judge-result.json",
        "judge-scorecard.json",
    ]
    for filename in required_evidence:
        if not (evidence_dir / filename).exists():
            failures.append(f"Missing evidence: {evidence_dir / filename}")

    eval_evidence_dir = Path(".aeos") / "evidence" / orchestrator.eval_runner.execution_id
    if not (eval_evidence_dir / "eval-scorecard.json").exists():
        failures.append(f"Missing eval evidence: {eval_evidence_dir}/eval-scorecard.json")

    readiness_evidence = Path(".aeos") / "evidence" / readiness_result.execution_id
    if not (readiness_evidence / "production-readiness-scorecard.json").exists():
        failures.append(f"Missing readiness evidence: {readiness_evidence}/production-readiness-scorecard.json")

    # Stage D: Finalize readiness manifest
    readiness_builder = StagedManifestBuilder(readiness_result.execution_id, str(readiness_evidence))
    if not (readiness_evidence / "readiness-evidence-manifest.json").exists():
        readiness_builder.finalize_readiness_manifest()
        print(f"  [D] Readiness evidence manifest finalized")

    # Stage E: Final bundle manifest (includes all staged manifests)
    exec_evidence_dir = Path(".aeos") / "evidence" / execution_id
    eval_evidence_dir = Path(".aeos") / "evidence" / orchestrator.eval_runner.execution_id
    workspace_root = Path(".").resolve()

    print(f"  [E] Finalizing bundle evidence-manifest.json...")
    final_builder = StagedManifestBuilder(execution_id, str(exec_evidence_dir), str(workspace_root))
    final_builder.finalize_evidence_manifest(
        extra_evidence_dirs=[str(eval_evidence_dir), str(readiness_evidence)]
    )

    # Verify all manifests in their original locations
    print(f"\n[Verification] Checking all staged manifests...")
    all_passed = True
    for stage, src_dir in [
        ("runtime", exec_evidence_dir),
        ("eval", eval_evidence_dir),
        ("judge", exec_evidence_dir),
        ("readiness", readiness_evidence),
        ("final", exec_evidence_dir),
    ]:
        stage_builder = StagedManifestBuilder(execution_id, str(src_dir), str(workspace_root))
        vres = stage_builder.verify_manifest(stage)
        if not vres.get("passed", False):
            all_passed = False
            for err in vres.get("file_errors", []):
                failures.append(f"Manifest [{stage}]: {err}")
                print(f"    - [{stage}] {err}")
    if all_passed:
        print(f"  All manifests verified: PASS")

    # Verify reports
    print("  Checking report files...")
    reports_dir = Path(".aeos") / "reports"
    required_reports = [
        (reports_dir / execution_id / "runtime-orchestrator-report.md", "runtime report"),
        (reports_dir / execution_id / "judge-report.md", "judge report"),
        (reports_dir / orchestrator.eval_runner.execution_id / "evaluation-harness-report.md", "eval report"),
        (reports_dir / readiness_result.execution_id / "production-readiness-report.md", "readiness report"),
    ]
    for fp, label in required_reports:
        if not fp.exists():
            failures.append(f"Missing report: {label} ({fp})")

    print("\n" + "=" * 60)
    if not failures:
        print("SMOKE TEST PASSED")
        print("=" * 60)
        print(f"\nSummary:")
        print(f"  Runtime:    {rt_result.status}")
        print(f"  Judge:      {judge_result.status} ({judge_result.score:.4f})")
        print(f"  Evals:      {scorecard.passed}/{scorecard.total_cases} passed ({scorecard.overall_score:.4f})")
        print(f"  Readiness:  {readiness_result.status} ({readiness_result.overall_score:.4f})")
        sys.exit(0)
    else:
        if any("BLOCKED" in f or "below 0.95" in f for f in failures):
            overall_exit = 1
        elif any("REVIEW" in f for f in failures):
            if overall_exit < 3:
                overall_exit = 3
        else:
            overall_exit = 1

        print("SMOKE TEST BLOCKED")
        print("=" * 60)
        print(f"\nFailures ({len(failures)}):")
        for f in failures:
            print(f"  - {f}")
        print(f"\nSummary:")
        print(f"  Runtime:    {rt_result.status}")
        print(f"  Judge:      {judge_result.status} ({judge_result.score:.4f})")
        print(f"  Evals:      {scorecard.passed}/{scorecard.total_cases} passed ({scorecard.overall_score:.4f})")
        print(f"  Readiness:  {readiness_result.status} ({readiness_result.overall_score:.4f})")
        sys.exit(overall_exit)


if __name__ == "__main__":
    try:
        main()
    except AssertionError as e:
        print(f"\nSMOKE TEST FAILED: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\nSMOKE TEST ERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(2)
