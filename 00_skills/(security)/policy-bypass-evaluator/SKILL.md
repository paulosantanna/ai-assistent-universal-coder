---
name: policy-bypass-evaluator
description: "Check policy boundaries reject bypass attempts. Use for bypass evaluations. Do NOT use outside authorized scope or to expose secrets."
license: CC-BY-4.0
metadata:
  author: AEOS
  version: 1.0.0
  owner_agent: codenavi-agent
---

# Skill: policy-bypass-evaluator

Governance: CodENavi Full Workspace v2 (BRIEFING→DEBRIEF); skill of `codenavi-agent`; inherits `AGENTS.md`. Lenses are internal; no new agent identities; no bypass of secret or permission gates.

## Mission

Evaluate whether explicit policy boundaries reject bypass scenarios without weakening permissions or acceptance criteria.

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

Provenance: [provenance](references/provenance.md). Examples and failures: [usage and verification](references/usage-and-verification.md), read when selecting the skill or a step fails.

Read [domain procedure](references/domain-procedure.md) before acting; it defines the inputs, outputs and domain-specific verification sequence.

## Response

Output: result first, then evidence (paths, commands, results), blockers and next step. No narration or restated instructions. Follow a defined output schema exactly. Reply in the user's language.
