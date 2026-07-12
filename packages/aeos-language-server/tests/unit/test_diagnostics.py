from __future__ import annotations

from unittest.mock import MagicMock, Mock

import pytest
from lsprotocol.types import Diagnostic, DiagnosticSeverity

from aeos_lsp.diagnostics.registry import DiagnosticRule, DiagnosticRuleRegistry, RuleMetadata
from aeos_lsp.diagnostics.engine import DiagnosticsEngine, DiagnosticsResult
from aeos_lsp.diagnostics.publisher import DiagnosticPublisher
from aeos_lsp.diagnostics.suppression import SuppressionManager, SuppressionEntry
from aeos_lsp.diagnostics.severity import DiagnosticSeverityMapper


class TestRuleMetadata:
    def test_metadata_creation(self):
        metadata = RuleMetadata(
            code="AEOS0001",
            name="test-rule",
            description="A test rule",
            severity=DiagnosticSeverity.Warning,
        )
        assert metadata.code == "AEOS0001"
        assert metadata.name == "test-rule"
        assert metadata.description == "A test rule"
        assert metadata.severity == DiagnosticSeverity.Warning

    def test_metadata_defaults(self):
        metadata = RuleMetadata(code="M001", name="Minimal", description="")
        assert metadata.severity == DiagnosticSeverity.Warning
        assert metadata.category == "general"


class TestDiagnosticRule:
    def test_rule_implementation(self):
        class TestRule(DiagnosticRule):
            metadata = RuleMetadata(code="T001", name="test", description="")

            def check_document(self, document_uri, document_text, semantic_model, config, cancellation_token=None):
                return []

        rule = TestRule()
        result = rule.check_document("test.yaml", "", MagicMock(), MagicMock())
        assert result == []

    def test_rule_workspace_default(self):
        class TestRule(DiagnosticRule):
            metadata = RuleMetadata(code="T002", name="test2", description="")

            def check_document(self, document_uri, document_text, semantic_model, config, cancellation_token=None):
                return []

        rule = TestRule()
        result = rule.check_workspace(MagicMock(), MagicMock(), MagicMock())
        assert result == []

    def test_rule_repr(self):
        class TestRule(DiagnosticRule):
            metadata = RuleMetadata(code="R001", name="repr-test", description="")

            def check_document(self, document_uri, document_text, semantic_model, config, cancellation_token=None):
                return []

        rule = TestRule()
        assert "R001" in repr(rule)


class TestDiagnosticRuleRegistry:
    @pytest.fixture
    def registry(self) -> DiagnosticRuleRegistry:
        return DiagnosticRuleRegistry()

    def test_register_and_get(self, registry):
        class TestRule(DiagnosticRule):
            metadata = RuleMetadata(code="REG001", name="reg-test", description="")

            def check_document(self, document_uri, document_text, semantic_model, config, cancellation_token=None):
                return []

        rule = TestRule()
        registry.register(rule)
        assert registry.get_rule("REG001") is rule
        assert registry.count() == 1

    def test_register_all(self, registry):
        rules = []
        for i in range(3):
            r = type(f"DynRule{i}", (DiagnosticRule,), {
                "metadata": RuleMetadata(code=f"D{i:03d}", name=f"dyn-{i}", description=""),
                "check_document": lambda self, du, dt, sm, c, ct=None: [],
            })()
            rules.append(r)
        registry.register_all(rules)
        assert registry.count() == 3

    def test_enable_disable(self, registry):
        class TestRule(DiagnosticRule):
            metadata = RuleMetadata(code="TGL001", name="toggle", description="")

            def check_document(self, document_uri, document_text, semantic_model, config, cancellation_token=None):
                return []

        rule = TestRule()
        registry.register(rule)
        assert registry.is_enabled("TGL001")
        registry.disable_rule("TGL001")
        assert not registry.is_enabled("TGL001")
        registry.enable_rule("TGL001")
        assert registry.is_enabled("TGL001")

    def test_get_enabled_rules(self, registry):
        class RuleA(DiagnosticRule):
            metadata = RuleMetadata(code="A", name="a", description="")
            def check_document(self, du, dt, sm, c, ct=None): return []

        class RuleB(DiagnosticRule):
            metadata = RuleMetadata(code="B", name="b", description="")
            def check_document(self, du, dt, sm, c, ct=None): return []

        registry.register_all([RuleA(), RuleB()])
        registry.disable_rule("A")
        enabled = registry.get_enabled_rules()
        assert len(enabled) == 1

    def test_clear(self, registry):
        class ClrRule(DiagnosticRule):
            metadata = RuleMetadata(code="CLR1", name="clear-test", description="")
            def check_document(self, du, dt, sm, c, ct=None): return []

        registry.register(ClrRule())
        registry.clear()
        assert registry.count() == 0


class TestDiagnosticsEngine:
    @pytest.fixture
    def engine(self) -> DiagnosticsEngine:
        publisher = MagicMock(spec=DiagnosticPublisher)
        return DiagnosticsEngine(publisher=publisher)

    def test_initialization(self, engine):
        assert engine.registry is not None
        assert engine.publisher is not None

    def test_run_document_diagnostics(self, engine):
        config = Mock()
        config.max_diagnostics_per_file = 100
        result = engine.run_document_diagnostics(
            uri="test.yaml",
            text="agent:\n  name: test\n",
            semantic_model=MagicMock(),
            config=config,
        )
        assert isinstance(result, DiagnosticsResult)


class TestSuppressionManager:
    @pytest.fixture
    def manager(self) -> SuppressionManager:
        return SuppressionManager()

    def test_parse_suppression_comments(self, manager):
        text = "# aeos-lsp:ignore AEOS0001\nagent:\n  name: test\n"
        entries = manager.parse_suppression_comments("test.yaml", text)
        assert len(entries) > 0


class TestDiagnosticSeverityMapper:
    @pytest.fixture
    def mapper(self) -> DiagnosticSeverityMapper:
        return DiagnosticSeverityMapper()

    def test_map_severity_default(self, mapper):
        result = mapper.map_severity(DiagnosticSeverity.Error)
        assert result == DiagnosticSeverity.Error

    def test_severity_from_label(self, mapper):
        result = mapper.severity_from_config("error")
        assert result == DiagnosticSeverity.Error
