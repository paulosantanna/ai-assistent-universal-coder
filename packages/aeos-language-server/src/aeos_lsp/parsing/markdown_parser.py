from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from lsprotocol.types import Position, Range

from aeos_lsp.parsing.base import (
    BaseParser,
    ParseError,
    ParseErrorSeverity,
    ParseResult,
)
from aeos_lsp.parsing.yaml_parser import YamlParser, YamlDocument


@dataclass(frozen=True)
class FrontMatter:
    raw_text: str
    range: Range
    data: dict[str, Any] = field(default_factory=dict)
    parse_errors: list[ParseError] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "raw_text": self.raw_text,
            "range": {
                "start": {"line": self.range.start.line, "character": self.range.start.character},
                "end": {"line": self.range.end.line, "character": self.range.end.character},
            },
        }


@dataclass(frozen=True)
class Heading:
    level: int
    text: str
    range: Range
    anchor: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "level": self.level,
            "text": self.text,
            "range": {
                "start": {"line": self.range.start.line, "character": self.range.start.character},
                "end": {"line": self.range.end.line, "character": self.range.end.character},
            },
        }


@dataclass(frozen=True)
class Directive:
    name: str
    args: str
    range: Range
    body_range: Range | None = None
    body: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "args": self.args,
            "range": {
                "start": {"line": self.range.start.line, "character": self.range.start.character},
                "end": {"line": self.range.end.line, "character": self.range.end.character},
            },
        }


@dataclass(frozen=True)
class Link:
    text: str
    url: str
    range: Range
    title: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "text": self.text,
            "url": self.url,
            "range": {
                "start": {"line": self.range.start.line, "character": self.range.start.character},
                "end": {"line": self.range.end.line, "character": self.range.end.character},
            },
        }


@dataclass(frozen=True)
class FencedCodeBlock:
    language: str
    content: str
    range: Range
    fence_char: str = "`"
    fence_length: int = 3

    def to_dict(self) -> dict[str, Any]:
        return {
            "language": self.language,
            "content": self.content,
            "fence_char": self.fence_char,
            "fence_length": self.fence_length,
            "range": {
                "start": {"line": self.range.start.line, "character": self.range.start.character},
                "end": {"line": self.range.end.line, "character": self.range.end.character},
            },
        }


@dataclass(frozen=True)
class AeoSElement:
    kind: str
    value: str
    range: Range
    ref_type: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "kind": self.kind,
            "value": self.value,
            "range": {
                "start": {"line": self.range.start.line, "character": self.range.start.character},
                "end": {"line": self.range.end.line, "character": self.range.end.character},
            },
        }


@dataclass(frozen=True)
class MarkdownAstNode:
    node_type: str
    range: Range
    content: str = ""
    children: list[MarkdownAstNode] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class MarkdownDocument:
    front_matter: FrontMatter | None = None
    headings: list[Heading] = field(default_factory=list)
    directives: list[Directive] = field(default_factory=list)
    links: list[Link] = field(default_factory=list)
    code_blocks: list[FencedCodeBlock] = field(default_factory=list)
    aeos_elements: list[AeoSElement] = field(default_factory=list)
    nodes: list[MarkdownAstNode] = field(default_factory=list)
    raw_text: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "front_matter": self.front_matter.to_dict() if self.front_matter else None,
            "headings": [h.to_dict() for h in self.headings],
            "directives": [d.to_dict() for d in self.directives],
            "links": [l.to_dict() for l in self.links],
            "code_blocks": [c.to_dict() for c in self.code_blocks],
            "aeos_elements": [e.to_dict() for e in self.aeos_elements],
        }


# Regex patterns
FRONT_MATTER_PATTERN = re.compile(r"^---\s*\n(.*?)\n---\s*", re.DOTALL)
HEADING_PATTERN = re.compile(r"^(#{1,6})\s+(.+?)(?:\s+#+.*)?$", re.MULTILINE)
DIRECTIVE_PATTERN = re.compile(r"^@(\w[\w-]*)(?:\s+(.*))?$", re.MULTILINE)
LINK_PATTERN = re.compile(r"\[([^\]]*)\]\(([^)]+)\)")
FENCED_CODE_PATTERN = re.compile(
    r"^(?P<fence>(?P<fchar>[`~])(?P=fchar){2,})\s*(?P<lang>\w*)\s*$",
    re.MULTILINE,
)
AEOS_REF_PATTERN = re.compile(r"(?:\b)(agent|skill|playbook|tool|policy|permission|gate|model|step|input|output|dependency|rollback|evidence|variable):([a-zA-Z_][\w./-]*)")


class MarkdownParser(BaseParser[MarkdownDocument]):
    file_extensions: set[str] = {".md", ".markdown", ".agent.md", ".skill.md", ".playbook.md", "AGENT.md", "AGENTS.md", "SKILL.md", "PLAYBOOK.md"}

    def __init__(self) -> None:
        self._yaml_parser = YamlParser()

    def parse(self, text: str, uri: str) -> ParseResult[MarkdownDocument]:
        errors: list[ParseError] = []
        ranges: dict[str, Range] = {}
        lines = text.splitlines(keepends=True)

        front_matter = self._parse_front_matter(text, lines, errors, ranges)
        body_start = 0
        if front_matter is not None:
            body_start = front_matter.range.end.line + 1

        headings = self._parse_headings(text, lines, ranges)
        directives = self._parse_directives(text, lines, ranges)
        links = self._parse_links(text, lines, ranges)
        code_blocks = self._parse_fenced_code_blocks(text, lines, ranges)
        aeos_elements = self._parse_aeos_references(text, lines, ranges)

        nodes = self._build_ast_nodes(
            text, lines, front_matter, headings, directives, code_blocks, ranges,
        )

        doc = MarkdownDocument(
            front_matter=front_matter,
            headings=headings,
            directives=directives,
            links=links,
            code_blocks=code_blocks,
            aeos_elements=aeos_elements,
            nodes=nodes,
            raw_text=text,
        )

        return ParseResult(ast=doc, errors=errors, ranges=ranges)

    def parse_file(self, path: str) -> ParseResult[MarkdownDocument]:
        text = Path(path).read_text(encoding="utf-8")
        return self.parse(text, path)

    def _parse_front_matter(
        self,
        text: str,
        lines: list[str],
        errors: list[ParseError],
        ranges: dict[str, Range],
    ) -> FrontMatter | None:
        m = FRONT_MATTER_PATTERN.match(text)
        if not m:
            return None

        yaml_text = m.group(1)
        start_line = 0
        end_line = 0
        char_count = 0
        for i, line in enumerate(lines):
            if line.rstrip("\n\r") == "---":
                if start_line == 0:
                    start_line = i
                    continue
                else:
                    end_line = i
                    break

        fm_range = Range(
            start=Position(line=start_line, character=0),
            end=Position(line=end_line, character=len(lines[end_line].rstrip("\n\r"))),
        )

        parse_result = self._yaml_parser.parse(yaml_text, "frontmatter")
        data = parse_result.ast.raw_data if isinstance(parse_result.ast, YamlDocument) else {}

        fm = FrontMatter(
            raw_text=yaml_text,
            range=fm_range,
            data=data,
            parse_errors=parse_result.errors,
        )
        ranges["front_matter"] = fm_range
        return fm

    def _parse_headings(
        self,
        text: str,
        lines: list[str],
        ranges: dict[str, Range],
    ) -> list[Heading]:
        headings: list[Heading] = []
        for m in HEADING_PATTERN.finditer(text):
            level = len(m.group(1))
            heading_text = m.group(2).strip()
            start_offset = m.start()
            end_offset = m.end()
            heading_range = self._make_range(text, start_offset, end_offset)
            anchor = re.sub(r"[^a-zA-Z0-9\s-]", "", heading_text).lower().replace(" ", "-")
            heading = Heading(level=level, text=heading_text, range=heading_range, anchor=anchor)
            headings.append(heading)
            ranges[f"heading:{heading_text}"] = heading_range
        return headings

    def _parse_directives(
        self,
        text: str,
        lines: list[str],
        ranges: dict[str, Range],
    ) -> list[Directive]:
        directives: list[Directive] = []
        for line_idx, line in enumerate(lines):
            stripped = line.strip()
            m = DIRECTIVE_PATTERN.match(stripped)
            if m:
                name = m.group(1)
                args = (m.group(2) or "").strip()
                start_char = line.index("@")
                end_char = start_char + len(stripped)
                d_range = Range(
                    start=Position(line=line_idx, character=start_char),
                    end=Position(line=line_idx, character=end_char),
                )
                directive = Directive(name=name, args=args, range=d_range)
                directives.append(directive)
                ranges[f"directive:{name}"] = d_range
        return directives

    def _parse_links(
        self,
        text: str,
        lines: list[str],
        ranges: dict[str, Range],
    ) -> list[Link]:
        links: list[Link] = []
        for m in LINK_PATTERN.finditer(text):
            link_text = m.group(1)
            url = m.group(2)
            start_offset = m.start()
            end_offset = m.end()
            link_range = self._make_range(text, start_offset, end_offset)
            title = ""
            title_m = re.search(r'\s+"([^"]*)"\s*$', url)
            if title_m:
                title = title_m.group(1)
                url = url[:title_m.start()].strip()
            link = Link(text=link_text, url=url, range=link_range, title=title)
            links.append(link)
            ranges[f"link:{url}"] = link_range
        return links

    def _parse_fenced_code_blocks(
        self,
        text: str,
        lines: list[str],
        ranges: dict[str, Range],
    ) -> list[FencedCodeBlock]:
        blocks: list[FencedCodeBlock] = []
        i = 0
        while i < len(lines):
            line = lines[i].rstrip("\n\r")
            m = re.match(r"^(?P<fence>(?P<fchar>[`~])(?P=fchar){2,})\s*(?P<lang>\w*)\s*$", line)
            if m:
                fence = m.group("fence")
                fchar = m.group("fchar")
                lang = m.group("lang") or ""
                fence_len = len(fence)
                start_line = i
                start_char = lines[i].index(fence[0])
                i += 1
                content_lines: list[str] = []
                while i < len(lines):
                    closing = lines[i].rstrip("\n\r")
                    if closing.strip() == fence or (closing.startswith(fence[0] * 3) and set(closing.strip()) == {fence[0]}):
                        end_line = i
                        end_char = len(lines[i].rstrip("\n\r"))
                        block_range = Range(
                            start=Position(line=start_line, character=start_char),
                            end=Position(line=end_line, character=end_char),
                        )
                        block = FencedCodeBlock(
                            language=lang,
                            content="".join(content_lines),
                            range=block_range,
                            fence_char=fchar,
                            fence_length=fence_len,
                        )
                        blocks.append(block)
                        ranges[f"codeblock:{lang}"] = block_range
                        i += 1
                        break
                    content_lines.append(lines[i])
                    i += 1
                else:
                    end_line = len(lines) - 1
                    end_char = len(lines[end_line].rstrip("\n\r"))
                    block_range = Range(
                        start=Position(line=start_line, character=start_char),
                        end=Position(line=end_line, character=end_char),
                    )
                    block = FencedCodeBlock(
                        language=lang,
                        content="".join(content_lines),
                        range=block_range,
                        fence_char=fchar,
                        fence_length=fence_len,
                    )
                    blocks.append(block)
                    ranges[f"codeblock:{lang}"] = block_range
            else:
                i += 1
        return blocks

    def _parse_aeos_references(
        self,
        text: str,
        lines: list[str],
        ranges: dict[str, Range],
    ) -> list[AeoSElement]:
        elements: list[AeoSElement] = []
        for m in AEOS_REF_PATTERN.finditer(text):
            ref_type = m.group(1)
            ref_value = m.group(2)
            start_offset = m.start()
            end_offset = m.end()
            ref_range = self._make_range(text, start_offset, end_offset)
            element = AeoSElement(
                kind="reference",
                value=ref_value,
                range=ref_range,
                ref_type=ref_type,
            )
            elements.append(element)
            ranges[f"aeos_ref:{ref_type}:{ref_value}"] = ref_range
        return elements

    def _build_ast_nodes(
        self,
        text: str,
        lines: list[str],
        front_matter: FrontMatter | None,
        headings: list[Heading],
        directives: list[Directive],
        code_blocks: list[FencedCodeBlock],
        ranges: dict[str, Range],
    ) -> list[MarkdownAstNode]:
        nodes: list[MarkdownAstNode] = []

        if front_matter is not None:
            nodes.append(MarkdownAstNode(
                node_type="front_matter",
                range=front_matter.range,
                content=front_matter.raw_text,
            ))

        for heading in headings:
            nodes.append(MarkdownAstNode(
                node_type=f"heading_{heading.level}",
                range=heading.range,
                content=heading.text,
                metadata={"level": heading.level, "anchor": heading.anchor},
            ))

        for directive in directives:
            nodes.append(MarkdownAstNode(
                node_type="directive",
                range=directive.range,
                content=f"@{directive.name} {directive.args}",
                metadata={"name": directive.name, "args": directive.args},
            ))

        for block in code_blocks:
            nodes.append(MarkdownAstNode(
                node_type="code_block",
                range=block.range,
                content=block.content,
                metadata={"language": block.language},
            ))

        paragraph_start = 0
        if front_matter is not None:
            paragraph_start = front_matter.range.end.line + 1

        covered_lines: set[int] = set()
        for heading in headings:
            for ln in range(heading.range.start.line, heading.range.end.line + 1):
                covered_lines.add(ln)
        for directive in directives:
            covered_lines.add(directive.range.start.line)
        for block in code_blocks:
            for ln in range(block.range.start.line, block.range.end.line + 1):
                covered_lines.add(ln)

        para_text = ""
        para_start = -1
        for i in range(paragraph_start, len(lines)):
            if i in covered_lines:
                if para_text.strip():
                    para_range = Range(
                        start=Position(line=para_start, character=0),
                        end=Position(line=i - 1, character=len(lines[i - 1].rstrip("\n\r"))),
                    )
                    nodes.append(MarkdownAstNode(
                        node_type="paragraph",
                        range=para_range,
                        content=para_text.strip(),
                    ))
                    para_text = ""
                    para_start = -1
                continue
            if para_start == -1:
                para_start = i
            para_text += lines[i]

        if para_text.strip():
            para_range = Range(
                start=Position(line=para_start, character=0),
                end=Position(line=len(lines) - 1, character=len(lines[-1].rstrip("\n\r"))),
            )
            nodes.append(MarkdownAstNode(
                node_type="paragraph",
                range=para_range,
                content=para_text.strip(),
            ))

        return nodes
