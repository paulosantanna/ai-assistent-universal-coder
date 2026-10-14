---
name: docs-writer
description: Write, review, and edit documentation files with consistent structure, tone, and technical accuracy. Use when creating docs, reviewing markdown files, writing READMEs, updating `/docs` directories, or when user says "write documentation", "review this doc", "improve this README", "create a guide", or "edit markdown". Do NOT use for code comments, inline JSDoc, or API reference generation.
license: CC-BY-4.0
metadata:
  author: Tech Leads Club
  version: 1.0.0
  owner_agent: codenavi-agent
---

# Skill: docs-writer

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; inherit `AGENTS.md`.
Lifecycle: BRIEFING → RECON → PLAN → EXECUTE → VERIFY → DEBRIEF.
Source roles/workers are internal lenses. Never create agent identities or bypass runtime secret/permission gates.

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

## TLC source

For the catalog workflow and its local resources, read [TLC contract](references/tlc/UPSTREAM.md). Apply root governance and the local constraints above; upstream does not grant extra authority.

Provenance and source freshness: [provenance](references/provenance.md).

Example usage and failure handling: read [usage and verification](references/usage-and-verification.md) when selecting this skill or a required step fails.
