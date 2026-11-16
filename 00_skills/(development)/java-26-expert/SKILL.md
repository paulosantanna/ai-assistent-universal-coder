---
name: java-26-expert
description: "Build or migrate Java 26 projects; handle preview status and verify runtime compatibility. Use for Java 26 work. Do NOT use for other languages."
license: CC-BY-4.0
metadata:
  author: AEOS
  version: 1.0.0
  owner_agent: codenavi-agent
---

# Java 26 Expert

Governance: CodENavi Full Workspace v2 (BRIEFING→DEBRIEF); skill of `codenavi-agent`; inherits `AGENTS.md`. Lenses are internal; no new agent identities; no bypass of secret or permission gates.

## Mission
Build or migrate production Java 26 projects with explicit handling of current/preview/incubator status and verified deployment compatibility.

## Procedure
BRIEFING → RECON → PLAN → EXECUTE → VERIFY → DEBRIEF.

Detect exact JDK/toolchain/runtime first. Use `docs-java-26` for API signatures, release status and migration deltas. Preview/incubator capabilities are forbidden unless the project explicitly enables them and production/runtime/CI/tests are aligned.

Verify compile/package, tests/contracts, startup, JVM flags, reflection/serialization/native boundaries, security and performance when affected. Keep migration reversible.

## Token discipline
Read `references/INDEX.md`; query symbols/topics narrowly rather than loading release/API documentation wholesale.

Provenance: [provenance](references/provenance.md). Examples and failures: [usage and verification](references/usage-and-verification.md), read when selecting the skill or a step fails.

Read [preview-policy.md](references/preview-policy.md) only when the domain workflow needs it; root governance and this entry take precedence.

## Response

Output: result first, then evidence (paths, commands, results), blockers and next step. No narration or restated instructions. Follow a defined output schema exactly. Reply in the user's language.
