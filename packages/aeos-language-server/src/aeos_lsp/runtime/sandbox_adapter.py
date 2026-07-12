from __future__ import annotations

import logging
import os
import tempfile
import time
import uuid
from pathlib import Path
from typing import Any

from aeos_lsp.runtime.ports import ExecutionResult, SandboxPort

logger = logging.getLogger(__name__)


class SandboxAdapter(SandboxPort):
    def __init__(self, base_dir: str | Path | None = None) -> None:
        self._initialized = False
        self._sandboxes: dict[str, dict[str, Any]] = {}
        self._base_dir = Path(base_dir) if base_dir else Path(tempfile.gettempdir()) / "aeos-sandboxes"

    async def initialize(self, config: dict[str, Any] | None = None) -> None:
        self._initialized = True
        self._base_dir.mkdir(parents=True, exist_ok=True)
        if config and "base_dir" in config:
            self._base_dir = Path(config["base_dir"])
            self._base_dir.mkdir(parents=True, exist_ok=True)
        logger.info("Sandbox adapter initialized (base_dir=%s)", self._base_dir)

    async def shutdown(self) -> None:
        self._initialized = False
        for sandbox_id in list(self._sandboxes.keys()):
            await self.destroy(sandbox_id)
        logger.info("Sandbox adapter shut down")

    async def create(self, name: str, config: dict[str, Any] | None = None) -> str:
        sandbox_id = f"sandbox-{uuid.uuid4().hex[:12]}"
        sandbox_dir = self._base_dir / sandbox_id
        sandbox_dir.mkdir(parents=True, exist_ok=True)

        self._sandboxes[sandbox_id] = {
            "id": sandbox_id,
            "name": name,
            "path": str(sandbox_dir),
            "created": time.monotonic(),
            "config": config or {},
            "active": True,
        }

        logger.info("Created sandbox: %s (%s)", sandbox_id, name)
        return sandbox_id

    async def destroy(self, sandbox_id: str) -> bool:
        sandbox = self._sandboxes.pop(sandbox_id, None)
        if sandbox is None:
            return False

        sandbox_path = Path(sandbox["path"])
        if sandbox_path.is_dir():
            import shutil
            try:
                shutil.rmtree(sandbox_path)
            except OSError as exc:
                logger.warning("Failed to remove sandbox directory %s: %s", sandbox_path, exc)

        logger.info("Destroyed sandbox: %s", sandbox_id)
        return True

    async def execute_in_sandbox(
        self,
        sandbox_id: str,
        command: str,
        timeout: float | None = None,
    ) -> ExecutionResult:
        sandbox = self._sandboxes.get(sandbox_id)
        if sandbox is None:
            return ExecutionResult(
                success=False,
                error=f"Sandbox '{sandbox_id}' not found",
            )

        start = time.monotonic()
        sandbox_path = sandbox["path"]

        try:
            from aeos_lsp.runtime.subprocess_adapter import SubprocessAdapter
            sub = SubprocessAdapter()
            result = sub.run(
                command=command,
                cwd=sandbox_path,
                timeout=timeout or 30.0,
                env={
                    "SANDBOX_ID": sandbox_id,
                    "SANDBOX_PATH": sandbox_path,
                },
            )

            elapsed = time.monotonic() - start
            return ExecutionResult(
                success=result["returncode"] == 0,
                output=result.get("stdout", ""),
                error=result.get("stderr", "") if result["returncode"] != 0 else None,
                elapsed_seconds=elapsed,
                metadata={
                    "sandbox_id": sandbox_id,
                    "returncode": result["returncode"],
                },
            )
        except Exception as exc:
            elapsed = time.monotonic() - start
            return ExecutionResult(
                success=False,
                error=str(exc),
                elapsed_seconds=elapsed,
            )

    async def list_sandboxes(self) -> list[dict[str, Any]]:
        return [
            {
                "id": s["id"],
                "name": s["name"],
                "path": s["path"],
                "active": s["active"],
                "created": s["created"],
            }
            for s in self._sandboxes.values()
        ]

    async def sandbox_health(self, sandbox_id: str) -> dict[str, Any]:
        sandbox = self._sandboxes.get(sandbox_id)
        if sandbox is None:
            return {"status": "not_found"}

        sandbox_path = Path(sandbox["path"])
        return {
            "status": "ok" if sandbox_path.is_dir() else "missing",
            "id": sandbox_id,
            "name": sandbox["name"],
            "path_exists": sandbox_path.is_dir(),
        }

    async def health_check(self) -> dict[str, Any]:
        return {
            "status": "ok" if self._initialized else "not_initialized",
            "active_sandboxes": len(self._sandboxes),
            "base_dir": str(self._base_dir),
        }
