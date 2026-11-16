---
name: social-media-operator
description: "Governed TikTok/Instagram operations via cookie or browser sessions. Use for social profile reads. Do NOT use for OAuth keys or developer accounts."
license: CC-BY-4.0
metadata:
  author: Tech Lead's Club / CodENavi
  version: 1.0.0
  owner_agent: codenavi-agent
---

# Social Media Operator Skill

Governance: CodENavi Full Workspace v2 (BRIEFING→DEBRIEF); skill of `codenavi-agent`; inherits `AGENTS.md`. Lenses are internal; no new agent identities; no bypass of secret or permission gates.

## Mission

Governed TikTok and Instagram operations via browser-based authentication sessions. Sessions persist for 30 days or until platform cookies expire, whichever comes first. No OAuth API keys required - uses manual browser login with cookie import.

## Workflow and module routing

Read contract, input and security modules before tools; follow the procedure in order. Load optional modes only when in scope.

- 1. [Purpose and contract](references/instructions/01-purpose-and-contract.md) — before acting.
- 2. [Mission](references/instructions/02-mission.md) — before acting.
- 3. [Capabilities](references/instructions/03-capabilities.md) — when in scope.
- 4. [Required MCPs](references/instructions/04-required-mcps.md) — when in scope.
- 5. [Risk Level](references/instructions/05-risk-level.md) — when in scope.
- 6. [Authentication Model](references/instructions/06-authentication-model.md) — when in scope.
- 7. [Session Lifecycle](references/instructions/07-session-lifecycle.md) — when in scope.
- 8. [Security Rules](references/instructions/08-security-rules.md) — before acting.
- 9. [Quality Gates](references/instructions/09-quality-gates.md) — before claiming completion.
- 10. [Platform-Specific Operations](references/instructions/10-platform-specific-operations.md) — when in scope.
- 11. [Usage Patterns](references/instructions/11-usage-patterns.md) — when choosing an output or matching a use case.
- 12. [Cookie Export Instructions](references/instructions/12-cookie-export-instructions.md) — when in scope.
- 13. [Error Handling](references/instructions/13-error-handling.md) — when an input, tool or check fails.
- 14. [Compliance](references/instructions/14-compliance.md) — when in scope.

## Boundaries and result

Use only tools actually available for the authorized task. Keep secrets in runtime providers. Missing evidence, inputs or permissions blocks the affected action. Return the domain output with source pointers, executed checks and remaining uncertainty; never claim an unexecuted check passed.

Provenance: [provenance](references/provenance.md). Examples and failures: [usage and verification](references/usage-and-verification.md), read when selecting the skill or a step fails.

Read [package-notes.md](references/package-notes.md) only when the domain workflow needs it; root governance and this entry take precedence.

## Response

Output: result first, then evidence (paths, commands, results), blockers and next step. No narration or restated instructions. Follow a defined output schema exactly. Reply in the user's language.
