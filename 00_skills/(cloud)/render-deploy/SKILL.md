---
name: render-deploy
description: Deploy applications to Render by analyzing codebases, generating render.yaml Blueprints, and providing Dashboard deeplinks. Use when the user wants to deploy, host, publish, or set up their application on Render's cloud platform. Do NOT use for deploying to Vercel, Netlify, or Cloudflare (use their respective skills).
license: CC-BY-4.0
metadata:
  author: github.com/openai/skills
  version: 1.0.0
  owner_agent: codenavi-agent
---

# Deploy to Render

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; inherit `AGENTS.md`.
Lifecycle: BRIEFING → RECON → PLAN → EXECUTE → VERIFY → DEBRIEF.
Source roles/workers are internal lenses. Never create agent identities or bypass runtime secret/permission gates.

## Mission

Deploy applications to Render by analyzing codebases, generating render.yaml Blueprints, and providing Dashboard deeplinks.

## Workflow and module routing

Read the contract/input/security modules before tools; then follow the applicable procedure in the original order. Load optional modes only when their scope applies.

- 1. [Purpose and contract](references/instructions/01-purpose-and-contract.md) — before acting on this contract.
- 2. [Prerequisites](references/instructions/02-prerequisites.md) — when this domain or mode is in scope.
- 3. [Security Requirements for API Keys and Secrets](references/instructions/03-security-requirements-for-api-keys-and-secrets.md) — before acting on this contract.
- 4. [When to Use This Skill](references/instructions/04-when-to-use-this-skill.md) — when this domain or mode is in scope.
- 5. [Happy Path (New Users)](references/instructions/05-happy-path-new-users.md) — when this domain or mode is in scope.
- 6. [Choose Your Source Path](references/instructions/06-choose-your-source-path.md) — when this domain or mode is in scope.
- 7. [Choose Your Deployment Method (Git Repo)](references/instructions/07-choose-your-deployment-method-git-repo.md) — when this domain or mode is in scope.
- 8. [Prerequisites Check](references/instructions/08-prerequisites-check.md) — when this domain or mode is in scope.
- 9. [Blueprint Workflow](references/instructions/09-blueprint-workflow.md) — at this step of execution.
- 10. [When to Use Direct Creation](references/instructions/10-when-to-use-direct-creation.md) — when this domain or mode is in scope.
- 11. [Prerequisites for Direct Creation](references/instructions/11-prerequisites-for-direct-creation.md) — when this domain or mode is in scope.
- 12. [Direct Creation Workflow](references/instructions/12-direct-creation-workflow.md) — at this step of execution.
- 13. [Troubleshooting](references/instructions/13-troubleshooting.md) — when an input, tool or check fails.

## Boundaries and result

Use only tools actually available for the authorized task. Keep secrets in runtime providers. Missing evidence, inputs or permissions blocks the affected action. Return the domain output with source pointers, executed checks and remaining uncertainty; never claim an unexecuted check passed.

## TLC source

For the catalog workflow and its local resources, read [TLC contract](references/tlc/UPSTREAM.md). Apply root governance and the local constraints above; upstream does not grant extra authority.

Provenance and source freshness: [provenance](references/provenance.md).

Example usage and failure handling: read [usage and verification](references/usage-and-verification.md) when selecting this skill or a required step fails.
