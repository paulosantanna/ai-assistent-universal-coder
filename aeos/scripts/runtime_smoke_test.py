#!/usr/bin/env python3
"""AEOS Runtime Smoke Test — validates Skill Engine, Playbook Engine, Agent Runtime integration."""

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from aeos.core.runtime.runtime_orchestrator import RuntimeOrchestrator
from aeos.core.runtime.runtime_models import RuntimeRequest, generate_execution_id

EXECUTION_ID = generate_execution_id()
results: list[tuple[str, bool, str]] = []
errors: list[str] = []


def check(name: str, condition: bool, detail: str = ""):
    if condition:
        print(f"  [PASS] {name}")
    else:
        msg = f"  [FAIL] {name}"
        if detail:
            msg += f" - {detail}"
        print(msg)
        errors.append(name)
    results.append((name, condition, detail))


def main() -> int:
    print("=" * 60)
    print("AEOS Runtime Smoke Test")
    print(f"Execution ID: {EXECUTION_ID}")
    print("=" * 60)

    orchestrator = RuntimeOrchestrator(workspace_root=".")
    orchestrator.initialize()

    # 1. Run skill
    print("\n[1] Execute skill via RuntimeOrchestrator")
    req = RuntimeRequest(
        execution_id=EXECUTION_ID,
        run_type="skill",
        entity_id="repo-scanner",
        actor="smoke-tester",
        role="tester",
        input={"target_path": "."},
        dry_run=True,
    )
    result = orchestrator.run_skill(req)
    check("skill executed", result.status in ("PASS", "BLOCKED"), f"got {result.status}")

    # 2. Run playbook
    print("\n[2] Execute playbook via RuntimeOrchestrator")
    req = RuntimeRequest(
        execution_id=EXECUTION_ID,
        run_type="playbook",
        entity_id="project-analysis",
        actor="smoke-tester",
        role="tester",
        input={"target_path": "."},
        dry_run=True,
    )
    result = orchestrator.run_playbook(req)
    check("playbook executed", result.status in ("PASS", "BLOCKED"), f"got {result.status}")

    # 3. Run agent task
    print("\n[3] Execute agent task via RuntimeOrchestrator")
    req = RuntimeRequest(
        execution_id=EXECUTION_ID,
        run_type="agent",
        entity_id="planner",
        actor="smoke-tester",
        role="tester",
        input={"objective": "dry-run project analysis", "target_path": "."},
        dry_run=True,
    )
    result = orchestrator.run_agent_task(req)
    check("agent task executed", result.status in ("PASS", "BLOCKED"), f"got {result.status}")

    # 4. Run unknown type
    print("\n[4] Run unknown type => ERROR")
    req = RuntimeRequest(
        execution_id=EXECUTION_ID,
        run_type="unknown",
        entity_id="test",
        actor="tester",
        role="tester",
    )
    result = orchestrator.run(req)
    check("unknown type blocked", result.status == "ERROR", f"got {result.status}")

    # 5. Evidence generated
    print("\n[5] Evidence files generated")
    import json
    evidence_base = os.path.join(".aeos", "evidence", EXECUTION_ID)
    if os.path.isdir(evidence_base):
        files = os.listdir(evidence_base)
        check("evidence exists", len(files) > 0, f"got {len(files)} files")
        for f in sorted(files):
            print(f"    - {f}")
    else:
        check("evidence dir exists", False, f"not found: {evidence_base}")

    # 6. Report generated
    print("\n[6] Report files generated")
    report_base = os.path.join(".aeos", "reports", EXECUTION_ID)
    if os.path.isdir(report_base):
        files = os.listdir(report_base)
        check("reports exist", len(files) > 0, f"got {len(files)} files")
        for f in sorted(files):
            print(f"    - {f}")
    else:
        check("reports dir exists", False, f"not found: {report_base}")

    print("\n" + "=" * 60)
    passed = sum(1 for r in results if r[1])
    total = len(results)
    failed = total - passed
    print(f"Results: {passed}/{total} passed, {failed} failed")
    if failed == 0:
        print("\n  STATUS: PASS")
    else:
        print(f"\n  STATUS: FAIL ({failed} errors)")
    print("=" * 60)

    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
