---
name: nx-workspace
description: "Assimilated TLC Nx workspace skill. Configure, explore and optimize Nx monorepos: project boundaries, affected analysis, caching and CI with affected commands. Triggers: nx, monorepo, workspace, projects, targets, affected. Do not use as the primary skill only to run a task or only to generate code."
---

# Nx Workspace

Assimilated from installed `nx-workspace`. Original contract: `references/ORIGINAL_SKILL.md`. Upstream references stay under `reference/`.

## Identity

A skill of the single canonical `codenavi-agent`. It creates no new agent identity.

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
