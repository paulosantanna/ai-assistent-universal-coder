"""Central orchestrator for token budget management across phases and subagents."""

from __future__ import annotations

import time
from typing import Any, Dict, List, Optional, Tuple

from .token_budget_models import (
    TokenBudgetAllocation,
    TokenBudgetPolicy,
    TokenBudgetState,
    TokenPriority,
    TokenUsageRecord,
)
from .context_cache import TokenContextCache
from .context_compressor import ContextCompressor
from .token_reporter import TokenReporter


class TokenBudgetManager:
    """Manages token budgets for AEOS phases and subagents.

    Usage:
        tm = TokenBudgetManager()
        tm.begin_phase("phase-12")
        tm.allocate("observability-architect-sa", 14000)
        content, state = tm.read_context(sa_id, file_path, priority)
        if state.blocked:
            return {"status": "TOKEN_BUDGET_BLOCKED"}
        tm.add_context(sa_id, extra_content, priority)
        tm.charge(sa_id, tokens)
        tm.status() -> dict
    """

    def __init__(
        self,
        policy: Optional[TokenBudgetPolicy] = None,
        cache: Optional[TokenContextCache] = None,
        compressor: Optional[ContextCompressor] = None,
    ):
        self.policy = policy or TokenBudgetPolicy()
        self.cache = cache or TokenContextCache()
        self.compressor = compressor or ContextCompressor()
        self.reporter = TokenReporter()
        self._allocations: Dict[str, TokenBudgetAllocation] = {}
        self._global_consumed: int = 0
        self._phase: str = ""
        self._phase_start: float = 0.0

    def begin_phase(self, phase: str) -> None:
        self._phase = phase
        self._allocations.clear()
        self._global_consumed = 0
        self._phase_start = time.time()
        self.reporter.reset()

    @property
    def phase(self) -> str:
        return self._phase

    def allocate(
        self,
        subagent_id: str,
        budget: int,
        priority: TokenPriority = TokenPriority.useful_context,
    ) -> TokenBudgetState:
        if subagent_id in self._allocations:
            raise ValueError(f"Subagent {subagent_id} already allocated")
        alloc = TokenBudgetAllocation(
            subagent_id=subagent_id,
            budget=budget,
            priority=priority,
        )
        self._allocations[subagent_id] = alloc
        return TokenBudgetState(
            subagent_id=subagent_id,
            budget=budget,
            consumed=0,
            blocked=False,
        )

    def read_context(
        self, subagent_id: str, file_path: str, priority: TokenPriority
    ) -> Tuple[str, TokenBudgetState]:
        state = self.state(subagent_id)
        if state.blocked:
            return ("", state)

        if self.policy.overage_block and self._global_consumed >= self.policy.global_budget:
            return ("", TokenBudgetState(
                subagent_id=subagent_id,
                budget=state.budget,
                consumed=state.consumed,
                blocked=True,
            ))

        alloc = self._allocations.get(subagent_id)
        if alloc is None:
            return ("", TokenBudgetState(
                subagent_id=subagent_id, budget=0, consumed=0, blocked=True
            ))

        import hashlib
        try:
            with open(file_path, "rb") as f:
                content = f.read()
            content_str = content.decode("utf-8", errors="replace")
        except (OSError, UnicodeDecodeError):
            return ("", state)

        content_hash = hashlib.sha256(content).hexdigest()

        cached = self.cache.get(file_path, content_hash, "deepseek-v4")
        if cached is not None:
            alloc.cache_hits += 1
            tokens_used = len(cached) // 4
            self._charge(subagent_id, tokens_used, "cache_read")
            compressed = cached
        else:
            alloc.cache_misses += 1
            compressed, ratio = self.compressor.compress(
                content_str, file_path, priority
            )
            alloc.compression_ratio = ratio
            self.cache.put(file_path, content_hash, "deepseek-v4", compressed)
            tokens_used = len(compressed) // 4
            self._charge(subagent_id, tokens_used, "compress_read")

        return compressed, self.state(subagent_id)

    def add_context(
        self,
        subagent_id: str,
        content: str,
        priority: TokenPriority,
        label: str = "inline",
    ) -> TokenBudgetState:
        state = self.state(subagent_id)
        if state.blocked:
            return state

        tokens = len(content) // 4
        self._charge(subagent_id, tokens, f"add_context:{label}")
        return self.state(subagent_id)

    def charge(
        self, subagent_id: str, tokens: int, operation: str = "explicit"
    ) -> TokenBudgetState:
        self._charge(subagent_id, tokens, operation)
        return self.state(subagent_id)

    def _charge(self, subagent_id: str, tokens: int, operation: str) -> None:
        alloc = self._allocations.get(subagent_id)
        if alloc is None:
            return
        alloc.consumed += tokens
        self._global_consumed += tokens
        alloc.records.append(TokenUsageRecord(
            subagent_id=subagent_id,
            operation=operation,
            tokens_charged=tokens,
        ))

    def state(self, subagent_id: str) -> TokenBudgetState:
        alloc = self._allocations.get(subagent_id)
        if alloc is None:
            return TokenBudgetState(
                subagent_id=subagent_id, budget=0, consumed=0, blocked=True
            )
        blocked = False
        if self.policy.overage_block:
            if alloc.consumed >= alloc.budget:
                blocked = True
            if self._global_consumed >= self.policy.global_budget:
                blocked = True
        return TokenBudgetState(
            subagent_id=subagent_id,
            budget=alloc.budget,
            consumed=alloc.consumed,
            blocked=blocked,
        )

    def status(self, subagent_id: Optional[str] = None) -> Dict[str, Any]:
        if subagent_id:
            alloc = self._allocations.get(subagent_id)
            if alloc is None:
                return {"error": f"unknown subagent: {subagent_id}"}
            return {
                "subagent_id": subagent_id,
                "budget": alloc.budget,
                "consumed": alloc.consumed,
                "remaining": alloc.budget - alloc.consumed,
                "utilization_pct": alloc.utilization_pct
                    if hasattr(alloc, "utilization_pct")
                    else round((alloc.consumed / alloc.budget) * 100, 1),
                "blocked": self.state(subagent_id).blocked,
                "cache_hits": alloc.cache_hits,
                "cache_misses": alloc.cache_misses,
                "compression_ratio": alloc.compression_ratio,
            }

        total_budget = sum(a.budget for a in self._allocations.values())
        allocs_status = []
        for aid, alloc in self._allocations.items():
            s = self.state(aid)
            allocs_status.append({
                "subagent_id": aid,
                "budget": alloc.budget,
                "consumed": alloc.consumed,
                "remaining": s.remaining,
                "utilization_pct": s.utilization_pct,
                "blocked": s.blocked,
                "status": s.status,
                "cache_hits": alloc.cache_hits,
                "cache_misses": alloc.cache_misses,
                "compression_ratio": alloc.compression_ratio,
            })

        return {
            "phase": self._phase,
            "global_budget": self.policy.global_budget,
            "global_consumed": self._global_consumed,
            "global_remaining": self.policy.global_budget - self._global_consumed,
            "total_allocated": total_budget,
            "subagents": allocs_status,
        }

    def summary(self) -> Dict[str, Any]:
        return self.status()

    @property
    def blocked(self) -> bool:
        if self._global_consumed >= self.policy.global_budget:
            return True
        return any(self.state(aid).blocked for aid in self._allocations)
