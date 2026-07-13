from aeos.core.performance.performance_optimizer import PerformanceOptimizer, PerformanceSignal


def test_performance_optimizer_passes_clean_signals():
    plan = PerformanceOptimizer().plan([
        PerformanceSignal("registry_load", 0.01, 0.05, 0.2, "registry"),
        PerformanceSignal("evidence_batch", 0.02, 0.1, 0.3, "evidence"),
    ])

    assert plan["status"] == "PASS"
    assert plan["summary"]["passed"] == 2
    assert plan["blocking_conditions"] == []


def test_performance_optimizer_recommends_for_breached_categories():
    plan = PerformanceOptimizer().plan([
        PerformanceSignal("registry_load", 0.3, 0.05, 0.2, "registry"),
        PerformanceSignal("scan", 7.0, 2.0, 5.0, "scanner"),
    ])

    assert plan["status"] == "BREACHED"
    assert len(plan["blocking_conditions"]) == 2
    areas = {item["area"] for item in plan["recommendations"]}
    assert {"registry", "scanner"} <= areas
