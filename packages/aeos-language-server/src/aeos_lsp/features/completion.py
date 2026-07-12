from __future__ import annotations

import re
import threading
from dataclasses import dataclass, field
from typing import Any

from lsprotocol.types import (
    CompletionItem,
    CompletionItemKind,
    CompletionList,
    CompletionParams,
    InsertTextFormat,
    Position,
    Range,
    TextEdit,
)
from pygls.lsp.server import LanguageServer

from aeos_lsp.configuration import LSPClientConfig
from aeos_lsp.constants import MAX_COMPLETION_ITEMS_DEFAULT
from aeos_lsp.parsing.dispatcher import AEOSDocumentType
from aeos_lsp.semantic.models import SymbolKind
from aeos_lsp.semantic.semantic_model import SemanticModel
from aeos_lsp.semantic.symbols import SemanticSymbol


class _ContextKind:
    FRONT_MATTER = "front_matter"
    BODY = "body"
    EXPRESSION = "expression"
    DIRECTIVE = "directive"
    VALUE = "value"
    KEY = "key"
    UNKNOWN = "unknown"


@dataclass
class _CompletionContext:
    kind: str = _ContextKind.UNKNOWN
    prefix: str = ""
    path: list[str] = field(default_factory=list)
    parent_key: str = ""
    line_text: str = ""
    column: int = 0


_AEOS_DIRECTIVES = frozenset({
    "@agent", "@skill", "@playbook", "@tool", "@policy", "@permission",
    "@evidence", "@gate", "@model", "@step", "@variable", "@input",
    "@output", "@dependency", "@rollback",
})

_AEOS_TOP_LEVEL_KEYS: dict[str, set[str]] = {
    "config": {"aeos", "runtime", "registries", "execution", "security", "judge", "packaging", "observability"},
    "agent": {"agent", "name", "stable_id", "description", "visibility", "deprecation",
              "parent", "extends", "skills", "layers", "metadata", "model", "token_budget",
              "timeout", "retry", "approval", "evidence", "rollback"},
    "skill": {"skill", "name", "stable_id", "description", "visibility", "deprecation",
              "tools", "inputs", "outputs", "model", "token_budget", "timeout",
              "metadata", "evidence", "rollback"},
    "playbook": {"playbook", "name", "stable_id", "description", "visibility", "deprecation",
                 "steps", "variables", "inputs", "outputs", "metadata",
                 "timeout", "retry", "approval", "rollback"},
}

_AEOS_ENUM_VALUES: dict[str, list[str]] = {
    "visibility": ["public", "private", "internal", "restricted"],
    "deprecation": ["current", "deprecated", "removed", "experimental", "superseded"],
    "mode": ["ai-first-governed", "human-review", "fully-automated", "dry-run-only"],
    "transport": ["stdio", "streamable_http"],
    "log_level": ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
    "severity": ["error", "warning", "info", "hint"],
}

_AEOS_EXPRESSION_KEYWORDS = frozenset({
    "true", "false", "null", "and", "or", "not", "in", "if", "else",
    "then", "for", "each", "as", "import", "from", "return", "let",
    "match", "case", "when", "try", "catch", "finally",
})

_AEOS_POLICY_NAMES = frozenset({
    "require_evidence", "require_judge", "require_rollback_plan",
    "require_test_evidence", "require_branch_for_code_changes",
    "require_diff_summary", "require_approval",
    "block_plaintext_secrets", "block_secret_logging",
    "block_auto_deploy", "block_auto_merge",
    "block_wildcard_approval", "block_unverified_package_extract",
})

_AEOS_EVIDENCE_TYPES = frozenset({
    "tool_calls", "mcp_calls", "permission_decisions", "policy_decisions",
    "hash_outputs", "judge_report", "test_results", "coverage_report",
    "lint_report", "scan_report", "audit_log",
})

_AEOS_GATE_TYPES = frozenset({
    "quality_gate", "security_gate", "compliance_gate", "performance_gate",
    "approval_gate", "evidence_gate", "judge_gate",
})

_AEOS_PERMISSION_SCOPES = frozenset({
    "read", "write", "execute", "admin", "deploy", "audit",
    "read:tools", "write:tools", "execute:tools",
    "read:agents", "write:agents",
    "read:playbooks", "write:playbooks", "execute:playbooks",
    "read:skills", "write:skills", "execute:skills",
    "read:policies", "write:policies",
    "read:secrets", "write:secrets",
})

_AEOS_SNIPPETS: list[tuple[str, str, str]] = [
    ("agent", "agent:\n  name: ${1:agent_name}\n  description: ${2:description}\n  skills:\n    - ${3:skill_id}", "New agent definition"),
    ("skill", "skill:\n  name: ${1:skill_name}\n  description: ${2:description}\n  tools:\n    - ${3:tool_id}", "New skill definition"),
    ("playbook", "playbook:\n  name: ${1:playbook_name}\n  description: ${2:description}\n  steps:\n    - name: ${3:step_name}\n      skill: ${4:skill_id}", "New playbook definition"),
    ("step", "  - name: ${1:step_name}\n    skill: ${2:skill_id}\n    inputs:\n      ${3:key}: ${4:value}\n    timeout: ${5:30}\n    retry: ${6:3}\n    rollback: ${7:rollback_id}", "New playbook step"),
    ("variable", "  - name: ${1:var_name}\n    type: ${2:string}\n    default: ${3:default_value}", "New variable definition"),
    ("input", "  - name: ${1:input_name}\n    type: ${2:string}\n    required: ${3:true}", "New input definition"),
    ("output", "  - name: ${1:output_name}\n    type: ${2:string}\n    description: ${3:description}", "New output definition"),
    ("layer", "  - name: ${1:layer_name}\n    description: ${2:description}\n    skills:\n      - ${3:skill_id}", "New agent layer"),
    ("policy_rule", "  - name: ${1:rule_name}\n    condition: \"${2:condition}\"\n    action: ${3:block}", "New policy rule"),
    ("rollback", "rollback:\n  name: ${1:rollback_name}\n  steps:\n    - ${2:step_name}\n  strategy: ${3:sequential}", "New rollback definition"),
    ("permission", "  - name: ${1:permission_name}\n    scopes:\n      - ${2:read}\n    capabilities:\n      - ${3:execute}", "New permission entry"),
]


class CompletionFeature:
    def __init__(self, server: LanguageServer, semantic_model: SemanticModel) -> None:
        self._server = server
        self._semantic_model = semantic_model
        self._lock = threading.RLock()

    def _detect_context(self, params: CompletionParams, text: str) -> _CompletionContext:
        ctx = _CompletionContext()
        pos = params.position
        lines = text.splitlines(keepends=False)
        if pos.line >= len(lines):
            return ctx
        ctx.line_text = lines[pos.line]
        ctx.column = pos.character

        line_before = ctx.line_text[:pos.character]
        stripped = ctx.line_text.strip()

        if stripped.startswith("@"):
            ctx.kind = _ContextKind.DIRECTIVE
            ctx.prefix = stripped.lstrip("@")
            return ctx

        if "${" in stripped or "{{" in stripped:
            ctx.kind = _ContextKind.EXPRESSION
            expr_match = re.search(r"\$\{([^}]*)\}$", line_before)
            if expr_match:
                ctx.prefix = expr_match.group(1)
            return ctx

        if stripped == "---" or (pos.line < 2 and "---" in lines[0] if lines else False):
            ctx.kind = _ContextKind.FRONT_MATTER
            return ctx

        if ":" in line_before:
            parts = line_before.rsplit(":", 1)
            if not parts[1].strip():
                ctx.kind = _ContextKind.VALUE
                ctx.parent_key = parts[0].strip().split()[-1] if parts[0].strip() else ""
                indent_match = re.match(r"^(\s*)", ctx.line_text)
                if indent_match:
                    ctx.path = self._compute_path(lines, pos.line, len(indent_match.group(1)))
                return ctx

        if ":" not in stripped and stripped and not stripped.startswith("-") and not stripped.startswith("#"):
            ctx.kind = _ContextKind.KEY
            indent_match = re.match(r"^(\s*)", ctx.line_text)
            if indent_match:
                ctx.path = self._compute_path(lines, pos.line, len(indent_match.group(1)))
            ctx.prefix = stripped.split(":")[0] if ":" in stripped else stripped
            return ctx

        return ctx

    def _compute_path(self, lines: list[str], current_line: int, indent: int) -> list[str]:
        path: list[str] = []
        for i in range(current_line - 1, -1, -1):
            line = lines[i]
            if not line.strip() or line.strip().startswith("#"):
                continue
            line_indent = len(line) - len(line.lstrip())
            if line_indent < indent and ":" in line:
                key = line.strip().split(":")[0].lstrip("-").strip()
                path.insert(0, key)
                indent = line_indent
        return path

    def _build_completion_item(
        self,
        label: str,
        kind: CompletionItemKind,
        detail: str = "",
        documentation: str = "",
        insert_text: str = "",
        insert_text_format: InsertTextFormat = InsertTextFormat.PlainText,
        filter_text: str = "",
        score: float = 0.0,
    ) -> tuple[CompletionItem, float]:
        item = CompletionItem(
            label=label,
            kind=kind,
            detail=detail,
            documentation=documentation,
            insert_text=insert_text or label,
            insert_text_format=insert_text_format,
            filter_text=filter_text or label,
        )
        return (item, score)

    def _add_directive_completions(self, ctx: _CompletionContext, items: list[CompletionItem], scores: list[float]) -> None:
        for directive in sorted(_AEOS_DIRECTIVES):
            label = directive.lstrip("@")
            if ctx.prefix and not label.startswith(ctx.prefix):
                continue
            item, score = self._build_completion_item(
                label=directive,
                kind=CompletionItemKind.Keyword,
                detail=f"AEOS directive",
                insert_text=directive,
                score=25.0 if label.startswith(ctx.prefix) else 10.0,
            )
            items.append(item)
            scores.append(score)

    def _add_expression_completions(self, ctx: _CompletionContext, items: list[CompletionItem], scores: list[float]) -> None:
        for kw in sorted(_AEOS_EXPRESSION_KEYWORDS):
            if ctx.prefix and not kw.startswith(ctx.prefix):
                continue
            item, score = self._build_completion_item(
                label=kw,
                kind=CompletionItemKind.Keyword,
                detail="expression keyword",
                score=20.0 if kw.startswith(ctx.prefix) else 5.0,
            )
            items.append(item)
            scores.append(score)

    def _add_key_completions(self, ctx: _CompletionContext, items: list[CompletionItem], scores: list[float]) -> None:
        doc_type = self._detect_doc_type(ctx)
        keys = _AEOS_TOP_LEVEL_KEYS.get(doc_type, set())
        for key in sorted(keys):
            if ctx.prefix and not key.startswith(ctx.prefix):
                continue
            item, score = self._build_completion_item(
                label=key,
                kind=CompletionItemKind.Property,
                detail=f"{doc_type} field",
                insert_text=f"{key}: ",
                score=30.0 if key.startswith(ctx.prefix) else 10.0,
            )
            items.append(item)
            scores.append(score)

    def _detect_doc_type(self, ctx: _CompletionContext) -> str:
        for p in ctx.path:
            if p in ("agent", "agents"):
                return "agent"
            if p in ("skill", "skills"):
                return "skill"
            if p in ("playbook", "playbooks"):
                return "playbook"
            if p in ("aeos", "config"):
                return "config"
        return "config"

    def _add_value_completions(self, ctx: _CompletionContext, items: list[CompletionItem], scores: list[float]) -> None:
        parent = ctx.parent_key
        if parent in _AEOS_ENUM_VALUES:
            for val in _AEOS_ENUM_VALUES[parent]:
                item, score = self._build_completion_item(
                    label=val,
                    kind=CompletionItemKind.EnumMember,
                    detail=f"enum value for {parent}",
                    score=30.0,
                )
                items.append(item)
                scores.append(score)
            return

        if parent == "policy" or parent.startswith("policy"):
            for pname in sorted(_AEOS_POLICY_NAMES):
                if ctx.prefix and not pname.startswith(ctx.prefix):
                    continue
                item, score = self._build_completion_item(
                    label=pname,
                    kind=CompletionItemKind.Property,
                    detail="policy name",
                    score=20.0,
                )
                items.append(item)
                scores.append(score)
        elif parent == "evidence":
            for ev in sorted(_AEOS_EVIDENCE_TYPES):
                if ctx.prefix and not ev.startswith(ctx.prefix):
                    continue
                item, score = self._build_completion_item(
                    label=ev,
                    kind=CompletionItemKind.Property,
                    detail="evidence type",
                    score=20.0,
                )
                items.append(item)
                scores.append(score)
        elif parent == "gate":
            for gt in sorted(_AEOS_GATE_TYPES):
                if ctx.prefix and not gt.startswith(ctx.prefix):
                    continue
                item, score = self._build_completion_item(
                    label=gt,
                    kind=CompletionItemKind.Property,
                    detail="gate type",
                    score=20.0,
                )
                items.append(item)
                scores.append(score)
        elif parent == "scope" or "scope" in parent.lower():
            for sc in sorted(_AEOS_PERMISSION_SCOPES):
                if ctx.prefix and not sc.startswith(ctx.prefix):
                    continue
                item, score = self._build_completion_item(
                    label=sc,
                    kind=CompletionItemKind.EnumMember,
                    detail="permission scope",
                    score=20.0,
                )
                items.append(item)
                scores.append(score)

    def _add_symbol_completions(
        self,
        ctx: _CompletionContext,
        kind: SymbolKind,
        items: list[CompletionItem],
        scores: list[float],
        uri: str,
    ) -> None:
        symbols = self._semantic_model.get_symbols_by_kind(kind)
        for sym in symbols:
            name = getattr(sym, "name", sym.stable_id)
            if ctx.prefix and not name.startswith(ctx.prefix):
                continue
            sid = sym.stable_id
            src_uri = getattr(sym, "source_uri", "")
            is_local = src_uri == uri
            completion_kind = self._symbol_kind_to_completion_kind(kind)
            item_kind = CompletionItemKind.Reference if completion_kind == -1 else completion_kind
            detail = f"({kind.value}) {sid}"
            doc = getattr(sym, "documentation", "") or getattr(sym, "description", "")
            score = 40.0 if is_local else 20.0
            if name.startswith(ctx.prefix):
                score += 10.0
            item, score_val = self._build_completion_item(
                label=name,
                kind=item_kind,
                detail=detail,
                documentation=str(doc)[:200] if doc else "",
                score=score,
            )
            items.append(item)
            scores.append(score_val)

    def _add_snippet_completions(self, ctx: _CompletionContext, items: list[CompletionItem], scores: list[float]) -> None:
        for trigger, snippet, desc in _AEOS_SNIPPETS:
            if ctx.prefix and not trigger.startswith(ctx.prefix):
                continue
            item, score = self._build_completion_item(
                label=trigger,
                kind=CompletionItemKind.Snippet,
                detail=desc,
                insert_text=snippet,
                insert_text_format=InsertTextFormat.Snippet,
                score=35.0 if trigger.startswith(ctx.prefix) else 15.0,
            )
            items.append(item)
            scores.append(score)

    def _add_model_completions(self, ctx: _CompletionContext, items: list[CompletionItem], scores: list[float]) -> None:
        models = self._semantic_model.get_symbols_by_kind(SymbolKind.MODEL_PROFILE)
        for model in models:
            name = getattr(model, "name", model.stable_id)
            if ctx.prefix and not name.startswith(ctx.prefix):
                continue
            provider = getattr(model, "provider", "")
            ctx_window = getattr(model, "context_window", 0)
            detail = f"model ({provider}) ctx={ctx_window}" if provider else "model profile"
            item, score = self._build_completion_item(
                label=name,
                kind=CompletionItemKind.Class,
                detail=detail,
                score=25.0 if name.startswith(ctx.prefix) else 15.0,
            )
            items.append(item)
            scores.append(score)

    def _add_token_budget_completions(self, ctx: _CompletionContext, items: list[CompletionItem], scores: list[float]) -> None:
        budgets = self._semantic_model.get_symbols_by_kind(SymbolKind.TOKEN_BUDGET)
        for budget in budgets:
            name = getattr(budget, "name", budget.stable_id)
            if ctx.prefix and not name.startswith(ctx.prefix):
                continue
            max_tokens = getattr(budget, "max_total_tokens", 0)
            detail = f"token budget (max={max_tokens})" if max_tokens else "token budget"
            item, score = self._build_completion_item(
                label=name,
                kind=CompletionItemKind.Constant,
                detail=detail,
                score=25.0 if name.startswith(ctx.prefix) else 15.0,
            )
            items.append(item)
            scores.append(score)

    def _add_workspace_path_completions(self, ctx: _CompletionContext, items: list[CompletionItem], scores: list[float]) -> None:
        ws = self._semantic_model.get_workspace()
        if ws is not None and ws.folders:
            root = ws.folders[0]
            if ctx.prefix:
                completions = self._suggest_paths(root, ctx.prefix)
                for path, is_dir in completions:
                    item, score = self._build_completion_item(
                        label=path,
                        kind=CompletionItemKind.File if not is_dir else CompletionItemKind.Folder,
                        detail="directory" if is_dir else "file",
                        score=10.0,
                    )
                    items.append(item)
                    scores.append(score)

    def _suggest_paths(self, root_uri: str, prefix: str) -> list[tuple[str, bool]]:
        try:
            from pathlib import Path
            root_path = Path(root_uri.replace("file://", "").replace("\\", "/"))

            import os
            if not os.path.isdir(root_path):
                return []

            suggestions: list[tuple[str, bool]] = []
            base_dir = root_path
            if "/" in prefix.rstrip("/"):
                parent_part = prefix.rsplit("/", 1)[0]
                file_part = prefix.rsplit("/", 1)[1] if "/" in prefix else prefix
                base_dir = root_path / parent_part.lstrip("/")
                prefix_part = file_part
            else:
                prefix_part = prefix

            if not os.path.isdir(base_dir):
                return []

            for entry in sorted(os.listdir(base_dir)):
                if entry.startswith(".") or entry.startswith("__"):
                    continue
                if prefix_part and not entry.startswith(prefix_part):
                    continue
                full_path = str(base_dir / entry)
                is_dir = os.path.isdir(full_path)
                suggestions.append((entry + "/" if is_dir else entry, is_dir))
                if len(suggestions) >= 20:
                    break
            return suggestions
        except Exception:
            return []

    def _symbol_kind_to_completion_kind(self, kind: SymbolKind) -> int:
        mapping = {
            SymbolKind.AGENT: CompletionItemKind.Class,
            SymbolKind.SKILL: CompletionItemKind.Function,
            SymbolKind.PLAYBOOK: CompletionItemKind.Method,
            SymbolKind.TOOL: CompletionItemKind.Function,
            SymbolKind.COMMAND: CompletionItemKind.Function,
            SymbolKind.POLICY: CompletionItemKind.Property,
            SymbolKind.PERMISSION: CompletionItemKind.Property,
            SymbolKind.REGISTRY: CompletionItemKind.Module,
            SymbolKind.MODEL_PROFILE: CompletionItemKind.Class,
            SymbolKind.TOKEN_BUDGET: CompletionItemKind.Constant,
            SymbolKind.VARIABLE: CompletionItemKind.Variable,
            SymbolKind.INPUT: CompletionItemKind.Variable,
            SymbolKind.OUTPUT: CompletionItemKind.Variable,
        }
        return mapping.get(kind, CompletionItemKind.Reference)

    def provide_completions(self, params: CompletionParams) -> CompletionList:
        uri = params.text_document.uri
        doc = self._server.workspace.text_documents.get(uri)
        if doc is None:
            return CompletionList(is_incomplete=False, items=[])

        text = doc.source
        ctx = self._detect_context(params, text)

        all_items: list[CompletionItem] = []
        scores: list[float] = []

        config: LSPClientConfig = self._server.workspace.get_config(uri) if hasattr(self._server.workspace, "get_config") else LSPClientConfig()
        max_items = config.max_completion_items if hasattr(config, "max_completion_items") else MAX_COMPLETION_ITEMS_DEFAULT

        if ctx.kind == _ContextKind.DIRECTIVE:
            self._add_directive_completions(ctx, all_items, scores)
        elif ctx.kind == _ContextKind.EXPRESSION:
            self._add_expression_completions(ctx, all_items, scores)
            self._add_symbol_completions(ctx, SymbolKind.VARIABLE, all_items, scores, uri)
            self._add_symbol_completions(ctx, SymbolKind.INPUT, all_items, scores, uri)
            self._add_symbol_completions(ctx, SymbolKind.OUTPUT, all_items, scores, uri)
        elif ctx.kind == _ContextKind.KEY:
            self._add_key_completions(ctx, all_items, scores)
            self._add_snippet_completions(ctx, all_items, scores)
        elif ctx.kind == _ContextKind.VALUE:
            self._add_value_completions(ctx, all_items, scores)
            self._add_symbol_completions(ctx, SymbolKind.AGENT, all_items, scores, uri)
            self._add_symbol_completions(ctx, SymbolKind.SKILL, all_items, scores, uri)
            self._add_symbol_completions(ctx, SymbolKind.PLAYBOOK, all_items, scores, uri)
            self._add_symbol_completions(ctx, SymbolKind.TOOL, all_items, scores, uri)
            self._add_symbol_completions(ctx, SymbolKind.COMMAND, all_items, scores, uri)
            self._add_symbol_completions(ctx, SymbolKind.POLICY, all_items, scores, uri)
            self._add_model_completions(ctx, all_items, scores)
            self._add_token_budget_completions(ctx, all_items, scores)
            self._add_workspace_path_completions(ctx, all_items, scores)
        else:
            self._add_key_completions(ctx, all_items, scores)
            self._add_symbol_completions(ctx, SymbolKind.AGENT, all_items, scores, uri)
            self._add_symbol_completions(ctx, SymbolKind.SKILL, all_items, scores, uri)
            self._add_symbol_completions(ctx, SymbolKind.PLAYBOOK, all_items, scores, uri)
            self._add_symbol_completions(ctx, SymbolKind.TOOL, all_items, scores, uri)
            self._add_snippet_completions(ctx, all_items, scores)

        paired = list(zip(all_items, scores))
        paired.sort(key=lambda x: -x[1])
        paired = paired[:max_items]

        is_incomplete = len(paired) >= max_items
        return CompletionList(
            is_incomplete=is_incomplete,
            items=[item for item, _ in paired],
        )
