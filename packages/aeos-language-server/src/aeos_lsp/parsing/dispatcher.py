from __future__ import annotations

import re
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Any

from lsprotocol.types import Position, Range

from aeos_lsp.parsing.base import (
    BaseParser,
    ParseError,
    ParseErrorSeverity,
    ParseResult,
)
from aeos_lsp.parsing.incremental import IncrementalParseCache
from aeos_lsp.parsing.yaml_parser import YamlParser, YamlDocument
from aeos_lsp.parsing.json_parser import JsonParser, JsonAstNode
from aeos_lsp.parsing.toml_parser import TomlParser, TomlDocument
from aeos_lsp.parsing.markdown_parser import MarkdownParser, MarkdownDocument
from aeos_lsp.parsing.expression_parser import ExprParser, ExprAstNode


class AEOSDocumentType(Enum):
    AGENT = "agent"
    SKILL = "skill"
    PLAYBOOK = "playbook"
    REGISTRY = "registry"
    CONFIG = "config"
    PERMISSIONS = "permissions"
    POLICIES = "policies"
    OVERLAY = "overlay"
    MARKDOWN = "markdown"
    EXPRESSION = "expression"
    UNKNOWN = "unknown"


# Quick-reject patterns for non-AEOS documents
_QUICK_REJECT_PATTERNS: list[re.Pattern[str]] = [
    re.compile(r"^node_modules/", re.IGNORECASE),
    re.compile(r"__pycache__"),
    re.compile(r"\.git/"),
    re.compile(r"\.venv/"),
    re.compile(r"venv/"),
    re.compile(r"node_modules/"),
    re.compile(r"\.next/"),
    re.compile(r"dist/"),
    re.compile(r"build/"),
]

_AEOS_CONTENT_PATTERNS: list[re.Pattern[str]] = [
    re.compile(r"^\s*aeos\s*:", re.MULTILINE),
    re.compile(r"^\s*agent\s*:", re.MULTILINE),
    re.compile(r"^\s*skill\s*:", re.MULTILINE),
    re.compile(r"^\s*playbook\s*:", re.MULTILINE),
    re.compile(r"^@(?:aeos|agent|skill|playbook|tool|policy|permission|gate|model|step|variable|input|output|dependency|rollback|evidence)\b", re.MULTILINE),
    re.compile(r"---\s*\n.*\n---\s*\n", re.DOTALL),
    re.compile(r"\$\{[^}]*\}"),
    re.compile(r"(?:agent|skill|playbook|tool|policy|permission):[a-zA-Z_][\w./-]*"),
]

_AEOS_FILENAME_PATTERNS: list[re.Pattern[str]] = [
    re.compile(r"^AGENTS?\.MD$", re.IGNORECASE),
    re.compile(r"^SKILL\.MD$", re.IGNORECASE),
    re.compile(r"^PLAYBOOK\.MD$", re.IGNORECASE),
    re.compile(r"\.agent\.md$", re.IGNORECASE),
    re.compile(r"\.skill\.md$", re.IGNORECASE),
    re.compile(r"\.playbook\.md$", re.IGNORECASE),
    re.compile(r"\.aeos(?:\.(?:yaml|yml|json|jsonc|toml))?$", re.IGNORECASE),
    re.compile(r"aeos\.config\.yaml$", re.IGNORECASE),
    re.compile(r"(?:permissions|policies)\.yaml$", re.IGNORECASE),
    re.compile(r"overlay\.(?:index|registry\.index)\.yaml$", re.IGNORECASE),
    re.compile(r".*\.registry\.yaml$", re.IGNORECASE),
]


@dataclass
class ParserDispatcher:
    """Dispatches parsing to the appropriate parser based on file type and content.

    Supports incremental parsing via IncrementalParseCache, and provides
    quick rejection for non-AEOS documents.
    """

    yaml_parser: YamlParser = field(default_factory=YamlParser)
    json_parser: JsonParser = field(default_factory=JsonParser)
    toml_parser: TomlParser = field(default_factory=TomlParser)
    markdown_parser: MarkdownParser = field(default_factory=MarkdownParser)
    expr_parser: ExprParser = field(default_factory=ExprParser)
    cache: IncrementalParseCache = field(default_factory=IncrementalParseCache)

    def parse(self, uri: str, text: str) -> ParseResult[Any]:
        """Convenience wrapper that matches the server's calling convention.
        
        Args:
            uri: The document URI.
            text: The document text to parse.

        Returns:
            A ParseResult containing the parsed AST or errors.
        """
        return self.dispatch(text, uri)

    def dispatch(self, text: str, uri: str) -> ParseResult[Any]:
        """Dispatch to the correct parser based on file extension and content.

        Args:
            text: The document text to parse.
            uri: The document URI.

        Returns:
            A ParseResult containing the parsed AST or errors.
        """
        if not is_aeos_document(uri, text, None):
            return ParseResult(
                ast=None,
                errors=[],
            )

        cached = self.cache.get(uri, text)
        if cached is not None:
            return cached

        ext = _get_extension(uri)
        aeos_type = detect_aeos_type(uri, text)

        parser = self._select_parser(ext, aeos_type)
        if parser is None:
            return ParseResult(
                ast=None,
                errors=[ParseError(
                    message=f"No parser available for {ext} files",
                    range=Range(start=Position(line=0, character=0), end=Position(line=0, character=0)),
                    severity=ParseErrorSeverity.ERROR,
                    code="NO_PARSER",
                )],
            )

        result = parser.parse(text, uri)
        self.cache.set(uri, text, result)
        return result

    def dispatch_incremental(
        self,
        uri: str,
        old_text: str,
        new_text: str,
        change_range: Range | None,
    ) -> ParseResult[Any]:
        """Dispatch with incremental parsing support.

        Args:
            uri: The document URI.
            old_text: The previous document text.
            new_text: The updated document text.
            change_range: The range that was changed, if known.

        Returns:
            A ParseResult containing the parsed AST.
        """
        if change_range is not None:
            result = self.cache.reparse_region(
                uri, old_text, new_text, change_range,
            )
            if result is not None:
                return result

        return self.dispatch(new_text, uri)

    def _select_parser(self, ext: str, aeos_type: AEOSDocumentType | None) -> BaseParser[Any] | None:
        if aeos_type == AEOSDocumentType.EXPRESSION:
            return self.expr_parser

        if ext in (".yaml", ".yml", ".aeos.yaml", ".aeos.yml"):
            return self.yaml_parser
        if ext in (".json", ".jsonc", ".aeos.json", ".aeos.jsonc"):
            return self.json_parser
        if ext in (".toml", ".aeos.toml"):
            return self.toml_parser
        if ext in (".md", ".markdown", ".agent.md", ".skill.md", ".playbook.md"):
            return self.markdown_parser
        if ext == ".expr":
            return self.expr_parser

        if aeos_type == AEOSDocumentType.MARKDOWN:
            return self.markdown_parser
        if aeos_type in (AEOSDocumentType.UNKNOWN, AEOSDocumentType.CONFIG):
            return self.yaml_parser

        return None

    def invalidate(self, uri: str) -> None:
        """Invalidate the cached result for a URI."""
        self.cache.invalidate(uri)

    def clear_cache(self) -> None:
        """Clear the entire parse cache."""
        self.cache.clear()


def is_aeos_document(
    path: str,
    content: str | None,
    workspace_config: Any | None = None,
) -> bool:
    """Quick-reject test for non-AEOS documents.

    Checks filename patterns, directory exclusions, and content markers
    to determine if a document might be an AEOS artifact.

    Args:
        path: The file path or URI.
        content: The file content, if available.
        workspace_config: Optional workspace configuration.

    Returns:
        True if the document appears to be an AEOS document.
    """
    path_lower = path.lower().replace("\\", "/")

    for pattern in _QUICK_REJECT_PATTERNS:
        if pattern.search(path_lower):
            return False

    for pattern in _AEOS_FILENAME_PATTERNS:
        if pattern.search(path_lower):
            return True

    if content is not None and len(content) < 100_000:
        for pattern in _AEOS_CONTENT_PATTERNS:
            if pattern.search(content):
                return True

    return False


def detect_aeos_type(path: str, content: str | None) -> AEOSDocumentType | None:
    """Detect the AEOS document type from path and content.

    Checks filename patterns first, then falls back to content analysis.

    Args:
        path: The file path or URI.
        content: The file content, if available.

    Returns:
        The detected AEOSDocumentType, or None if not detectable.
    """
    path_lower = path.lower().replace("\\", "/")

    if re.search(r"^AGENTS?\.MD$", path_lower, re.IGNORECASE):
        return AEOSDocumentType.MARKDOWN
    if re.search(r"^SKILL\.MD$", path_lower, re.IGNORECASE):
        return AEOSDocumentType.SKILL
    if re.search(r"^PLAYBOOK\.MD$", path_lower, re.IGNORECASE):
        return AEOSDocumentType.PLAYBOOK
    if re.search(r"(?:^AGENT\.MD$|\.agent\.md$)", path_lower, re.IGNORECASE):
        return AEOSDocumentType.AGENT
    if re.search(r"(?:^SKILL\.MD$|\.skill\.md$)", path_lower, re.IGNORECASE):
        return AEOSDocumentType.SKILL
    if re.search(r"(?:^PLAYBOOK\.MD$|\.playbook\.md$)", path_lower, re.IGNORECASE):
        return AEOSDocumentType.PLAYBOOK
    if re.search(r"aeos\.config\.yaml$", path_lower):
        return AEOSDocumentType.CONFIG
    if re.search(r"(?:permissions|policies)\.yaml$", path_lower):
        return AEOSDocumentType.PERMISSIONS
    if re.search(r"overlay\.(?:index|registry\.index)\.yaml$", path_lower):
        return AEOSDocumentType.OVERLAY
    if re.search(r".*\.registry\.yaml$", path_lower):
        return AEOSDocumentType.REGISTRY
    if re.search(r"\.expr$", path_lower):
        return AEOSDocumentType.EXPRESSION
    if re.search(r"\.(?:yaml|yml|json|jsonc|toml)$", path_lower):
        pass

    if content is not None:
        if re.search(r"^\s*aeos\s*:", content, re.MULTILINE):
            return AEOSDocumentType.CONFIG
        if re.search(r"^\s*agent\s*:", content, re.MULTILINE):
            return AEOSDocumentType.AGENT
        if re.search(r"^\s*skill\s*:", content, re.MULTILINE):
            return AEOSDocumentType.SKILL
        if re.search(r"^\s*playbook\s*:", content, re.MULTILINE):
            return AEOSDocumentType.PLAYBOOK
        if re.search(r"---\s*\n.*?\n---", content, re.DOTALL):
            return AEOSDocumentType.MARKDOWN
        if re.search(r"\$\{[^}]*\}", content):
            return AEOSDocumentType.EXPRESSION

    return None


def _get_extension(path: str) -> str:
    path_lower = path.lower()
    for ext in [".aeos.yaml", ".aeos.yml", ".aeos.json", ".aeos.jsonc", ".aeos.toml",
                ".agent.md", ".skill.md", ".playbook.md"]:
        if path_lower.endswith(ext):
            return ext
    p = Path(path_lower)
    return p.suffix
