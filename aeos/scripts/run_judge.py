#!/usr/bin/env python3
"""
AEOS Judge Runner — deterministic evaluation of execution evidence.
Usage: py -3 aeos/scripts/run_judge.py --execution-id <id>
       py -3 aeos/scripts/run_judge.py --execution-id latest
Exit codes: 0=PASS  1=BLOCKED  2=ERROR  3=REVIEW
"""

from __future__ import annotations

import sys
import os
import argparse

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from aeos.core.judge.judge_engine import JudgeEngine
from aeos.core.judge.judge_models import JUDGE_STATUS_PASS, JUDGE_STATUS_BLOCKED, JUDGE_STATUS_ERROR, JUDGE_STATUS_REVIEW
from aeos.core.judge.judge_gate_loader import JudgeGateLoader


def main():
    parser = argparse.ArgumentParser(description="AEOS Judge Runner")
    parser.add_argument("--execution-id", default="latest", help="Execution ID or 'latest'")
    parser.add_argument("--target-path", default=".", help="Target path")
    args = parser.parse_args()

    engine = JudgeEngine(workspace_root=".")
    gate_loader = JudgeGateLoader(workspace_root=".")

    execution_id = args.execution_id
    if execution_id == "latest":
        latest = gate_loader.load_latest_judge_result()
        if latest is not None:
            execution_id = latest.execution_id
            print(f"[JUDGE] Re-judging last execution: {execution_id}")
            result = engine.evaluate(execution_id, args.target_path)
        else:
            # No previous judge result — build fresh from evidence
            import glob as glob_mod
            evidence_dirs = sorted(
                [d for d in glob_mod.glob(".aeos/evidence/*/") if os.path.isdir(d)],
                key=lambda d: os.path.getmtime(d), reverse=True,
            )
            if not evidence_dirs:
                print("[JUDGE] ERROR: No evidence directories found")
                sys.exit(2)
            execution_id = os.path.basename(os.path.normpath(evidence_dirs[0]))
            print(f"[JUDGE] Using latest evidence: {execution_id}")
            result = engine.evaluate(execution_id, args.target_path)
    else:
        result = engine.evaluate(execution_id, args.target_path)

    summary = engine.summarize(result)
    print(f"\n[JUDGE] Status: {result.status}")
    print(f"[JUDGE] Score: {result.score:.4f}")
    print(f"[JUDGE] Blocking rules: {len(result.blocking_rules)}")
    for rule in result.blocking_rules:
        print(f"       - {rule}")
    print(f"[JUDGE] Warnings: {len(result.warnings)}")
    print(f"[JUDGE] Evidence: .aeos/evidence/{execution_id}/judge-result.json")
    print(f"[JUDGE] Report: .aeos/reports/{execution_id}/judge-report.md")

    exit_codes = {
        JUDGE_STATUS_PASS: 0,
        JUDGE_STATUS_BLOCKED: 1,
        JUDGE_STATUS_ERROR: 2,
        JUDGE_STATUS_REVIEW: 3,
    }
    sys.exit(exit_codes.get(result.status, 2))


if __name__ == "__main__":
    main()
