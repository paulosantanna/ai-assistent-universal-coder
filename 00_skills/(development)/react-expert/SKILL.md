---
name: react-expert
description: Implement and refactor production React applications using the exact repository React/runtime/framework version and existing component/state/data-fetching conventions. Use when the user requests react expert or invokes react-expert. Do NOT use for unrelated languages, domains or production deployment.
license: CC-BY-4.0
metadata:
  author: AEOS
  version: 1.0.0
  owner_agent: codenavi-agent
---

# React Expert

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; inherit `AGENTS.md`.
Lifecycle: BRIEFING → RECON → PLAN → EXECUTE → VERIFY → DEBRIEF.
Source roles/workers are internal lenses. Never create agent identities or bypass runtime secret/permission gates.

Governance: CodENavi Full Workspace v2

## Mission
Implement and refactor production React applications using the exact repository React/runtime/framework version and existing component/state/data-fetching conventions.

## Recon
Detect React version, framework (if any), bundler, router, state/data libraries, SSR/RSC/client boundaries, TypeScript config and test stack. Verify current React/framework behavior from official/governed docs before relying on memory.

## Execution
Preserve component ownership and state locality. Avoid effects when derived/render-time logic suffices. Respect server/client boundaries and existing styling/testing conventions. Make surgical changes.

## Verify
Type/build, behavior-focused component/integration/e2e tests where required, hydration/runtime errors, accessibility and performance when affected.

## Token discipline
Read `references/INDEX.md`; open only state/rendering/server-client/verification modules relevant to the mission.

Provenance and source freshness: [provenance](references/provenance.md).

Example usage and failure handling: read [usage and verification](references/usage-and-verification.md) when selecting this skill or a required step fails.
Read [rendering-state.md](references/rendering-state.md) only when the domain workflow needs that supporting context; root governance and this entry take precedence.
Read [verification.md](references/verification.md) only when the domain workflow needs that supporting context; root governance and this entry take precedence.
