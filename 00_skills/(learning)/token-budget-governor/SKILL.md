---
name: token-budget-governor
description: Prevent token waste across GPT, Codex, Claude, DeepSeek and local/free models by enforcing scoped prompts, compact context and narrow internal lenses contracts. Use when the user requests token budget governor or invokes token-budget-governor. Do NOT use to promote unverified claims or transient task status into durable memory.
license: CC-BY-4.0
metadata:
  author: AEOS
  version: 1.0.0
  owner_agent: codenavi-agent
---

# Skill: token-budget-governor

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; inherit `AGENTS.md`.
Lifecycle: BRIEFING → RECON → PLAN → EXECUTE → VERIFY → DEBRIEF.
Source roles/workers are internal lenses. Never create agent identities or bypass runtime secret/permission gates.

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

Provenance and source freshness: [provenance](references/provenance.md).

Example usage and failure handling: read [usage and verification](references/usage-and-verification.md) when selecting this skill or a required step fails.
