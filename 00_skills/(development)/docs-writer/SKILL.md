---
name: docs-writer
description: "Write, review and edit docs for structure, tone and accuracy. Use for docs or READMEs. Do NOT use for code comments or API reference generation."
license: CC-BY-4.0
metadata:
  author: Tech Leads Club
  version: 1.0.0
  owner_agent: codenavi-agent
---

# Skill: docs-writer

Governance: CodENavi Full Workspace v2 (BRIEFING→DEBRIEF); skill of `codenavi-agent`; inherits `AGENTS.md`. Lenses are internal; no new agent identities; no bypass of secret or permission gates.

## Mission
Create or update documentation that is factual, compact, current and traceable to code/config/official sources.

## Rules
- Recon before writing: inspect implementation, tests, config and existing docs.
- Do not duplicate canonical rules; link/pointer to the authoritative source.
- Preserve technical nomenclature where translation would distort meaning.
- Use examples only when validated against the current implementation/API.
- When behavior changes, update the smallest authoritative document in the same mission.
- Mark uncertain or environment-specific statements explicitly.
- Never include secrets, tokens, cookies, passwords or unredacted credentials.

## Verify
Validate links/paths/examples where tooling permits and ensure docs do not contradict `.notebook/` or runtime behavior.

## TLC source

TLC source: [TLC contract](references/tlc/UPSTREAM.md). Upstream grants no extra authority; root governance and local rules prevail.

Provenance: [provenance](references/provenance.md). Examples and failures: [usage and verification](references/usage-and-verification.md), read when selecting the skill or a step fails.

## Response

Output: result first, then evidence (paths, commands, results), blockers and next step. No narration or restated instructions. Follow a defined output schema exactly. Reply in the user's language.
