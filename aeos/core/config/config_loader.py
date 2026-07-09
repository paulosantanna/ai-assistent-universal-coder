from __future__ import annotations

import os
from pathlib import Path
from typing import Optional

import yaml

from aeos.core.registries.registry_models import AEOSConfig, ConfigRegistryPaths, ValidationFinding, ValidationSeverity


class ConfigLoader:
    def __init__(self, workspace_root: str = ".", aeos_root: Optional[str] = None):
        self.workspace_root = Path(workspace_root).resolve()
        self.aeos_root = Path(aeos_root).resolve() if aeos_root else self.workspace_root
        self.config: Optional[AEOSConfig] = None
        self.findings: list[ValidationFinding] = []

    def load(self, config_path: str = "aeos/config/aeos.config.yaml") -> AEOSConfig:
        full_path = self.aeos_root / config_path
        if not full_path.exists():
            raise FileNotFoundError(f"Config file not found: {full_path}")

        with open(full_path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)

        aeos_data = data.get("aeos", {})
        reg_data = data.get("registries", {})

        reg_paths = ConfigRegistryPaths(
            agents=self._resolve_registry_path(reg_data.get("agents", "")),
            skills=self._resolve_registry_path(reg_data.get("skills", "")),
            playbooks=self._resolve_registry_path(reg_data.get("playbooks", "")),
            mcps=self._resolve_registry_path(reg_data.get("mcps", "")),
            lcps=self._resolve_registry_path(reg_data.get("lcps", "")),
            blueprints=self._resolve_registry_path(reg_data.get("blueprints", "")),
            enterprise_skills=self._resolve_registry_path(reg_data.get("enterprise_skills", "")),
            enterprise_playbooks=self._resolve_registry_path(reg_data.get("enterprise_playbooks", "")),
            workbench_profiles=self._resolve_registry_path(reg_data.get("workbench_profiles", "")),
            overlay_index=self._resolve_registry_path(reg_data.get("overlay_index", "")),
        )

        self.config = AEOSConfig(
            name=aeos_data.get("name", ""),
            version=aeos_data.get("version", ""),
            mode=aeos_data.get("mode", ""),
            registries=reg_paths,
        )

        self._validate_paths()
        return self.config

    def _resolve_registry_path(self, path: str) -> str:
        if not path:
            return ""
        return str(self.workspace_root / path)

    def _validate_paths(self) -> None:
        if not self.config:
            return
        for field_name in vars(self.config.registries):
            path = getattr(self.config.registries, field_name)
            if not path:
                self.findings.append(
                    ValidationFinding(
                        check=f"config.{field_name}",
                        status="MISSING",
                        severity=ValidationSeverity.WARNING,
                        detail=f"Config registry path '{field_name}' is empty",
                    )
                )
                continue
            full = Path(path)
            if not full.exists():
                self.findings.append(
                    ValidationFinding(
                        check=f"config.{field_name}",
                        status="NOT_FOUND",
                        severity=ValidationSeverity.ERROR,
                        detail=f"Config registry path '{field_name}' = '{path}' does not exist",
                    )
                )

    def get_config_paths(self) -> ConfigRegistryPaths:
        if not self.config:
            raise RuntimeError("Config not loaded. Call load() first.")
        return self.config.registries

    def get_registry_paths_list(self) -> list[str]:
        paths = self.get_config_paths()
        return [
            paths.agents,
            paths.skills,
            paths.playbooks,
            paths.mcps,
            paths.lcps,
            paths.blueprints,
            paths.enterprise_skills,
            paths.enterprise_playbooks,
            paths.workbench_profiles,
            paths.overlay_index,
        ]
