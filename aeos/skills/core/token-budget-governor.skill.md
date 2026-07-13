# Skill: token-budget-governor

## Mission

Prevent token waste across GPT, Codex, Claude, DeepSeek and local/free models by enforcing scoped prompts, compact context and narrow subagent contracts.

## Allowed Actions

- Estimate prompt and output token budgets.
- Recommend context reduction.
- Split budgets across subagents.
- Block unbounded or unrequested work.
- Generate token budget reports.

## Forbidden Actions

- Broadcast full context to all subagents.
- Re-read whole repositories without evidence of need.
- Expand scope without user approval.
- Use long-context models when targeted reads are enough.
- Continue after the requested task is satisfied.

## Required Inputs

- provider
- prompt_scope
- requested_output_tokens
- task_priority
- subagent_count

## Output Schema

```json
{
  "status": "PASS|REVIEW|BLOCKED",
  "estimated_tokens": 0,
  "limit": 0,
  "provider": "",
  "subagent_budget": 0,
  "recommendations": [],
  "blocking_conditions": []
}
```

## Quality Gates

- Prompt uses file refs instead of pasted files when possible.
- Subagents receive only narrow task contracts.
- Output schema is explicit.
- Stop conditions are explicit.
- Provider limits are respected.

## Stop Conditions

- Prompt exceeds provider budget.
- Subagent scope is broad or duplicated.
- Missing output schema.
- Unrequested work detected.
