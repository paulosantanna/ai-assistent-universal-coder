from __future__ import annotations

import json
import sys


def cmd_performance_benchmark(args) -> int:
    from aeos.cli.main import get_workspace_root, resolve_aeos_root
    from aeos.core.performance.benchmark_runner import PerformanceBenchmarkRunner

    workspace = get_workspace_root(args)
    aeos_root = resolve_aeos_root(args)
    iterations = int(getattr(args, "iterations", 3))
    profile = str(getattr(args, "profile", "quick"))
    fail_on = str(getattr(args, "fail_on", "warn"))

    try:
        runner = PerformanceBenchmarkRunner(workspace_root=workspace, aeos_root=aeos_root)
        result = runner.run(iterations=iterations, profile=profile)
        reports = runner.write_reports(result)
        if getattr(args, "json", False):
            print(json.dumps({"result": result, "reports": reports}, indent=2, ensure_ascii=False))
        else:
            print(f"Performance benchmark: {result['status']}")
            print(f"Profile: {profile}")
            print(f"Iterations: {iterations}")
            for case in result["cases"]:
                print(
                    f"  - {case['name']}: {case['status']} "
                    f"(p50={case['p50_seconds']:.6f}s, p95={case['p95_seconds']:.6f}s)"
                )
            print(f"Report: {reports['markdown']}")
        if result["status"] == "BREACHED":
            return 1
        if result["status"] == "WARN":
            return 3 if fail_on == "warn" else 0
        return 0
    except Exception as exc:
        print(f"Performance benchmark error: {exc}", file=sys.stderr)
        return 2
