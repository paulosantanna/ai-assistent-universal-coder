---
name: jira-assistant
description: Manage Jira issues via Atlassian MCP — search, create, update, transition status, and handle sprint tasks. Auto-detects workspace configuration. Use when user says "create a Jira ticket", "update my sprint", "check Jira status", "transition this issue", "search Jira", or "move ticket to done". Do NOT use for Confluence pages (use confluence-assistant).
license: CC-BY-4.0
metadata:
  author: Tech Leads Club
  version: 1.0.0
  owner_agent: codenavi-agent
---

# Jira Assistant

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; inherit `AGENTS.md`.
Lifecycle: BRIEFING → RECON → PLAN → EXECUTE → VERIFY → DEBRIEF.
Source roles/workers are internal lenses. Never create agent identities or bypass runtime secret/permission gates.

Governance: CodENavi v1

## Mission
Turn engineering evidence into actionable Jira work items and reconcile implementation with acceptance criteria.

## Contract
Create concise title, problem/evidence, scope/non-goals, acceptance criteria, dependencies, risk, verification and definition of done. Do not invent issue IDs/status/assignees. Writes require an authorized Jira integration.

## TLC source

For the catalog workflow and its local resources, read [TLC contract](references/tlc/UPSTREAM.md). Apply root governance and the local constraints above; upstream does not grant extra authority.

Provenance and source freshness: [provenance](references/provenance.md).

Example usage and failure handling: read [usage and verification](references/usage-and-verification.md) when selecting this skill or a required step fails.
