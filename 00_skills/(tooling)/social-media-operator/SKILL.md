---
name: social-media-operator
description: Governed TikTok and Instagram operations via browser-based authentication sessions. Use when user asks for social media session management, TikTok/Instagram profile reading, or cookie-based authentication. Do NOT use for OAuth API keys or developer account management.
license: CC-BY-4.0
metadata:
  author: Tech Lead's Club / CodENavi
  version: 1.0.0
  owner_agent: codenavi-agent
---

# Social Media Operator Skill

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; inherit `AGENTS.md`.
Lifecycle: BRIEFING → RECON → PLAN → EXECUTE → VERIFY → DEBRIEF.
Source roles/workers are internal lenses. Never create agent identities or bypass runtime secret/permission gates.

## Mission

Governed TikTok and Instagram operations via browser-based authentication sessions. Sessions persist for 30 days or until platform cookies expire, whichever comes first. No OAuth API keys required - uses manual browser login with cookie import.

## Workflow and module routing

Read the contract/input/security modules before tools; then follow the applicable procedure in the original order. Load optional modes only when their scope applies.

- 1. [Purpose and contract](references/instructions/01-purpose-and-contract.md) — before acting on this contract.
- 2. [Mission](references/instructions/02-mission.md) — before acting on this contract.
- 3. [Capabilities](references/instructions/03-capabilities.md) — when this domain or mode is in scope.
- 4. [Required MCPs](references/instructions/04-required-mcps.md) — when this domain or mode is in scope.
- 5. [Risk Level](references/instructions/05-risk-level.md) — when this domain or mode is in scope.
- 6. [Authentication Model](references/instructions/06-authentication-model.md) — when this domain or mode is in scope.
- 7. [Session Lifecycle](references/instructions/07-session-lifecycle.md) — when this domain or mode is in scope.
- 8. [Security Rules](references/instructions/08-security-rules.md) — before acting on this contract.
- 9. [Quality Gates](references/instructions/09-quality-gates.md) — before claiming completion.
- 10. [Platform-Specific Operations](references/instructions/10-platform-specific-operations.md) — when this domain or mode is in scope.
- 11. [Usage Patterns](references/instructions/11-usage-patterns.md) — when choosing an output or matching a use case.
- 12. [Cookie Export Instructions](references/instructions/12-cookie-export-instructions.md) — when this domain or mode is in scope.
- 13. [Error Handling](references/instructions/13-error-handling.md) — when an input, tool or check fails.
- 14. [Compliance](references/instructions/14-compliance.md) — when this domain or mode is in scope.

## Boundaries and result

Use only tools actually available for the authorized task. Keep secrets in runtime providers. Missing evidence, inputs or permissions blocks the affected action. Return the domain output with source pointers, executed checks and remaining uncertainty; never claim an unexecuted check passed.

Provenance and source freshness: [provenance](references/provenance.md).

Example usage and failure handling: read [usage and verification](references/usage-and-verification.md) when selecting this skill or a required step fails.
Read [package-notes.md](references/package-notes.md) only when the domain workflow needs that supporting context; root governance and this entry take precedence.
