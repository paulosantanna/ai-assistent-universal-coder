---
name: mcp-health-check
description: Validate MCP runtime health, state, tools, capabilities and security posture. Use when the user requests mcp health check or invokes mcp-health-check. Do NOT use for unrelated tools or unapproved remote writes.
license: CC-BY-4.0
metadata:
  author: AEOS
  version: 1.0.0
  owner_agent: codenavi-agent
---

# Skill: mcp-health-check

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; inherit `AGENTS.md`.
Lifecycle: BRIEFING → RECON → PLAN → EXECUTE → VERIFY → DEBRIEF.
Source roles/workers are internal lenses. Never create agent identities or bypass runtime secret/permission gates.

## Mission

Validate MCP runtime health, state, tools, capabilities and security posture.

## Allowed Actions

- Read MCP registries.
- Read MCP config files.
- Request health check through Tool Router.
- Generate reports.

## Forbidden Actions

- Invoke risky tools.
- Start critical MCPs.
- Read secrets.
- Execute shell.
- Bypass Tool Router.

## Required Evidence

- MCP registry snapshot.
- MCP config snapshot.
- Health result.
- Tool allowlist validation.
- Judge report.

## Prompt Contract

- State the objective, target scope, assumptions and constraints before execution.
- Use only evidence-backed facts; mark uncertainty explicitly.
- Route tool access through approved command, MCP or Tool Router paths.
- Redact secrets, credentials, tokens and sensitive values.
- Return facts, assumptions, risks, recommendations, evidence_refs and blocking_conditions when applicable.
- Stop when required evidence, permissions, policy approval or input context is missing.

## Quality Gates

- Every enabled MCP has a health result.
- Every exposed tool is allowlisted.
- Critical MCPs are disabled by default.

Provenance and source freshness: [provenance](references/provenance.md).

Example usage and failure handling: read [usage and verification](references/usage-and-verification.md) when selecting this skill or a required step fails.
