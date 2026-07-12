from __future__ import annotations

import re
import threading
from typing import Any

from lsprotocol.types import (
    DocumentRangeFormattingParams,
    FormattingOptions,
    Position,
    Range,
    TextEdit,
)
from pygls.lsp.server import LanguageServer


class RangeFormattingFeature:
    def __init__(self, server: LanguageServer) -> None:
        self._server = server
        self._lock = threading.RLock()

    def provide_range_formatting(self, params: DocumentRangeFormattingParams) -> list[TextEdit] | None:
        uri = params.text_document.uri
        range_ = params.range
        options = params.options

        doc = self._server.workspace.text_documents.get(uri)
        if doc is None:
            return None

        text = doc.source
        lines = text.splitlines(keepends=True)

        start_line = max(0, range_.start.line)
        end_line = min(len(lines) - 1, range_.end.line)

        if start_line > end_line:
            return None

        formatted_lines: list[str] = []
        for i in range(start_line, end_line + 1):
            line = lines[i].rstrip("\n\r")
            formatted = self._format_line(line, options)
            formatted_lines.append(formatted)

        if not formatted_lines:
            return None

        new_text = "".join(formatted_lines)
        original_text = "".join(lines[start_line:end_line + 1])
        if new_text == original_text:
            return None

        return [TextEdit(
            range=Range(
                start=Position(line=start_line, character=0),
                end=Position(line=end_line, character=len(lines[end_line].rstrip("\n\r"))),
            ),
            new_text=new_text,
        )]

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
            return "\n"

        if stripped.startswith("#") or stripped.startswith("//"):
            return f"{new_indent}{stripped}\n"

        if ":" in stripped and not stripped.startswith("-"):
            parts = stripped.split(":", 1)
            key = parts[0].strip()
            value = parts[1].strip() if len(parts) > 1 else ""
            return f"{new_indent}{key}: {value}\n" if value else f"{new_indent}{key}:\n"

        if stripped.startswith("- "):
            item = stripped[2:].strip()
            return f"{new_indent}- {item}\n"

        return f"{new_indent}{stripped}\n"
