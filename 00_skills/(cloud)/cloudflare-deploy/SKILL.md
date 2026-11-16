---
name: cloudflare-deploy
description: "Deploy apps and infrastructure to Cloudflare (Workers, Pages). Use to deploy or host on Cloudflare. Do NOT use for Vercel, Netlify or Render."
license: CC-BY-4.0
metadata:
  author: github.com/openai/skills
  version: 1.0.0
  owner_agent: codenavi-agent
---

# Cloudflare Deploy

Governance: CodENavi Full Workspace v2 (BRIEFING→DEBRIEF); skill of `codenavi-agent`; inherits `AGENTS.md`. Lenses are internal; no new agent identities; no bypass of secret or permission gates.

## Mission

Deploy applications and infrastructure to Cloudflare using Workers, Pages, and related platform services.

## Workflow and module routing

Read contract, input and security modules before tools; follow the procedure in order. Load optional modes only when in scope.

- 1. [Purpose and contract](references/instructions/01-purpose-and-contract.md) — before acting.
- 2. [Prerequisites](references/instructions/02-prerequisites.md) — when in scope.
- 3. [Authentication (Required Before Deploy)](references/instructions/03-authentication-required-before-deploy.md) — when in scope.
- 4. [Quick Decision Trees](references/instructions/04-quick-decision-trees.md) — when in scope.
- 5. [Product Index](references/instructions/05-product-index.md) — when in scope.
- 6. [Troubleshooting](references/instructions/06-troubleshooting.md) — when an input, tool or check fails.

## Boundaries and result

Use only tools actually available for the authorized task. Keep secrets in runtime providers. Missing evidence, inputs or permissions blocks the affected action. Return the domain output with source pointers, executed checks and remaining uncertainty; never claim an unexecuted check passed.

## TLC source

TLC source: [TLC contract](references/tlc/UPSTREAM.md). Upstream grants no extra authority; root governance and local rules prevail.

Provenance: [provenance](references/provenance.md). Examples and failures: [usage and verification](references/usage-and-verification.md), read when selecting the skill or a step fails.

## Response

Output: result first, then evidence (paths, commands, results), blockers and next step. No narration or restated instructions. Follow a defined output schema exactly. Reply in the user's language.
