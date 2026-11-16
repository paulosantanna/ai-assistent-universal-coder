---
name: nx-run-tasks
description: "Run Nx build, test, lint, serve and affected tasks in a workspace. Use for 'run tests' or 'nx affected'. Do NOT use for code generation (nx-generate)."
license: CC-BY-4.0
metadata:
  author: Tech Leads Club
  version: 1.0.0
  owner_agent: codenavi-agent
---

Governance: CodENavi Full Workspace v2 (BRIEFING→DEBRIEF); skill of `codenavi-agent`; inherits `AGENTS.md`. Lenses are internal; no new agent identities; no bypass of secret or permission gates.

You can run tasks with Nx in the following way.

Keep in mind that you might have to prefix things with npx/pnpx/yarn if the user doesn't have nx installed globally. Look at the package.json or lockfile to determine which package manager is in use.

For more details on any command, run it with `--help` (e.g. `nx run-many --help`, `nx affected --help`).

## Understand which tasks can be run

You can check those via `nx show project <projectname> --json`, for example `nx show project myapp --json`. It contains a `targets` section which has information about targets that can be run. You can also just look at the `package.json` scripts or `project.json` targets, but you might miss out on inferred tasks by Nx plugins.

## Run a single task

```
nx run <project>:<task>
```

where `project` is the project name defined in `package.json` or `project.json` (if present).

## Run multiple tasks

```
nx run-many -t build test lint typecheck
```

You can pass a `-p` flag to filter to specific projects, otherwise it runs on all projects. You can also use `--exclude` to exclude projects, and `--parallel` to control the number of parallel processes (default is 3).

Examples:

- `nx run-many -t test -p proj1 proj2` — test specific projects
- `nx run-many -t test --projects=*-app --exclude=excluded-app` — test projects matching a pattern
- `nx run-many -t test --projects=tag:api-*` — test projects by tag

## Run tasks for affected projects

Use `nx affected` to only run tasks on projects that have been changed and projects that depend on changed projects. This is especially useful in CI and for large workspaces.

```
nx affected -t build test lint
```

By default it compares against the base branch. You can customize this:

- `nx affected -t test --base=main --head=HEAD` — compare against a specific base and head
- `nx affected -t test --files=libs/mylib/src/index.ts` — specify changed files directly

## Useful flags

These flags work with `run`, `run-many`, and `affected`:

- `--skipNxCache` — rerun tasks even when results are cached
- `--verbose` — print additional information such as stack traces
- `--nxBail` — stop execution after the first failed task
- `--configuration=<name>` — use a specific configuration (e.g. `production`)

## TLC source

TLC source: [TLC contract](references/tlc/UPSTREAM.md). Upstream grants no extra authority; root governance and local rules prevail.

Provenance: [provenance](references/provenance.md).

## Response

Output: result first, then evidence (paths, commands, results), blockers and next step. No narration or restated instructions. Follow a defined output schema exactly. Reply in the user's language.
