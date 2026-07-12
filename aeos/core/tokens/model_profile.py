"""Registry of model profiles for token cost estimation."""

from __future__ import annotations

from typing import Dict, List, Optional

from .token_budget_models import ModelProfile


class ModelProfileRegistry:
    """Registry of known model profiles for token cost estimation."""

    def __init__(self):
        self._profiles: Dict[str, ModelProfile] = {}
        self._register_defaults()

    def _register_defaults(self) -> None:
        defaults = [
            ModelProfile("deepseek-v4", "deepseek", 0.0, 0.0, 128000, recommended=True),
            ModelProfile("gemini-3-pro", "google", 0.0025, 0.01, 1048576),
            ModelProfile("gpt-5", "openai", 0.01, 0.04, 131072),
            ModelProfile("claude-4", "anthropic", 0.015, 0.075, 200000),
            ModelProfile("llama-3-70b", "meta", 0.0, 0.0, 8192),
            ModelProfile("mistral-large", "mistral", 0.002, 0.006, 32768),
            ModelProfile("local-llama", "local", 0.0, 0.0, 8192),
            ModelProfile("local-mistral", "local", 0.0, 0.0, 32768),
        ]
        for profile in defaults:
            self._profiles[profile.model_id] = profile

    def get(self, model_id: str) -> Optional[ModelProfile]:
        return self._profiles.get(model_id)

    def register(self, profile: ModelProfile) -> None:
        self._profiles[profile.model_id] = profile

    def cheapest(
        self,
        input_tokens: int = 0,
        output_tokens: int = 0,
    ) -> ModelProfile:
        best = None
        best_cost = float("inf")
        for profile in self._profiles.values():
            cost = (
                profile.input_cost_per_1k * input_tokens / 1000
                + profile.output_cost_per_1k * output_tokens / 1000
            )
            if cost < best_cost:
                best_cost = cost
                best = profile
        return best or ModelProfile("unknown", "unknown", 0, 0, 0)

    def list_profiles(self) -> List[ModelProfile]:
        return list(self._profiles.values())

    def recommended(self) -> List[ModelProfile]:
        return [p for p in self._profiles.values() if p.recommended]
