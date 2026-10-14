# MEMORY

Updated: 2026-10-13

## Active memory

### Source-backed repository/skill routing
- Status: static mapping artifact; not external runtime validation.
- Fact: `07_mapeamentos/repositorios-skills/` records canonical catalog IDs, per-project ten-dimension maps, four applicability states and file/line/hash evidence. Source projects are read-only; aliases do not count as additional skills.
- Evidence: `07_mapeamentos/repositorios-skills/{README.md,mapa.json,verificacao.json,browser-verificacao.json}`; focused note `repositorios-skills.md`.
- Decision: refresh on source/catalog drift; never infer a local integration from name similarity, runtime availability from instructions, or CVE/EOL safety from manifests.
- Updated: 2026-10-13


### Canonical TLC instruction discovery
- Status: active instruction catalog; external runtime availability is not inferred.
- Fact: user-selected `00_skills/(category)/slug/` holds 302 active packages, including all 92 TLC packages pinned at `6df68d52028b9261058231e0f4998048c0352f45` and Impeccable 4.1.1 pinned at `5a149f3fdb1b5793f10567233b1dcab98fc305fd`. SKILL.md includes frontmatter in the 100-line cap; details are skill-local modules. Native discovery has 305 canonical/alias pointers; source resources retain license/attribution and hashes.
- Evidence: `00_skills/catalog.json`, `00_skills/upstream.manifest.json`, `00_skills/photo-update-verification.json`; focused entrypoint `tlc-skills.md`.
- Decision: preserve external deletions; never restore removed AEOS runtime/configuration from stale notes. Existing skill instructions remain usable subject to actual prerequisite checks.
- Updated: 2026-10-13

### Photo-derived skill activation boundaries
- Status: active instructions, not external runtime installation.
- Fact: the 2026-10-13 batch changes learning-opportunities to AAR/reusable-knowledge selection (quartet writing remains with its owning skills) and skill-architect to creating/evaluating/scoring/improving skills. Meeting/call video routes to acta-aurea even for a transcription-only verb; bare audio routes to vox-aurum. Impeccable source profiles are sequential local lenses, never new identities or genuinely blind independent review.
- Evidence: `00_skills/PHOTO-UPDATE.md`, affected canonical SKILL.md files, `00_skills/PHOTO-STRUCTURE.md`.
- Decision: name-only photographed skills remain inactive folders pending real contracts; official fonts/logo, private runtime integrations and absent speech engines are not inferred from photographs.
- Updated: 2026-10-13

### Runtime pointer reconciliation
- Status: current workspace boundary.
- Fact: the external reorganization removed root aeos/runtime/scripts/templates/references during the skill migration. Historical entries below retain prior verified observations, but references to deleted routers/registries/MCP configurations do not establish current runtime availability. Current instruction paths/catalog are the source of discovery truth.
- Evidence: `PROGRESS.md:Final acceptance evidence`, `00_skills/VERIFICATION.md`.
- Updated: 2026-10-12


### csharp-expert current stable pin
- Status: retained instruction knowledge; removed runtime pointers are historical
- Fact: `csharp-expert` is a TLC-format skill of `codenavi-agent` for production C# source. The folder id is `csharp-expert` because the TLC kebab-case check rejects `#`; the description triggers on `c#-expert`. New code targets C# 14 on .NET 10.0.12 (SDK 10.0.401, LTS, support through 2028-11-14). An existing project keeps its declared TFM. .NET 11.0.0-rc.1 / C# 15 stays unused unless the repository already targets it. There is no C# docs MCP.
- Historical/runtime evidence (check availability before use): `00_skills/(development)/csharp-expert/SKILL.md`, `00_skills/(development)/csharp-expert/references/current-release.md`, `aeos/registries/skills.csharp-expert.additions.yaml`
- Updated: 2026-10-09

### tests-expert oracle
- Status: retained instruction knowledge; removed runtime pointers are historical
- Fact: `tests-expert` runs real functional and end-to-end checks after a bug fix or new behavior. The user request is the only oracle. Frozen expectations cannot be edited to match a failing application. An open failure is `.aeos/tests-expert/RESUME.md` for a later context window, not a `MEMORY.md` entry. Unit and class tests are outside this skill.
- Historical/runtime evidence (check availability before use): `00_skills/(quality)/tests-expert/SKILL.md`, `00_skills/(quality)/tests-expert/scripts/charter.mjs`, `aeos/registries/skills.tests-expert.additions.yaml`, `tests/node/tests-expert-charter.test.cjs`
- Updated: 2026-10-08

### Architecture knowledge skills and MCP
- Status: retained instruction knowledge; removed runtime pointers are historical
- Fact: ADR, ADL, ASR and AKM are governed TLC-format skills owned by `codenavi-agent`: `architecture-decision-record` (derived from TLC `create-adr` 1.0.0, updated to MADR 4.0.0), `architecture-decision-log`, `architecturally-significant-requirement` and the super-skill `architecture-knowledge-management`. MCP `architecture-knowledge` is governed by `architecture-knowledge-management`, allowed by playbook `architecture-knowledge-lifecycle`, serves the skills through TLC progressive disclosure and runs their scripts offline. Accepted ADRs are immutable and numbers are never reused.
- Historical/runtime evidence (check availability before use): `aeos/registries/skills.architecture-knowledge.additions.yaml`, `aeos/mcps/architecture-knowledge.mcp.yaml`, `aeos/knowledge/architecture-knowledge-map.json`, `tests/node/architecture-knowledge-mcp.test.cjs`
- Updated: 2026-10-07

### TypeSafe Jev function-calling skill
- Status: retained instruction knowledge; removed runtime pointers are historical
- Fact: Upstream `typesafe-ai` is installed for agent use, and project-native `jev-call-expert` governs confidence-aware natural-language dispatch into allowlisted typed functions. Jev supplies bounded Choice/Noul judgments; code retains validation, defaults, authorization, confirmation and invocation.
- Historical/runtime evidence (check availability before use): `.agents/skills/typesafe-ai/SKILL.md`, `00_skills/(development)/jev-call-expert/SKILL.md`, `aeos/registries/skills.typesafe.additions.yaml`
- Updated: 2026-09-17

### Canonical agent identity
- Status: retained instruction knowledge; removed runtime pointers are historical
- Fact: AEOS has exactly one agent identity: `codenavi-agent`; specialization belongs to skills, playbooks, MCPs, LSPs/LCPs, lenses and tools.
- Historical/runtime evidence (check availability before use): `AGENT.md`, `aeos/registries/agents.registry.yaml`
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

### WordPress complete plugin universe
- Status: active
- Fact: `wordpress-expert` inventories and operates every plugin in `wp-content/plugins` and `wp-content/mu-plugins` (regular, must-use, single-file; active and inactive). A static catalog is not a ceiling. `kinghost-wordpress-publish` uploads those full plugin trees with the theme.
- Evidence: `00_skills/(development)/wordpress-expert/PLUGINS.md`, `kinghost-control-mcp/wordpress-ops.mjs:listLocalWordpressPlugins`, `wordpress_knowledge.plugin_universe_plan`
- Updated: 2026-09-16

### WordPress first-run Beta Mapping
- Status: retained instruction knowledge; removed runtime pointers are historical
- Fact: `wordpress-expert` performs a full read-only Beta Mapping only when no valid consolidated site map exists. Later runs reuse the map and use lightweight drift/preflight; full remap requires explicit request or invalid/corrupt map.
- Historical/runtime evidence (check availability before use): `00_skills/(development)/wordpress-expert/BETA_MAPPING.md`, `aeos/playbooks/wordpress-expert-site-lifecycle.playbook.md`
- Updated: 2026-09-11

### WordPress knowledge authority
- Status: retained instruction knowledge; removed runtime pointers are historical
- Fact: Official WordPress developer/project documentation is normative for API/security semantics; Reddit is retained as non-normative community evidence for operational experience, edge cases and failure patterns.
- Historical/runtime evidence (check availability before use): `aeos/mcps/wordpress-knowledge.mcp.yaml`, `aeos/mcp-servers/wordpress-knowledge-mcp.mjs`
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
- Evidence: `00_skills/(cloud)/devops-pipeline-engineering/SKILL.md`, `00_skills/(tooling)/github-operations/actions/GUARDIANS.md`
- Updated: 2026-09-11

### Latest-SHA CI truth
- Status: active
- Fact: GitHub API HTTP success is not pipeline success. Merge evidence is valid only when all repository-required Actions/jobs/checks for the current expected head SHA are terminal and successful; corrective pushes invalidate prior-SHA CI evidence.
- Evidence: `scripts/aeos-devops-pipeline-governance.mjs`, `00_skills/(cloud)/devops-pipeline-engineering/SKILL.md`
- Updated: 2026-09-11

### Repository deletion policy
- Status: active
- Fact: AEOS permanently denies repository deletion even for owner/admin requests. Deletion is manual-only outside AEOS and cannot be approved, delegated or automated.
- Evidence: `00_skills/(tooling)/github-operations/SKILL.md`, `00_skills/(cloud)/devops-pipeline-engineering/PERMISSIONS.yaml`
- Updated: 2026-09-11

### GitHub credential handling
- Status: active
- Fact: PAT/secret values are runtime-only; tracked configuration contains references, not values. GitHub credentials never enter model context, Token Manager, evidence, notebook or Git bundles.
- Evidence: `00_skills/(tooling)/github-operations/SKILL.md`, `00_skills/(tooling)/github-operations/POLICY.md`
- Updated: 2026-09-11

### Python is allowed in the workspace
- Status: active
- Fact: The zero-Python inventory policy is retired. Python source and project metadata are allowed. Skill-local `*.py` validators are first-class. AEOS kernel/runtime orchestration remains Node/TypeScript unless a later mission changes that surface.
- Evidence: `references/PYTHON_WORKSPACE_POLICY.md`, `scripts/aeos-python-workspace-guard.mjs`
- Updated: 2026-09-12

### Spec-driven feature skills assimilated
- Status: retained instruction knowledge; removed runtime pointers are historical
- Fact: Installed Tech Lead's Club `tlc-spec-driven` 3.3.0 and `tlc-spec-lean` 1.0.0 are governed AEOS skills `spec-driven` and `spec-driven-lean`, owned by `codenavi-agent`. Source sub-agent roles are lenses. `specs` remains the mutating preflight. Overlay fragment: `aeos/registries/skills.spec-driven.additions.yaml`.
- Historical/runtime evidence (check availability before use): `00_skills/(development)/spec-driven/SKILL.md`, `00_skills/(development)/spec-driven-lean/SKILL.md`, `aeos/registries/overlay.registry.index.yaml`
- Updated: 2026-09-12

### KingHost one-command WordPress publish
- Status: retained instruction knowledge; removed runtime pointers are historical
- Fact: Playbook `kinghost-wordpress-publish` publishes a locally altered WordPress/PHP/WooCommerce tree onto an already-hosted KingHost domain via `npm run aeos:kinghost:publish`. Default APPLY is scoped `wp-content` code. Live orders, customers, `siteurl`/`home`, payment secrets and `wp-config.php` stay on production. `--replace-database` is blocked on this path.
- Historical/runtime evidence (check availability before use): `aeos/playbooks/kinghost-wordpress-publish.playbook.md`, `scripts/aeos-kinghost-publish.mjs`, `kinghost-control-mcp/index.mjs:publishPreflight`
- Updated: 2026-09-16

### KingHost control MCP and expert super-skill
- Status: retained instruction knowledge; removed runtime pointers are historical
- Fact: `kinghost-control` is the KingHost Hospedagem control plane: cookie-jar panel login, existing domain list/select, already-created user inventory (redacted), WordPress/PHP/MySQL/WooCommerce, site clone and FTP tree publish. `kinghost-expert` governs the production FSM. Passwords and cookie values are never persisted or returned to the model. `kinghost-commerce` remains the SSH/SFTP/Postgres commerce adapter.
- Historical/runtime evidence (check availability before use): `aeos/mcps/kinghost-control.mcp.yaml`, `00_skills/(cloud)/kinghost-expert/SKILL.md`, `kinghost-control-mcp/index.mjs`, `kinghost-control-mcp/knowledge.mjs`
- Updated: 2026-09-16

### TLC catalog skills copied into the workspace
- Status: retained instruction knowledge; removed runtime pointers are historical
- Fact: Installed TLC skills `not-your-babysitter`, `cursor-subagent-creator`, `subagent-creator`, `skill-architect`, `technical-design-doc-creator`, `best-practices`, `the-fool`, `the-jury`, `ai-seo`, `nx-workspace`, `tlc-plan`, `learning-opportunities`, `perf-astro`, `core-web-vitals`, `perf-lighthouse`, `perf-web-optimization`, `security-best-practices`, `security-ownership-map`, `security-threat-model` and `web-quality-audit` live under `skills/` and overlay fragment `aeos/registries/skills.tlc-catalog.additions.yaml`. All are owned by `codenavi-agent`. `cursor-subagent-creator`, `subagent-creator` and `the-jury` remap source subagents to lenses; they must not register another agent identity. Session teaching from `learning-opportunities` is not a LEARNING.md promotion unless `learning-curator` verifies it. `security-audit` / `threat-modeler` remain the existing AEOS audit playbooks; the TLC trio does not replace them.
- Historical/runtime evidence (check availability before use): `aeos/registries/skills.tlc-catalog.additions.yaml`, `00_skills/(creation)/cursor-subagent-creator/SKILL.md`, `00_skills/(decision-making)/the-jury/SKILL.md`
- Updated: 2026-09-12

### Kotlin current-stable language expert
- Status: retained instruction knowledge; removed runtime pointers are historical
- Fact: `kotlin-expert` follows the `java-21-expert` skill contract and loads current stable Kotlin through `docs-kotlin-current`. Resolved version is Kotlin 2.4.20. The MCP is governed by `kotlin-expert`.
- Historical/runtime evidence (check availability before use): `00_skills/(development)/kotlin-expert/SKILL.md`, `aeos/mcps/docs-kotlin-current.mcp.yaml`, `aeos/docs/sources/language-docs.registry.yaml`
- Updated: 2026-09-13

### Open PRs require a Why/Porquê section
- Status: active
- Fact: Every open pull request must describe why the change exists. `github-operations` and `devops-pipeline-engineering` block PR create/update/merge when Why/Porquê is missing, empty or a placeholder. The gate exists so later worktrees keep adequate context. Executable check: `scripts/aeos-devops-pipeline-governance.mjs` `evaluatePrWhy()` / `mergeReadiness()`.
- Evidence: `00_skills/(tooling)/github-operations/SKILL.md`, `00_skills/(cloud)/devops-pipeline-engineering/SKILL.md`, `scripts/aeos-devops-pipeline-governance.mjs`, `.github/PULL_REQUEST_TEMPLATE.md`
- Updated: 2026-09-13

### RAG Node.js MCP stores the TLC repository's causal model
- Status: retained instruction knowledge; removed runtime pointers are historical
- Fact: `rag-node` is the governed offline Node.js/Express RAG MCP. Its 1.1.0 knowledge map derives from all 22 files and 12 commits of TLC source repo `odanieldcs/rag-api` at `27f7aab`, classifies it as 2-Step RAG, records why each indexing/query/serving step exists, and separates the educational baseline from current production guidance backed by official LangChain, OpenAI, Qdrant, MDN and Express docs.
- Historical/runtime evidence (check availability before use): `aeos/knowledge/rag-node-course-map.json`, `aeos/mcps/rag-node.mcp.yaml`, `aeos/mcp-servers/rag-node-mcp.mjs`, `tests/node/rag-node-mcp.test.cjs`
- Updated: 2026-09-18

### Dark-videos creative runtime contracts
- Durable creative/worker contracts are recorded in D:/Git/dark-videos/.notebook/MEMORY.md; source and verification pointer: `.work/creative-repair/RESULTADO.md`. The local model provider input modality was verified with actual image calls; text-model availability alone does not establish visual review capability.
- Updated: 2026-10-13

### Dark-videos scheduled publication contracts
Updated:2026-10-13
Entry point: D:/Git/dark-videos/.notebook/MEMORY.md
- Validated transaction/renderer/child-job contracts and source pointers live in the target notebook. Verified correction and functional charter: .work/publishing-fix/RESULTADO.md; .work/publishing-fix/state.json.

### Agenda distinguishes the queue from blocked history
Updated:2026-10-13
Entry point: backend/app/modules/publishing/api.py:schedule
- `publications` contains up to100 nonblocked upcoming rows; `blocked_publications` holds up to100 historical blocked rows separately. `upcoming_counts` spans the full eligible-status queue and `blocked_count` spans all blocked rows. The frontend marks blocked dates as previous schedules and offers no publishing action for them.
- Language admission checks ORIGINAL source title OR description, not the generated publishing copy. Confirmed by user; current code mining/metadata_policy.py and dispatch.py:_job.
- Evidence: E:/Github/ai-assistent-universal-coder/.work/youtube-unblock/RESULTADO.md; test_schedule_history.py and schedule/page.test.tsx.

### Asynchronous YouTube processing receipt
Updated:2026-10-13
Entry point: backend/app/modules/publishing/browser_post.py:_click_done/_youtube_dialog
- The processing notice can remain open after the Public save; receipt timing and shadow roots must be observed throughout the completion window. It is not publication proof: the same captured media ID must pass owned-channel Public/metadata confirmation. Capture is nonblocking because some flows expose the link only after save.
- Evidence: E:/Github/ai-assistent-universal-coder/.work/youtube-publish-now/RESULTADO.md; test_youtube_processing.py and receipt_applied-processing-tests.json. Final real-upload behavior remains a separate verification gate.

- Política obrigatória desde2026-10-14: dispatch prepara uploads antecipados; somente remote_id e scheduled_for exato retornados pelo Studio autorizam PLATFORM_SCHEDULED/carrier=platform. PENDING/SCHEDULED são reservas locais. Nenhum fallback worker ou publicação imediata em caso de falha. Fontes: publishing/release.py:_release_locked, dispatch.py:_run_dispatch/_write, studio_schedule.py; testes test_platform_schedule.py/test_native_studio_receipts.py.
- TikTok Stories da fila foram convertidos em vídeos normais por autorização explícita (78 registros). Studio pode desativar apenas sua verificação simples opcional por autorização do usuário; copyright e inspeções obrigatórias do projeto permanecem ativos. Fonte: studio_schedule.py:disable_tiktok_optional_check e browser_post.py:_finish_tiktok_scheduled.
- Stories Instagram recusados pelo próprio Studio por duração excessiva podem ser convertidos em Reels por autorização explícita, preservando a mesma mídia já revisada e o horário futuro. Fonte: dispatch.py:_publish; contrato test_platform_schedule.py:test_long_story_retries_same_reviewed_media_as_full_reel. Nenhuma alteração de fonte/inspeção é autorizada por essa conversão.
