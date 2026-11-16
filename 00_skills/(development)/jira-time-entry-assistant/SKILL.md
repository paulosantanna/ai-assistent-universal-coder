---
name: jira-time-entry-assistant
description: "Prepare auditable Jira worklog proposals from actual task evidence. Use for Jira time entries. Do NOT use for unrelated stacks or deployment."
license: CC-BY-4.0
metadata:
  author: AEOS
  version: 1.0.0
  owner_agent: codenavi-agent
---

# Jira Time Entry Assistant

Governance: CodENavi Full Workspace v2 (BRIEFING→DEBRIEF); skill of `codenavi-agent`; inherits `AGENTS.md`. Lenses are internal; no new agent identities; no bypass of secret or permission gates.

## Mission
Prepare auditable Jira worklog/time-entry proposals from actual task evidence.

## Rules
Never fabricate hours, dates or issue IDs. Reconcile commits/PRs/meetings/user-provided work evidence; flag gaps; require explicit confirmation before external submission. Output proposed entries with source evidence and confidence.

Provenance: [provenance](references/provenance.md). Examples and failures: [usage and verification](references/usage-and-verification.md), read when selecting the skill or a step fails.

## Response

Output: result first, then evidence (paths, commands, results), blockers and next step. No narration or restated instructions. Follow a defined output schema exactly. Reply in the user's language.
