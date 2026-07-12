from __future__ import annotations

import os
import re

from lsprotocol.types import Diagnostic, DiagnosticSeverity, Position, Range

from aeos_lsp.configuration import LSPClientConfig
from aeos_lsp.diagnostics.registry import DiagnosticRule, RuleMetadata
from aeos_lsp.protocol.cancellation import CancellationToken
from aeos_lsp.semantic.semantic_model import SemanticModel

_PATH_ESCAPE_PATTERNS = [
    re.compile(r"\.\./"),
    re.compile(r"\.\.\\"),
    re.compile(r"\.\.[/\\]"),
    re.compile(r"~[/\\]"),
    re.compile(r"\$HOME"),
    re.compile(r"\${?HOME}?"),
    re.compile(r"\${?ENV}?\["),
    re.compile(r"/proc/"),
    re.compile(r"/sys/"),
    re.compile(r"/dev/"),
    re.compile(r"/etc/passwd"),
    re.compile(r"/etc/shadow"),
    re.compile(r"/windows/system32", re.IGNORECASE),
    re.compile(r"%SYSTEMROOT%", re.IGNORECASE),
    re.compile(r"%WINDIR%", re.IGNORECASE),
    re.compile(r"\\\\[A-Za-z]:\\"),
]


class PathEscapeRule(DiagnosticRule):
    metadata = RuleMetadata(
        code="AEOS0033",
        name="path-escape",
        description="Detects path traversal or escape attempts in file references",
        severity=DiagnosticSeverity.Error,
        category="security",
        version="1.0.0",
        tags=("security", "paths", "traversal"),
    )

    def check_document(
        self,
        document_uri: str,
        document_text: str,
        semantic_model: SemanticModel,
        config: LSPClientConfig,
        cancellation_token: CancellationToken | None = None,
    ) -> list[Diagnostic]:
        diagnostics: list[Diagnostic] = []

        lines = document_text.splitlines()
        for line_idx, line_text in enumerate(lines):
            if cancellation_token and cancellation_token.cancelled:
                break

            stripped = line_text.strip()
            if stripped.startswith("#") or stripped.startswith("//"):
                continue

            path_match = self._find_path_reference(stripped)
            if path_match:
                start_char, end_char, path_value = path_match

                if self._is_path_escape(path_value):
                    diagnostics.append(Diagnostic(
                        range=Range(
                            start=Position(line=line_idx, character=start_char),
                            end=Position(line=line_idx, character=end_char),
                        ),
                        severity=DiagnosticSeverity.Error,
                        code=self.metadata.code,
                        message=f"AEOS0033: Path escape detected: '{path_value}' references files outside workspace",
                        source="aeos-lsp",
                    ))

        return diagnostics

    @staticmethod
    def _find_path_reference(text: str) -> tuple[int, int, str] | None:
        path_patterns = [
            re.compile(r'(?:path|file|source|target|location|dir|directory)\s*[:=]\s*["\']?([^"\',\s}]+)'),
            re.compile(r'["\']((?:\.\.|~|/|\\\\|[A-Za-z]:\\|/proc/|/etc/)[^"\']*)["\']'),
        ]
        for pattern in path_patterns:
            m = pattern.search(text)
            if m:
                path_val = m.group(1) if m.lastindex else m.group(0)
                start = m.start(1) if m.lastindex else m.start()
                end = m.end(1) if m.lastindex else m.end()
                return start, end, path_val
        return None

    @staticmethod
    def _is_path_escape(path: str) -> bool:
        path = path.strip().strip("'").strip('"')

        for pattern in _PATH_ESCAPE_PATTERNS:
            if pattern.search(path):
                return True

        if os.path.isabs(path) and not path.startswith("/workspace") and not path.startswith("${"):
            return True

        if ".." in path:
            normalized = os.path.normpath(path)
            if normalized.startswith("..") or "/../" in normalized or "\\..\\" in normalized:
                return True

        if os.path.sep == "\\":
            if re.match(r"^[A-Za-z]:\\", path):
                return True

        return False
