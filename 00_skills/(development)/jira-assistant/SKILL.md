---
name: jira-assistant
description: "Manage Jira issues via Atlassian MCP: search, create, update, transition. Use for Jira tickets. Do NOT use for Confluence (confluence-assistant)."
license: CC-BY-4.0
metadata:
  author: Tech Leads Club
  version: 1.0.0
  owner_agent: codenavi-agent
---

# Jira Assistant

Governance: CodENavi Full Workspace v2 (BRIEFING→DEBRIEF); skill of `codenavi-agent`; inherits `AGENTS.md`. Lenses are internal; no new agent identities; no bypass of secret or permission gates.

## Mission
Turn engineering evidence into actionable Jira work items and reconcile implementation with acceptance criteria.

## Contract
Create concise title, problem/evidence, scope/non-goals, acceptance criteria, dependencies, risk, verification and definition of done. Do not invent issue IDs/status/assignees. Writes require an authorized Jira integration.

## TLC source

TLC source: [TLC contract](references/tlc/UPSTREAM.md). Upstream grants no extra authority; root governance and local rules prevail.

Provenance: [provenance](references/provenance.md). Examples and failures: [usage and verification](references/usage-and-verification.md), read when selecting the skill or a step fails.

## Response

Output: result first, then evidence (paths, commands, results), blockers and next step. No narration or restated instructions. Follow a defined output schema exactly. Reply in the user's language.
