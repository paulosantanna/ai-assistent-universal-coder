#!/usr/bin/env python3
"""
AEOS Production Readiness Audit Runner.
Usage: py -3 aeos/scripts/run_readiness_audit.py
Exit codes: 0=PASS  1=BLOCKED  2=ERROR  3=REVIEW
"""

from __future__ import annotations

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from aeos.core.readiness.production_gate import ProductionGate
from aeos.core.readiness.readiness_models import (
    READINESS_PASS, READINESS_BLOCKED, READINESS_ERROR, READINESS_REVIEW,
)
from aeos.core.readiness.readiness_reporter import ReadinessReporter


def main():
    print("[READINESS] Running Production Readiness Audit...\n")
    gate = ProductionGate(workspace_root=".")
    result = gate.evaluate()
    reporter = ReadinessReporter(workspace_root=".")

    print(f"Status: {result.status}")
    print(f"Overall Score: {result.overall_score:.4f}")
    print(f"\nCategory Scores:")
    for cat, score in sorted(result.categories.items()):
        icon = "PASS" if score >= 0.95 else "WARN" if score >= 0.80 else "FAIL"
        print(f"  [{icon}] {cat}: {score:.4f}")

    print(f"\nCritical Blockers: {len(result.critical_blockers)}")
    for cb in result.critical_blockers:
        print(f"  - {cb}")
    print(f"High Risks: {len(result.high_risks)}")
    for hr in result.high_risks:
        print(f"  - {hr}")

    report_path = f".aeos/reports/{result.execution_id}/production-readiness-report.md"
    print(f"\nReport: {report_path}")

    exit_codes = {
        READINESS_PASS: 0,
        READINESS_BLOCKED: 1,
        READINESS_ERROR: 2,
        READINESS_REVIEW: 3,
    }
    sys.exit(exit_codes.get(result.status, 2))


if __name__ == "__main__":
    main()
