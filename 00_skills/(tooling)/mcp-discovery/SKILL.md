---
name: mcp-discovery
description: Discover and validate MCP tools and capabilities against AEOS policies. Use when the user requests mcp discovery or invokes mcp-discovery. Do NOT use for unrelated tools or unapproved remote writes.
license: CC-BY-4.0
metadata:
  author: AEOS
  version: 1.0.0
  owner_agent: codenavi-agent
---

# Skill: mcp-discovery

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; inherit `AGENTS.md`.
Lifecycle: BRIEFING → RECON → PLAN → EXECUTE → VERIFY → DEBRIEF.
Source roles/workers are internal lenses. Never create agent identities or bypass runtime secret/permission gates.

## Mission

Discover and validate MCP tools and capabilities against AEOS policies.

## Output

- tools discovered
- capabilities discovered
- allowlist comparison
- blocked tools
- risk classification

## Blocking Conditions

- unknown high-risk tool
- forbidden capability
- critical MCP enabled
- missing evidence

## Prompt Contract

- State the objective, target scope, assumptions and constraints before execution.
- Use only evidence-backed facts; mark uncertainty explicitly.
- Route tool access through approved command, MCP or Tool Router paths.
- Redact secrets, credentials, tokens and sensitive values.
- Return facts, assumptions, risks, recommendations, evidence_refs and blocking_conditions when applicable.
- Stop when required evidence, permissions, policy approval or input context is missing.

Provenance and source freshness: [provenance](references/provenance.md).

Example usage and failure handling: read [usage and verification](references/usage-and-verification.md) when selecting this skill or a required step fails.
