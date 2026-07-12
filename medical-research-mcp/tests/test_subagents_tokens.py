from medical_research_mcp.subagents import create_tasks, registry
from medical_research_mcp.token_budget import TokenBudget, context_cache_key


def test_unique_specialized_subagents_exist() -> None:
    agents = registry()
    assert len(agents) >= 19
    assert "rag-specialist" in agents
    assert "vulnerability-intelligence-specialist" in agents
    assert "expert-judge" in agents


def test_tasks_have_bounded_token_budgets() -> None:
    tasks = create_tasks("audit project", 60000)
    assert all(task["context_budget_tokens"] >= 512 for task in tasks)
    assert all(task["output_budget_tokens"] <= 3500 for task in tasks)


def test_budget_totals_are_partitioned() -> None:
    allocation = TokenBudget(10000).allocate()
    assert sum(allocation.values()) == 10000


def test_context_hash_is_deterministic() -> None:
    assert context_cache_key({"a": 1, "b": 2}) == context_cache_key({"b": 2, "a": 1})
