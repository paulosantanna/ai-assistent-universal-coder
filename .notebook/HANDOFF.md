# HANDOFF

Updated: 2026-09-13

## Objective
- Create `kotlin-expert` in the `java-21-expert` pattern and load the current stable Kotlin release.

## Last Verified State
- Skill contract: `skills/kotlin-expert/{SKILL.md,TOKEN_PROFILE.yaml,references/INDEX.md,references/current-release.md}`.
- Docs MCP: `docs-kotlin-current` resolved to Kotlin 2.4.20.
- Registries: skills.registry.yaml, skills.image-ai-pack.additions.yaml, mcps.registry.yaml, language-docs.registry.yaml, mcp-tools.allowlist.yaml, playbooks.registry.yaml.
- Verification not yet run in this session.

## Working Set
- `skills/kotlin-expert/`
- `aeos/mcps/docs-kotlin-current.mcp.yaml`
- `aeos/docs/sources/language-docs.registry.yaml`
- `aeos/registries/{skills.registry.yaml,skills.image-ai-pack.additions.yaml,mcps.registry.yaml,playbooks.registry.yaml}`
- `scripts/aeos-mcp-startup-smoke.mjs`
- `tests/node/{runtime-auth-broker.test.cjs,skill-router-overlay.test.cjs}`

## Risks And Next Actions
- Reconfirm Kotlin currency with `docs-kotlin-current` `language_docs.version_status` if a newer GitHub tag appears after 2.4.20.
- Run skill-frontmatter, skill-adapter, MCP smoke, overlay Jest and `aeos:verify`.
