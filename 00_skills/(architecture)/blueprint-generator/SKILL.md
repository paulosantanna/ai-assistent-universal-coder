---
name: blueprint-generator
description: Generate an evidence-based project blueprint covering boundaries, components, data, deployment constraints and verification gates. Use when the user requests blueprint generator or invokes blueprint-generator. Do NOT use for an unrelated implementation change or deployment execution.
license: CC-BY-4.0
metadata:
  author: AEOS
  version: 1.0.0
  owner_agent: codenavi-agent
---

# Skill: blueprint-generator

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; inherit `AGENTS.md`.
Lifecycle: BRIEFING → RECON → PLAN → EXECUTE → VERIFY → DEBRIEF.
Source roles/workers are internal lenses. Never create agent identities or bypass runtime secret/permission gates.

## Mission

Generate an evidence-based project blueprint covering boundaries, components, data, deployment constraints and verification gates.

## Allowed Actions

- Read authorized configuration files through Tool Router.
- Read evidence refs.
- Generate sandbox artifacts.
- Generate reports.
- Generate evaluation outputs.
- Register evidence.

## Forbidden Actions

- Direct tool access.
- Direct filesystem mutation.
- Secret value exposure.
- Approval bypass.
- Unrestricted shell.
- Unsupported factual claims.
- Mutating active registries without staging and approval.

## Required Evidence

- input references
- files inspected
- policy decisions
- permission decisions
- generated artifacts
- risk report
- Judge input

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
- No raw secrets.
- No direct tool bypass.
- Outputs are schema-valid.

Provenance and source freshness: [provenance](references/provenance.md).

Example usage and failure handling: read [usage and verification](references/usage-and-verification.md) when selecting this skill or a required step fails.

Read [domain procedure](references/domain-procedure.md) before acting; it defines the inputs, outputs and domain-specific verification sequence.
