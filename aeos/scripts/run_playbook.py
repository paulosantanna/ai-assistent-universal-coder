#!/usr/bin/env python3
"""AEOS — Run a playbook through the RuntimeOrchestrator."""

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

import argparse
import json

from aeos.core.runtime.runtime_orchestrator import RuntimeOrchestrator
from aeos.core.runtime.runtime_models import RuntimeRequest, generate_execution_id


def main() -> int:
    parser = argparse.ArgumentParser(description="AEOS — Run a playbook")
    parser.add_argument("--playbook-id", required=True, help="Playbook ID to execute")
    parser.add_argument("--actor", default="cli-user", help="Actor name")
    parser.add_argument("--role", default="architect", help="Role name")
    parser.add_argument("--target", default=".", help="Target path")
    parser.add_argument("--dry-run", action="store_true", default=True, help="Dry run mode")
    parser.add_argument("--no-dry-run", action="store_false", dest="dry_run", help="Execute for real")
    parser.add_argument("--input", default="{}", help="JSON input for the playbook")
    args = parser.parse_args()

    try:
        input_data = json.loads(args.input)
    except json.JSONDecodeError:
        input_data = {"raw": args.input}

    orchestrator = RuntimeOrchestrator(workspace_root=args.target)
    orchestrator.initialize()

    execution_id = generate_execution_id()
    print(f"[AEOS] Execution ID: {execution_id}")
    print(f"[AEOS] Running playbook '{args.playbook_id}' (dry_run={args.dry_run})...")

    request = RuntimeRequest(
        execution_id=execution_id,
        run_type="playbook",
        entity_id=args.playbook_id,
        actor=args.actor,
        role=args.role,
        input=input_data,
        target_path=args.target,
        dry_run=args.dry_run,
    )

    result = orchestrator.run(request)

    print(f"\n[AEOS] Status: {result.status}")
    print(f"[AEOS] Duration: {result.duration_ms}ms")
    if result.blocking_conditions:
        print(f"[AEOS] Blocking conditions: {result.blocking_conditions}")
    if result.error:
        print(f"[AEOS] Error: {result.error}")
    print(f"[AEOS] Evidence: .aeos/evidence/{execution_id}/")

    exit_codes = {"PASS": 0, "BLOCKED": 1, "ERROR": 2, "WAITING_APPROVAL": 3}
    return exit_codes.get(result.status, 2)


if __name__ == "__main__":
    sys.exit(main())
