from dataclasses import dataclass, field
from typing import Any
from .constants import (
    MAX_DIAGNOSTICS_PER_FILE_DEFAULT,
    MAX_WORKSPACE_DIAGNOSTICS_DEFAULT,
    MAX_COMPLETION_ITEMS_DEFAULT,
    MAX_REFERENCES_DEFAULT,
    MAX_OUTPUT_CHARS_DEFAULT,
    DEBOUNCE_MILLISECONDS_DEFAULT,
    INDEXING_CONCURRENCY_DEFAULT,
    BACKGROUND_INDEXING_DEFAULT,
    DIAGNOSTIC_PROFILE_DEFAULT,
    ENABLE_EXPERIMENTAL_FEATURES_DEFAULT,
)


@dataclass
class LSPClientConfig:
    max_diagnostics_per_file: int = MAX_DIAGNOSTICS_PER_FILE_DEFAULT
    max_workspace_diagnostics: int = MAX_WORKSPACE_DIAGNOSTICS_DEFAULT
    max_completion_items: int = MAX_COMPLETION_ITEMS_DEFAULT
    max_references: int = MAX_REFERENCES_DEFAULT
    max_output_chars: int = MAX_OUTPUT_CHARS_DEFAULT
    debounce_milliseconds: int = DEBOUNCE_MILLISECONDS_DEFAULT
    indexing_concurrency: int = INDEXING_CONCURRENCY_DEFAULT
    background_indexing: bool = BACKGROUND_INDEXING_DEFAULT
    diagnostic_profile: str = DIAGNOSTIC_PROFILE_DEFAULT
    enable_experimental_features: bool = ENABLE_EXPERIMENTAL_FEATURES_DEFAULT
    excluded_paths: set[str] = field(default_factory=set)
    trusted_workspace: bool = False
    log_level: str = "WARNING"

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "LSPClientConfig":
        return cls(
            max_diagnostics_per_file=data.get("maxDiagnosticsPerFile", MAX_DIAGNOSTICS_PER_FILE_DEFAULT),
            max_workspace_diagnostics=data.get("maxWorkspaceDiagnostics", MAX_WORKSPACE_DIAGNOSTICS_DEFAULT),
            max_completion_items=data.get("maxCompletionItems", MAX_COMPLETION_ITEMS_DEFAULT),
            max_references=data.get("maxReferences", MAX_REFERENCES_DEFAULT),
            max_output_chars=data.get("maxOutputChars", MAX_OUTPUT_CHARS_DEFAULT),
            debounce_milliseconds=data.get("debounceMilliseconds", DEBOUNCE_MILLISECONDS_DEFAULT),
            indexing_concurrency=data.get("indexingConcurrency", INDEXING_CONCURRENCY_DEFAULT),
            background_indexing=data.get("backgroundIndexing", BACKGROUND_INDEXING_DEFAULT),
            diagnostic_profile=data.get("diagnosticProfile", DIAGNOSTIC_PROFILE_DEFAULT),
            enable_experimental_features=data.get("enableExperimentalFeatures", ENABLE_EXPERIMENTAL_FEATURES_DEFAULT),
            excluded_paths=set(data.get("excludedPaths", [])),
            trusted_workspace=data.get("trustedWorkspace", False),
            log_level=data.get("logLevel", "WARNING"),
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "maxDiagnosticsPerFile": self.max_diagnostics_per_file,
            "maxWorkspaceDiagnostics": self.max_workspace_diagnostics,
            "maxCompletionItems": self.max_completion_items,
            "maxReferences": self.max_references,
            "maxOutputChars": self.max_output_chars,
            "debounceMilliseconds": self.debounce_milliseconds,
            "indexingConcurrency": self.indexing_concurrency,
            "backgroundIndexing": self.background_indexing,
            "diagnosticProfile": self.diagnostic_profile,
            "enableExperimentalFeatures": self.enable_experimental_features,
        }


def merge_config(default: LSPClientConfig, overrides: dict[str, Any] | None) -> LSPClientConfig:
    if not overrides:
        return default
    merged = default.to_dict()
    merged.update(overrides)
    return LSPClientConfig.from_dict(merged)
