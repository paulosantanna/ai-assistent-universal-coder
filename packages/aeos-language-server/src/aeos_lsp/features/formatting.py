from __future__ import annotations

import re
import threading
from typing import Any

from lsprotocol.types import (
    DocumentFormattingParams,
    FormattingOptions,
    Position,
    Range,
    TextEdit,
)
from pygls.lsp.server import LanguageServer


_KEY_ORDER = [
    "aeos", "name", "stable_id", "version", "description", "documentation",
    "kind", "type", "mode", "runtime",
    "agent", "agents", "skill", "skills", "playbook", "playbooks",
    "tool", "tools", "command", "commands",
    "policy", "policies", "permission", "permissions",
    "registry", "registries",
    "parent", "extends", "visibility", "deprecation",
    "model", "token_budget",
    "layers", "steps", "variables",
    "inputs", "outputs",
    "timeout", "retry", "approval", "rollback",
    "evidence", "judge", "gate",
    "metadata", "references", "content_hash",
    "security", "execution", "packaging", "observability",
    "registries",
    "exclusions", "config",
]


class FormattingFeature:
    def __init__(self, server: LanguageServer) -> None:
        self._server = server
        self._lock = threading.RLock()

    def provide_formatting(self, params: DocumentFormattingParams) -> list[TextEdit] | None:
        uri = params.text_document.uri
        options = params.options

        doc = self._server.workspace.text_documents.get(uri)
        if doc is None:
            return None

        text = doc.source
        formatted = self._format_document(text, options)
        if formatted == text:
            return None

        lines = text.splitlines(keepends=False)
        if not lines:
            return None

        full_range = Range(
            start=Position(line=0, character=0),
            end=Position(line=len(lines) - 1, character=len(lines[-1])),
        )

        return [TextEdit(range=full_range, new_text=formatted)]

    def _format_document(self, text: str, options: FormattingOptions) -> str:
        lines = text.splitlines(keepends=True)
        formatted_lines: list[str] = []
        in_fenced_block = False
        in_front_matter = False
        front_matter_end = -1

        for i, line in enumerate(lines):
            stripped = line.rstrip("\n\r")

            if stripped.strip() == "---":
                if not in_front_matter and i == 0:
                    in_front_matter = True
                    formatted_lines.append(stripped + "\n")
                    continue
                elif in_front_matter:
                    in_front_matter = False
                    front_matter_end = i
                    formatted_lines.append(stripped + "\n")
                    continue

            if in_front_matter:
                formatted_lines.append(stripped + "\n")
                continue

            if stripped.strip().startswith("```") or stripped.strip().startswith("~~~"):
                in_fenced_block = not in_fenced_block
                formatted_lines.append(stripped + "\n")
                continue

            if in_fenced_block:
                formatted_lines.append(stripped + "\n")
                continue

            if stripped.strip().startswith("#") or stripped.strip().startswith("//"):
                formatted_lines.append(stripped + "\n")
                continue

            if not stripped.strip():
                indent = self._detect_indent(lines, i)
                formatted_lines.append("")
                continue

            formatted = self._format_line(stripped, options)
            formatted_lines.append(formatted)

        result = "".join(formatted_lines)

        if not result.endswith("\n"):
            result += "\n"

        return result

    def _format_line(self, line: str, options: FormattingOptions) -> str:
        indent_size = options.tab_size if not options.insert_spaces else options.tab_size
        indent_char = " " if options.insert_spaces else "\t"

        original_indent = len(line) - len(line.lstrip())
        if original_indent > 0 and not options.insert_spaces:
            tab_indent = original_indent // indent_size
            remaining = original_indent % indent_size
            new_indent = ("\t" * tab_indent) + (" " * remaining)
        elif original_indent > 0 and options.insert_spaces:
            new_indent = " " * original_indent
        else:
            new_indent = ""

        stripped = line.strip()
        if not stripped:
            return ""

        if ":" in stripped and not stripped.startswith("-"):
            parts = stripped.split(":", 1)
            key = parts[0].strip()
            value = parts[1].strip() if len(parts) > 1 else ""
            return f"{new_indent}{key}: {value}\n" if value else f"{new_indent}{key}:\n"

        if stripped.startswith("- "):
            item = stripped[2:].strip()
            return f"{new_indent}- {item}\n"

        return f"{new_indent}{stripped}\n"

    def _detect_indent(self, lines: list[str], current_line: int) -> int:
        for i in range(current_line - 1, -1, -1):
            prev = lines[i].rstrip("\n\r")
            if prev.strip() and not prev.strip().startswith("#"):
                return len(prev) - len(prev.lstrip())
        return 0
