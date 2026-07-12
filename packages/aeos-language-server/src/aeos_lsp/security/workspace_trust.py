from __future__ import annotations

import logging
from enum import Enum
from typing import Any

logger = logging.getLogger(__name__)


class TrustMode(Enum):
    TRUSTED = "trusted"
    UNTRUSTED = "untrusted"
    ASK = "ask"


_BLOCKED_OPERATIONS: dict[TrustMode, set[str]] = {
    TrustMode.TRUSTED: set(),
    TrustMode.UNTRUSTED: {
        "execute_arbitrary_command",
        "access_network",
        "read_system_files",
        "write_system_files",
        "install_packages",
        "access_environment_variables",
        "access_credentials",
        "modify_git_config",
        "run_background_processes",
        "access_known_hosts",
        "access_ssh_keys",
        "modify_shell_config",
    },
    TrustMode.ASK: {
        "execute_arbitrary_command",
        "access_network",
        "read_system_files",
        "write_system_files",
        "install_packages",
        "access_environment_variables",
        "access_credentials",
        "modify_git_config",
        "run_background_processes",
        "access_known_hosts",
        "access_ssh_keys",
        "modify_shell_config",
    },
}

_TRUST_INDICATORS: dict[str, list[str]] = {
    "positive": [
        "Has known repository owner",
        "Has CI/CD configuration",
        "Has security policy file (SECURITY.md)",
        "Has code owners file",
        "Has dependency lock files",
        "Has code signing",
        "Has branch protection rules",
        "Has recent security audit",
        "Repository is verified by platform",
        "Has license file",
    ],
    "negative": [
        "No repository owner verification",
        "No security policy",
        "No branch protection",
        "No CI/CD pipeline",
        "Has unverified dependencies",
        "Recently created (less than 30 days)",
        "No code review process",
        "No license file",
        "Hidden or system files in workspace root",
        "Executable files in workspace root (suspicious)",
    ],
}


class WorkspaceTrust:
    def __init__(self, default_mode: TrustMode = TrustMode.ASK) -> None:
        self._mode = default_mode
        self._folders: dict[str, TrustMode] = {}
        self._trusted_folders: set[str] = set()

    @property
    def mode(self) -> TrustMode:
        return self._mode

    @mode.setter
    def mode(self, value: TrustMode) -> None:
        self._mode = value
        logger.info("Workspace trust mode set to: %s", value.value)

    def set_trust_mode(self, mode: str) -> None:
        try:
            self._mode = TrustMode(mode.lower())
            logger.info("Workspace trust mode set to: %s", self._mode.value)
        except ValueError:
            valid = ", ".join(t.value for t in TrustMode)
            raise ValueError(f"Invalid trust mode '{mode}'. Valid modes: {valid}")

    def is_operation_allowed(self, operation: str, folder_uri: str | None = None) -> bool:
        effective_mode = self._mode

        if folder_uri is not None:
            folder_mode = self._folders.get(folder_uri)
            if folder_mode is not None:
                effective_mode = folder_mode
            elif folder_uri in self._trusted_folders:
                effective_mode = TrustMode.TRUSTED

        blocked = _BLOCKED_OPERATIONS.get(effective_mode, set())
        return operation not in blocked

    def require_approval(self, operation: str, folder_uri: str | None = None) -> bool:
        effective_mode = self._mode
        if folder_uri is not None:
            folder_mode = self._folders.get(folder_uri)
            if folder_mode is not None:
                effective_mode = folder_mode
            elif folder_uri in self._trusted_folders:
                return False

        return effective_mode == TrustMode.ASK and operation in _BLOCKED_OPERATIONS.get(TrustMode.ASK, set())

    def trust_folder(self, folder_uri: str) -> None:
        self._trusted_folders.add(folder_uri)
        self._folders.pop(folder_uri, None)
        logger.info("Trusted folder: %s", folder_uri)

    def untrust_folder(self, folder_uri: str) -> None:
        self._trusted_folders.discard(folder_uri)
        logger.info("Untrusted folder: %s", folder_uri)

    def set_folder_mode(self, folder_uri: str, mode: TrustMode) -> None:
        self._folders[folder_uri] = mode
        logger.info("Set trust mode for folder %s to %s", folder_uri, mode.value)

    def is_folder_trusted(self, folder_uri: str) -> bool:
        mode = self._folders.get(folder_uri, self._mode)
        return mode == TrustMode.TRUSTED or folder_uri in self._trusted_folders

    def get_trust_indicators(self, folder_path: str | None = None) -> dict[str, list[str]]:
        return _TRUST_INDICATORS

    def get_blocked_operations(self, folder_uri: str | None = None) -> list[str]:
        effective_mode = self._mode
        if folder_uri is not None:
            folder_mode = self._folders.get(folder_uri)
            if folder_mode is not None:
                effective_mode = folder_mode
            elif folder_uri in self._trusted_folders:
                return []
        return list(_BLOCKED_OPERATIONS.get(effective_mode, set()))

    def get_allowed_operations(self, folder_uri: str | None = None) -> list[str]:
        effective_mode = self._mode
        if folder_uri is not None:
            folder_mode = self._folders.get(folder_uri)
            if folder_mode is not None:
                effective_mode = folder_mode
            elif folder_uri in self._trusted_folders:
                effective_mode = TrustMode.TRUSTED

        blocked = _BLOCKED_OPERATIONS.get(effective_mode, set())
        all_ops = set()
        for ops in _BLOCKED_OPERATIONS.values():
            all_ops.update(ops)
        return [op for op in all_ops if op not in blocked]

    def to_dict(self) -> dict[str, Any]:
        return {
            "mode": self._mode.value,
            "trusted_folders": list(self._trusted_folders),
            "folder_modes": {uri: mode.value for uri, mode in self._folders.items()},
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> WorkspaceTrust:
        wt = cls(default_mode=TrustMode(data.get("mode", "ask")))
        for uri in data.get("trusted_folders", []):
            wt._trusted_folders.add(uri)
        for uri, mode_str in data.get("folder_modes", {}).items():
            wt._folders[uri] = TrustMode(mode_str)
        return wt

    def __repr__(self) -> str:
        return f"WorkspaceTrust(mode={self._mode.value}, trusted_folders={len(self._trusted_folders)})"
