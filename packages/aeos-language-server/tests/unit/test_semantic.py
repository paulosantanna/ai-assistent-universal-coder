from __future__ import annotations

from unittest.mock import MagicMock

import pytest
from lsprotocol.types import Position, Range

from aeos_lsp.semantic.symbols import SymbolTable, SymbolVisitor, accept_visitor
from aeos_lsp.semantic.references import Reference, ReferenceKind, ReferenceRole, ReferenceTable
from aeos_lsp.semantic.resolver import CrossReferenceResolver, ResolutionResult
from aeos_lsp.semantic.dependency_graph import DependencyGraph, DependencyNode
from aeos_lsp.semantic.inheritance_graph import InheritanceGraph
from aeos_lsp.semantic.semantic_model import SemanticModel, ReadWriteLock
from aeos_lsp.semantic.models import (
    Agent, AgentLayer, Skill, Playbook, PlaybookStep, Tool, Command,
    Policy, Permission, Registry, Variable, Input, Output,
    SymbolKind, Visibility, DeprecationStatus, Workspace, Repository,
)
from aeos_lsp.semantic.scopes import Scope, ScopeKind, ScopeTree

A_RANGE = Range(start=Position(line=0, character=0), end=Position(line=1, character=0))


class TestSymbolTable:
    def test_add_and_get(self, symbol_table, sample_agent_symbol):
        symbol_table.add(sample_agent_symbol)
        assert symbol_table.get(sample_agent_symbol.stable_id) is sample_agent_symbol

    def test_get_by_kind(self, symbol_table, sample_agent_symbol, sample_skill_symbol):
        symbol_table.add(sample_agent_symbol)
        symbol_table.add(sample_skill_symbol)
        agents = symbol_table.get_by_kind(SymbolKind.AGENT)
        assert len(agents) == 1

    def test_remove(self, symbol_table, sample_agent_symbol):
        symbol_table.add(sample_agent_symbol)
        assert symbol_table.remove(sample_agent_symbol.stable_id)
        assert symbol_table.count() == 0

    def test_has_id(self, symbol_table, sample_agent_symbol):
        symbol_table.add(sample_agent_symbol)
        assert symbol_table.has_id(sample_agent_symbol.stable_id)
        assert not symbol_table.has_id("nonexistent")

    def test_all_symbols(self, symbol_table, sample_agent_symbol, sample_skill_symbol):
        symbol_table.add(sample_agent_symbol)
        symbol_table.add(sample_skill_symbol)
        assert len(symbol_table.all_symbols()) == 2

    def test_remove_by_uri(self, symbol_table, sample_agent_symbol):
        symbol_table.add(sample_agent_symbol)
        count = symbol_table.remove_by_uri(sample_agent_symbol.source_uri)
        assert count == 1

    def test_clear(self, symbol_table, sample_agent_symbol):
        symbol_table.add(sample_agent_symbol)
        symbol_table.clear()
        assert symbol_table.count() == 0


class TestReferenceTable:
    @pytest.fixture
    def sample_ref(self) -> Reference:
        return Reference(
            source_uri="file:///source.yaml",
            source_range=Range(start=Position(0, 0), end=Position(0, 10)),
            target_uri="file:///target.yaml",
            target_range=Range(start=Position(1, 0), end=Position(1, 5)),
        )

    def test_add_and_get(self, reference_table, sample_ref):
        reference_table.add_reference(sample_ref)
        outgoing = reference_table.get_outgoing("file:///source.yaml")
        assert len(outgoing) == 1

    def test_get_incoming(self, reference_table, sample_ref):
        reference_table.add_reference(sample_ref)
        incoming = reference_table.get_incoming("file:///target.yaml")
        assert len(incoming) == 1

    def test_find_references(self, reference_table, sample_ref):
        reference_table.add_reference(sample_ref)
        refs = reference_table.find_references("file:///target.yaml")
        assert len(refs) == 1

    def test_find_definitions(self, reference_table):
        ref = Reference(
            source_uri="file:///source.yaml",
            source_range=Range(start=Position(0, 0), end=Position(0, 1)),
            target_uri="file:///target.yaml",
            target_range=Range(start=Position(1, 0), end=Position(1, 1)),
            kind=ReferenceKind.DEFINITION,
        )
        reference_table.add_reference(ref)
        defns = reference_table.find_definitions("file:///target.yaml")
        assert len(defns) == 1

    def test_remove_for_uri(self, reference_table, sample_ref):
        reference_table.add_reference(sample_ref)
        count = reference_table.remove_for_uri("file:///source.yaml")
        assert count > 0

    def test_clear(self, reference_table, sample_ref):
        reference_table.add_reference(sample_ref)
        reference_table.clear()
        assert reference_table.count() == 0


class TestCrossReferenceResolver:
    def test_resolve_by_id_found(self, resolver, sample_agent_symbol):
        resolver.symbol_table.add(sample_agent_symbol)
        result = resolver.resolve_by_id(sample_agent_symbol.stable_id)
        assert result.resolved
        assert result.symbol is sample_agent_symbol

    def test_resolve_by_id_not_found(self, resolver):
        result = resolver.resolve_by_id("nonexistent")
        assert not result.resolved

    def test_resolve_by_name_found(self, resolver, sample_agent_symbol):
        resolver.symbol_table.add(sample_agent_symbol)
        result = resolver.resolve_by_name("test-agent", SymbolKind.AGENT)
        assert result.resolved

    def test_resolve_by_name_not_found(self, resolver):
        result = resolver.resolve_by_name("nonexistent")
        assert not result.resolved

    def test_resolve_agent_parent(self, resolver):
        parent = Agent(
            stable_id="agent:parent", name="parent",
            source_uri="file:///parent.yaml",
            selection_range=A_RANGE, full_range=A_RANGE,
        )
        child = Agent(
            stable_id="agent:child", name="child",
            source_uri="file:///child.yaml",
            selection_range=A_RANGE, full_range=A_RANGE,
            parent_id="agent:parent",
        )
        resolver.symbol_table.add(parent)
        resolver.symbol_table.add(child)
        result = resolver.resolve_agent_parent(child)
        assert result.resolved
        assert result.symbol is parent

    def test_invalidate_cache(self, resolver, sample_agent_symbol):
        resolver.symbol_table.add(sample_agent_symbol)
        resolver.resolve_by_id(sample_agent_symbol.stable_id)
        resolver.invalidate_cache(sample_agent_symbol.stable_id)
        result = resolver.resolve_by_id(sample_agent_symbol.stable_id)
        assert result.resolved

    def test_clear_cache(self, resolver, sample_agent_symbol):
        resolver.symbol_table.add(sample_agent_symbol)
        resolver.resolve_by_id(sample_agent_symbol.stable_id)
        resolver.clear_cache()
        result = resolver.resolve_by_id(sample_agent_symbol.stable_id)
        assert result.resolved


class TestDependencyGraph:
    def test_add_node(self, dependency_graph):
        node = DependencyNode(id="test", kind=SymbolKind.AGENT, uri="file:///test.yaml")
        dependency_graph.add_node(node)
        assert dependency_graph.has_node("test")

    def test_add_dependency(self, dependency_graph):
        dependency_graph.add_dependency("a", "b")
        deps = dependency_graph.get_dependencies("a")
        assert len(deps) == 1

    def test_get_dependents(self, dependency_graph):
        dependency_graph.add_dependency("a", "b")
        dependents = dependency_graph.get_dependents("b")
        assert len(dependents) == 1

    def test_has_cycle(self, dependency_graph):
        dependency_graph.add_dependency("a", "b")
        dependency_graph.add_dependency("b", "c")
        dependency_graph.add_dependency("c", "a")
        assert dependency_graph.has_cycle()

    def test_no_cycle(self, dependency_graph):
        dependency_graph.add_dependency("a", "b")
        dependency_graph.add_dependency("b", "c")
        assert not dependency_graph.has_cycle()

    def test_find_cycles(self, dependency_graph):
        dependency_graph.add_dependency("a", "b")
        dependency_graph.add_dependency("b", "c")
        dependency_graph.add_dependency("c", "a")
        cycles = dependency_graph.find_cycles()
        assert len(cycles) > 0

    def test_topological_sort(self, dependency_graph):
        dependency_graph.add_dependency("a", "b")
        dependency_graph.add_dependency("b", "c")
        sorted_ids = dependency_graph.topological_sort()
        assert len(sorted_ids) == 3
        assert sorted_ids[-1] == "a"
        assert sorted_ids[0] == "c"

    def test_reachable_from(self, dependency_graph):
        dependency_graph.add_dependency("a", "b")
        dependency_graph.add_dependency("b", "c")
        reachable = dependency_graph.reachable_from("a")
        assert "b" in reachable
        assert "c" in reachable

    def test_impact_analysis(self, dependency_graph):
        dependency_graph.add_dependency("a", "b")
        dependency_graph.add_dependency("b", "c")
        impact = dependency_graph.impact_analysis({"c"})
        assert "c" in impact
        assert "a" in impact["c"]
        assert "b" in impact["c"]

    def test_merge(self, dependency_graph):
        other = DependencyGraph()
        other.add_dependency("x", "y")
        dependency_graph.add_dependency("a", "b")
        dependency_graph.merge(other)
        assert dependency_graph.has_node("x")
        assert dependency_graph.has_node("y")

    def test_clear(self, dependency_graph):
        dependency_graph.add_dependency("a", "b")
        dependency_graph.clear()
        assert dependency_graph.count() == 0

    def test_subgraph(self, dependency_graph):
        dependency_graph.add_dependency("a", "b")
        dependency_graph.add_dependency("b", "c")
        sub = dependency_graph.subgraph({"a", "b"})
        assert sub.has_node("a")
        assert not sub.has_node("c")


class TestInheritanceGraph:
    def test_add_relationship(self, inheritance_graph):
        inheritance_graph.add_relationship("child", "parent")
        assert inheritance_graph.get_parent("child") == "parent"

    def test_get_ancestors(self, inheritance_graph):
        inheritance_graph.add_relationship("child", "parent")
        inheritance_graph.add_relationship("parent", "grandparent")
        ancestors = inheritance_graph.get_ancestors("child")
        assert "parent" in ancestors
        assert "grandparent" in ancestors

    def test_get_descendants(self, inheritance_graph):
        inheritance_graph.add_relationship("child", "parent")
        inheritance_graph.add_relationship("grandchild", "child")
        descendants = inheritance_graph.get_descendants("parent")
        assert "child" in descendants
        assert "grandchild" in descendants

    def test_has_cycle(self, inheritance_graph):
        inheritance_graph.add_relationship("a", "b")
        inheritance_graph.add_relationship("b", "c")
        inheritance_graph.add_relationship("c", "a")
        assert inheritance_graph.has_cycle()

    def test_no_cycle(self, inheritance_graph):
        inheritance_graph.add_relationship("a", "b")
        inheritance_graph.add_relationship("b", "c")
        assert not inheritance_graph.has_cycle()

    def test_compute_mro(self, inheritance_graph):
        inheritance_graph.add_relationship("child", "parent")
        inheritance_graph.add_relationship("parent", "grandparent")
        mro = inheritance_graph.compute_mro("child")
        assert "grandparent" in mro
        assert "parent" in mro
        assert "child" in mro

    def test_remove_node(self, inheritance_graph):
        inheritance_graph.add_relationship("child", "parent")
        assert inheritance_graph.remove_node("child")
        assert inheritance_graph.get_parent("child") is None

    def test_clear(self, inheritance_graph):
        inheritance_graph.add_relationship("child", "parent")
        inheritance_graph.clear()
        assert inheritance_graph.count() == 0


class TestReadWriteLock:
    def test_acquire_release_read(self):
        lock = ReadWriteLock()
        lock.acquire_read()
        lock.release_read()

    def test_acquire_release_write(self):
        lock = ReadWriteLock()
        lock.acquire_write()
        lock.release_write()

    def test_context_manager(self):
        lock = ReadWriteLock()
        with lock:
            pass


class TestVisitor:
    def test_accept_visitor(self):
        class TestVisitor(SymbolVisitor):
            def visit_agent(self, symbol): return "visited_agent"
            visit_workspace = lambda self, s: None
            visit_repository = lambda self, s: None
            visit_agent_layer = lambda self, s: None
            visit_skill = lambda self, s: None
            visit_playbook = lambda self, s: None
            visit_playbook_step = lambda self, s: None
            visit_tool = lambda self, s: None
            visit_command = lambda self, s: None
            visit_policy = lambda self, s: None
            visit_permission = lambda self, s: None
            visit_registry = lambda self, s: None
            visit_model_profile = lambda self, s: None
            visit_token_budget = lambda self, s: None
            visit_quality_gate = lambda self, s: None
            visit_judge_rule = lambda self, s: None
            visit_evidence_requirement = lambda self, s: None
            visit_artifact = lambda self, s: None
            visit_variable = lambda self, s: None
            visit_input = lambda self, s: None
            visit_output = lambda self, s: None
            visit_dependency = lambda self, s: None
            visit_execution_target = lambda self, s: None
            visit_approval_requirement = lambda self, s: None
            visit_rollback_definition = lambda self, s: None

        agent = Agent(
            stable_id="agent:test", name="test",
            source_uri="file:///test.yaml",
            selection_range=A_RANGE, full_range=A_RANGE,
        )
        visitor = TestVisitor()
        result = accept_visitor(agent, visitor)
        assert result == "visited_agent"


class TestScopes:
    def test_scope_tree(self):
        tree = ScopeTree()
        scope = tree.get_or_create_file_scope("file:///test.yaml")
        assert scope is not None
        assert scope.uri == "file:///test.yaml"
        assert scope.kind == ScopeKind.FILE

    def test_scope_add_symbol(self):
        tree = ScopeTree()
        scope = tree.get_or_create_file_scope("file:///test.yaml")
        sym = Agent(
            stable_id="agent:test", name="test",
            source_uri="file:///test.yaml",
            selection_range=A_RANGE, full_range=A_RANGE,
        )
        scope.add_symbol(sym)
        assert len(scope.symbols) == 1

    def test_scope_remove(self):
        tree = ScopeTree()
        tree.get_or_create_file_scope("file:///test.yaml")
        tree.remove_scope("file:///test.yaml")
        scope = tree.find_scope_at("file:///test.yaml", Position(0, 0))
        assert scope is None
