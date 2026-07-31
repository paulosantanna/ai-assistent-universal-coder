# N8N Automation Orchestration

## Goal

Orchestrate repeatable AEOS operations through N8N without transferring governance decisions to the automation layer.

## Flow

1. Load the approved specification and current normative hash.
2. Validate the workflow against the AEOS allowlist.
3. Start in dry-run and record the correlation ID.
4. Require explicit approval before enabling remote side effects.
5. Trigger the workflow with minimal payload and no secrets.
6. Collect logs, metrics and resulting evidence references.
7. Submit evidence to the AEOS judge.

## Non-delegable Decisions

N8N MUST NOT approve specifications, accept delivery, bypass quality gates, or expose provider credentials.
