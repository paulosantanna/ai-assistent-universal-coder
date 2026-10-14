---
name: v1-readiness-auditor
description: Validate AEOS against v1.0 release gates and generate blocking report. Use when the user requests v1 readiness auditor or invokes v1-readiness-auditor. Do NOT use as deployment authorization or as evidence for checks that were not executed.
license: CC-BY-4.0
metadata:
  author: AEOS
  version: 1.0.0
  owner_agent: codenavi-agent
---

# Skill: v1-readiness-auditor

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; inherit `AGENTS.md`.
Lifecycle: BRIEFING → RECON → PLAN → EXECUTE → VERIFY → DEBRIEF.
Source roles/workers are internal lenses. Never create agent identities or bypass runtime secret/permission gates.

## Mission

Validate AEOS against v1.0 release gates and generate blocking report.

## Allowed Actions

- Read AEOS configs through Tool Router.
- Read registries through Tool Router.
- Read evidence and reports.
- Generate reports under `.aeos/reports`.
- Generate evidence under `.aeos/evidence`.

## Forbidden Actions

- Direct filesystem access.
- Direct MCP invocation.
- Secret exposure.
- Approval bypass.
- Policy bypass.
- Unapproved mutation.
- Unsupported factual claims.

## Required Evidence

- config refs
- registry refs
- tool call refs
- policy decision refs
- permission decision refs
- generated report refs

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
- Blocking conditions are explicit.
- No raw secrets.
- Judge can validate outputs deterministically.

Provenance and source freshness: [provenance](references/provenance.md).

Example usage and failure handling: read [usage and verification](references/usage-and-verification.md) when selecting this skill or a required step fails.
