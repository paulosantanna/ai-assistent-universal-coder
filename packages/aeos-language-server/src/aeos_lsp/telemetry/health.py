from __future__ import annotations

import logging
import os
import time
from typing import Any

from aeos_lsp.telemetry.metrics import MetricsCollector
from aeos_lsp.telemetry.performance import PerformanceMonitor

logger = logging.getLogger(__name__)


class HealthCheck:
    def __init__(
        self,
        performance_monitor: PerformanceMonitor | None = None,
        metrics_collector: MetricsCollector | None = None,
    ) -> None:
        self._perf = performance_monitor
        self._metrics = metrics_collector or MetricsCollector()
        self._server: Any = None
        self._start_time = time.monotonic()

    def bind_server(self, server: Any) -> None:
        self._server = server

    def check_server(self) -> dict[str, Any]:
        status = "ok"
        issues: list[str] = []

        if self._server is None:
            return {"status": "not_initialized", "issues": ["Server not bound to health check"]}

        server_initialized = getattr(self._server, "initialized", None)
        if server_initialized is not None and not server_initialized:
            status = "degraded"
            issues.append("Server not fully initialized")

        return {
            "status": status,
            "issues": issues,
            "uptime_seconds": round(time.monotonic() - self._start_time, 2),
            "version": getattr(self._server, "version", "unknown"),
        }

    def check_index(self) -> dict[str, Any]:
        if self._server is None:
            return {"status": "not_available", "issues": ["Server not available"]}

        indexer = getattr(self._server, "indexer", None)
        if indexer is None:
            return {"status": "not_available", "issues": ["Indexer not available"]}

        try:
            indexed = indexer.get_indexed_count()
            failed = indexer.get_failed_count()
            total = indexed + failed

            status = "ok"
            issues: list[str] = []
            if failed > 0:
                status = "degraded"
                issues.append(f"{failed} documents failed to index")
            if indexed == 0 and total == 0:
                status = "empty"
                issues.append("No documents indexed yet")

            return {
                "status": status,
                "indexed_count": indexed,
                "failed_count": failed,
                "total_count": total,
                "issues": issues,
            }
        except Exception as exc:
            return {"status": "error", "error": str(exc)}

    def check_memory(self) -> dict[str, Any]:
        try:
            import psutil
            process = psutil.Process(os.getpid())
            mem = process.memory_info()
            rss_mb = mem.rss / (1024 * 1024)
            vms_mb = mem.vms / (1024 * 1024)
            percent = process.memory_percent()

            status = "ok"
            issues: list[str] = []
            if rss_mb > 1024:
                status = "degraded"
                issues.append(f"Memory usage high: {rss_mb:.0f} MB")
            if percent > 80:
                status = "degraded"
                issues.append(f"Memory percent high: {percent:.1f}%")

            return {
                "status": status,
                "rss_mb": round(rss_mb, 2),
                "vms_mb": round(vms_mb, 2),
                "percent": round(percent, 1),
                "issues": issues,
            }
        except ImportError:
            return {
                "status": "ok",
                "rss_mb": 0.0,
                "vms_mb": 0.0,
                "note": "psutil not available, memory monitoring disabled",
            }
        except Exception as exc:
            return {"status": "error", "error": str(exc)}

    def check_runtime(self) -> dict[str, Any]:
        if self._server is None:
            return {"status": "not_available", "issues": ["Server not available"]}

        runtime = getattr(self._server, "runtime_adapter", None)
        if runtime is None:
            return {"status": "not_available", "issues": ["Runtime adapter not available"]}

        try:
            health = runtime.health_check()
            if hasattr(health, "__await__"):
                import asyncio
                try:
                    loop = asyncio.get_event_loop()
                    if loop.is_running():
                        health = {"status": "ok", "note": "async health check deferred"}
                    else:
                        health = loop.run_until_complete(health)
                except RuntimeError:
                    health = {"status": "ok", "note": "async health check deferred"}

            return {
                "status": health.get("status", "unknown"),
                "runtime": health,
            }
        except Exception as exc:
            return {"status": "error", "error": str(exc)}

    def check_workspace(self) -> dict[str, Any]:
        if self._server is None:
            return {"status": "not_available", "issues": ["Server not available"]}

        workspace = getattr(self._server, "workspace_manager", None)
        if workspace is None:
            return {"status": "not_available", "issues": ["Workspace manager not available"]}

        try:
            folder_count = len(workspace.workspace_folders) if hasattr(workspace, "workspace_folders") else 0
            doc_count = workspace.document_store.count() if hasattr(workspace, "document_store") and hasattr(workspace.document_store, "count") else 0
            aeos_root = getattr(workspace, "aeos_root", None)

            return {
                "status": "ok",
                "folder_count": folder_count,
                "document_count": doc_count,
                "has_aeos_root": aeos_root is not None,
                "aeos_root": str(aeos_root) if aeos_root else None,
            }
        except Exception as exc:
            return {"status": "error", "error": str(exc)}

    def full_health_report(self) -> dict[str, Any]:
        return {
            "server": self.check_server(),
            "index": self.check_index(),
            "memory": self.check_memory(),
            "runtime": self.check_runtime(),
            "workspace": self.check_workspace(),
            "overall_status": self._overall_status(),
        }

    def _overall_status(self) -> str:
        server_check = self.check_server()
        if server_check.get("status") == "error":
            return "error"

        index_check = self.check_index()
        if index_check.get("status") == "error":
            return "error"

        memory_check = self.check_memory()
        if memory_check.get("status") == "error":
            return "error"

        statuses = [
            server_check.get("status", "ok"),
            index_check.get("status", "ok"),
            memory_check.get("status", "ok"),
        ]

        if any(s == "degraded" for s in statuses):
            return "degraded"
        if any(s == "empty" for s in statuses):
            return "degraded"
        if all(s == "ok" for s in statuses):
            return "ok"
        return "unknown"

    def __repr__(self) -> str:
        return f"HealthCheck(uptime={round(time.monotonic() - self._start_time, 0)}s)"
