from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from lsprotocol.types import DiagnosticSeverity

from aeos_lsp.configuration import LSPClientConfig

SEVERITY_LABELS: dict[int, str] = {
    DiagnosticSeverity.Error: "error",
    DiagnosticSeverity.Warning: "warning",
    DiagnosticSeverity.Information: "information",
    DiagnosticSeverity.Hint: "hint",
}

SEVERITY_FROM_LABEL: dict[str, int] = {v: k for k, v in SEVERITY_LABELS.items()}

PROFILE_SEVERITY_OVERRIDES: dict[str, dict[str, int]] = {
    "editor": {},
    "agent": {
        "warning": DiagnosticSeverity.Error,
    },
    "ci": {
        "warning": DiagnosticSeverity.Error,
        "information": DiagnosticSeverity.Error,
        "hint": DiagnosticSeverity.Warning,
    },
}

DEFAULT_SEVERITY_MAP: dict[str, int] = {
    "error": DiagnosticSeverity.Error,
    "warning": DiagnosticSeverity.Warning,
    "information": DiagnosticSeverity.Information,
    "hint": DiagnosticSeverity.Hint,
}


@dataclass
class DiagnosticSeverityMapper:
    profile: str = "editor"
    custom_overrides: dict[str, dict[str, int]] = field(default_factory=dict)

    def severity_from_config(self, config_value: str | int | None) -> int:
        if isinstance(config_value, int):
            if config_value in (
                DiagnosticSeverity.Error,
                DiagnosticSeverity.Warning,
                DiagnosticSeverity.Information,
                DiagnosticSeverity.Hint,
            ):
                return config_value
            return DiagnosticSeverity.Warning
        if isinstance(config_value, str):
            label = config_value.lower()
            profile = self.profile
            overrides = self._get_profile_overrides(profile)
            if label in overrides:
                return overrides[label]
            return SEVERITY_FROM_LABEL.get(label, DiagnosticSeverity.Warning)
        return DiagnosticSeverity.Warning

    def map_severity(self, base_severity: int) -> int:
        profile = self.profile
        overrides = self._get_profile_overrides(profile)
        label = SEVERITY_LABELS.get(base_severity, "warning")
        return overrides.get(label, base_severity)

    def _get_profile_overrides(self, profile: str) -> dict[str, int]:
        merged = dict(DEFAULT_SEVERITY_MAP)
        base = PROFILE_SEVERITY_OVERRIDES.get(profile, {})
        for label, sev in base.items():
            merged[label] = sev
        custom = self.custom_overrides.get(profile, {})
        for label, sev in custom.items():
            merged[label] = sev
        return merged

    def update_from_config(self, config: LSPClientConfig) -> None:
        self.profile = config.diagnostic_profile

    @staticmethod
    def severity_label(severity: int) -> str:
        return SEVERITY_LABELS.get(severity, "unknown")

    @staticmethod
    def sort_key(severity: int) -> int:
        ordering = {
            DiagnosticSeverity.Error: 0,
            DiagnosticSeverity.Warning: 1,
            DiagnosticSeverity.Information: 2,
            DiagnosticSeverity.Hint: 3,
        }
        return ordering.get(severity, 99)
