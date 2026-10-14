---
name: jira-time-entry-assistant
description: Prepare auditable Jira worklog/time-entry proposals from actual task evidence. Use when the user requests jira time entry assistant or invokes jira-time-entry-assistant. Do NOT use for unrelated languages, domains or production deployment.
license: CC-BY-4.0
metadata:
  author: AEOS
  version: 1.0.0
  owner_agent: codenavi-agent
---

# Jira Time Entry Assistant

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; inherit `AGENTS.md`.
Lifecycle: BRIEFING → RECON → PLAN → EXECUTE → VERIFY → DEBRIEF.
Source roles/workers are internal lenses. Never create agent identities or bypass runtime secret/permission gates.

Governance: CodENavi v1

## Mission
Prepare auditable Jira worklog/time-entry proposals from actual task evidence.

## Rules
Never fabricate hours, dates or issue IDs. Reconcile commits/PRs/meetings/user-provided work evidence; flag gaps; require explicit confirmation before external submission. Output proposed entries with source evidence and confidence.

Provenance and source freshness: [provenance](references/provenance.md).

Example usage and failure handling: read [usage and verification](references/usage-and-verification.md) when selecting this skill or a required step fails.
