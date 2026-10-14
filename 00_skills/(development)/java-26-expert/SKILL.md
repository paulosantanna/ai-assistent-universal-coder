---
name: java-26-expert
description: Build or migrate production Java 26 projects with explicit handling of current/preview/incubator status and verified deployment compatibility. Use when the user requests java 26 expert or invokes java-26-expert. Do NOT use for unrelated languages, domains or production deployment.
license: CC-BY-4.0
metadata:
  author: AEOS
  version: 1.0.0
  owner_agent: codenavi-agent
---

# Java 26 Expert

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; inherit `AGENTS.md`.
Lifecycle: BRIEFING → RECON → PLAN → EXECUTE → VERIFY → DEBRIEF.
Source roles/workers are internal lenses. Never create agent identities or bypass runtime secret/permission gates.

Governance: CodENavi Full Workspace v2

## Mission
Build or migrate production Java 26 projects with explicit handling of current/preview/incubator status and verified deployment compatibility.

## Procedure
BRIEFING → RECON → PLAN → EXECUTE → VERIFY → DEBRIEF.

Detect exact JDK/toolchain/runtime first. Use `docs-java-26` for API signatures, release status and migration deltas. Preview/incubator capabilities are forbidden unless the project explicitly enables them and production/runtime/CI/tests are aligned.

Verify compile/package, tests/contracts, startup, JVM flags, reflection/serialization/native boundaries, security and performance when affected. Keep migration reversible.

## Token discipline
Read `references/INDEX.md`; query symbols/topics narrowly rather than loading release/API documentation wholesale.

Provenance and source freshness: [provenance](references/provenance.md).

Example usage and failure handling: read [usage and verification](references/usage-and-verification.md) when selecting this skill or a required step fails.
Read [preview-policy.md](references/preview-policy.md) only when the domain workflow needs that supporting context; root governance and this entry take precedence.
