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

### DevOps workflow guardians
- Status: active
- Fact: GitHub Actions specialization must not recreate subagent identities. Per-workflow coverage uses `WorkflowGuardianLens`; per-job/matrix coverage uses `JobGuardianWorkUnit`, all owned by `codenavi-agent`.
- Evidence: `skills/devops-pipeline-engineering/SKILL.md`, `skills/github-operations/actions/GUARDIANS.md`
- Updated: 2026-09-11

### Latest-SHA CI truth
- Status: active
- Fact: GitHub API HTTP success is not pipeline success. Merge evidence is valid only when all repository-required Actions/jobs/checks for the current expected head SHA are terminal and successful; corrective pushes invalidate prior-SHA CI evidence.
- Evidence: `scripts/aeos-devops-pipeline-governance.mjs`, `aeos/playbooks/devops-recursive-pipeline-recovery.playbook.md`
- Updated: 2026-09-11

### Repository deletion policy
- Status: active
- Fact: AEOS permanently denies repository deletion even for owner/admin requests. Deletion is manual-only outside AEOS and cannot be approved, delegated or automated.
- Evidence: `skills/github-operations/SKILL.md`, `skills/devops-pipeline-engineering/PERMISSIONS.yaml`
- Updated: 2026-09-11

### GitHub credential handling
- Status: active
- Fact: PAT/secret values are runtime-only; tracked configuration may contain only references such as `env://GITHUB_PAT`. Credentials never enter model context, Token Manager, evidence, notebook or Git bundles.
- Evidence: `skills/github-operations/SKILL.md`, `skills/github-operations/POLICY.md`
- Updated: 2026-09-11
