---
name: angular-8-to-20-migration
description: "Migrate Angular 8 to 20 one major per step, keeping UI and async behavior. Use for upgrades. Do NOT use for single-version code (angular-20-expert)."
license: CC-BY-4.0
metadata:
  author: AEOS; photographic reference supplied by user
  version: 1.0.0
  owner_agent: codenavi-agent
---

# Angular 8 To 20 Migration

Governance: CodENavi Full Workspace v2 (BRIEFING→DEBRIEF); skill of `codenavi-agent`; inherits `AGENTS.md`. Lenses are internal; no new agent identities; no bypass of secret or permission gates.

Plan and execute Angular 8 to 20 migration one major at a time, preserving rendered UI, custom elements, HTTP interceptors and async behavior.

## Workflow

1. Capture manifests, lockfile, Angular/CLI/TypeScript/RxJS/Node versions and passing behavior before the first change.
2. Use legacy-migration-planner for baseline, strategy, phased plan and parity; consult the official Angular update guide for each adjacent major.
3. Advance 8→9→10→11→12→13→14→15→16→17→18→19→20. Run ng update for one major and verify before proceeding.
4. Track builders, Ivy, lint, tests, bootstrap, polyfills, RxJS, micro-frontend tags and any repository-specific CLI such as AFE as separate migration axes.
5. Compare before/after render, CSS encapsulation, custom-element name and inputs, interceptors and empty async streams; preserve evidence for a parity verdict.

## Rules

- The detected repository version governs until its migration step succeeds. Standalone, signals, zoneless and Jest are separate choices, never silent additions.
- A successful build does not prove parity. No next major while an acceptance check fails.
- Santander counts/paths in the photos are examples from that workspace, not facts about this one.

## Inputs and outputs

Inputs: the user-requested target, authorized source paths/access, scope and expected result.

A major-by-major plan, minimal diffs, version matrix, executed build/behavior checks and a parity verdict with source pointers.

## Verification and stop

Verify the actual outputs and relevant contract checks. Missing evidence, dependency, source asset, input or permission blocks its dependent stage; report the precise gap.

Provenance: [provenance](references/provenance.md).

## Response

Output: result first, then evidence (paths, commands, results), blockers and next step. No narration or restated instructions. Follow a defined output schema exactly. Reply in the user's language.
