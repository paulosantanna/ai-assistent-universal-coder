---
name: netlify-deploy
description: Deploy web projects to Netlify using the Netlify CLI (`npx netlify`). Use when the user asks to deploy, host, publish, or link a site/repo on Netlify, including preview and production deploys. Do NOT use for deploying to Vercel, Cloudflare, or Render (use their respective skills).
license: CC-BY-4.0
metadata:
  author: github.com/openai/skills
  version: 1.0.0
  owner_agent: codenavi-agent
---

# Netlify Deployment Skill

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; inherit `AGENTS.md`.
Lifecycle: BRIEFING → RECON → PLAN → EXECUTE → VERIFY → DEBRIEF.
Source roles/workers are internal lenses. Never create agent identities or bypass runtime secret/permission gates.

## Mission

Deploy web projects to Netlify using the Netlify CLI (`npx netlify`).

## Workflow and module routing

Read the contract/input/security modules before tools; then follow the applicable procedure in the original order. Load optional modes only when their scope applies.

- 1. [Purpose and contract](references/instructions/01-purpose-and-contract.md) — before acting on this contract.
- 2. [Overview](references/instructions/02-overview.md) — when this domain or mode is in scope.
- 3. [Prerequisites](references/instructions/03-prerequisites.md) — when this domain or mode is in scope.
- 4. [Authentication Pattern](references/instructions/04-authentication-pattern.md) — when choosing an output or matching a use case.
- 5. [Workflow](references/instructions/05-workflow.md) — at this step of execution.
- 6. [Handling netlify.toml](references/instructions/06-handling-netlify-toml.md) — when this domain or mode is in scope.
- 7. [Example Full Workflow](references/instructions/07-example-full-workflow.md) — when choosing an output or matching a use case.
- 8. [Error Handling](references/instructions/08-error-handling.md) — when an input, tool or check fails.
- 9. [Troubleshooting](references/instructions/09-troubleshooting.md) — when an input, tool or check fails.
- 10. [Environment Variables](references/instructions/10-environment-variables.md) — when this domain or mode is in scope.
- 11. [Tips](references/instructions/11-tips.md) — when this domain or mode is in scope.
- 12. [Reference](references/instructions/12-reference.md) — when this domain or mode is in scope.
- 13. [Bundled References (Load As Needed)](references/instructions/13-bundled-references-load-as-needed.md) — when this domain or mode is in scope.

## Boundaries and result

Use only tools actually available for the authorized task. Keep secrets in runtime providers. Missing evidence, inputs or permissions blocks the affected action. Return the domain output with source pointers, executed checks and remaining uncertainty; never claim an unexecuted check passed.

## TLC source

For the catalog workflow and its local resources, read [TLC contract](references/tlc/UPSTREAM.md). Apply root governance and the local constraints above; upstream does not grant extra authority.

Provenance and source freshness: [provenance](references/provenance.md).
