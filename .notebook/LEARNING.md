# LEARNING

Updated: 2026-09-11

## Validated learnings

### Separate continuity concerns instead of using one oversized memory file
- Context/trigger: long-running workspace work needs state continuity across sessions without contaminating durable memory with transient logs.
- Problem/failure mode: mixing current progress, durable facts, handoff state and generalized lessons creates stale or contradictory context.
- Root cause: different information lifetimes were stored in the same undifferentiated artifact.
- Verified correction/prevention: use four bounded artifacts — HANDOFF, MEMORY, PROGRESS and LEARNING — and cross-link instead of duplicating.
- Reuse scope: all material CodENavi-governed workspaces.
- Evidence: `references/CODENAVI_CONTINUITY_STANDARD.md`
- Confidence: high
- Updated: 2026-09-09

### Shared Node test files must respect every configured test runner
- Context/trigger: a new `.test.cjs` file is executed by both Jest and Mocha in `aeos:verify:full`.
- Problem/failure mode: Mocha `before` failed under Jest; switching blindly to Jest `beforeAll` then failed under Mocha.
- Root cause: the repository intentionally points more than one test runner at the same test glob, so runner-specific lifecycle globals are not portable.
- Verified correction/prevention: use a small compatibility selection (`beforeAll` when available, otherwise `before`) or runner-neutral test structure; verify the full matrix, not only the first runner.
- Reuse scope: all shared `tests/node/**/*.test.cjs` suites.
- Evidence: PR #26 recovery cycles 1–3; `tests/node/devops-pipeline-engineering.test.cjs`.
- Confidence: high
- Updated: 2026-09-11

### CI recovery must invalidate previous-SHA success after every corrective push
- Context/trigger: recursive pipeline repair creates a new commit for each root-cause correction.
- Problem/failure mode: treating a green older SHA as merge evidence can merge code that was never verified.
- Root cause: CI state was correlated to branch/PR conceptually rather than to the immutable head commit.
- Verified correction/prevention: bind run/job/check evidence and merge approval to expected head SHA; rediscover all relevant runs after every push.
- Reuse scope: every GitHub Actions recovery/merge workflow.
- Evidence: `scripts/aeos-devops-pipeline-governance.mjs`, `skills/devops-pipeline-engineering/SKILL.md`.
- Confidence: high
- Updated: 2026-09-11

### Overlay registries must be resolved by runtime routing, not merely indexed on disk
- Context/trigger: new DevOps/GitHub skills were added as overlay fragments.
- Problem/failure mode: `aeos-skill-router.mjs` originally read only `skills.registry.yaml`, so valid overlay skills could exist but never be selected.
- Root cause: runtime routing and registry overlay architecture had diverged.
- Verified correction/prevention: resolve active skill fragments from `overlay.registry.index.yaml`, merge by skill id in authoritative overlay order and test routing of overlay-only skills.
- Reuse scope: all future skill registry fragments.
- Evidence: `scripts/aeos-skill-router.mjs`, `tests/node/skill-router-overlay.test.cjs`.
- Confidence: high
- Updated: 2026-09-11
