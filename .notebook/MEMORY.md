# MEMORY

Updated: 2026-09-12

## Active memory

### Canonical agent identity
- Status: active
- Fact: AEOS has exactly one agent identity: `codenavi-agent`; specialization belongs to skills, playbooks, MCPs, LSPs/LCPs, lenses and tools.
- Evidence: `AGENT.md`, `aeos/registries/agents.registry.yaml`
- Updated: 2026-09-09

### Canonical mission lifecycle
- Status: active
- Fact: Material missions follow `BRIEFING → RECON → PLAN → EXECUTE → VERIFY → DEBRIEF`.
- Evidence: `AGENT.md`
- Updated: 2026-09-09

### Continuity quartet
- Status: active
- Fact: Material work uses `.notebook/HANDOFF.md`, `.notebook/MEMORY.md`, `.notebook/PROGRESS.md` and `.notebook/LEARNING.md` with non-overlapping responsibilities.
- Evidence: `references/CODENAVI_CONTINUITY_STANDARD.md`
- Updated: 2026-09-09

### Universal runtime authentication
- Status: active
- Fact: Every resolved AEOS playbook can access core `runtime-auth` and `runtime-http`; skills exchange opaque runtime session references rather than raw cookies/tokens/passwords. External cookie files may be consumed in place but credential contents never enter persisted/model-facing artifacts.
- Evidence: `references/CODENAVI_RUNTIME_AUTH_STANDARD.md`, `runtime/src/kernel/runtime-auth-broker.ts`, `runtime/src/kernel/registry-loader.ts`
- Updated: 2026-09-11

### Overlay registries are runtime-active
- Status: active
- Fact: Runtime loading of skills, playbooks, MCPs and LCPs resolves active fragments from `overlay.registry.index.yaml`; overlay-only entries are not documentation-only.
- Evidence: `runtime/src/kernel/registry-loader.ts`, `tests/node/runtime-auth-broker.test.cjs`
- Updated: 2026-09-11

### WordPress first-run Beta Mapping
- Status: active
- Fact: `wordpress-expert` performs a full read-only Beta Mapping only when no valid consolidated site map exists. Later runs reuse the map and use lightweight drift/preflight; full remap requires explicit request or invalid/corrupt map.
- Evidence: `skills/wordpress-expert/BETA_MAPPING.md`, `aeos/playbooks/wordpress-expert-site-lifecycle.playbook.md`
- Updated: 2026-09-11

### WordPress knowledge authority
- Status: active
- Fact: Official WordPress developer/project documentation is normative for API/security semantics; Reddit is retained as non-normative community evidence for operational experience, edge cases and failure patterns.
- Evidence: `aeos/mcps/wordpress-knowledge.mcp.yaml`, `aeos/mcp-servers/wordpress-knowledge-mcp.mjs`
- Updated: 2026-09-11

### Rei do ABC WordPress clone anchor
- Status: active
- Fact: `https://reidoabc.com.br` maps to site id `3015e2f77281a57c0f638d5ae2f64ed86a7694fbe018bbe926f36319d945d6d5`; its local working clone path is `E:\GitHub\repos-workspace\reidoabc`.
- Evidence: `.aeos/wordpress/sites/3015e2f77281a57c0f638d5ae2f64ed86a7694fbe018bbe926f36319d945d6d5/beta-map.json`, `E:\GitHub\repos-workspace\reidoabc\README.md`
- Updated: 2026-09-11

### Rei do ABC full local WordPress runtime
- Status: active
- Fact: `E:\GitHub\repos-workspace\reidoabc` is the complete local WordPress/WooCommerce evaluation runtime, using PHP 8.5, MySQL 8.4 and the black-and-gold `reidoabc-gourmet-reference` theme. `E:\GitHub\repos-workspace\reidoabc-wordpress` is the preserved reference package, not the runtime target. Neither is deployed to KingHost.
- Evidence: `E:\GitHub\repos-workspace\reidoabc\README.md`, `E:\GitHub\repos-workspace\reidoabc\docs\reference-gourmet-mobile.png`, `.notebook\PROGRESS.md`
- Updated: 2026-09-12

### DevOps workflow guardians
- Status: active
- Fact: GitHub Actions specialization must not recreate subagent identities. Per-workflow coverage uses `WorkflowGuardianLens`; per-job/matrix coverage uses `JobGuardianWorkUnit`, all owned by `codenavi-agent`.
- Evidence: `skills/devops-pipeline-engineering/SKILL.md`, `skills/github-operations/actions/GUARDIANS.md`
- Updated: 2026-09-11

### Latest-SHA CI truth
- Status: active
- Fact: GitHub API HTTP success is not pipeline success. Merge evidence is valid only when all repository-required Actions/jobs/checks for the current expected head SHA are terminal and successful; corrective pushes invalidate prior-SHA CI evidence.
- Evidence: `scripts/aeos-devops-pipeline-governance.mjs`, `skills/devops-pipeline-engineering/SKILL.md`
- Updated: 2026-09-11

### Repository deletion policy
- Status: active
- Fact: AEOS permanently denies repository deletion even for owner/admin requests. Deletion is manual-only outside AEOS and cannot be approved, delegated or automated.
- Evidence: `skills/github-operations/SKILL.md`, `skills/devops-pipeline-engineering/PERMISSIONS.yaml`
- Updated: 2026-09-11

### GitHub credential handling
- Status: active
- Fact: PAT/secret values are runtime-only; tracked configuration contains references, not values. GitHub credentials never enter model context, Token Manager, evidence, notebook or Git bundles.
- Evidence: `skills/github-operations/SKILL.md`, `skills/github-operations/POLICY.md`
- Updated: 2026-09-11

### Python is allowed in the workspace
- Status: active
- Fact: The zero-Python inventory policy is retired. Python source and project metadata are allowed. Skill-local `*.py` validators are first-class. AEOS kernel/runtime orchestration remains Node/TypeScript unless a later mission changes that surface.
- Evidence: `references/PYTHON_WORKSPACE_POLICY.md`, `scripts/aeos-python-workspace-guard.mjs`
- Updated: 2026-09-12

### Spec-driven feature skills assimilated
- Status: active
- Fact: Installed Tech Lead's Club `tlc-spec-driven` 3.3.0 and `tlc-spec-lean` 1.0.0 are governed AEOS skills `spec-driven` and `spec-driven-lean`, owned by `codenavi-agent`. Source sub-agent roles are lenses. `specs` remains the mutating preflight. Overlay fragment: `aeos/registries/skills.spec-driven.additions.yaml`.
- Evidence: `skills/spec-driven/SKILL.md`, `skills/spec-driven-lean/SKILL.md`, `aeos/registries/overlay.registry.index.yaml`
- Updated: 2026-09-12

### KingHost control MCP and expert super-skill
- Status: active
- Fact: `kinghost-control` is the deterministic MCP for KingHost environments, opaque credential bind, WordPress/PHP/MySQL plans and FTP publish. `kinghost-expert` is the governing super-skill; production follows a fixed FSM and may authenticate with an external cookie jar or Playwright. Passwords are never persisted or returned to the model.
- Evidence: `aeos/mcps/kinghost-control.mcp.yaml`, `skills/kinghost-expert/SKILL.md`, `kinghost-control-mcp/index.mjs`, `aeos/playbooks/kinghost-expert-production-lifecycle.playbook.md`
- Updated: 2026-09-12

### TLC catalog skills copied into the workspace
- Status: active
- Fact: Installed TLC skills `not-your-babysitter`, `cursor-subagent-creator`, `subagent-creator`, `skill-architect`, `technical-design-doc-creator`, `best-practices`, `the-fool`, `the-jury`, `ai-seo`, `nx-workspace`, `tlc-plan`, `learning-opportunities`, `perf-astro`, `core-web-vitals`, `perf-lighthouse`, `perf-web-optimization`, `security-best-practices`, `security-ownership-map`, `security-threat-model` and `web-quality-audit` live under `skills/` and overlay fragment `aeos/registries/skills.tlc-catalog.additions.yaml`. All are owned by `codenavi-agent`. `cursor-subagent-creator`, `subagent-creator` and `the-jury` remap source subagents to lenses; they must not register another agent identity. Session teaching from `learning-opportunities` is not a LEARNING.md promotion unless `learning-curator` verifies it. `security-audit` / `threat-modeler` remain the existing AEOS audit playbooks; the TLC trio does not replace them.
- Evidence: `aeos/registries/skills.tlc-catalog.additions.yaml`, `skills/cursor-subagent-creator/SKILL.md`, `skills/the-jury/SKILL.md`
- Updated: 2026-09-12
