---
name: workspace-brain
description: Operate the CodENavi workspace brain MCP and CLI — cloud DeepSeek RAG, disk corpus at WORKSPACE_BRAIN_ROOT, Jev URL curation, and event logging for Cursor/Codex/OpenCode/Claude. Use when ingesting repo knowledge, asking the brain, mapping web seeds, or recording AI-driven file changes. Do NOT use for local Ollama RAG or storing API keys in git.
license: MIT
metadata:
  author: AEOS
  version: 0.1.0
  owner_agent: codenavi-agent
---

# workspace-brain

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`.

## Preconditions

- `WORKSPACE_BRAIN_ROOT` set (Windows default `E:\Github\workspace-brain`).
- `DEEPSEEK_API_KEY` or `E:\JEV\deepseek.key` for `brain_ask`.
- Optional: `TYPESAFE_API_KEY` or `E:\JEV` for Jev URL gates.

## Workflow

1. `wb doctor` — verify layout and credential presence (no secret values).
2. `wb ingest <universal-coder-root>` — chunk text into corpus.
3. `wb map-seeds` — ingest GitHub URLs from `07_mapeamentos` when `UNIVERSAL_CODER_ROOT` is set.
4. Register MCP via `wb install-agents` and merge snippets into `.cursor`, `.opencode`, etc.
5. After code changes, call `brain_record_event` or `wb event` so the brain can re-ingest incrementally.

## MCP tools

Prefer MCP over ad-hoc scripts: `brain_search`, `brain_ask`, `brain_ingest_path`, `brain_ingest_url`, `brain_map_seeds`, `brain_record_event`, `brain_manifest`, `brain_health`.

## Boundaries

- Corpus and manifests stay on disk; promotion to `.notebook/MEMORY.md` follows `chromatic-mega-brain`.
- No second agent identity; this skill routes work for `codenavi-agent`.
