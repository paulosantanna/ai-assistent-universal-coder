from __future__ import annotations

import json
import threading
from typing import Any

from lsprotocol.types import (
    CodeAction,
    CodeActionContext,
    CodeActionKind,
    CodeActionParams,
    Command,
    Diagnostic,
    DiagnosticSeverity,
    Position,
    Range,
    TextEdit,
    WorkspaceEdit,
)
from pygls.lsp.server import LanguageServer

from aeos_lsp.semantic.semantic_model import SemanticModel


_AEOS_ACTION_KINDS: dict[str, str] = {
    "add_registration": "aeos.addRegistration",
    "fix_reference": "aeos.fixReference",
    "create_stub": "aeos.createStub",
    "add_timeout": "aeos.addTimeout",
    "add_retry_limit": "aeos.addRetryLimit",
    "add_rollback": "aeos.addRollback",
    "add_approval": "aeos.addApproval",
    "add_evidence": "aeos.addEvidenceRequirement",
    "fix_token_budget": "aeos.fixTokenBudget",
    "migrate_deprecated": "aeos.migrateDeprecatedField",
    "normalize_front_matter": "aeos.normalizeFrontMatter",
    "sort_keys": "aeos.sortKeys",
    "deduplicate_registry": "aeos.deduplicateRegistryEntry",
    "fix_relative_path": "aeos.fixRelativePath",
    "add_default_exclusions": "aeos.addDefaultExclusions",
    "suppress_diagnostic": "aeos.suppressDiagnostic",
    "open_docs": "aeos.openDiagnosticDocumentation",
}


class CodeActionsFeature:
    def __init__(self, server: LanguageServer, semantic_model: SemanticModel) -> None:
        self._server = server
        self._semantic_model = semantic_model
        self._lock = threading.RLock()

    def provide_code_actions(self, params: CodeActionParams) -> list[CodeAction | Command] | None:
        uri = params.text_document.uri
        diagnostics = params.context.diagnostics
        range_ = params.range

        with self._lock:
            actions: list[CodeAction] = []

            doc = self._server.workspace.text_documents.get(uri)
            if doc is None:
                return None
            text = doc.source

            for diagnostic in diagnostics:
                actions.extend(self._actions_for_diagnostic(diagnostic, uri, text))

            actions.extend(self._generic_actions(uri, range_, text))

            return actions if actions else None

    def _actions_for_diagnostic(self, diagnostic: Diagnostic, uri: str, text: str) -> list[CodeAction]:
        actions: list[CodeAction] = []
        code = diagnostic.code
        if not isinstance(code, str):
            return actions

        prefix = "Add missing registration"
        if "unresolved" in code.lower() or "missing" in code.lower():
            if "registration" in code.lower() or "registry" in code.lower():
                actions.append(self._make_action(
                    title=f"{prefix} for '{diagnostic.message}'",
                    kind=CodeActionKind.QuickFix,
                    diagnostic=diagnostic,
                    command=Command(
                        title=prefix,
                        command=_AEOS_ACTION_KINDS["add_registration"],
                        arguments=[uri, diagnostic.message, diagnostic.range],
                    ),
                ))

            actions.append(self._make_action(
                title=f"Fix reference: {diagnostic.message}",
                kind=CodeActionKind.QuickFix,
                diagnostic=diagnostic,
                command=Command(
                    title="Fix reference",
                    command=_AEOS_ACTION_KINDS["fix_reference"],
                    arguments=[uri, diagnostic.range],
                ),
            ))

        if "timeout" in code.lower():
            actions.append(self._make_action(
                title="Add timeout configuration",
                kind=CodeActionKind.QuickFix,
                diagnostic=diagnostic,
                command=Command(
                    title="Add timeout",
                    command=_AEOS_ACTION_KINDS["add_timeout"],
                    arguments=[uri, diagnostic.range],
                ),
            ))

        if "retry" in code.lower():
            actions.append(self._make_action(
                title="Add retry limit",
                kind=CodeActionKind.QuickFix,
                diagnostic=diagnostic,
                command=Command(
                    title="Add retry limit",
                    command=_AEOS_ACTION_KINDS["add_retry_limit"],
                    arguments=[uri, diagnostic.range],
                ),
            ))

        if "rollback" in code.lower():
            actions.append(self._make_action(
                title="Add rollback plan",
                kind=CodeActionKind.QuickFix,
                diagnostic=diagnostic,
                command=Command(
                    title="Add rollback",
                    command=_AEOS_ACTION_KINDS["add_rollback"],
                    arguments=[uri, diagnostic.range],
                ),
            ))

        if "approval" in code.lower():
            actions.append(self._make_action(
                title="Add approval requirement",
                kind=CodeActionKind.QuickFix,
                diagnostic=diagnostic,
                command=Command(
                    title="Add approval",
                    command=_AEOS_ACTION_KINDS["add_approval"],
                    arguments=[uri, diagnostic.range],
                ),
            ))

        if "evidence" in code.lower():
            actions.append(self._make_action(
                title="Add evidence requirement",
                kind=CodeActionKind.QuickFix,
                diagnostic=diagnostic,
                command=Command(
                    title="Add evidence requirement",
                    command=_AEOS_ACTION_KINDS["add_evidence"],
                    arguments=[uri, diagnostic.range],
                ),
            ))

        if "token_budget" in code.lower() or "token" in code.lower():
            actions.append(self._make_action(
                title="Fix token budget configuration",
                kind=CodeActionKind.QuickFix,
                diagnostic=diagnostic,
                command=Command(
                    title="Fix token budget",
                    command=_AEOS_ACTION_KINDS["fix_token_budget"],
                    arguments=[uri, diagnostic.range],
                ),
            ))

        if "deprecated" in code.lower():
            actions.append(self._make_action(
                title="Migrate deprecated field",
                kind=CodeActionKind.QuickFix,
                diagnostic=diagnostic,
                command=Command(
                    title="Migrate deprecated field",
                    command=_AEOS_ACTION_KINDS["migrate_deprecated"],
                    arguments=[uri, diagnostic.message, diagnostic.range],
                ),
            ))

        if "relative_path" in code.lower() or "path" in code.lower():
            actions.append(self._make_action(
                title="Fix relative path",
                kind=CodeActionKind.QuickFix,
                diagnostic=diagnostic,
                command=Command(
                    title="Fix relative path",
                    command=_AEOS_ACTION_KINDS["fix_relative_path"],
                    arguments=[uri, diagnostic.range],
                ),
            ))

        if diagnostic.severity is not None and diagnostic.severity <= DiagnosticSeverity.Warning:
            actions.append(self._make_action(
                title=f"Suppress diagnostic '{code}': {diagnostic.message[:40]}...",
                kind=CodeActionKind.QuickFix,
                diagnostic=diagnostic,
                command=Command(
                    title="Suppress diagnostic",
                    command=_AEOS_ACTION_KINDS["suppress_diagnostic"],
                    arguments=[uri, code, diagnostic.message],
                ),
            ))

        actions.append(self._make_action(
            title=f"Open documentation for '{code}'",
            kind=CodeActionKind.QuickFix,
            diagnostic=diagnostic,
            command=Command(
                title="Open documentation",
                command=_AEOS_ACTION_KINDS["open_docs"],
                arguments=[code],
            ),
        ))

        return actions

    def _generic_actions(self, uri: str, range_: Range, text: str) -> list[CodeAction]:
        actions: list[CodeAction] = []

        actions.append(self._make_code_action(
            title="Normalize front matter",
            kind=CodeActionKind.Refactor,
            edit=self._normalize_front_matter(text, uri, range_),
        ))
        actions.append(self._make_code_action(
            title="Sort keys alphabetically",
            kind=CodeActionKind.Refactor,
            edit=self._sort_keys(text, uri, range_),
        ))
        actions.append(self._make_code_action(
            title="Add default exclusions",
            kind=CodeActionKind.Refactor,
            edit=self._add_default_exclusions(text, uri, range_),
        ))
        actions.append(self._make_code_action(
            title="Create stub agent",
            kind=CodeActionKind.QuickFix,
            command=Command(
                title="Create stub",
                command=_AEOS_ACTION_KINDS["create_stub"],
                arguments=[uri, "agent", range_],
            ),
        ))
        actions.append(self._make_code_action(
            title="Create stub skill",
            kind=CodeActionKind.QuickFix,
            command=Command(
                title="Create stub",
                command=_AEOS_ACTION_KINDS["create_stub"],
                arguments=[uri, "skill", range_],
            ),
        ))
        actions.append(self._make_code_action(
            title="Create stub playbook",
            kind=CodeActionKind.QuickFix,
            command=Command(
                title="Create stub",
                command=_AEOS_ACTION_KINDS["create_stub"],
                arguments=[uri, "playbook", range_],
            ),
        ))

        return actions

    def _normalize_front_matter(self, text: str, uri: str, range_: Range) -> WorkspaceEdit:
        lines = text.splitlines(keepends=True)
        edits: list[TextEdit] = []
        if lines and lines[0].strip() == "---":
            edits.append(TextEdit(
                range=Range(
                    start=Position(line=0, character=0),
                    end=Position(line=0, character=3),
                ),
                new_text="---",
            ))
        return WorkspaceEdit(changes={uri: edits}) if edits else WorkspaceEdit(changes=None)

    def _sort_keys(self, text: str, uri: str, range_: Range) -> WorkspaceEdit:
        lines = text.splitlines(keepends=True)
        start_line = range_.start.line
        end_line = min(range_.end.line + 1, len(lines))
        target_lines = lines[start_line:end_line]

        key_value_pairs: list[tuple[int, str, str]] = []
        for i, line in enumerate(target_lines):
            if ":" in line and not line.strip().startswith("#") and not line.strip().startswith("-"):
                key = line.split(":", 1)[0].strip()
                key_value_pairs.append((i, key, line))

        if len(key_value_pairs) < 2:
            return WorkspaceEdit(changes=None)

        sorted_pairs = sorted(key_value_pairs, key=lambda x: x[1])
        if sorted_pairs == key_value_pairs:
            return WorkspaceEdit(changes=None)

        edits: list[TextEdit] = []
        for orig_idx, sorted_idx in enumerate([p[0] for p in sorted_pairs]):
            if orig_idx != target_lines.index(key_value_pairs[sorted_idx][2]):
                pass

        return WorkspaceEdit(changes=None)

    def _add_default_exclusions(self, text: str, uri: str, range_: Range) -> WorkspaceEdit:
        edit = TextEdit(
            range=Range(
                start=Position(line=range_.end.line, character=0),
                end=Position(line=range_.end.line, character=0),
            ),
            new_text="\nexclusions:\n  - .git\n  - node_modules\n  - .venv\n  - __pycache__\n",
        )
        return WorkspaceEdit(changes={uri: [edit]})

    def _make_action(
        self,
        title: str,
        kind: str,
        diagnostic: Diagnostic,
        command: Command | None = None,
        edit: WorkspaceEdit | None = None,
    ) -> CodeAction:
        return CodeAction(
            title=title,
            kind=kind,
            diagnostics=[diagnostic],
            command=command,
            edit=edit,
            is_preferred=False,
        )

    def _make_code_action(
        self,
        title: str,
        kind: str,
        command: Command | None = None,
        edit: WorkspaceEdit | None = None,
    ) -> CodeAction:
        return CodeAction(
            title=title,
            kind=kind,
            command=command,
            edit=edit,
            is_preferred=False,
        )
