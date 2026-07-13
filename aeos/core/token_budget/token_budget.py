from __future__ import annotations

from dataclasses import dataclass


PROVIDER_DEFAULT_LIMITS = {
    "gpt": 32000,
    "openai": 32000,
    "codex": 24000,
    "claude": 32000,
    "deepseek": 16000,
    "deepseek-free": 8000,
    "local": 12000,
    "unknown": 8000,
}


def estimate_tokens(text: str) -> int:
    """Cheap conservative estimator: roughly 4 chars/token, with floor for short prompts."""
    if not text:
        return 0
    return max(1, (len(text) + 3) // 4)


@dataclass(frozen=True)
class TokenBudgetDecision:
    status: str
    provider: str
    estimated_tokens: int
    limit: int
    hard_limit: int
    recommendations: list[str]
    blocking_conditions: list[str]

    def to_dict(self) -> dict:
        return {
            "status": self.status,
            "provider": self.provider,
            "estimated_tokens": self.estimated_tokens,
            "limit": self.limit,
            "hard_limit": self.hard_limit,
            "recommendations": self.recommendations,
            "blocking_conditions": self.blocking_conditions,
        }


class TokenBudgetGovernor:
    def __init__(self, provider_limits: dict[str, int] | None = None):
        self.provider_limits = {**PROVIDER_DEFAULT_LIMITS, **(provider_limits or {})}

    def evaluate(
        self,
        prompt: str,
        provider: str = "unknown",
        requested_output_tokens: int = 2000,
        task_priority: str = "normal",
    ) -> TokenBudgetDecision:
        provider_key = provider.lower()
        hard_limit = self.provider_limits.get(provider_key, self.provider_limits["unknown"])
        reserve = max(512, requested_output_tokens)
        limit = max(1, hard_limit - reserve)
        estimated = estimate_tokens(prompt)
        recommendations = []
        blocking = []

        if estimated > limit:
            blocking.append("prompt exceeds provider token budget after output reserve")
            recommendations.extend(self._reduction_steps(task_priority))
            status = "BLOCKED"
        elif estimated > int(limit * 0.75):
            recommendations.extend(self._reduction_steps(task_priority))
            status = "REVIEW"
        else:
            recommendations.append("Proceed with current prompt; keep file refs instead of pasted content.")
            status = "PASS"

        return TokenBudgetDecision(
            status=status,
            provider=provider_key,
            estimated_tokens=estimated,
            limit=limit,
            hard_limit=hard_limit,
            recommendations=recommendations,
            blocking_conditions=blocking,
        )

    def subagent_budget(self, parent_limit: int, subagent_count: int, reserve_ratio: float = 0.25) -> int:
        if subagent_count <= 0:
            return parent_limit
        usable = int(parent_limit * (1 - reserve_ratio))
        return max(512, usable // subagent_count)

    def _reduction_steps(self, task_priority: str) -> list[str]:
        steps = [
            "replace pasted files with path refs and line-scoped summaries",
            "drop unrelated history and generated artifacts",
            "ask one clarifying question when required inputs are missing",
            "delegate only narrow sub-tasks with explicit output schemas",
            "stop instead of expanding scope beyond the user request",
        ]
        if task_priority != "high":
            steps.insert(0, "run a narrower first pass before deep analysis")
        return steps
