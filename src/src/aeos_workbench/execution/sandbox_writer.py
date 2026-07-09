"""Sandbox Writer — all writes go to .aeos/sandbox/{execution_id}/."""

from pathlib import Path
from typing import Optional


class SandboxWriter:
    def __init__(self, workspace_root: Path, execution_id: str):
        self.workspace_root = workspace_root.resolve()
        self.execution_id = execution_id
        self.sandbox_dir = self.workspace_root / ".aeos" / "sandbox" / execution_id
        self.written_files: list[Path] = []

    def resolve_path(self, relative_path: str) -> Path:
        return (self.sandbox_dir / relative_path).resolve()

    def write(self, relative_path: str, content: str) -> Path:
        abs_path = self.resolve_path(relative_path)
        abs_path.parent.mkdir(parents=True, exist_ok=True)
        abs_path.write_text(content, encoding="utf-8")
        self.written_files.append(abs_path)
        return abs_path

    def is_within_sandbox(self, target_path: Path) -> bool:
        try:
            target_path.resolve().relative_to(self.sandbox_dir.resolve())
            return True
        except ValueError:
            return False

    def is_within_allowed_aeos(self, target_path: Path) -> bool:
        allowed = self.workspace_root / ".aeos"
        try:
            target_path.resolve().relative_to(allowed.resolve())
            return True
        except ValueError:
            return False

    def validate_write_target(self, target_path: Path) -> None:
        resolved = target_path.resolve()
        if not self.is_within_sandbox(resolved) and not self.is_within_allowed_aeos(resolved):
            raise PermissionError(
                f"Write target {resolved} is outside sandbox and .aeos directory. "
                f"All writes must be within .aeos/sandbox/{self.execution_id}/ "
                f"or .aeos/ (evidence, reports, approvals). "
                f"Writing outside requires explicit approval via ApprovalGateway."
            )

    def get_all_written(self) -> list[Path]:
        return list(self.written_files)