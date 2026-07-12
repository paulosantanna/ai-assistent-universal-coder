from __future__ import annotations

import json
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Optional
from uuid import uuid4

from aeos.core.readiness.readiness_models import (
    ReadinessResult,
    READINESS_PASS,
    READINESS_BLOCKED,
    READINESS_REVIEW,
    READINESS_ERROR,
)
from aeos.core.readiness.readiness_auditor import ReadinessAuditor


HEALTH_STARTUP_OK = "STARTUP_OK"
HEALTH_STARTUP_DEGRADED = "STARTUP_DEGRADED"
HEALTH_STARTUP_FAILED = "STARTUP_FAILED"
HEALTH_READY = "READY"
HEALTH_NOT_READY = "NOT_READY"
HEALTH_DEGRADED = "DEGRADED"


@dataclass
class HealthStatus:
    status: str
    service: str = "aeos"
    version: str = "1.0.0"
    checks: dict[str, Any] = field(default_factory=dict)
    timestamp: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "status": self.status,
            "service": self.service,
            "version": self.version,
            "checks": self.checks,
            "timestamp": self.timestamp or datetime.now(timezone.utc).isoformat(),
        }


class HealthService:
    def __init__(self, workspace_root: str = "."):
        self.workspace_root = workspace_root
        self._auditor = ReadinessAuditor(workspace_root=workspace_root)

    def startup(self) -> HealthStatus:
        checks = {
            "core_modules": self._check_core_modules(),
            "config_present": self._check_config(),
        }
        all_ok = all(c.get("ok", False) for c in checks.values())
        return HealthStatus(
            status=HEALTH_STARTUP_OK if all_ok else HEALTH_STARTUP_DEGRADED,
            checks=checks,
            timestamp=datetime.now(timezone.utc).isoformat(),
        )

    def readiness_shallow(self, skip_llm: bool = False) -> HealthStatus:
        result = self._auditor.audit()
        checks: dict[str, Any] = {
            "overall_score": result.overall_score,
            "status": result.status,
            "critical_blockers": len(result.critical_blockers),
        }
        if not skip_llm:
            llm_checks = self._check_llm()
            checks["llm"] = llm_checks

        status = HEALTH_READY
        if result.status == READINESS_BLOCKED:
            status = HEALTH_NOT_READY
        elif result.status == READINESS_REVIEW:
            status = HEALTH_DEGRADED

        return HealthStatus(
            status=status,
            checks=checks,
            timestamp=datetime.now(timezone.utc).isoformat(),
        )

    def _check_core_modules(self) -> dict[str, Any]:
        from pathlib import Path
        root = Path(self.workspace_root)
        core = root / "aeos" / "core"
        modules = ["runtime", "judge", "evals", "readiness", "skill_engine", "tool_router"]
        present = [m for m in modules if (core / m).is_dir()]
        return {"ok": len(present) == len(modules), "modules_present": len(present), "modules_total": len(modules)}

    def _check_config(self) -> dict[str, Any]:
        from pathlib import Path
        config = Path(self.workspace_root) / "aeos" / "config"
        expected = ["aeos.config.yaml", "permissions.yaml", "policies.yaml"]
        found = [f for f in expected if (config / f).exists()]
        return {"ok": len(found) == len(expected), "configs_found": len(found), "configs_expected": len(expected)}

    def _check_llm(self) -> dict[str, Any]:
        return {"available": False, "note": "LLM check not implemented in shallow mode"}
