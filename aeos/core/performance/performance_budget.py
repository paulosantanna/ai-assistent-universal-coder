from dataclasses import dataclass

@dataclass
class PerformanceBudget:
    name: str
    p50_seconds: float
    p95_seconds: float
    max_files: int | None = None
    max_file_mb: int | None = None

class PerformanceBudgetGuard:
    def evaluate(self, budget: PerformanceBudget, actual_seconds: float) -> dict:
        if actual_seconds > budget.p95_seconds:
            return {"status": "BREACHED", "severity": "high", "reason": "p95_budget_exceeded"}
        if actual_seconds > budget.p50_seconds:
            return {"status": "WARN", "severity": "medium", "reason": "p50_budget_exceeded"}
        return {"status": "PASS", "severity": "low", "reason": "within_budget"}
