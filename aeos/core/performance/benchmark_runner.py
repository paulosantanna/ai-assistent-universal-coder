from __future__ import annotations

import json
import statistics
import tempfile
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Any

import yaml

from aeos.core.evidence.evidence_store import EvidenceStore
from aeos.core.performance.performance_optimizer import PerformanceOptimizer, PerformanceSignal
from aeos.core.scanner.fast_repo_scanner import FastRepoScanner
from aeos.core.skill_engine.skill_loader import SkillLoader
from aeos.core.skill_engine.skill_registry_resolver import SkillRegistryResolver


@dataclass(frozen=True)
class BenchmarkCase:
    name: str
    category: str
    operation: Callable[[], None]


@dataclass(frozen=True)
class BenchmarkCaseResult:
    name: str
    category: str
    samples_seconds: list[float]
    p50_seconds: float
    p95_seconds: float
    budget_p50_seconds: float
    budget_p95_seconds: float
    status: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "category": self.category,
            "samples_seconds": self.samples_seconds,
            "p50_seconds": self.p50_seconds,
            "p95_seconds": self.p95_seconds,
            "budget_p50_seconds": self.budget_p50_seconds,
            "budget_p95_seconds": self.budget_p95_seconds,
            "status": self.status,
        }


class PerformanceBenchmarkRunner:
    def __init__(self, workspace_root: str | Path = ".", aeos_root: str | Path | None = None):
        self.workspace_root = Path(workspace_root).resolve()
        self.aeos_root = Path(aeos_root).resolve() if aeos_root else self.workspace_root
        self.budgets = self._load_budgets()

    def run(self, iterations: int = 3, profile: str = "quick") -> dict[str, Any]:
        if iterations < 1:
            raise ValueError("iterations must be >= 1")
        cases = self._cases(profile)
        results = [self._run_case(case, iterations) for case in cases]
        signals = [
            PerformanceSignal(
                name=result.name,
                actual_seconds=result.p95_seconds,
                p50_seconds=result.budget_p50_seconds,
                p95_seconds=result.budget_p95_seconds,
                category=result.category,
            )
            for result in results
        ]
        optimization_plan = PerformanceOptimizer().plan(signals)
        return {
            "status": optimization_plan["status"],
            "profile": profile,
            "iterations": iterations,
            "cases": [result.to_dict() for result in results],
            "summary": optimization_plan["summary"],
            "recommendations": optimization_plan["recommendations"],
            "blocking_conditions": optimization_plan["blocking_conditions"],
        }

    def write_reports(self, result: dict[str, Any], output_dir: str | Path | None = None) -> dict[str, str]:
        base = Path(output_dir).resolve() if output_dir else self.workspace_root / ".aeos" / "reports" / "performance"
        base.mkdir(parents=True, exist_ok=True)
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        json_path = base / f"performance-benchmark-{timestamp}.json"
        md_path = base / f"performance-benchmark-{timestamp}.md"
        json_path.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")
        md_path.write_text(self._markdown(result), encoding="utf-8")
        return {"json": str(json_path), "markdown": str(md_path)}

    def _cases(self, profile: str) -> list[BenchmarkCase]:
        if profile != "quick":
            raise ValueError(f"Unsupported benchmark profile: {profile}")
        return [
            BenchmarkCase("registry_load", "registry", self._bench_registry_load),
            BenchmarkCase("skill_contract_load", "registry", self._bench_skill_contract_load),
            BenchmarkCase("scanner_pruned", "scanner", self._bench_scanner_pruned),
            BenchmarkCase("evidence_batch_write", "evidence", self._bench_evidence_batch_write),
        ]

    def _run_case(self, case: BenchmarkCase, iterations: int) -> BenchmarkCaseResult:
        samples = []
        for _ in range(iterations):
            start = time.perf_counter()
            case.operation()
            samples.append(time.perf_counter() - start)
        p50 = statistics.median(samples)
        p95 = max(samples) if len(samples) < 20 else statistics.quantiles(samples, n=100)[94]
        budget = self._budget_for(case.name)
        status = PerformanceSignal(
            name=case.name,
            actual_seconds=p95,
            p50_seconds=budget["p50_seconds"],
            p95_seconds=budget["p95_seconds"],
            category=case.category,
        ).status()
        return BenchmarkCaseResult(
            name=case.name,
            category=case.category,
            samples_seconds=[round(sample, 6) for sample in samples],
            p50_seconds=round(p50, 6),
            p95_seconds=round(p95, 6),
            budget_p50_seconds=budget["p50_seconds"],
            budget_p95_seconds=budget["p95_seconds"],
            status=status,
        )

    def _bench_registry_load(self) -> None:
        SkillRegistryResolver.clear_cache()
        resolver = SkillRegistryResolver(str(self.aeos_root))
        resolver.load()

    def _bench_skill_contract_load(self) -> None:
        loader = SkillLoader(str(self.aeos_root))
        loader.load_skill_contract("repo-scanner")
        loader.load_skill_contract("repo-scanner")

    def _bench_scanner_pruned(self) -> None:
        with tempfile.TemporaryDirectory(prefix="aeos-bench-scan-") as tmp:
            root = Path(tmp)
            for i in range(20):
                (root / f"file{i}.py").write_text("x = 1\n", encoding="utf-8")
            ignored = root / "node_modules" / "pkg"
            ignored.mkdir(parents=True)
            for i in range(80):
                (ignored / f"ignored{i}.js").write_text("module.exports = {}\n", encoding="utf-8")
            FastRepoScanner(root=root, exclude=["node_modules"], count_ignored_files=False).scan()

    def _bench_evidence_batch_write(self) -> None:
        with tempfile.TemporaryDirectory(prefix="aeos-bench-evidence-") as tmp:
            store = EvidenceStore(tmp)
            store.store_records("bench", "audit", [{"i": i} for i in range(25)])

    def _load_budgets(self) -> dict[str, Any]:
        path = self.aeos_root / "aeos" / "config" / "performance-budgets.yaml"
        if not path.exists():
            return {}
        with open(path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f) or {}
        return data.get("performance_budgets", {})

    def _budget_for(self, name: str) -> dict[str, float]:
        budget = self.budgets.get(name, {})
        return {
            "p50_seconds": float(budget.get("p50_seconds", 1.0)),
            "p95_seconds": float(budget.get("p95_seconds", 5.0)),
        }

    def _markdown(self, result: dict[str, Any]) -> str:
        lines = [
            "# AEOS Performance Benchmark",
            "",
            f"- Status: `{result['status']}`",
            f"- Profile: `{result['profile']}`",
            f"- Iterations: `{result['iterations']}`",
            "",
            "## Cases",
            "",
            "| Case | Status | p50 | p95 | Budget p95 |",
            "| --- | --- | ---: | ---: | ---: |",
        ]
        for case in result["cases"]:
            lines.append(
                f"| `{case['name']}` | `{case['status']}` | "
                f"{case['p50_seconds']:.6f}s | {case['p95_seconds']:.6f}s | "
                f"{case['budget_p95_seconds']:.6f}s |"
            )
        lines.extend(["", "## Blocking Conditions", ""])
        blockers = result.get("blocking_conditions", [])
        if blockers:
            lines.extend(f"- {item}" for item in blockers)
        else:
            lines.append("- None")
        lines.extend(["", "## Recommendations", ""])
        recommendations = result.get("recommendations", [])
        if recommendations:
            lines.extend(f"- `{item['area']}`: {item['action']}" for item in recommendations)
        else:
            lines.append("- None")
        return "\n".join(lines) + "\n"
