---
name: react-expert
description: "Implement and refactor React apps on the repo's exact React version and conventions. Use for React work. Do NOT use for other stacks or deployment."
license: CC-BY-4.0
metadata:
  author: AEOS
  version: 1.0.0
  owner_agent: codenavi-agent
---

# React Expert

Governance: CodENavi Full Workspace v2 (BRIEFING→DEBRIEF); skill of `codenavi-agent`; inherits `AGENTS.md`. Lenses are internal; no new agent identities; no bypass of secret or permission gates.

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

Provenance: [provenance](references/provenance.md). Examples and failures: [usage and verification](references/usage-and-verification.md), read when selecting the skill or a step fails.

Read [rendering-state.md](references/rendering-state.md) only when the domain workflow needs it; root governance and this entry take precedence.
Read [verification.md](references/verification.md) only when the domain workflow needs it; root governance and this entry take precedence.

## Response

Output: result first, then evidence (paths, commands, results), blockers and next step. No narration or restated instructions. Follow a defined output schema exactly. Reply in the user's language.
