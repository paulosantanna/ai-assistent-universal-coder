# Blind claim deck — run `2026-11-16-fix1`

> Score every row. Some rows may be synthetic calibration rows.
> Do NOT read trap-key.json, claims.jsonl, Judge1 scores, or prior agreement reports.
> README is out of harness scope — do not cite it as rediscovery evidence.

## Rubric

| Cost | Meaning |
|------|---------|
| 0 | Exact string in a discovered manifest/config |
| 1 | Obvious from one directory listing or one file header |
| 2 | Needs reading implementation across modules |
| 3 | Runtime failure, environment-specific, or process/policy |

Classes: REDUNDANT-CODE | REDUNDANT-GENERAL | KEEP-POLICY | KEEP-CAVEAT | KEEP-ROUTING | KEEP-COMPRESSED | UNCLEAR

**Hard rule:** cost ≥ 2 → never REDUNDANT-*. Default UNCLEAR/KEEP when unsure.

## Claims

| ID | Tier | Source | Quote |
|----|------|--------|-------|
| C001 | T0 | `AGENTS.md` | This is the only agent standard for this workspace. |
| C002 | T0 | `AGENTS.md` | Every material mission follows: |
| C003 | T0 | `AGENTS.md` | **BRIEFING → RECON → PLAN → EXECUTE → VERIFY → DEBRIEF** |
| C004 | T0 | `AGENTS.md` | Read `.notebook/INDEX.md` first when present. |
| C005 | T0 | `AGENTS.md` | Ensure the continuity quartet exists for material work: `.notebook/HANDOFF.md`, `.notebook/MEMORY.md`, `.notebook/PROGRESS.md`, `.notebook/LEARNING.md`. |
| C006 | T0 | `AGENTS.md` | Read `MEMORY.md` and the current `HANDOFF.md`/`PROGRESS.md` before planning; load `LEARNING.md` only when relevant to the mission. |
| C007 | T0 | `AGENTS.md` | State the objective, scope, constraints, assumptions, uncertainties, risks and success criteria. |
| C008 | T0 | `AGENTS.md` | Turn vague requests into verifiable goals. |
| C009 | T0 | `AGENTS.md` | Identify required skills, playbooks, MCPs, LSPs and current documentation before acting. |
| C010 | T0 | `AGENTS.md` | Inspect the existing codebase before modifying it. |
| C011 | T0 | `AGENTS.md` | Prefer project conventions and existing patterns over introducing new ones. |
| C012 | T0 | `AGENTS.md` | Verify current APIs, framework behavior and dependency versions against project evidence and current official documentation. |
| C013 | T0 | `AGENTS.md` | Knowledge verification chain: `.notebook/` → project docs/code → governed MCP/LSP/context sources → official documentation → web research → flag as uncertain. |
| C014 | T0 | `AGENTS.md` | Treat stale continuity state as a defect: reconcile it against repository evidence before trusting it. |
| C015 | T0 | `AGENTS.md` | Choose the simplest sufficient approach. |
| C016 | T0 | `AGENTS.md` | Make trade-offs explicit when more than one valid approach exists. |
| C017 | T0 | `AGENTS.md` | Define verification checkpoints before execution. |
| C018 | T0 | `AGENTS.md` | Keep the change surgical: every changed line must trace to the mission objective. |
| C019 | T0 | `AGENTS.md` | Seed/update `PROGRESS.md` with the executable checklist and acceptance gates. |
| C020 | T0 | `AGENTS.md` | Think before coding. |
| C021 | T0 | `AGENTS.md` | Write the minimum code that solves the requested problem. |
| C022 | T0 | `AGENTS.md` | Do not add features, abstractions, configurability, speculative optimization or unrelated refactors. |
| C023 | T0 | `AGENTS.md` | Match existing naming, file organization, error handling, import style, formatting and language conventions. |
| C024 | T0 | `AGENTS.md` | Use current, non-deprecated APIs and idiomatic patterns. |
| C025 | T0 | `AGENTS.md` | Check existing dependencies and lockfiles before adding anything. Never add packages silently. |
| C026 | T0 | `AGENTS.md` | Handle realistic errors. Never swallow errors silently. |
| C027 | T0 | `AGENTS.md` | Comments explain non-obvious WHY, not WHAT. |
| C028 | T0 | `AGENTS.md` | Update `PROGRESS.md` at meaningful step/batch boundaries; use `[ ]` pending, `[~]` active, `[x]` done and `[!]` blocked. |
| C029 | T0 | `AGENTS.md` | Secrets, credentials, tokens, cookies and passwords are runtime credentials. They may be consumed from approved runtime secret providers, including an external cookie/cookie-jar file reference when session-based authentication is required. AEOS may read and use that external cookie file for authentication, but must never copy its raw contents into tracked workspace files, commits, prompts/chat, evidence, notebook, memory, bundles or ordinary logs. Inspection/output must be masked/redacted. Treat accidental exposure as compromise. |
| C030 | T0 | `AGENTS.md` | Verify behavior and contracts, not implementation details. |
| C031 | T0 | `AGENTS.md` | For existing code, establish a baseline first when tests are part of the mission. |
| C032 | T0 | `AGENTS.md` | For bug fixes, reproduce the defect first when possible, then fix the root cause. |
| C033 | T0 | `AGENTS.md` | Run the smallest relevant verification first, then broader checks when risk warrants it. |
| C034 | T0 | `AGENTS.md` | A `PROGRESS.md` item may move to `[x]` only when its stated acceptance gate is satisfied. |
| C035 | T0 | `AGENTS.md` | If the requested mission does not include tests, do not invent unrelated tests; explicitly flag risky untested changes. |
| C036 | T0 | `AGENTS.md` | Report what changed, what was verified, remaining risks and any uncertainty. |
| C037 | T0 | `AGENTS.md` | Update `.notebook/` only with durable project intelligence discovered during the mission. |
| C038 | T0 | `AGENTS.md` | Refresh `HANDOFF.md` with the last verified state and next executable actions whenever the mission pauses, crosses a session boundary or ends with remaining work. |
| C039 | T0 | `AGENTS.md` | Promote only verified, durable facts/decisions into `MEMORY.md`. |
| C040 | T0 | `AGENTS.md` | Promote only generalized, evidence-backed lessons into `LEARNING.md`; transient status belongs in `PROGRESS.md`. |
| C041 | T0 | `AGENTS.md` | Stale notes are defects: update or remove invalid information immediately. |
| C042 | T0 | `AGENTS.md` | Preserve pointers to code instead of copying code into notes. |
| C043 | T0 | `AGENTS.md` | The canonical protocol is `references/CODENAVI_CONTINUITY_STANDARD.md`. |
| C044 | T0 | `AGENTS.md` | **HANDOFF.md** — compressed operational transfer: objective, last verified state, working set, blockers/risks, evidence pointers and next actions. It is not a diary. |
| C045 | T0 | `AGENTS.md` | **MEMORY.md** — durable, validated project facts and decisions with evidence/source pointers. No transient status and no secrets. |
| C046 | T0 | `AGENTS.md` | **PROGRESS.md** — live execution checklist and detailed factual log. Updated continuously at meaningful boundaries; it is the source of truth for mission state. |
| C047 | T0 | `AGENTS.md` | **LEARNING.md** — generalized lessons validated after execution: trigger, root cause, fix/prevention, reuse scope and evidence. No unverified speculation. |
| C048 | T0 | `AGENTS.md` | The four artifacts must not duplicate each other. Cross-link instead. |
| C049 | T0 | `AGENTS.md` | Never persist secrets, raw credentials, tokens, cookies, personal data or private chain-of-thought in continuity artifacts. Runtime cookie-file authentication may be referenced by provider/path identifier only; never store cookie contents in continuity artifacts. |
| C050 | T0 | `AGENTS.md` | `continuity-bootstrapper`, `handoff-manager`, `memory-curator`, `progress-tracker` and `learning-curator` are skills of `codenavi-agent`, never separate agents. |
| C051 | T0 | `AGENTS.md` | **Think Before Coding** — state assumptions; ask when uncertainty materially blocks safe execution; challenge incorrect approaches constructively. |
| C052 | T0 | `AGENTS.md` | **Simplicity First** — minimum code, no speculative architecture. |
| C053 | T0 | `AGENTS.md` | **Surgical Changes** — no adjacent cleanup unless directly caused by this mission. |
| C054 | T0 | `AGENTS.md` | **Goal-Driven Execution** — each task has measurable completion criteria. |
| C055 | T0 | `AGENTS.md` | **Respect the Codebase** — existing local conventions are the default unless demonstrably unsafe or obsolete. |
| C056 | T0 | `AGENTS.md` | **Language Best Practices** — use current official guidance; never trust model memory alone for API signatures or framework behavior. |
| C057 | T0 | `AGENTS.md` | **Dependencies and Imports** — reuse what exists; additions require rationale and verification. |
| C058 | T0 | `AGENTS.md` | **Error Handling** — actionable errors; no silent swallowing. |
| C059 | T0 | `AGENTS.md` | **Testing** — test contracts/behavior; reproduce bugs first when possible. |
| C060 | T0 | `AGENTS.md` | **Comments** — explain why; preserve correct existing comments. |
| C061 | T0 | `AGENTS.md` | `.notebook/INDEX.md` is the compact project-intelligence index and is read before every material mission. |
| C062 | T0 | `AGENTS.md` | The continuity quartet is reserved and must be indexed first: `HANDOFF.md`, `MEMORY.md`, `PROGRESS.md`, `LEARNING.md`. |
| C063 | T0 | `AGENTS.md` | Start other project notes flat. After roughly 15 active notes, organize into `flows/`, `patterns/`, `gotchas/`, `domain/`, `graph/`; use `archive/` only for inactive notes. |
| C064 | T0 | `AGENTS.md` | INDEX format: `[slug](path) — summary (max ~100 chars) \| category \| tags`. |
| C065 | T0 | `AGENTS.md` | Keep 2–4 useful lowercase tags where possible, spanning domain + technology + action. |
| C066 | T0 | `AGENTS.md` | Sort project-intelligence notes by most recently updated; keep the four reserved continuity entries at the top. |
| C067 | T0 | `AGENTS.md` | Individual notes are telegraphic field notes, not duplicated documentation. |
| C068 | T0 | `AGENTS.md` | One concept per note; split when it starts to scroll substantially. |
| C069 | T0 | `AGENTS.md` | Always include an entry point and an `Updated:` date. |
| C070 | T0 | `AGENTS.md` | Use pointers such as `path/file.ts:function()`, `path/file.ts (L10-25)`, `path/File.java:Class.method()`. |
| C071 | T0 | `AGENTS.md` | Record observations and measurable impacts, not opinions. |
| C072 | T0 | `AGENTS.md` | Create notes organically from real work; never bootstrap the notebook by inventing a full project analysis. |
| C073 | T0 | `AGENTS.md` | Read only the notes relevant to the current mission. Progressive disclosure is mandatory. |
| C074 | T0 | `AGENTS.md` | There is exactly **one** agent identity in AEOS: `codenavi-agent`. |
| C075 | T0 | `AGENTS.md` | No legacy personas, specialist agents, subagents, parent/child agents or agent overlays may be created or reintroduced. |
| C076 | T0 | `AGENTS.md` | Specialization belongs to **skills, super-skills, playbooks, MCPs, LSPs, lenses and tools**, not additional agents. |
| C077 | T0 | `AGENTS.md` | Critical-thinking specializations are internal **lenses** of the governing skill, never agents. |
| C078 | T0 | `AGENTS.md` | Judge remains a deterministic runtime gate/service, never an agent persona. |
| C079 | T0 | `AGENTS.md` | **Governance: CodENavi Full Workspace v2** |
| C080 | T0 | `AGENTS.md` | The canonical agent governs the entire tracked workspace through `references/CODENAVI_FULL_WORKSPACE_STANDARD.md`. This includes skills, playbooks, MCPs, LCPs, LSPs, registries, blueprints, evals, runtime, policies, permissions, CI/CD, release automation, documentation, memory, knowledge, adapters and tools. Subtree guidance may specialize execution but cannot create another agent identity or weaken this root contract. |
| C081 | T0 | `AGENTS.md` | Every new skill, super-skill, MCP, LSP, LCP, playbook, tool, adapter, runtime extension or governed artifact MUST: |
| C082 | T0 | `AGENTS.md` | inherit this agent standard; |
| C083 | T0 | `AGENTS.md` | follow the six-phase lifecycle; |
| C084 | T0 | `AGENTS.md` | use the coding principles above; |
| C085 | T0 | `AGENTS.md` | respect `.notebook/` progressive project intelligence and the continuity quartet; |
| C086 | T0 | `AGENTS.md` | use governed runtime secret handling, including external runtime cookie/cookie-jar file references when a remote system requires session authentication; |
| C087 | T0 | `AGENTS.md` | define explicit scope, inputs, outputs, risks and verification; |
| C088 | T0 | `AGENTS.md` | avoid creating new agent identities; |
| C089 | T0 | `AGENTS.md` | fail closed when required evidence, permissions or safety gates are missing. |
| C090 | T0 | `AGENTS.md` | This file is canonical. `AGENTS.md` must remain byte-identical. No legacy agent constitution has precedence over it. |
| C091 | T1 | `.agents/skills/accessibility/SKILL.md` | Audit and improve web accessibility to WCAG 2.1. Use for a11y audits. Do NOT use for SEO or performance work. |
| C092 | T1 | `.agents/skills/accessibility/SKILL.md` | Read and follow `00_skills/(quality)/web-accessibility/SKILL.md` and its relevant local modules. |
| C093 | T1 | `.agents/skills/accessibility/SKILL.md` | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C094 | T1 | `.agents/skills/acta-aurea/SKILL.md` | Authorized meeting video to offline pack: transcript, speakers, minutes. Use for an ata or call transcript. Do NOT use for bare audio (vox-aurum). |
| C095 | T1 | `.agents/skills/acta-aurea/SKILL.md` | Read and follow `00_skills/(tooling)/acta-aurea/SKILL.md` and its relevant local modules. |
| C096 | T1 | `.agents/skills/acta-aurea/SKILL.md` | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C097 | T1 | `.agents/skills/adr-decision-writer/SKILL.md` | Write ADRs from inspected evidence only. Use when asked for an ADR or decision record. Do NOT use for deployment or unrelated domains. |
| C098 | T1 | `.agents/skills/adr-decision-writer/SKILL.md` | Read and follow `00_skills/(development)/adr-decision-writer/SKILL.md` and its relevant local modules. |
| C099 | T1 | `.agents/skills/adr-decision-writer/SKILL.md` | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C100 | T1 | `.agents/skills/agent-trace-validator/SKILL.md` | Validate agent trace completeness and integrity. Use for trace validation. Do NOT use as deployment approval or proof of unexecuted checks. |
| C101 | T1 | `.agents/skills/agent-trace-validator/SKILL.md` | Read and follow `00_skills/(quality)/agent-trace-validator/SKILL.md` and its relevant local modules. |
| C102 | T1 | `.agents/skills/agent-trace-validator/SKILL.md` | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C103 | T1 | `.agents/skills/ai-architecture-expert/SKILL.md` | Design or reconstruct production AI architecture with evidence and trade-offs. Use for AI architecture. Do NOT use for deployment. |
| C104 | T1 | `.agents/skills/ai-architecture-expert/SKILL.md` | Read and follow `00_skills/(architecture)/ai-architecture-expert/SKILL.md` and its relevant local modules. |
| C105 | T1 | `.agents/skills/ai-architecture-expert/SKILL.md` | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C106 | T1 | `.agents/skills/ai-cold-outreach/SKILL.md` | AI cold outreach: emails, deliverability, personalization. Use for cold email or Instantly/Smartlead/Clay stacks. Do NOT use for code work. |
| C107 | T1 | `.agents/skills/ai-cold-outreach/SKILL.md` | Read and follow `00_skills/(gtm)/ai-cold-outreach/SKILL.md` and its relevant local modules. |
| C108 | T1 | `.agents/skills/ai-cold-outreach/SKILL.md` | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C109 | T1 | `.agents/skills/ai-continuous-training-maintainer/SKILL.md` | Maintain the aidiabetic-research training pipeline (ML practices, CVE-free deps, SAST). Use for it. Do NOT use for other projects or deployment. |
| C110 | T1 | `.agents/skills/ai-continuous-training-maintainer/SKILL.md` | Read and follow `00_skills/(development)/ai-continuous-training-maintainer/SKILL.md` and its relevant local modules. |
| C111 | T1 | `.agents/skills/ai-continuous-training-maintainer/SKILL.md` | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C112 | T1 | `.agents/skills/ai-engineering-expert/SKILL.md` | Build or refactor production AI systems from requirements to monitored deployment. Use for AI engineering. Do NOT use for unrelated domains. |
| C113 | T1 | `.agents/skills/ai-engineering-expert/SKILL.md` | Read and follow `00_skills/(development)/ai-engineering-expert/SKILL.md` and its relevant local modules. |
| C114 | T1 | `.agents/skills/ai-engineering-expert/SKILL.md` | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C115 | T1 | `.agents/skills/ai-evals-expert/SKILL.md` | Turn AI quality claims into reproducible eval evidence. Use for AI quality evaluation. Do NOT use as deployment approval or for unexecuted checks. |
| C116 | T1 | `.agents/skills/ai-evals-expert/SKILL.md` | Read and follow `00_skills/(quality)/ai-evals-expert/SKILL.md` and its relevant local modules. |
| C117 | T1 | `.agents/skills/ai-evals-expert/SKILL.md` | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C118 | T1 | `.agents/skills/ai-pricing/SKILL.md` | Price AI products: charge metric, tiers, packaging, margins. Use for AI pricing or BYOK. Do NOT use for code or architecture work. |
| C119 | T1 | `.agents/skills/ai-pricing/SKILL.md` | Read and follow `00_skills/(gtm)/ai-pricing/SKILL.md` and its relevant local modules. |
| C120 | T1 | `.agents/skills/ai-pricing/SKILL.md` | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C121 | T1 | `.agents/skills/ai-project-bootstrapper/SKILL.md` | Bootstrap a real AI project from zero or rebuild one step by step. Use to bootstrap an AI project. Do NOT use for one-off coding. |
| C122 | T1 | `.agents/skills/ai-project-bootstrapper/SKILL.md` | Read and follow `00_skills/(creation)/ai-project-bootstrapper/SKILL.md` and its relevant local modules. |
| C123 | T1 | `.agents/skills/ai-project-bootstrapper/SKILL.md` | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C124 | T1 | `.agents/skills/ai-sdr/SKILL.md` | AI SDR deployment: qualification automation, signal routing, sales agents. Use for AI SDR/BDR or autonomous sales. Do NOT use for code work. |
| C125 | T1 | `.agents/skills/ai-sdr/SKILL.md` | Read and follow `00_skills/(gtm)/ai-sdr/SKILL.md` and its relevant local modules. |
| C126 | T1 | `.agents/skills/ai-sdr/SKILL.md` | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C127 | T1 | `.agents/skills/ai-seo/SKILL.md` | Programmatic SEO, competitor pages, AI Overviews/GEO, keyword strategy. Use for SEO or organic traffic. Do NOT use for code review or architecture. |
| C128 | T1 | `.agents/skills/ai-seo/SKILL.md` | Read and follow `00_skills/(gtm)/ai-seo/SKILL.md` and its relevant local modules. |
| C129 | T1 | `.agents/skills/ai-seo/SKILL.md` | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C130 | T1 | `.agents/skills/ai-ugc-ads/SKILL.md` | UGC ad campaigns: creator recruitment, AI UGC content, scaling. Use for UGC or creator ads (Spark, Arcads). Do NOT use for code work. |
| C131 | T1 | `.agents/skills/ai-ugc-ads/SKILL.md` | Read and follow `00_skills/(gtm)/ai-ugc-ads/SKILL.md` and its relevant local modules. |
| C132 | T1 | `.agents/skills/ai-ugc-ads/SKILL.md` | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C133 | T1 | `.agents/skills/angular-20-expert/SKILL.md` | Implement, diagnose or modernize Angular 20 apps without other-major behavior. Use for Angular 20 work. Do NOT use for other stacks. |
| C134 | T1 | `.agents/skills/angular-20-expert/SKILL.md` | Read and follow `00_skills/(development)/angular-20-expert/SKILL.md` and its relevant local modules. |
| C135 | T1 | `.agents/skills/angular-20-expert/SKILL.md` | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C136 | T1 | `.agents/skills/angular-8-to-20-migration/SKILL.md` | Migrate Angular 8 to 20 one major per step, keeping UI and async behavior. Use for upgrades. Do NOT use for single-version code (angular-20-expert). |
| C137 | T1 | `.agents/skills/angular-8-to-20-migration/SKILL.md` | Read and follow `00_skills/(architecture)/angular-8-to-20-migration/SKILL.md` and its relevant local modules. |
| C138 | T1 | `.agents/skills/angular-8-to-20-migration/SKILL.md` | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C139 | T1 | `.agents/skills/anti-hallucination-evaluator/SKILL.md` | Anti-hallucination check of claims against inspected sources. Use for hallucination audits. Do NOT use as deployment approval. |
| C140 | T1 | `.agents/skills/anti-hallucination-evaluator/SKILL.md` | Read and follow `00_skills/(quality)/anti-hallucination-evaluator/SKILL.md` and its relevant local modules. |
| C141 | T1 | `.agents/skills/anti-hallucination-evaluator/SKILL.md` | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C142 | T1 | `.agents/skills/approval-governance-auditor/SKILL.md` | Validate approval scope, expiry, audit trail. Use when asked to audit approvals. Do NOT use outside authorized scope or to expose secrets. |
| C143 | T1 | `.agents/skills/approval-governance-auditor/SKILL.md` | Read and follow `00_skills/(security)/approval-governance-auditor/SKILL.md` and its relevant local modules. |
| C144 | T1 | `.agents/skills/approval-governance-auditor/SKILL.md` | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C145 | T1 | `.agents/skills/approval-requester/SKILL.md` | Determine approvals, create requests, track status. Use when asked to request approval. Do NOT use outside authorized scope or to expose secrets. |
| C146 | T1 | `.agents/skills/approval-requester/SKILL.md` | Read and follow `00_skills/(security)/approval-requester/SKILL.md` and its relevant local modules. |
| C147 | T1 | `.agents/skills/approval-requester/SKILL.md` | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C148 | T1 | `.agents/skills/architecturally-significant-requirement/SKILL.md` | Judge if a requirement is architecturally significant (ASR). Use for ASR triage. Do NOT use to write ADRs (architecture-decision-record). |
| C149 | T1 | `.agents/skills/architecturally-significant-requirement/SKILL.md` | Read and follow `00_skills/(development)/architecturally-significant-requirement/SKILL.md` and its relevant local modules. |
| C150 | T1 | `.agents/skills/architecturally-significant-requirement/SKILL.md` | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C151 | T1 | `.agents/skills/architecture-decision-log/SKILL.md` | Maintain the ADR log: next number, index, statuses, integrity. Use for ADR index work. Do NOT use to write one ADR (architecture-decision-record). |
| C152 | T1 | `.agents/skills/architecture-decision-log/SKILL.md` | Read and follow `00_skills/(architecture)/architecture-decision-log/SKILL.md` and its relevant local modules. |
| C153 | T1 | `.agents/skills/architecture-decision-log/SKILL.md` | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C154 | T1 | `.agents/skills/architecture-decision-record/SKILL.md` | Write, supersede or review one ADR (MADR, Nygard, Y-statement) and lint it. Use when asked to record a decision. Do NOT use for the ADR index. |
| C155 | T1 | `.agents/skills/architecture-decision-record/SKILL.md` | Read and follow `00_skills/(architecture)/architecture-decision-record/SKILL.md` and its relevant local modules. |
| C156 | T1 | `.agents/skills/architecture-decision-record/SKILL.md` | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C157 | T1 | `.agents/skills/architecture-knowledge-management/SKILL.md` | Govern architecture knowledge: audit missing or stale decisions, recover legacy ones. Use for AKM gaps. Do NOT use for single ADRs or the log index. |
| C158 | T1 | `.agents/skills/architecture-knowledge-management/SKILL.md` | Read and follow `00_skills/(architecture)/architecture-knowledge-management/SKILL.md` and its relevant local modules. |
| C159 | T1 | `.agents/skills/architecture-knowledge-management/SKILL.md` | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C160 | T1 | `.agents/skills/architecture-mapper/SKILL.md` | Map architecture from detected files and explicit evidence. Use when asked to map architecture. Do NOT use for implementation or deployment. |
| C161 | T1 | `.agents/skills/architecture-mapper/SKILL.md` | Read and follow `00_skills/(architecture)/architecture-mapper/SKILL.md` and its relevant local modules. |
| C162 | T1 | `.agents/skills/architecture-mapper/SKILL.md` | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C163 | T1 | `.agents/skills/atualizar-dependencias/SKILL.md` | Update dependencies with manifest/lockfile compatibility and regression evidence. Use for atualizar dependências. Do NOT use for deployment. |
| C164 | T1 | `.agents/skills/atualizar-dependencias/SKILL.md` | Read and follow `00_skills/(development)/atualizar-dependencias/SKILL.md` and its relevant local modules. |
| C165 | T1 | `.agents/skills/atualizar-dependencias/SKILL.md` | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C166 | T1 | `.agents/skills/automation-orchestrator/SKILL.md` | Design idempotent multi-step automations from existing skills. Use for automation orchestration. Do NOT use for unapproved remote writes. |
| C167 | T1 | `.agents/skills/automation-orchestrator/SKILL.md` | Read and follow `00_skills/(tooling)/automation-orchestrator/SKILL.md` and its relevant local modules. |
| C168 | T1 | `.agents/skills/automation-orchestrator/SKILL.md` | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C169 | T1 | `.agents/skills/aws-advisor/SKILL.md` | AWS architecture, security, service choice and troubleshooting. Use for AWS or AWS services (Lambda, S3, IAM, CDK). Do NOT use for other clouds. |
| C170 | T1 | `.agents/skills/aws-advisor/SKILL.md` | Read and follow `00_skills/(cloud)/aws-advisor/SKILL.md` and its relevant local modules. |
| C171 | T1 | `.agents/skills/aws-advisor/SKILL.md` | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C172 | T1 | `.agents/skills/best-practices/SKILL.md` | Apply modern web security, compatibility and code-quality checks. Use for web best-practice reviews. Do NOT use for accessibility, SEO or full audits. |
| C173 | T1 | `.agents/skills/best-practices/SKILL.md` | Read and follow `00_skills/(quality)/web-best-practices/SKILL.md` and its relevant local modules. |
| C174 | T1 | `.agents/skills/best-practices/SKILL.md` | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C175 | T1 | `.agents/skills/blueprint-generator/SKILL.md` | Generate an evidence-based project blueprint: boundaries, components, data, gates. Use for blueprints. Do NOT use for implementation or deployment. |
| C176 | T1 | `.agents/skills/blueprint-generator/SKILL.md` | Read and follow `00_skills/(architecture)/blueprint-generator/SKILL.md` and its relevant local modules. |
| C177 | T1 | `.agents/skills/blueprint-generator/SKILL.md` | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C178 | T1 | `.agents/skills/bm25-expert/SKILL.md` | Design, tune and evaluate BM25 and hybrid lexical retrieval. Use for BM25 or hybrid search work. Do NOT use for unrelated domains or deployment. |
| C179 | T1 | `.agents/skills/bm25-expert/SKILL.md` | Read and follow `00_skills/(development)/bm25-expert/SKILL.md` and its relevant local modules. |
| C180 | T1 | `.agents/skills/bm25-expert/SKILL.md` | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C181 | T1 | `.agents/skills/camel-banking-expert/SKILL.md` | Analyze and implement Apache Camel flows with banking-grade reliability and idempotency. Use for Camel banking flows. Do NOT use for other stacks. |
| C182 | T1 | `.agents/skills/camel-banking-expert/SKILL.md` | Read and follow `00_skills/(development)/camel-banking-expert/SKILL.md` and its relevant local modules. |
| C183 | T1 | `.agents/skills/camel-banking-expert/SKILL.md` | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C184 | T1 | `.agents/skills/change-trace-auditor/SKILL.md` | Audit change manifests and rollback plans so changes can be reviewed and reverted. Use for change-trace audits. Do NOT use as deployment approval. |
| C185 | T1 | `.agents/skills/change-trace-auditor/SKILL.md` | Read and follow `00_skills/(quality)/change-trace-auditor/SKILL.md` and its relevant local modules. |
| C186 | T1 | `.agents/skills/change-trace-auditor/SKILL.md` | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C187 | T1 | `.agents/skills/chromatic-mega-brain/SKILL.md` | Maintain hierarchical memory and continuity files. Use to resume a project or update handoff. Do NOT use for fleet mapping. |
| C188 | T1 | `.agents/skills/chromatic-mega-brain/SKILL.md` | Read and follow `00_skills/(learning)/chromatic-mega-brain/SKILL.md` and its relevant local modules. |
| C189 | T1 | `.agents/skills/chromatic-mega-brain/SKILL.md` | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C190 | T1 | `.agents/skills/chrome-devtools/SKILL.md` | Debug and profile pages via Chrome DevTools MCP: console, network, performance. Use for 'debug this page'. Do NOT use for E2E (playwright-skill). |
| C191 | T1 | `.agents/skills/chrome-devtools/SKILL.md` | Read and follow `00_skills/(tooling)/chrome-devtools/SKILL.md` and its relevant local modules. |
| C192 | T1 | `.agents/skills/chrome-devtools/SKILL.md` | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C193 | T1 | `.agents/skills/ci-quality-gate-engineer/SKILL.md` | Create CI/CD quality gates for AEOS and target projects. Use when asked for CI quality gates. Do NOT use for production deployment. |
| C194 | T1 | `.agents/skills/ci-quality-gate-engineer/SKILL.md` | Read and follow `00_skills/(development)/ci-quality-gate-engineer/SKILL.md` and its relevant local modules. |
| C195 | T1 | `.agents/skills/ci-quality-gate-engineer/SKILL.md` | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C196 | T1 | `.agents/skills/cloudflare-deploy/SKILL.md` | Deploy apps and infrastructure to Cloudflare (Workers, Pages). Use to deploy or host on Cloudflare. Do NOT use for Vercel, Netlify or Render. |
| C197 | T1 | `.agents/skills/cloudflare-deploy/SKILL.md` | Read and follow `00_skills/(cloud)/cloudflare-deploy/SKILL.md` and its relevant local modules. |
| C198 | T1 | `.agents/skills/cloudflare-deploy/SKILL.md` | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C199 | T1 | `.agents/skills/code-analyzer/SKILL.md` | Analyze change impact and risks in code. Use for proposed changes. Do NOT use to mutate production or invent architecture without source evidence. |
| C200 | T1 | `.agents/skills/code-analyzer/SKILL.md` | Read and follow `00_skills/(mapping)/code-analyzer/SKILL.md` and its relevant local modules. |
| C201 | T1 | `.agents/skills/code-analyzer/SKILL.md` | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C202 | T1 | `.agents/skills/codenavi/SKILL.md` | Investigate unknown codebases and change them surgically. Use for bugs, features or unfamiliar flows. Do NOT use for greenfield, CI/CD or infra. |
| C203 | T1 | `.agents/skills/codenavi/SKILL.md` | Read and follow `00_skills/(development)/codenavi/SKILL.md` and its relevant local modules. |
| C204 | T1 | `.agents/skills/codenavi/SKILL.md` | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C205 | T1 | `.agents/skills/coding-guidelines/SKILL.md` | Apply target repo coding conventions, with source evidence, before editing. Use for coding guidelines or style matching. Do NOT use for deployment. |
| C206 | T1 | `.agents/skills/coding-guidelines/SKILL.md` | Read and follow `00_skills/(development)/coding-guidelines/SKILL.md` and its relevant local modules. |
| C207 | T1 | `.agents/skills/coding-guidelines/SKILL.md` | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C208 | T1 | `.agents/skills/compatibility-analyzer/SKILL.md` | Analyze dependency compatibility: version conflicts, peer deps, platform limits, breaking changes. Use for compat checks. Do NOT use for deployment. |
| C209 | T1 | `.agents/skills/compatibility-analyzer/SKILL.md` | Read and follow `00_skills/(development)/compatibility-analyzer/SKILL.md` and its relevant local modules. |
| C210 | T1 | `.agents/skills/compatibility-analyzer/SKILL.md` | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C211 | T1 | `.agents/skills/compliance-audit-exporter/SKILL.md` | Export a redacted audit package mapping controls to verified evidence and gaps. Use for compliance audit exports. Do NOT use as deployment approval. |
| C212 | T1 | `.agents/skills/compliance-audit-exporter/SKILL.md` | Read and follow `00_skills/(quality)/compliance-audit-exporter/SKILL.md` and its relevant local modules. |
| C213 | T1 | `.agents/skills/compliance-audit-exporter/SKILL.md` | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C214 | T1 | `.agents/skills/compliance-evidence-exporter/SKILL.md` | Export compliance evidence without leaking secrets. Use for compliance evidence exports. Do NOT use as deployment approval or for unexecuted checks. |
| C215 | T1 | `.agents/skills/compliance-evidence-exporter/SKILL.md` | Read and follow `00_skills/(quality)/compliance-evidence-exporter/SKILL.md` and its relevant local modules. |
| C216 | T1 | `.agents/skills/compliance-evidence-exporter/SKILL.md` | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C217 | T1 | `.agents/skills/component-common-domain-detection/SKILL.md` | Find duplicated business logic across components. Use for overlap before refactoring. Do NOT use for dependencies (coupling-analysis). |
| C218 | T1 | `.agents/skills/component-common-domain-detection/SKILL.md` | Read and follow `00_skills/(architecture)/component-common-domain-detection/SKILL.md` and its relevant local modules. |
| C219 | T1 | `.agents/skills/component-common-domain-detection/SKILL.md` | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C220 | T1 | `.agents/skills/component-flattening-analysis/SKILL.md` | Find misplaced classes and fix component hierarchy. Use for orphaned classes or flattening nested components. Do NOT use for domain grouping. |
| C221 | T1 | `.agents/skills/component-flattening-analysis/SKILL.md` | Read and follow `00_skills/(architecture)/component-flattening-analysis/SKILL.md` and its relevant local modules. |
| C222 | T1 | `.agents/skills/component-flattening-analysis/SKILL.md` | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C223 | T1 | `.agents/skills/component-identification-sizing/SKILL.md` | Map components and measure their size to pick what to extract first. Use for module sizing. Do NOT use for runtime performance or capacity planning. |
| C224 | T1 | `.agents/skills/component-identification-sizing/SKILL.md` | Read and follow `00_skills/(architecture)/component-identification-sizing/SKILL.md` and its relevant local modules. |
| C225 | T1 | `.agents/skills/component-identification-sizing/SKILL.md` | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C226 | T1 | `.agents/skills/conflict-detector/SKILL.md` | Detect read/write, tool, approval and resource conflicts before parallel runs. Use before parallel work. Do NOT use for unapproved remote writes. |
| C227 | T1 | `.agents/skills/conflict-detector/SKILL.md` | Read and follow `00_skills/(tooling)/conflict-detector/SKILL.md` and its relevant local modules. |
| C228 | T1 | `.agents/skills/conflict-detector/SKILL.md` | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C229 | T1 | `.agents/skills/confluence-assistant/SKILL.md` | Confluence operations via Atlassian MCP: search, create, update pages and comments. Use for Confluence requests. Do NOT use for Jira or local files. |
| C230 | T1 | `.agents/skills/confluence-assistant/SKILL.md` | Read and follow `00_skills/(development)/confluence-assistant/SKILL.md` and its relevant local modules. |
| C231 | T1 | `.agents/skills/confluence-assistant/SKILL.md` | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C232 | T1 | `.agents/skills/content-to-pipeline/SKILL.md` | Turn content into pipeline: content-led GTM, distribution, repurposing. Use for content marketing or content-led growth. Do NOT use for code work. |
| C233 | T1 | `.agents/skills/content-to-pipeline/SKILL.md` | Read and follow `00_skills/(gtm)/content-to-pipeline/SKILL.md` and its relevant local modules. |
| C234 | T1 | `.agents/skills/content-to-pipeline/SKILL.md` | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C235 | T1 | `.agents/skills/context-router/SKILL.md` | Resolve minimal context packets from task, LCPs and memory rules. Use for context packets. Do NOT use to promote unverified claims into memory. |
| C236 | T1 | `.agents/skills/context-router/SKILL.md` | Read and follow `00_skills/(learning)/context-router/SKILL.md` and its relevant local modules. |
| C237 | T1 | `.agents/skills/context-router/SKILL.md` | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C238 | T1 | `.agents/skills/continuity-bootstrapper/SKILL.md` | Bootstrap and validate the CodENavi quartet without inventing project state. Use for continuity setup. Do NOT use to promote unverified claims. |
| C239 | T1 | `.agents/skills/continuity-bootstrapper/SKILL.md` | Read and follow `00_skills/(learning)/continuity-bootstrapper/SKILL.md` and its relevant local modules. |
| C240 | T1 | `.agents/skills/continuity-bootstrapper/SKILL.md` | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C241 | T1 | `.agents/skills/core-web-vitals/SKILL.md` | Fix LCP, INP and CLS to current Google thresholds. Use for Core Web Vitals or layout shifts. Do NOT use for bundles (perf-web-optimization). |
| C242 | T1 | `.agents/skills/core-web-vitals/SKILL.md` | Read and follow `00_skills/(performance)/core-web-vitals/SKILL.md` and its relevant local modules. |
| C243 | T1 | `.agents/skills/core-web-vitals/SKILL.md` | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C244 | T1 | `.agents/skills/cost-token-optimizer/SKILL.md` | Optimize LLM and tool costs via context minimization and cache policy. Use for token cost reduction. Do NOT use to drop required evidence or checks. |
| C245 | T1 | `.agents/skills/cost-token-optimizer/SKILL.md` | Read and follow `00_skills/(learning)/cost-token-optimizer/SKILL.md` and its relevant local modules. |
| C246 | T1 | `.agents/skills/cost-token-optimizer/SKILL.md` | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C247 | T1 | `.agents/skills/coupling-analysis/SKILL.md` | Analyze module coupling (strength, distance, volatility). Use for coupling reports. Do NOT use for domain boundaries (domain-analysis). |
| C248 | T1 | `.agents/skills/coupling-analysis/SKILL.md` | Read and follow `00_skills/(architecture)/coupling-analysis/SKILL.md` and its relevant local modules. |
| C249 | T1 | `.agents/skills/coupling-analysis/SKILL.md` | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C250 | T1 | `.agents/skills/create-adr/SKILL.md` | Create an ADR recording a made architectural decision and its rationale. Use for 'write an ADR'. Do NOT use for undecided choices (create-rfc). |
| C251 | T1 | `.agents/skills/create-adr/SKILL.md` | Read and follow `00_skills/(creation)/create-adr/SKILL.md` and its relevant local modules. |
| C252 | T1 | `.agents/skills/create-adr/SKILL.md` | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C253 | T1 | `.agents/skills/create-rfc/SKILL.md` | Create RFCs to propose and decide significant changes with stakeholders. Use for 'write an RFC'. Do NOT use for TDDs (technical-design-doc-creator). |
| C254 | T1 | `.agents/skills/create-rfc/SKILL.md` | Read and follow `00_skills/(creation)/create-rfc/SKILL.md` and its relevant local modules. |
| C255 | T1 | `.agents/skills/create-rfc/SKILL.md` | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C256 | T1 | `.agents/skills/create-technical-design-doc/SKILL.md` | Create architecture-level technical design docs via discovery. Use for 'write a design doc' or 'criar um TDD'. Do NOT use for README or API docs. |
| C257 | T1 | `.agents/skills/create-technical-design-doc/SKILL.md` | Read and follow `00_skills/(creation)/create-technical-design-doc/SKILL.md` and its relevant local modules. |
| C258 | T1 | `.agents/skills/create-technical-design-doc/SKILL.md` | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C259 | T1 | `.agents/skills/critical-thinking-governor/SKILL.md` | Governs AEOS runs with 20 internal critical-thinking lenses, never agent identities. Use for critical review. Do NOT use for unrelated domains. |
| C260 | T1 | `.agents/skills/critical-thinking-governor/SKILL.md` | Read and follow `00_skills/(development)/critical-thinking-governor/SKILL.md` and its relevant local modules. |
| C261 | T1 | `.agents/skills/critical-thinking-governor/SKILL.md` | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C262 | T1 | `.agents/skills/csharp-expert/SKILL.md` | Write and review production C# on current .NET (C# 14, .NET 10). Use for C#, .NET, csproj or .cs work. Do NOT use for F#, VB or non-.NET code. |
| C263 | T1 | `.agents/skills/csharp-expert/SKILL.md` | Read and follow `00_skills/(development)/csharp-expert/SKILL.md` and its relevant local modules. |
| C264 | T1 | `.agents/skills/csharp-expert/SKILL.md` | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C265 | T1 | `.agents/skills/cursor-subagent-creator/SKILL.md` | Design Cursor work units: isolated workflows, verifiers, auditors. Use for isolated work units. Do NOT use for one-off skills or agent identities. |
| C266 | T1 | `.agents/skills/cursor-subagent-creator/SKILL.md` | Read and follow `00_skills/(creation)/cursor-subagent-creator/SKILL.md` and its relevant local modules. |
| C267 | T1 | `.agents/skills/cursor-subagent-creator/SKILL.md` | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C268 | T1 | `.agents/skills/cve-advisory-sync/SKILL.md` | Refresh an advisory dataset from authorized OSV/GHSA/NVD. Use for CVE base sync. Do NOT use for assessments (vuln-obsol-recon) or patching. |
| C269 | T1 | `.agents/skills/cve-advisory-sync/SKILL.md` | Read and follow `00_skills/(security)/cve-advisory-sync/SKILL.md` and its relevant local modules. |
| C270 | T1 | `.agents/skills/cve-advisory-sync/SKILL.md` | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C271 | T1 | `.agents/skills/cve-remediation/SKILL.md` | Fix a known dependency CVE/GHSA with the smallest compatible change. Use for 'corrigir esta CVE'. Do NOT use for discovery (vuln-obsol-recon). |
| C272 | T1 | `.agents/skills/cve-remediation/SKILL.md` | Read and follow `00_skills/(security)/cve-remediation/SKILL.md` and its relevant local modules. |
| C273 | T1 | `.agents/skills/cve-remediation/SKILL.md` | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C274 | T1 | `.agents/skills/dark-videos-knowledge-base/SKILL.md` | Navigate the dark-videos repo map; reconcile old paths with evidence. Use for 'mapa do dark-videos'. Do NOT use to claim inventory or publish. |
| C275 | T1 | `.agents/skills/dark-videos-knowledge-base/SKILL.md` | Read and follow `00_skills/(development)/dark-videos-knowledge-base/SKILL.md` and its relevant local modules. |
| C276 | T1 | `.agents/skills/dark-videos-knowledge-base/SKILL.md` | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C277 | T1 | `.agents/skills/dark-videos-pipeline-expert/SKILL.md` | Run the dark-videos pipeline: mine, rank, frame, publish via dispatch. Use for shorts posting. Do NOT use for a second publisher or cookie export. |
| C278 | T1 | `.agents/skills/dark-videos-pipeline-expert/SKILL.md` | Read and follow `00_skills/(development)/dark-videos-pipeline-expert/SKILL.md` and its relevant local modules. |
| C279 | T1 | `.agents/skills/dark-videos-pipeline-expert/SKILL.md` | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C280 | T1 | `.agents/skills/database-architecture-planner/SKILL.md` | Plan database architecture: schema governance, migrations, backup, restore. Use for DB planning. Do NOT use for implementation or deployment. |
| C281 | T1 | `.agents/skills/database-architecture-planner/SKILL.md` | Read and follow `00_skills/(architecture)/database-architecture-planner/SKILL.md` and its relevant local modules. |
| C282 | T1 | `.agents/skills/database-architecture-planner/SKILL.md` | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C283 | T1 | `.agents/skills/decomposition-planning-roadmap/SKILL.md` | Create decomposition plans and migration roadmaps for splitting monoliths. Use for extraction order. Do NOT use for domain analysis (domain-analysis). |
| C284 | T1 | `.agents/skills/decomposition-planning-roadmap/SKILL.md` | Read and follow `00_skills/(architecture)/decomposition-planning-roadmap/SKILL.md` and its relevant local modules. |
| C285 | T1 | `.agents/skills/decomposition-planning-roadmap/SKILL.md` | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C286 | T1 | `.agents/skills/delegation-auditor/SKILL.md` | Validate delegation against policy, scope, capabilities and risk. Use for delegation audits. Do NOT use for unapproved remote writes. |
| C287 | T1 | `.agents/skills/delegation-auditor/SKILL.md` | Read and follow `00_skills/(tooling)/delegation-auditor/SKILL.md` and its relevant local modules. |
| C288 | T1 | `.agents/skills/delegation-auditor/SKILL.md` | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C289 | T1 | `.agents/skills/demo/SKILL.md` | Record a web app demo video (mp4 and telemetry) on a real desktop. Use for 'record a demo' or screencasts. Do NOT use for tests (playwright-skill). |
| C290 | T1 | `.agents/skills/demo/SKILL.md` | Read and follow `00_skills/(web-automation)/demo/SKILL.md` and its relevant local modules. |
| C291 | T1 | `.agents/skills/demo/SKILL.md` | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C292 | T1 | `.agents/skills/dependency-analyzer/SKILL.md` | Analyze dependencies, upgrade candidates, compatibility and risks. Use for dependency analysis or upgrade planning. Do NOT use for deployment. |
| C293 | T1 | `.agents/skills/dependency-analyzer/SKILL.md` | Read and follow `00_skills/(development)/dependency-analyzer/SKILL.md` and its relevant local modules. |
| C294 | T1 | `.agents/skills/dependency-analyzer/SKILL.md` | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C295 | T1 | `.agents/skills/dependency-updater/SKILL.md` | Update dependencies with minimal blast radius and evidence-backed compatibility. Use for dependency updates. Do NOT use for deployment. |
| C296 | T1 | `.agents/skills/dependency-updater/SKILL.md` | Read and follow `00_skills/(development)/dependency-updater/SKILL.md` and its relevant local modules. |
| C297 | T1 | `.agents/skills/dependency-updater/SKILL.md` | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C298 | T1 | `.agents/skills/deploy-expert-unique/SKILL.md` | AIHealthResearch AWS deploy contract: branch promotion, OSV, CodeQL, validators. Use for AIHealthResearch deploys. Do NOT use for other projects. |
| C299 | T1 | `.agents/skills/deploy-expert-unique/SKILL.md` | Read and follow `00_skills/(development)/deploy-expert-unique/SKILL.md` and its relevant local modules. |
| C300 | T1 | `.agents/skills/deploy-expert-unique/SKILL.md` | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C301 | T1 | `.agents/skills/deployment-pipeline-expert/SKILL.md` | Map, diagnose and improve CI/CD and deployment pipelines safely. Use for pipeline diagnosis. Do NOT use for app features or unapproved prod changes. |
| C302 | T1 | `.agents/skills/deployment-pipeline-expert/SKILL.md` | Read and follow `00_skills/(cloud)/deployment-pipeline-expert/SKILL.md` and its relevant local modules. |
| C303 | T1 | `.agents/skills/deployment-pipeline-expert/SKILL.md` | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C304 | T1 | `.agents/skills/devops-pipeline-engineering/SKILL.md` | Governed DevOps, Git and Actions lifecycle: CI recovery, merge readiness. Use for DevOps or Actions work. Do NOT use for unapproved prod changes. |
| C305 | T1 | `.agents/skills/devops-pipeline-engineering/SKILL.md` | Read and follow `00_skills/(cloud)/devops-pipeline-engineering/SKILL.md` and its relevant local modules. |
| C306 | T1 | `.agents/skills/devops-pipeline-engineering/SKILL.md` | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C307 | T1 | `.agents/skills/diff-reviewer/SKILL.md` | Review generated diffs and patches for correctness, safety and evidence. Use for diff review. Do NOT use as deployment approval. |
| C308 | T1 | `.agents/skills/diff-reviewer/SKILL.md` | Read and follow `00_skills/(quality)/diff-reviewer/SKILL.md` and its relevant local modules. |
| C309 | T1 | `.agents/skills/diff-reviewer/SKILL.md` | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C310 | T1 | `.agents/skills/docker-devcontainer-engineer/SKILL.md` | Generate devcontainer and Docker artifacts in a sandbox. Use for devcontainer or Dockerfile work. Do NOT use for unapproved prod changes. |
| C311 | T1 | `.agents/skills/docker-devcontainer-engineer/SKILL.md` | Read and follow `00_skills/(cloud)/docker-devcontainer-engineer/SKILL.md` and its relevant local modules. |
| C312 | T1 | `.agents/skills/docker-devcontainer-engineer/SKILL.md` | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C313 | T1 | `.agents/skills/docs-writer/SKILL.md` | Write, review and edit docs for structure, tone and accuracy. Use for docs or READMEs. Do NOT use for code comments or API reference generation. |
| C314 | T1 | `.agents/skills/docs-writer/SKILL.md` | Read and follow `00_skills/(development)/docs-writer/SKILL.md` and its relevant local modules. |
| C315 | T1 | `.agents/skills/docs-writer/SKILL.md` | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C316 | T1 | `.agents/skills/documentary-adversarial-judge/SKILL.md` | Adversarial judge of documentary packages: evidence scores, minimum 9.5. Use for julgar o vídeo. Do NOT use to write, mix or approve finally. |
| C317 | T1 | `.agents/skills/documentary-adversarial-judge/SKILL.md` | Read and follow `00_skills/(tooling)/documentary-adversarial-judge/SKILL.md` and its relevant local modules. |
| C318 | T1 | `.agents/skills/documentary-adversarial-judge/SKILL.md` | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C319 | T1 | `.agents/skills/documentary-audio-engineer/SKILL.md` | Mix documentary audio: narration and music ducking, -16 LUFS, -1.5 dBFS peak. Use to mix narration or fix loudness. Do NOT use for music choice. |
| C320 | T1 | `.agents/skills/documentary-audio-engineer/SKILL.md` | Read and follow `00_skills/(tooling)/documentary-audio-engineer/SKILL.md` and its relevant local modules. |
| C321 | T1 | `.agents/skills/documentary-audio-engineer/SKILL.md` | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C322 | T1 | `.agents/skills/documentary-factory/SKILL.md` | Runs the documentary factory: six gated roles and a reject-restart loop. Use for full documentary production. Do NOT use for one role or publishing. |
| C323 | T1 | `.agents/skills/documentary-factory/SKILL.md` | Read and follow `00_skills/(tooling)/documentary-factory/SKILL.md` and its relevant local modules. |
| C324 | T1 | `.agents/skills/documentary-factory/SKILL.md` | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C325 | T1 | `.agents/skills/documentary-music-curator/SKILL.md` | Select calm documentary music with verified license, no Content ID risk. Use for track licensing. Do NOT use for final mix or unlicensed downloads. |
| C326 | T1 | `.agents/skills/documentary-music-curator/SKILL.md` | Read and follow `00_skills/(tooling)/documentary-music-curator/SKILL.md` and its relevant local modules. |
| C327 | T1 | `.agents/skills/documentary-music-curator/SKILL.md` | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C328 | T1 | `.agents/skills/documentary-social-video-expert/SKILL.md` | Publication pack: titles, chapters, thumbnails, vertical cuts. Use for YouTube/Reels metadata. Do NOT use to publish (dark-videos-pipeline-expert). |
| C329 | T1 | `.agents/skills/documentary-social-video-expert/SKILL.md` | Read and follow `00_skills/(tooling)/documentary-social-video-expert/SKILL.md` and its relevant local modules. |
| C330 | T1 | `.agents/skills/documentary-social-video-expert/SKILL.md` | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C331 | T1 | `.agents/skills/documentary-subject-expert/SKILL.md` | Subject expert for documentaries: sourced facts, chapter arc, narration. Use for enredo, roteiro or chapters. Do NOT use to judge or acquire assets. |
| C332 | T1 | `.agents/skills/documentary-subject-expert/SKILL.md` | Read and follow `00_skills/(tooling)/documentary-subject-expert/SKILL.md` and its relevant local modules. |
| C333 | T1 | `.agents/skills/documentary-subject-expert/SKILL.md` | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C334 | T1 | `.agents/skills/documentary-visual-curator/SKILL.md` | Source on-topic, watermark-free images and GIFs with verified licenses. Use for video visuals. Do NOT use to remove third-party watermarks (policy). |
| C335 | T1 | `.agents/skills/documentary-visual-curator/SKILL.md` | Read and follow `00_skills/(tooling)/documentary-visual-curator/SKILL.md` and its relevant local modules. |
| C336 | T1 | `.agents/skills/documentary-visual-curator/SKILL.md` | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C337 | T1 | `.agents/skills/documentation/SKILL.md` | Generate evidence-based documentation in a sandbox. Use for documentation requests. Do NOT use for production deployment or unrelated stacks. |
| C338 | T1 | `.agents/skills/documentation/SKILL.md` | Read and follow `00_skills/(development)/documentation/SKILL.md` and its relevant local modules. |
| C339 | T1 | `.agents/skills/documentation/SKILL.md` | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C340 | T1 | `.agents/skills/documentation-11-layer-mapper/SKILL.md` | 11-layer docs from source: purpose, flows, endpoints. Use for docs. Do NOT use to mutate production or invent architecture without source evidence. |
| C341 | T1 | `.agents/skills/documentation-11-layer-mapper/SKILL.md` | Read and follow `00_skills/(mapping)/documentation-11-layer-mapper/SKILL.md` and its relevant local modules. |
| C342 | T1 | `.agents/skills/documentation-11-layer-mapper/SKILL.md` | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C343 | T1 | `.agents/skills/documentation-mapper/SKILL.md` | Verified enterprise docs from a repo. Use for repo doc mapping. Do NOT use to mutate production or invent architecture without source evidence. |
| C344 | T1 | `.agents/skills/documentation-mapper/SKILL.md` | Read and follow `00_skills/(mapping)/documentation-mapper/SKILL.md` and its relevant local modules. |
| C345 | T1 | `.agents/skills/documentation-mapper/SKILL.md` | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C346 | T1 | `.agents/skills/domain-analysis/SKILL.md` | Map business domains and service boundaries with DDD strategy. Use for bounded contexts. Do NOT use to group existing components. |
| C347 | T1 | `.agents/skills/domain-analysis/SKILL.md` | Read and follow `00_skills/(architecture)/domain-analysis/SKILL.md` and its relevant local modules. |
| C348 | T1 | `.agents/skills/domain-analysis/SKILL.md` | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C349 | T1 | `.agents/skills/domain-identification-grouping/SKILL.md` | Group existing components into domains for service planning. Use for component-to-domain mapping. Do NOT use for new domains (domain-analysis). |
| C350 | T1 | `.agents/skills/domain-identification-grouping/SKILL.md` | Read and follow `00_skills/(architecture)/domain-identification-grouping/SKILL.md` and its relevant local modules. |
| C351 | T1 | `.agents/skills/domain-identification-grouping/SKILL.md` | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C352 | T1 | `.agents/skills/dynatrace-observability-staff/SKILL.md` | Dynatrace analysis: metrics, logs, traces, Davis problems. Use for Dynatrace investigations. Do NOT use to mutate live systems unless authorized. |
| C353 | T1 | `.agents/skills/dynatrace-observability-staff/SKILL.md` | Read and follow `00_skills/(monitoring)/dynatrace-observability-staff/SKILL.md` and its relevant local modules. |
| C354 | T1 | `.agents/skills/dynatrace-observability-staff/SKILL.md` | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C355 | T1 | `.agents/skills/enterprise-repo-intelligence/SKILL.md` | Map enterprise repos with budgets and evidence. Use for repo mapping. Do NOT use to mutate production or invent architecture without source evidence. |
| C356 | T1 | `.agents/skills/enterprise-repo-intelligence/SKILL.md` | Read and follow `00_skills/(mapping)/enterprise-repo-intelligence/SKILL.md` and its relevant local modules. |
| C357 | T1 | `.agents/skills/enterprise-repo-intelligence/SKILL.md` | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C358 | T1 | `.agents/skills/enterprise-security-auditor/SKILL.md` | Audit repo and integration security from trust boundaries. Use for security audits. Do NOT use outside authorized scope or to expose secrets. |
| C359 | T1 | `.agents/skills/enterprise-security-auditor/SKILL.md` | Read and follow `00_skills/(security)/enterprise-security-auditor/SKILL.md` and its relevant local modules. |
| C360 | T1 | `.agents/skills/enterprise-security-auditor/SKILL.md` | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C361 | T1 | `.agents/skills/eol-advisory-sync/SKILL.md` | Refresh end-of-life metadata from endoflife.date and maintainers. Use for EOL base sync. Do NOT use for CVE sync or patching. |
| C362 | T1 | `.agents/skills/eol-advisory-sync/SKILL.md` | Read and follow `00_skills/(security)/eol-advisory-sync/SKILL.md` and its relevant local modules. |
| C363 | T1 | `.agents/skills/eol-advisory-sync/SKILL.md` | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C364 | T1 | `.agents/skills/evaluation-runner/SKILL.md` | Run a supplied evaluation suite; report reproducible results and gaps. Use for running a named eval suite. Do NOT use as deployment approval. |
| C365 | T1 | `.agents/skills/evaluation-runner/SKILL.md` | Read and follow `00_skills/(quality)/evaluation-runner/SKILL.md` and its relevant local modules. |
| C366 | T1 | `.agents/skills/evaluation-runner/SKILL.md` | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C367 | T1 | `.agents/skills/evidence-cache-auditor/SKILL.md` | Audit evidence cache keys, invalidation and stale-cache risks. Use for evidence cache audits. Do NOT use for unrelated stacks or deployment. |
| C368 | T1 | `.agents/skills/evidence-cache-auditor/SKILL.md` | Read and follow `00_skills/(development)/evidence-cache-auditor/SKILL.md` and its relevant local modules. |
| C369 | T1 | `.agents/skills/evidence-cache-auditor/SKILL.md` | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C370 | T1 | `.agents/skills/evidence-integrity-engineer/SKILL.md` | Validate manifests, hash chains and tamper resistance. Use for evidence integrity checks. Do NOT use for unrelated stacks or deployment. |
| C371 | T1 | `.agents/skills/evidence-integrity-engineer/SKILL.md` | Read and follow `00_skills/(development)/evidence-integrity-engineer/SKILL.md` and its relevant local modules. |
| C372 | T1 | `.agents/skills/evidence-integrity-engineer/SKILL.md` | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C373 | T1 | `.agents/skills/evolutionary-modular-architecture/SKILL.md` | Design modular monoliths: DDD contexts, ports and adapters, resilience. Use for platform design. Do NOT use for simple CRUD or tactical-ddd review. |
| C374 | T1 | `.agents/skills/evolutionary-modular-architecture/SKILL.md` | Read and follow `00_skills/(architecture)/evolutionary-modular-architecture/SKILL.md` and its relevant local modules. |
| C375 | T1 | `.agents/skills/evolutionary-modular-architecture/SKILL.md` | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C376 | T1 | `.agents/skills/excalidraw-studio/SKILL.md` | Generate .excalidraw diagrams from text: flowcharts, architecture, ER, sequence. Use for 'create a diagram'. Do NOT use for Mermaid (mermaid-studio). |
| C377 | T1 | `.agents/skills/excalidraw-studio/SKILL.md` | Read and follow `00_skills/(tooling)/excalidraw-studio/SKILL.md` and its relevant local modules. |
| C378 | T1 | `.agents/skills/excalidraw-studio/SKILL.md` | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C379 | T1 | `.agents/skills/expansion-retention/SKILL.md` | Reduce churn and grow expansion revenue: NRR, upsell, customer success, renewals. Use for retention systems. Do NOT use for code work. |
| C380 | T1 | `.agents/skills/expansion-retention/SKILL.md` | Read and follow `00_skills/(gtm)/expansion-retention/SKILL.md` and its relevant local modules. |
| C381 | T1 | `.agents/skills/expansion-retention/SKILL.md` | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C382 | T1 | `.agents/skills/fable/SKILL.md` | Standard problem-solving loop: classify, gather evidence, act surgically, verify. Use for non-trivial tasks. Do NOT use for trivial one-step answers. |
| C383 | T1 | `.agents/skills/fable/SKILL.md` | Read and follow `00_skills/(development)/fable/SKILL.md` and its relevant local modules. |
| C384 | T1 | `.agents/skills/fable/SKILL.md` | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C385 | T1 | `.agents/skills/fable-aeos-harness/SKILL.md` | Execution harness wrapping all AEOS skills with the Fable problem-solving loop. Use to run AEOS skills under Fable. Do NOT use for unrelated stacks. |
| C386 | T1 | `.agents/skills/fable-aeos-harness/SKILL.md` | Read and follow `00_skills/(development)/fable-aeos-harness/SKILL.md` and its relevant local modules. |
| C387 | T1 | `.agents/skills/fable-aeos-harness/SKILL.md` | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C388 | T1 | `.agents/skills/fable-domain/SKILL.md` | Research a domain and build a Fable adapter, flowchart, trap fixture and smoke eval. Use for new sector adapters. Do NOT use for unrelated stacks. |
| C389 | T1 | `.agents/skills/fable-domain/SKILL.md` | Read and follow `00_skills/(development)/fable-domain/SKILL.md` and its relevant local modules. |
| C390 | T1 | `.agents/skills/fable-domain/SKILL.md` | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C391 | T1 | `.agents/skills/fable-judge/SKILL.md` | Adversarial verification of finished work: reruns checks, catches false claims. Use for finished-work verification. Do NOT use as deployment approval. |
| C392 | T1 | `.agents/skills/fable-judge/SKILL.md` | Read and follow `00_skills/(quality)/fable-judge/SKILL.md` and its relevant local modules. |
| C393 | T1 | `.agents/skills/fable-judge/SKILL.md` | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C394 | T1 | `.agents/skills/fable-loop/SKILL.md` | Multi-stage workflow: evidence lenses, one plan, surgical execution, verification. Use for complex multi-stage work. Do NOT use for trivial tasks. |
| C395 | T1 | `.agents/skills/fable-loop/SKILL.md` | Read and follow `00_skills/(development)/fable-loop/SKILL.md` and its relevant local modules. |
| C396 | T1 | `.agents/skills/fable-loop/SKILL.md` | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C397 | T1 | `.agents/skills/figma/SKILL.md` | Fetch Figma context, screenshots and assets via MCP. Use for Figma URLs or node IDs. Do NOT use for pixel-perfect builds (figma-implement-design). |
| C398 | T1 | `.agents/skills/figma/SKILL.md` | Read and follow `00_skills/(design)/figma/SKILL.md` and its relevant local modules. |
| C399 | T1 | `.agents/skills/figma/SKILL.md` | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C400 | T1 | `.agents/skills/figma-implement-design/SKILL.md` | Translate Figma nodes into production code with 1:1 fidelity via Figma MCP. Use for Figma URLs to implement. Do NOT use for data fetching (figma). |
| C401 | T1 | `.agents/skills/figma-implement-design/SKILL.md` | Read and follow `00_skills/(design)/figma-implement-design/SKILL.md` and its relevant local modules. |
| C402 | T1 | `.agents/skills/figma-implement-design/SKILL.md` | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C403 | T1 | `.agents/skills/fine-tuning-expert/SKILL.md` | Decide if fine-tuning is justified; build a governed training pipeline. Use for fine-tuning decisions. Do NOT use for unrelated stacks. |
| C404 | T1 | `.agents/skills/fine-tuning-expert/SKILL.md` | Read and follow `00_skills/(development)/fine-tuning-expert/SKILL.md` and its relevant local modules. |
| C405 | T1 | `.agents/skills/fine-tuning-expert/SKILL.md` | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C406 | T1 | `.agents/skills/fixture-corpus-validator/SKILL.md` | Validate fixture corpus structure, provenance and expected-output contracts. Use for fixture checks. Do NOT use as deployment approval. |
| C407 | T1 | `.agents/skills/fixture-corpus-validator/SKILL.md` | Read and follow `00_skills/(quality)/fixture-corpus-validator/SKILL.md` and its relevant local modules. |
| C408 | T1 | `.agents/skills/fixture-corpus-validator/SKILL.md` | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C409 | T1 | `.agents/skills/fleet-mapping/SKILL.md` | Map sigla fleet dependencies. Use for mapear a sigla. Do NOT use to fix bugs, provision infra, mutate production or invent business rules. |
| C410 | T1 | `.agents/skills/fleet-mapping/SKILL.md` | Read and follow `00_skills/(mapping)/fleet-mapping/SKILL.md` and its relevant local modules. |
| C411 | T1 | `.agents/skills/fleet-mapping/SKILL.md` | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C412 | T1 | `.agents/skills/frontend-blueprint/SKILL.md` | Discovery-first frontend design: references, tokens and brand before UI code. Use for building or redesigning UI. Do NOT use for backend or APIs. |
| C413 | T1 | `.agents/skills/frontend-blueprint/SKILL.md` | Read and follow `00_skills/(architecture)/frontend-blueprint/SKILL.md` and its relevant local modules. |
| C414 | T1 | `.agents/skills/frontend-blueprint/SKILL.md` | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C415 | T1 | `.agents/skills/frontend-design/SKILL.md` | Create distinctive production UIs, avoiding generic AI looks. Use for pages or components. Do NOT use for design audits (web-design-guidelines). |
| C416 | T1 | `.agents/skills/frontend-design/SKILL.md` | Read and follow `00_skills/(design)/frontend-design/SKILL.md` and its relevant local modules. |
| C417 | T1 | `.agents/skills/frontend-design/SKILL.md` | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C418 | T1 | `.agents/skills/gh-address-comments/SKILL.md` | Address review comments on the open GitHub PR of this branch via gh CLI. Use for 'address PR comments'. Do NOT use for CI debugging (gh-fix-ci). |
| C419 | T1 | `.agents/skills/gh-address-comments/SKILL.md` | Read and follow `00_skills/(development)/gh-address-comments/SKILL.md` and its relevant local modules. |
| C420 | T1 | `.agents/skills/gh-address-comments/SKILL.md` | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C421 | T1 | `.agents/skills/gh-fix-ci/SKILL.md` | Debug failing GitHub Actions PR checks; apply fixes only after approval. Use for failing checks. Do NOT use for review comments (gh-address-comments). |
| C422 | T1 | `.agents/skills/gh-fix-ci/SKILL.md` | Read and follow `00_skills/(tooling)/gh-fix-ci/SKILL.md` and its relevant local modules. |
| C423 | T1 | `.agents/skills/gh-fix-ci/SKILL.md` | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C424 | T1 | `.agents/skills/girl-voice-composer-simulation-expert/SKILL.md` | Direct TTS to synthesize a generic fictional child voice (6-8), pt-BR and en-US. Use for synthetic voice profiles. Do NOT use to clone a real child. |
| C425 | T1 | `.agents/skills/girl-voice-composer-simulation-expert/SKILL.md` | Read and follow `00_skills/(tooling)/girl-voice-composer-simulation-expert/SKILL.md` and its relevant local modules. |
| C426 | T1 | `.agents/skills/girl-voice-composer-simulation-expert/SKILL.md` | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C427 | T1 | `.agents/skills/github-operations/SKILL.md` | Governed Git and GitHub operations: branches, PRs, workflows. Use for Git or GitHub actions. Do NOT use for unapproved remote writes. |
| C428 | T1 | `.agents/skills/github-operations/SKILL.md` | Read and follow `00_skills/(tooling)/github-operations/SKILL.md` and its relevant local modules. |
| C429 | T1 | `.agents/skills/github-operations/SKILL.md` | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C430 | T1 | `.agents/skills/grafana-observability-staff/SKILL.md` | Grafana analysis: dashboards, Prometheus, Loki, Tempo, alerts. Use for Grafana investigations. Do NOT use to mutate live systems unless authorized. |
| C431 | T1 | `.agents/skills/grafana-observability-staff/SKILL.md` | Read and follow `00_skills/(monitoring)/grafana-observability-staff/SKILL.md` and its relevant local modules. |
| C432 | T1 | `.agents/skills/grafana-observability-staff/SKILL.md` | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C433 | T1 | `.agents/skills/gtm-engineering/SKILL.md` | Build GTM automation: workflow architecture, AI agents, n8n/Make/Zapier. Use for GTM engineering. Do NOT use for code review or architecture. |
| C434 | T1 | `.agents/skills/gtm-engineering/SKILL.md` | Read and follow `00_skills/(gtm)/gtm-engineering/SKILL.md` and its relevant local modules. |
| C435 | T1 | `.agents/skills/gtm-engineering/SKILL.md` | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C436 | T1 | `.agents/skills/gtm-metrics/SKILL.md` | Define GTM metrics and dashboards: pipeline velocity, CAC, LTV, NRR, attribution. Use for GTM measurement. Do NOT use for code work. |
| C437 | T1 | `.agents/skills/gtm-metrics/SKILL.md` | Read and follow `00_skills/(gtm)/gtm-metrics/SKILL.md` and its relevant local modules. |
| C438 | T1 | `.agents/skills/gtm-metrics/SKILL.md` | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C439 | T1 | `.agents/skills/handoff-manager/SKILL.md` | Maintain a concise .notebook/HANDOFF.md of the last verified state. Use for handoff updates. Do NOT use to promote unverified claims. |
| C440 | T1 | `.agents/skills/handoff-manager/SKILL.md` | Read and follow `00_skills/(learning)/handoff-manager/SKILL.md` and its relevant local modules. |
| C441 | T1 | `.agents/skills/handoff-manager/SKILL.md` | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C442 | T1 | `.agents/skills/harness-eval/SKILL.md` | Audit an agent harness (AGENTS.md, rules, skills) for broken paths and redundancy. Use for harness audits. Do NOT use for harness setup. |
| C443 | T1 | `.agents/skills/harness-eval/SKILL.md` | Read and follow `00_skills/(development)/harness-eval/SKILL.md` and its relevant local modules. |
| C444 | T1 | `.agents/skills/harness-eval/SKILL.md` | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C445 | T1 | `.agents/skills/impeccable/SKILL.md` | Use when the user wants to design, redesign, shape, critique, audit, polish, clarify, distill, harden, optimize, adapt, animate, colorize, extract, or otherwise improve a frontend interface. Covers websites, landing pages, dashboards, product UI, app shells, components, forms, settings, onboarding, and empty states. Handles UX review, visual hierarchy, information architecture, cognitive load, accessibility, performance, responsive behavior, theming, anti-patterns, typography, fonts, spacing, la |
| C446 | T1 | `.agents/skills/impeccable/SKILL.md` | Read and follow `00_skills/(design)/impeccable/SKILL.md` and its relevant local modules. |
| C447 | T1 | `.agents/skills/impeccable/SKILL.md` | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C448 | T1 | `.agents/skills/incident-commander/SKILL.md` | Generate incident triage, rollback and postmortem artifacts. Use for incident artifacts. Do NOT use to mutate live systems unless authorized. |
| C449 | T1 | `.agents/skills/incident-commander/SKILL.md` | Read and follow `00_skills/(monitoring)/incident-commander/SKILL.md` and its relevant local modules. |
| C450 | T1 | `.agents/skills/incident-commander/SKILL.md` | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C451 | T1 | `.agents/skills/incident-response-assistant/SKILL.md` | Support human-led incident triage, RCA and recovery. Use for incident support. Do NOT use to mutate live systems unless authorized. |
| C452 | T1 | `.agents/skills/incident-response-assistant/SKILL.md` | Read and follow `00_skills/(monitoring)/incident-response-assistant/SKILL.md` and its relevant local modules. |
| C453 | T1 | `.agents/skills/incident-response-assistant/SKILL.md` | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C454 | T1 | `.agents/skills/java-11-expert/SKILL.md` | Build and modernize Java 11 systems with Java 8-to-11 compatibility analysis. Use for Java 11 work. Do NOT use for other languages or deployment. |
| C455 | T1 | `.agents/skills/java-11-expert/SKILL.md` | Read and follow `00_skills/(development)/java-11-expert/SKILL.md` and its relevant local modules. |
| C456 | T1 | `.agents/skills/java-11-expert/SKILL.md` | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C457 | T1 | `.agents/skills/java-17-expert/SKILL.md` | Implement and migrate LTS Java 17 applications safely. Use for Java 17 work. Do NOT use for other languages or deployment. |
| C458 | T1 | `.agents/skills/java-17-expert/SKILL.md` | Read and follow `00_skills/(development)/java-17-expert/SKILL.md` and its relevant local modules. |
| C459 | T1 | `.agents/skills/java-17-expert/SKILL.md` | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C460 | T1 | `.agents/skills/java-21-expert/SKILL.md` | Design and implement Java 21 systems and migrations with LTS-aware verification. Use for Java 21 work. Do NOT use for other languages or deployment. |
| C461 | T1 | `.agents/skills/java-21-expert/SKILL.md` | Read and follow `00_skills/(development)/java-21-expert/SKILL.md` and its relevant local modules. |
| C462 | T1 | `.agents/skills/java-21-expert/SKILL.md` | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C463 | T1 | `.agents/skills/java-25-expert/SKILL.md` | Build or migrate Java 25 projects using only APIs verified for toolchain and runtime. Use for Java 25 work. Do NOT use for other languages. |
| C464 | T1 | `.agents/skills/java-25-expert/SKILL.md` | Read and follow `00_skills/(development)/java-25-expert/SKILL.md` and its relevant local modules. |
| C465 | T1 | `.agents/skills/java-25-expert/SKILL.md` | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C466 | T1 | `.agents/skills/java-26-expert/SKILL.md` | Build or migrate Java 26 projects; handle preview status and verify runtime compatibility. Use for Java 26 work. Do NOT use for other languages. |
| C467 | T1 | `.agents/skills/java-26-expert/SKILL.md` | Read and follow `00_skills/(development)/java-26-expert/SKILL.md` and its relevant local modules. |
| C468 | T1 | `.agents/skills/java-26-expert/SKILL.md` | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C469 | T1 | `.agents/skills/java-8-expert/SKILL.md` | Implement, diagnose and modernize Java 8 systems without later-version APIs. Use for Java 8 work. Do NOT use for other languages or deployment. |
| C470 | T1 | `.agents/skills/java-8-expert/SKILL.md` | Read and follow `00_skills/(development)/java-8-expert/SKILL.md` and its relevant local modules. |
| C471 | T1 | `.agents/skills/java-8-expert/SKILL.md` | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C472 | T1 | `.agents/skills/java-bug-solver/SKILL.md` | Analyze Java stack traces, find root causes, validate fixes, keep lessons. Use for Java stack traces. Do NOT use for other languages or deployment. |
| C473 | T1 | `.agents/skills/java-bug-solver/SKILL.md` | Read and follow `00_skills/(development)/java-bug-solver/SKILL.md` and its relevant local modules. |
| C474 | T1 | `.agents/skills/java-bug-solver/SKILL.md` | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C475 | T1 | `.agents/skills/java-bug-solver-skill/SKILL.md` | Create a Java bug-solver skill that analyzes stack traces and validates fixes. Use for creating a Java bug solver. Do NOT use for other languages. |
| C476 | T1 | `.agents/skills/java-bug-solver-skill/SKILL.md` | Read and follow `00_skills/(development)/java-bug-solver-skill/SKILL.md` and its relevant local modules. |
| C477 | T1 | `.agents/skills/java-bug-solver-skill/SKILL.md` | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C478 | T1 | `.agents/skills/java-enterprise-modernizer/SKILL.md` | Analyze Java/Spring enterprise modernization opportunities safely. Use for Java/Spring modernization. Do NOT use for other languages or deployment. |
| C479 | T1 | `.agents/skills/java-enterprise-modernizer/SKILL.md` | Read and follow `00_skills/(development)/java-enterprise-modernizer/SKILL.md` and its relevant local modules. |
| C480 | T1 | `.agents/skills/java-enterprise-modernizer/SKILL.md` | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C481 | T1 | `.agents/skills/java-expert/SKILL.md` | Implement, diagnose and migrate Java projects with version-correct APIs and evidence. Use for Java work. Do NOT use for other languages. |
| C482 | T1 | `.agents/skills/java-expert/SKILL.md` | Read and follow `00_skills/(development)/java-expert/SKILL.md` and its relevant local modules. |
| C483 | T1 | `.agents/skills/java-expert/SKILL.md` | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C484 | T1 | `.agents/skills/java-migration/SKILL.md` | Analyze Java projects and perform version migrations, API replacements and build updates. Use for Java migrations. Do NOT use for other languages. |
| C485 | T1 | `.agents/skills/java-migration/SKILL.md` | Read and follow `00_skills/(development)/java-migration/SKILL.md` and its relevant local modules. |
| C486 | T1 | `.agents/skills/java-migration/SKILL.md` | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C487 | T1 | `.agents/skills/java-version-expert/SKILL.md` | Route Java work to the exact verified JDK profile, loading only needed knowledge. Use for JDK version routing. Do NOT use for other languages. |
| C488 | T1 | `.agents/skills/java-version-expert/SKILL.md` | Read and follow `00_skills/(development)/java-version-expert/SKILL.md` and its relevant local modules. |
| C489 | T1 | `.agents/skills/java-version-expert/SKILL.md` | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C490 | T1 | `.agents/skills/javascript-expert/SKILL.md` | Implement, diagnose and modernize JavaScript with exact runtime and module compatibility. Use for JavaScript work. Do NOT use for other languages. |
| C491 | T1 | `.agents/skills/javascript-expert/SKILL.md` | Read and follow `00_skills/(development)/javascript-expert/SKILL.md` and its relevant local modules. |
| C492 | T1 | `.agents/skills/javascript-expert/SKILL.md` | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C493 | T1 | `.agents/skills/jev-call-expert/SKILL.md` | Design and review TypeSafe Jev function calling with typed signatures. Use for Jev calls. Do NOT use for generic tool calling or unapproved actions. |
| C494 | T1 | `.agents/skills/jev-call-expert/SKILL.md` | Read and follow `00_skills/(development)/jev-call-expert/SKILL.md` and its relevant local modules. |
| C495 | T1 | `.agents/skills/jev-call-expert/SKILL.md` | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C496 | T1 | `.agents/skills/jira-assistant/SKILL.md` | Manage Jira issues via Atlassian MCP: search, create, update, transition. Use for Jira tickets. Do NOT use for Confluence (confluence-assistant). |
| C497 | T1 | `.agents/skills/jira-assistant/SKILL.md` | Read and follow `00_skills/(development)/jira-assistant/SKILL.md` and its relevant local modules. |
| C498 | T1 | `.agents/skills/jira-assistant/SKILL.md` | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C499 | T1 | `.agents/skills/jira-confluence-assistant/SKILL.md` | Prepare governed Jira/Confluence work with traceability to code and evidence. Use for Jira/Confluence tracing. Do NOT use for unrelated stacks. |
| C500 | T1 | `.agents/skills/jira-confluence-assistant/SKILL.md` | Read and follow `00_skills/(development)/jira-confluence-assistant/SKILL.md` and its relevant local modules. |
| C501 | T1 | `.agents/skills/jira-confluence-assistant/SKILL.md` | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C502 | T1 | `.agents/skills/jira-time-entry-assistant/SKILL.md` | Prepare auditable Jira worklog proposals from actual task evidence. Use for Jira time entries. Do NOT use for unrelated stacks or deployment. |
| C503 | T1 | `.agents/skills/jira-time-entry-assistant/SKILL.md` | Read and follow `00_skills/(development)/jira-time-entry-assistant/SKILL.md` and its relevant local modules. |
| C504 | T1 | `.agents/skills/jira-time-entry-assistant/SKILL.md` | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C505 | T1 | `.agents/skills/judge-benchmark-runner/SKILL.md` | Benchmark a deterministic Judge gate against a supplied corpus and thresholds. Use for Judge benchmarks. Do NOT use as deployment approval. |
| C506 | T1 | `.agents/skills/judge-benchmark-runner/SKILL.md` | Read and follow `00_skills/(quality)/judge-benchmark-runner/SKILL.md` and its relevant local modules. |
| C507 | T1 | `.agents/skills/judge-benchmark-runner/SKILL.md` | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C508 | T1 | `.agents/skills/kinghost-backup-recovery-expert/SKILL.md` | Governed KingHost backup and rollback-safe restore: sites, databases, email. Use for KingHost backups. Do NOT use for unapproved prod changes. |
| C509 | T1 | `.agents/skills/kinghost-backup-recovery-expert/SKILL.md` | Read and follow `00_skills/(cloud)/kinghost-backup-recovery-expert/SKILL.md` and its relevant local modules. |
| C510 | T1 | `.agents/skills/kinghost-backup-recovery-expert/SKILL.md` | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C511 | T1 | `.agents/skills/kinghost-clone-site-expert/SKILL.md` | Governed KingHost site clone via verified FTP copy, never mutating the origin. Use for KingHost clones. Do NOT use for unapproved production changes. |
| C512 | T1 | `.agents/skills/kinghost-clone-site-expert/SKILL.md` | Read and follow `00_skills/(cloud)/kinghost-clone-site-expert/SKILL.md` and its relevant local modules. |
| C513 | T1 | `.agents/skills/kinghost-clone-site-expert/SKILL.md` | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C514 | T1 | `.agents/skills/kinghost-database-expert/SKILL.md` | Governed KingHost MySQL work: access, backup, query analysis, migration, recovery. Use for KingHost databases. Do NOT use for unrelated changes. |
| C515 | T1 | `.agents/skills/kinghost-database-expert/SKILL.md` | Read and follow `00_skills/(architecture)/kinghost-database-expert/SKILL.md` and its relevant local modules. |
| C516 | T1 | `.agents/skills/kinghost-database-expert/SKILL.md` | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C517 | T1 | `.agents/skills/kinghost-domain-dns-ssl-expert/SKILL.md` | Governed KingHost domain, DNS and SSL changes with snapshot and rollback. Use for KingHost DNS or SSL. Do NOT use for unapproved production changes. |
| C518 | T1 | `.agents/skills/kinghost-domain-dns-ssl-expert/SKILL.md` | Read and follow `00_skills/(cloud)/kinghost-domain-dns-ssl-expert/SKILL.md` and its relevant local modules. |
| C519 | T1 | `.agents/skills/kinghost-domain-dns-ssl-expert/SKILL.md` | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C520 | T1 | `.agents/skills/kinghost-email-expert/SKILL.md` | Governed KingHost email: mailboxes, DNS/MX, webmail, recovery, no secret exposure. Use for KingHost email. Do NOT use for unapproved prod changes. |
| C521 | T1 | `.agents/skills/kinghost-email-expert/SKILL.md` | Read and follow `00_skills/(cloud)/kinghost-email-expert/SKILL.md` and its relevant local modules. |
| C522 | T1 | `.agents/skills/kinghost-email-expert/SKILL.md` | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C523 | T1 | `.agents/skills/kinghost-expert/SKILL.md` | KingHost hosting super-skill: domains, FTP/SSH publish, WordPress, MySQL, backups. Use for KingHost work. Do NOT use for unapproved prod changes. |
| C524 | T1 | `.agents/skills/kinghost-expert/SKILL.md` | Read and follow `00_skills/(cloud)/kinghost-expert/SKILL.md` and its relevant local modules. |
| C525 | T1 | `.agents/skills/kinghost-expert/SKILL.md` | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C526 | T1 | `.agents/skills/kinghost-performance-expert/SKILL.md` | Measured KingHost performance: resources, cache, PHP runtime, PageSpeed. Use for KingHost performance. Do NOT use for unapproved prod changes. |
| C527 | T1 | `.agents/skills/kinghost-performance-expert/SKILL.md` | Read and follow `00_skills/(cloud)/kinghost-performance-expert/SKILL.md` and its relevant local modules. |
| C528 | T1 | `.agents/skills/kinghost-performance-expert/SKILL.md` | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C529 | T1 | `.agents/skills/kinghost-security-expert/SKILL.md` | KingHost security: malware scans, quarantine, WAF, SSL. Use for KingHost security. Do NOT use outside authorized scope or to expose secrets. |
| C530 | T1 | `.agents/skills/kinghost-security-expert/SKILL.md` | Read and follow `00_skills/(security)/kinghost-security-expert/SKILL.md` and its relevant local modules. |
| C531 | T1 | `.agents/skills/kinghost-security-expert/SKILL.md` | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C532 | T1 | `.agents/skills/kinghost-site-publish-ftp-expert/SKILL.md` | Governed KingHost WordPress/PHP FTP publish with backup and rollback. Use for KingHost publishing. Do NOT use for unapproved production changes. |
| C533 | T1 | `.agents/skills/kinghost-site-publish-ftp-expert/SKILL.md` | Read and follow `00_skills/(cloud)/kinghost-site-publish-ftp-expert/SKILL.md` and its relevant local modules. |
| C534 | T1 | `.agents/skills/kinghost-site-publish-ftp-expert/SKILL.md` | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C535 | T1 | `.agents/skills/kotlin-expert/SKILL.md` | Design and implement Kotlin systems on the current stable release. Use for Kotlin work. Do NOT use for other languages. |
| C536 | T1 | `.agents/skills/kotlin-expert/SKILL.md` | Read and follow `00_skills/(development)/kotlin-expert/SKILL.md` and its relevant local modules. |
| C537 | T1 | `.agents/skills/kotlin-expert/SKILL.md` | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C538 | T1 | `.agents/skills/kubernetes-code-context-mapper/SKILL.md` | Map Kubernetes workloads, services and logs back to repo code and owners. Use for K8s-to-code mapping. Do NOT use for unapproved prod changes. |
| C539 | T1 | `.agents/skills/kubernetes-code-context-mapper/SKILL.md` | Read and follow `00_skills/(cloud)/kubernetes-code-context-mapper/SKILL.md` and its relevant local modules. |
| C540 | T1 | `.agents/skills/kubernetes-code-context-mapper/SKILL.md` | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C541 | T1 | `.agents/skills/kubernetes-observability-staff/SKILL.md` | Kubernetes observability: health, workloads, events, probes. Use for K8s investigations. Do NOT use to mutate live systems unless authorized. |
| C542 | T1 | `.agents/skills/kubernetes-observability-staff/SKILL.md` | Read and follow `00_skills/(monitoring)/kubernetes-observability-staff/SKILL.md` and its relevant local modules. |
| C543 | T1 | `.agents/skills/kubernetes-observability-staff/SKILL.md` | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C544 | T1 | `.agents/skills/laya-expert/SKILL.md` | Implement calibrated typed decisions with the Laya SDK. Use for Laya decisions or RLCD training. Do NOT use for open-ended text or GraphRAG. |
| C545 | T1 | `.agents/skills/laya-expert/SKILL.md` | Read and follow `00_skills/(development)/laya-expert/SKILL.md` and its relevant local modules. |
| C546 | T1 | `.agents/skills/laya-expert/SKILL.md` | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C547 | T1 | `.agents/skills/lead-enrichment/SKILL.md` | Lead enrichment waterfalls, ICP scoring and contact verification (Clay, Apollo). Use for enrichment or lead scoring. Do NOT use for code work. |
| C548 | T1 | `.agents/skills/lead-enrichment/SKILL.md` | Read and follow `00_skills/(gtm)/lead-enrichment/SKILL.md` and its relevant local modules. |
| C549 | T1 | `.agents/skills/lead-enrichment/SKILL.md` | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C550 | T1 | `.agents/skills/learning-curator/SKILL.md` | Promote verified, reusable engineering lessons into .notebook/LEARNING.md. Use for learning promotion. Do NOT use to promote unverified claims. |
| C551 | T1 | `.agents/skills/learning-curator/SKILL.md` | Read and follow `00_skills/(learning)/learning-curator/SKILL.md` and its relevant local modules. |
| C552 | T1 | `.agents/skills/learning-curator/SKILL.md` | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C553 | T1 | `.agents/skills/learning-opportunities/SKILL.md` | Identify reusable lessons and promotion candidates from finished work. Use for session reviews. Do NOT use to write continuity files. |
| C554 | T1 | `.agents/skills/learning-opportunities/SKILL.md` | Read and follow `00_skills/(learning)/learning-opportunities/SKILL.md` and its relevant local modules. |
| C555 | T1 | `.agents/skills/learning-opportunities/SKILL.md` | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C556 | T1 | `.agents/skills/legacy-migration-planner/SKILL.md` | Plan legacy migrations, strangler-fig rewrites and framework upgrades. Use for migration strategy. Do NOT use for domain analysis (domain-analysis). |
| C557 | T1 | `.agents/skills/legacy-migration-planner/SKILL.md` | Read and follow `00_skills/(architecture)/legacy-migration-planner/SKILL.md` and its relevant local modules. |
| C558 | T1 | `.agents/skills/legacy-migration-planner/SKILL.md` | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C559 | T1 | `.agents/skills/legacy-risk-mapper/SKILL.md` | Map legacy risks, modernization blockers and migration strategy. Use for legacy risk mapping. Do NOT use for unrelated implementation or deployment. |
| C560 | T1 | `.agents/skills/legacy-risk-mapper/SKILL.md` | Read and follow `00_skills/(architecture)/legacy-risk-mapper/SKILL.md` and its relevant local modules. |
| C561 | T1 | `.agents/skills/legacy-risk-mapper/SKILL.md` | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C562 | T1 | `.agents/skills/llm-calibration-temperature-expert/SKILL.md` | Engineer LLM decoding and calibration behavior instead of tuning temperature blindly. Use for LLM calibration. Do NOT use for unrelated stacks. |
| C563 | T1 | `.agents/skills/llm-calibration-temperature-expert/SKILL.md` | Read and follow `00_skills/(development)/llm-calibration-temperature-expert/SKILL.md` and its relevant local modules. |
| C564 | T1 | `.agents/skills/llm-calibration-temperature-expert/SKILL.md` | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C565 | T1 | `.agents/skills/llm-model-selection-expert/SKILL.md` | Select the best current model for a workload, using live capability data and evals. Use for model selection. Do NOT use for unrelated stacks. |
| C566 | T1 | `.agents/skills/llm-model-selection-expert/SKILL.md` | Read and follow `00_skills/(development)/llm-model-selection-expert/SKILL.md` and its relevant local modules. |
| C567 | T1 | `.agents/skills/llm-model-selection-expert/SKILL.md` | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C568 | T1 | `.agents/skills/local-secret-vault/SKILL.md` | Read authorized local credential vaults, exposing only masked metadata. Use for local vault access. Do NOT use outside scope or to expose secrets. |
| C569 | T1 | `.agents/skills/local-secret-vault/SKILL.md` | Read and follow `00_skills/(security)/local-secret-vault/SKILL.md` and its relevant local modules. |
| C570 | T1 | `.agents/skills/local-secret-vault/SKILL.md` | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C571 | T1 | `.agents/skills/lora-qlora-dora-expert/SKILL.md` | Implement LoRA, QLoRA or DoRA fine-tuning with reproducible experiments. Use for PEFT work. Do NOT use for unrelated stacks. |
| C572 | T1 | `.agents/skills/lora-qlora-dora-expert/SKILL.md` | Read and follow `00_skills/(development)/lora-qlora-dora-expert/SKILL.md` and its relevant local modules. |
| C573 | T1 | `.agents/skills/lora-qlora-dora-expert/SKILL.md` | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C574 | T1 | `.agents/skills/mantis-architecture/SKILL.md` | Build the Mantis knowledge base (architecture, entities, vulnerabilities). Use at the start of a review loop. Do NOT use for threat models or plans. |
| C575 | T1 | `.agents/skills/mantis-architecture/SKILL.md` | Read and follow `00_skills/(security)/mantis-architecture/SKILL.md` and its relevant local modules. |
| C576 | T1 | `.agents/skills/mantis-architecture/SKILL.md` | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C577 | T1 | `.agents/skills/mantis-calibrate/SKILL.md` | Calculate final risk scores from evidence and architectural impact. Use when findings are processed. Do NOT use to find vulnerabilities or patch. |
| C578 | T1 | `.agents/skills/mantis-calibrate/SKILL.md` | Read and follow `00_skills/(security)/mantis-calibrate/SKILL.md` and its relevant local modules. |
| C579 | T1 | `.agents/skills/mantis-calibrate/SKILL.md` | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C580 | T1 | `.agents/skills/mantis-chain/SKILL.md` | Combine validated findings into exploit chains that raise impact. Use after validation. Do NOT use for initial audits or patch code. |
| C581 | T1 | `.agents/skills/mantis-chain/SKILL.md` | Read and follow `00_skills/(security)/mantis-chain/SKILL.md` and its relevant local modules. |
| C582 | T1 | `.agents/skills/mantis-chain/SKILL.md` | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C583 | T1 | `.agents/skills/mantis-critic/SKILL.md` | Assess production viability of validated findings, filtering debug-only paths. Use for release-build triggerability. Do NOT use for patches. |
| C584 | T1 | `.agents/skills/mantis-critic/SKILL.md` | Read and follow `00_skills/(security)/mantis-critic/SKILL.md` and its relevant local modules. |
| C585 | T1 | `.agents/skills/mantis-critic/SKILL.md` | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C586 | T1 | `.agents/skills/mantis-dedupe/SKILL.md` | Consolidate raw security findings to remove redundant reports. Use before review of raw findings. Do NOT use for auditing code or patch generation. |
| C587 | T1 | `.agents/skills/mantis-dedupe/SKILL.md` | Read and follow `00_skills/(security)/mantis-dedupe/SKILL.md` and its relevant local modules. |
| C588 | T1 | `.agents/skills/mantis-dedupe/SKILL.md` | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C589 | T1 | `.agents/skills/mantis-history/SKILL.md` | Mine VCS history for past vulnerabilities and fixes. Use as first Mantis pre-processing step. Do NOT use for code review or patches. |
| C590 | T1 | `.agents/skills/mantis-history/SKILL.md` | Read and follow `00_skills/(security)/mantis-history/SKILL.md` and its relevant local modules. |
| C591 | T1 | `.agents/skills/mantis-history/SKILL.md` | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C592 | T1 | `.agents/skills/mantis-meta-agent/SKILL.md` | Supervise a long-running automated security review campaign. Use for autonomous campaigns. Do NOT use to run single review stages. |
| C593 | T1 | `.agents/skills/mantis-meta-agent/SKILL.md` | Read and follow `00_skills/(security)/mantis-meta-agent/SKILL.md` and its relevant local modules. |
| C594 | T1 | `.agents/skills/mantis-meta-agent/SKILL.md` | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C595 | T1 | `.agents/skills/mantis-patch/SKILL.md` | Generate minimal security fixes in isolated copies, then apply and verify. Use for reproduced findings. Do NOT use for research or payloads. |
| C596 | T1 | `.agents/skills/mantis-patch/SKILL.md` | Read and follow `00_skills/(security)/mantis-patch/SKILL.md` and its relevant local modules. |
| C597 | T1 | `.agents/skills/mantis-patch/SKILL.md` | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C598 | T1 | `.agents/skills/mantis-pipeline-adapter/SKILL.md` | Design custom deterministic harnesses that wrap Mantis skills. Use for building your own pipeline. Do NOT use to run the default pipeline. |
| C599 | T1 | `.agents/skills/mantis-pipeline-adapter/SKILL.md` | Read and follow `00_skills/(security)/mantis-pipeline-adapter/SKILL.md` and its relevant local modules. |
| C600 | T1 | `.agents/skills/mantis-pipeline-adapter/SKILL.md` | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C601 | T1 | `.agents/skills/mantis-plan/SKILL.md` | Formulate a targeted defensive review plan from the threat model and learnings. Use when starting a campaign. Do NOT use for reviews or patches. |
| C602 | T1 | `.agents/skills/mantis-plan/SKILL.md` | Read and follow `00_skills/(security)/mantis-plan/SKILL.md` and its relevant local modules. |
| C603 | T1 | `.agents/skills/mantis-plan/SKILL.md` | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C604 | T1 | `.agents/skills/mantis-reflect/SKILL.md` | Extract learnings from finished review runs: successes, failures, false assumptions. Use for Mantis reflection. Do NOT use for source or patches. |
| C605 | T1 | `.agents/skills/mantis-reflect/SKILL.md` | Read and follow `00_skills/(security)/mantis-reflect/SKILL.md` and its relevant local modules. |
| C606 | T1 | `.agents/skills/mantis-reflect/SKILL.md` | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C607 | T1 | `.agents/skills/mantis-report/SKILL.md` | Generate a stakeholder security review packet from confirmed findings. Use at the end of a review cycle. Do NOT use for audits or patch checks. |
| C608 | T1 | `.agents/skills/mantis-report/SKILL.md` | Read and follow `00_skills/(security)/mantis-report/SKILL.md` and its relevant local modules. |
| C609 | T1 | `.agents/skills/mantis-report/SKILL.md` | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C610 | T1 | `.agents/skills/mantis-reproduce/SKILL.md` | Write and run crash reproducers to verify security flaws. Use when viable findings exist. Do NOT use for code auditing or patching. |
| C611 | T1 | `.agents/skills/mantis-reproduce/SKILL.md` | Read and follow `00_skills/(security)/mantis-reproduce/SKILL.md` and its relevant local modules. |
| C612 | T1 | `.agents/skills/mantis-reproduce/SKILL.md` | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C613 | T1 | `.agents/skills/mantis-researcher/SKILL.md` | Audit production source files per the review plan with static analysis and deep dives. Use when a plan exists. Do NOT use for planning or patches. |
| C614 | T1 | `.agents/skills/mantis-researcher/SKILL.md` | Read and follow `00_skills/(security)/mantis-researcher/SKILL.md` and its relevant local modules. |
| C615 | T1 | `.agents/skills/mantis-researcher/SKILL.md` | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C616 | T1 | `.agents/skills/mantis-review/SKILL.md` | Independently review findings and filter false positives against source. Use for source validation of findings. Do NOT use for repro or patches. |
| C617 | T1 | `.agents/skills/mantis-review/SKILL.md` | Read and follow `00_skills/(security)/mantis-review/SKILL.md` and its relevant local modules. |
| C618 | T1 | `.agents/skills/mantis-review/SKILL.md` | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C619 | T1 | `.agents/skills/mantis-structural-index/SKILL.md` | Build a content-addressed semantic index of source units. Use when a pinned codebase is available. Do NOT use for findings or patches. |
| C620 | T1 | `.agents/skills/mantis-structural-index/SKILL.md` | Read and follow `00_skills/(security)/mantis-structural-index/SKILL.md` and its relevant local modules. |
| C621 | T1 | `.agents/skills/mantis-structural-index/SKILL.md` | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C622 | T1 | `.agents/skills/mantis-summarize/SKILL.md` | Generate security summaries per directory before planning. Use at the start of a review campaign. Do NOT use for reviews or patches. |
| C623 | T1 | `.agents/skills/mantis-summarize/SKILL.md` | Read and follow `00_skills/(security)/mantis-summarize/SKILL.md` and its relevant local modules. |
| C624 | T1 | `.agents/skills/mantis-summarize/SKILL.md` | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C625 | T1 | `.agents/skills/mantis-threat-model/SKILL.md` | Synthesize trust boundaries, attack surfaces and attackers into a living threat model. Use for KB stage B. Do NOT use for source analysis. |
| C626 | T1 | `.agents/skills/mantis-threat-model/SKILL.md` | Read and follow `00_skills/(security)/mantis-threat-model/SKILL.md` and its relevant local modules. |
| C627 | T1 | `.agents/skills/mantis-threat-model/SKILL.md` | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C628 | T1 | `.agents/skills/marketplace-curator/SKILL.md` | Curate capability listings by provenance, licensing, scope and compatibility. Use for marketplace curation. Do NOT use for unapproved remote writes. |
| C629 | T1 | `.agents/skills/marketplace-curator/SKILL.md` | Read and follow `00_skills/(tooling)/marketplace-curator/SKILL.md` and its relevant local modules. |
| C630 | T1 | `.agents/skills/marketplace-curator/SKILL.md` | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C631 | T1 | `.agents/skills/mcp-discovery/SKILL.md` | Discover and validate MCP tools and capabilities against AEOS policies. Use for MCP discovery. Do NOT use for unapproved remote writes. |
| C632 | T1 | `.agents/skills/mcp-discovery/SKILL.md` | Read and follow `00_skills/(tooling)/mcp-discovery/SKILL.md` and its relevant local modules. |
| C633 | T1 | `.agents/skills/mcp-discovery/SKILL.md` | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C634 | T1 | `.agents/skills/mcp-health-check/SKILL.md` | Validate MCP runtime health, tools, capabilities and security posture. Use for MCP health checks. Do NOT use for unapproved remote writes. |
| C635 | T1 | `.agents/skills/mcp-health-check/SKILL.md` | Read and follow `00_skills/(tooling)/mcp-health-check/SKILL.md` and its relevant local modules. |
| C636 | T1 | `.agents/skills/mcp-health-check/SKILL.md` | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C637 | T1 | `.agents/skills/mcp-poisoning-evaluator/SKILL.md` | Evaluate MCP descriptions and responses for injection and poisoning. Use for MCP reviews. Do NOT use outside authorized scope or to expose secrets. |
| C638 | T1 | `.agents/skills/mcp-poisoning-evaluator/SKILL.md` | Read and follow `00_skills/(security)/mcp-poisoning-evaluator/SKILL.md` and its relevant local modules. |
| C639 | T1 | `.agents/skills/mcp-poisoning-evaluator/SKILL.md` | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C640 | T1 | `.agents/skills/mcp-risk-controller/SKILL.md` | Audit MCPs, tool descriptions, capabilities and poisoning risks. Use for MCP risk audits. Do NOT use for unapproved remote writes. |
| C641 | T1 | `.agents/skills/mcp-risk-controller/SKILL.md` | Read and follow `00_skills/(tooling)/mcp-risk-controller/SKILL.md` and its relevant local modules. |
| C642 | T1 | `.agents/skills/mcp-risk-controller/SKILL.md` | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C643 | T1 | `.agents/skills/memory-curator/SKILL.md` | Curate durable, evidence-backed memory in .notebook/MEMORY.md. Use for memory curation. Do NOT use to promote unverified claims or transient status. |
| C644 | T1 | `.agents/skills/memory-curator/SKILL.md` | Read and follow `00_skills/(learning)/memory-curator/SKILL.md` and its relevant local modules. |
| C645 | T1 | `.agents/skills/memory-curator/SKILL.md` | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C646 | T1 | `.agents/skills/memory-governance-auditor/SKILL.md` | Audit memory reads and writes for evidence, scope and secret safety. Use for memory audits. Do NOT use to promote unverified claims into memory. |
| C647 | T1 | `.agents/skills/memory-governance-auditor/SKILL.md` | Read and follow `00_skills/(learning)/memory-governance-auditor/SKILL.md` and its relevant local modules. |
| C648 | T1 | `.agents/skills/memory-governance-auditor/SKILL.md` | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C649 | T1 | `.agents/skills/mermaid-studio/SKILL.md` | Create, validate and render Mermaid diagrams (SVG, PNG, ASCII). Use for diagrams or mermaid files. Do NOT use for chart plotting or image generation. |
| C650 | T1 | `.agents/skills/mermaid-studio/SKILL.md` | Read and follow `00_skills/(tooling)/mermaid-studio/SKILL.md` and its relevant local modules. |
| C651 | T1 | `.agents/skills/mermaid-studio/SKILL.md` | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C652 | T1 | `.agents/skills/modular-decomposition/SKILL.md` | Monolith-to-modular pipeline: sizing, duplication, hierarchy, coupling. Use for splitting monoliths. Do NOT use for roadmaps. |
| C653 | T1 | `.agents/skills/modular-decomposition/SKILL.md` | Read and follow `00_skills/(architecture)/modular-decomposition/SKILL.md` and its relevant local modules. |
| C654 | T1 | `.agents/skills/modular-decomposition/SKILL.md` | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C655 | T1 | `.agents/skills/modular-design-principles/SKILL.md` | Modular design principles: bounded contexts, boundaries, contracts, splits. Use for module structure reviews. Do NOT use for decomposition pipelines. |
| C656 | T1 | `.agents/skills/modular-design-principles/SKILL.md` | Read and follow `00_skills/(architecture)/modular-design-principles/SKILL.md` and its relevant local modules. |
| C657 | T1 | `.agents/skills/modular-design-principles/SKILL.md` | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C658 | T1 | `.agents/skills/motion-comic-animation-expert/SKILL.md` | Motion Comic animation in Python and FFmpeg: camera, layers, parallax. Use for animar camadas or timeline HQ. Do NOT use to promise unrendered output. |
| C659 | T1 | `.agents/skills/motion-comic-animation-expert/SKILL.md` | Read and follow `00_skills/(tooling)/motion-comic-animation-expert/SKILL.md` and its relevant local modules. |
| C660 | T1 | `.agents/skills/motion-comic-animation-expert/SKILL.md` | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C661 | T1 | `.agents/skills/motion-comic-art-expert/SKILL.md` | Arte HQ científica em camadas. Use for storyboards ou bíblia visual. Do NOT use para chamar imagem única de animação ou inventar referência anexada. |
| C662 | T1 | `.agents/skills/motion-comic-art-expert/SKILL.md` | Read and follow `00_skills/(tooling)/motion-comic-art-expert/SKILL.md` and its relevant local modules. |
| C663 | T1 | `.agents/skills/motion-comic-art-expert/SKILL.md` | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C664 | T1 | `.agents/skills/multi-platform-launch/SKILL.md` | Plan and run multi-platform product launches: Product Hunt, waitlists, launch day. Use for launch strategy. Do NOT use for code work. |
| C665 | T1 | `.agents/skills/multi-platform-launch/SKILL.md` | Read and follow `00_skills/(gtm)/multi-platform-launch/SKILL.md` and its relevant local modules. |
| C666 | T1 | `.agents/skills/multi-platform-launch/SKILL.md` | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C667 | T1 | `.agents/skills/multirepo-ecosystem-mapper/SKILL.md` | Map multi-repo ecosystems and owners. Use for multi-repo mapping. Do NOT use to mutate production or invent architecture without source evidence. |
| C668 | T1 | `.agents/skills/multirepo-ecosystem-mapper/SKILL.md` | Read and follow `00_skills/(mapping)/multirepo-ecosystem-mapper/SKILL.md` and its relevant local modules. |
| C669 | T1 | `.agents/skills/multirepo-ecosystem-mapper/SKILL.md` | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C670 | T1 | `.agents/skills/nestjs-modular-monolith/SKILL.md` | Design NestJS modular monoliths with DDD, CQRS and clean architecture. Use for NestJS bounded contexts. Do NOT use for simple CRUD. |
| C671 | T1 | `.agents/skills/nestjs-modular-monolith/SKILL.md` | Read and follow `00_skills/(development)/nestjs-modular-monolith/SKILL.md` and its relevant local modules. |
| C672 | T1 | `.agents/skills/nestjs-modular-monolith/SKILL.md` | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C673 | T1 | `.agents/skills/netlify-deploy/SKILL.md` | Deploy web projects to Netlify via the CLI, including previews. Use for Netlify deploys or links. Do NOT use for Vercel, Cloudflare or Render. |
| C674 | T1 | `.agents/skills/netlify-deploy/SKILL.md` | Read and follow `00_skills/(cloud)/netlify-deploy/SKILL.md` and its relevant local modules. |
| C675 | T1 | `.agents/skills/netlify-deploy/SKILL.md` | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C676 | T1 | `.agents/skills/not-your-babysitter/SKILL.md` | Autonomous operator: drive tasks to verified results, evidence-or-stop. Use for autonomous runs. Do NOT use for tutorials or brainstorms. |
| C677 | T1 | `.agents/skills/not-your-babysitter/SKILL.md` | Read and follow `00_skills/(development)/not-your-babysitter/SKILL.md` and its relevant local modules. |
| C678 | T1 | `.agents/skills/not-your-babysitter/SKILL.md` | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C679 | T1 | `.agents/skills/notebook-intelligence/SKILL.md` | Maintain compact, fresh project intelligence in .notebook/. Use for notebook maintenance. Do NOT use to promote unverified claims. |
| C680 | T1 | `.agents/skills/notebook-intelligence/SKILL.md` | Read and follow `00_skills/(learning)/notebook-intelligence/SKILL.md` and its relevant local modules. |
| C681 | T1 | `.agents/skills/notebook-intelligence/SKILL.md` | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C682 | T1 | `.agents/skills/nx-ci-monitor/SKILL.md` | Monitor Nx Cloud CI status and handle self-healing fixes. Use for 'watch CI' on Nx. Do NOT use for local task runs (nx-run-tasks). |
| C683 | T1 | `.agents/skills/nx-ci-monitor/SKILL.md` | Read and follow `00_skills/(tooling)/nx-ci-monitor/SKILL.md` and its relevant local modules. |
| C684 | T1 | `.agents/skills/nx-ci-monitor/SKILL.md` | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C685 | T1 | `.agents/skills/nx-generate/SKILL.md` | Scaffold code with Nx generators: projects, libraries, features. Use for 'nx generate' tasks. Do NOT use for running tasks (nx-run-tasks). |
| C686 | T1 | `.agents/skills/nx-generate/SKILL.md` | Read and follow `00_skills/(tooling)/nx-generate/SKILL.md` and its relevant local modules. |
| C687 | T1 | `.agents/skills/nx-generate/SKILL.md` | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C688 | T1 | `.agents/skills/nx-run-tasks/SKILL.md` | Run Nx build, test, lint, serve and affected tasks in a workspace. Use for 'run tests' or 'nx affected'. Do NOT use for code generation (nx-generate). |
| C689 | T1 | `.agents/skills/nx-run-tasks/SKILL.md` | Read and follow `00_skills/(tooling)/nx-run-tasks/SKILL.md` and its relevant local modules. |
| C690 | T1 | `.agents/skills/nx-run-tasks/SKILL.md` | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C691 | T1 | `.agents/skills/nx-workspace/SKILL.md` | Configure and optimize Nx monorepos: boundaries, affected analysis, caching, CI. Use for Nx workspace setup. Do NOT use to run tasks or generate code. |
| C692 | T1 | `.agents/skills/nx-workspace/SKILL.md` | Read and follow `00_skills/(tooling)/nx-workspace/SKILL.md` and its relevant local modules. |
| C693 | T1 | `.agents/skills/nx-workspace/SKILL.md` | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C694 | T1 | `.agents/skills/observability-architect/SKILL.md` | Design logs, traces, metrics, dashboards, alerting. Use for observability design. Do NOT use to mutate live systems unless authorized. |
| C695 | T1 | `.agents/skills/observability-architect/SKILL.md` | Read and follow `00_skills/(monitoring)/observability-architect/SKILL.md` and its relevant local modules. |
| C696 | T1 | `.agents/skills/observability-architect/SKILL.md` | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C697 | T1 | `.agents/skills/observability-reporter/SKILL.md` | Generate timelines, metrics, trace summaries and failure analysis. Use for observability reports. Do NOT use to mutate live systems unless authorized. |
| C698 | T1 | `.agents/skills/observability-reporter/SKILL.md` | Read and follow `00_skills/(monitoring)/observability-reporter/SKILL.md` and its relevant local modules. |
| C699 | T1 | `.agents/skills/observability-reporter/SKILL.md` | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C700 | T1 | `.agents/skills/observability-root-cause-integrator/SKILL.md` | Merge observability and code evidence into a root-cause plan. Use for root-cause integration. Do NOT use to mutate live systems unless authorized. |
| C701 | T1 | `.agents/skills/observability-root-cause-integrator/SKILL.md` | Read and follow `00_skills/(monitoring)/observability-root-cause-integrator/SKILL.md` and its relevant local modules. |
| C702 | T1 | `.agents/skills/observability-root-cause-integrator/SKILL.md` | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C703 | T1 | `.agents/skills/openshift-observability-staff/SKILL.md` | OpenShift observability: monitoring, alerts, logging, operators. Use for OpenShift work. Do NOT use to mutate live systems unless authorized. |
| C704 | T1 | `.agents/skills/openshift-observability-staff/SKILL.md` | Read and follow `00_skills/(monitoring)/openshift-observability-staff/SKILL.md` and its relevant local modules. |
| C705 | T1 | `.agents/skills/openshift-observability-staff/SKILL.md` | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C706 | T1 | `.agents/skills/pack-marketplace-auditor/SKILL.md` | Audit pack marketplace quarantine, staging, active packs and trust policy. Use for pack marketplace audits. Do NOT use for unapproved remote writes. |
| C707 | T1 | `.agents/skills/pack-marketplace-auditor/SKILL.md` | Read and follow `00_skills/(tooling)/pack-marketplace-auditor/SKILL.md` and its relevant local modules. |
| C708 | T1 | `.agents/skills/pack-marketplace-auditor/SKILL.md` | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C709 | T1 | `.agents/skills/package-trust-engineer/SKILL.md` | Verify packages, manifests, quarantine and promotion. Use for package trust checks. Do NOT use outside authorized scope or to expose secrets. |
| C710 | T1 | `.agents/skills/package-trust-engineer/SKILL.md` | Read and follow `00_skills/(security)/package-trust-engineer/SKILL.md` and its relevant local modules. |
| C711 | T1 | `.agents/skills/package-trust-engineer/SKILL.md` | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C712 | T1 | `.agents/skills/packaging/SKILL.md` | Create, inspect and verify AEOS packages with manifests and checksums. Use for packaging work. Do NOT use for unapproved remote writes. |
| C713 | T1 | `.agents/skills/packaging/SKILL.md` | Read and follow `00_skills/(tooling)/packaging/SKILL.md` and its relevant local modules. |
| C714 | T1 | `.agents/skills/packaging/SKILL.md` | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C715 | T1 | `.agents/skills/paid-creative-ai/SKILL.md` | AI paid ad creative: generation, testing, fatigue, ROAS. Use for ad creative or Meta/Google/TikTok ads. Do NOT use for code work. |
| C716 | T1 | `.agents/skills/paid-creative-ai/SKILL.md` | Read and follow `00_skills/(gtm)/paid-creative-ai/SKILL.md` and its relevant local modules. |
| C717 | T1 | `.agents/skills/paid-creative-ai/SKILL.md` | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C718 | T1 | `.agents/skills/parallel-scheduler/SKILL.md` | Create deterministic safe schedules for playbook tasks from dependency sets. Use for parallel scheduling. Do NOT use for unapproved remote writes. |
| C719 | T1 | `.agents/skills/parallel-scheduler/SKILL.md` | Read and follow `00_skills/(tooling)/parallel-scheduler/SKILL.md` and its relevant local modules. |
| C720 | T1 | `.agents/skills/parallel-scheduler/SKILL.md` | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C721 | T1 | `.agents/skills/partner-affiliate/SKILL.md` | Design partner and affiliate programs: recruitment, revenue share, co-marketing. Use for partner programs. Do NOT use for code work. |
| C722 | T1 | `.agents/skills/partner-affiliate/SKILL.md` | Read and follow `00_skills/(gtm)/partner-affiliate/SKILL.md` and its relevant local modules. |
| C723 | T1 | `.agents/skills/partner-affiliate/SKILL.md` | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C724 | T1 | `.agents/skills/patch-planner/SKILL.md` | Generate patch proposals and rollback plans without applying them. Use for patch planning. Do NOT use for unrelated stacks or deployment. |
| C725 | T1 | `.agents/skills/patch-planner/SKILL.md` | Read and follow `00_skills/(development)/patch-planner/SKILL.md` and its relevant local modules. |
| C726 | T1 | `.agents/skills/patch-planner/SKILL.md` | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C727 | T1 | `.agents/skills/perf-astro/SKILL.md` | Optimize Astro sites for Lighthouse: critical CSS, fonts, LCP. Use for Astro performance. Do NOT use for non-Astro sites or Lighthouse-only audits. |
| C728 | T1 | `.agents/skills/perf-astro/SKILL.md` | Read and follow `00_skills/(performance)/perf-astro/SKILL.md` and its relevant local modules. |
| C729 | T1 | `.agents/skills/perf-astro/SKILL.md` | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C730 | T1 | `.agents/skills/perf-lighthouse/SKILL.md` | Run Lighthouse via CLI or Node, parse reports, set budgets. Use for Lighthouse audits. Do NOT use for CWV fixes (core-web-vitals). |
| C731 | T1 | `.agents/skills/perf-lighthouse/SKILL.md` | Read and follow `00_skills/(performance)/perf-lighthouse/SKILL.md` and its relevant local modules. |
| C732 | T1 | `.agents/skills/perf-lighthouse/SKILL.md` | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C733 | T1 | `.agents/skills/perf-web-optimization/SKILL.md` | Measure, then cut bundle size, images, caching and page speed. Use for web performance work. Do NOT use for CWV-only work (core-web-vitals). |
| C734 | T1 | `.agents/skills/perf-web-optimization/SKILL.md` | Read and follow `00_skills/(performance)/perf-web-optimization/SKILL.md` and its relevant local modules. |
| C735 | T1 | `.agents/skills/perf-web-optimization/SKILL.md` | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C736 | T1 | `.agents/skills/performance-optimizer/SKILL.md` | Measure and improve AEOS hot paths: registry, skill runs, evidence. Use for measured optimization. Do NOT use for speculative tuning. |
| C737 | T1 | `.agents/skills/performance-optimizer/SKILL.md` | Read and follow `00_skills/(performance)/performance-optimizer/SKILL.md` and its relevant local modules. |
| C738 | T1 | `.agents/skills/performance-optimizer/SKILL.md` | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C739 | T1 | `.agents/skills/performance-profiler/SKILL.md` | Profile AEOS runs: repo scans, hashing, package verification, Judge runtime. Use for AEOS profiling. Do NOT use for speculative tuning. |
| C740 | T1 | `.agents/skills/performance-profiler/SKILL.md` | Read and follow `00_skills/(performance)/performance-profiler/SKILL.md` and its relevant local modules. |
| C741 | T1 | `.agents/skills/performance-profiler/SKILL.md` | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C742 | T1 | `.agents/skills/playbook-factory-generator/SKILL.md` | Generate a reviewable playbook with step contracts, dependencies and verification gates. Use for playbook generation. Do NOT use for one-off coding. |
| C743 | T1 | `.agents/skills/playbook-factory-generator/SKILL.md` | Read and follow `00_skills/(creation)/playbook-factory-generator/SKILL.md` and its relevant local modules. |
| C744 | T1 | `.agents/skills/playbook-factory-generator/SKILL.md` | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C745 | T1 | `.agents/skills/playbook-optimizer/SKILL.md` | Optimize playbooks for execution time, safety and evidence quality. Use for playbook optimization. Do NOT use for one-off coding. |
| C746 | T1 | `.agents/skills/playbook-optimizer/SKILL.md` | Read and follow `00_skills/(creation)/playbook-optimizer/SKILL.md` and its relevant local modules. |
| C747 | T1 | `.agents/skills/playbook-optimizer/SKILL.md` | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C748 | T1 | `.agents/skills/playwright-skill/SKILL.md` | Browser automation and E2E tests with Playwright: forms, flows, responsive checks. Use for web tests. Do NOT use for debugging (chrome-devtools). |
| C749 | T1 | `.agents/skills/playwright-skill/SKILL.md` | Read and follow `00_skills/(web-automation)/playwright-skill/SKILL.md` and its relevant local modules. |
| C750 | T1 | `.agents/skills/playwright-skill/SKILL.md` | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C751 | T1 | `.agents/skills/policy-bypass-evaluator/SKILL.md` | Check policy boundaries reject bypass attempts. Use for bypass evaluations. Do NOT use outside authorized scope or to expose secrets. |
| C752 | T1 | `.agents/skills/policy-bypass-evaluator/SKILL.md` | Read and follow `00_skills/(security)/policy-bypass-evaluator/SKILL.md` and its relevant local modules. |
| C753 | T1 | `.agents/skills/policy-bypass-evaluator/SKILL.md` | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C754 | T1 | `.agents/skills/policy-hardening-auditor/SKILL.md` | Audit policies for unsafe paths and fail-closed behavior. Use for policy hardening. Do NOT use outside authorized scope or to expose secrets. |
| C755 | T1 | `.agents/skills/policy-hardening-auditor/SKILL.md` | Read and follow `00_skills/(security)/policy-hardening-auditor/SKILL.md` and its relevant local modules. |
| C756 | T1 | `.agents/skills/policy-hardening-auditor/SKILL.md` | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C757 | T1 | `.agents/skills/positioning-icp/SKILL.md` | ICP definition, market positioning, messaging and PMF validation for AI-native products. Use for ICP or positioning work. Do NOT use for code work. |
| C758 | T1 | `.agents/skills/positioning-icp/SKILL.md` | Read and follow `00_skills/(gtm)/positioning-icp/SKILL.md` and its relevant local modules. |
| C759 | T1 | `.agents/skills/positioning-icp/SKILL.md` | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C760 | T1 | `.agents/skills/pr-comment-resolver/SKILL.md` | Resolve PR review comments systematically, without blindly obeying incorrect feedback. Use for PR comment resolution. Do NOT use for deployment. |
| C761 | T1 | `.agents/skills/pr-comment-resolver/SKILL.md` | Read and follow `00_skills/(development)/pr-comment-resolver/SKILL.md` and its relevant local modules. |
| C762 | T1 | `.agents/skills/pr-comment-resolver/SKILL.md` | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C763 | T1 | `.agents/skills/pr-reviewer/SKILL.md` | Review pull requests as an independent, evidence-based reviewer. Use for PR reviews. Do NOT use for deployment or unrelated stacks. |
| C764 | T1 | `.agents/skills/pr-reviewer/SKILL.md` | Read and follow `00_skills/(development)/pr-reviewer/SKILL.md` and its relevant local modules. |
| C765 | T1 | `.agents/skills/pr-reviewer/SKILL.md` | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C766 | T1 | `.agents/skills/pr-reviewer-advanced/SKILL.md` | Perform severity-ranked, evidence-backed PR reviews. Use for deep PR reviews. Do NOT use for deployment or unrelated stacks. |
| C767 | T1 | `.agents/skills/pr-reviewer-advanced/SKILL.md` | Read and follow `00_skills/(development)/pr-reviewer-advanced/SKILL.md` and its relevant local modules. |
| C768 | T1 | `.agents/skills/pr-reviewer-advanced/SKILL.md` | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C769 | T1 | `.agents/skills/production-deployment-planner/SKILL.md` | Plan production packaging, CI/CD, deployment, observability and rollback. Use for deployment plans. Do NOT use for unapproved prod changes. |
| C770 | T1 | `.agents/skills/production-deployment-planner/SKILL.md` | Read and follow `00_skills/(cloud)/production-deployment-planner/SKILL.md` and its relevant local modules. |
| C771 | T1 | `.agents/skills/production-deployment-planner/SKILL.md` | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C772 | T1 | `.agents/skills/progress-tracker/SKILL.md` | Keep .notebook/PROGRESS.md as the live, evidence-backed mission checklist. Use for progress tracking. Do NOT use to promote unverified claims. |
| C773 | T1 | `.agents/skills/progress-tracker/SKILL.md` | Read and follow `00_skills/(learning)/progress-tracker/SKILL.md` and its relevant local modules. |
| C774 | T1 | `.agents/skills/progress-tracker/SKILL.md` | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C775 | T1 | `.agents/skills/prompt-optimizer/SKILL.md` | Convert vague prompts into bounded, evidence-based task prompts. Use for prompt optimization. Do NOT use for unapproved remote writes. |
| C776 | T1 | `.agents/skills/prompt-optimizer/SKILL.md` | Read and follow `00_skills/(tooling)/prompt-optimizer/SKILL.md` and its relevant local modules. |
| C777 | T1 | `.agents/skills/prompt-optimizer/SKILL.md` | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C778 | T1 | `.agents/skills/ptbr-documentary-voice-expert/SKILL.md` | Deep male PT-BR documentary narration, scientific pronunciation. Use for narrador de documentário. Do NOT use to clone voices without authorization. |
| C779 | T1 | `.agents/skills/ptbr-documentary-voice-expert/SKILL.md` | Read and follow `00_skills/(tooling)/ptbr-documentary-voice-expert/SKILL.md` and its relevant local modules. |
| C780 | T1 | `.agents/skills/ptbr-documentary-voice-expert/SKILL.md` | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C781 | T1 | `.agents/skills/python-ai-productionizer/SKILL.md` | Analyze Python AI/RAG systems for production readiness. Use for Python AI productionization. Do NOT use for unrelated stacks or deployment. |
| C782 | T1 | `.agents/skills/python-ai-productionizer/SKILL.md` | Read and follow `00_skills/(development)/python-ai-productionizer/SKILL.md` and its relevant local modules. |
| C783 | T1 | `.agents/skills/python-ai-productionizer/SKILL.md` | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C784 | T1 | `.agents/skills/python-bug-solver-skill/SKILL.md` | Create a Python bug-solver skill for stack traces and root-cause fixes. Use for creating a Python bug solver. Do NOT use for other languages. |
| C785 | T1 | `.agents/skills/python-bug-solver-skill/SKILL.md` | Read and follow `00_skills/(development)/python-bug-solver-skill/SKILL.md` and its relevant local modules. |
| C786 | T1 | `.agents/skills/python-bug-solver-skill/SKILL.md` | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C787 | T1 | `.agents/skills/python-expert/SKILL.md` | Implement, diagnose, test and modernize Python projects with version-correct APIs. Use for Python work. Do NOT use for other languages. |
| C788 | T1 | `.agents/skills/python-expert/SKILL.md` | Read and follow `00_skills/(development)/python-expert/SKILL.md` and its relevant local modules. |
| C789 | T1 | `.agents/skills/python-expert/SKILL.md` | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C790 | T1 | `.agents/skills/python-rag-audit/SKILL.md` | Audit Python RAG pipelines for security, data leakage and prompt injection. Use for Python RAG audits. Do NOT use for unrelated stacks. |
| C791 | T1 | `.agents/skills/python-rag-audit/SKILL.md` | Read and follow `00_skills/(development)/python-rag-audit/SKILL.md` and its relevant local modules. |
| C792 | T1 | `.agents/skills/python-rag-audit/SKILL.md` | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C793 | T1 | `.agents/skills/rag-expert/SKILL.md` | Implement and evaluate grounded retrieval: hybrid search, reranking, citations. Use for RAG work. Do NOT use for standalone Laya training. |
| C794 | T1 | `.agents/skills/rag-expert/SKILL.md` | Read and follow `00_skills/(development)/rag-expert/SKILL.md` and its relevant local modules. |
| C795 | T1 | `.agents/skills/rag-expert/SKILL.md` | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C796 | T1 | `.agents/skills/rag-laya-expert/SKILL.md` | Orchestrate evaluated RAG and GraphRAG with Laya decisions. Use for RAG or GraphRAG with Laya. Do NOT use for standalone graph drawing. |
| C797 | T1 | `.agents/skills/rag-laya-expert/SKILL.md` | Read and follow `00_skills/(development)/rag-laya-expert/SKILL.md` and its relevant local modules. |
| C798 | T1 | `.agents/skills/rag-laya-expert/SKILL.md` | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C799 | T1 | `.agents/skills/ragraph-expert/SKILL.md` | Build and evaluate source-backed knowledge-graph retrieval (GraphRAG). Use for GraphRAG or entity resolution. Do NOT use for generic diagrams. |
| C800 | T1 | `.agents/skills/ragraph-expert/SKILL.md` | Read and follow `00_skills/(development)/ragraph-expert/SKILL.md` and its relevant local modules. |
| C801 | T1 | `.agents/skills/ragraph-expert/SKILL.md` | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C802 | T1 | `.agents/skills/rails-dev/SKILL.md` | Rails conventions (rich models, concerns, Minitest). Use for any Rails model, schema or code topic. Do NOT use for non-Rails backends. |
| C803 | T1 | `.agents/skills/rails-dev/SKILL.md` | Read and follow `00_skills/(development)/rails-dev/SKILL.md` and its relevant local modules. |
| C804 | T1 | `.agents/skills/rails-dev/SKILL.md` | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C805 | T1 | `.agents/skills/react-best-practices/SKILL.md` | React/Next.js performance: data fetching, bundles, rendering. Use for React perf work. Do NOT use for component APIs (react-composition-patterns). |
| C806 | T1 | `.agents/skills/react-best-practices/SKILL.md` | Read and follow `00_skills/(quality)/react-best-practices/SKILL.md` and its relevant local modules. |
| C807 | T1 | `.agents/skills/react-best-practices/SKILL.md` | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C808 | T1 | `.agents/skills/react-composition-patterns/SKILL.md` | React composition: compound components, render props, React 19. Use for component API refactors. Do NOT use for performance (react-best-practices). |
| C809 | T1 | `.agents/skills/react-composition-patterns/SKILL.md` | Read and follow `00_skills/(architecture)/react-composition-patterns/SKILL.md` and its relevant local modules. |
| C810 | T1 | `.agents/skills/react-composition-patterns/SKILL.md` | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C811 | T1 | `.agents/skills/react-expert/SKILL.md` | Implement and refactor React apps on the repo's exact React version and conventions. Use for React work. Do NOT use for other stacks or deployment. |
| C812 | T1 | `.agents/skills/react-expert/SKILL.md` | Read and follow `00_skills/(development)/react-expert/SKILL.md` and its relevant local modules. |
| C813 | T1 | `.agents/skills/react-expert/SKILL.md` | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C814 | T1 | `.agents/skills/react-native-expert/SKILL.md` | Build production React Native and Expo apps: navigation, lists, native modules. Use for mobile app work. Do NOT use for Flutter or web-only React. |
| C815 | T1 | `.agents/skills/react-native-expert/SKILL.md` | Read and follow `00_skills/(development)/react-native-expert/SKILL.md` and its relevant local modules. |
| C816 | T1 | `.agents/skills/react-native-expert/SKILL.md` | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C817 | T1 | `.agents/skills/redaction-evaluator/SKILL.md` | Evaluate redaction in authorized outputs for leakage and over-redaction. Use for redaction reviews. Do NOT use outside scope or to expose secrets. |
| C818 | T1 | `.agents/skills/redaction-evaluator/SKILL.md` | Read and follow `00_skills/(security)/redaction-evaluator/SKILL.md` and its relevant local modules. |
| C819 | T1 | `.agents/skills/redaction-evaluator/SKILL.md` | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C820 | T1 | `.agents/skills/release-readiness-judge/SKILL.md` | Validate release readiness with deterministic gates. Use for release readiness checks. Do NOT use as deployment approval or for unexecuted checks. |
| C821 | T1 | `.agents/skills/release-readiness-judge/SKILL.md` | Read and follow `00_skills/(quality)/release-readiness-judge/SKILL.md` and its relevant local modules. |
| C822 | T1 | `.agents/skills/release-readiness-judge/SKILL.md` | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C823 | T1 | `.agents/skills/render-deploy/SKILL.md` | Deploy apps to Render: analyze code, generate render.yaml Blueprints. Use for Render deploys. Do NOT use for Vercel, Netlify or Cloudflare. |
| C824 | T1 | `.agents/skills/render-deploy/SKILL.md` | Read and follow `00_skills/(cloud)/render-deploy/SKILL.md` and its relevant local modules. |
| C825 | T1 | `.agents/skills/render-deploy/SKILL.md` | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C826 | T1 | `.agents/skills/repo-scanner/SKILL.md` | Map repositories into factual ecosystems. Use for repo scans. Do NOT use to mutate production or invent architecture without source evidence. |
| C827 | T1 | `.agents/skills/repo-scanner/SKILL.md` | Read and follow `00_skills/(mapping)/repo-scanner/SKILL.md` and its relevant local modules. |
| C828 | T1 | `.agents/skills/repo-scanner/SKILL.md` | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C829 | T1 | `.agents/skills/report-design/SKILL.md` | Apply the offline report layout: tokens, grids, filters, export, drill-down. Use for HTML report fixes. Do NOT use for data collection. |
| C830 | T1 | `.agents/skills/report-design/SKILL.md` | Read and follow `00_skills/(design)/report-design/SKILL.md` and its relevant local modules. |
| C831 | T1 | `.agents/skills/report-design/SKILL.md` | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C832 | T1 | `.agents/skills/resolver-comentarios/SKILL.md` | Resolve concrete PR review comments after inspecting code and verifying fixes. Use for PR comment fixes. Do NOT use for deployment. |
| C833 | T1 | `.agents/skills/resolver-comentarios/SKILL.md` | Read and follow `00_skills/(development)/resolver-comentarios/SKILL.md` and its relevant local modules. |
| C834 | T1 | `.agents/skills/resolver-comentarios/SKILL.md` | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C835 | T1 | `.agents/skills/revisar-pr/SKILL.md` | Review a PR diff against requirements and conventions, ranked findings. Use for revisar PR. Do NOT use for security review (revisar-seguranca-pr). |
| C836 | T1 | `.agents/skills/revisar-pr/SKILL.md` | Read and follow `00_skills/(development)/revisar-pr/SKILL.md` and its relevant local modules. |
| C837 | T1 | `.agents/skills/revisar-pr/SKILL.md` | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C838 | T1 | `.agents/skills/revisar-seguranca-pr/SKILL.md` | Review a PR diff for authorization, sensitive data and security failures. Use for PR security review. Do NOT use for general review (revisar-pr). |
| C839 | T1 | `.agents/skills/revisar-seguranca-pr/SKILL.md` | Read and follow `00_skills/(security)/revisar-seguranca-pr/SKILL.md` and its relevant local modules. |
| C840 | T1 | `.agents/skills/revisar-seguranca-pr/SKILL.md` | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C841 | T1 | `.agents/skills/risk-classifier/SKILL.md` | Classify change risk: scope, impact, reversibility, coverage. Use for risk classification. Do NOT use outside authorized scope or to expose secrets. |
| C842 | T1 | `.agents/skills/risk-classifier/SKILL.md` | Read and follow `00_skills/(security)/risk-classifier/SKILL.md` and its relevant local modules. |
| C843 | T1 | `.agents/skills/risk-classifier/SKILL.md` | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C844 | T1 | `.agents/skills/rollback-planner/SKILL.md` | Generate rollback plans that define how to undo every operation safely. Use for rollback planning. Do NOT use for unapproved production changes. |
| C845 | T1 | `.agents/skills/rollback-planner/SKILL.md` | Read and follow `00_skills/(cloud)/rollback-planner/SKILL.md` and its relevant local modules. |
| C846 | T1 | `.agents/skills/rollback-planner/SKILL.md` | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C847 | T1 | `.agents/skills/runtime-troubleshooting/SKILL.md` | Diagnose apps from read-only logs. Use for runtime failures. Do NOT use to restart, scale, deploy, redesign or invent inaccessible broker state. |
| C848 | T1 | `.agents/skills/runtime-troubleshooting/SKILL.md` | Read and follow `00_skills/(development)/runtime-troubleshooting/SKILL.md` and its relevant local modules. |
| C849 | T1 | `.agents/skills/runtime-troubleshooting/SKILL.md` | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C850 | T1 | `.agents/skills/rust-expert/SKILL.md` | Implement, diagnose, modernize and migrate Rust projects with version-correct APIs. Use for Rust work. Do NOT use for other languages or deployment. |
| C851 | T1 | `.agents/skills/rust-expert/SKILL.md` | Read and follow `00_skills/(development)/rust-expert/SKILL.md` and its relevant local modules. |
| C852 | T1 | `.agents/skills/rust-expert/SKILL.md` | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C853 | T1 | `.agents/skills/sales-motion-design/SKILL.md` | Choose PLG vs sales-led, design the sales motion and time-to-first-value. Use for sales motion or free-trial design. Do NOT use for code work. |
| C854 | T1 | `.agents/skills/sales-motion-design/SKILL.md` | Read and follow `00_skills/(gtm)/sales-motion-design/SKILL.md` and its relevant local modules. |
| C855 | T1 | `.agents/skills/sales-motion-design/SKILL.md` | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C856 | T1 | `.agents/skills/science-research-expert/SKILL.md` | Revisar fontes de ciência. Use for checar afirmações científicas. Do NOT use para inventar referências, certificar medicina ou renderizar vídeo. |
| C857 | T1 | `.agents/skills/science-research-expert/SKILL.md` | Read and follow `00_skills/(tooling)/science-research-expert/SKILL.md` and its relevant local modules. |
| C858 | T1 | `.agents/skills/science-research-expert/SKILL.md` | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C859 | T1 | `.agents/skills/science-script-expert/SKILL.md` | Escrever roteiros científicos PT-BR sincronizados com storyboard. Use for roteiro de ciência. Do NOT use for pesquisa sem fontes ou arte final. |
| C860 | T1 | `.agents/skills/science-script-expert/SKILL.md` | Read and follow `00_skills/(tooling)/science-script-expert/SKILL.md` and its relevant local modules. |
| C861 | T1 | `.agents/skills/science-script-expert/SKILL.md` | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C862 | T1 | `.agents/skills/science-studio-expert/SKILL.md` | Orquestrar Science Studio AI do tema ao Motion Comic revisável. Use for criar vídeo de ciência. Do NOT use to publish without review. |
| C863 | T1 | `.agents/skills/science-studio-expert/SKILL.md` | Read and follow `00_skills/(tooling)/science-studio-expert/SKILL.md` and its relevant local modules. |
| C864 | T1 | `.agents/skills/science-studio-expert/SKILL.md` | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C865 | T1 | `.agents/skills/science-vfx-expert/SKILL.md` | Plan controlled science VFX: gravitational lens, particles, glow. Use for VFX científicos em Motion Comic. Do NOT use to claim validated physics. |
| C866 | T1 | `.agents/skills/science-vfx-expert/SKILL.md` | Read and follow `00_skills/(tooling)/science-vfx-expert/SKILL.md` and its relevant local modules. |
| C867 | T1 | `.agents/skills/science-vfx-expert/SKILL.md` | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C868 | T1 | `.agents/skills/science-video-review-expert/SKILL.md` | Review and package science Motion Comic videos before export. Use for QA de vídeo de ciência. Do NOT use to self-approve or publish without request. |
| C869 | T1 | `.agents/skills/science-video-review-expert/SKILL.md` | Read and follow `00_skills/(tooling)/science-video-review-expert/SKILL.md` and its relevant local modules. |
| C870 | T1 | `.agents/skills/science-video-review-expert/SKILL.md` | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C871 | T1 | `.agents/skills/secret-redaction-specialist/SKILL.md` | Detect and redact sensitive data without exposing raw values. Use for secret redaction. Do NOT use outside authorized scope or to expose secrets. |
| C872 | T1 | `.agents/skills/secret-redaction-specialist/SKILL.md` | Read and follow `00_skills/(security)/secret-redaction-specialist/SKILL.md` and its relevant local modules. |
| C873 | T1 | `.agents/skills/secret-redaction-specialist/SKILL.md` | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C874 | T1 | `.agents/skills/security-audit/SKILL.md` | Detect security risks and possible secrets without exposing values. Use for security audits. Do NOT use outside authorized scope or to expose secrets. |
| C875 | T1 | `.agents/skills/security-audit/SKILL.md` | Read and follow `00_skills/(security)/security-audit/SKILL.md` and its relevant local modules. |
| C876 | T1 | `.agents/skills/security-audit/SKILL.md` | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C877 | T1 | `.agents/skills/security-best-practices/SKILL.md` | Review secure-by-default code (Java, Spring, Angular, Python, JS, Go). Use for secure coding. Do NOT use for PR diffs (revisar-seguranca-pr). |
| C878 | T1 | `.agents/skills/security-best-practices/SKILL.md` | Read and follow `00_skills/(security)/security-best-practices/SKILL.md` and its relevant local modules. |
| C879 | T1 | `.agents/skills/security-best-practices/SKILL.md` | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C880 | T1 | `.agents/skills/security-ownership-map/SKILL.md` | Map git ownership: people-to-file, bus factor, orphaned sensitive code. Use for bus-factor checks. Do NOT use for threat models. |
| C881 | T1 | `.agents/skills/security-ownership-map/SKILL.md` | Read and follow `00_skills/(security)/security-ownership-map/SKILL.md` and its relevant local modules. |
| C882 | T1 | `.agents/skills/security-ownership-map/SKILL.md` | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C883 | T1 | `.agents/skills/security-threat-model/SKILL.md` | Repo-grounded threat model: trust boundaries, assets, attackers, abuse paths. Use for threat modeling. Do NOT use for architecture summaries. |
| C884 | T1 | `.agents/skills/security-threat-model/SKILL.md` | Read and follow `00_skills/(security)/security-threat-model/SKILL.md` and its relevant local modules. |
| C885 | T1 | `.agents/skills/security-threat-model/SKILL.md` | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C886 | T1 | `.agents/skills/sentry/SKILL.md` | Inspect Sentry issues and production errors via the read-only API. Use for 'check Sentry' reports. Do NOT use for SDK setup or alerts. |
| C887 | T1 | `.agents/skills/sentry/SKILL.md` | Read and follow `00_skills/(monitoring)/sentry/SKILL.md` and its relevant local modules. |
| C888 | T1 | `.agents/skills/sentry/SKILL.md` | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C889 | T1 | `.agents/skills/seo/SKILL.md` | Optimize search visibility: meta tags, structured data, sitemaps. Use for 'improve SEO' requests. Do NOT use for accessibility or full site audits. |
| C890 | T1 | `.agents/skills/seo/SKILL.md` | Read and follow `00_skills/(quality)/seo/SKILL.md` and its relevant local modules. |
| C891 | T1 | `.agents/skills/seo/SKILL.md` | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C892 | T1 | `.agents/skills/servicenow-incident-assistant/SKILL.md` | Turn incident evidence into ServiceNow triage, updates and RCA. Use for ServiceNow incident work. Do NOT use to mutate live systems unless authorized. |
| C893 | T1 | `.agents/skills/servicenow-incident-assistant/SKILL.md` | Read and follow `00_skills/(monitoring)/servicenow-incident-assistant/SKILL.md` and its relevant local modules. |
| C894 | T1 | `.agents/skills/servicenow-incident-assistant/SKILL.md` | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C895 | T1 | `.agents/skills/shopify-developer/SKILL.md` | Shopify reference: Liquid, themes, GraphQL, Hydrogen, Functions. Use for .liquid files or Shopify apps. Do NOT use for other e-commerce platforms. |
| C896 | T1 | `.agents/skills/shopify-developer/SKILL.md` | Read and follow `00_skills/(development)/shopify-developer/SKILL.md` and its relevant local modules. |
| C897 | T1 | `.agents/skills/shopify-developer/SKILL.md` | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C898 | T1 | `.agents/skills/simulator-ai/SKILL.md` | Build a governed AI medical simulator. Use for simulator construction. Never hallucinates or invents results; do NOT use for unrelated stacks. |
| C899 | T1 | `.agents/skills/simulator-ai/SKILL.md` | Read and follow `00_skills/(development)/simulator-ai/SKILL.md` and its relevant local modules. |
| C900 | T1 | `.agents/skills/simulator-ai/SKILL.md` | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C901 | T1 | `.agents/skills/skill-architect/SKILL.md` | Build, score and improve reusable skills with minimal evidence-based edits. Use for creating or reviewing skills. Do NOT use for agent identities. |
| C902 | T1 | `.agents/skills/skill-architect/SKILL.md` | Read and follow `00_skills/(creation)/skill-architect/SKILL.md` and its relevant local modules. |
| C903 | T1 | `.agents/skills/skill-architect/SKILL.md` | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C904 | T1 | `.agents/skills/skill-factory/SKILL.md` | Create, refactor and validate workspace skills with precise routing. Use for criar or refatorar skills. Do NOT use for agent identities. |
| C905 | T1 | `.agents/skills/skill-factory/SKILL.md` | Read and follow `00_skills/(creation)/skill-factory/SKILL.md` and its relevant local modules. |
| C906 | T1 | `.agents/skills/skill-factory/SKILL.md` | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C907 | T1 | `.agents/skills/skill-factory-generator/SKILL.md` | Generate a bounded reusable skill package with routing and verifiable gates. Use for skill generation. Do NOT use for unrelated coding. |
| C908 | T1 | `.agents/skills/skill-factory-generator/SKILL.md` | Read and follow `00_skills/(creation)/skill-factory-generator/SKILL.md` and its relevant local modules. |
| C909 | T1 | `.agents/skills/skill-factory-generator/SKILL.md` | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C910 | T1 | `.agents/skills/skill-hardener/SKILL.md` | Harden skills with contracts, forbidden actions and quality gates. Use for skill hardening. Do NOT use for unrelated coding. |
| C911 | T1 | `.agents/skills/skill-hardener/SKILL.md` | Read and follow `00_skills/(creation)/skill-hardener/SKILL.md` and its relevant local modules. |
| C912 | T1 | `.agents/skills/skill-hardener/SKILL.md` | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C913 | T1 | `.agents/skills/slo-risk-analyzer/SKILL.md` | Map engineering operations to SLO/SLA risks and error budgets. Use for SLO risk analysis. Do NOT use for unmeasured speculative tuning. |
| C914 | T1 | `.agents/skills/slo-risk-analyzer/SKILL.md` | Read and follow `00_skills/(performance)/slo-risk-analyzer/SKILL.md` and its relevant local modules. |
| C915 | T1 | `.agents/skills/slo-risk-analyzer/SKILL.md` | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C916 | T1 | `.agents/skills/social-media-operator/SKILL.md` | Governed TikTok/Instagram operations via cookie or browser sessions. Use for social profile reads. Do NOT use for OAuth keys or developer accounts. |
| C917 | T1 | `.agents/skills/social-media-operator/SKILL.md` | Read and follow `00_skills/(tooling)/social-media-operator/SKILL.md` and its relevant local modules. |
| C918 | T1 | `.agents/skills/social-media-operator/SKILL.md` | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C919 | T1 | `.agents/skills/social-selling/SKILL.md` | LinkedIn social selling: profile optimization, DM sequences, DM-to-deal conversion. Use for LinkedIn selling. Do NOT use for code work. |
| C920 | T1 | `.agents/skills/social-selling/SKILL.md` | Read and follow `00_skills/(gtm)/social-selling/SKILL.md` and its relevant local modules. |
| C921 | T1 | `.agents/skills/social-selling/SKILL.md` | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C922 | T1 | `.agents/skills/solo-founder-gtm/SKILL.md` | GTM playbook for solo founders: stack, AI agent team, revenue stages, hiring. Use for solo-founder GTM. Do NOT use for code work. |
| C923 | T1 | `.agents/skills/solo-founder-gtm/SKILL.md` | Read and follow `00_skills/(gtm)/solo-founder-gtm/SKILL.md` and its relevant local modules. |
| C924 | T1 | `.agents/skills/solo-founder-gtm/SKILL.md` | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C925 | T1 | `.agents/skills/solve-problems/SKILL.md` | Fix defects across any language without changing project architecture. Use for defect fixes. Do NOT use for unrelated stacks or deployment. |
| C926 | T1 | `.agents/skills/solve-problems/SKILL.md` | Read and follow `00_skills/(development)/solve-problems/SKILL.md` and its relevant local modules. |
| C927 | T1 | `.agents/skills/solve-problems/SKILL.md` | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C928 | T1 | `.agents/skills/spec-driven/SKILL.md` | Spec-driven 4.0.0 (TLC): specify, design, tasks, execute with EARS and mutation checks. Use for feature specs. Do NOT use for pure architecture. |
| C929 | T1 | `.agents/skills/spec-driven/SKILL.md` | Read and follow `00_skills/(development)/spec-driven/SKILL.md` and its relevant local modules. |
| C930 | T1 | `.agents/skills/spec-driven/SKILL.md` | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C931 | T1 | `.agents/skills/spec-driven-eval/SKILL.md` | Grade how fully an implementation fulfills a PRD, with one comparable score. Use when explicitly named. Do NOT use to build (tlc-spec-driven). |
| C932 | T1 | `.agents/skills/spec-driven-eval/SKILL.md` | Read and follow `00_skills/(development)/spec-driven-eval/SKILL.md` and its relevant local modules. |
| C933 | T1 | `.agents/skills/spec-driven-eval/SKILL.md` | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C934 | T1 | `.agents/skills/spec-driven-lean/SKILL.md` | Tech Lead Club spec-lean 2.0.0: freeze obligations in proof-backed checks, then build. Use for spec-driven-lean work. Do NOT use for design docs. |
| C935 | T1 | `.agents/skills/spec-driven-lean/SKILL.md` | Read and follow `00_skills/(development)/spec-driven-lean/SKILL.md` and its relevant local modules. |
| C936 | T1 | `.agents/skills/spec-driven-lean/SKILL.md` | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C937 | T1 | `.agents/skills/specs/SKILL.md` | Require a spec before implementation: scope, checks, risks. Use for pre-implementation contracts. Do NOT use to override approved requirements. |
| C938 | T1 | `.agents/skills/specs/SKILL.md` | Read and follow `00_skills/(development)/specs/SKILL.md` and its relevant local modules. |
| C939 | T1 | `.agents/skills/specs/SKILL.md` | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C940 | T1 | `.agents/skills/splunk-observability-staff/SKILL.md` | Splunk analysis: searches, metrics, logs, traces, notable events. Use for Splunk work. Do NOT use to mutate live systems unless authorized. |
| C941 | T1 | `.agents/skills/splunk-observability-staff/SKILL.md` | Read and follow `00_skills/(monitoring)/splunk-observability-staff/SKILL.md` and its relevant local modules. |
| C942 | T1 | `.agents/skills/splunk-observability-staff/SKILL.md` | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C943 | T1 | `.agents/skills/staff-iii-architecture-governor/SKILL.md` | Plan and select architecture for new projects or changes. Use for architecture selection. Do NOT use for implementation or deployment. |
| C944 | T1 | `.agents/skills/staff-iii-architecture-governor/SKILL.md` | Read and follow `00_skills/(architecture)/staff-iii-architecture-governor/SKILL.md` and its relevant local modules. |
| C945 | T1 | `.agents/skills/staff-iii-architecture-governor/SKILL.md` | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C946 | T1 | `.agents/skills/staff-tdd-code-builder/SKILL.md` | Create or change code from an architecture plan using TDD by default. Use for TDD builds from a plan. Do NOT use for unrelated stacks or deployment. |
| C947 | T1 | `.agents/skills/staff-tdd-code-builder/SKILL.md` | Read and follow `00_skills/(development)/staff-tdd-code-builder/SKILL.md` and its relevant local modules. |
| C948 | T1 | `.agents/skills/staff-tdd-code-builder/SKILL.md` | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C949 | T1 | `.agents/skills/studio-creation-tlc/SKILL.md` | TLC rule for Dark Videos media (spec-driven, Spotify). Use for media creation with a role skill. Do NOT use as substitute or to upload mined files. |
| C950 | T1 | `.agents/skills/studio-creation-tlc/SKILL.md` | Read and follow `00_skills/(tooling)/studio-creation-tlc/SKILL.md` and its relevant local modules. |
| C951 | T1 | `.agents/skills/studio-creation-tlc/SKILL.md` | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C952 | T1 | `.agents/skills/subagent-creator/SKILL.md` | Design bounded lenses of codenavi-agent with one deliverable and a verdict. Use for verifier or audit units. Do NOT use to create agent identities. |
| C953 | T1 | `.agents/skills/subagent-creator/SKILL.md` | Read and follow `00_skills/(creation)/subagent-creator/SKILL.md` and its relevant local modules. |
| C954 | T1 | `.agents/skills/subagent-creator/SKILL.md` | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C955 | T1 | `.agents/skills/supply-chain-auditor/SKILL.md` | Audit dependency provenance and release integrity. Use for supply-chain audits. Do NOT use outside authorized scope or to expose secrets. |
| C956 | T1 | `.agents/skills/supply-chain-auditor/SKILL.md` | Read and follow `00_skills/(security)/supply-chain-auditor/SKILL.md` and its relevant local modules. |
| C957 | T1 | `.agents/skills/supply-chain-auditor/SKILL.md` | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C958 | T1 | `.agents/skills/tactical-ddd/SKILL.md` | Detect anemic domain models and refactor to rich DDD models. Use for DDD model reviews. Do NOT use for service boundaries or DTOs. |
| C959 | T1 | `.agents/skills/tactical-ddd/SKILL.md` | Read and follow `00_skills/(architecture)/tactical-ddd/SKILL.md` and its relevant local modules. |
| C960 | T1 | `.agents/skills/tactical-ddd/SKILL.md` | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C961 | T1 | `.agents/skills/task-graph-builder/SKILL.md` | Build a deterministic task graph from a playbook and objective. Use for task graphs. Do NOT use for unapproved remote writes. |
| C962 | T1 | `.agents/skills/task-graph-builder/SKILL.md` | Read and follow `00_skills/(tooling)/task-graph-builder/SKILL.md` and its relevant local modules. |
| C963 | T1 | `.agents/skills/task-graph-builder/SKILL.md` | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C964 | T1 | `.agents/skills/technical-design-doc-creator/SKILL.md` | Create architecture-level technical design docs via discovery. Use for 'write a design doc' or 'criar um TDD'. Do NOT use for README or API docs. |
| C965 | T1 | `.agents/skills/technical-design-doc-creator/SKILL.md` | Read and follow `00_skills/(creation)/create-technical-design-doc/SKILL.md` and its relevant local modules. |
| C966 | T1 | `.agents/skills/technical-design-doc-creator/SKILL.md` | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C967 | T1 | `.agents/skills/telemetry-bug-root-cause-solver/SKILL.md` | Resolve bugs from logs, metrics and traces via runtime evidence and code. Use for telemetry RCA. Do NOT use to mutate live systems unless authorized. |
| C968 | T1 | `.agents/skills/telemetry-bug-root-cause-solver/SKILL.md` | Read and follow `00_skills/(monitoring)/telemetry-bug-root-cause-solver/SKILL.md` and its relevant local modules. |
| C969 | T1 | `.agents/skills/telemetry-bug-root-cause-solver/SKILL.md` | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C970 | T1 | `.agents/skills/test-gap-analyzer/SKILL.md` | Analyze test coverage gaps: untested modules and edge cases. Use for test gap analysis. Do NOT use as deployment approval or for unexecuted checks. |
| C971 | T1 | `.agents/skills/test-gap-analyzer/SKILL.md` | Read and follow `00_skills/(quality)/test-gap-analyzer/SKILL.md` and its relevant local modules. |
| C972 | T1 | `.agents/skills/test-gap-analyzer/SKILL.md` | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C973 | T1 | `.agents/skills/test-generation/SKILL.md` | Detect test gaps and generate proposed tests in a sandbox. Use for test generation. Do NOT use as deployment approval or for unexecuted checks. |
| C974 | T1 | `.agents/skills/test-generation/SKILL.md` | Read and follow `00_skills/(quality)/test-generation/SKILL.md` and its relevant local modules. |
| C975 | T1 | `.agents/skills/test-generation/SKILL.md` | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C976 | T1 | `.agents/skills/test-strategy-architect/SKILL.md` | Build test strategy: unit, contract, e2e, security, performance. Use for test planning. Do NOT use as deployment approval or for unexecuted checks. |
| C977 | T1 | `.agents/skills/test-strategy-architect/SKILL.md` | Read and follow `00_skills/(quality)/test-strategy-architect/SKILL.md` and its relevant local modules. |
| C978 | T1 | `.agents/skills/test-strategy-architect/SKILL.md` | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C979 | T1 | `.agents/skills/test-writer/SKILL.md` | Generate proposed tests in a sandbox from evidence; never real test dirs. Use for test proposals. Do NOT use as approval or for unexecuted checks. |
| C980 | T1 | `.agents/skills/test-writer/SKILL.md` | Read and follow `00_skills/(quality)/test-writer/SKILL.md` and its relevant local modules. |
| C981 | T1 | `.agents/skills/test-writer/SKILL.md` | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C982 | T1 | `.agents/skills/tests-expert/SKILL.md` | Run real functional and e2e checks after a fix or new behavior. Use for fixes, new features or e2e tests. Do NOT use for unit tests or coverage. |
| C983 | T1 | `.agents/skills/tests-expert/SKILL.md` | Read and follow `00_skills/(quality)/tests-expert/SKILL.md` and its relevant local modules. |
| C984 | T1 | `.agents/skills/tests-expert/SKILL.md` | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C985 | T1 | `.agents/skills/the-fool/SKILL.md` | Stress-test a pending decision: threats, fragile assumptions, blind spots. Use for devil's advocate or pre-mortem. Do NOT use to decide for the owner. |
| C986 | T1 | `.agents/skills/the-fool/SKILL.md` | Read and follow `00_skills/(decision-making)/the-fool/SKILL.md` and its relevant local modules. |
| C987 | T1 | `.agents/skills/the-fool/SKILL.md` | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C988 | T1 | `.agents/skills/the-judge/SKILL.md` | Evidence-first PR judge: repo checks, correctness, security, one GitHub review. Use for 'review this PR' or 'julgue esse PR'. Do NOT use for CI fixes. |
| C989 | T1 | `.agents/skills/the-judge/SKILL.md` | Read and follow `00_skills/(quality)/the-judge/SKILL.md` and its relevant local modules. |
| C990 | T1 | `.agents/skills/the-judge/SKILL.md` | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C991 | T1 | `.agents/skills/the-jury/SKILL.md` | Tally a verdict on a decidable question through 3 or 5 orthogonal lenses. Use for decision panels. Do NOT use to spawn agents or implement. |
| C992 | T1 | `.agents/skills/the-jury/SKILL.md` | Read and follow `00_skills/(decision-making)/the-jury/SKILL.md` and its relevant local modules. |
| C993 | T1 | `.agents/skills/the-jury/SKILL.md` | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C994 | T1 | `.agents/skills/threat-modeler/SKILL.md` | Produce AEOS threat models for prompt injection, tool poisoning and secret leakage. Use for AEOS threat models. Do NOT use outside authorized scope. |
| C995 | T1 | `.agents/skills/threat-modeler/SKILL.md` | Read and follow `00_skills/(security)/threat-modeler/SKILL.md` and its relevant local modules. |
| C996 | T1 | `.agents/skills/threat-modeler/SKILL.md` | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C997 | T1 | `.agents/skills/tlc-discover/SKILL.md` | Interview an unshaped idea into a verdict and design doc. Use for 'should we build this' or discovery. Do NOT use to cut tasks or implement. |
| C998 | T1 | `.agents/skills/tlc-discover/SKILL.md` | Read and follow `00_skills/(development)/tlc-discover/SKILL.md` and its relevant local modules. |
| C999 | T1 | `.agents/skills/tlc-discover/SKILL.md` | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C1000 | T1 | `.agents/skills/tlc-generative-engine-optimization/SKILL.md` | Make pages citable by AI answer engines (GEO): schema, llms.txt, structure. Use for GEO or AI citability. Do NOT use for AI SEO strategy (ai-seo). |
| C1001 | T1 | `.agents/skills/tlc-generative-engine-optimization/SKILL.md` | Read and follow `00_skills/(quality)/tlc-generative-engine-optimization/SKILL.md` and its relevant local modules. |
| C1002 | T1 | `.agents/skills/tlc-generative-engine-optimization/SKILL.md` | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C1003 | T1 | `.agents/skills/tlc-implement/SKILL.md` | Implement planned work: extract a checklist, build it, prove each check. Use for 'build this ticket'. Do NOT use to design the work. |
| C1004 | T1 | `.agents/skills/tlc-implement/SKILL.md` | Read and follow `00_skills/(development)/tlc-implement/SKILL.md` and its relevant local modules. |
| C1005 | T1 | `.agents/skills/tlc-implement/SKILL.md` | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C1006 | T1 | `.agents/skills/tlc-plan/SKILL.md` | Turn a decided PRD or design doc into tasks with observable criteria. Use for task cutting. Do NOT use for discovery or implementation. |
| C1007 | T1 | `.agents/skills/tlc-plan/SKILL.md` | Read and follow `00_skills/(development)/tlc-plan/SKILL.md` and its relevant local modules. |
| C1008 | T1 | `.agents/skills/tlc-plan/SKILL.md` | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C1009 | T1 | `.agents/skills/tlc-prd/SKILL.md` | Interview an idea into a PRD: problem, success, boundaries, journeys. Use for 'write the PRD'. Do NOT use to design solutions or cut tasks. |
| C1010 | T1 | `.agents/skills/tlc-prd/SKILL.md` | Read and follow `00_skills/(development)/tlc-prd/SKILL.md` and its relevant local modules. |
| C1011 | T1 | `.agents/skills/tlc-prd/SKILL.md` | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C1012 | T1 | `.agents/skills/tlc-spec-driven/SKILL.md` | TLC spec-driven 4.0.0: specify, design, tasks, execute with EARS and proof checks. Use for feature specs. Do NOT use for pure architecture. |
| C1013 | T1 | `.agents/skills/tlc-spec-driven/SKILL.md` | Read and follow `00_skills/(development)/tlc-spec-driven/SKILL.md` and its relevant local modules. |
| C1014 | T1 | `.agents/skills/tlc-spec-driven/SKILL.md` | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C1015 | T1 | `.agents/skills/tlc-spec-lean/SKILL.md` | TLC spec-lean 2.0.0: freeze obligations in proof-backed checks, then build. Use for plan feature or write checks. Do NOT use for design docs. |
| C1016 | T1 | `.agents/skills/tlc-spec-lean/SKILL.md` | Read and follow `00_skills/(development)/tlc-spec-lean/SKILL.md` and its relevant local modules. |
| C1017 | T1 | `.agents/skills/tlc-spec-lean/SKILL.md` | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C1018 | T1 | `.agents/skills/token-budget-governor/SKILL.md` | Prevent token waste with scoped prompts, compact context and narrow lenses. Use for token budget governance. Do NOT use to promote unverified claims. |
| C1019 | T1 | `.agents/skills/token-budget-governor/SKILL.md` | Read and follow `00_skills/(learning)/token-budget-governor/SKILL.md` and its relevant local modules. |
| C1020 | T1 | `.agents/skills/token-budget-governor/SKILL.md` | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C1021 | T1 | `.agents/skills/tool-router-audit/SKILL.md` | Audit whether AEOS code and playbooks enforce Tool Router for external actions. Use for Tool Router audits. Do NOT use for unapproved remote writes. |
| C1022 | T1 | `.agents/skills/tool-router-audit/SKILL.md` | Read and follow `00_skills/(tooling)/tool-router-audit/SKILL.md` and its relevant local modules. |
| C1023 | T1 | `.agents/skills/tool-router-audit/SKILL.md` | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C1024 | T1 | `.agents/skills/typesafe-ai/SKILL.md` | Build AI features with TypeSafe models (Jev): typed judgments as code primitives. Use for programmable AI decisions. Do NOT use for unrelated stacks. |
| C1025 | T1 | `.agents/skills/typesafe-ai/SKILL.md` | Read and follow `00_skills/(development)/typesafe-ai/SKILL.md` and its relevant local modules. |
| C1026 | T1 | `.agents/skills/typesafe-ai/SKILL.md` | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C1027 | T1 | `.agents/skills/unique-environment-auditor/SKILL.md` | Audit an environment inventory for conflicting versions and unmet runtime needs. Use for environment audits. Do NOT use for unrelated stacks. |
| C1028 | T1 | `.agents/skills/unique-environment-auditor/SKILL.md` | Read and follow `00_skills/(development)/unique-environment-auditor/SKILL.md` and its relevant local modules. |
| C1029 | T1 | `.agents/skills/unique-environment-auditor/SKILL.md` | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C1030 | T1 | `.agents/skills/universal-project-factory/SKILL.md` | Plan and generate sandbox-first projects from zero to production for any stack. Use for project generation. Do NOT use for ordinary one-off coding. |
| C1031 | T1 | `.agents/skills/universal-project-factory/SKILL.md` | Read and follow `00_skills/(creation)/universal-project-factory/SKILL.md` and its relevant local modules. |
| C1032 | T1 | `.agents/skills/universal-project-factory/SKILL.md` | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C1033 | T1 | `.agents/skills/v1-readiness-auditor/SKILL.md` | Validate AEOS against v1.0 release gates and generate a blocking report. Use for v1 readiness checks. Do NOT use as deployment approval. |
| C1034 | T1 | `.agents/skills/v1-readiness-auditor/SKILL.md` | Read and follow `00_skills/(quality)/v1-readiness-auditor/SKILL.md` and its relevant local modules. |
| C1035 | T1 | `.agents/skills/v1-readiness-auditor/SKILL.md` | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C1036 | T1 | `.agents/skills/vercel-deploy/SKILL.md` | Deploy apps and websites to Vercel, including previews. Use for Vercel deploys or live links. Do NOT use for Netlify, Cloudflare or Render. |
| C1037 | T1 | `.agents/skills/vercel-deploy/SKILL.md` | Read and follow `00_skills/(cloud)/vercel-deploy/SKILL.md` and its relevant local modules. |
| C1038 | T1 | `.agents/skills/vercel-deploy/SKILL.md` | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C1039 | T1 | `.agents/skills/video-outreach/SKILL.md` | Video-first cold outreach: personalized video at scale, async selling, AI demos. Use for video prospecting. Do NOT use for code work. |
| C1040 | T1 | `.agents/skills/video-outreach/SKILL.md` | Read and follow `00_skills/(gtm)/video-outreach/SKILL.md` and its relevant local modules. |
| C1041 | T1 | `.agents/skills/video-outreach/SKILL.md` | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C1042 | T1 | `.agents/skills/voiceai/SKILL.md` | Voice interface for AEOS; activation is consent for authorized audio only. Use for voice input or transcription. Do NOT use for remote writes. |
| C1043 | T1 | `.agents/skills/voiceai/SKILL.md` | Read and follow `00_skills/(tooling)/voiceai/SKILL.md` and its relevant local modules. |
| C1044 | T1 | `.agents/skills/voiceai/SKILL.md` | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C1045 | T1 | `.agents/skills/vox-aurum/SKILL.md` | Transcribe authorized bare audio offline with local Whisper. Use for offline transcription. Do NOT use for meeting video (acta-aurea). |
| C1046 | T1 | `.agents/skills/vox-aurum/SKILL.md` | Read and follow `00_skills/(tooling)/vox-aurum/SKILL.md` and its relevant local modules. |
| C1047 | T1 | `.agents/skills/vox-aurum/SKILL.md` | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C1048 | T1 | `.agents/skills/vuln-obsol-recon/SKILL.md` | Assess CVE and EOL risk. Use for CVE checks. Do NOT use for base sync, patching or invented versions without manifests/runtime evidence. |
| C1049 | T1 | `.agents/skills/vuln-obsol-recon/SKILL.md` | Read and follow `00_skills/(security)/vuln-obsol-recon/SKILL.md` and its relevant local modules. |
| C1050 | T1 | `.agents/skills/vuln-obsol-recon/SKILL.md` | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C1051 | T1 | `.agents/skills/web-accessibility/SKILL.md` | Audit and improve web accessibility to WCAG 2.1. Use for a11y audits. Do NOT use for SEO or performance work. |
| C1052 | T1 | `.agents/skills/web-accessibility/SKILL.md` | Read and follow `00_skills/(quality)/web-accessibility/SKILL.md` and its relevant local modules. |
| C1053 | T1 | `.agents/skills/web-accessibility/SKILL.md` | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C1054 | T1 | `.agents/skills/web-best-practices/SKILL.md` | Apply modern web security, compatibility and code-quality checks. Use for web best-practice reviews. Do NOT use for accessibility, SEO or full audits. |
| C1055 | T1 | `.agents/skills/web-best-practices/SKILL.md` | Read and follow `00_skills/(quality)/web-best-practices/SKILL.md` and its relevant local modules. |
| C1056 | T1 | `.agents/skills/web-best-practices/SKILL.md` | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C1057 | T1 | `.agents/skills/web-design-guidelines/SKILL.md` | Review UI code against Web Interface Guidelines: visual and interaction patterns. Use for 'review my UI'. Do NOT use for performance or SEO audits. |
| C1058 | T1 | `.agents/skills/web-design-guidelines/SKILL.md` | Read and follow `00_skills/(design)/web-design-guidelines/SKILL.md` and its relevant local modules. |
| C1059 | T1 | `.agents/skills/web-design-guidelines/SKILL.md` | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C1060 | T1 | `.agents/skills/web-quality-audit/SKILL.md` | Multi-area web audit: performance, accessibility, SEO, best practices. Use for 'audit my site'. Do NOT use for single-area work. |
| C1061 | T1 | `.agents/skills/web-quality-audit/SKILL.md` | Read and follow `00_skills/(quality)/web-quality-audit/SKILL.md` and its relevant local modules. |
| C1062 | T1 | `.agents/skills/web-quality-audit/SKILL.md` | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C1063 | T1 | `.agents/skills/whatsapp-simulator/SKILL.md` | Generate synthetic WhatsApp-style conversation fixtures for testing. Use for chat fixtures. Do NOT use for unapproved remote writes. |
| C1064 | T1 | `.agents/skills/whatsapp-simulator/SKILL.md` | Read and follow `00_skills/(tooling)/whatsapp-simulator/SKILL.md` and its relevant local modules. |
| C1065 | T1 | `.agents/skills/whatsapp-simulator/SKILL.md` | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C1066 | T1 | `.agents/skills/wordpress-expert/SKILL.md` | Staff-level WordPress super-skill: site mapping, clean-code changes, plugins, themes. Use for WordPress work. Do NOT use for unrelated stacks. |
| C1067 | T1 | `.agents/skills/wordpress-expert/SKILL.md` | Read and follow `00_skills/(development)/wordpress-expert/SKILL.md` and its relevant local modules. |
| C1068 | T1 | `.agents/skills/wordpress-expert/SKILL.md` | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| C1069 | T1 | `.agents/skills/workbench-profile-resolver/SKILL.md` | Resolve the smallest compatible workbench profile from scope and constraints. Use for profile selection. Do NOT use for unapproved remote writes. |
| C1070 | T1 | `.agents/skills/workbench-profile-resolver/SKILL.md` | Read and follow `00_skills/(tooling)/workbench-profile-resolver/SKILL.md` and its relevant local modules. |
| C1071 | T1 | `.agents/skills/workbench-profile-resolver/SKILL.md` | Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity. |
| P003 | T1 | `.agents/skills/workflow-tips/SKILL.md` | Prefer clear variable names and small functions when writing code. |
| P004 | T1 | `.agents/skills/workflow-tips/SKILL.md` | Keep layers thin and delegate work to the appropriate lower layer. |
| P005 | T0 | `AGENTS.md` | Never commit secrets, API keys, or credentials into the repository; use environment configuration outside version control. |
| P006 | T0 | `AGENTS.md` | Known caveat: commands that pass locally can still fail in CI when they depend on machine-local env vars or secrets that are not present in the pipeline; prefer the project's documented CI entrypoint when validating. |

## Output

Write scores as a table: `| ID | Cost | Class | Evidence | Confidence | Trim suggestion |`

