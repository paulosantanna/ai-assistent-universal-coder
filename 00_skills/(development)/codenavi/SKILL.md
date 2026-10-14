---
name: codenavi
description: Your pathfinder for navigating unknown codebases. Investigates with precision, implements surgically, and never assumes — if it doesn't know, it says so. Maintains a .notebook/ knowledge base that grows across sessions, turning every discovery into lasting intelligence. Summons available skills, MCPs, and docs when the mission demands. Use when fixing bugs, implementing features, refactoring, investigating flows, or any development task in unfamiliar territory. Triggers on "fix this", "implement this", "how does this work", "investigate this flow", "help me with this code". Do NOT use for greenfield scaffolding, CI/CD, or infrastructure provisioning.
license: CC-BY-4.0
metadata:
  author: Tech Leads Club
  version: 1.0.0
  owner_agent: codenavi-agent
---

# Skill: codenavi

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; inherit `AGENTS.md`.
Lifecycle: BRIEFING → RECON → PLAN → EXECUTE → VERIFY → DEBRIEF.
Source roles/workers are internal lenses. Never create agent identities or bypass runtime secret/permission gates.

Governance: CodENavi v1

## Mission
Govern software changes through BRIEFING → RECON → PLAN → EXECUTE → VERIFY → DEBRIEF, using progressive project intelligence, continuity state and current authoritative documentation.

## Mandatory behavior
- Read `AGENTS.md`, `.notebook/INDEX.md` and relevant notes before material work.
- Ensure `.notebook/HANDOFF.md`, `.notebook/MEMORY.md`, `.notebook/PROGRESS.md` and `.notebook/LEARNING.md` exist and follow the root contract and the [continuity templates](../../(learning)/chromatic-mega-brain/templates/continuity/INDEX.md).
- State assumptions, uncertainty and acceptance criteria before coding.
- Prefer the simplest sufficient implementation and surgical diffs.
- Respect repository conventions and architectural boundaries.
- Verify APIs/framework behavior against current project/official docs.
- Keep `PROGRESS.md` live during execution; refresh HANDOFF, durable MEMORY and verified LEARNING in Debrief.
- Update stale notebook knowledge immediately.

## Output
`{"briefing":{},"recon":{},"plan":[],"changes":[],"verification":[],"continuity":{},"debrief":{},"status":"PASS|WARN|BLOCKED"}`

## TLC source

For the catalog workflow and its local resources, read [TLC contract](references/tlc/UPSTREAM.md). Apply root governance and the local constraints above; upstream does not grant extra authority.

Provenance and source freshness: [provenance](references/provenance.md).

Example usage and failure handling: read [usage and verification](references/usage-and-verification.md) when selecting this skill or a required step fails.
Read [coding-principles.md](references/coding-principles.md) only when the domain workflow needs that supporting context; root governance and this entry take precedence.
Read [notebook-spec.md](references/notebook-spec.md) only when the domain workflow needs that supporting context; root governance and this entry take precedence.
