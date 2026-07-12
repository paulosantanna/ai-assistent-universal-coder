from __future__ import annotations

import logging
import threading
from typing import Any

from aeos_lsp.runtime.ports import TokenBudget, TokenBudgetPort

logger = logging.getLogger(__name__)


class TokenBudgetAdapter(TokenBudgetPort):
    def __init__(self) -> None:
        self._initialized = False
        self._lock = threading.RLock()
        self._budgets: dict[str, TokenBudget] = {}
        self._default_max: int = 4096

    async def initialize(self, config: dict[str, Any] | None = None) -> None:
        self._initialized = True
        if config:
            self._default_max = config.get("default_max_tokens", self._default_max)
        logger.info("Token budget adapter initialized (default_max=%d)", self._default_max)

    async def shutdown(self) -> None:
        self._initialized = False
        with self._lock:
            self._budgets.clear()
        logger.info("Token budget adapter shut down")

    async def check_budget(self, agent_id: str, estimated_tokens: int) -> TokenBudget:
        with self._lock:
            budget = self._budgets.get(agent_id)
            if budget is None:
                budget = TokenBudget(max_tokens=self._default_max)
                self._budgets[agent_id] = budget

            budget.remaining_tokens = budget.max_tokens - budget.used_tokens
            budget.warnings = []

            if estimated_tokens > budget.remaining_tokens:
                budget.warnings.append(
                    f"Estimated {estimated_tokens} tokens exceeds remaining budget of {budget.remaining_tokens}"
                )
            if budget.remaining_tokens < budget.max_tokens * 0.1:
                budget.warnings.append(
                    f"Token budget nearly exhausted: {budget.remaining_tokens}/{budget.max_tokens} remaining"
                )

            return budget

    async def consume(self, agent_id: str, tokens: int) -> bool:
        with self._lock:
            budget = self._budgets.get(agent_id)
            if budget is None:
                budget = TokenBudget(max_tokens=self._default_max)
                self._budgets[agent_id] = budget

            if budget.used_tokens + tokens > budget.max_tokens:
                logger.warning(
                    "Token consumption would exceed budget for %s: %d + %d > %d",
                    agent_id, budget.used_tokens, tokens, budget.max_tokens,
                )
                return False

            budget.used_tokens += tokens
            budget.remaining_tokens = budget.max_tokens - budget.used_tokens
            return True

    async def reset(self, agent_id: str) -> None:
        with self._lock:
            budget = self._budgets.get(agent_id)
            if budget is not None:
                budget.used_tokens = 0
                budget.remaining_tokens = budget.max_tokens
                budget.warnings.clear()
                logger.info("Reset token budget for %s", agent_id)

    async def get_budget(self, agent_id: str) -> TokenBudget:
        with self._lock:
            budget = self._budgets.get(agent_id)
            if budget is None:
                budget = TokenBudget(max_tokens=self._default_max)
                self._budgets[agent_id] = budget
            budget.remaining_tokens = budget.max_tokens - budget.used_tokens
            return budget

    def set_default_max(self, max_tokens: int) -> None:
        self._default_max = max_tokens

    async def health_check(self) -> dict[str, Any]:
        with self._lock:
            return {
                "status": "ok" if self._initialized else "not_initialized",
                "active_agents": len(self._budgets),
                "default_max_tokens": self._default_max,
            }
