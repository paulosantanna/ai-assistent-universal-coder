---
name: codenavi
description: "Investigate unknown codebases and change them surgically. Use for bugs, features or unfamiliar flows. Do NOT use for greenfield, CI/CD or infra."
license: CC-BY-4.0
metadata:
  author: Tech Leads Club
  version: 1.0.0
  owner_agent: codenavi-agent
---

# Skill: codenavi

Governance: CodENavi Full Workspace v2 (BRIEFING→DEBRIEF); skill of `codenavi-agent`; inherits `AGENTS.md`. Lenses are internal; no new agent identities; no bypass of secret or permission gates.

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

TLC source: [TLC contract](references/tlc/UPSTREAM.md). Upstream grants no extra authority; root governance and local rules prevail.

Provenance: [provenance](references/provenance.md). Examples and failures: [usage and verification](references/usage-and-verification.md), read when selecting the skill or a step fails.

Read [coding-principles.md](references/coding-principles.md) only when the domain workflow needs it; root governance and this entry take precedence.
Read [notebook-spec.md](references/notebook-spec.md) only when the domain workflow needs it; root governance and this entry take precedence.

## Response

Output: result first, then evidence (paths, commands, results), blockers and next step. No narration or restated instructions. Follow a defined output schema exactly. Reply in the user's language.
