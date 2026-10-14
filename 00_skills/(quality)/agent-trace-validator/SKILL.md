---
name: agent-trace-validator
description: Validate agent trace completeness and integrity. Use when the user requests agent trace validator or invokes agent-trace-validator. Do NOT use as deployment authorization or as evidence for checks that were not executed.
license: CC-BY-4.0
metadata:
  author: AEOS
  version: 1.0.0
  owner_agent: codenavi-agent
---

# Skill: agent-trace-validator

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; inherit `AGENTS.md`.
Lifecycle: BRIEFING → RECON → PLAN → EXECUTE → VERIFY → DEBRIEF.
Source roles/workers are internal lenses. Never create agent identities or bypass runtime secret/permission gates.

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

Provenance and source freshness: [provenance](references/provenance.md).

Example usage and failure handling: read [usage and verification](references/usage-and-verification.md) when selecting this skill or a required step fails.
