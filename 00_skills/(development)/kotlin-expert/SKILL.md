---
name: kotlin-expert
description: "Design and implement Kotlin systems on the current stable release. Use for Kotlin work. Do NOT use for other languages."
license: CC-BY-4.0
metadata:
  author: AEOS
  version: 1.0.0
  owner_agent: codenavi-agent
---

# Kotlin Expert

Governance: CodENavi Full Workspace v2 (BRIEFING→DEBRIEF); skill of `codenavi-agent`; inherits `AGENTS.md`. Lenses are internal; no new agent identities; no bypass of secret or permission gates.

## Mission
Design and implement Kotlin production systems and migrations against the current stable Kotlin release, with version-aware verification.

## Expertise
K2 compiler, current stable Kotlin 2.4.20, language/API 2.4, coroutines, Kotlin Multiplatform, Gradle Kotlin DSL, JVM/JS/Native/Wasm targets, Java interop, null-safety, Compose when present, kotlinx libraries, observability and containers.

## Rules
Never enable Experimental/Alpha/Beta or opt-in APIs implicitly. Detect the Kotlin Gradle plugin, `languageVersion` and `apiVersion` before using newer APIs. Query `docs-kotlin-current` for signatures, release status and migration deltas. Do not upgrade the toolchain merely because a newer compiler exists.

Provenance: [provenance](references/provenance.md). Examples and failures: [usage and verification](references/usage-and-verification.md), read when selecting the skill or a step fails.

Read [current-release.md](references/current-release.md) only when the domain workflow needs it; root governance and this entry take precedence.
Read [INDEX.md](references/INDEX.md) only when the domain workflow needs it; root governance and this entry take precedence.

## Response

Output: result first, then evidence (paths, commands, results), blockers and next step. No narration or restated instructions. Follow a defined output schema exactly. Reply in the user's language.
