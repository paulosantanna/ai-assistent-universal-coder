---
name: approval-requester
description: "Determine approvals, create requests, track status. Use when asked to request approval. Do NOT use outside authorized scope or to expose secrets."
license: CC-BY-4.0
metadata:
  author: AEOS
  version: 1.0.0
  owner_agent: codenavi-agent
---

# Approval Requester Skill

Governance: CodENavi Full Workspace v2 (BRIEFING→DEBRIEF); skill of `codenavi-agent`; inherits `AGENTS.md`. Lenses are internal; no new agent identities; no bypass of secret or permission gates.

**ID:** approval-requester
**Version:** 1.0.0
**Owner Agent:** codenavi-agent
**Risk Level:** low

## Mission
Determine what approvals are needed for a proposed change, create approval requests, and track approval status.

## Scope
- Assess change scope and risk
- Determine required approvals (action + scope)
- Create approval requests in .aeos/approvals/
- Check approval status

## Allowed Actions
- `filesystem.read` — read patch and analysis files
- `filesystem.write_aeos` — write to .aeos/approvals/
- `generate_evidence` — register approval requests

## Forbidden Actions
- Approve or deny on behalf of human
- Create global unrestricted approvals (scope="**")
- Auto-approve without human review

## Required Capabilities
- READ_REPOSITORY
- MANAGE_APPROVALS
- GENERATE_REPORT

## Required Evidence
- Approval requests created (paths with SHA-256)
- Approval status report

## Prompt Contract

- State the objective, target scope, assumptions and constraints before execution.
- Use only evidence-backed facts; mark uncertainty explicitly.
- Route tool access through approved command, MCP or Tool Router paths.
- Redact secrets, credentials, tokens and sensitive values.
- Return facts, assumptions, risks, recommendations, evidence_refs and blocking_conditions when applicable.
- Stop when required evidence, permissions, policy approval or input context is missing.

## Quality Gates
- No approval with unrestricted scope (**)
- Each approval must have: execution_id, action, scope, expiration
- Approvals beyond 90 days must be flagged

## Output Schema
```json
{
  "approval_id": "ap-a1b2c3d4",
  "execution_id": "ex-20260101T120000-abc123",
  "action": "patch.propose",
  "scope": ".aeos/patches/**",
  "status": "pending",
  "expiration": "2026-02-01T00:00:00+00:00"
}
```

## Blocking Conditions
- Attempt to create approval with scope "**" or "all"
- Approval executed without human decision
- Approval for an action not in granular list

Provenance: [provenance](references/provenance.md). Examples and failures: [usage and verification](references/usage-and-verification.md), read when selecting the skill or a step fails.

## Response

Output: result first, then evidence (paths, commands, results), blockers and next step. No narration or restated instructions. Follow a defined output schema exactly. Reply in the user's language.
