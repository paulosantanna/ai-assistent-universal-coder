"""Context compression for token budget management.

Reduces file content to essential tokens based on priority level,
file type, and content characteristics.
"""

from __future__ import annotations

import os
import re
from typing import Optional, Tuple

from .token_budget_models import ExclusionRule, TokenPriority


class ContextCompressor:
    """Compresses file content to fit within token budgets."""

    def __init__(self, exclusion_rule: Optional[ExclusionRule] = None):
        self.exclusion_rule = exclusion_rule or ExclusionRule()

    def is_excluded(self, file_path: str) -> Tuple[bool, str]:
        if self.exclusion_rule.is_excluded(file_path):
            return True, "matched_exclusion_pattern"
        try:
            size = os.path.getsize(file_path)
            if size > 10 * 1024 * 1024:
                return True, "file_too_large"
        except OSError:
            return True, "unreadable"
        return False, ""

    def compress(
        self,
        content: str,
        file_path: str,
        priority: TokenPriority,
        target_tokens: Optional[int] = None,
    ) -> Tuple[str, float]:
        original_chars = len(content)
        original_tokens = original_chars // 4

        if priority == TokenPriority.critical_context:
            result = content
        elif priority == TokenPriority.excluded_context:
            result = ""
        else:
            ext = os.path.splitext(file_path)[1].lower()
            if ext in (".py", ".js", ".ts", ".java", ".rs", ".go", ".c", ".cpp", ".h"):
                result = self._compress_code(content, priority)
            elif ext in (".md", ".rst", ".txt"):
                result = self._compress_doc(content, priority)
            elif ext in (".yaml", ".yml", ".toml", ".json", ".cfg", ".ini", ".conf"):
                result = self._compress_config(content, priority)
            else:
                result = self._compress_generic(content, priority)

            if target_tokens and (len(result) // 4) > target_tokens:
                lines = result.split("\n")
                max_chars = target_tokens * 4
                truncated = ""
                for line in lines:
                    if len(truncated) + len(line) + 1 > max_chars:
                        truncated += f"\n... truncated ({len(lines)} lines total)"
                        break
                    truncated += line + "\n"
                result = truncated

        compressed_chars = len(result)
        compressed_tokens = compressed_chars // 4
        ratio = compressed_tokens / original_tokens if original_tokens > 0 else 1.0

        result = re.sub(r"\n{3,}", "\n\n", result)
        return result.strip(), round(ratio, 4)

    def _compress_code(self, content: str, priority: TokenPriority) -> str:
        lines = content.split("\n")
        imports = [l for l in lines if l.startswith(("import ", "from "))]
        signatures = [
            l for l in lines
            if re.match(r"^\s*(def |class |async def |@)", l)
        ]

        if priority == TokenPriority.optional_context:
            result = "\n".join(imports)
            if signatures:
                result += "\n" + "\n".join(signatures)
            return result

        result = "\n".join(imports) + "\n" + "\n".join(signatures)
        tail = lines[-25:] if len(lines) > 50 else []
        if tail:
            result += "\n\n# ... (tail " + str(len(tail)) + " lines)"
            result += "\n" + "\n".join(tail)
        return result

    def _compress_doc(self, content: str, priority: TokenPriority) -> str:
        lines = content.split("\n")
        headers = [l for l in lines if l.startswith("#")]

        if priority == TokenPriority.optional_context:
            return "\n".join(headers)

        result = "\n".join(headers)
        body_start = next(
            (i for i, l in enumerate(lines) if l.strip() and not l.startswith("#")),
            len(lines),
        )
        remaining = lines[body_start:]
        if remaining:
            result += "\n\n" + "\n".join(remaining[:30])
            if len(remaining) > 40:
                result += f"\n\n... ({len(remaining)} total lines in body)"
                tail = remaining[-10:] if len(remaining) > 10 else []
                if tail:
                    result += "\n" + "\n".join(tail)
        return result

    def _compress_config(self, content: str, priority: TokenPriority) -> str:
        lines = content.split("\n")
        kv_lines = [l for l in lines if ":" in l or "=" in l]
        if len(kv_lines) > 40:
            shown = kv_lines[:35]
            shown.append(f"# ... ({len(kv_lines) - 35} more keys)")
            result = "\n".join(shown)
        else:
            result = "\n".join(lines[:80])
        return result

    def _compress_generic(self, content: str, priority: TokenPriority) -> str:
        lines = content.split("\n")
        if len(lines) > 60:
            head = lines[:20]
            tail = lines[-20:]
            result = "\n".join(head)
            result += f"\n\n... ({len(lines)} total lines, showing first 20 and last 20)"
            result += "\n" + "\n".join(tail)
        else:
            result = content
        return result
