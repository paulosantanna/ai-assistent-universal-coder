---
name: github-operations
description: "Governed Git and GitHub operations: branches, PRs, workflows. Use for Git or GitHub actions. Do NOT use for unapproved remote writes."
license: CC-BY-4.0
metadata:
  author: AEOS
  version: 1.0.0
  owner_agent: codenavi-agent
---

# GitHub Operations

Governance: CodENavi Full Workspace v2 (BRIEFING→DEBRIEF); skill of `codenavi-agent`; inherits `AGENTS.md`. Lenses are internal; no new agent identities; no bypass of secret or permission gates.

## Mission

Provide one governed surface for local Git and remote GitHub operations used by AEOS skills/playbooks, including branches, commits, remotes, pull requests, workflow inspection/rerun, releases, bundle handoff and merge preparation.

## Workflow and module routing

Read contract, input and security modules before tools; follow the procedure in order. Load optional modes only when in scope.

- 1. [Purpose and contract](references/instructions/01-purpose-and-contract.md) — before acting.
- 2. [Identity](references/instructions/02-identity.md) — before acting.
- 3. [Mission](references/instructions/03-mission.md) — before acting.
- 4. [Authentication](references/instructions/04-authentication.md) — when in scope.
- 5. [Supported operation classes](references/instructions/05-supported-operation-classes.md) — when in scope.
- 6. [Immutable denials](references/instructions/06-immutable-denials.md) — when in scope.
- 7. [Pull request Why contract](references/instructions/07-pull-request-why-contract.md) — before acting.
- 8. [Operation planning](references/instructions/08-operation-planning.md) — at this step.
- 9. [Command safety](references/instructions/09-command-safety.md) — when in scope.
- 10. [Integration](references/instructions/10-integration.md) — when in scope.
- 11. [Completion](references/instructions/11-completion.md) — before claiming completion.

## Boundaries and result

Use only tools actually available for the authorized task. Keep secrets in runtime providers. Missing evidence, inputs or permissions blocks the affected action. Return the domain output with source pointers, executed checks and remaining uncertainty; never claim an unexecuted check passed.

Provenance: [provenance](references/provenance.md). Examples and failures: [usage and verification](references/usage-and-verification.md), read when selecting the skill or a step fails.

## Response

Output: result first, then evidence (paths, commands, results), blockers and next step. No narration or restated instructions. Follow a defined output schema exactly. Reply in the user's language.
