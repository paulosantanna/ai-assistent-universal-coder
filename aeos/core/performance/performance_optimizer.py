from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class PerformanceSignal:
    name: str
    actual_seconds: float
    p50_seconds: float
    p95_seconds: float
    category: str

    def status(self) -> str:
        if self.actual_seconds > self.p95_seconds:
            return "BREACHED"
        if self.actual_seconds > self.p50_seconds:
            return "WARN"
        return "PASS"

    def to_dict(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "actual_seconds": self.actual_seconds,
            "p50_seconds": self.p50_seconds,
            "p95_seconds": self.p95_seconds,
            "category": self.category,
            "status": self.status(),
        }


class PerformanceOptimizer:
    """Create bounded optimization plans from measured hot-path signals."""

    def plan(self, signals: list[PerformanceSignal]) -> dict[str, Any]:
        findings = [signal.to_dict() for signal in signals]
        breached = [signal for signal in signals if signal.status() == "BREACHED"]
        warnings = [signal for signal in signals if signal.status() == "WARN"]
        recommendations = self._recommendations(signals)
        status = "BREACHED" if breached else "WARN" if warnings else "PASS"

        return {
            "status": status,
            "signals": findings,
            "summary": {
                "total": len(signals),
                "passed": len([signal for signal in signals if signal.status() == "PASS"]),
                "warnings": len(warnings),
                "breached": len(breached),
            },
            "recommendations": recommendations,
            "blocking_conditions": [
                f"{signal.name}: p95 budget exceeded" for signal in breached
            ],
        }

    def _recommendations(self, signals: list[PerformanceSignal]) -> list[dict[str, str]]:
        recommendations: list[dict[str, str]] = []
        categories = {signal.category for signal in signals if signal.status() != "PASS"}
        if "registry" in categories:
            recommendations.append({
                "area": "registry",
                "action": "Reuse fingerprinted registry caches and avoid repeated YAML parsing.",
            })
        if "scanner" in categories:
            recommendations.append({
                "area": "scanner",
                "action": "Prune ignored directories before file-level scanning and inspect large files as metadata.",
            })
        if "evidence" in categories:
            recommendations.append({
                "area": "evidence",
                "action": "Batch evidence writes and flush hash-chain metadata once per logical batch.",
            })
        if "runtime" in categories:
            recommendations.append({
                "area": "runtime",
                "action": "Cache parsed config and index registry arrays by id in memory.",
            })
        return recommendations
