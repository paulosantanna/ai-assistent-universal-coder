---
name: tool-router-audit
description: Audit whether AEOS code and playbooks enforce Tool Router for every external action. Use when the user requests tool router audit or invokes tool-router-audit. Do NOT use for unrelated tools or unapproved remote writes.
license: CC-BY-4.0
metadata:
  author: AEOS
  version: 1.0.0
  owner_agent: codenavi-agent
---

# Skill: tool-router-audit

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; inherit `AGENTS.md`.
Lifecycle: BRIEFING → RECON → PLAN → EXECUTE → VERIFY → DEBRIEF.
Source roles/workers are internal lenses. Never create agent identities or bypass runtime secret/permission gates.

## Mission

Audit whether AEOS code and playbooks enforce Tool Router for every external action.

## Checks

- direct filesystem access
- direct Git mutation
- direct subprocess calls
- direct HTTP calls to tools
- direct secret access
- missing tool-call evidence

## Prompt Contract

- State the objective, target scope, assumptions and constraints before execution.
- Use only evidence-backed facts; mark uncertainty explicitly.
- Route tool access through approved command, MCP or Tool Router paths.
- Redact secrets, credentials, tokens and sensitive values.
- Return facts, assumptions, risks, recommendations, evidence_refs and blocking_conditions when applicable.
- Stop when required evidence, permissions, policy approval or input context is missing.

## Quality Gates

- No direct tool bypass.
- Every action maps to a Tool Router call.
- Every action creates permission and policy decisions.

Provenance and source freshness: [provenance](references/provenance.md).

Example usage and failure handling: read [usage and verification](references/usage-and-verification.md) when selecting this skill or a required step fails.
