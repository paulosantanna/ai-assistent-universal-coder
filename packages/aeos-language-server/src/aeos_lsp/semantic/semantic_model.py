from __future__ import annotations

import threading
from dataclasses import dataclass, field
from typing import Any

from lsprotocol.types import Position, Range

from aeos_lsp.parsing.base import ParseResult
from aeos_lsp.parsing.yaml_parser import AeoSDocumentType, YamlDocument
from aeos_lsp.semantic.dependency_graph import DependencyGraph, DependencyNode
from aeos_lsp.semantic.inheritance_graph import InheritanceGraph
from aeos_lsp.semantic.models import (
    Agent,
    AgentLayer,
    ApprovalRequirement,
    Artifact,
    Command,
    Dependency,
    DeprecationStatus,
    EvidenceRequirement,
    ExecutionTarget,
    Input,
    JudgeRule,
    ModelProfile,
    Output,
    Permission,
    Playbook,
    PlaybookStep,
    Policy,
    QualityGate,
    Registry,
    Repository,
    RollbackDefinition,
    Skill,
    SymbolKind,
    TokenBudget,
    Tool,
    Variable,
    Visibility,
    Workspace,
)
from aeos_lsp.semantic.references import (
    Reference,
    ReferenceKind,
    ReferenceRole,
    ReferenceTable,
)
from aeos_lsp.semantic.resolver import CrossReferenceResolver, ResolutionResult
from aeos_lsp.semantic.scopes import Scope, ScopeKind, ScopeTree
from aeos_lsp.semantic.symbols import SemanticSymbol, SymbolTable, accept_visitor
from aeos_lsp.workspace.manager import WorkspaceManager


class ReadWriteLock:
    def __init__(self) -> None:
        self._lock = threading.Lock()
        self._rcond = threading.Condition(self._lock)
        self._wcond = threading.Condition(self._lock)
        self._readers = 0
        self._writers = 0
        self._pending_writers = 0

    def acquire_read(self) -> None:
        with self._lock:
            while self._writers > 0 or self._pending_writers > 0:
                self._rcond.wait()
            self._readers += 1

    def release_read(self) -> None:
        with self._lock:
            self._readers -= 1
            if self._readers == 0:
                self._wcond.notify_all()

    def acquire_write(self) -> None:
        with self._lock:
            self._pending_writers += 1
            while self._readers > 0 or self._writers > 0:
                self._wcond.wait()
            self._pending_writers -= 1
            self._writers += 1

    def release_write(self) -> None:
        with self._lock:
            self._writers -= 1
            self._rcond.notify_all()
            self._wcond.notify_all()

    def __enter__(self) -> None:
        self.acquire_write()

    def __exit__(self, *args: Any) -> None:
        self.release_write()

    def read(self) -> "_ReadLock":
        return _ReadLock(self)


class _ReadLock:
    def __init__(self, rwlock: ReadWriteLock) -> None:
        self._rwlock = rwlock

    def __enter__(self) -> None:
        self._rwlock.acquire_read()

    def __exit__(self, *args: Any) -> None:
        self._rwlock.release_read()


@dataclass
class HoverContent:
    contents: str
    range: Range | None = None


@dataclass
class CompletionItem:
    label: str
    kind: SymbolKind = SymbolKind.UNKNOWN
    detail: str = ""
    documentation: str = ""
    insert_text: str = ""
    stable_id: str = ""


class SemanticModel:
    def __init__(self) -> None:
        self._lock = ReadWriteLock()
        self._symbol_table = SymbolTable()
        self._reference_table = ReferenceTable()
        self._resolver = CrossReferenceResolver(self._symbol_table)
        self._scope_tree = ScopeTree()
        self._dependency_graph = DependencyGraph()
        self._inheritance_graph = InheritanceGraph()
        self._workspace: Workspace | None = None
        self._repositories: dict[str, Repository] = {}

    @property
    def symbol_table(self) -> SymbolTable:
        return self._symbol_table

    @property
    def reference_table(self) -> ReferenceTable:
        return self._reference_table

    @property
    def resolver(self) -> CrossReferenceResolver:
        return self._resolver

    @property
    def scope_tree(self) -> ScopeTree:
        return self._scope_tree

    @property
    def dependency_graph(self) -> DependencyGraph:
        return self._dependency_graph

    @property
    def inheritance_graph(self) -> InheritanceGraph:
        return self._inheritance_graph

    def read_lock(self) -> _ReadLock:
        return _ReadLock(self._lock)

    def build_from_workspace(self, workspace_manager: WorkspaceManager) -> None:
        with self._lock:
            self._symbol_table.clear()
            self._reference_table.clear()
            self._scope_tree.clear()
            self._dependency_graph.clear()
            self._inheritance_graph.clear()
            self._repositories.clear()

            root_uri = workspace_manager.root_uri
            if root_uri is None:
                return

            self._workspace = Workspace(
                stable_id=f"workspace:{root_uri}",
                name="AEOS Workspace",
                folders=[f.uri for f in workspace_manager.workspace_folders],
            )
            self._symbol_table.add(self._workspace)

            for folder in workspace_manager.workspace_folders:
                repo = Repository(
                    stable_id=f"repo:{folder.uri}",
                    uri=folder.uri,
                    name=folder.name,
                )
                self._repositories[folder.uri] = repo
                self._symbol_table.add(repo)

    def update_for_document(self, uri: str, parse_result: ParseResult[YamlDocument]) -> None:
        with self._lock:
            self._symbol_table.remove_by_uri(uri)
            self._reference_table.remove_for_uri(uri)
            self._resolver.invalidate_for_uri(uri)

            doc = parse_result.ast
            if not isinstance(doc, YamlDocument):
                return

            file_scope = self._scope_tree.get_or_create_file_scope(uri)
            symbols = self._extract_symbols(uri, doc, parse_result)
            for sym in symbols:
                self._symbol_table.add(sym)
                self._scope_tree.add_symbol_to_scope(uri, sym)
                self._update_graphs(sym)

    def _extract_symbols(
        self,
        uri: str,
        doc: YamlDocument,
        parse_result: ParseResult[YamlDocument],
    ) -> list[SemanticSymbol]:
        symbols: list[SemanticSymbol] = []
        raw = doc.raw_data
        if not isinstance(raw, dict):
            return symbols

        doc_type = doc.document_type

        if doc_type == AeoSDocumentType.CONFIG:
            symbols.extend(self._extract_config_symbols(uri, raw))
        elif doc_type == AeoSDocumentType.AGENT:
            symbols.extend(self._extract_agent_symbols(uri, raw))
        elif doc_type == AeoSDocumentType.SKILL:
            symbols.extend(self._extract_skill_symbols(uri, raw))
        elif doc_type == AeoSDocumentType.PLAYBOOK:
            symbols.extend(self._extract_playbook_symbols(uri, raw))
        elif doc_type == AeoSDocumentType.REGISTRY:
            symbols.extend(self._extract_registry_symbols(uri, raw))
        elif doc_type == AeoSDocumentType.PERMISSIONS:
            symbols.extend(self._extract_permission_symbols(uri, raw))
        elif doc_type == AeoSDocumentType.POLICIES:
            symbols.extend(self._extract_policy_symbols(uri, raw))
        elif doc_type == AeoSDocumentType.OVERLAY:
            symbols.extend(self._extract_overlay_symbols(uri, raw))

        return symbols

    def _extract_config_symbols(self, uri: str, raw: dict) -> list[SemanticSymbol]:
        symbols: list[SemanticSymbol] = []
        aeos_section = raw.get("aeos", {})
        if isinstance(aeos_section, dict):
            name = aeos_section.get("name", "AEOS Config")
            symbols.append(Workspace(
                stable_id=f"workspace:{uri}",
                name=str(name),
                folders=[uri],
                config=raw,
            ))
        return symbols

    def _extract_agent_symbols(self, uri: str, raw: dict) -> list[SemanticSymbol]:
        symbols: list[SemanticSymbol] = []
        agent_data = raw.get("agent") or raw.get("agents", {})
        if isinstance(agent_data, dict):
            agent = self._build_agent(uri, agent_data)
            if agent is not None:
                symbols.append(agent)
        elif isinstance(agent_data, list):
            for item in agent_data:
                if isinstance(item, dict):
                    agent = self._build_agent(uri, item)
                    if agent is not None:
                        symbols.append(agent)
        return symbols

    def _build_agent(self, uri: str, data: dict) -> Agent | None:
        name = data.get("name", "")
        if not name:
            return None
        stable_id = data.get("stable_id", f"agent:{uri}#{name}")
        layers_data = data.get("layers", [])
        layers: list[AgentLayer] = []
        if isinstance(layers_data, list):
            for i, ld in enumerate(layers_data):
                if isinstance(ld, dict):
                    layer = AgentLayer(
                        stable_id=f"{stable_id}/layer:{ld.get('name', f'layer_{i}')}",
                        name=str(ld.get("name", f"layer_{i}")),
                        skills=[str(s) for s in ld.get("skills", []) if isinstance(s, str)],
                        description=str(ld.get("description", "")),
                    )
                    layers.append(layer)

        return Agent(
            stable_id=stable_id,
            name=str(name),
            source_uri=uri,
            selection_range=self._make_range(data),
            full_range=self._make_range(data),
            documentation=str(data.get("description", data.get("documentation", ""))),
            metadata=data.get("metadata", {}),
            visibility=Visibility(data.get("visibility", "public")) if isinstance(data.get("visibility"), str) else Visibility.PUBLIC,
            deprecation=DeprecationStatus(data.get("deprecation", "current")) if isinstance(data.get("deprecation"), str) else DeprecationStatus.CURRENT,
            references=[str(r) for r in data.get("references", []) if isinstance(r, str)],
            content_hash=str(data.get("content_hash", "")),
            parent_id=str(data.get("parent", data.get("extends", ""))) or None,
            skills=[str(s) for s in data.get("skills", []) if isinstance(s, str)],
            layers=layers,
        )

    def _extract_skill_symbols(self, uri: str, raw: dict) -> list[SemanticSymbol]:
        symbols: list[SemanticSymbol] = []
        skill_data = raw.get("skill") or raw.get("skills", {})
        if isinstance(skill_data, dict):
            skill = self._build_skill(uri, skill_data)
            if skill is not None:
                symbols.append(skill)
        elif isinstance(skill_data, list):
            for item in skill_data:
                if isinstance(item, dict):
                    skill = self._build_skill(uri, item)
                    if skill is not None:
                        symbols.append(skill)
        return symbols

    def _build_skill(self, uri: str, data: dict) -> Skill | None:
        name = data.get("name", "")
        if not name:
            return None
        stable_id = data.get("stable_id", f"skill:{uri}#{name}")
        return Skill(
            stable_id=stable_id,
            name=str(name),
            source_uri=uri,
            selection_range=self._make_range(data),
            full_range=self._make_range(data),
            documentation=str(data.get("description", data.get("documentation", ""))),
            metadata=data.get("metadata", {}),
            visibility=Visibility(data.get("visibility", "public")) if isinstance(data.get("visibility"), str) else Visibility.PUBLIC,
            deprecation=DeprecationStatus(data.get("deprecation", "current")) if isinstance(data.get("deprecation"), str) else DeprecationStatus.CURRENT,
            references=[str(r) for r in data.get("references", []) if isinstance(r, str)],
            content_hash=str(data.get("content_hash", "")),
            tools=[str(t) for t in data.get("tools", []) if isinstance(t, str)],
            inputs=[str(i) for i in data.get("inputs", []) if isinstance(i, str)],
            outputs=[str(o) for o in data.get("outputs", []) if isinstance(o, str)],
        )

    def _extract_playbook_symbols(self, uri: str, raw: dict) -> list[SemanticSymbol]:
        symbols: list[SemanticSymbol] = []
        playbook_data = raw.get("playbook") or raw.get("playbooks", {})
        if isinstance(playbook_data, dict):
            pb = self._build_playbook(uri, playbook_data)
            if pb is not None:
                symbols.append(pb)
                for step_sym in self._extract_steps(uri, playbook_data, pb.stable_id):
                    symbols.append(step_sym)
        elif isinstance(playbook_data, list):
            for item in playbook_data:
                if isinstance(item, dict):
                    pb = self._build_playbook(uri, item)
                    if pb is not None:
                        symbols.append(pb)
                        for step_sym in self._extract_steps(uri, item, pb.stable_id):
                            symbols.append(step_sym)
        return symbols

    def _build_playbook(self, uri: str, data: dict) -> Playbook | None:
        name = data.get("name", "")
        if not name:
            return None
        stable_id = data.get("stable_id", f"playbook:{uri}#{name}")
        return Playbook(
            stable_id=stable_id,
            name=str(name),
            source_uri=uri,
            selection_range=self._make_range(data),
            full_range=self._make_range(data),
            documentation=str(data.get("description", data.get("documentation", ""))),
            metadata=data.get("metadata", {}),
            visibility=Visibility(data.get("visibility", "public")) if isinstance(data.get("visibility"), str) else Visibility.PUBLIC,
            deprecation=DeprecationStatus(data.get("deprecation", "current")) if isinstance(data.get("deprecation"), str) else DeprecationStatus.CURRENT,
            references=[str(r) for r in data.get("references", []) if isinstance(r, str)],
            content_hash=str(data.get("content_hash", "")),
            steps=[str(s) for s in data.get("steps", []) if isinstance(s, str)],
            variables=[str(v) for v in data.get("variables", []) if isinstance(v, str)],
        )

    def _extract_steps(self, uri: str, playbook_data: dict, playbook_id: str) -> list[PlaybookStep]:
        steps: list[PlaybookStep] = []
        steps_raw = playbook_data.get("steps", [])
        if isinstance(steps_raw, list):
            for i, s in enumerate(steps_raw):
                if isinstance(s, dict):
                    step = self._build_step(uri, s, playbook_id, i)
                    if step is not None:
                        steps.append(step)
        return steps

    def _build_step(self, uri: str, data: dict, playbook_id: str, index: int) -> PlaybookStep | None:
        name = data.get("name", data.get("step", f"step_{index}"))
        stable_id = data.get("stable_id", f"{playbook_id}/step:{name}")
        return PlaybookStep(
            stable_id=stable_id,
            name=str(name),
            step_type=str(data.get("type", data.get("step_type", ""))),
            tool=str(data.get("tool")) if data.get("tool") else None,
            skill=str(data.get("skill")) if data.get("skill") else None,
            playbook=str(data.get("playbook")) if data.get("playbook") else None,
            inputs=data.get("inputs", {}),
            outputs=data.get("outputs", {}),
            conditions=[str(c) for c in data.get("conditions", []) if isinstance(c, str)],
            timeout=data.get("timeout") if isinstance(data.get("timeout"), int) else None,
            retry=data.get("retry") if isinstance(data.get("retry"), int) else None,
            approval=bool(data.get("approval", False)),
            rollback=str(data.get("rollback")) if data.get("rollback") else None,
            executor=str(data.get("executor")) if data.get("executor") else None,
            source_uri=uri,
        )

    def _extract_registry_symbols(self, uri: str, raw: dict) -> list[SemanticSymbol]:
        symbols: list[SemanticSymbol] = []
        for key, value in raw.items():
            if isinstance(value, dict) and ("registry" in key or key.endswith(".registry") or key in ("agents", "skills", "playbooks", "mcps", "lcps", "blueprints")):
                registry = Registry(
                    stable_id=f"registry:{uri}#{key}",
                    name=str(key),
                    entries=value,
                    registry_type=str(key),
                    source_uri=uri,
                )
                symbols.append(registry)
        return symbols

    def _extract_permission_symbols(self, uri: str, raw: dict) -> list[SemanticSymbol]:
        symbols: list[SemanticSymbol] = []
        perms = raw.get("permissions", raw.get("permission", []))
        if isinstance(perms, list):
            for p in perms:
                if isinstance(p, dict):
                    symbols.append(self._build_permission(uri, p))
        elif isinstance(perms, dict):
            symbols.append(self._build_permission(uri, perms))
        return symbols

    def _build_permission(self, uri: str, data: dict) -> Permission:
        name = data.get("name", "unnamed")
        return Permission(
            stable_id=data.get("stable_id", f"permission:{uri}#{name}"),
            name=str(name),
            scopes=[str(s) for s in data.get("scopes", []) if isinstance(s, str)],
            capabilities=[str(c) for c in data.get("capabilities", []) if isinstance(c, str)],
            source_uri=uri,
        )

    def _extract_policy_symbols(self, uri: str, raw: dict) -> list[SemanticSymbol]:
        symbols: list[SemanticSymbol] = []
        policies = raw.get("policies", raw.get("policy", []))
        if isinstance(policies, list):
            for p in policies:
                if isinstance(p, dict):
                    symbols.append(self._build_policy(uri, p))
        elif isinstance(policies, dict):
            symbols.append(self._build_policy(uri, policies))
        return symbols

    def _build_policy(self, uri: str, data: dict) -> Policy:
        name = data.get("name", "unnamed")
        return Policy(
            stable_id=data.get("stable_id", f"policy:{uri}#{name}"),
            name=str(name),
            rules=data.get("rules", {}),
            source_uri=uri,
        )

    def _extract_overlay_symbols(self, uri: str, raw: dict) -> list[SemanticSymbol]:
        symbols: list[SemanticSymbol] = []
        overlay = raw.get("overlay", raw)
        if isinstance(overlay, dict):
            for key, value in overlay.items():
                if isinstance(value, dict):
                    kind = value.get("kind", "unknown")
                    name = value.get("name", key)
                    if kind == "agent":
                        agent = self._build_agent(uri, value)
                        if agent is not None:
                            symbols.append(agent)
                    elif kind == "skill":
                        skill = self._build_skill(uri, value)
                        if skill is not None:
                            symbols.append(skill)
                    elif kind == "playbook":
                        pb = self._build_playbook(uri, value)
                        if pb is not None:
                            symbols.append(pb)
        return symbols

    def _update_graphs(self, symbol: SemanticSymbol) -> None:
        kind = self._get_symbol_kind(symbol)
        sid = symbol.stable_id
        uri = getattr(symbol, "source_uri", "") or ""

        dep_node = DependencyNode(id=sid, kind=kind, uri=uri)
        self._dependency_graph.add_node(dep_node)

        if isinstance(symbol, Agent):
            if symbol.parent_id:
                self._inheritance_graph.add_relationship(sid, symbol.parent_id)
                self._dependency_graph.add_dependency(sid, symbol.parent_id)
            for skill_id in symbol.skills:
                self._dependency_graph.add_dependency(sid, skill_id)

        elif isinstance(symbol, Playbook):
            for step_id in symbol.steps:
                self._dependency_graph.add_dependency(sid, step_id)

        elif isinstance(symbol, PlaybookStep):
            if symbol.tool:
                self._dependency_graph.add_dependency(sid, f"tool:{symbol.tool}")
            if symbol.skill:
                self._dependency_graph.add_dependency(sid, f"skill:{symbol.skill}")
            if symbol.playbook:
                self._dependency_graph.add_dependency(sid, f"playbook:{symbol.playbook}")

        elif isinstance(symbol, Skill):
            for tool_ref in symbol.tools:
                self._dependency_graph.add_dependency(sid, tool_ref)

    def remove_document(self, uri: str) -> None:
        with self._lock:
            self._symbol_table.remove_by_uri(uri)
            self._reference_table.remove_for_uri(uri)
            self._scope_tree.remove_scope(uri)
            self._resolver.invalidate_for_uri(uri)

    def get_symbol(self, uri: str, position: Position) -> SemanticSymbol | None:
        with self._lock.read():
            scope = self._scope_tree.find_scope_at(uri, position)
            if scope is None:
                symbols = self._symbol_table.get_by_uri(uri)
                for sym in symbols:
                    sym_range = getattr(sym, "selection_range", None)
                    if sym_range and self._position_in_range(position, sym_range):
                        return sym
                return None
            for sym in scope.symbols:
                sym_range = getattr(sym, "selection_range", None)
                if sym_range and self._position_in_range(position, sym_range):
                    return sym
            for ancestor in scope.ancestors():
                for sym in ancestor.symbols:
                    sym_range = getattr(sym, "selection_range", None)
                    if sym_range and self._position_in_range(position, sym_range):
                        return sym
            return None

    def get_symbol_at(self, uri: str, line: int, character: int) -> SemanticSymbol | None:
        return self.get_symbol(uri, Position(line=line, character=character))

    def get_completions(self, uri: str, position: Position, context: dict[str, Any] | None = None) -> list:
        with self._lock.read():
                items: list[CompletionItem] = []
                scope = self._scope_tree.find_scope_at(uri, position)
                if scope is not None:
                    symbols_in_scope: list[SemanticSymbol] = []
                    symbols_in_scope.extend(scope.symbols)
                    for ancestor in scope.ancestors():
                        symbols_in_scope.extend(ancestor.symbols)
                    seen: set[str] = set()
                    for sym in symbols_in_scope:
                        sid = sym.stable_id
                        if sid not in seen:
                            seen.add(sid)
                            name = getattr(sym, "name", sid)
                            kind = self._get_symbol_kind(sym)
                            items.append(CompletionItem(
                                label=str(name),
                                kind=kind,
                                detail=str(getattr(sym, "documentation", "")),
                                stable_id=sid,
                            ))

                if context and context.get("include_workspace_symbols", True):
                    for sym in self._symbol_table.all_symbols():
                        sid = sym.stable_id
                        if sid not in {i.stable_id for i in items}:
                            name = getattr(sym, "name", sid)
                            kind = self._get_symbol_kind(sym)
                            items.append(CompletionItem(
                                label=str(name),
                                kind=kind,
                                stable_id=sid,
                            ))

                return items
            

    def get_hover(self, uri: str, position: Position) -> HoverContent | None:
        with self._lock.read():
                symbol = self.get_symbol(uri, position)
                if symbol is None:
                    return None

                lines: list[str] = []
                kind = self._get_symbol_kind(symbol)
                name = getattr(symbol, "name", symbol.stable_id)
                lines.append(f"**{kind.value}**: `{name}`")

                doc = getattr(symbol, "documentation", "")
                if doc:
                    lines.append("")
                    lines.append(str(doc))

                if isinstance(symbol, Agent):
                    if symbol.parent_id:
                        lines.append("")
                        lines.append(f"*Extends:* `{symbol.parent_id}`")
                    if symbol.skills:
                        lines.append("")
                        lines.append(f"*Skills:* {', '.join(symbol.skills)}")
                    lines.append(f"*Visibility:* {symbol.visibility.value}")
                    if symbol.deprecation != DeprecationStatus.CURRENT:
                        lines.append(f"*Status:* {symbol.deprecation.value}")

                if isinstance(symbol, Skill):
                    if symbol.tools:
                        lines.append("")
                        lines.append(f"*Tools:* {', '.join(symbol.tools)}")

                if isinstance(symbol, Playbook):
                    if symbol.steps:
                        lines.append("")
                        lines.append(f"*Steps:* {len(symbol.steps)}")

                if isinstance(symbol, Tool):
                    lines.append("")
                    lines.append(f"*Command:* `{symbol.command}`")
                    if symbol.mutating:
                        lines.append("*Mutating:* Yes")
                    if symbol.timeout:
                        lines.append(f"*Timeout:* {symbol.timeout}s")

                if isinstance(symbol, Variable):
                    lines.append(f"*Type:* {symbol.type_ref or 'any'}")

                if isinstance(symbol, (Input, Output)):
                    lines.append(f"*Type:* {symbol.type_ref or 'any'}")

                metadata = getattr(symbol, "metadata", {})
                if metadata:
                    lines.append("")
                    lines.append("*Metadata:*")
                    for k, v in metadata.items() if isinstance(metadata, dict) else []:
                        lines.append(f"  - {k}: {v}")

                return HoverContent(
                    contents="\n".join(lines),
                    range=getattr(symbol, "selection_range", None),
                )
            

    def get_definitions(self, uri: str, position: Position) -> list:
        with self._lock.read():
                symbol = self.get_symbol(uri, position)
                if symbol is None:
                    return []

                sid = symbol.stable_id
                defns = self._reference_table.find_definitions(sid)

                result = []
                for ref in defns:
                    result.append({
                        "uri": ref.target_uri,
                        "range": ref.target_range,
                    })

                if not result:
                    result.append({
                        "uri": getattr(symbol, "source_uri", uri),
                        "range": getattr(symbol, "selection_range", None),
                    })

                return result
            

    def get_references(self, uri: str, position: Position) -> list:
        with self._lock.read():
                symbol = self.get_symbol(uri, position)
                if symbol is None:
                    return []

                sid = symbol.stable_id
                refs = self._reference_table.find_references(sid)

                return [
                    {
                        "uri": ref.source_uri,
                        "range": ref.source_range,
                        "kind": ref.kind.value,
                        "role": ref.role.value,
                    }
                    for ref in refs
                ]
            

    def get_symbol_by_id(self, stable_id: str) -> SemanticSymbol | None:
        with self._lock.read():
                return self._symbol_table.get(stable_id)
            

    def get_symbols_by_kind(self, kind: SymbolKind) -> list[SemanticSymbol]:
        with self._lock.read():
                return self._symbol_table.get_by_kind(kind)
            

    def get_symbols_by_uri(self, uri: str) -> list[SemanticSymbol]:
        with self._lock.read():
                return self._symbol_table.get_by_uri(uri)
            

    def get_workspace(self) -> Workspace | None:
        with self._lock.read():
                return self._workspace
            

    def get_repositories(self) -> list[Repository]:
        with self._lock.read():
                return list(self._repositories.values())
            

    def has_cycles(self) -> bool:
        with self._lock.read():
                return self._dependency_graph.has_cycle() or self._inheritance_graph.has_cycle()
            

    def impact_of_change(self, changed_uris: set[str]) -> dict[str, list[str]]:
        with self._lock.read():
                changed_ids: set[str] = set()
                for changed_uri in changed_uris:
                    symbols = self._symbol_table.get_by_uri(changed_uri)
                    for sym in symbols:
                        changed_ids.add(sym.stable_id)
                return self._dependency_graph.impact_analysis(changed_ids)
            

    def clear(self) -> None:
        with self._lock:
            self._symbol_table.clear()
            self._reference_table.clear()
            self._scope_tree.clear()
            self._dependency_graph.clear()
            self._inheritance_graph.clear()
            self._resolver.clear_cache()
            self._workspace = None
            self._repositories.clear()

    def _make_range(self, data: dict) -> Range:
        try:
            line = int(data.get("_line", 0))
            col = int(data.get("_column", 0))
            end_line = int(data.get("_end_line", line))
            end_col = int(data.get("_end_column", col + 1))
            return Range(
                start=Position(line=line, character=col),
                end=Position(line=end_line, character=end_col),
            )
        except (ValueError, TypeError):
            return Range(start=Position(line=0, character=0), end=Position(line=0, character=0))

    @staticmethod
    def _position_in_range(position: Position, range_: Range) -> bool:
        if position.line < range_.start.line:
            return False
        if position.line > range_.end.line:
            return False
        if position.line == range_.start.line and position.character < range_.start.character:
            return False
        if position.line == range_.end.line and position.character > range_.end.character:
            return False
        return True

    @staticmethod
    def _get_symbol_kind(symbol: SemanticSymbol) -> SymbolKind:
        if hasattr(symbol, "symbol_kind"):
            return symbol.symbol_kind
        if hasattr(symbol, "kind"):
            return symbol.kind
        return SymbolKind.UNKNOWN
