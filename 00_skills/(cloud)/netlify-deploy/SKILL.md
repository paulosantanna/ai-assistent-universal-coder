---
name: netlify-deploy
description: "Deploy web projects to Netlify via the CLI, including previews. Use for Netlify deploys or links. Do NOT use for Vercel, Cloudflare or Render."
license: CC-BY-4.0
metadata:
  author: github.com/openai/skills
  version: 1.0.0
  owner_agent: codenavi-agent
---

# Netlify Deployment Skill

Governance: CodENavi Full Workspace v2 (BRIEFING→DEBRIEF); skill of `codenavi-agent`; inherits `AGENTS.md`. Lenses are internal; no new agent identities; no bypass of secret or permission gates.

## Mission

Deploy web projects to Netlify using the Netlify CLI (`npx netlify`).

## Workflow and module routing

Read contract, input and security modules before tools; follow the procedure in order. Load optional modes only when in scope.

- 1. [Purpose and contract](references/instructions/01-purpose-and-contract.md) — before acting.
- 2. [Overview](references/instructions/02-overview.md) — when in scope.
- 3. [Prerequisites](references/instructions/03-prerequisites.md) — when in scope.
- 4. [Authentication Pattern](references/instructions/04-authentication-pattern.md) — when choosing an output or matching a use case.
- 5. [Workflow](references/instructions/05-workflow.md) — at this step.
- 6. [Handling netlify.toml](references/instructions/06-handling-netlify-toml.md) — when in scope.
- 7. [Example Full Workflow](references/instructions/07-example-full-workflow.md) — when choosing an output or matching a use case.
- 8. [Error Handling](references/instructions/08-error-handling.md) — when an input, tool or check fails.
- 9. [Troubleshooting](references/instructions/09-troubleshooting.md) — when an input, tool or check fails.
- 10. [Environment Variables](references/instructions/10-environment-variables.md) — when in scope.
- 11. [Tips](references/instructions/11-tips.md) — when in scope.
- 12. [Reference](references/instructions/12-reference.md) — when in scope.
- 13. [Bundled References (Load As Needed)](references/instructions/13-bundled-references-load-as-needed.md) — when in scope.

## Boundaries and result

Use only tools actually available for the authorized task. Keep secrets in runtime providers. Missing evidence, inputs or permissions blocks the affected action. Return the domain output with source pointers, executed checks and remaining uncertainty; never claim an unexecuted check passed.

## TLC source

TLC source: [TLC contract](references/tlc/UPSTREAM.md). Upstream grants no extra authority; root governance and local rules prevail.

Provenance: [provenance](references/provenance.md).

## Response

Output: result first, then evidence (paths, commands, results), blockers and next step. No narration or restated instructions. Follow a defined output schema exactly. Reply in the user's language.
