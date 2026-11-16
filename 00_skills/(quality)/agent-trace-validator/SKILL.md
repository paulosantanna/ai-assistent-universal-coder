---
name: agent-trace-validator
description: "Validate agent trace completeness and integrity. Use for trace validation. Do NOT use as deployment approval or proof of unexecuted checks."
license: CC-BY-4.0
metadata:
  author: AEOS
  version: 1.0.0
  owner_agent: codenavi-agent
---

# Skill: agent-trace-validator

Governance: CodENavi Full Workspace v2 (BRIEFING→DEBRIEF); skill of `codenavi-agent`; inherits `AGENTS.md`. Lenses are internal; no new agent identities; no bypass of secret or permission gates.

## Mission

Validate agent trace completeness and integrity.

## Allowed Actions

- Read AEOS config and registries.
- Read evidence refs.
- Generate reports.
- Generate task/context/audit artifacts inside `.aeos`.

## Forbidden Actions

- Direct tool access.
- Scope expansion.
- Secret exposure.
- Self-approval.
- Direct mutation of project files.

## Required Evidence

- input refs
- generated artifact refs
- policy decision refs
- task graph refs when applicable
- agent trace refs when applicable

## Prompt Contract

- State the objective, target scope, assumptions and constraints before execution.
- Use only evidence-backed facts; mark uncertainty explicitly.
- Route tool access through approved command, MCP or Tool Router paths.
- Redact secrets, credentials, tokens and sensitive values.
- Return facts, assumptions, risks, recommendations, evidence_refs and blocking_conditions when applicable.
- Stop when required evidence, permissions, policy approval or input context is missing.

## Quality Gates

- Facts cite evidence.
- Assumptions are marked.
- Risks are classified.
- Outputs match schema.
- No raw secrets.

Provenance: [provenance](references/provenance.md). Examples and failures: [usage and verification](references/usage-and-verification.md), read when selecting the skill or a step fails.

## Response

Output: result first, then evidence (paths, commands, results), blockers and next step. No narration or restated instructions. Follow a defined output schema exactly. Reply in the user's language.
