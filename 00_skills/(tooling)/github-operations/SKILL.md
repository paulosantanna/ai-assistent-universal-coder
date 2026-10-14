---
name: github-operations
description: Governed Git and GitHub operations with runtime-only authentication, immutable safety denials, branch/PR/workflow management and Work Bundle integration. Use when the user requests github operations or invokes github-operations. Do NOT use for unrelated tools or unapproved remote writes.
license: CC-BY-4.0
metadata:
  author: AEOS
  version: 1.0.0
  owner_agent: codenavi-agent
---

# GitHub Operations

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; inherit `AGENTS.md`.
Lifecycle: BRIEFING → RECON → PLAN → EXECUTE → VERIFY → DEBRIEF.
Source roles/workers are internal lenses. Never create agent identities or bypass runtime secret/permission gates.

## Mission

Provide one governed surface for local Git and remote GitHub operations used by AEOS skills/playbooks, including branches, commits, remotes, pull requests, workflow inspection/rerun, releases, bundle handoff and merge preparation.

## Workflow and module routing

Read the contract/input/security modules before tools; then follow the applicable procedure in the original order. Load optional modes only when their scope applies.

- 1. [Purpose and contract](references/instructions/01-purpose-and-contract.md) — before acting on this contract.
- 2. [Identity](references/instructions/02-identity.md) — before acting on this contract.
- 3. [Mission](references/instructions/03-mission.md) — before acting on this contract.
- 4. [Authentication](references/instructions/04-authentication.md) — when this domain or mode is in scope.
- 5. [Supported operation classes](references/instructions/05-supported-operation-classes.md) — when this domain or mode is in scope.
- 6. [Immutable denials](references/instructions/06-immutable-denials.md) — when this domain or mode is in scope.
- 7. [Pull request Why contract](references/instructions/07-pull-request-why-contract.md) — before acting on this contract.
- 8. [Operation planning](references/instructions/08-operation-planning.md) — at this step of execution.
- 9. [Command safety](references/instructions/09-command-safety.md) — when this domain or mode is in scope.
- 10. [Integration](references/instructions/10-integration.md) — when this domain or mode is in scope.
- 11. [Completion](references/instructions/11-completion.md) — before claiming completion.

## Boundaries and result

Use only tools actually available for the authorized task. Keep secrets in runtime providers. Missing evidence, inputs or permissions blocks the affected action. Return the domain output with source pointers, executed checks and remaining uncertainty; never claim an unexecuted check passed.

Provenance and source freshness: [provenance](references/provenance.md).

Example usage and failure handling: read [usage and verification](references/usage-and-verification.md) when selecting this skill or a required step fails.
