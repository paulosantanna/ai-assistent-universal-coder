from __future__ import annotations

import logging
from typing import Any

from aeos_lsp.runtime.ports import AeosRuntimePort, ExecutionRequest, ExecutionResult

logger = logging.getLogger(__name__)


class AeosRuntimeAdapter(AeosRuntimePort):
    def __init__(self) -> None:
        self._initialized = False
        self._config: dict[str, Any] = {}
        self._adapters: dict[str, Any] = {}

    def register_adapter(self, name: str, adapter: Any) -> None:
        self._adapters[name] = adapter
        logger.debug("Registered runtime adapter: %s", name)

    def get_adapter(self, name: str) -> Any | None:
        return self._adapters.get(name)

    async def initialize(self, config: dict[str, Any] | None = None) -> None:
        if self._initialized:
            logger.warning("Runtime already initialized")
            return
        self._config = config or {}
        self._initialized = True
        logger.info("AEOS runtime adapter initialized")

    async def shutdown(self) -> None:
        self._initialized = False
        for name, adapter in self._adapters.items():
            if hasattr(adapter, "shutdown") and callable(adapter.shutdown):
                try:
                    await adapter.shutdown() if hasattr(adapter.shutdown, "__await__") else adapter.shutdown()
                except Exception:
                    logger.exception("Failed to shutdown adapter: %s", name)
        self._adapters.clear()
        logger.info("AEOS runtime adapter shut down")

    async def health_check(self) -> dict[str, Any]:
        statuses: dict[str, Any] = {"runtime": "ok", "initialized": self._initialized}
        for name, adapter in self._adapters.items():
            if hasattr(adapter, "health_check") and callable(adapter.health_check):
                try:
                    result = adapter.health_check()
                    if hasattr(result, "__await__"):
                        result = await result
                    statuses[name] = result
                except Exception as exc:
                    statuses[name] = {"status": "error", "error": str(exc)}
        return statuses

    async def execute_request(self, request: ExecutionRequest) -> ExecutionResult:
        if not self._initialized:
            return ExecutionResult(
                success=False,
                error="Runtime not initialized",
            )

        if request.skill_id:
            adapter = self._adapters.get("skill")
            if adapter is None:
                return ExecutionResult(success=False, error="Skill adapter not available")
            skill_def = await adapter.resolve(request.skill_id)
            if skill_def is None:
                return ExecutionResult(success=False, error=f"Skill '{request.skill_id}' not found")
            return await adapter.execute(skill_def, request.inputs, request.context)

        if request.playbook_id:
            adapter = self._adapters.get("playbook")
            if adapter is None:
                return ExecutionResult(success=False, error="Playbook adapter not available")
            pb_def = await adapter.resolve(request.playbook_id)
            if pb_def is None:
                return ExecutionResult(success=False, error=f"Playbook '{request.playbook_id}' not found")
            return await adapter.execute(pb_def, request.inputs, request.context)

        return ExecutionResult(success=False, error="No executable target specified")
