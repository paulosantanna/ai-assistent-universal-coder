# MEMORY

Updated: 2026-09-11

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
