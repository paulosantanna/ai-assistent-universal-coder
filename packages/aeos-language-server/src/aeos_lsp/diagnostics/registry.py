from __future__ import annotations

import threading
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any

from lsprotocol.types import Diagnostic, DiagnosticSeverity

from aeos_lsp.configuration import LSPClientConfig
from aeos_lsp.protocol.cancellation import CancellationToken
from aeos_lsp.semantic.semantic_model import SemanticModel
from aeos_lsp.workspace.manager import WorkspaceManager


@dataclass(frozen=True)
class RuleMetadata:
    code: str
    name: str
    description: str
    severity: int = DiagnosticSeverity.Warning
    category: str = "general"
    version: str = "1.0.0"
    check_document: bool = True
    check_workspace: bool = False
    tags: tuple[str, ...] = ()


class DiagnosticRule(ABC):
    metadata: RuleMetadata

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} [{self.metadata.code}]>"

    def check_document(
        self,
        document_uri: str,
        document_text: str,
        semantic_model: SemanticModel,
        config: LSPClientConfig,
        cancellation_token: CancellationToken | None = None,
    ) -> list[Diagnostic]:
        return []

    def check_workspace(
        self,
        workspace: WorkspaceManager,
        semantic_model: SemanticModel,
        config: LSPClientConfig,
        cancellation_token: CancellationToken | None = None,
    ) -> list[Diagnostic]:
        return []


@dataclass
class DiagnosticRuleRegistry:
    rules: dict[str, DiagnosticRule] = field(default_factory=dict)
    rules_by_category: dict[str, list[DiagnosticRule]] = field(default_factory=dict)
    rules_by_code: dict[str, DiagnosticRule] = field(default_factory=dict)
    disabled_rules: set[str] = field(default_factory=set)
    _lock: threading.RLock = field(default_factory=threading.RLock)

    def register_defaults(self) -> None:
        from aeos_lsp.diagnostics.rules import register_all_rules
        register_all_rules(self)

    def register(self, rule: DiagnosticRule) -> None:
        with self._lock:
            meta = rule.metadata
            self.rules[meta.code] = rule
            self.rules_by_code[meta.code] = rule
            category = meta.category
            if category not in self.rules_by_category:
                self.rules_by_category[category] = []
            self.rules_by_category[category].append(rule)

    def register_all(self, rules: list[DiagnosticRule]) -> None:
        for rule in rules:
            self.register(rule)

    def get_rule(self, code: str) -> DiagnosticRule | None:
        with self._lock:
            return self.rules_by_code.get(code)

    def get_rules_by_category(self, category: str) -> list[DiagnosticRule]:
        with self._lock:
            return list(self.rules_by_category.get(category, []))

    def get_all_rules(self) -> list[DiagnosticRule]:
        with self._lock:
            return list(self.rules.values())

    def get_enabled_rules(self) -> list[DiagnosticRule]:
        with self._lock:
            return [
                rule for code, rule in self.rules.items()
                if code not in self.disabled_rules
            ]

    def get_enabled_rules_for_document(self) -> list[DiagnosticRule]:
        with self._lock:
            return [
                rule for code, rule in self.rules.items()
                if code not in self.disabled_rules and rule.metadata.check_document
            ]

    def get_enabled_rules_for_workspace(self) -> list[DiagnosticRule]:
        with self._lock:
            return [
                rule for code, rule in self.rules.items()
                if code not in self.disabled_rules and rule.metadata.check_workspace
            ]

    def enable_rule(self, code: str) -> bool:
        with self._lock:
            if code not in self.rules:
                return False
            self.disabled_rules.discard(code)
            return True

    def disable_rule(self, code: str) -> bool:
        with self._lock:
            if code not in self.rules:
                return False
            self.disabled_rules.add(code)
            return True

    def is_enabled(self, code: str) -> bool:
        with self._lock:
            return code not in self.disabled_rules

    def enable_all(self) -> None:
        with self._lock:
            self.disabled_rules.clear()

    def disable_all(self) -> None:
        with self._lock:
            self.disabled_rules.update(self.rules.keys())

    def get_categories(self) -> list[str]:
        with self._lock:
            return list(self.rules_by_category.keys())

    def count(self) -> int:
        with self._lock:
            return len(self.rules)

    def count_enabled(self) -> int:
        with self._lock:
            return len(self.rules) - len(self.disabled_rules)

    def apply_config_suppressions(self, config: LSPClientConfig) -> None:
        pass

    def clear(self) -> None:
        with self._lock:
            self.rules.clear()
            self.rules_by_category.clear()
            self.rules_by_code.clear()
            self.disabled_rules.clear()
