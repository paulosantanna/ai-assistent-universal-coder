from __future__ import annotations

import re
from dataclasses import dataclass, field
from enum import Enum, auto
from pathlib import Path
from typing import Any

from lsprotocol.types import Position, Range

from aeos_lsp.parsing.base import (
    BaseParser,
    ParseError,
    ParseErrorSeverity,
    ParseResult,
)


class ExprTokenType(Enum):
    EOF = auto()
    IDENTIFIER = auto()
    STRING = auto()
    NUMBER = auto()
    BOOLEAN = auto()
    DOT = auto()
    COLON = auto()
    COMMA = auto()
    LPAREN = auto()
    RPAREN = auto()
    LBRACE = auto()
    RBRACE = auto()
    LBRACKET = auto()
    RBRACKET = auto()
    DOLLAR_LBRACE = auto()
    PIPE = auto()
    EQ = auto()
    NEQ = auto()
    LT = auto()
    GT = auto()
    LE = auto()
    GE = auto()
    AND = auto()
    OR = auto()
    NOT = auto()
    IF = auto()
    ELSE = auto()
    ELIF = auto()
    ENDIF = auto()
    PLUS = auto()
    MINUS = auto()
    STAR = auto()
    SLASH = auto()
    PERCENT = auto()
    ARROW = auto()
    HASH = auto()
    AT = auto()
    NEWLINE = auto()
    INDENT = auto()
    DEDENT = auto()


@dataclass(frozen=True)
class ExprToken:
    type: ExprTokenType
    value: str
    start: Position
    end: Position

    @property
    def range(self) -> Range:
        return Range(start=self.start, end=self.end)

    def to_dict(self) -> dict[str, Any]:
        return {
            "type": self.type.name,
            "value": self.value,
            "start": {"line": self.start.line, "character": self.start.character},
            "end": {"line": self.end.line, "character": self.end.character},
        }


@dataclass(frozen=True)
class ExprAstNode:
    node_type: str
    range: Range
    children: list[ExprAstNode] = field(default_factory=list)
    value: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "node_type": self.node_type,
            "range": {
                "start": {"line": self.range.start.line, "character": self.range.start.character},
                "end": {"line": self.range.end.line, "character": self.range.end.character},
            },
            "children": [c.to_dict() for c in self.children],
            "value": self.value,
            "metadata": self.metadata,
        }


class ExprError(Exception):
    def __init__(self, message: str, token: ExprToken | None = None) -> None:
        self.message = message
        self.token = token
        super().__init__(message)


# Grammar:
#   expression      -> boolean_expr
#   boolean_expr    -> comparison (("and" | "or") comparison)*
#   comparison      -> addition (("==" | "!=" | "<" | ">" | "<=" | ">=") addition)?
#   addition        -> term (("+" | "-") term)*
#   term            -> unary (("*" | "/" | "%") unary)*
#   unary           -> ("not" | "-") unary | primary
#   primary          -> "(" expression ")"
#                    | "if" expression ":" NEWLINE block ("elif" expression ":" NEWLINE block)* ("else" ":" NEWLINE block)? "endif"
#                    | "${" expression "}"
#                    | function_call
#                    | variable_ref
#                    | string
#                    | number
#                    | boolean
#   function_call   -> IDENTIFIER "(" [expression ("," expression)*] ")"
#   variable_ref    -> IDENTIFIER ("." IDENTIFIER)* (":" IDENTIFIER)?
#   string          -> '"' [^"]* '"' | "'" [^']* "'"
#   number          -> DIGIT+ ("." DIGIT+)? (("e"|"E") ("+"|"-")? DIGIT+)?
#   boolean          -> "true" | "false"

ALLOWED_FUNCTIONS: set[str] = {
    "len", "str", "int", "float", "bool",
    "upper", "lower", "strip", "replace",
    "startswith", "endswith", "contains",
    "join", "split",
    "type", "is_defined", "default",
    "coalesce", "concat",
    "to_json", "from_json",
    "to_yaml", "from_yaml",
    "file_exists", "env",
    "uuid", "now", "format_date",
    "regex_match", "regex_replace",
    "sha256", "base64_encode", "base64_decode",
}


def allowed_functions() -> set[str]:
    return ALLOWED_FUNCTIONS.copy()


class ExprLexer:
    """Lexer for AEOS expressions with full position tracking."""

    def __init__(self, text: str, start_offset: int = 0) -> None:
        self._text = text
        self._pos = 0
        self._line = 0
        self._col = 0
        self._start_offset = start_offset
        self._token_patterns: list[tuple[re.Pattern[str], ExprTokenType, str | None]] = []

        self._init_patterns()

    def _init_patterns(self) -> None:
        patterns: list[tuple[str, ExprTokenType, str | None]] = [
            (r"\$\{", ExprTokenType.DOLLAR_LBRACE, None),
            (r"==", ExprTokenType.EQ, None),
            (r"!=", ExprTokenType.NEQ, None),
            (r"<=", ExprTokenType.LE, None),
            (r">=", ExprTokenType.GE, None),
            (r"&&", ExprTokenType.AND, None),
            (r"\|\|", ExprTokenType.OR, None),
            (r"->", ExprTokenType.ARROW, None),
            (r"<<", ExprTokenType.LT, None),
            (r">>", ExprTokenType.GT, None),
            (r"\band\b", ExprTokenType.AND, None),
            (r"\bor\b", ExprTokenType.OR, None),
            (r"\bnot\b", ExprTokenType.NOT, None),
            (r"\bif\b", ExprTokenType.IF, None),
            (r"\belse\b", ExprTokenType.ELSE, None),
            (r"\belif\b", ExprTokenType.ELIF, None),
            (r"\bendif\b", ExprTokenType.ENDIF, None),
            (r"\btrue\b", ExprTokenType.BOOLEAN, None),
            (r"\bfalse\b", ExprTokenType.BOOLEAN, None),
            (r'"', ExprTokenType.STRING, "double"),
            (r"'", ExprTokenType.STRING, "single"),
            (r"\d+(?:\.\d+)?(?:[eE][+-]?\d+)?", ExprTokenType.NUMBER, None),
            (r"[a-zA-Z_][a-zA-Z0-9_]*", ExprTokenType.IDENTIFIER, None),
            (r"\.", ExprTokenType.DOT, None),
            (r":", ExprTokenType.COLON, None),
            (r",", ExprTokenType.COMMA, None),
            (r"\(", ExprTokenType.LPAREN, None),
            (r"\)", ExprTokenType.RPAREN, None),
            (r"\{", ExprTokenType.LBRACE, None),
            (r"\}", ExprTokenType.RBRACE, None),
            (r"\[", ExprTokenType.LBRACKET, None),
            (r"\]", ExprTokenType.RBRACKET, None),
            (r"\|", ExprTokenType.PIPE, None),
            (r"<", ExprTokenType.LT, None),
            (r">", ExprTokenType.GT, None),
            (r"\+", ExprTokenType.PLUS, None),
            (r"-", ExprTokenType.MINUS, None),
            (r"\*", ExprTokenType.STAR, None),
            (r"/", ExprTokenType.SLASH, None),
            (r"%", ExprTokenType.PERCENT, None),
            (r"#", ExprTokenType.HASH, None),
            (r"@", ExprTokenType.AT, None),
            (r"\n", ExprTokenType.NEWLINE, None),
            (r"[ \t]+", None, None),
        ]
        for pat, tok_type, extra in patterns:
            if tok_type is not None:
                self._token_patterns.append((re.compile(pat), tok_type, extra))
            else:
                self._token_patterns.append((re.compile(pat), None, None))

    def tokenize(self) -> list[ExprToken]:
        tokens: list[ExprToken] = []
        while self._pos < len(self._text):
            matched = False
            for pattern, tok_type, extra in self._token_patterns:
                m = pattern.match(self._text, self._pos)
                if m:
                    if tok_type is not None:
                        value = m.group(0)
                        start_pos = self._get_position(m.start())
                        end_pos = self._get_position(m.end())
                        if tok_type == ExprTokenType.STRING:
                            value = self._scan_string(extra == "double")
                            if value is not None:
                                str_end = self._get_position(self._pos)
                                tokens.append(ExprToken(
                                    type=ExprTokenType.STRING,
                                    value=value,
                                    start=start_pos,
                                    end=str_end,
                                ))
                        else:
                            tokens.append(ExprToken(
                                type=tok_type,
                                value=value,
                                start=start_pos,
                                end=end_pos,
                            ))
                    self._pos = m.end()
                    matched = True
                    break
            if not matched:
                self._pos += 1

        eof_pos = self._get_position(len(self._text))
        tokens.append(ExprToken(
            type=ExprTokenType.EOF,
            value="",
            start=eof_pos,
            end=eof_pos,
        ))
        return tokens

    def _scan_string(self, double_quote: bool) -> str | None:
        quote_char = '"' if double_quote else "'"
        self._pos += 1
        result: list[str] = []
        while self._pos < len(self._text):
            ch = self._text[self._pos]
            if ch == "\\":
                self._pos += 1
                if self._pos < len(self._text):
                    esc = self._text[self._pos]
                    escape_map = {
                        "n": "\n", "t": "\t", "r": "\r",
                        '"': '"', "'": "'", "\\": "\\",
                    }
                    result.append(escape_map.get(esc, esc))
                    self._pos += 1
            elif ch == quote_char:
                self._pos += 1
                return "".join(result)
            else:
                result.append(ch)
                self._pos += 1
        return None

    def _get_position(self, offset: int) -> Position:
        line_texts = self._text[:offset].splitlines(keepends=True)
        if not line_texts:
            return Position(line=0, character=0)
        last_line = line_texts[-1]
        if last_line.endswith("\n") or last_line.endswith("\r"):
            return Position(line=len(line_texts), character=0)
        char_count = 0
        for ch in last_line:
            char_count += 2 if ord(ch) >= 0x10000 else 1
        return Position(line=len(line_texts) - 1, character=char_count)


class ExprParser(BaseParser[ExprAstNode]):
    """Parser for AEOS expressions. Uses recursive descent with explicit grammar."""

    file_extensions: set[str] = {".expr"}

    def __init__(self) -> None:
        self._tokens: list[ExprToken] = []
        self._pos: int = 0
        self._errors: list[ParseError] = []
        self._ranges: dict[str, Range] = {}

    def parse(self, text: str, uri: str) -> ParseResult[ExprAstNode]:
        self._tokens = ExprLexer(text).tokenize()
        self._pos = 0
        self._errors = []
        self._ranges = {}
        self._text = text

        if not text.strip():
            return ParseResult(
                ast=ExprAstNode(node_type="empty", range=Range(
                    start=Position(line=0, character=0),
                    end=Position(line=0, character=0),
                )),
            )

        try:
            ast = self._parse_expression()
            self._ranges["expression"] = ast.range
            return ParseResult(ast=ast, errors=self._errors, ranges=self._ranges)
        except ExprError as e:
            error_range = e.token.range if e.token else Range(
                start=Position(line=0, character=0),
                end=Position(line=0, character=0),
            )
            self._errors.append(ParseError(
                message=e.message,
                range=error_range,
                severity=ParseErrorSeverity.ERROR,
                code="EXPR_PARSE_ERROR",
            ))
            return ParseResult(
                ast=ExprAstNode(node_type="error", range=error_range, value=e.message),
                errors=self._errors,
                ranges=self._ranges,
            )

    def parse_file(self, path: str) -> ParseResult[ExprAstNode]:
        text = Path(path).read_text(encoding="utf-8")
        return self.parse(text, path)

    def parse_expression(self, text: str) -> ExprAstNode:
        """Public entry point for parsing a single expression."""
        result = self.parse(text, "")
        return result.ast

    def _peek(self) -> ExprToken:
        return self._tokens[self._pos] if self._pos < len(self._tokens) else self._tokens[-1]

    def _advance(self) -> ExprToken:
        token = self._tokens[self._pos]
        self._pos += 1
        return token

    def _expect(self, *types: ExprTokenType) -> ExprToken:
        token = self._peek()
        if token.type not in types:
            expected = ", ".join(t.name for t in types)
            raise ExprError(f"Expected {expected}, got {token.type.name} ('{token.value}')", token)
        return self._advance()

    def _check(self, *types: ExprTokenType) -> bool:
        return self._peek().type in types

    def _make_range(self, start: ExprToken, end: ExprToken) -> Range:
        return Range(start=start.start, end=end.end)

    def _parse_expression(self) -> ExprAstNode:
        return self._parse_boolean_expr()

    def _parse_boolean_expr(self) -> ExprAstNode:
        left = self._parse_comparison()
        while self._check(ExprTokenType.AND, ExprTokenType.OR):
            op = self._advance()
            right = self._parse_comparison()
            left = ExprAstNode(
                node_type="boolean_op",
                range=self._make_range(self._find_start(left), op),
                children=[left, right],
                value=op.value,
                metadata={"operator": op.value},
            )
        return left

    def _parse_comparison(self) -> ExprAstNode:
        left = self._parse_addition()
        if self._check(ExprTokenType.EQ, ExprTokenType.NEQ, ExprTokenType.LT, ExprTokenType.GT, ExprTokenType.LE, ExprTokenType.GE):
            op = self._advance()
            right = self._parse_addition()
            left = ExprAstNode(
                node_type="comparison",
                range=self._make_range(self._find_start(left), op),
                children=[left, right],
                value=op.value,
                metadata={"operator": op.value},
            )
        return left

    def _parse_addition(self) -> ExprAstNode:
        left = self._parse_term()
        while self._check(ExprTokenType.PLUS, ExprTokenType.MINUS):
            op = self._advance()
            right = self._parse_term()
            left = ExprAstNode(
                node_type="binary_op",
                range=self._make_range(self._find_start(left), op),
                children=[left, right],
                value=op.value,
                metadata={"operator": op.value},
            )
        return left

    def _parse_term(self) -> ExprAstNode:
        left = self._parse_unary()
        while self._check(ExprTokenType.STAR, ExprTokenType.SLASH, ExprTokenType.PERCENT):
            op = self._advance()
            right = self._parse_unary()
            left = ExprAstNode(
                node_type="binary_op",
                range=self._make_range(self._find_start(left), op),
                children=[left, right],
                value=op.value,
                metadata={"operator": op.value},
            )
        return left

    def _parse_unary(self) -> ExprAstNode:
        if self._check(ExprTokenType.NOT, ExprTokenType.MINUS):
            op = self._advance()
            operand = self._parse_unary()
            return ExprAstNode(
                node_type="unary_op",
                range=self._make_range(op, self._find_end(operand)),
                children=[operand],
                value=op.value,
                metadata={"operator": op.value},
            )
        return self._parse_primary()

    def _parse_primary(self) -> ExprAstNode:
        if self._check(ExprTokenType.LPAREN):
            lparen = self._advance()
            expr = self._parse_expression()
            self._expect(ExprTokenType.RPAREN)
            return ExprAstNode(
                node_type="group",
                range=self._make_range(lparen, self._peek()),
                children=[expr],
            )

        if self._check(ExprTokenType.DOLLAR_LBRACE):
            start = self._advance()
            expr = self._parse_expression()
            self._expect(ExprTokenType.RBRACE)
            return ExprAstNode(
                node_type="interpolation",
                range=self._make_range(start, self._peek()),
                children=[expr],
                metadata={"expression": True},
            )

        if self._check(ExprTokenType.IF):
            return self._parse_if_expression()

        if self._check(ExprTokenType.STRING):
            tok = self._advance()
            return ExprAstNode(
                node_type="string",
                range=self._make_range(tok, tok),
                value=tok.value,
            )

        if self._check(ExprTokenType.NUMBER):
            tok = self._advance()
            return ExprAstNode(
                node_type="number",
                range=self._make_range(tok, tok),
                value=tok.value,
            )

        if self._check(ExprTokenType.BOOLEAN):
            tok = self._advance()
            return ExprAstNode(
                node_type="boolean",
                range=self._make_range(tok, tok),
                value=tok.value,
            )

        if self._check(ExprTokenType.IDENTIFIER):
            return self._parse_identifier_expression()

        if self._check(ExprTokenType.LBRACKET):
            return self._parse_array_literal()

        if self._check(ExprTokenType.LBRACE):
            return self._parse_object_literal()

        raise ExprError(f"Unexpected token '{self._peek().value}'", self._peek())

    def _parse_if_expression(self) -> ExprAstNode:
        if_token = self._advance()
        condition = self._parse_expression()
        self._expect(ExprTokenType.COLON)
        then_branch: list[ExprAstNode] = []
        while self._pos < len(self._tokens) - 1:
            tok = self._peek()
            if tok.type in (ExprTokenType.ELIF, ExprTokenType.ELSE, ExprTokenType.ENDIF):
                break
            then_branch.append(self._parse_expression())
            if self._check(ExprTokenType.COMMA):
                self._advance()

        elif_branches: list[list[ExprAstNode]] = []
        elif_conditions: list[ExprAstNode] = []
        while self._check(ExprTokenType.ELIF):
            elif_token = self._advance()
            elif_cond = self._parse_expression()
            self._expect(ExprTokenType.COLON)
            elif_body: list[ExprAstNode] = []
            while self._pos < len(self._tokens) - 1:
                tok = self._peek()
                if tok.type in (ExprTokenType.ELIF, ExprTokenType.ELSE, ExprTokenType.ENDIF):
                    break
                elif_body.append(self._parse_expression())
                if self._check(ExprTokenType.COMMA):
                    self._advance()
            elif_conditions.append(elif_cond)
            elif_branches.append(elif_body)

        else_branch: list[ExprAstNode] = []
        if self._check(ExprTokenType.ELSE):
            self._advance()
            self._expect(ExprTokenType.COLON)
            while self._pos < len(self._tokens) - 1:
                tok = self._peek()
                if tok.type == ExprTokenType.ENDIF:
                    break
                else_branch.append(self._parse_expression())
                if self._check(ExprTokenType.COMMA):
                    self._advance()

        self._expect(ExprTokenType.ENDIF)
        end_tok = self._peek()

        children: list[ExprAstNode] = [condition, ExprAstNode(
            node_type="then_block",
            range=Range(start=condition.range.end, end=end_tok.start),
            children=then_branch,
        )]
        for i, (elif_cond, elif_body) in enumerate(zip(elif_conditions, elif_branches)):
            children.append(elif_cond)
            children.append(ExprAstNode(
                node_type="elif_block",
                range=elif_cond.range if not elif_body else self._make_range(
                    self._find_start(elif_cond),
                    self._find_end(elif_body[-1]),
                ),
                children=elif_body,
            ))
        if else_branch:
            children.append(ExprAstNode(
                node_type="else_block",
                range=Range(start=children[-1].range.end, end=end_tok.start),
                children=else_branch,
            ))

        return ExprAstNode(
            node_type="if_expr",
            range=self._make_range(if_token, end_tok),
            children=children,
        )

    def _parse_identifier_expression(self) -> ExprAstNode:
        ident = self._advance()
        parts = [ident]
        while self._check(ExprTokenType.DOT):
            self._advance()
            parts.append(self._expect(ExprTokenType.IDENTIFIER))

        type_suffix = ""
        if self._check(ExprTokenType.COLON):
            self._advance()
            type_suffix = self._expect(ExprTokenType.IDENTIFIER).value

        if self._check(ExprTokenType.LPAREN):
            return self._parse_function_call(parts[0], parts, type_suffix)

        full_name = ".".join(p.value for p in parts)
        if type_suffix:
            full_name += f":{type_suffix}"

        return ExprAstNode(
            node_type="variable",
            range=self._make_range(parts[0], parts[-1]),
            value=full_name,
            metadata={"parts": [p.value for p in parts], "type_suffix": type_suffix},
        )

    def _parse_function_call(self, name_token: ExprToken, path_parts: list[ExprToken], type_suffix: str) -> ExprAstNode:
        func_name = name_token.value
        if func_name not in ALLOWED_FUNCTIONS:
            raise ExprError(
                f"Function '{func_name}' is not in the allowed list",
                name_token,
            )

        lparen = self._advance()
        args: list[ExprAstNode] = []
        while not self._check(ExprTokenType.RPAREN):
            if self._check(ExprTokenType.EOF):
                raise ExprError("Unclosed function call arguments", lparen)
            args.append(self._parse_expression())
            if self._check(ExprTokenType.COMMA):
                self._advance()
        rparen = self._expect(ExprTokenType.RPAREN)

        return ExprAstNode(
            node_type="function_call",
            range=self._make_range(name_token, rparen),
            value=func_name,
            children=args,
            metadata={"type_suffix": type_suffix},
        )

    def _parse_array_literal(self) -> ExprAstNode:
        lbracket = self._advance()
        elements: list[ExprAstNode] = []
        while not self._check(ExprTokenType.RBRACKET):
            if self._check(ExprTokenType.EOF):
                raise ExprError("Unclosed array literal", lbracket)
            elements.append(self._parse_expression())
            if self._check(ExprTokenType.COMMA):
                self._advance()
        rbracket = self._expect(ExprTokenType.RBRACKET)

        return ExprAstNode(
            node_type="array",
            range=self._make_range(lbracket, rbracket),
            children=elements,
        )

    def _parse_object_literal(self) -> ExprAstNode:
        lbrace = self._advance()
        entries: list[ExprAstNode] = []
        while not self._check(ExprTokenType.RBRACE):
            if self._check(ExprTokenType.EOF):
                raise ExprError("Unclosed object literal", lbrace)
            key = self._parse_expression()
            self._expect(ExprTokenType.COLON)
            value = self._parse_expression()
            entries.append(ExprAstNode(
                node_type="entry",
                range=self._make_range(self._find_start(key), self._find_end(value)),
                children=[key, value],
            ))
            if self._check(ExprTokenType.COMMA):
                self._advance()
        rbrace = self._expect(ExprTokenType.RBRACE)

        return ExprAstNode(
            node_type="object",
            range=self._make_range(lbrace, rbrace),
            children=entries,
        )

    def _find_start(self, node: ExprAstNode) -> ExprToken:
        return ExprToken(
            type=ExprTokenType.IDENTIFIER,
            value=node.value or "",
            start=node.range.start,
            end=node.range.start,
        )

    def _find_end(self, node: ExprAstNode) -> ExprToken:
        return ExprToken(
            type=ExprTokenType.IDENTIFIER,
            value=node.value or "",
            start=node.range.end,
            end=node.range.end,
        )

    @classmethod
    def extract_interpolations(cls, text: str) -> list[tuple[str, Range]]:
        results: list[tuple[str, Range]] = []
        pattern = re.compile(r"\$\{([^}]*)\}")
        for m in pattern.finditer(text):
            expr_text = m.group(1)
            start_offset = m.start()
            end_offset = m.end()
            lines = text.splitlines(keepends=True)
            line = 0
            remaining = start_offset
            for line_text in lines:
                line_len = len(line_text)
                if remaining <= line_len:
                    char_count = 0
                    for ch in line_text[:remaining]:
                        char_count += 2 if ord(ch) >= 0x10000 else 1
                    sub_lines = text.splitlines(keepends=True)
                    end_line = 0
                    end_remaining = end_offset
                    for lt in sub_lines:
                        ll = len(lt)
                        if end_remaining <= ll:
                            end_char = 0
                            for ch in lt[:end_remaining]:
                                end_char += 2 if ord(ch) >= 0x10000 else 1
                            results.append((
                                expr_text,
                                Range(
                                    start=Position(line=line, character=char_count),
                                    end=Position(line=end_line, character=end_char),
                                ),
                            ))
                            break
                        end_remaining -= ll
                        end_line += 1
                    break
                remaining -= line_len
                line += 1
        return results


def allowed_functions() -> set[str]:
    return ALLOWED_FUNCTIONS.copy()
