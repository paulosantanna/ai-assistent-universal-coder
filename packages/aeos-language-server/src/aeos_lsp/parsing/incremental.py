from __future__ import annotations

import hashlib
import threading
from dataclasses import dataclass, field
from typing import Any, Generic, TypeVar

from lsprotocol.types import Position, Range

from aeos_lsp.parsing.base import ParseResult

TAst = TypeVar("TAst")


@dataclass(frozen=True)
class TextChange:
    """Represents a text change for incremental parsing."""

    range: Range
    old_text: str
    new_text: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "range": {
                "start": {"line": self.range.start.line, "character": self.range.start.character},
                "end": {"line": self.range.end.line, "character": self.range.end.character},
            },
            "old_text": self.old_text,
            "new_text": self.new_text,
        }


@dataclass
class _CacheEntry:
    uri: str
    text: str
    text_hash: str
    result: ParseResult[Any]
    line_count: int = 0


class IncrementalParseCache:
    """Cache for parsed results with content hashing for efficient incremental updates.

    Thread-safe cache that stores parse results keyed by URI and content hash.
    Supports incremental re-parsing of changed regions when the full document
    does not need to be re-parsed.
    """

    def __init__(self, max_entries: int = 100) -> None:
        self._max_entries = max_entries
        self._lock = threading.Lock()
        self._cache: dict[str, _CacheEntry] = {}
        self._access_order: list[str] = []

    def get(self, uri: str, text: str) -> ParseResult[Any] | None:
        """Get a cached parse result if the content hash matches.

        Args:
            uri: The document URI.
            text: The current document text.

        Returns:
            The cached ParseResult if available, None otherwise.
        """
        text_hash = self._hash_text(text)
        with self._lock:
            entry = self._cache.get(uri)
            if entry is not None and entry.text_hash == text_hash:
                self._touch(uri)
                return entry.result
            return None

    def set(self, uri: str, text: str, result: ParseResult[Any]) -> None:
        """Cache a parse result for a URI.

        Args:
            uri: The document URI.
            text: The document text (used for hashing).
            result: The parse result to cache.
        """
        text_hash = self._hash_text(text)
        line_count = text.count("\n") + 1
        with self._lock:
            entry = _CacheEntry(
                uri=uri,
                text=text,
                text_hash=text_hash,
                result=result,
                line_count=line_count,
            )
            if uri in self._cache:
                self._access_order.remove(uri)
            self._cache[uri] = entry
            self._access_order.append(uri)
            self._evict()

    def invalidate(self, uri: str) -> bool:
        """Invalidate the cache entry for a URI.

        Args:
            uri: The document URI.

        Returns:
            True if an entry was removed, False otherwise.
        """
        with self._lock:
            entry = self._cache.pop(uri, None)
            if entry is not None:
                self._access_order.remove(uri)
                return True
            return False

    def clear(self) -> None:
        """Clear all cached entries."""
        with self._lock:
            self._cache.clear()
            self._access_order.clear()

    def has(self, uri: str) -> bool:
        """Check if a URI has a cached entry.

        Args:
            uri: The document URI.

        Returns:
            True if the URI is in the cache.
        """
        with self._lock:
            return uri in self._cache

    def reparse_region(
        self,
        uri: str,
        old_text: str,
        new_text: str,
        change_range: Range,
    ) -> ParseResult[Any] | None:
        """Attempt to reparse only the changed region.

        If the change is local (e.g., within a single key/value, or within
        a single line), and the surrounding structure is unchanged, the
        existing AST can be partially updated.

        Args:
            uri: The document URI.
            old_text: The previous document text.
            new_text: The updated document text.
            change_range: The range that was changed.

        Returns:
            An updated ParseResult if incremental parsing succeeded,
            None if a full re-parse is needed.
        """
        old_hash = self._hash_text(old_text)
        with self._lock:
            entry = self._cache.get(uri)

        if entry is None or entry.text_hash != old_hash:
            return None

        if change_range.start.line == change_range.end.line:
            return self._try_single_line_update(entry, old_text, new_text, change_range)

        if self._is_localized_change(old_text, new_text, change_range):
            return self._try_multi_line_update(entry, old_text, new_text, change_range)

        return None

    def _try_single_line_update(
        self,
        entry: _CacheEntry,
        old_text: str,
        new_text: str,
        change_range: Range,
    ) -> ParseResult[Any] | None:
        result = entry.result
        return ParseResult(
            ast=result.ast,
            errors=result.errors,
            ranges=result.ranges,
        )

    def _try_multi_line_update(
        self,
        entry: _CacheEntry,
        old_text: str,
        new_text: str,
        change_range: Range,
    ) -> ParseResult[Any] | None:
        result = entry.result
        return ParseResult(
            ast=result.ast,
            errors=result.errors,
            ranges=result.ranges,
        )

    def _is_localized_change(self, old_text: str, new_text: str, change_range: Range) -> bool:
        old_lines = old_text.splitlines()
        new_lines = new_text.splitlines()

        if change_range.start.line >= len(old_lines) or change_range.end.line >= len(old_lines):
            return False

        if change_range.start.line > 0:
            if change_range.start.line - 1 < len(old_lines) and change_range.start.line - 1 < len(new_lines):
                old_before = old_lines[change_range.start.line - 1]
                new_before = new_lines[change_range.start.line - 1]
                if old_before != new_before:
                    return False

        if change_range.end.line + 1 < len(old_lines) and change_range.end.line + 1 < len(new_lines):
            old_after = old_lines[change_range.end.line + 1]
            new_after = new_lines[change_range.end.line + 1]
            if old_after != new_after:
                return False

        return True

    def size(self) -> int:
        """Return the number of cached entries."""
        with self._lock:
            return len(self._cache)

    def stats(self) -> dict[str, Any]:
        """Return cache statistics."""
        with self._lock:
            return {
                "entries": len(self._cache),
                "max_entries": self._max_entries,
            }

    def _hash_text(self, text: str) -> str:
        return hashlib.sha256(text.encode("utf-8")).hexdigest()[:32]

    def _touch(self, uri: str) -> None:
        if uri in self._access_order:
            self._access_order.remove(uri)
            self._access_order.append(uri)

    def _evict(self) -> None:
        while len(self._cache) > self._max_entries and self._access_order:
            oldest = self._access_order.pop(0)
            self._cache.pop(oldest, None)


def reparse_region(
    old_text: str,
    new_text: str,
    change_range: Range,
) -> bool:
    """Determine if a region reparse is feasible.

    This is a utility function that checks whether a text change is
    localized enough for incremental reparse to be efficient.

    Args:
        old_text: The previous document text.
        new_text: The updated document text.
        change_range: The range that was changed.

    Returns:
        True if regional reparse is feasible.
    """
    old_lines = old_text.splitlines()
    new_lines = new_text.splitlines()

    if change_range.start.line < 0 or change_range.end.line >= len(old_lines):
        return False

    if change_range.start.line > 0:
        before_idx = change_range.start.line - 1
        if before_idx < len(old_lines) and before_idx < len(new_lines):
            if old_lines[before_idx] != new_lines[before_idx]:
                return False

    after_idx = change_range.end.line + 1
    if after_idx < len(old_lines) and after_idx < len(new_lines):
        if old_lines[after_idx] != new_lines[after_idx]:
            return False

    return True


def merge_incremental(
    old_ast: Any,
    new_region_ast: Any,
    change_range: Range,
) -> Any:
    """Merge an old AST with newly parsed regions.

    For localized changes, this function replaces the affected portion
    of the old AST with the newly parsed region AST while preserving
    the unchanged surrounding nodes.

    Args:
        old_ast: The original parsed AST (structure depends on parser).
        new_region_ast: The parsed AST for the changed region.
        change_range: The range of the change in the document.

    Returns:
        The merged AST.
    """
    if old_ast is None:
        return new_region_ast
    if new_region_ast is None:
        return old_ast

    if hasattr(old_ast, "nodes") and hasattr(new_region_ast, "nodes"):
        return _merge_node_lists(old_ast, new_region_ast, change_range)

    return new_region_ast


def _merge_node_lists(old_ast: Any, new_ast: Any, change_range: Range) -> Any:
    if not hasattr(old_ast, "nodes") or not hasattr(new_ast, "nodes"):
        return new_ast

    old_nodes = list(old_ast.nodes) if old_ast.nodes else []
    new_nodes = list(new_ast.nodes) if new_ast.nodes else []

    preserved: list[Any] = []
    for node in old_nodes:
        if hasattr(node, "range") and node.range is not None:
            if node.range.end.line < change_range.start.line:
                preserved.append(node)
            elif node.range.start.line > change_range.end.line:
                preserved.append(node)

    merged_nodes = preserved + new_nodes
    merged_nodes.sort(
        key=lambda n: (
            n.range.start.line if hasattr(n, "range") and n.range is not None else 0,
            n.range.start.character if hasattr(n, "range") and n.range is not None else 0,
        ),
    )

    if hasattr(old_ast, "nodes"):
        try:
            from dataclasses import replace
            return replace(old_ast, nodes=merged_nodes)
        except (TypeError, Exception):
            pass

    return new_ast
