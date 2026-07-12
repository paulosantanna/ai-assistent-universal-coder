"""Reporting and aggregation for token budget management."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional


class TokenReporter:
    """Aggregates token usage data and generates reports."""

    def __init__(self):
        self._phase_reports: List[Dict[str, Any]] = []
        self._current_phase: str = ""

    def reset(self) -> None:
        self._current_phase = ""
        self._phase_reports.clear()

    def record_phase(self, phase: str, status: Dict[str, Any]) -> None:
        self._current_phase = phase
        entry = {
            "phase": phase,
            "timestamp_utc": datetime.now(tz=timezone.utc).isoformat(),
            "status": status,
        }
        self._phase_reports.append(entry)

    def summary(self) -> Dict[str, Any]:
        if not self._phase_reports:
            return {"phases": [], "total_tokens": 0, "cache_hits": 0, "cache_misses": 0}
        last = self._phase_reports[-1]
        subagents = last["status"].get("subagents", [])
        total_tokens = sum(s.get("consumed", 0) for s in subagents)
        total_hits = sum(s.get("cache_hits", 0) for s in subagents)
        total_misses = sum(s.get("cache_misses", 0) for s in subagents)
        ratios = [
            s.get("compression_ratio", 1.0)
            for s in subagents
            if s.get("compression_ratio", 1.0) < 1.0
        ]
        avg_ratio = round(sum(ratios) / len(ratios), 4) if ratios else 1.0
        return {
            "phase": self._current_phase,
            "total_tokens_consumed": total_tokens,
            "total_cache_hits": total_hits,
            "total_cache_misses": total_misses,
            "overall_compression_ratio": avg_ratio,
            "subagent_count": len(subagents),
        }

    def compression_report(self) -> Dict[str, Any]:
        if not self._phase_reports:
            return {"compression_by_subagent": []}
        last = self._phase_reports[-1]
        subagents = last["status"].get("subagents", [])
        report = []
        for s in subagents:
            if s.get("consumed", 0) > 0:
                report.append({
                    "subagent_id": s["subagent_id"],
                    "consumed": s["consumed"],
                    "budget": s["budget"],
                    "compression_ratio": s.get("compression_ratio", 1.0),
                    "budget_utilization_pct": s.get("utilization_pct", 0),
                })
        return {"compression_by_subagent": report}

    def cache_report(self) -> Dict[str, Any]:
        if not self._phase_reports:
            return {"cache_hits": 0, "cache_misses": 0, "hit_rate": 0.0}
        last = self._phase_reports[-1]
        subagents = last["status"].get("subagents", [])
        total_hits = sum(s.get("cache_hits", 0) for s in subagents)
        total_misses = sum(s.get("cache_misses", 0) for s in subagents)
        total = total_hits + total_misses
        hit_rate = round(total_hits / total, 4) if total > 0 else 0.0
        return {
            "cache_hits": total_hits,
            "cache_misses": total_misses,
            "hit_rate": hit_rate,
        }

    def top_consumers(self, n: int = 5) -> List[Dict[str, Any]]:
        if not self._phase_reports:
            return []
        last = self._phase_reports[-1]
        subagents = last["status"].get("subagents", [])
        sorted_sa = sorted(subagents, key=lambda s: s.get("consumed", 0), reverse=True)
        return [
            {
                "subagent_id": s["subagent_id"],
                "consumed": s["consumed"],
                "budget": s["budget"],
                "utilization_pct": s.get("utilization_pct", 0),
            }
            for s in sorted_sa[:n]
        ]

    def export(self, path: str) -> str:
        data = {
            "generated_at": datetime.now(tz=timezone.utc).isoformat(),
            "summary": self.summary(),
            "compression": self.compression_report(),
            "cache": self.cache_report(),
            "top_consumers": self.top_consumers(),
            "phase_reports": self._phase_reports,
        }
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        return path
