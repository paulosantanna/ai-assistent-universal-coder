from medical_research_mcp.subagents import registry,create_tasks
def test_registry(): assert len(registry())>=10 and "expert-judge" in registry()
def test_budget(): assert all(x["context_budget_tokens"]>=512 for x in create_tasks("audit",20000))
