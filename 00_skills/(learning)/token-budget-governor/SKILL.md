---
name: token-budget-governor
description: "Prevent token waste with scoped prompts, compact context and narrow lenses. Use for token budget governance. Do NOT use to promote unverified claims."
license: CC-BY-4.0
metadata:
  author: AEOS
  version: 1.0.0
  owner_agent: codenavi-agent
---

# Skill: token-budget-governor

Governance: CodENavi Full Workspace v2 (BRIEFING→DEBRIEF); skill of `codenavi-agent`; inherits `AGENTS.md`. Lenses are internal; no new agent identities; no bypass of secret or permission gates.

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

Provenance: [provenance](references/provenance.md). Examples and failures: [usage and verification](references/usage-and-verification.md), read when selecting the skill or a step fails.

## Response

Output: result first, then evidence (paths, commands, results), blockers and next step. No narration or restated instructions. Follow a defined output schema exactly. Reply in the user's language.
