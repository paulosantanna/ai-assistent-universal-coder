from __future__ import annotations

import sys
import os
import json

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..")))

from aeos.core.health.health_service import (
    HealthService,
    HEALTH_STARTUP_OK,
    HEALTH_STARTUP_DEGRADED,
    HEALTH_READY,
    HEALTH_NOT_READY,
    HEALTH_DEGRADED,
)


class TestHealthEndpointSmoke:
    def setup_method(self):
        self.service = HealthService(workspace_root=".")

    def test_health_startup(self):
        status = self.service.startup()
        data = status.to_dict()
        assert "status" in data
        assert data["status"] in (HEALTH_STARTUP_OK, HEALTH_STARTUP_DEGRADED)
        assert "checks" in data
        assert "core_modules" in data["checks"]
        assert "config_present" in data["checks"]
        assert "timestamp" in data

    def test_health_ready_shallow(self):
        status = self.service.readiness_shallow()
        data = status.to_dict()
        assert data["status"] in (HEALTH_READY, HEALTH_NOT_READY, HEALTH_DEGRADED)
        assert "checks" in data
        assert "overall_score" in data["checks"]
        assert "status" in data["checks"]
        assert "critical_blockers" in data["checks"]
        assert "timestamp" in data

    def test_health_shallow_skips_llm(self):
        status = self.service.readiness_shallow(skip_llm=True)
        data = status.to_dict()
        assert "llm" not in data["checks"]
        assert data["status"] in (HEALTH_READY, HEALTH_NOT_READY, HEALTH_DEGRADED)
