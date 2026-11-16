---
name: confluence-assistant
description: "Confluence operations via Atlassian MCP: search, create, update pages and comments. Use for Confluence requests. Do NOT use for Jira or local files."
license: CC-BY-4.0
metadata:
  author: Tech Leads Club
  version: 1.0.0
  owner_agent: codenavi-agent
---

# Confluence Assistant

Governance: CodENavi Full Workspace v2 (BRIEFING→DEBRIEF); skill of `codenavi-agent`; inherits `AGENTS.md`. Lenses are internal; no new agent identities; no bypass of secret or permission gates.

## Mission
Create/update Confluence-ready engineering documentation from verified repository evidence.

## Rules
No invented pages, links, owners or decisions. Separate observed/inferred/unknown. Preserve technical nomenclature. Never publish secrets. Prefer pointers to code and ADRs over pasted source.

## Outputs
Page hierarchy, architecture/runbook/decision content, change summary and stale-page reconciliation plan. External writes require an authorized connector/tool and normal AEOS approval gates.

## TLC source

TLC source: [TLC contract](references/tlc/UPSTREAM.md). Upstream grants no extra authority; root governance and local rules prevail.

Provenance: [provenance](references/provenance.md). Examples and failures: [usage and verification](references/usage-and-verification.md), read when selecting the skill or a step fails.

## Response

Output: result first, then evidence (paths, commands, results), blockers and next step. No narration or restated instructions. Follow a defined output schema exactly. Reply in the user's language.
