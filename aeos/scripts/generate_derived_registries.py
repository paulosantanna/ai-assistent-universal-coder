#!/usr/bin/env python3
"""Generate deterministic AEOS derived registries."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from aeos.core.registries.registry_loader_orchestrator import run_phase2


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Generate .aeos/derived/registries from source registries.")
    parser.add_argument("--workspace-root", default=".", help="Workspace root to process.")
    parser.add_argument("--json", action="store_true", help="Print machine-readable result.")
    args = parser.parse_args(argv)

    result = run_phase2(args.workspace_root)
    if args.json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0 if result.get("status") == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
