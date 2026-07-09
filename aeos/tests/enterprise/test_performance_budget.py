from aeos.core.performance.performance_budget import PerformanceBudget, PerformanceBudgetGuard

def test_budget_pass():
    guard = PerformanceBudgetGuard()
    result = guard.evaluate(PerformanceBudget("scan", 10, 30), 5)
    assert result["status"] == "PASS"

def test_budget_breached():
    guard = PerformanceBudgetGuard()
    result = guard.evaluate(PerformanceBudget("scan", 10, 30), 31)
    assert result["status"] == "BREACHED"
