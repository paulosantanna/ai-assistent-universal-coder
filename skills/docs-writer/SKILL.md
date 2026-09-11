---
name: docs-writer
description: "Use for Skill: docs-writer."
---

# Skill: docs-writer
Governance: CodENavi v1

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