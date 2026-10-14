---
name: angular-20-expert
description: Implement, diagnose and modernize Angular 20 applications without silently introducing behavior from a different Angular major. Use when the user requests angular 20 expert or invokes angular-20-expert. Do NOT use for unrelated languages, domains or production deployment.
license: CC-BY-4.0
metadata:
  author: AEOS
  version: 1.0.0
  owner_agent: codenavi-agent
---

# Angular 20 Expert

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; inherit `AGENTS.md`.
Lifecycle: BRIEFING → RECON → PLAN → EXECUTE → VERIFY → DEBRIEF.
Source roles/workers are internal lenses. Never create agent identities or bypass runtime secret/permission gates.

Governance: CodENavi Full Workspace v2

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

Provenance and source freshness: [provenance](references/provenance.md).

Example usage and failure handling: read [usage and verification](references/usage-and-verification.md) when selecting this skill or a required step fails.
Read [architecture.md](references/architecture.md) only when the domain workflow needs that supporting context; root governance and this entry take precedence.
Read [verification.md](references/verification.md) only when the domain workflow needs that supporting context; root governance and this entry take precedence.
