from __future__ import annotations

import re
import threading
from pathlib import Path
from typing import Any

from lsprotocol.types import (
    DocumentLink,
    DocumentLinkParams,
    Position,
    Range,
)
from pygls.lsp.server import LanguageServer


_FILE_REF_RE = re.compile(r"(?:file://|\.\./|\./|/)?([\w./\\-]+\.(?:yaml|yml|json|toml|md|aeos))")
_URI_RE = re.compile(r"https?://[^\s'\")}\]>]+")
_REF_RE = re.compile(r"\$ref\s*:\s*['\"]?([^'\"]+)['\"]?")
_IMPORT_RE = re.compile(r"(?:import|include|source)\s+['\"]?([^'\"]+)['\"]?")
_STABLE_ID_RE = re.compile(r"stable_id\s*:\s*['\"]?([a-zA-Z_][\w.:/#-]*)['\"]?")


class DocumentLinksFeature:
    def __init__(self, server: LanguageServer) -> None:
        self._server = server
        self._lock = threading.RLock()

    def provide_document_links(self, params: DocumentLinkParams) -> list[DocumentLink] | None:
        uri = params.text_document.uri
        doc = self._server.workspace.text_documents.get(uri)
        if doc is None:
            return None

        text = doc.source
        links: list[DocumentLink] = []

        links.extend(self._find_file_links(text, uri))
        links.extend(self._find_uri_links(text))
        links.extend(self._find_ref_links(text))
        links.extend(self._find_import_links(text, uri))
        links.extend(self._find_stable_id_links(text, uri))

        return links if links else None

    def _find_file_links(self, text: str, base_uri: str) -> list[DocumentLink]:
        links: list[DocumentLink] = []
        for m in _FILE_REF_RE.finditer(text):
            start_pos = self._offset_to_position(text, m.start())
            end_pos = self._offset_to_position(text, m.end())
            ref_path = m.group(1)

            target = self._resolve_file_path(ref_path, base_uri)
            if target:
                links.append(DocumentLink(
                    range=Range(start=start_pos, end=end_pos),
                    target=target,
                    tooltip=f"Open {ref_path}",
                ))
        return links

    def _find_uri_links(self, text: str) -> list[DocumentLink]:
        links: list[DocumentLink] = []
        for m in _URI_RE.finditer(text):
            start_pos = self._offset_to_position(text, m.start())
            end_pos = self._offset_to_position(text, m.end())
            uri_str = m.group(0)
            links.append(DocumentLink(
                range=Range(start=start_pos, end=end_pos),
                target=uri_str,
                tooltip=f"Open {uri_str[:50]}",
            ))
        return links

    def _find_ref_links(self, text: str) -> list[DocumentLink]:
        links: list[DocumentLink] = []
        for m in _REF_RE.finditer(text):
            start_pos = self._offset_to_position(text, m.start(1))
            end_pos = self._offset_to_position(text, m.end(1))
            ref_path = m.group(1)
            links.append(DocumentLink(
                range=Range(start=start_pos, end=end_pos),
                target=ref_path,
                tooltip=f"Navigate to $ref: {ref_path}",
            ))
        return links

    def _find_import_links(self, text: str, base_uri: str) -> list[DocumentLink]:
        links: list[DocumentLink] = []
        for m in _IMPORT_RE.finditer(text):
            start_pos = self._offset_to_position(text, m.start(1))
            end_pos = self._offset_to_position(text, m.end(1))
            import_path = m.group(1)
            target = self._resolve_file_path(import_path, base_uri)
            if target:
                links.append(DocumentLink(
                    range=Range(start=start_pos, end=end_pos),
                    target=target,
                    tooltip=f"Open imported file: {import_path}",
                ))
        return links

    def _find_stable_id_links(self, text: str, base_uri: str) -> list[DocumentLink]:
        links: list[DocumentLink] = []
        for m in _STABLE_ID_RE.finditer(text):
            start_pos = self._offset_to_position(text, m.start(1))
            end_pos = self._offset_to_position(text, m.end(1))
            stable_id = m.group(1)

            from aeos_lsp.semantic.models import SymbolKind
            sm = getattr(self._server, "_semantic_model", None)
            if sm is not None:
                sym = sm.get_symbol_by_id(stable_id)
                if sym is not None:
                    sym_uri = getattr(sym, "source_uri", "")
                    if sym_uri:
                        links.append(DocumentLink(
                            range=Range(start=start_pos, end=end_pos),
                            target=sym_uri,
                            tooltip=f"Go to {stable_id}",
                        ))

        return links

    def _resolve_file_path(self, ref_path: str, base_uri: str) -> str | None:
        try:
            if ref_path.startswith("file://"):
                return ref_path

            base = base_uri.replace("file://", "").replace("\\", "/")
            if base.endswith("/"):
                base = base[:-1]
            base_dir = base.rsplit("/", 1)[0] if "/" in base else ""

            resolved = Path(base_dir) / ref_path
            if resolved.exists():
                return resolved.as_uri()

            ws_root = base_uri.split("/src/")[0] if "/src/" in base_uri else base_dir
            resolved2 = Path(ws_root) / ref_path
            if resolved2.exists():
                return resolved2.as_uri()

            return None
        except Exception:
            return None

    def _offset_to_position(self, text: str, offset: int) -> Position:
        if offset <= 0:
            return Position(line=0, character=0)
        if offset >= len(text):
            offset = len(text) - 1

        line = text[:offset].count("\n")
        last_newline = text[:offset].rfind("\n")
        character = offset - last_newline - 1 if last_newline >= 0 else offset
        return Position(line=line, character=character)
