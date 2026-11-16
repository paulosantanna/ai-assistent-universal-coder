---
name: render-deploy
description: "Deploy apps to Render: analyze code, generate render.yaml Blueprints. Use for Render deploys. Do NOT use for Vercel, Netlify or Cloudflare."
license: CC-BY-4.0
metadata:
  author: github.com/openai/skills
  version: 1.0.0
  owner_agent: codenavi-agent
---

# Deploy to Render

Governance: CodENavi Full Workspace v2 (BRIEFING→DEBRIEF); skill of `codenavi-agent`; inherits `AGENTS.md`. Lenses are internal; no new agent identities; no bypass of secret or permission gates.

## Mission

Deploy applications to Render by analyzing codebases, generating render.yaml Blueprints, and providing Dashboard deeplinks.

## Workflow and module routing

Read contract, input and security modules before tools; follow the procedure in order. Load optional modes only when in scope.

- 1. [Purpose and contract](references/instructions/01-purpose-and-contract.md) — before acting.
- 2. [Prerequisites](references/instructions/02-prerequisites.md) — when in scope.
- 3. [Security Requirements for API Keys and Secrets](references/instructions/03-security-requirements-for-api-keys-and-secrets.md) — before acting.
- 4. [When to Use This Skill](references/instructions/04-when-to-use-this-skill.md) — when in scope.
- 5. [Happy Path (New Users)](references/instructions/05-happy-path-new-users.md) — when in scope.
- 6. [Choose Your Source Path](references/instructions/06-choose-your-source-path.md) — when in scope.
- 7. [Choose Your Deployment Method (Git Repo)](references/instructions/07-choose-your-deployment-method-git-repo.md) — when in scope.
- 8. [Prerequisites Check](references/instructions/08-prerequisites-check.md) — when in scope.
- 9. [Blueprint Workflow](references/instructions/09-blueprint-workflow.md) — at this step.
- 10. [When to Use Direct Creation](references/instructions/10-when-to-use-direct-creation.md) — when in scope.
- 11. [Prerequisites for Direct Creation](references/instructions/11-prerequisites-for-direct-creation.md) — when in scope.
- 12. [Direct Creation Workflow](references/instructions/12-direct-creation-workflow.md) — at this step.
- 13. [Troubleshooting](references/instructions/13-troubleshooting.md) — when an input, tool or check fails.

## Boundaries and result

Use only tools actually available for the authorized task. Keep secrets in runtime providers. Missing evidence, inputs or permissions blocks the affected action. Return the domain output with source pointers, executed checks and remaining uncertainty; never claim an unexecuted check passed.

## TLC source

TLC source: [TLC contract](references/tlc/UPSTREAM.md). Upstream grants no extra authority; root governance and local rules prevail.

Provenance: [provenance](references/provenance.md). Examples and failures: [usage and verification](references/usage-and-verification.md), read when selecting the skill or a step fails.

## Response

Output: result first, then evidence (paths, commands, results), blockers and next step. No narration or restated instructions. Follow a defined output schema exactly. Reply in the user's language.
