---
name: security-audit
description: Detect security risks and possible secrets without exposing values. Use when the user requests security audit or invokes security-audit. Do NOT use outside authorized defensive scope or to expose secret values.
license: CC-BY-4.0
metadata:
  author: AEOS
  version: 1.0.0
  owner_agent: codenavi-agent
---

# Skill: security-audit

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; inherit `AGENTS.md`.
Lifecycle: BRIEFING → RECON → PLAN → EXECUTE → VERIFY → DEBRIEF.
Source roles/workers are internal lenses. Never create agent identities or bypass runtime secret/permission gates.

## Mission

Detect security risks and possible secrets without exposing values.

## Allowed Actions

- Read authorized files through Tool Router.
- Generate reports in `.aeos/reports`.
- Generate evidence in `.aeos/evidence`.
- Generate sandbox artifacts when permitted.
- Never bypass permissions.

## Forbidden Actions

- Direct filesystem access.
- Direct Git mutation.
- Secret value exposure.
- Destructive shell.
- Unapproved writes outside `.aeos`.
- Unsupported factual claims.
- Silent failure.

## Required Evidence

- files inspected
- tool calls
- permission decisions
- generated artifacts
- risk classification
- Judge input when applicable

## Prompt Contract

- State the objective, target scope, assumptions and constraints before execution.
- Use only evidence-backed facts; mark uncertainty explicitly.
- Route tool access through approved command, MCP or Tool Router paths.
- Redact secrets, credentials, tokens and sensitive values.
- Return facts, assumptions, risks, recommendations, evidence_refs and blocking_conditions when applicable.
- Stop when required evidence, permissions, policy approval or input context is missing.

## Quality Gates

- Facts cite evidence.
- Assumptions are explicitly marked.
- Risks are classified.
- Outputs follow schema.
- No secrets are printed.
- Required artifacts are hashed.

Provenance and source freshness: [provenance](references/provenance.md).

Example usage and failure handling: read [usage and verification](references/usage-and-verification.md) when selecting this skill or a required step fails.
Read [package-notes.md](references/package-notes.md) only when the domain workflow needs that supporting context; root governance and this entry take precedence.
