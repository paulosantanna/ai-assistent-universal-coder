#!/usr/bin/env python3
"""
AEOS Evaluation Harness Runner.
Usage: py -3 aeos/scripts/run_evals.py --suite all
       py -3 aeos/scripts/run_evals.py --suite anti_hallucination
Exit codes: 0=PASS  1=FAIL  2=ERROR
"""

from __future__ import annotations

import sys
import os
import argparse

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from aeos.core.evals.eval_runner import EvalRunner
from aeos.core.evals.eval_reporter import EvalReporter


def main():
    parser = argparse.ArgumentParser(description="AEOS Evaluation Harness Runner")
    parser.add_argument("--suite", default="all", help="Suite ID or 'all'")
    args = parser.parse_args()

    runner = EvalRunner(workspace_root=".")
    reporter = EvalReporter(workspace_root=".")

    if args.suite == "all":
        print("[EVALS] Running all suites...")
        results = runner.run_all_suites()
    else:
        print(f"[EVALS] Running suite: {args.suite}")
        results = runner.run_suite_by_id(args.suite)

    scorecard = runner.get_scorecard()

    report_path = reporter.generate_report(results, scorecard)
    print(f"\n[EVALS] Results: {scorecard.passed}/{scorecard.total_cases} passed")
    print(f"[EVALS] Overall score: {scorecard.overall_score:.4f}")
    print(f"[EVALS] Blocking failures: {len(scorecard.blocking_failures)}")
    for bf in scorecard.blocking_failures:
        print(f"       - {bf}")
    print(f"[EVALS] Report: {report_path}")

    if scorecard.blocking_failures:
        sys.exit(1)

    sys.exit(0 if scorecard.status == "PASS" else 1)


if __name__ == "__main__":
    main()
