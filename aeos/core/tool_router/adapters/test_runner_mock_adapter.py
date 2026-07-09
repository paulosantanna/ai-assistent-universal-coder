from __future__ import annotations

from typing import Any

from aeos.core.tool_router.adapters.base_adapter import BaseToolAdapter


class TestRunnerMockAdapter(BaseToolAdapter):
    tool_id = "test-runner-controlled"

    def execute(self, action: str, resource: str, input_data: dict[str, Any]) -> dict[str, Any]:
        if action == "test.detect":
            return {
                "detected": True,
                "framework": "pytest",
                "note": "Real test execution is disabled in this phase. Use direct pytest instead.",
            }
        elif action == "test.run_allowlisted":
            return {
                "executed": False,
                "note": "Real test execution via Tool Router is disabled in this phase. Use 'py -m pytest ...' directly.",
            }
        else:
            return {"error": f"Unknown action '{action}' for test-runner-controlled adapter"}
