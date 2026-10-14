---
name: jira-confluence-assistant
description: Read, analyze and prepare governed Jira/Confluence work while preserving traceability between requirement, code, evidence and documentation. Use when the user requests jira confluence assistant or invokes jira-confluence-assistant. Do NOT use for unrelated languages, domains or production deployment.
license: CC-BY-4.0
metadata:
  author: AEOS
  version: 1.0.0
  owner_agent: codenavi-agent
---

# Skill: jira-confluence-assistant

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; inherit `AGENTS.md`.
Lifecycle: BRIEFING → RECON → PLAN → EXECUTE → VERIFY → DEBRIEF.
Source roles/workers are internal lenses. Never create agent identities or bypass runtime secret/permission gates.

Governance: CodENavi v1

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

Provenance and source freshness: [provenance](references/provenance.md).

Example usage and failure handling: read [usage and verification](references/usage-and-verification.md) when selecting this skill or a required step fails.
