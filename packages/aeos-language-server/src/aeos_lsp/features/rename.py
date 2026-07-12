from __future__ import annotations

import threading
from typing import Any

from lsprotocol.types import (
    AnnotatedTextEdit,
    AnnotatedTextEdit,
    ChangeAnnotation,
    OptionalVersionedTextDocumentIdentifier,
    Position,
    Range,
    RenameParams,
    TextEdit,
    WorkspaceEdit,
    WorkspaceEdit,
)
from pygls.lsp.server import LanguageServer

from aeos_lsp.semantic.models import (
    Agent,
    PlaybookStep,
    Skill,
    SymbolKind,
)
from aeos_lsp.semantic.semantic_model import SemanticModel


class RenameFeature:
    def __init__(self, server: LanguageServer, semantic_model: SemanticModel) -> None:
        self._server = server
        self._semantic_model = semantic_model
        self._lock = threading.RLock()

    def rename(self, params: RenameParams) -> WorkspaceEdit | WorkspaceEdit | None:
        uri = params.text_document.uri
        pos = params.position
        new_name = params.new_name.strip()

        if not new_name:
            return None

        with self._lock:
            symbol = self._semantic_model.get_symbol(uri, pos)
            if symbol is None:
                return None

            stable_id = symbol.stable_id
            source_uri = getattr(symbol, "source_uri", uri)

            changes: dict[str, list[TextEdit]] = {}
            annotations: dict[str, ChangeAnnotation] = {
                "rename": ChangeAnnotation(
                    label=f"Rename '{getattr(symbol, 'name', stable_id)}' to '{new_name}'",
                    needs_confirmation=True,
                ),
            }

            self._add_self_rename(symbol, new_name, source_uri, changes)

            self._rename_references(stable_id, symbol, new_name, source_uri, changes)

            self._rename_dependents(stable_id, new_name, changes)

            self._rename_registries(symbol, new_name, changes)

            if isinstance(symbol, Agent):
                self._rename_agent_children(symbol, new_name, changes)

            self._rename_in_expressions(stable_id, getattr(symbol, "name", stable_id), new_name, changes)

            if not changes:
                return None

            return WorkspaceEdit(
                changes={
                    uri: edits
                    for uri, edits in changes.items()
                } if not self._use_v1() else None,
                change_annotations=annotations if self._use_v1() else None,
                document_changes=[
                    AnnotatedTextEdit(
                        text_document=OptionalVersionedTextDocumentIdentifier(uri=u, version=None),
                        edits=edits,
                        annotation_id="rename",
                    )
                    for u, edits in changes.items()
                ] if self._use_v1() else None,
            )

    def _add_self_rename(self, symbol: Any, new_name: str, source_uri: str, changes: dict[str, list[TextEdit]]) -> None:
        range_ = getattr(symbol, "selection_range", None) or getattr(symbol, "full_range", None)
        if range_ is not None:
            changes.setdefault(source_uri, []).append(
                TextEdit(range=range_, new_text=new_name)
            )

    def _rename_references(self, stable_id: str, symbol: Any, new_name: str, source_uri: str, changes: dict[str, list[TextEdit]]) -> None:
        ref_table = self._semantic_model.reference_table
        all_refs = ref_table._by_uri.get(source_uri, [])
        for ref in all_refs:
            if ref.target_uri == source_uri or stable_id in str(getattr(ref, "target_range", "")):
                changes.setdefault(ref.source_uri, []).append(
                    TextEdit(range=ref.source_range, new_text=new_name)
                )

        for sym in self._semantic_model.symbol_table.all_symbols():
            other_uri = getattr(sym, "source_uri", "")
            refs_list = getattr(sym, "references", [])
            if isinstance(refs_list, list) and stable_id in refs_list:
                sym_range = getattr(sym, "selection_range", None) or getattr(sym, "full_range", None)
                if sym_range is not None:
                    changes.setdefault(other_uri, []).append(
                        TextEdit(range=sym_range, new_text=new_name)
                    )

    def _rename_dependents(self, stable_id: str, new_name: str, changes: dict[str, list[TextEdit]]) -> None:
        dep_graph = self._semantic_model.dependency_graph
        dependents = dep_graph.get_dependents(stable_id)
        for dep_node in dependents:
            dep_sym = self._semantic_model.get_symbol_by_id(dep_node.id)
            if dep_sym is not None:
                dep_range = getattr(dep_sym, "selection_range", None) or getattr(dep_sym, "full_range", None)
                if dep_range is not None:
                    dep_uri = getattr(dep_sym, "source_uri", "")
                    changes.setdefault(dep_uri, []).append(
                        TextEdit(range=dep_range, new_text=new_name)
                    )

    def _rename_registries(self, symbol: Any, new_name: str, changes: dict[str, list[TextEdit]]) -> None:
        name = getattr(symbol, "name", symbol.stable_id)
        registries = self._semantic_model.get_symbols_by_kind(SymbolKind.REGISTRY)
        for reg in registries:
            entries = getattr(reg, "entries", {})
            if isinstance(entries, dict):
                for entry_key, entry_val in entries.items():
                    if entry_key == name:
                        reg_uri = getattr(reg, "source_uri", "")
                        changes.setdefault(reg_uri, []).append(
                            TextEdit(
                                range=Range(start=Position(0, 0), end=Position(0, 0)),
                                new_text=f"# rename {name} -> {new_name} in registry",
                            )
                        )

    def _rename_agent_children(self, agent: Agent, new_name: str, changes: dict[str, list[TextEdit]]) -> None:
        children_ids = self._semantic_model.inheritance_graph.get_children(agent.stable_id)
        for child_id in children_ids:
            child = self._semantic_model.resolver.resolve_by_id(child_id)
            if child.resolved and child.symbol is not None:
                child_uri = getattr(child.symbol, "source_uri", "")
                parent_range = getattr(child.symbol, "selection_range", None) or getattr(child.symbol, "full_range", None)
                if parent_range is not None:
                    changes.setdefault(child_uri, []).append(
                        TextEdit(range=parent_range, new_text=new_name)
                    )

    def _rename_in_expressions(self, stable_id: str, old_name: str, new_name: str, changes: dict[str, list[TextEdit]]) -> None:
        all_symbols = self._semantic_model.symbol_table.all_symbols()
        for sym in all_symbols:
            doc = getattr(sym, "documentation", "") or ""
            if old_name in doc:
                pass

    def _use_v1(self) -> bool:
        try:
            from lsprotocol.types import AnnotatedTextEdit
            return True
        except ImportError:
            return False
