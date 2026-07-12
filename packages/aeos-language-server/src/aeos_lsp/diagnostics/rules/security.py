from __future__ import annotations

import re

from lsprotocol.types import Diagnostic, DiagnosticSeverity, Position, Range

from aeos_lsp.configuration import LSPClientConfig
from aeos_lsp.diagnostics.registry import DiagnosticRule, RuleMetadata
from aeos_lsp.protocol.cancellation import CancellationToken
from aeos_lsp.semantic.models import Command, Tool
from aeos_lsp.semantic.semantic_model import SemanticModel

_SHELL_ESCAPE_PATTERNS = [
    re.compile(r"(?:^|[|;&`\'\"\\])\s*(?:rm|del|rd|format|mkfs|dd|shutdown|reboot|halt|poweroff|init|killall|pkill|chmod\s+777|chown|sudo|su)\s"),
    re.compile(r">\s*/dev/"),
    re.compile(r"\${?(?:curl|wget|fetch|bash|sh|python|perl|ruby|powershell|cmd)\s"),
    re.compile(r"2>&1"),
    re.compile(r"exec\s+\S+"),
    re.compile(r"eval\s"),
    re.compile(r"`[^`]+`"),
]

_INTERPOLATION_PATTERNS = [
    re.compile(r"\$\{[^}]+\}"),
    re.compile(r"\$\([^)]+\)"),
    re.compile(r"`[^`]+`"),
    re.compile(r"%[^%]+%"),
]


class InsecureShellCommandRule(DiagnosticRule):
    metadata = RuleMetadata(
        code="AEOS0031",
        name="insecure-shell-command",
        description="Detects shell command configurations that may be insecure",
        severity=DiagnosticSeverity.Error,
        category="security",
        version="1.0.0",
        tags=("security", "shell", "injection"),
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

        symbols = semantic_model.get_symbols_by_uri(document_uri)

        for sym in symbols:
            if cancellation_token and cancellation_token.cancelled:
                break

            if isinstance(sym, Tool):
                command = getattr(sym, "command", "")
                if command:
                    sr = getattr(sym, "selection_range", None)
                    for pattern in _SHELL_ESCAPE_PATTERNS:
                        m = pattern.search(command)
                        if m:
                            if sr is not None:
                                diagnostics.append(Diagnostic(
                                    range=sr,
                                    severity=DiagnosticSeverity.Error,
                                    code=self.metadata.code,
                                    message=f"AEOS0031: Tool '{sym.name}' contains potentially insecure shell command: '{m.group().strip()}'",
                                    source="aeos-lsp",
                                ))
                            break

            elif isinstance(sym, Command):
                shell = getattr(sym, "shell", False)
                args = getattr(sym, "args", [])
                if shell:
                    for arg in args:
                        if isinstance(arg, str):
                            for pattern in _SHELL_ESCAPE_PATTERNS:
                                m = pattern.search(arg)
                                if m:
                                    diagnostics.append(Diagnostic(
                                        range=Range(
                                            start=Position(line=0, character=0),
                                            end=Position(line=0, character=1),
                                        ),
                                        severity=DiagnosticSeverity.Error,
                                        code=self.metadata.code,
                                        message=f"AEOS0031: Command '{sym.name}' shell argument contains insecure pattern: '{m.group().strip()}'",
                                        source="aeos-lsp",
                                    ))
                                    break

        return diagnostics


class CommandInjectionRule(DiagnosticRule):
    metadata = RuleMetadata(
        code="AEOS0032",
        name="command-injection",
        description="Detects string interpolation patterns that may be susceptible to command injection",
        severity=DiagnosticSeverity.Warning,
        category="security",
        version="1.0.0",
        tags=("security", "injection", "interpolation"),
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

            for pattern in _INTERPOLATION_PATTERNS:
                for m in pattern.finditer(stripped):
                    interpolation = m.group()
                    # Check if the interpolation looks injectable
                    if _is_suspicious_interpolation(interpolation):
                        start_char = line_text.find(interpolation)
                        if start_char >= 0:
                            diagnostics.append(Diagnostic(
                                range=Range(
                                    start=Position(line=line_idx, character=start_char),
                                    end=Position(line=line_idx, character=start_char + len(interpolation)),
                                ),
                                severity=DiagnosticSeverity.Warning,
                                code=self.metadata.code,
                                message=f"AEOS0032: String interpolation '{interpolation}' may be susceptible to injection",
                                source="aeos-lsp",
                            ))

        symbols = semantic_model.get_symbols_by_uri(document_uri)
        for sym in symbols:
            if cancellation_token and cancellation_token.cancelled:
                break

            if isinstance(sym, Tool):
                command = getattr(sym, "command", "")
                if command:
                    sr = getattr(sym, "selection_range", None)
                    for pattern in _INTERPOLATION_PATTERNS:
                        m = pattern.search(command)
                        if m:
                            interpolation = m.group()
                            if _is_suspicious_interpolation(interpolation):
                                if sr is not None:
                                    diagnostics.append(Diagnostic(
                                        range=sr,
                                        severity=DiagnosticSeverity.Warning,
                                        code=self.metadata.code,
                                        message=f"AEOS0032: Tool '{sym.name}' uses interpolation '{interpolation}' which may allow injection",
                                        source="aeos-lsp",
                                    ))
                                break

        return diagnostics


def _is_suspicious_interpolation(interpolation: str) -> bool:
    lowered = interpolation.lower()
    suspicious = ["input.", "user.", "arg.", "param.", "query.", "request.",
                  "env.", "getenv", "argv", "stdin", "${input", "${user",
                  "$(cat ", "$(curl ", "$(wget ", "`cat ", "`curl "]
    for s in suspicious:
        if s in lowered:
            return True
    return False
