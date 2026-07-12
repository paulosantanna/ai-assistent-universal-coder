from __future__ import annotations

import logging
import threading
import time
from collections import defaultdict
from typing import Any

logger = logging.getLogger(__name__)


class MetricsCollector:
    def __init__(self) -> None:
        self._lock = threading.RLock()
        self._counters: dict[str, int] = defaultdict(int)
        self._timings: dict[str, list[float]] = defaultdict(list)
        self._gauges: dict[str, float] = {}
        self._histograms: dict[str, list[float]] = defaultdict(list)
        self._start_time = time.monotonic()

    def increment(self, metric: str, value: int = 1) -> None:
        with self._lock:
            self._counters[metric] += value

    def decrement(self, metric: str, value: int = 1) -> None:
        with self._lock:
            self._counters[metric] -= value

    def gauge(self, metric: str, value: float) -> None:
        with self._lock:
            self._gauges[metric] = value

    def timing(self, metric: str, duration: float) -> None:
        with self._lock:
            self._timings[metric].append(duration)

    def record_time(self, metric: str) -> _TimerContext:
        return _TimerContext(self, metric)

    def observe(self, metric: str, value: float) -> None:
        with self._lock:
            self._histograms[metric].append(value)

    def get_counter(self, metric: str) -> int:
        with self._lock:
            return self._counters.get(metric, 0)

    def get_timing_stats(self, metric: str) -> dict[str, float] | None:
        with self._lock:
            values = self._timings.get(metric)
            if not values:
                return None
            n = len(values)
            sorted_vals = sorted(values)
            mean = sum(values) / n
            variance = sum((v - mean) ** 2 for v in values) / n if n > 1 else 0.0
            return {
                "count": n,
                "mean": round(mean, 4),
                "min": round(sorted_vals[0], 4),
                "max": round(sorted_vals[-1], 4),
                "median": round(sorted_vals[n // 2], 4),
                "p95": round(sorted_vals[int(n * 0.95)], 4),
                "p99": round(sorted_vals[int(n * 0.99)], 4),
                "stddev": round(math.sqrt(variance), 4),
            }

    def get_gauge(self, metric: str) -> float | None:
        with self._lock:
            return self._gauges.get(metric)

    def snapshot(self) -> dict[str, Any]:
        with self._lock:
            uptime = time.monotonic() - self._start_time
            timing_snapshots: dict[str, dict[str, float]] = {}
            for metric_key in self._timings:
                stats = self.get_timing_stats(metric_key)
                if stats is not None:
                    timing_snapshots[metric_key] = stats

            histogram_snapshots: dict[str, dict[str, Any]] = {}
            for metric_key, values in self._histograms.items():
                if values:
                    n = len(values)
                    sorted_vals = sorted(values)
                    histogram_snapshots[metric_key] = {
                        "count": n,
                        "min": round(sorted_vals[0], 4),
                        "max": round(sorted_vals[-1], 4),
                        "mean": round(sum(values) / n, 4),
                    }

            return {
                "uptime_seconds": round(uptime, 2),
                "counters": dict(self._counters),
                "gauges": dict(self._gauges),
                "timings": timing_snapshots,
                "histograms": histogram_snapshots,
            }

    def reset(self) -> None:
        with self._lock:
            self._counters.clear()
            self._timings.clear()
            self._gauges.clear()
            self._histograms.clear()
            self._start_time = time.monotonic()

    def get_all_metrics(self) -> dict[str, Any]:
        return self.snapshot()


import math


class _TimerContext:
    def __init__(self, collector: MetricsCollector, metric: str) -> None:
        self._collector = collector
        self._metric = metric
        self._start: float = 0.0

    def __enter__(self) -> _TimerContext:
        self._start = time.monotonic()
        return self

    def __exit__(self, *args: Any) -> None:
        duration = time.monotonic() - self._start
        self._collector.timing(self._metric, duration)
