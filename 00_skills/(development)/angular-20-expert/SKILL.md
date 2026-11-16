---
name: angular-20-expert
description: "Implement, diagnose or modernize Angular 20 apps without other-major behavior. Use for Angular 20 work. Do NOT use for other stacks."
license: CC-BY-4.0
metadata:
  author: AEOS
  version: 1.0.0
  owner_agent: codenavi-agent
---

# Angular 20 Expert

Governance: CodENavi Full Workspace v2 (BRIEFING→DEBRIEF); skill of `codenavi-agent`; inherits `AGENTS.md`. Lenses are internal; no new agent identities; no bypass of secret or permission gates.

## Mission
Implement, diagnose and modernize Angular 20 applications without silently introducing behavior from a different Angular major.

## Recon
Detect Angular/CLI/TypeScript/RxJS/Node versions from manifests/lockfiles, workspace config, tsconfig, builders, SSR/hydration setup and tests. Use `docs-angular-20` for current Angular 20 APIs and migration guidance.

## Execution
Follow existing standalone/module architecture, signals/RxJS conventions, DI, routing, forms, SSR/hydration and change-detection patterns already present. Do not perform unrelated framework modernization.

## Verify
Build/typecheck, unit/integration/e2e where applicable, SSR/hydration, bundle/performance, accessibility and browser-visible contracts.

## Token discipline
Read `references/INDEX.md`; load only architecture/testing/migration reference needed by the mission.

Provenance: [provenance](references/provenance.md). Examples and failures: [usage and verification](references/usage-and-verification.md), read when selecting the skill or a step fails.

Read [architecture.md](references/architecture.md) only when the domain workflow needs it; root governance and this entry take precedence.
Read [verification.md](references/verification.md) only when the domain workflow needs it; root governance and this entry take precedence.

## Response

Output: result first, then evidence (paths, commands, results), blockers and next step. No narration or restated instructions. Follow a defined output schema exactly. Reply in the user's language.
