from __future__ import annotations

import logging
import os
import threading
import time
from collections import defaultdict
from typing import Any

from aeos_lsp.telemetry.metrics import MetricsCollector

logger = logging.getLogger(__name__)


_MEMORY_CHECK_INTERVAL = 60.0


class PerformanceMonitor:
    def __init__(
        self,
        metrics_collector: MetricsCollector | None = None,
        enable_memory_monitoring: bool = True,
        memory_check_interval: float = _MEMORY_CHECK_INTERVAL,
    ) -> None:
        self._metrics = metrics_collector or MetricsCollector()
        self._enable_memory = enable_memory_monitoring
        self._memory_interval = memory_check_interval
        self._lock = threading.RLock()
        self._operation_stats: dict[str, dict[str, Any]] = defaultdict(lambda: {
            "count": 0, "total_time": 0.0, "min_time": float("inf"),
            "max_time": 0.0, "errors": 0,
        })
        self._background_thread: threading.Thread | None = None
        self._cancel_flag = threading.Event()

    @property
    def metrics(self) -> MetricsCollector:
        return self._metrics

    def start(self) -> None:
        if self._enable_memory and self._background_thread is None:
            self._cancel_flag.clear()
            self._background_thread = threading.Thread(
                target=self._memory_monitor_loop,
                name="aeos-perf-monitor",
                daemon=True,
            )
            self._background_thread.start()
            logger.info("Performance monitor started")

    def stop(self) -> None:
        self._cancel_flag.set()
        if self._background_thread is not None:
            self._background_thread.join(timeout=5)
            self._background_thread = None
        logger.info("Performance monitor stopped")

    def record_operation(
        self,
        operation: str,
        duration: float,
        error: bool = False,
    ) -> None:
        with self._lock:
            stats = self._operation_stats[operation]
            stats["count"] += 1
            stats["total_time"] += duration
            stats["min_time"] = min(stats["min_time"], duration)
            stats["max_time"] = max(stats["max_time"], duration)
            if error:
                stats["errors"] += 1

        self._metrics.increment(f"operation.{operation}.count")
        self._metrics.timing(f"operation.{operation}.duration", duration)
        if error:
            self._metrics.increment(f"operation.{operation}.errors")

    def instrument(self, operation: str) -> _OperationTimer:
        return _OperationTimer(self, operation)

    def get_operation_stats(self, operation: str) -> dict[str, Any] | None:
        with self._lock:
            stats = self._operation_stats.get(operation)
            if stats is None:
                return None
            count = stats["count"]
            if count == 0:
                return None
            return {
                "operation": operation,
                "count": count,
                "total_time_seconds": round(stats["total_time"], 4),
                "avg_time_seconds": round(stats["total_time"] / count, 4),
                "min_time_seconds": round(stats["min_time"], 4),
                "max_time_seconds": round(stats["max_time"], 4),
                "error_count": stats["errors"],
                "error_rate": round(stats["errors"] / count, 4),
            }

    def get_all_stats(self) -> dict[str, Any]:
        with self._lock:
            return {
                op: self.get_operation_stats(op)
                for op in self._operation_stats
            }

    def get_memory_usage(self) -> dict[str, Any]:
        try:
            import psutil
            process = psutil.Process(os.getpid())
            mem_info = process.memory_info()
            return {
                "rss_bytes": mem_info.rss,
                "rss_mb": round(mem_info.rss / (1024 * 1024), 2),
                "vms_bytes": mem_info.vms,
                "vms_mb": round(mem_info.vms / (1024 * 1024), 2),
                "percent": process.memory_percent(),
            }
        except ImportError:
            import gc
            return {
                "rss_bytes": 0,
                "rss_mb": 0.0,
                "note": "psutil not available, using gc stats",
                "gc_objects": len(gc.get_objects()),
            }

    def get_cpu_usage(self) -> dict[str, Any]:
        try:
            import psutil
            process = psutil.Process(os.getpid())
            return {
                "cpu_percent": process.cpu_percent(interval=0.1),
                "num_threads": process.num_threads(),
                "cpu_times": {
                    "user": process.cpu_times().user,
                    "system": process.cpu_times().system,
                },
            }
        except ImportError:
            return {"note": "psutil not available"}

    def snapshot(self) -> dict[str, Any]:
        return {
            "operations": self.get_all_stats(),
            "memory": self.get_memory_usage(),
            "cpu": self.get_cpu_usage(),
            "metrics": self._metrics.snapshot(),
        }

    def _memory_monitor_loop(self) -> None:
        while not self._cancel_flag.is_set():
            try:
                mem = self.get_memory_usage()
                rss_mb = mem.get("rss_mb", 0.0)
                self._metrics.gauge("memory.rss_mb", rss_mb)
                logger.debug("Memory usage: %.1f MB", rss_mb)
            except Exception:
                logger.exception("Memory monitor error")
            self._cancel_flag.wait(self._memory_interval)


class _OperationTimer:
    def __init__(self, monitor: PerformanceMonitor, operation: str) -> None:
        self._monitor = monitor
        self._operation = operation
        self._start: float = 0.0
        self._error: bool = False

    def __enter__(self) -> _OperationTimer:
        self._start = time.monotonic()
        return self

    def __exit__(self, *args: Any) -> None:
        duration = time.monotonic() - self._start
        error = args[0] is not None
        self._monitor.record_operation(self._operation, duration, error=error)
