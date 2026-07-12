"""Data models for token budget management."""

from __future__ import annotations

import hashlib
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Any, Dict, List, Optional


class TokenPriority(Enum):
    critical_context = auto()
    useful_context = auto()
    optional_context = auto()
    excluded_context = auto()


@dataclass
class TokenUsageRecord:
    subagent_id: str
    operation: str
    tokens_charged: int
    label: str = ""
    timestamp_utc: str = ""


@dataclass
class TokenBudgetState:
    subagent_id: str
    budget: int
    consumed: int = 0
    blocked: bool = False

    @property
    def remaining(self) -> int:
        return self.budget - self.consumed

    @property
    def utilization_pct(self) -> float:
        if self.budget == 0:
            return 0.0
        return round((self.consumed / self.budget) * 100, 1)

    @property
    def status(self) -> str:
        if self.blocked:
            return "TOKEN_BUDGET_BLOCKED"
        if self.utilization_pct >= 100:
            return "EXHAUSTED"
        if self.utilization_pct >= 80:
            return "WARN"
        return "OK"


@dataclass
class TokenBudgetPolicy:
    global_budget: int = 100000
    per_subagent_default: int = 10000
    overage_block: bool = True
    warn_threshold_pct: float = 80.0


@dataclass
class TokenBudgetAllocation:
    subagent_id: str
    budget: int
    priority: TokenPriority = TokenPriority.useful_context
    consumed: int = 0
    cache_hits: int = 0
    cache_misses: int = 0
    compression_ratio: float = 1.0
    records: List[TokenUsageRecord] = field(default_factory=list)


@dataclass
class ExclusionRule:
    patterns: List[str] = field(default_factory=lambda: [
        ".venv", "venv", "__pycache__", ".git", "node_modules",
        "*.bin", "*.onnx", "*.pt", "*.pth", "*.pkl", "*.joblib",
        "*.h5", "*.gguf", "*.safetensors",
        "*.db", "*.sqlite", "*.sqlite3",
        "*.log", "*.lock",
        ".env", ".env.local", ".env.production",
        "secrets/",
        "data/", "datasets/", "models/",
        "chroma/", "chromadb/", "vectorstores/",
    ])

    def is_excluded(self, file_path: str) -> bool:
        import fnmatch
        for pattern in self.patterns:
            if fnmatch.fnmatch(file_path, pattern):
                return True
            if pattern.endswith("/") and pattern.rstrip("/") in file_path.split("/"):
                return True
            if pattern.endswith("/") and pattern.rstrip("/") in file_path.split("\\"):
                return True
        return False


@dataclass
class ModelProfile:
    model_id: str
    provider: str
    input_cost_per_1k: float
    output_cost_per_1k: float
    max_context_tokens: int
    recommended: bool = False
