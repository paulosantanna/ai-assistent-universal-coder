# architecture-knowledge

Entry point: `aeos/mcps/architecture-knowledge.mcp.yaml`, server `aeos/mcp-servers/architecture-knowledge-mcp.mjs`, playbook `aeos/playbooks/architecture-knowledge-lifecycle.playbook.md`
Updated: 2026-10-07

- Skills (TLC format, owner `codenavi-agent`): `architecture-decision-record` (ADR), `architecture-decision-log` (ADL), `architecturally-significant-requirement` (ASR), `architecture-knowledge-management` (AKM super-skill composing the other three). Registry: `aeos/registries/skills.architecture-knowledge.additions.yaml`.
- TLC baseline: ADR derives from TLC `create-adr` 1.0.0 (CC-BY-4.0), verbatim at `skills/architecture-decision-record/references/ORIGINAL_SKILL.md`; deltas to MADR 4.0.0 in `aeos/knowledge/architecture-knowledge-map.json` (`tlc_baseline`).
- Scripts (zero-dependency Node ESM, pure exports plus CLI): `adr_lint.mjs` is the shared ADR parser (`--strict` = authoring gate); `adl_index.mjs` imports it, never reuses numbers, rewrites only the `<!-- adl:index:* -->` block; `asr_test.mjs` maps 0 / 1 / 2-3 / 4+ criteria met to low / low-medium / medium-high / high (Zimmermann's examples).
- MCP: TLC disclosure `search_skills → read_skill → fetch_skill_files` (`list_skills` explicit only; floor 20; at most 5 files; 50,000 chars) plus `adr_lint | adl_index | asr_test | concepts | sources | health`. Read-only; paths confined by realpath to the workspace.
- Framing: replies in each request's framing; official `@modelcontextprotocol/sdk` 1.29.0 client connects. `rag-node` and `wordpress-knowledge` fail that handshake (see LEARNING).
- Router: `scripts/aeos-skill-router.mjs:scoreSkill()` matches space-delimited acronym aliases against a padded request; registry missions carry the Portuguese names.
- Workspace log: `aeos/docs/adr/` (`ADR-NNNN-UPPER-KEBAB.md`, `templates/ADR_TEMPLATE.md`); ADR-0001 is `proposed` and undated.
- Tests: `tests/node/architecture-knowledge-skills.test.cjs`, `tests/node/architecture-knowledge-mcp.test.cjs`, plus router and loader asserts.
