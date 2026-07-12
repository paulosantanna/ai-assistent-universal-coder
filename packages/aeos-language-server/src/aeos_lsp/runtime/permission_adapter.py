from __future__ import annotations

import logging
from typing import Any

from aeos_lsp.runtime.ports import PermissionCheck, PermissionPort

logger = logging.getLogger(__name__)


class PermissionAdapter(PermissionPort):
    def __init__(self) -> None:
        self._initialized = False
        self._grants: dict[tuple[str, str, str], float] = {}

    async def initialize(self, config: dict[str, Any] | None = None) -> None:
        self._initialized = True
        logger.info("Permission adapter initialized")

    async def shutdown(self) -> None:
        self._initialized = False
        self._grants.clear()
        logger.info("Permission adapter shut down")

    async def check_permission(
        self,
        agent_id: str,
        scope: str,
        capability: str,
        resource: str = "",
    ) -> PermissionCheck:
        if not self._initialized:
            return PermissionCheck(allowed=False, reason="Adapter not initialized")

        key = (agent_id, scope, capability)
        expiry = self._grants.get(key)
        if expiry is not None:
            import time
            if time.monotonic() < expiry:
                return PermissionCheck(
                    allowed=True,
                    scope=scope,
                    capability=capability,
                )

        return PermissionCheck(
            allowed=False,
            scope=scope,
            capability=capability,
            reason=f"Agent '{agent_id}' lacks permission for '{capability}' in scope '{scope}'",
        )

    async def grant_permission(
        self,
        agent_id: str,
        scope: str,
        capability: str,
        ttl_seconds: int | None = None,
    ) -> bool:
        import time
        expiry = time.monotonic() + (ttl_seconds if ttl_seconds else 3600)
        self._grants[(agent_id, scope, capability)] = expiry
        logger.info("Granted %s/%s to %s (TTL=%s)", scope, capability, agent_id, ttl_seconds)
        return True

    async def revoke_permission(
        self,
        agent_id: str,
        scope: str,
        capability: str,
    ) -> bool:
        key = (agent_id, scope, capability)
        if key in self._grants:
            del self._grants[key]
            logger.info("Revoked %s/%s from %s", scope, capability, agent_id)
            return True
        return False

    async def list_permissions(self, agent_id: str) -> list[PermissionCheck]:
        results: list[PermissionCheck] = []
        import time
        now = time.monotonic()
        for (aid, scope, capability), expiry in list(self._grants.items()):
            if aid == agent_id:
                results.append(PermissionCheck(
                    allowed=now < expiry,
                    scope=scope,
                    capability=capability,
                ))
        return results

    async def health_check(self) -> dict[str, Any]:
        return {
            "status": "ok" if self._initialized else "not_initialized",
            "active_grants": len(self._grants),
        }
