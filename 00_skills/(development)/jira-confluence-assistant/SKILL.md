---
name: jira-confluence-assistant
description: "Prepare governed Jira/Confluence work with traceability to code and evidence. Use for Jira/Confluence tracing. Do NOT use for unrelated stacks."
license: CC-BY-4.0
metadata:
  author: AEOS
  version: 1.0.0
  owner_agent: codenavi-agent
---

# Skill: jira-confluence-assistant

Governance: CodENavi Full Workspace v2 (BRIEFING→DEBRIEF); skill of `codenavi-agent`; inherits `AGENTS.md`. Lenses are internal; no new agent identities; no bypass of secret or permission gates.

## Mission
Read, analyze and prepare governed Jira/Confluence work while preserving traceability between requirement, code, evidence and documentation.

## Workflow
BRIEFING: identify issue/page, objective, expected outcome and authority.
RECON: current ticket/page, linked requirements, code/docs/tests, prior decisions and notebook notes.
PLAN: minimal updates and verification criteria.
EXECUTE: draft or apply only authorized changes through connected official tools.
VERIFY: re-read resulting state and cross-check links/status/acceptance criteria.
DEBRIEF: record pointers and stale knowledge updates.

## Rules
- Never invent ticket state, assignee, acceptance criteria or Confluence content.
- Preserve IDs, project keys and technical nomenclature exactly.
- Comments/status changes are mutations and require appropriate authorization.
- Prefer pointers over duplicating entire tickets/pages into memory.

Provenance: [provenance](references/provenance.md). Examples and failures: [usage and verification](references/usage-and-verification.md), read when selecting the skill or a step fails.

## Response

Output: result first, then evidence (paths, commands, results), blockers and next step. No narration or restated instructions. Follow a defined output schema exactly. Reply in the user's language.
