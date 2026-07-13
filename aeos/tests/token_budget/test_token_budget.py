from aeos.core.token_budget import TokenBudgetGovernor, estimate_tokens


def test_estimate_tokens_is_conservative_for_short_text():
    assert estimate_tokens("abcd") == 1
    assert estimate_tokens("abcde") == 2


def test_token_budget_passes_small_prompt():
    decision = TokenBudgetGovernor().evaluate("Build a small API", provider="deepseek-free")
    assert decision.status == "PASS"


def test_token_budget_blocks_large_prompt_for_free_model():
    decision = TokenBudgetGovernor().evaluate("x" * 40000, provider="deepseek-free")
    assert decision.status == "BLOCKED"
    assert decision.blocking_conditions


def test_subagent_budget_splits_parent_budget_with_reserve():
    budget = TokenBudgetGovernor().subagent_budget(12000, 3)
    assert budget == 3000
