# LEARNING

Updated: 2026-09-12

## Validated learnings

### Zero-Python inventory blocks assimilated skill gates
- Context/trigger: feature skills that ship `scripts/*.py` were copied into the workspace while `aeos-no-python-guard.mjs` still failed on any `*.py`.
- Problem/failure mode: assimilation could look complete in registries and still be blocked by bootstrap/verify.
- Root cause: a workspace-wide language ban treated skill tools as policy violations.
- Verified correction/prevention: allow Python in the workspace; keep Node for kernel orchestration; make the guard require declared skill scripts instead of forbidding them.
- Reuse scope: any later assimilation of a skill that ships Python validators or project metadata.
- Evidence: `references/PYTHON_WORKSPACE_POLICY.md`, `scripts/aeos-python-workspace-guard.mjs`, `.notebook/PROGRESS.md`
- Confidence: high
- Updated: 2026-09-12


### Bootstrap containerized WordPress through a physical script
- Context/trigger: local WordPress installation and WooCommerce seed data needed to run inside a Docker container without leaking generated credentials.
- Problem/failure mode: ad hoc PHP fed through a container stdin can be interpreted inconsistently and makes exit-status validation less clear.
- Root cause: bootstrap logic was coupled to shell transport rather than a versioned PHP entry point.
- Verified correction/prevention: run a repository-owned bootstrap PHP script through `docker compose exec`, pass the generated local admin secret only as a runtime environment variable, and fail PowerShell on a non-zero exit code.
- Reuse scope: local Docker WordPress initialization and other containerized PHP migrations.
- Evidence: `E:\GitHub\repos-workspace\reidoabc\scripts\bootstrap-local-wordpress.ps1`, `.notebook\PROGRESS.md`.
- Confidence: high
- Updated: 2026-09-12

### Validate external cookie files before any content preview
- Context/trigger: WordPress runtime access was requested through an external cookie path, but the requested `.txt` file was missing and a nearby file was not a cookie jar.
- Problem/failure mode: treating a nearby credential-looking file as a cookie source can expose plaintext credentials during diagnostics and still fail authentication.
- Root cause: file existence and cookie-jar format were not validated before inspecting nearby candidate content.
- Verified correction/prevention: first verify exact path existence, then validate Netscape/Set-Cookie shape without printing contents; if invalid, stop credential handling and request/procure a real cookie jar or governed backup/export access.
- Reuse scope: any AEOS workflow that consumes external cookie/cookie-jar files for authenticated HTTP.
- Evidence: `.notebook/PROGRESS.md`, `.aeos/wordpress/sites/3015e2f77281a57c0f638d5ae2f64ed86a7694fbe018bbe926f36319d945d6d5/security-audit.json`
- Confidence: high
- Updated: 2026-09-11

### Centralize runtime credentials behind opaque sessions
- Context/trigger: session-authenticated systems such as remote WordPress require cookie jars, while workspace rules prohibit persisting credential values.
- Problem/failure mode: implementing cookie reading separately in each skill/MCP either duplicates security logic or pushes raw credentials into model/tool parameters.
- Root cause: credential acquisition and credential use were coupled to domain adapters.
- Verified correction/prevention: keep acquisition/materialization in a central runtime broker; return opaque session refs; make governed adapters consume the session internally with TTL, host scoping, redaction and shutdown cleanup.
- Reuse scope: every AEOS integration that requires cookies, environment credentials or future credential-provider adapters.
- Evidence: `runtime/src/kernel/runtime-auth-broker.ts`, `runtime/src/kernel/tool-router.ts`, `references/CODENAVI_RUNTIME_AUTH_STANDARD.md`, AEOS Enterprise CI runs #154/#155.
- Confidence: high
- Updated: 2026-09-11

### Overlay registries must be active in the execution runtime
- Context/trigger: WordPress skills/playbooks/MCPs were correctly indexed as overlay fragments but the kernel still loaded several base registries directly.
- Problem/failure mode: an artifact can exist, pass documentation/static checks and still be unreachable by real playbook execution.
- Root cause: registry overlay resolution and execution-time registry loading had diverged.
- Verified correction/prevention: load base + active overlay fragments by registry type with deterministic replacement order; test that overlay-only skill/playbook/MCP IDs resolve and that core runtime MCPs are injected.
- Reuse scope: all future AEOS registry extensions.
- Evidence: `runtime/src/kernel/registry-loader.ts`, `tests/node/runtime-auth-broker.test.cjs`.
- Confidence: high
- Updated: 2026-09-11

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
