---
name: confluence-assistant
description: Expert in Confluence operations using Atlassian MCP. Use when the user says "search Confluence", "create a Confluence page", "update a page", "find documentation in Confluence", "list spaces", or "add a comment to a page". Do NOT use for Jira issues, general web search, or local file creation.
license: CC-BY-4.0
metadata:
  author: Tech Leads Club
  version: 1.0.0
  owner_agent: codenavi-agent
---

# Confluence Assistant

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; inherit `AGENTS.md`.
Lifecycle: BRIEFING → RECON → PLAN → EXECUTE → VERIFY → DEBRIEF.
Source roles/workers are internal lenses. Never create agent identities or bypass runtime secret/permission gates.

Governance: CodENavi v1

## Mission
Create/update Confluence-ready engineering documentation from verified repository evidence.

## Rules
No invented pages, links, owners or decisions. Separate observed/inferred/unknown. Preserve technical nomenclature. Never publish secrets. Prefer pointers to code and ADRs over pasted source.

## Outputs
Page hierarchy, architecture/runbook/decision content, change summary and stale-page reconciliation plan. External writes require an authorized connector/tool and normal AEOS approval gates.

## TLC source

For the catalog workflow and its local resources, read [TLC contract](references/tlc/UPSTREAM.md). Apply root governance and the local constraints above; upstream does not grant extra authority.

Provenance and source freshness: [provenance](references/provenance.md).

Example usage and failure handling: read [usage and verification](references/usage-and-verification.md) when selecting this skill or a required step fails.
