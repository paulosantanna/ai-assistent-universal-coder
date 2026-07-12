from __future__ import annotations

import pytest
from lsprotocol.types import Diagnostic, DiagnosticSeverity, Position, Range

from aeos_lsp.output.limits import OutputLimiter
from aeos_lsp.output.compaction import OutputCompactor
from aeos_lsp.output.diagnostic_formatter import DiagnosticFormatter


class TestOutputLimiter:
    @pytest.fixture
    def limiter(self) -> OutputLimiter:
        return OutputLimiter(max_chars=100, max_lines=5)

    def test_limit_text_by_chars(self, limiter):
        result = limiter.limit_text("a" * 200)
        assert len(result) <= 100

    def test_limit_text_by_lines(self, limiter):
        result = limiter.limit_text("\n".join(f"line {i}" for i in range(20)))
        assert len(result.split("\n")) <= 5

    def test_short_text_not_truncated(self, limiter):
        result = limiter.limit_text("hello")
        assert result == "hello"

    def test_limit_diagnostics(self, limiter):
        diag = Diagnostic(
            range=Range(start=Position(0, 0), end=Position(0, 1)),
            message="test", severity=DiagnosticSeverity.Error,
        )
        result = limiter.limit_diagnostics([diag] * 20)
        assert len(result) <= 20

    def test_empty_text(self, limiter):
        assert limiter.limit_text("") == ""


class TestOutputCompactor:
    @pytest.fixture
    def compactor(self) -> OutputCompactor:
        return OutputCompactor(max_repeated_lines=3)

    def test_compact_text(self, compactor):
        result = compactor.compact_text("a\nb\nb\nb\nc\n")
        assert result is not None
        assert isinstance(result, str)

    def test_compact_diagnostics(self, compactor):
        diag = Diagnostic(
            range=Range(start=Position(0, 0), end=Position(0, 1)),
            message="error", severity=DiagnosticSeverity.Error,
            code="E001", source="test",
        )
        result = compactor.compact_diagnostics([diag, diag, diag])
        assert len(result) == 1
        assert result[0].get("duplicates", 0) >= 1

    def test_empty(self, compactor):
        assert compactor.compact_diagnostics([]) == []


class TestDiagnosticFormatter:
    @pytest.fixture
    def formatter(self) -> DiagnosticFormatter:
        return DiagnosticFormatter()

    def test_format_editor(self, formatter):
        diag = Diagnostic(
            range=Range(start=Position(0, 0), end=Position(0, 10)),
            message="test error", severity=DiagnosticSeverity.Error,
            code="E001",
        )
        result = formatter.format([diag], "test.yaml")
        assert "test error" in result

    def test_format_json(self):
        formatter = DiagnosticFormatter(profile="json")
        diag = Diagnostic(
            range=Range(start=Position(0, 0), end=Position(0, 1)),
            message="json error", severity=DiagnosticSeverity.Warning,
            code="W001",
        )
        result = formatter.format([diag], "test.yaml")
        assert "json error" in result

    def test_format_empty(self, formatter):
        assert formatter.format([], "test.yaml") == ""
