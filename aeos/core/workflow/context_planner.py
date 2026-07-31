from __future__ import annotations

import hashlib
import json
from pathlib import Path
from aeos.core.evidence.evidence_store import EvidenceStore
from aeos.core.redaction.redactor import Redactor
from aeos.core.token_budget import estimate_tokens
from aeos.core.tokens.token_budget_models import ExclusionRule

from .workflow_models import ContextFile, ContextPack, ExcludedContextFile


class ContextPlanner:
    def __init__(
        self,
        workspace_root: str = ".",
        evidence_store: EvidenceStore | None = None,
        max_preview_chars: int = 2000,
    ):
        self.workspace_root = Path(workspace_root).resolve()
        self.evidence_store = evidence_store or EvidenceStore()
        self.max_preview_chars = max_preview_chars
        self.redactor = Redactor()
        self.exclusion_rule = ExclusionRule()

    def build_context_pack(
        self,
        *,
        execution_id: str,
        objective: str,
        target_path: str = ".",
        required_paths: list[str] | None = None,
        evidence_refs: list[str] | None = None,
        token_hard_limit: int = 12000,
        output_reserve_tokens: int = 2000,
    ) -> ContextPack:
        target = self._resolve_under_workspace(target_path)
        paths = required_paths or self._default_context_paths(target)
        files: list[ContextFile] = []
        excluded: list[ExcludedContextFile] = []
        blocking: list[str] = []

        for raw_path in paths:
            try:
                path = self._resolve_under_workspace(raw_path, base=target)
            except ValueError as exc:
                excluded.append(ExcludedContextFile(path=raw_path, reason=str(exc)))
                continue

            if not path.exists():
                excluded.append(ExcludedContextFile(path=str(path), reason="not_found"))
                continue
            if path.is_dir():
                for child in self._iter_context_files(path):
                    item, reason = self._context_file(child)
                    if item:
                        files.append(item)
                    else:
                        excluded.append(ExcludedContextFile(path=str(child), reason=reason))
                continue

            item, reason = self._context_file(path)
            if item:
                files.append(item)
            else:
                excluded.append(ExcludedContextFile(path=str(path), reason=reason))

        estimated = sum(item.estimated_tokens for item in files)
        available = max(token_hard_limit - output_reserve_tokens, 0)
        if estimated > available:
            blocking.append("context_pack_exceeds_available_token_budget")

        pack = ContextPack(
            execution_id=execution_id,
            objective=objective,
            target_path=str(target),
            files=files,
            excluded_files=excluded,
            evidence_refs=list(evidence_refs or []),
            token_budget={
                "hard_limit": token_hard_limit,
                "output_reserve_tokens": output_reserve_tokens,
                "available_input_tokens": available,
            },
            status="BLOCKED" if blocking else "PASS",
            blocking_conditions=blocking,
        )
        self._persist_pack(pack)
        self.evidence_store.store_record(execution_id, "context-pack", pack.to_dict())
        return pack

    def _default_context_paths(self, target: Path) -> list[str]:
        candidates = [
            "AGENT.md",
            "package.json",
            "pyproject.toml",
            "requirements-dev.txt",
            "aeos/config/token-budget-governor.config.yaml",
            "aeos/config/optimized-prompt-policy.yaml",
            "aeos/config/model-router.config.yaml",
            "aeos/config/workflow-kernel.config.yaml",
        ]
        return [item for item in candidates if (target / item).exists()]

    def _iter_context_files(self, directory: Path) -> list[Path]:
        files: list[Path] = []
        for path in sorted(directory.rglob("*")):
            if path.is_file():
                files.append(path)
        return files

    def _context_file(self, path: Path) -> tuple[ContextFile | None, str]:
        rel = self._relative(path)
        excluded, reason = self.exclusion_rule.is_excluded(rel), "matched_exclusion_pattern"
        if excluded:
            return None, reason
        try:
            raw = path.read_bytes()
        except OSError:
            return None, "unreadable"
        if len(raw) > 1024 * 1024:
            return None, "file_too_large"
        text = raw.decode("utf-8", errors="replace")
        preview, findings = self.redactor.redact(text[: self.max_preview_chars])
        digest = hashlib.sha256(raw).hexdigest()
        cache_key = hashlib.sha256(f"{rel}:{digest}".encode("utf-8")).hexdigest()
        return (
            ContextFile(
                path=rel,
                sha256=digest,
                bytes=len(raw),
                estimated_tokens=estimate_tokens(preview),
                cache_key=cache_key,
                preview=preview,
                redaction_findings=findings,
            ),
            "",
        )

    def _resolve_under_workspace(self, value: str, base: Path | None = None) -> Path:
        raw = Path(value)
        root = base or self.workspace_root
        path = raw if raw.is_absolute() else root / raw
        resolved = path.resolve()
        try:
            resolved.relative_to(self.workspace_root)
        except ValueError as exc:
            raise ValueError("path_outside_workspace") from exc
        return resolved

    def _relative(self, path: Path) -> str:
        try:
            return str(path.resolve().relative_to(self.workspace_root))
        except ValueError:
            return str(path)

    def _persist_pack(self, pack: ContextPack) -> str:
        base = self.workspace_root / ".aeos" / "evidence" / pack.execution_id
        base.mkdir(parents=True, exist_ok=True)
        path = base / "context-pack.json"
        path.write_text(json.dumps(pack.to_dict(), indent=2, ensure_ascii=False), encoding="utf-8")
        return str(path)
