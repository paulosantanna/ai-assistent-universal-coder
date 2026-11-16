---
name: code-analyzer
description: "Analyze change impact and risks in code. Use for proposed changes. Do NOT use to mutate production or invent architecture without source evidence."
license: CC-BY-4.0
metadata:
  author: AEOS
  version: 1.0.0
  owner_agent: codenavi-agent
---

# Skill: code-analyzer

Governance: CodENavi Full Workspace v2 (BRIEFING→DEBRIEF); skill of `codenavi-agent`; inherits `AGENTS.md`. Lenses are internal; no new agent identities; no bypass of secret or permission gates.

## Mission

Analyze code structure, impact, and risks for proposed changes.

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

Provenance: [provenance](references/provenance.md). Examples and failures: [usage and verification](references/usage-and-verification.md), read when selecting the skill or a step fails.

## Response

Output: result first, then evidence (paths, commands, results), blockers and next step. No narration or restated instructions. Follow a defined output schema exactly. Reply in the user's language.
