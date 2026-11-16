---
name: nx-workspace
description: "Configure and optimize Nx monorepos: boundaries, affected analysis, caching, CI. Use for Nx workspace setup. Do NOT use to run tasks or generate code."
license: CC-BY-4.0
metadata:
  author: Tech Leads Club
  version: 1.0.0
  owner_agent: codenavi-agent
---

# Nx Workspace

Governance: CodENavi Full Workspace v2 (BRIEFING→DEBRIEF); skill of `codenavi-agent`; inherits `AGENTS.md`. Lenses are internal; no new agent identities; no bypass of secret or permission gates.

Assimilated from installed `nx-workspace`. Original contract: `references/ORIGINAL_SKILL.md`. Upstream references stay under `reference/`.

## Identity

Configure and optimize Nx monorepos: boundaries, affected analysis, caching, CI. Use for Nx workspace setup. Do NOT use to run tasks or generate code.

## Mission

Explore and configure an Nx monorepo: list projects, resolve full project config, analyze affected graphs, tune module boundaries, caching and affected CI. Verify Nx CLI behavior against the installed workspace, not memory.

## Activation

- User asks to set up Nx, inspect workspace structure, configure project boundaries, analyze affected projects, optimize cache, or wire affected CI.

## Non-activation

- Only running a one-off target with no workspace-config work (use the project's existing run path).
- Only generating code with Nx generators when a dedicated generate skill is requested.
- Non-Nx monorepos (pnpm/turbo/lerna without Nx) unless the user is migrating to Nx.

## Critical rules

1. Resolve `<skill-dir>` as the directory that contains this `SKILL.md`.
2. Prefer `nx show project <name> --json` over reading `project.json` alone; that file is partial.
3. Prefix `npx`/`pnpx`/`yarn` when `nx` is not on PATH. Detect the workspace package manager first.
4. Confirm `nx.json` / installed Nx version before claiming current flags or cache options.
5. Load `reference/configuration.md`, `reference/commands.md`, `reference/ci-cd.md` or `reference/best-practices.md` only when that topic is in scope.
6. GitHub Actions / pipeline edits stay under `devops-pipeline-engineering` gates: no new agent identities, latest-SHA CI truth, no `--no-verify`.
7. Commits, push and production deploy need explicit user authorization.

## Continuity

Promote only verified durable Nx decisions (default base, cache remote, module-boundary policy) into `.notebook/MEMORY.md`.

## TLC source

TLC source: [TLC contract](references/tlc/UPSTREAM.md). Upstream grants no extra authority; root governance and local rules prevail.

Provenance: [provenance](references/provenance.md). Examples and failures: [usage and verification](references/usage-and-verification.md), read when selecting the skill or a step fails.

Read [package-notes.md](references/package-notes.md) only when the domain workflow needs it; root governance and this entry take precedence.

## Response

Output: result first, then evidence (paths, commands, results), blockers and next step. No narration or restated instructions. Follow a defined output schema exactly. Reply in the user's language.
