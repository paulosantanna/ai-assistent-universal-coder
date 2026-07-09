from __future__ import annotations

from pathlib import Path
from typing import Any, Optional

from aeos.core.runtime.runtime_models import generate_execution_id, now_iso


class ExecutionContext:
    def __init__(self, workspace_root: str = ".", aeos_root: Optional[str] = None, target_path: Optional[str] = None):
        self.workspace_root = Path(workspace_root).resolve()
        self.aeos_root = Path(aeos_root).resolve() if aeos_root else self.workspace_root
        self.target_path = Path(target_path).resolve() if target_path else self.workspace_root
        self.execution_id = generate_execution_id()
        self.created_at = now_iso()
        self._metadata: dict[str, Any] = {}
        self._sandbox_dir: Optional[Path] = None

    def create_sandbox(self) -> Path:
        sandbox = self.workspace_root / ".aeos" / "sandbox" / self.execution_id
        sandbox.mkdir(parents=True, exist_ok=True)
        self._sandbox_dir = sandbox
        return sandbox

    def ensure_dirs(self) -> dict[str, Path]:
        evidence_dir = self.workspace_root / ".aeos" / "evidence" / self.execution_id
        report_dir = self.workspace_root / ".aeos" / "reports" / self.execution_id
        sandbox_dir = self.workspace_root / ".aeos" / "sandbox" / self.execution_id

        evidence_dir.mkdir(parents=True, exist_ok=True)
        report_dir.mkdir(parents=True, exist_ok=True)
        sandbox_dir.mkdir(parents=True, exist_ok=True)

        return {
            "evidence": evidence_dir,
            "reports": report_dir,
            "sandbox": sandbox_dir,
        }

    def set_metadata(self, key: str, value: Any) -> None:
        self._metadata[key] = value

    def get_metadata(self, key: str, default: Any = None) -> Any:
        return self._metadata.get(key, default)

    def to_dict(self) -> dict[str, Any]:
        return {
            "execution_id": self.execution_id,
            "created_at": self.created_at,
            "workspace_root": str(self.workspace_root),
            "aeos_root": str(self.aeos_root),
            "target_path": str(self.target_path),
            "metadata": self._metadata,
        }
