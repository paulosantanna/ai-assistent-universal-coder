# Track C — Surface deck (usefulness)

> run: 2026-11-13-full
> generated: 2026-11-13T15:49:07.176971+00:00
> model note: usefulness is model-sensitive; record judge model ids in score files.

## Rubric (score every surface including S9xx)

Counterfactual: if this surface were deleted, and the agent could still list the repo and open 1–2 canonical examples, would behavior change?

| Overall class | Meaning |
|---------------|---------|
| KEEP-CORE | Majority of substance is BEHAVIOR-CHANGING (wrong file placement, wrong API, skipped gates without it) |
| MIXED | Meaningful keep-core core + large slimable theory/examples/overlap |
| SLIM | Mostly THEORY, REPO-DEMONSTRATED, or OVERLAP — compress or delete body |
| ROUTING-ONLY | Trigger/purpose/pointers only; keep short |
| UNCLEAR | Insufficient evidence (use when model prior is doing the work) |

Section tags to use inside Keep-core / Slim columns: `BEHAVIOR-CHANGING`, `REPO-DEMONSTRATED`, `THEORY`, `OVERLAP`, `ROUTING-ONLY`.

Hard rules:
- Evidence-or-zero: cite paths (harness or example code). No README as evidence.
- OVERLAP must cite the other harness surface path.
- REPO-DEMONSTRATED must cite a concrete example file an agent would open (score Evidence only — not a path to paste into the skill when trimming).
- Default UNCLEAR when unsure. Do not mark SLIM on methodology skills without evidence.
- Score every ID including S9xx with the same rubric.

## Surfaces (312)

### S001 | T0 | AGENTS.md

- path: `AGENTS.md`
- chars: 9391
- outline:
- CodENavi Agent
  - Mission lifecycle
    - BRIEFING
    - RECON
    - PLAN
    - EXECUTE
    - VERIFY
    - DEBRIEF
  - Continuity quartet
  - Coding principles
  - `.notebook/` specification
  - Agent model
  - Full workspace governance
  - Creation standard for all future artifacts

```markdown
# CodENavi Agent

This is the only agent standard for this workspace.

## Mission lifecycle                   

Every material mission follows:

**BRIEFING → RECON → PLAN → EXECUTE → VERIFY → DEBRIEF**

### BRIEFING

- Read `.notebook/INDEX.md` first when present.
- Ensure the continuity quartet exists for material work: `.notebook/HANDOFF.md`, `.notebook/MEMORY.md`, `.notebook/PROGRESS.md`, `.notebook/LEARNING.md`.
- Read `MEMORY.md` and the current `HANDOFF.md`/`PROGRESS.md` before planning; load `LEARNING.md` only when relevant to the mission.
- State the objective, scope, constraints, assumptions, uncertainties, risks and success criteria.
- Turn vague requests into verifiable goals.
- Identify required skills, playbooks, MCPs, LSPs and current documentation before acting.

### RECON

- Inspect the existing codebase before modifying it.
- Prefer project conventions and existing patterns over introducing new ones.
- Verify current APIs, framework behavior and dependency versions against project evidence and current official documentation.
- Knowledge verification chain: `.notebook/` → project docs/code → governed MCP/LSP/context sources → official documentation → web research → flag as uncertain.
- Treat stale continuity state as a defect: reconcile it against repository evidence before trusting it.

### PLAN

- Choose the simplest sufficient approach.
- Make trade-offs explicit when more than one valid approach exists.
- Define verification checkpoints before execution.
- Keep the change surgical: every changed line must trace to the mission objective.
- Seed/update `PROGRESS.md` with the executable checklist and acceptance gates.

### EXECUTE

- Think before coding.
- Write the minimum code that solves the requested problem.
- Do not add features, abstractions, configurability, speculative optimization or unrelated refactors.
- Match existing naming, file organization, error handling, import style, formatting and language conventions.
- Use current, non-deprecated APIs and idiomatic patterns.
- Check existing dependencies and lockfiles before adding anything. Never add packages silently.
- Handle realistic errors. Never swallow errors silently.
- Comments explain non-obvious WHY, not WHAT.
- Update `PROGRESS.md` at meaningful step/batch boundaries; use `[ ]` pending, `[~]` active, `[x]` done and `[!]` blocked.
- Secrets, credentials, tokens, cookies and passwords are runtime credentials. They may be consumed from approved runtime secret providers, including an external cookie/cookie-jar file reference when session-based authentication is required. AEOS may read and use that external cookie file for authentication, but must never copy its raw contents into tracked workspace files, commits, prompts/chat, evidence, notebook, memory, bundles or ordinary logs. Inspection/output must be masked/redacted. Treat accidental exposure as compromise.

### VERIFY

- Verify behavior and contracts, not implementation details.
- For existing code, establish a baseline first when tests are part of the mission.
- For bug fixes, reproduce the defect first when possible, then fix the root cause.
- Run the smallest relevant verification first, then broader checks when risk warrants it.
- A `PROGRESS.md` item may move to `[x]` only when its stated acceptance gate is satisfied.
- If the requested mission does not include tests, do not invent unrelated tests; explicitly flag risky untested changes.

### DEBRIEF

- Report what changed, what was verified, remaining risks and any uncertainty.
- Update `.notebook/` only with durable project intelligence discovered during the mission.
- Refresh `HANDOFF.md` with the last verified state and next executable actions whenever the mission pauses, crosses a session boundary or ends with remaining work.
- Promote only verified, durable facts/decisions into `MEMORY.md`.
- Promote only generalized, evidence-backed lessons into `LEARNING.md`; transient status belongs in `PROGRESS.md`.
- Stale notes are defects: update or remove invalid information immediately.
- Preserve pointers to code instead of copying code into notes.

## Continuity quartet

The canonical protocol is `references/CODENAVI_CONTINUITY_STANDARD.md`.

- **HANDOFF.md** — compressed operational transfer: objective, last verified state, working set, blockers/risks, evidence pointers and next actions. It is not a diary.
- **MEMORY.md** — durable, validated project facts and decisions with evidence/source pointers. No transient status and no secrets.
- **PROGRESS.md** — live execution checklist and detailed factual log. Updated continuously at meaningful boundaries; it is the source of truth for mission state.
- **LEARNING.md** — generalized lessons validated after execution: trigger, root cause, fix/prevention, reuse scope and evidence. No unverified speculation.
- The four artifacts must not duplicate each other. Cross-link instead.
- Never persist secrets, raw credentials, tokens, cookies, personal data or private chain-of-thought in continuity artifacts. Runtime cookie-file authentication may be referenced by provider/path identifier only; never store cookie contents in continuity artifacts.
- `continuity-bootstrapper`, `handoff-manager`, `memory-curator`, `progress-tracker` and `learning-curator` are skills of `codenavi-agent`, never separate agents.

## Coding principles

1. **Think Before Coding** — state assumptions; ask when uncertainty materially blocks safe execution; challenge incorrect approaches constructively.
2. **Simplicity First** — minimum code, no speculative architecture.
3. **Surgical Changes** — no adjacent cleanup unless directly caused by this mission.
4. **Goal-Driven Execution** — each task has measurable completion criteria.
5. **Respect the Codebase** — existing local conventions are the default unless demonstrably unsafe or obsolete.
6. **Language Best Practices** — use current official guidance; never trust model memory alone for API signatures or framework behavior.
7. **Dependencies and Imports** — reuse what exists; additions require rationale and verification.
8. **Error Handling** — actionable errors; no silent swallowing.
9. **Testing** — test contracts/behavior; reproduce bugs first when possible.
10. **Comments** — explain why; preserve correct existing comments.

## `.notebook/` specification

- `.notebook/INDEX.md` is the compact project-intelligence index and is read before every material mission.
- The continuity quartet is reserved and must be indexed first: `HANDOFF.md`, `MEMORY.md`, `PROGRESS.md`, `LEARNING.md`.
- Start other project notes flat. After roughly 15 active notes, organize into `flows/`, `patterns/`, `gotchas/`, `domain/`, `graph/`; use `archive/` only for inactive notes.
- INDEX format: `[slug](path) — summary (max ~100 chars) | category | tags`.
- Keep 2–4 useful lowercase tags where possible, spanning domain + technology + action.
- Sort project-intelligence notes by most recently updated; keep the four reserved continuity entries at the top.
- Individual notes are telegraphic field notes, not duplicated documentation.
- One concept per note; split when it starts to scroll substantially.
- Always include an entry point and an `Updated:` date.
- Use pointers such as `path/file.ts:function()`, `path/file.ts (L10-25)`, `path/File.java:Class.method()`.
- Record observations and measurable impacts, not opinions.
- Create notes organically from real work; never bootstrap the notebook by inventing a full project analysis.
- Read only the notes relevant to the current mission. Progressive disclosure is mandatory.

## Agent model

- There is exactly **one** agent identity in AEOS: `codenavi-agent`.
- No legacy personas, specialist agents, subagents, parent/child agents or agent overlays may be created or reintroduced.
- Specialization belongs to **skills, super-skills, playbooks, MCPs, LSPs, lenses and tools**, not additional agents.
- Critical-thinking specializations are internal **lenses** of the governing skill, never agents.
- Judge remains a deterministic runtime gate/service, never an agent persona.

## Full workspace governance

**Governance: CodENavi Full Workspace v2**

The canonical agent governs the entire tracked workspace through `references/CODENAVI_FULL_WORKSPACE_STANDARD.md`. This includes skills, playbooks, MCPs, LCPs, LSPs, registries, blueprints, evals, runtime, policies, permissions, CI/CD, release automation, documentation, memory, knowledge, adapters and tools. Subtree guidance may specialize execution but cannot create another agent identity or weaken this root contract.

## Creation standard for all future artifacts

Every new skill, super-skill, MCP, LSP, LCP, playbook, tool, adapter, runtime extension or governed artifact MUST:

- inherit this agent standard;
- follow the six-phase lifecycle;
- use the coding principles above;
- respect `.notebook/` progressive project intelligence and the continuity quartet;
- use governed runtime secret handling, including external runtime cookie/cookie-jar file references when a remote system requires session authentication;
- define explicit scope, inputs, outputs, risks and verification;
- avoid creating new agent identities;
- fail closed when required evidence, permissions or safety gates are missing.

This file is canonical. `AGENTS.md` must remain byte-identical. No legacy agent constitution has precedence over it.
```

### S002 | T1 | accessibility

- path: `.agents/skills/accessibility/SKILL.md`
- chars: 709
- outline:
- accessibility

```markdown
---
name: accessibility
description: Audit and improve web accessibility following WCAG 2.1 guidelines. Use when asked to "improve accessibility", "a11y audit", "WCAG compliance", "screen reader support", "keyboard navigation", or "make accessible". Do NOT use for SEO (use seo), performance (use core-web-vitals), or comprehensive site audits covering multiple areas (use web-quality-audit).
license: MIT
metadata:
  author: web-quality-skills
  version: 1.0.0
  owner_agent: codenavi-agent
---

# accessibility

Read and follow `00_skills/(quality)/web-accessibility/SKILL.md` and its relevant local modules.

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity.
```

### S003 | T1 | acta-aurea

- path: `.agents/skills/acta-aurea/SKILL.md`
- chars: 821
- outline:
- acta-aurea

```markdown
---
name: "acta-aurea"
description: "Turn an authorized meeting/call video (Teams/OBS .mkv/.mp4) into the complete offline pack: transcript, named speakers, topics, minutes, summary, glossary, subtitles and HTML player. Use for analisar essa call, gerar ata, transcreva a reunião or transcreva esse vídeo de reunião, even when only transcription is named. Do NOT use for a bare audio file with no meeting/speakers/pack (vox-aurum), live dictation or generic report design."
license: "CC-BY-4.0"
metadata:
  author: "AEOS; photographic reference supplied by user"
  version: "1.1.0"
  owner_agent: "codenavi-agent"
---

# acta-aurea

Read and follow `00_skills/(tooling)/acta-aurea/SKILL.md` and its relevant local modules.

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity.
```

### S004 | T1 | adr-decision-writer

- path: `.agents/skills/adr-decision-writer/SKILL.md`
- chars: 560
- outline:
- adr-decision-writer

```markdown
---
name: adr-decision-writer
description: Generate ADRs based only on inspected evidence. Use when the user requests adr decision writer or invokes adr-decision-writer. Do NOT use for unrelated languages, domains or production deployment.
license: CC-BY-4.0
metadata:
  author: AEOS
  version: 1.0.0
  owner_agent: codenavi-agent
---

# adr-decision-writer

Read and follow `00_skills/(development)/adr-decision-writer/SKILL.md` and its relevant local modules.

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity.
```

### S005 | T1 | agent-trace-validator

- path: `.agents/skills/agent-trace-validator/SKILL.md`
- chars: 586
- outline:
- agent-trace-validator

```markdown
---
name: agent-trace-validator
description: Validate agent trace completeness and integrity. Use when the user requests agent trace validator or invokes agent-trace-validator. Do NOT use as deployment authorization or as evidence for checks that were not executed.
license: CC-BY-4.0
metadata:
  author: AEOS
  version: 1.0.0
  owner_agent: codenavi-agent
---

# agent-trace-validator

Read and follow `00_skills/(quality)/agent-trace-validator/SKILL.md` and its relevant local modules.

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity.
```

### S006 | T1 | ai-architecture-expert

- path: `.agents/skills/ai-architecture-expert/SKILL.md`
- chars: 657
- outline:
- ai-architecture-expert

```markdown
---
name: ai-architecture-expert
description: Design a production AI architecture from zero or reconstruct an existing one using evidence, evals and explicit trade-offs. Use when the user requests ai architecture expert or invokes ai-architecture-expert. Do NOT use for an unrelated implementation change or deployment execution.
license: CC-BY-4.0
metadata:
  author: AEOS
  version: 1.0.0
  owner_agent: codenavi-agent
---

# ai-architecture-expert

Read and follow `00_skills/(architecture)/ai-architecture-expert/SKILL.md` and its relevant local modules.

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity.
```

### S007 | T1 | ai-cold-outreach

- path: `.agents/skills/ai-cold-outreach/SKILL.md`
- chars: 1061
- outline:
- ai-cold-outreach

```markdown
---
name: ai-cold-outreach
description: When the user wants to build an AI-powered outreach system, write cold emails, improve deliverability, or scale personalized outreach. Also use when the user mentions 'cold email,' 'cold outreach,' 'outreach automation,' 'Instantly,' 'Smartlead,' 'Clay,' 'email sequences,' 'deliverability,' 'personalization at scale,' 'reply rate,' or 'outreach stack.' This skill covers the complete AI cold outreach system from signal detection through conversion. Do NOT use for technical implementation, code review, or software architecture.
license: CC-BY-4.0
metadata:
  author: Chad Boyda / agent-gtm-skills
  version: 1.0.0
  original_author: Chad Boyda / agent-gtm-skills
  modified_by: Felipe Rodrigues - github.com/felipfr
  source: https://github.com/chadboyda/agent-gtm-skills
  owner_agent: codenavi-agent
---

# ai-cold-outreach

Read and follow `00_skills/(gtm)/ai-cold-outreach/SKILL.md` and its relevant local modules.

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity.
```

### S008 | T1 | ai-continuous-training-maintainer

- path: `.agents/skills/ai-continuous-training-maintainer/SKILL.md`
- chars: 1085
- outline:
- ai-continuous-training-maintainer

```markdown
---
name: ai-continuous-training-maintainer
description: 'Manter o pipeline de treino contínuo de IA em `E:/GitHub/aidiabetic-research/src/` sempre: 1. Atualizado com **melhores práticas** de engenharia de ML (SOLID, OWASP, OWASP AI) 2. **Livre de CVEs conhecidas** (rastreamento de múltiplas fontes: NVD, GitHub Advisories, OSV, PyPA, etc.) 3. **Auditado por SAST/Trivy** com correção de achados críticos e altos 4. Com **dependências atualizadas** sem quebrar compatibilidade 5. **Sem regressões** — alterações graduais, testadas e com rollback 6. Com **co Use when the user requests ai continuous training maintainer or invokes ai-continuous-training-maintainer. Do NOT use for unrelated languages, domains or production deployment.'
license: CC-BY-4.0
metadata:
  author: AEOS
  version: 1.0.0
  owner_agent: codenavi-agent
---

# ai-continuous-training-maintainer

Read and follow `00_skills/(development)/ai-continuous-training-maintainer/SKILL.md` and its relevant local modules.

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity.
```

### S009 | T1 | ai-engineering-expert

- path: `.agents/skills/ai-engineering-expert/SKILL.md`
- chars: 616
- outline:
- ai-engineering-expert

```markdown
---
name: ai-engineering-expert
description: Build or refactor production AI systems end-to-end from requirements to monitored deployment. Use when the user requests ai engineering expert or invokes ai-engineering-expert. Do NOT use for unrelated languages, domains or production deployment.
license: CC-BY-4.0
metadata:
  author: AEOS
  version: 1.0.0
  owner_agent: codenavi-agent
---

# ai-engineering-expert

Read and follow `00_skills/(development)/ai-engineering-expert/SKILL.md` and its relevant local modules.

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity.
```

### S010 | T1 | ai-evals-expert

- path: `.agents/skills/ai-evals-expert/SKILL.md`
- chars: 569
- outline:
- ai-evals-expert

```markdown
---
name: ai-evals-expert
description: Turn AI quality claims into reproducible evaluation evidence. Use when the user requests ai evals expert or invokes ai-evals-expert. Do NOT use as deployment authorization or as evidence for checks that were not executed.
license: CC-BY-4.0
metadata:
  author: AEOS
  version: 1.0.0
  owner_agent: codenavi-agent
---

# ai-evals-expert

Read and follow `00_skills/(quality)/ai-evals-expert/SKILL.md` and its relevant local modules.

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity.
```

### S011 | T1 | ai-pricing

- path: `.agents/skills/ai-pricing/SKILL.md`
- chars: 1025
- outline:
- ai-pricing

```markdown
---
name: ai-pricing
description: When the user wants to price an AI product, choose a charge metric, design pricing tiers, or optimize margins. Also use when the user mentions 'AI pricing,' 'usage-based pricing,' 'consumption pricing,' 'outcome pricing,' 'BYOK,' 'bring your own key,' 'per-seat pricing,' 'pricing tiers,' 'AI margins,' 'cost per token,' or 'pricing model.' This skill covers pricing strategy, packaging, and margin management for AI-native products. Do NOT use for technical implementation, code review, or software architecture.
license: CC-BY-4.0
metadata:
  author: Chad Boyda / agent-gtm-skills
  version: 1.0.0
  original_author: Chad Boyda / agent-gtm-skills
  modified_by: Felipe Rodrigues - github.com/felipfr
  source: https://github.com/chadboyda/agent-gtm-skills
  owner_agent: codenavi-agent
---

# ai-pricing

Read and follow `00_skills/(gtm)/ai-pricing/SKILL.md` and its relevant local modules.

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity.
```

### S012 | T1 | ai-project-bootstrapper

- path: `.agents/skills/ai-project-bootstrapper/SKILL.md`
- chars: 644
- outline:
- ai-project-bootstrapper

```markdown
---
name: ai-project-bootstrapper
description: Implement a real AI project from zero or reconstruct an existing project step-by-step using the specialist skill pack. Use when the user requests ai project bootstrapper or invokes ai-project-bootstrapper. Do NOT use for ordinary one-off coding or human competency lists.
license: CC-BY-4.0
metadata:
  author: AEOS
  version: 1.0.0
  owner_agent: codenavi-agent
---

# ai-project-bootstrapper

Read and follow `00_skills/(creation)/ai-project-bootstrapper/SKILL.md` and its relevant local modules.

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity.
```

### S013 | T1 | ai-sdr

- path: `.agents/skills/ai-sdr/SKILL.md`
- chars: 1035
- outline:
- ai-sdr

```markdown
---
name: ai-sdr
description: When the user wants to deploy AI sales development reps, automate sales qualification, build signal-to-action routing, or design AI agent architecture for sales. Also use when the user mentions 'AI SDR,' 'AI sales agent,' 'automated qualification,' 'signal routing,' 'sales automation,' '11x,' 'Artisan,' 'AiSDR,' 'AI BDR,' or 'autonomous sales.' This skill covers AI SDR deployment, qualification automation, and agent architecture for sales development. Do NOT use for technical implementation, code review, or software architecture.
license: CC-BY-4.0
metadata:
  author: Chad Boyda / agent-gtm-skills
  version: 1.0.0
  original_author: Chad Boyda / agent-gtm-skills
  modified_by: Felipe Rodrigues - github.com/felipfr
  source: https://github.com/chadboyda/agent-gtm-skills
  owner_agent: codenavi-agent
---

# ai-sdr

Read and follow `00_skills/(gtm)/ai-sdr/SKILL.md` and its relevant local modules.

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity.
```

### S014 | T1 | ai-seo

- path: `.agents/skills/ai-seo/SKILL.md`
- chars: 626
- outline:
- ai-seo

```markdown
---
name: ai-seo
description: 'Assimilated TLC AI SEO skill (1.0.0). Programmatic SEO, competitor-alternative pages, AI Overviews/GEO, keyword strategy and content ops. Triggers: SEO, programmatic SEO, AI Overviews, DataForSEO, keyword strategy, organic traffic. Do not use for application code review or software architecture.'
license: CC-BY-4.0
metadata:
  author: Tech Leads Club
  version: 1.0.0
  owner_agent: codenavi-agent
---

# ai-seo

Read and follow `00_skills/(gtm)/ai-seo/SKILL.md` and its relevant local modules.

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity.
```

### S015 | T1 | ai-ugc-ads

- path: `.agents/skills/ai-ugc-ads/SKILL.md`
- chars: 996
- outline:
- ai-ugc-ads

```markdown
---
name: ai-ugc-ads
description: When the user wants to create UGC ad campaigns, recruit UGC creators, generate AI UGC content, or scale with user-generated content. Also use when the user mentions 'UGC,' 'user-generated content,' 'creator ads,' 'Spark Ads,' 'whitelisting,' 'AI UGC,' 'Arcads,' 'Creatify,' 'creator brief,' or 'UGC testing.' This skill covers the UGC growth framework from creator recruitment through AI-powered scaling. Do NOT use for technical implementation, code review, or software architecture.
license: CC-BY-4.0
metadata:
  author: Chad Boyda / agent-gtm-skills
  version: 1.0.0
  original_author: Chad Boyda / agent-gtm-skills
  modified_by: Felipe Rodrigues - github.com/felipfr
  source: https://github.com/chadboyda/agent-gtm-skills
  owner_agent: codenavi-agent
---

# ai-ugc-ads

Read and follow `00_skills/(gtm)/ai-ugc-ads/SKILL.md` and its relevant local modules.

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity.
```

### S016 | T1 | angular-20-expert

- path: `.agents/skills/angular-20-expert/SKILL.md`
- chars: 630
- outline:
- angular-20-expert

```markdown
---
name: angular-20-expert
description: Implement, diagnose and modernize Angular 20 applications without silently introducing behavior from a different Angular major. Use when the user requests angular 20 expert or invokes angular-20-expert. Do NOT use for unrelated languages, domains or production deployment.
license: CC-BY-4.0
metadata:
  author: AEOS
  version: 1.0.0
  owner_agent: codenavi-agent
---

# angular-20-expert

Read and follow `00_skills/(development)/angular-20-expert/SKILL.md` and its relevant local modules.

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity.
```

### S017 | T1 | angular-8-to-20-migration

- path: `.agents/skills/angular-8-to-20-migration/SKILL.md`
- chars: 787
- outline:
- angular-8-to-20-migration

```markdown
---
name: angular-8-to-20-migration
description: Plan and execute Angular 8 to 20 migration one major at a time, preserving rendered UI, custom elements, HTTP interceptors and async behavior. Use when the user says migrar Angular 8 para 20, subir o major do Angular or migração Angular. Do NOT use for single-version coding (angular-20-expert), generic rewrite strategy (legacy-migration-planner), or deployment.
license: CC-BY-4.0
metadata:
  author: AEOS; photographic reference supplied by user
  version: 1.0.0
  owner_agent: codenavi-agent
---

# angular-8-to-20-migration

Read and follow `00_skills/(architecture)/angular-8-to-20-migration/SKILL.md` and its relevant local modules.

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity.
```

### S018 | T1 | anti-hallucination-evaluator

- path: `.agents/skills/anti-hallucination-evaluator/SKILL.md`
- chars: 696
- outline:
- anti-hallucination-evaluator

```markdown
---
name: anti-hallucination-evaluator
description: Evaluate factual claims against inspected sources and identify unsupported assertions, contradictions and missing evidence. Use when the user requests anti hallucination evaluator or invokes anti-hallucination-evaluator. Do NOT use as deployment authorization or as evidence for checks that were not executed.
license: CC-BY-4.0
metadata:
  author: AEOS
  version: 1.0.0
  owner_agent: codenavi-agent
---

# anti-hallucination-evaluator

Read and follow `00_skills/(quality)/anti-hallucination-evaluator/SKILL.md` and its relevant local modules.

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity.
```

### S019 | T1 | approval-governance-auditor

- path: `.agents/skills/approval-governance-auditor/SKILL.md`
- chars: 606
- outline:
- approval-governance-auditor

```markdown
---
name: approval-governance-auditor
description: Validate approval scope, expiration and audit trail. Use when the user requests approval governance auditor or invokes approval-governance-auditor. Do NOT use outside authorized defensive scope or to expose secret values.
license: CC-BY-4.0
metadata:
  author: AEOS
  version: 1.0.0
  owner_agent: codenavi-agent
---

# approval-governance-auditor

Read and follow `00_skills/(security)/approval-governance-auditor/SKILL.md` and its relevant local modules.

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity.
```

### S020 | T1 | approval-requester

- path: `.agents/skills/approval-requester/SKILL.md`
- chars: 620
- outline:
- approval-requester

```markdown
---
name: approval-requester
description: Determine what approvals are needed for a proposed change, create approval requests, and track approval status. Use when the user requests approval requester or invokes approval-requester. Do NOT use outside authorized defensive scope or to expose secret values.
license: CC-BY-4.0
metadata:
  author: AEOS
  version: 1.0.0
  owner_agent: codenavi-agent
---

# approval-requester

Read and follow `00_skills/(security)/approval-requester/SKILL.md` and its relevant local modules.

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity.
```

### S021 | T1 | architecturally-significant-requirement

- path: `.agents/skills/architecturally-significant-requirement/SKILL.md`
- chars: 1197
- outline:
- architecturally-significant-requirement

```markdown
---
name: architecturally-significant-requirement
description: Decides whether a requirement, change request or design issue is an Architecturally Significant Requirement (ASR), a requirement with a measurable effect on the architecture and quality of a system, using the seven-criteria ASR Test, then makes it specific and measurable as a quality attribute scenario and hands the decisions it drives to an ADR. Use when the user asks "is this architecturally significant", "ASR", "requisito arquiteturalmente significativo", "does this need an ADR", "architectural drivers", "quality attribute scenario" or "priorize os requisitos que impactam a arquitetura". Do NOT use for writing the ADR itself (use architecture-decision-record), for full feature specification (use spec-driven), or for threat modeling (use security-threat-model).
license: CC-BY-4.0
metadata:
  author: AEOS
  version: 1.0.0
  owner_agent: codenavi-agent
---

# architecturally-significant-requirement

Read and follow `00_skills/(development)/architecturally-significant-requirement/SKILL.md` and its relevant local modules.

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity.
```

### S022 | T1 | architecture-decision-log

- path: `.agents/skills/architecture-decision-log/SKILL.md`
- chars: 1186
- outline:
- architecture-decision-log

```markdown
---
name: architecture-decision-log
description: 'Maintains the Architecture Decision Log (ADL), the collection of all ADRs of a project: finds the log and its naming convention, assigns the next number, regenerates the index, records status transitions and checks integrity such as duplicate numbers, gaps, broken or circular supersession links and stale proposals. Use when the user says "decision log", "ADR index", "list our ADRs", "which ADRs are superseded", "next ADR number", "log de decisões", "índice de ADRs", "próximo número de ADR" or "quais decisões estão vigentes". Do NOT use for writing the content of a single ADR (use architecture-decision-record), for judging architectural significance (use architecturally-significant-requirement), or for designing an organization-wide knowledge practice (use architecture-knowledge-management).'
license: CC-BY-4.0
metadata:
  author: AEOS
  version: 1.0.0
  owner_agent: codenavi-agent
---

# architecture-decision-log

Read and follow `00_skills/(architecture)/architecture-decision-log/SKILL.md` and its relevant local modules.

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity.
```

### S023 | T1 | architecture-decision-record

- path: `.agents/skills/architecture-decision-record/SKILL.md`
- chars: 1268
- outline:
- architecture-decision-record

```markdown
---
name: architecture-decision-record
description: Writes, supersedes and reviews one Architecture Decision Record (ADR), the record of a single architectural decision with its context, options, outcome and consequences, in MADR 4.0.0, Nygard or Y-statement format, then lints it. Use when the user says "write an ADR", "document this decision", "record why we chose X", "supersede ADR-0007", "review this ADR", "escreva um ADR", "registre a decisão arquitetural" or "crie um registro de decisão de arquitetura". Do NOT use for indexing or auditing the whole decision log (use architecture-decision-log), for judging whether a requirement is architecturally significant (use architecturally-significant-requirement), for an organization-wide decision practice (use architecture-knowledge-management), for making a still-open choice (use the-jury or technical-design-doc-creator), or for general documentation (use docs-writer).
license: CC-BY-4.0
metadata:
  author: AEOS
  version: 1.0.0
  owner_agent: codenavi-agent
---

# architecture-decision-record

Read and follow `00_skills/(architecture)/architecture-decision-record/SKILL.md` and its relevant local modules.

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity.
```

### S024 | T1 | architecture-knowledge-management

- path: `.agents/skills/architecture-knowledge-management/SKILL.md`
- chars: 1280
- outline:
- architecture-knowledge-management

```markdown
---
name: architecture-knowledge-management
description: 'Governs Architecture Knowledge Management (AKM) across ASRs, ADRs and the decision log: decides where architectural knowledge lives, audits it for missing, stale, contradictory or unrecorded decisions, assesses the team on the five-level decision adoption model, recovers past decisions from brownfield evidence, and plans review and reuse. Use when the user says "architecture knowledge management", "AKM", "gestão do conhecimento arquitetural", "audit our architecture decisions", "nobody knows why we chose X", "set up an ADR practice", "decision backlog" or "recuperar decisões de um sistema legado". Do NOT use for writing one ADR (use architecture-decision-record), for maintaining the log index (use architecture-decision-log), for triaging one requirement (use architecturally-significant-requirement), or for general project memory curation (use memory-curator).'
license: CC-BY-4.0
metadata:
  author: AEOS
  version: 1.0.0
  owner_agent: codenavi-agent
---

# architecture-knowledge-management

Read and follow `00_skills/(architecture)/architecture-knowledge-management/SKILL.md` and its relevant local modules.

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity.
```

### S025 | T1 | architecture-mapper

- path: `.agents/skills/architecture-mapper/SKILL.md`
- chars: 582
- outline:
- architecture-mapper

```markdown
---
name: architecture-mapper
description: Map architecture based on detected files and explicit evidence. Use when the user requests architecture mapper or invokes architecture-mapper. Do NOT use for an unrelated implementation change or deployment execution.
license: CC-BY-4.0
metadata:
  author: AEOS
  version: 1.0.0
  owner_agent: codenavi-agent
---

# architecture-mapper

Read and follow `00_skills/(architecture)/architecture-mapper/SKILL.md` and its relevant local modules.

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity.
```

### S026 | T1 | atualizar-dependencias

- path: `.agents/skills/atualizar-dependencias/SKILL.md`
- chars: 617
- outline:
- atualizar-dependencias

```markdown
---
name: atualizar-dependencias
description: Update project dependencies with manifest/lockfile compatibility and regression evidence. Use when the user requests atualizar dependencias or invokes atualizar-dependencias. Do NOT use for unrelated languages, domains or production deployment.
license: CC-BY-4.0
metadata:
  author: AEOS
  version: 1.0.0
  owner_agent: codenavi-agent
---

# atualizar-dependencias

Read and follow `00_skills/(development)/atualizar-dependencias/SKILL.md` and its relevant local modules.

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity.
```

### S027 | T1 | automation-orchestrator

- path: `.agents/skills/automation-orchestrator/SKILL.md`
- chars: 620
- outline:
- automation-orchestrator

```markdown
---
name: automation-orchestrator
description: Design deterministic, idempotent multi-step engineering automations using existing AEOS skills/tools. Use when the user requests automation orchestrator or invokes automation-orchestrator. Do NOT use for unrelated tools or unapproved remote writes.
license: CC-BY-4.0
metadata:
  author: AEOS
  version: 1.0.0
  owner_agent: codenavi-agent
---

# automation-orchestrator

Read and follow `00_skills/(tooling)/automation-orchestrator/SKILL.md` and its relevant local modules.

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity.
```

### S028 | T1 | aws-advisor

- path: `.agents/skills/aws-advisor/SKILL.md`
- chars: 885
- outline:
- aws-advisor

```markdown
---
name: aws-advisor
description: Expert AWS Cloud Advisor for architecture design, security review, and implementation guidance. Leverages AWS MCP tools for accurate, documentation-backed answers. Use when user asks about AWS architecture, security, service selection, migrations, troubleshooting, or learning AWS. Triggers on AWS, Lambda, S3, EC2, ECS, EKS, DynamoDB, RDS, CloudFormation, CDK, Terraform, Serverless, SAM, IAM, VPC, API Gateway, or any AWS service. Do NOT use for non-AWS cloud providers or general infrastructure without AWS context.
license: CC-BY-4.0
metadata:
  author: Felipe Rodrigues - github.com/felipfr
  version: 1.0.0
  owner_agent: codenavi-agent
---

# aws-advisor

Read and follow `00_skills/(cloud)/aws-advisor/SKILL.md` and its relevant local modules.

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity.
```

### S029 | T1 | best-practices

- path: `.agents/skills/best-practices/SKILL.md`
- chars: 677
- outline:
- best-practices

```markdown
---
name: best-practices
description: 'Assimilated TLC/web-quality best-practices skill. Apply modern web security, compatibility, and code-quality checks. Triggers: apply best practices, security audit, modernize code, code quality review, check for vulnerabilities. Do not use as the primary skill for accessibility, SEO (ai-seo), or a full multi-area audit.'
license: MIT
metadata:
  author: Tech Leads Club
  version: 1.0.0
  owner_agent: codenavi-agent
---

# best-practices

Read and follow `00_skills/(quality)/web-best-practices/SKILL.md` and its relevant local modules.

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity.
```

### S030 | T1 | blueprint-generator

- path: `.agents/skills/blueprint-generator/SKILL.md`
- chars: 649
- outline:
- blueprint-generator

```markdown
---
name: blueprint-generator
description: Generate an evidence-based project blueprint covering boundaries, components, data, deployment constraints and verification gates. Use when the user requests blueprint generator or invokes blueprint-generator. Do NOT use for an unrelated implementation change or deployment execution.
license: CC-BY-4.0
metadata:
  author: AEOS
  version: 1.0.0
  owner_agent: codenavi-agent
---

# blueprint-generator

Read and follow `00_skills/(architecture)/blueprint-generator/SKILL.md` and its relevant local modules.

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity.
```

### S031 | T1 | bm25-expert

- path: `.agents/skills/bm25-expert/SKILL.md`
- chars: 543
- outline:
- bm25-expert

```markdown
---
name: bm25-expert
description: Design, tune and evaluate lexical retrieval and hybrid BM25 pipelines. Use when the user requests bm25 expert or invokes bm25-expert. Do NOT use for unrelated languages, domains or production deployment.
license: CC-BY-4.0
metadata:
  author: AEOS
  version: 1.0.0
  owner_agent: codenavi-agent
---

# bm25-expert

Read and follow `00_skills/(development)/bm25-expert/SKILL.md` and its relevant local modules.

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity.
```

### S032 | T1 | camel-banking-expert

- path: `.agents/skills/camel-banking-expert/SKILL.md`
- chars: 660
- outline:
- camel-banking-expert

```markdown
---
name: camel-banking-expert
description: Analyze and implement Apache Camel integration flows in banking-grade systems with strong reliability, security, traceability and idempotency. Use when the user requests camel banking expert or invokes camel-banking-expert. Do NOT use for unrelated languages, domains or production deployment.
license: CC-BY-4.0
metadata:
  author: AEOS
  version: 1.0.0
  owner_agent: codenavi-agent
---

# camel-banking-expert

Read and follow `00_skills/(development)/camel-banking-expert/SKILL.md` and its relevant local modules.

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity.
```

### S033 | T1 | change-trace-auditor

- path: `.agents/skills/change-trace-auditor/SKILL.md`
- chars: 654
- outline:
- change-trace-auditor

```markdown
---
name: change-trace-auditor
description: Audit change manifests and rollback plans so generated or modified files can be reviewed, reproduced and reverted safely. Use when the user requests change trace auditor or invokes change-trace-auditor. Do NOT use as deployment authorization or as evidence for checks that were not executed.
license: CC-BY-4.0
metadata:
  author: AEOS
  version: 1.0.0
  owner_agent: codenavi-agent
---

# change-trace-auditor

Read and follow `00_skills/(quality)/change-trace-auditor/SKILL.md` and its relevant local modules.

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity.
```

### S034 | T1 | chromatic-mega-brain

- path: `.agents/skills/chromatic-mega-brain/SKILL.md`
- chars: 777
- outline:
- chromatic-mega-brain

```markdown
---
name: chromatic-mega-brain
description: Maintain workspace/category/project memory inheritance with canonical continuity files, evidence-backed promotion and exact next actions. Use when the user says organizar memória, cérebro hierárquico, retomar projeto or atualizar handoff. Do NOT use for repository fleet collection (fleet-mapping), deciding which claims deserve promotion (memory-curator/learning-curator), or unconstrained multi-agent reasoning.
license: CC-BY-4.0
metadata:
  author: AEOS
  version: 2.0.0
  owner_agent: codenavi-agent
---

# chromatic-mega-brain

Read and follow `00_skills/(learning)/chromatic-mega-brain/SKILL.md` and its relevant local modules.

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity.
```

### S035 | T1 | chrome-devtools

- path: `.agents/skills/chrome-devtools/SKILL.md`
- chars: 677
- outline:
- chrome-devtools

```markdown
---
name: chrome-devtools
description: Browser debugging, performance profiling, and automation via Chrome DevTools MCP. Use when user says "debug this page", "take a screenshot", "check network requests", "profile performance", "inspect console errors", or "analyze page load". Do NOT use for full E2E test suites (use playwright-skill) or non-browser debugging.
license: MIT
metadata:
  author: Tech Leads Club
  version: 1.0.0
  owner_agent: codenavi-agent
---

# chrome-devtools

Read and follow `00_skills/(tooling)/chrome-devtools/SKILL.md` and its relevant local modules.

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity.
```

### S036 | T1 | ci-quality-gate-engineer

- path: `.agents/skills/ci-quality-gate-engineer/SKILL.md`
- chars: 594
- outline:
- ci-quality-gate-engineer

```markdown
---
name: ci-quality-gate-engineer
description: Create CI/CD quality gates for AEOS and target projects. Use when the user requests ci quality gate engineer or invokes ci-quality-gate-engineer. Do NOT use for unrelated languages, domains or production deployment.
license: CC-BY-4.0
metadata:
  author: AEOS
  version: 1.0.0
  owner_agent: codenavi-agent
---

# ci-quality-gate-engineer

Read and follow `00_skills/(development)/ci-quality-gate-engineer/SKILL.md` and its relevant local modules.

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity.
```

### S037 | T1 | cloudflare-deploy

- path: `.agents/skills/cloudflare-deploy/SKILL.md`
- chars: 647
- outline:
- cloudflare-deploy

```markdown
---
name: cloudflare-deploy
description: Deploy applications and infrastructure to Cloudflare using Workers, Pages, and related platform services. Use when the user asks to deploy, host, publish, or set up a project on Cloudflare. Do NOT use for deploying to Vercel, Netlify, or Render (use their respective skills).
license: CC-BY-4.0
metadata:
  author: github.com/openai/skills
  version: 1.0.0
  owner_agent: codenavi-agent
---

# cloudflare-deploy

Read and follow `00_skills/(cloud)/cloudflare-deploy/SKILL.md` and its relevant local modules.

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity.
```

### S038 | T1 | code-analyzer

- path: `.agents/skills/code-analyzer/SKILL.md`
- chars: 552
- outline:
- code-analyzer

```markdown
---
name: code-analyzer
description: Analyze code structure, impact, and risks for proposed changes. Use when the user requests code analyzer or invokes code-analyzer. Do NOT use to mutate production or invent architecture without source evidence.
license: CC-BY-4.0
metadata:
  author: AEOS
  version: 1.0.0
  owner_agent: codenavi-agent
---

# code-analyzer

Read and follow `00_skills/(mapping)/code-analyzer/SKILL.md` and its relevant local modules.

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity.
```

### S039 | T1 | codenavi

- path: `.agents/skills/codenavi/SKILL.md`
- chars: 1000
- outline:
- codenavi

```markdown
---
name: codenavi
description: Your pathfinder for navigating unknown codebases. Investigates with precision, implements surgically, and never assumes — if it doesn't know, it says so. Maintains a .notebook/ knowledge base that grows across sessions, turning every discovery into lasting intelligence. Summons available skills, MCPs, and docs when the mission demands. Use when fixing bugs, implementing features, refactoring, investigating flows, or any development task in unfamiliar territory. Triggers on "fix this", "implement this", "how does this work", "investigate this flow", "help me with this code". Do NOT use for greenfield scaffolding, CI/CD, or infrastructure provisioning.
license: CC-BY-4.0
metadata:
  author: Tech Leads Club
  version: 1.0.0
  owner_agent: codenavi-agent
---

# codenavi

Read and follow `00_skills/(development)/codenavi/SKILL.md` and its relevant local modules.

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity.
```

### S040 | T1 | coding-guidelines

- path: `.agents/skills/coding-guidelines/SKILL.md`
- chars: 615
- outline:
- coding-guidelines

```markdown
---
name: coding-guidelines
description: Inspect and apply the target repository coding conventions with source evidence before changing code. Use when the user requests coding guidelines or invokes coding-guidelines. Do NOT use for unrelated languages, domains or production deployment.
license: CC-BY-4.0
metadata:
  author: Tech Leads Club
  version: 1.0.0
  owner_agent: codenavi-agent
---

# coding-guidelines

Read and follow `00_skills/(development)/coding-guidelines/SKILL.md` and its relevant local modules.

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity.
```

### S041 | T1 | compatibility-analyzer

- path: `.agents/skills/compatibility-analyzer/SKILL.md`
- chars: 649
- outline:
- compatibility-analyzer

```markdown
---
name: compatibility-analyzer
description: Analyze dependency compatibility — version conflicts, peer dependency issues, platform constraints, breaking change risk. Use when the user requests compatibility analyzer or invokes compatibility-analyzer. Do NOT use for unrelated languages, domains or production deployment.
license: CC-BY-4.0
metadata:
  author: AEOS
  version: 1.0.0
  owner_agent: codenavi-agent
---

# compatibility-analyzer

Read and follow `00_skills/(development)/compatibility-analyzer/SKILL.md` and its relevant local modules.

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity.
```

### S042 | T1 | compliance-audit-exporter

- path: `.agents/skills/compliance-audit-exporter/SKILL.md`
- chars: 660
- outline:
- compliance-audit-exporter

```markdown
---
name: compliance-audit-exporter
description: Export a redacted audit package that maps requested controls to verified evidence and unresolved gaps. Use when the user requests compliance audit exporter or invokes compliance-audit-exporter. Do NOT use as deployment authorization or as evidence for checks that were not executed.
license: CC-BY-4.0
metadata:
  author: AEOS
  version: 1.0.0
  owner_agent: codenavi-agent
---

# compliance-audit-exporter

Read and follow `00_skills/(quality)/compliance-audit-exporter/SKILL.md` and its relevant local modules.

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity.
```

### S043 | T1 | compliance-evidence-exporter

- path: `.agents/skills/compliance-evidence-exporter/SKILL.md`
- chars: 624
- outline:
- compliance-evidence-exporter

```markdown
---
name: compliance-evidence-exporter
description: Export compliance evidence without leaking secrets. Use when the user requests compliance evidence exporter or invokes compliance-evidence-exporter. Do NOT use as deployment authorization or as evidence for checks that were not executed.
license: CC-BY-4.0
metadata:
  author: AEOS
  version: 1.0.0
  owner_agent: codenavi-agent
---

# compliance-evidence-exporter

Read and follow `00_skills/(quality)/compliance-evidence-exporter/SKILL.md` and its relevant local modules.

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity.
```

### S044 | T1 | component-common-domain-detection

- path: `.agents/skills/component-common-domain-detection/SKILL.md`
- chars: 818
- outline:
- component-common-domain-detection

```markdown
---
name: component-common-domain-detection
description: Finds duplicate business logic spread across multiple components and suggests consolidation. Use when asking "where is this logic duplicated?", "find common code between services", "what can be consolidated?", "detect shared domain logic", or analyzing component overlap before refactoring. Do NOT use for code-level duplication detection (use linters) or dependency analysis (use coupling-analysis).
license: CC-BY-4.0
metadata:
  author: Tech Leads Club
  version: 1.0.0
  owner_agent: codenavi-agent
---

# component-common-domain-detection

Read and follow `00_skills/(architecture)/component-common-domain-detection/SKILL.md` and its relevant local modules.

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity.
```

### S045 | T1 | component-flattening-analysis

- path: `.agents/skills/component-flattening-analysis/SKILL.md`
- chars: 840
- outline:
- component-flattening-analysis

```markdown
---
name: component-flattening-analysis
description: Detects misplaced classes and fixes component hierarchy problems — finds code that should belong inside a component but sits at the root level. Use when asking "clean up component structure", "find orphaned classes", "fix module hierarchy", "flatten nested components", or analyzing why namespaces have misplaced code. Do NOT use for dependency analysis (use coupling-analysis) or domain grouping (use domain-identification-grouping).
license: CC-BY-4.0
metadata:
  author: Tech Leads Club
  version: 1.0.0
  owner_agent: codenavi-agent
---

# component-flattening-analysis

Read and follow `00_skills/(architecture)/component-flattening-analysis/SKILL.md` and its relevant local modules.

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity.
```

### S046 | T1 | component-identification-sizing

- path: `.agents/skills/component-identification-sizing/SKILL.md`
- chars: 796
- outline:
- component-identification-sizing

```markdown
---
name: component-identification-sizing
description: Maps architectural components in a codebase and measures their size to identify what should be extracted first. Use when asking "how big is each module?", "what components do I have?", "which service is too large?", "analyze codebase structure", "size my monolith", or planning where to start decomposing. Do NOT use for runtime performance sizing or infrastructure capacity planning.
license: CC-BY-4.0
metadata:
  author: Tech Leads Club
  version: 1.0.0
  owner_agent: codenavi-agent
---

# component-identification-sizing

Read and follow `00_skills/(architecture)/component-identification-sizing/SKILL.md` and its relevant local modules.

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity.
```

### S047 | T1 | conflict-detector

- path: `.agents/skills/conflict-detector/SKILL.md`
- chars: 566
- outline:
- conflict-detector

```markdown
---
name: conflict-detector
description: Detect read/write/tool/approval/resource conflicts before parallel execution. Use when the user requests conflict detector or invokes conflict-detector. Do NOT use for unrelated tools or unapproved remote writes.
license: CC-BY-4.0
metadata:
  author: AEOS
  version: 1.0.0
  owner_agent: codenavi-agent
---

# conflict-detector

Read and follow `00_skills/(tooling)/conflict-detector/SKILL.md` and its relevant local modules.

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity.
```

### S048 | T1 | confluence-assistant

- path: `.agents/skills/confluence-assistant/SKILL.md`
- chars: 672
- outline:
- confluence-assistant

```markdown
---
name: confluence-assistant
description: Expert in Confluence operations using Atlassian MCP. Use when the user says "search Confluence", "create a Confluence page", "update a page", "find documentation in Confluence", "list spaces", or "add a comment to a page". Do NOT use for Jira issues, general web search, or local file creation.
license: CC-BY-4.0
metadata:
  author: Tech Leads Club
  version: 1.0.0
  owner_agent: codenavi-agent
---

# confluence-assistant

Read and follow `00_skills/(development)/confluence-assistant/SKILL.md` and its relevant local modules.

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity.
```

### S049 | T1 | content-to-pipeline

- path: `.agents/skills/content-to-pipeline/SKILL.md`
- chars: 1090
- outline:
- content-to-pipeline

```markdown
---
name: content-to-pipeline
description: When the user wants to turn content into revenue, build a content-led GTM motion, reverse engineer distribution, or repurpose content across platforms. Also use when the user mentions 'content marketing,' 'content-led growth,' 'content to pipeline,' 'distribution,' 'content repurposing,' 'content strategy,' 'thought leadership,' 'newsletter,' 'content flywheel,' 'organic growth.' This skill covers content-to-revenue systems from creation through pipeline attribution. Do NOT use for technical implementation, code review, or software architecture.
license: CC-BY-4.0
metadata:
  author: Chad Boyda / agent-gtm-skills
  version: 1.0.0
  original_author: Chad Boyda / agent-gtm-skills
  modified_by: Felipe Rodrigues - github.com/felipfr
  source: https://github.com/chadboyda/agent-gtm-skills
  owner_agent: codenavi-agent
---

# content-to-pipeline

Read and follow `00_skills/(gtm)/content-to-pipeline/SKILL.md` and its relevant local modules.

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity.
```

### S050 | T1 | context-router

- path: `.agents/skills/context-router/SKILL.md`
- chars: 581
- outline:
- context-router

```markdown
---
name: context-router
description: Resolve minimal context packets for agents based on task, LCPs and memory rules. Use when the user requests context router or invokes context-router. Do NOT use to promote unverified claims or transient task status into durable memory.
license: CC-BY-4.0
metadata:
  author: AEOS
  version: 1.0.0
  owner_agent: codenavi-agent
---

# context-router

Read and follow `00_skills/(learning)/context-router/SKILL.md` and its relevant local modules.

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity.
```

### S051 | T1 | continuity-bootstrapper

- path: `.agents/skills/continuity-bootstrapper/SKILL.md`
- chars: 649
- outline:
- continuity-bootstrapper

```markdown
---
name: continuity-bootstrapper
description: Bootstrap and validate the CodENavi continuity quartet for a workspace without inventing project state. Use when the user requests continuity bootstrapper or invokes continuity-bootstrapper. Do NOT use to promote unverified claims or transient task status into durable memory.
license: CC-BY-4.0
metadata:
  author: AEOS
  version: 1.0.0
  owner_agent: codenavi-agent
---

# continuity-bootstrapper

Read and follow `00_skills/(learning)/continuity-bootstrapper/SKILL.md` and its relevant local modules.

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity.
```

### S052 | T1 | core-web-vitals

- path: `.agents/skills/core-web-vitals/SKILL.md`
- chars: 713
- outline:
- core-web-vitals

```markdown
---
name: core-web-vitals
description: 'Assimilated TLC/web-quality Core Web Vitals skill. Fix LCP, INP and CLS against current Google thresholds. Triggers: improve Core Web Vitals, fix LCP, reduce CLS, optimize INP, page experience, layout shifts. Do not use for generic bundle/caching work (perf-web-optimization), only running Lighthouse (perf-lighthouse), or Astro-only config (perf-astro).'
license: MIT
metadata:
  author: Tech Leads Club
  version: 1.0.0
  owner_agent: codenavi-agent
---

# core-web-vitals

Read and follow `00_skills/(performance)/core-web-vitals/SKILL.md` and its relevant local modules.

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity.
```

### S053 | T1 | cost-token-optimizer

- path: `.agents/skills/cost-token-optimizer/SKILL.md`
- chars: 599
- outline:
- cost-token-optimizer

```markdown
---
name: cost-token-optimizer
description: Optimize LLM/tool costs using context minimization and cache policy. Use when the user requests cost token optimizer or invokes cost-token-optimizer. Do NOT use to promote unverified claims or transient task status into durable memory.
license: CC-BY-4.0
metadata:
  author: AEOS
  version: 1.0.0
  owner_agent: codenavi-agent
---

# cost-token-optimizer

Read and follow `00_skills/(learning)/cost-token-optimizer/SKILL.md` and its relevant local modules.

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity.
```

### S054 | T1 | coupling-analysis

- path: `.agents/skills/coupling-analysis/SKILL.md`
- chars: 833
- outline:
- coupling-analysis

```markdown
---
name: coupling-analysis
description: Analyzes coupling between modules using the three-dimensional model (strength, distance, volatility) from "Balancing Coupling in Software Design". Use when asking "are these modules too coupled?", "show me dependencies", "analyze integration quality", "which modules should I decouple?", "coupling report", or evaluating architectural health. Do NOT use for domain boundary analysis (use domain-analysis) or component sizing (use component-identification-sizing).
license: CC-BY-4.0
metadata:
  author: Tech Leads Club
  version: 1.0.0
  owner_agent: codenavi-agent
---

# coupling-analysis

Read and follow `00_skills/(architecture)/coupling-analysis/SKILL.md` and its relevant local modules.

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity.
```

### S055 | T1 | create-adr

- path: `.agents/skills/create-adr/SKILL.md`
- chars: 923
- outline:
- create-adr

```markdown
---
name: create-adr
description: Creates Architecture Decision Records (ADRs) to document significant architectural choices and their rationale for future team members. Use when the user says "write an ADR", "document this decision", "record why we chose X", "add an architecture decision record", "create an ADR for", or wants to capture the reasoning behind a technical choice so the team understands it later. Do NOT use when the decision hasn't been made yet (use create-rfc instead), for implementation planning (use technical-design-doc-creator), or for general documentation.
license: CC-BY-4.0
metadata:
  author: Tech Leads Club - github.com/tech-leads-club
  version: 1.0.0
  owner_agent: codenavi-agent
---

# create-adr

Read and follow `00_skills/(creation)/create-adr/SKILL.md` and its relevant local modules.

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity.
```

### S056 | T1 | create-rfc

- path: `.agents/skills/create-rfc/SKILL.md`
- chars: 817
- outline:
- create-rfc

```markdown
---
name: create-rfc
description: Creates structured Request for Comments (RFC) documents for proposing and deciding on significant changes. Use when the user says "write an RFC", "create a proposal", "I need to propose a change", "draft an RFC", "document a decision", or needs stakeholder alignment before making a major technical or process decision. Do NOT use for TDDs/implementation docs (use technical-design-doc-creator instead), README files, or general documentation.
license: CC-BY-4.0
metadata:
  author: Tech Leads Club - github.com/tech-leads-club
  version: 1.0.0
  owner_agent: codenavi-agent
---

# create-rfc

Read and follow `00_skills/(creation)/create-rfc/SKILL.md` and its relevant local modules.

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity.
```

### S057 | T1 | create-technical-design-doc

- path: `.agents/skills/create-technical-design-doc/SKILL.md`
- chars: 680
- outline:
- create-technical-design-doc

```markdown
---
name: create-technical-design-doc
description: 'Assimilated TLC TDD writer. Create architecture-level Technical Design Documents through discovery. Triggers: write a design doc, create a TDD, technical spec, architecture document, RFC, design proposal, criar um TDD. Do not use for README, API docs, or general docs (docs-writer).'
license: CC-BY-4.0
metadata:
  author: Tech Leads Club
  version: 1.0.0
  owner_agent: codenavi-agent
---

# create-technical-design-doc

Read and follow `00_skills/(creation)/create-technical-design-doc/SKILL.md` and its relevant local modules.

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity.
```

### S058 | T1 | critical-thinking-governor

- path: `.agents/skills/critical-thinking-governor/SKILL.md`
- chars: 738
- outline:
- critical-thinking-governor

```markdown
---
name: critical-thinking-governor
description: Governa toda execução de skills do AEOS com uma seleção limitada e auditável de 20 lentes internas de pensamento crítico. As lentes são especializações da skill e nunca identidades de agent. Use when the user requests critical thinking governor or invokes critical-thinking-governor. Do NOT use for unrelated languages, domains or production deployment.
license: CC-BY-4.0
metadata:
  author: AEOS
  version: 1.0.0
  owner_agent: codenavi-agent
---

# critical-thinking-governor

Read and follow `00_skills/(development)/critical-thinking-governor/SKILL.md` and its relevant local modules.

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity.
```

### S059 | T1 | csharp-expert

- path: `.agents/skills/csharp-expert/SKILL.md`
- chars: 635
- outline:
- csharp-expert

```markdown
---
name: csharp-expert
description: Writes and reviews production C# on the current stable .NET release (C# 14, .NET 10). Use when the user says c#-expert, C#, csharp, .NET, csproj, dotnet, or asks to implement, fix, or review .cs code. Do NOT use for F#, Visual Basic, non-.NET languages, or work that is not C#/.NET source.
license: CC-BY-4.0
metadata:
  author: AEOS
  version: 1.0.0
  owner_agent: codenavi-agent
---

# csharp-expert

Read and follow `00_skills/(development)/csharp-expert/SKILL.md` and its relevant local modules.

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity.
```

### S060 | T1 | cursor-subagent-creator

- path: `.agents/skills/cursor-subagent-creator/SKILL.md`
- chars: 696
- outline:
- cursor-subagent-creator

```markdown
---
name: cursor-subagent-creator
description: 'Assimilated TLC Cursor work-unit designer. Use when the user asks for a Cursor specialist, isolated-context workflow, verifier, debugger, or auditor. Triggers: cursor internal lenses, cursor agent, isolated work unit. Do not spawn or register another AEOS agent identity. Do not use for a simple one-off skill.'
license: CC-BY-4.0
metadata:
  author: Tech Leads Club
  version: 1.0.0
  owner_agent: codenavi-agent
---

# cursor-subagent-creator

Read and follow `00_skills/(creation)/cursor-subagent-creator/SKILL.md` and its relevant local modules.

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity.
```

### S061 | T1 | cve-advisory-sync

- path: `.agents/skills/cve-advisory-sync/SKILL.md`
- chars: 725
- outline:
- cve-advisory-sync

```markdown
---
name: cve-advisory-sync
description: Refresh a provenance-tracked local vulnerability advisory dataset from authorized OSV/GHSA/NVD sources. Use when the user says atualizar a base de CVEs or sincronizar advisories. Do NOT use for a version-specific vulnerability assessment (vuln-obsol-recon), known-CVE patching (cve-remediation), or EOL dates (eol-advisory-sync).
license: CC-BY-4.0
metadata:
  author: AEOS; photographic reference supplied by user
  version: 1.0.0
  owner_agent: codenavi-agent
---

# cve-advisory-sync

Read and follow `00_skills/(security)/cve-advisory-sync/SKILL.md` and its relevant local modules.

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity.
```

### S062 | T1 | cve-remediation

- path: `.agents/skills/cve-remediation/SKILL.md`
- chars: 716
- outline:
- cve-remediation

```markdown
---
name: cve-remediation
description: Fix an already identified dependency CVE/GHSA with the smallest compatible change and behavior evidence. Use when the user says corrigir esta CVE, remediar GHSA or atualizar a dependência vulnerável. Do NOT use for discovering all vulnerabilities (vuln-obsol-recon), advisory ingestion, or publishing/merging the resulting PR.
license: CC-BY-4.0
metadata:
  author: AEOS; photographic reference supplied by user
  version: 1.0.0
  owner_agent: codenavi-agent
---

# cve-remediation

Read and follow `00_skills/(security)/cve-remediation/SKILL.md` and its relevant local modules.

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity.
```

### S063 | T1 | dark-videos-knowledge-base

- path: `.agents/skills/dark-videos-knowledge-base/SKILL.md`
- chars: 742
- outline:
- dark-videos-knowledge-base

```markdown
---
name: dark-videos-knowledge-base
description: "Navigate the retained dark-videos repository map and reconcile historical paths with current evidence. Use when the user asks for 'mapa do dark-videos', 'onde fica o publicador', or 'entender o pipeline dark-videos'. Do NOT use to claim a current inventory, run the pipeline, or publish videos without inspecting the actual repository and authorization."
license: CC-BY-4.0
metadata:
  author: "AEOS"
  version: 3.0.1
  owner_agent: codenavi-agent
---

# dark-videos-knowledge-base

Read and follow `00_skills/(development)/dark-videos-knowledge-base/SKILL.md` and its relevant local modules.

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity.
```

### S064 | T1 | dark-videos-pipeline-expert

- path: `.agents/skills/dark-videos-pipeline-expert/SKILL.md`
- chars: 705
- outline:
- dark-videos-pipeline-expert

```markdown
---
name: dark-videos-pipeline-expert
description: 'Operate the dark-videos pipeline: mine the last 24h, rank the top 20 with LAYA, frame from the project template, and publish through the existing dispatch. Use when mining, framing, scheduling, or posting shorts in dark-videos. Do not use for a second publisher, cookie export, or posting below the app''s red team.'
license: CC-BY-4.0
metadata:
  author: AEOS
  version: 2.0.0
  owner_agent: codenavi-agent
---

# dark-videos-pipeline-expert

Read and follow `00_skills/(development)/dark-videos-pipeline-expert/SKILL.md` and its relevant local modules.

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity.
```

### S065 | T1 | database-architecture-planner

- path: `.agents/skills/database-architecture-planner/SKILL.md`
- chars: 693
- outline:
- database-architecture-planner

```markdown
---
name: database-architecture-planner
description: Plan database architecture, schema governance, migrations, backup, restore and production safety for any requested database. Use when the user requests database architecture planner or invokes database-architecture-planner. Do NOT use for an unrelated implementation change or deployment execution.
license: CC-BY-4.0
metadata:
  author: AEOS
  version: 1.0.0
  owner_agent: codenavi-agent
---

# database-architecture-planner

Read and follow `00_skills/(architecture)/database-architecture-planner/SKILL.md` and its relevant local modules.

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity.
```

### S066 | T1 | decomposition-planning-roadmap

- path: `.agents/skills/decomposition-planning-roadmap/SKILL.md`
- chars: 842
- outline:
- decomposition-planning-roadmap

```markdown
---
name: decomposition-planning-roadmap
description: Creates step-by-step decomposition plans and migration roadmaps for breaking apart monolithic applications. Use when asking "what order should I extract services?", "plan my migration", "create a decomposition roadmap", "prioritize what to split", "monolith to microservices strategy", or tracking decomposition progress. Do NOT use for domain analysis (use domain-analysis) or component sizing (use component-identification-sizing).
license: CC-BY-4.0
metadata:
  author: Tech Leads Club
  version: 1.0.0
  owner_agent: codenavi-agent
---

# decomposition-planning-roadmap

Read and follow `00_skills/(architecture)/decomposition-planning-roadmap/SKILL.md` and its relevant local modules.

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity.
```

### S067 | T1 | delegation-auditor

- path: `.agents/skills/delegation-auditor/SKILL.md`
- chars: 559
- outline:
- delegation-auditor

```markdown
---
name: delegation-auditor
description: Validate delegation against policy, scope, capabilities and risk. Use when the user requests delegation auditor or invokes delegation-auditor. Do NOT use for unrelated tools or unapproved remote writes.
license: CC-BY-4.0
metadata:
  author: AEOS
  version: 1.0.0
  owner_agent: codenavi-agent
---

# delegation-auditor

Read and follow `00_skills/(tooling)/delegation-auditor/SKILL.md` and its relevant local modules.

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity.
```

### S068 | T1 | demo

- path: `.agents/skills/demo/SKILL.md`
- chars: 992
- outline:
- demo

```markdown
---
name: demo
description: "Record a demo video of a web app feature or flow on a real desktop (Docker, Xvfb, XFCE, real X cursor), producing an mp4 plus a click/hover/scroll/type telemetry file. Takes a flow description, an existing demo name or path, or init. Use when the user says \"record a demo of the checkout\", \"gravar um demo dessa feature\", \"make a screencast of this flow\", \"video for the changelog\", \"re-record the checkout demo\", \"refresh the demo video\", or \"demo init\". Do NOT use for general browser testing or automation that needs no video (use playwright-skill), page debugging or network inspection (use chrome-devtools), or static screenshots."
license: CC-BY-4.0
metadata:
  author: "github.com/wcalderipe"
  version: 1.0.0
  owner_agent: codenavi-agent
---

# demo

Read and follow `00_skills/(web-automation)/demo/SKILL.md` and its relevant local modules.

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity.
```

### S069 | T1 | dependency-analyzer

- path: `.agents/skills/dependency-analyzer/SKILL.md`
- chars: 580
- outline:
- dependency-analyzer

```markdown
---
name: dependency-analyzer
description: Analyze dependencies, upgrade candidates, compatibility, and risks. Use when the user requests dependency analyzer or invokes dependency-analyzer. Do NOT use for unrelated languages, domains or production deployment.
license: CC-BY-4.0
metadata:
  author: AEOS
  version: 1.0.0
  owner_agent: codenavi-agent
---

# dependency-analyzer

Read and follow `00_skills/(development)/dependency-analyzer/SKILL.md` and its relevant local modules.

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity.
```

### S070 | T1 | dependency-updater

- path: `.agents/skills/dependency-updater/SKILL.md`
- chars: 588
- outline:
- dependency-updater

```markdown
---
name: dependency-updater
description: Update dependencies with minimal blast radius and evidence-backed compatibility. Use when the user requests dependency updater or invokes dependency-updater. Do NOT use for unrelated languages, domains or production deployment.
license: CC-BY-4.0
metadata:
  author: AEOS
  version: 1.0.0
  owner_agent: codenavi-agent
---

# dependency-updater

Read and follow `00_skills/(development)/dependency-updater/SKILL.md` and its relevant local modules.

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity.
```

### S071 | T1 | deploy-expert-unique

- path: `.agents/skills/deploy-expert-unique/SKILL.md`
- chars: 694
- outline:
- deploy-expert-unique

```markdown
---
name: deploy-expert-unique
description: Apply the unique governed AWS deployment pipeline contract for AIHealthResearch, including branch promotion, Google OSV CVE, CodeQL SAST, Python security and deploy validators. Use when the user requests deploy expert unique or invokes deploy-expert-unique. Do NOT use for unrelated languages, domains or production deployment.
license: CC-BY-4.0
metadata:
  author: AEOS
  version: 1.0.0
  owner_agent: codenavi-agent
---

# deploy-expert-unique

Read and follow `00_skills/(development)/deploy-expert-unique/SKILL.md` and its relevant local modules.

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity.
```

### S072 | T1 | deployment-pipeline-expert

- path: `.agents/skills/deployment-pipeline-expert/SKILL.md`
- chars: 612
- outline:
- deployment-pipeline-expert

```markdown
---
name: deployment-pipeline-expert
description: Map, diagnose and improve CI/CD/deployment pipelines safely. Use when the user requests deployment pipeline expert or invokes deployment-pipeline-expert. Do NOT use for unrelated application features or unapproved production changes.
license: CC-BY-4.0
metadata:
  author: AEOS
  version: 1.0.0
  owner_agent: codenavi-agent
---

# deployment-pipeline-expert

Read and follow `00_skills/(cloud)/deployment-pipeline-expert/SKILL.md` and its relevant local modules.

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity.
```

### S073 | T1 | devops-pipeline-engineering

- path: `.agents/skills/devops-pipeline-engineering/SKILL.md`
- chars: 694
- outline:
- devops-pipeline-engineering

```markdown
---
name: devops-pipeline-engineering
description: Governed DevOps, Git and GitHub Actions lifecycle with recursive CI recovery, per-workflow guardians, merge readiness and bundle handoff. Use when the user requests devops pipeline engineering or invokes devops-pipeline-engineering. Do NOT use for unrelated application features or unapproved production changes.
license: CC-BY-4.0
metadata:
  author: AEOS
  version: 1.0.0
  owner_agent: codenavi-agent
---

# devops-pipeline-engineering

Read and follow `00_skills/(cloud)/devops-pipeline-engineering/SKILL.md` and its relevant local modules.

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity.
```

### S074 | T1 | diff-reviewer

- path: `.agents/skills/diff-reviewer/SKILL.md`
- chars: 582
- outline:
- diff-reviewer

```markdown
---
name: diff-reviewer
description: Review generated diffs/patches for correctness, safety, and alignment with evidence. Use when the user requests diff reviewer or invokes diff-reviewer. Do NOT use as deployment authorization or as evidence for checks that were not executed.
license: CC-BY-4.0
metadata:
  author: AEOS
  version: 1.0.0
  owner_agent: codenavi-agent
---

# diff-reviewer

Read and follow `00_skills/(quality)/diff-reviewer/SKILL.md` and its relevant local modules.

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity.
```

### S075 | T1 | docker-devcontainer-engineer

- path: `.agents/skills/docker-devcontainer-engineer/SKILL.md`
- chars: 612
- outline:
- docker-devcontainer-engineer

```markdown
---
name: docker-devcontainer-engineer
description: Generate devcontainer/Docker artifacts in sandbox. Use when the user requests docker devcontainer engineer or invokes docker-devcontainer-engineer. Do NOT use for unrelated application features or unapproved production changes.
license: CC-BY-4.0
metadata:
  author: AEOS
  version: 1.0.0
  owner_agent: codenavi-agent
---

# docker-devcontainer-engineer

Read and follow `00_skills/(cloud)/docker-devcontainer-engineer/SKILL.md` and its relevant local modules.

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity.
```

### S076 | T1 | docs-writer

- path: `.agents/skills/docs-writer/SKILL.md`
- chars: 742
- outline:
- docs-writer

```markdown
---
name: docs-writer
description: Write, review, and edit documentation files with consistent structure, tone, and technical accuracy. Use when creating docs, reviewing markdown files, writing READMEs, updating `/docs` directories, or when user says "write documentation", "review this doc", "improve this README", "create a guide", or "edit markdown". Do NOT use for code comments, inline JSDoc, or API reference generation.
license: CC-BY-4.0
metadata:
  author: Tech Leads Club
  version: 1.0.0
  owner_agent: codenavi-agent
---

# docs-writer

Read and follow `00_skills/(development)/docs-writer/SKILL.md` and its relevant local modules.

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity.
```

### S077 | T1 | documentation

- path: `.agents/skills/documentation/SKILL.md`
- chars: 532
- outline:
- documentation

```markdown
---
name: documentation
description: Generate evidence-based documentation in sandbox. Use when the user requests documentation or invokes documentation. Do NOT use for unrelated languages, domains or production deployment.
license: CC-BY-4.0
metadata:
  author: AEOS
  version: 1.0.0
  owner_agent: codenavi-agent
---

# documentation

Read and follow `00_skills/(development)/documentation/SKILL.md` and its relevant local modules.

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity.
```

### S078 | T1 | documentation-11-layer-mapper

- path: `.agents/skills/documentation-11-layer-mapper/SKILL.md`
- chars: 784
- outline:
- documentation-11-layer-mapper

```markdown
---
name: documentation-11-layer-mapper
description: Generate an 11-layer documentation package that explains what the project does, how it works, why decisions were made, how every endpoint and feature integrates end to end, and what is required to operate it safely. Use when the user requests documentation 11 layer mapper or invokes documentation-11-layer-mapper. Do NOT use to mutate production or invent architecture without source evidence.
license: CC-BY-4.0
metadata:
  author: AEOS
  version: 1.0.0
  owner_agent: codenavi-agent
---

# documentation-11-layer-mapper

Read and follow `00_skills/(mapping)/documentation-11-layer-mapper/SKILL.md` and its relevant local modules.

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity.
```

### S079 | T1 | documentation-mapper

- path: `.agents/skills/documentation-mapper/SKILL.md`
- chars: 618
- outline:
- documentation-mapper

```markdown
---
name: documentation-mapper
description: Transform a target project repository into complete, verified, enterprise-grade documentation. Use when the user requests documentation mapper or invokes documentation-mapper. Do NOT use to mutate production or invent architecture without source evidence.
license: CC-BY-4.0
metadata:
  author: AEOS
  version: 1.0.0
  owner_agent: codenavi-agent
---

# documentation-mapper

Read and follow `00_skills/(mapping)/documentation-mapper/SKILL.md` and its relevant local modules.

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity.
```

### S080 | T1 | domain-analysis

- path: `.agents/skills/domain-analysis/SKILL.md`
- chars: 802
- outline:
- domain-analysis

```markdown
---
name: domain-analysis
description: Maps business domains and suggests service boundaries in any codebase using DDD Strategic Design. Use when asking "what are the domains in this codebase?", "where should I draw service boundaries?", "identify bounded contexts", "classify subdomains", "DDD analysis", or analyzing domain cohesion. Do NOT use for grouping existing components into domains (use domain-identification-grouping) or dependency analysis (use coupling-analysis).
license: CC-BY-4.0
metadata:
  author: Tech Leads Club
  version: 1.0.0
  owner_agent: codenavi-agent
---

# domain-analysis

Read and follow `00_skills/(architecture)/domain-analysis/SKILL.md` and its relevant local modules.

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity.
```

### S081 | T1 | domain-identification-grouping

- path: `.agents/skills/domain-identification-grouping/SKILL.md`
- chars: 815
- outline:
- domain-identification-grouping

```markdown
---
name: domain-identification-grouping
description: Groups existing components into logical business domains to plan service-based architecture. Use when asking "which components belong together?", "group these into services", "organize by domain", "component-to-domain mapping", or planning service extraction from an existing codebase. Do NOT use for identifying new domains from scratch (use domain-analysis) or analyzing coupling (use coupling-analysis).
license: CC-BY-4.0
metadata:
  author: Tech Leads Club
  version: 1.0.0
  owner_agent: codenavi-agent
---

# domain-identification-grouping

Read and follow `00_skills/(architecture)/domain-identification-grouping/SKILL.md` and its relevant local modules.

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity.
```

### S082 | T1 | dynatrace-observability-staff

- path: `.agents/skills/dynatrace-observability-staff/SKILL.md`
- chars: 745
- outline:
- dynatrace-observability-staff

```markdown
---
name: dynatrace-observability-staff
description: Deep Staff-level Dynatrace observability analysis for metrics, logs, traces, Davis problems, topology, Kubernetes context, SLOs and cost-safe root-cause evidence. Use when the user requests dynatrace observability staff or invokes dynatrace-observability-staff. Do NOT use to restart, scale or mutate live systems without an authorized operations task.
license: CC-BY-4.0
metadata:
  author: AEOS
  version: 1.0.0
  owner_agent: codenavi-agent
---

# dynatrace-observability-staff

Read and follow `00_skills/(monitoring)/dynatrace-observability-staff/SKILL.md` and its relevant local modules.

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity.
```

### S083 | T1 | enterprise-repo-intelligence

- path: `.agents/skills/enterprise-repo-intelligence/SKILL.md`
- chars: 636
- outline:
- enterprise-repo-intelligence

```markdown
---
name: enterprise-repo-intelligence
description: Map large enterprise repositories with performance budgets and evidence. Use when the user requests enterprise repo intelligence or invokes enterprise-repo-intelligence. Do NOT use to mutate production or invent architecture without source evidence.
license: CC-BY-4.0
metadata:
  author: AEOS
  version: 1.0.0
  owner_agent: codenavi-agent
---

# enterprise-repo-intelligence

Read and follow `00_skills/(mapping)/enterprise-repo-intelligence/SKILL.md` and its relevant local modules.

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity.
```

### S084 | T1 | enterprise-security-auditor

- path: `.agents/skills/enterprise-security-auditor/SKILL.md`
- chars: 663
- outline:
- enterprise-security-auditor

```markdown
---
name: enterprise-security-auditor
description: Audit repository and integration security using observed trust boundaries, configuration and source evidence. Use when the user requests enterprise security auditor or invokes enterprise-security-auditor. Do NOT use outside authorized defensive scope or to expose secret values.
license: CC-BY-4.0
metadata:
  author: AEOS
  version: 1.0.0
  owner_agent: codenavi-agent
---

# enterprise-security-auditor

Read and follow `00_skills/(security)/enterprise-security-auditor/SKILL.md` and its relevant local modules.

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity.
```

### S085 | T1 | eol-advisory-sync

- path: `.agents/skills/eol-advisory-sync/SKILL.md`
- chars: 726
- outline:
- eol-advisory-sync

```markdown
---
name: eol-advisory-sync
description: Refresh local end-of-life/support metadata from endoflife.date API v1 and official maintainers with product aliases and freshness. Use when the user says atualizar a base EOL or sincronizar obsolescência. Do NOT use for CVE synchronization, vulnerability patching, or claiming unsupported internal libraries have public EOL dates.
license: CC-BY-4.0
metadata:
  author: AEOS; photographic reference supplied by user
  version: 1.0.0
  owner_agent: codenavi-agent
---

# eol-advisory-sync

Read and follow `00_skills/(security)/eol-advisory-sync/SKILL.md` and its relevant local modules.

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity.
```

### S086 | T1 | evaluation-runner

- path: `.agents/skills/evaluation-runner/SKILL.md`
- chars: 634
- outline:
- evaluation-runner

```markdown
---
name: evaluation-runner
description: Run an explicitly supplied evaluation suite and report reproducible results, failed cases and missing prerequisites. Use when the user requests evaluation runner or invokes evaluation-runner. Do NOT use as deployment authorization or as evidence for checks that were not executed.
license: CC-BY-4.0
metadata:
  author: AEOS
  version: 1.0.0
  owner_agent: codenavi-agent
---

# evaluation-runner

Read and follow `00_skills/(quality)/evaluation-runner/SKILL.md` and its relevant local modules.

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity.
```

### S087 | T1 | evidence-cache-auditor

- path: `.agents/skills/evidence-cache-auditor/SKILL.md`
- chars: 605
- outline:
- evidence-cache-auditor

```markdown
---
name: evidence-cache-auditor
description: Audit evidence cache keys, invalidation, allowed types and stale cache risks. Use when the user requests evidence cache auditor or invokes evidence-cache-auditor. Do NOT use for unrelated languages, domains or production deployment.
license: CC-BY-4.0
metadata:
  author: AEOS
  version: 1.0.0
  owner_agent: codenavi-agent
---

# evidence-cache-auditor

Read and follow `00_skills/(development)/evidence-cache-auditor/SKILL.md` and its relevant local modules.

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity.
```

### S088 | T1 | evidence-integrity-engineer

- path: `.agents/skills/evidence-integrity-engineer/SKILL.md`
- chars: 607
- outline:
- evidence-integrity-engineer

```markdown
---
name: evidence-integrity-engineer
description: Validate manifests, hash chains and tamper resistance. Use when the user requests evidence integrity engineer or invokes evidence-integrity-engineer. Do NOT use for unrelated languages, domains or production deployment.
license: CC-BY-4.0
metadata:
  author: AEOS
  version: 1.0.0
  owner_agent: codenavi-agent
---

# evidence-integrity-engineer

Read and follow `00_skills/(development)/evidence-integrity-engineer/SKILL.md` and its relevant local modules.

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity.
```

### S089 | T1 | evolutionary-modular-architecture

- path: `.agents/skills/evolutionary-modular-architecture/SKILL.md`
- chars: 1411
- outline:
- evolutionary-modular-architecture

```markdown
---
name: evolutionary-modular-architecture
description: Guides design and implementation of evolutionary modular-monolith platforms with DDD (strategic + tactical), flat-by-aggregate organization, an Anti-Corruption Layer for vendor independence, a transactional outbox for events, smart resilience (backoff with jitter, circuit breakers, idempotency), and a polished architecture HTML document with elegant SVG diagrams. Use when designing a platform or backend, defining bounded contexts, organizing modules and folders, choosing monolith vs microservices, decoupling from an external service (ERP, storage, AI), making calls resilient, adding real-time push, picking a 2026 TypeScript stack (Nx, NestJS, React), or producing an architecture document or diagram. Also triggers on 'modular monolith', 'bounded contexts', 'flat-by-aggregate', 'ports and adapters', 'architecture diagram'. Do NOT use for simple CRUD, NestJS-only deep implementation (use nestjs-modular-monolith), or pure domain-model review (use tactical-ddd).
license: CC-BY-4.0
metadata:
  author: Felipe Rodrigues - github.com/felipfr
  version: 1.0.0
  owner_agent: codenavi-agent
---

# evolutionary-modular-architecture

Read and follow `00_skills/(architecture)/evolutionary-modular-architecture/SKILL.md` and its relevant local modules.

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity.
```

### S090 | T1 | excalidraw-studio

- path: `.agents/skills/excalidraw-studio/SKILL.md`
- chars: 1086
- outline:
- excalidraw-studio

```markdown
---
name: excalidraw-studio
description: Generate Excalidraw diagrams from natural language descriptions. Outputs .excalidraw JSON files openable in Excalidraw. Use when asked to "create a diagram", "make a flowchart", "visualize a process", "draw a system architecture", "create a mind map", "generate an Excalidraw file", "draw an ER diagram", "create a sequence diagram", or "make a class diagram". Supports flowcharts, relationship diagrams, mind maps, architecture, DFD, swimlane, class, sequence, and ER diagrams. Can use icon libraries (AWS, GCP, etc.) when set up. Do NOT use for code architecture analysis (use the architecture skills), Mermaid diagram rendering (use mermaid-studio), or non-visual documentation (use docs-writer).
license: CC-BY-4.0
metadata:
  author: Felipe Rodrigues - github.com/felipfr
  version: 1.0.1
  owner_agent: codenavi-agent
---

# excalidraw-studio

Read and follow `00_skills/(tooling)/excalidraw-studio/SKILL.md` and its relevant local modules.

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity.
```

### S091 | T1 | expansion-retention

- path: `.agents/skills/expansion-retention/SKILL.md`
- chars: 1033
- outline:
- expansion-retention

```markdown
---
name: expansion-retention
description: When the user wants to reduce churn, build expansion revenue, automate customer success, or optimize net revenue retention. Also use when the user mentions 'churn,' 'retention,' 'expansion revenue,' 'upsell,' 'NRR,' 'net revenue retention,' 'customer success,' 'land and expand,' 'closed-lost,' or 'renewal.' This skill covers expansion and retention systems from usage triggers through automated customer success. Do NOT use for technical implementation, code review, or software architecture.
license: CC-BY-4.0
metadata:
  author: Chad Boyda / agent-gtm-skills
  version: 1.0.0
  original_author: Chad Boyda / agent-gtm-skills
  modified_by: Felipe Rodrigues - github.com/felipfr
  source: https://github.com/chadboyda/agent-gtm-skills
  owner_agent: codenavi-agent
---

# expansion-retention

Read and follow `00_skills/(gtm)/expansion-retention/SKILL.md` and its relevant local modules.

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity.
```

### S092 | T1 | fable

- path: `.agents/skills/fable/SKILL.md`
- chars: 664
- outline:
- fable

```markdown
---
name: fable
description: Standard problem-solving loop (classify ask, define done, gather evidence, decide, act surgically, verify by observation, report outcome-first). Use for non-trivial multi-step tasks, diagnosis, planning, or auditing work. Use when the user requests fable or invokes fable. Do NOT use for unrelated languages, domains or production deployment.
license: CC-BY-4.0
metadata:
  author: AEOS
  version: 1.0.0
  owner_agent: codenavi-agent
---

# fable

Read and follow `00_skills/(development)/fable/SKILL.md` and its relevant local modules.

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity.
```

### S093 | T1 | fable-aeos-harness

- path: `.agents/skills/fable-aeos-harness/SKILL.md`
- chars: 604
- outline:
- fable-aeos-harness

```markdown
---
name: fable-aeos-harness
description: Universal execution harness wrapping all AEOS skills with the Fable Method problem-solving loop. Use when the user requests fable aeos harness or invokes fable-aeos-harness. Do NOT use for unrelated languages, domains or production deployment.
license: CC-BY-4.0
metadata:
  author: AEOS
  version: 1.0.0
  owner_agent: codenavi-agent
---

# fable-aeos-harness

Read and follow `00_skills/(development)/fable-aeos-harness/SKILL.md` and its relevant local modules.

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity.
```

### S094 | T1 | fable-domain

- path: `.agents/skills/fable-domain/SKILL.md`
- chars: 557
- outline:
- fable-domain

```markdown
---
name: fable-domain
description: Research a domain, create a domain adapter, flowchart, trap fixture, and smoke eval for the Fable Method. Use when creating new sector adapters. Do NOT use for unrelated languages, domains or production deployment.
license: CC-BY-4.0
metadata:
  author: AEOS
  version: 1.0.0
  owner_agent: codenavi-agent
---

# fable-domain

Read and follow `00_skills/(development)/fable-domain/SKILL.md` and its relevant local modules.

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity.
```

### S095 | T1 | fable-judge

- path: `.agents/skills/fable-judge/SKILL.md`
- chars: 677
- outline:
- fable-judge

```markdown
---
name: fable-judge
description: Adversarial verification of finished work. Re-runs verifications, diffs changes, detects weakened checks and false completion claims, delivering VERIFIED, VERIFIED WITH CAVEATS, or REFUTED. Use when the user requests fable judge or invokes fable-judge. Do NOT use as deployment authorization or as evidence for checks that were not executed.
license: CC-BY-4.0
metadata:
  author: AEOS
  version: 1.0.0
  owner_agent: codenavi-agent
---

# fable-judge

Read and follow `00_skills/(quality)/fable-judge/SKILL.md` and its relevant local modules.

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity.
```

### S096 | T1 | fable-loop

- path: `.agents/skills/fable-loop/SKILL.md`
- chars: 617
- outline:
- fable-loop

```markdown
---
name: fable-loop
description: Orchestrated multi-stage workflow running parallel evidence internal lenses, single committed plan, surgical execution, and adversarial verification. Use when the user requests fable loop or invokes fable-loop. Do NOT use for unrelated languages, domains or production deployment.
license: CC-BY-4.0
metadata:
  author: AEOS
  version: 1.0.0
  owner_agent: codenavi-agent
---

# fable-loop

Read and follow `00_skills/(development)/fable-loop/SKILL.md` and its relevant local modules.

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity.
```

### S097 | T1 | figma

- path: `.agents/skills/figma/SKILL.md`
- chars: 787
- outline:
- figma

```markdown
---
name: figma
description: Use the Figma MCP server to fetch design context, screenshots, variables, and assets from Figma, and to translate Figma nodes into production code. Use when a task involves Figma URLs, node IDs, design-to-code implementation, or Figma MCP setup and troubleshooting. Covers general Figma data fetching and exploration. Do NOT use when the goal is specifically pixel-perfect code implementation from a Figma design (use figma-implement-design instead).
license: CC-BY-4.0
metadata:
  author: github.com/openai/skills
  version: 1.0.0
  owner_agent: codenavi-agent
---

# figma

Read and follow `00_skills/(design)/figma/SKILL.md` and its relevant local modules.

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity.
```

### S098 | T1 | figma-implement-design

- path: `.agents/skills/figma-implement-design/SKILL.md`
- chars: 846
- outline:
- figma-implement-design

```markdown
---
name: figma-implement-design
description: Translate Figma nodes into production-ready code with 1:1 visual fidelity using the Figma MCP workflow (design context, screenshots, assets, and project-convention translation). Use when the user provides Figma URLs or node IDs and asks to implement designs or components that must match Figma specs. Requires a working Figma MCP server connection. Do NOT use for general Figma data fetching, variable exploration, or MCP troubleshooting (use figma instead).
license: CC-BY-4.0
metadata:
  author: github.com/openai/skills
  version: 1.0.0
  owner_agent: codenavi-agent
---

# figma-implement-design

Read and follow `00_skills/(design)/figma-implement-design/SKILL.md` and its relevant local modules.

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity.
```

### S099 | T1 | fine-tuning-expert

- path: `.agents/skills/fine-tuning-expert/SKILL.md`
- chars: 560
- outline:
- fine-tuning-expert

```markdown
---
name: fine-tuning-expert
description: Decide whether fine-tuning is justified and implement a governed training pipeline when supported by the selected model/provider. Do NOT use for unrelated languages, domains or production deployment.
license: CC-BY-4.0
metadata:
  author: AEOS
  version: 1.0.0
  owner_agent: codenavi-agent
---

# fine-tuning-expert

Read and follow `00_skills/(development)/fine-tuning-expert/SKILL.md` and its relevant local modules.

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity.
```

### S100 | T1 | fixture-corpus-validator

- path: `.agents/skills/fixture-corpus-validator/SKILL.md`
- chars: 658
- outline:
- fixture-corpus-validator

```markdown
---
name: fixture-corpus-validator
description: Validate fixture corpus structure, provenance, integrity and expected-output contracts before evaluation. Use when the user requests fixture corpus validator or invokes fixture-corpus-validator. Do NOT use as deployment authorization or as evidence for checks that were not executed.
license: CC-BY-4.0
metadata:
  author: AEOS
  version: 1.0.0
  owner_agent: codenavi-agent
---

# fixture-corpus-validator

Read and follow `00_skills/(quality)/fixture-corpus-validator/SKILL.md` and its relevant local modules.

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity.
```

### S101 | T1 | fleet-mapping

- path: `.agents/skills/fleet-mapping/SKILL.md`
- chars: 760
- outline:
- fleet-mapping

```markdown
---
name: "fleet-mapping"
description: "Map authorized repository fleets by sigla with corporate, domain and repository knowledge, scoped glossaries, evidenced dependencies and an offline consolidated report. Use for mapear os repositorios da sigla, jornada do sistema, glossário do fleet or visão sistêmica. Do NOT use to fix one bug, provision infrastructure, mutate production or invent business rules."
license: "CC-BY-4.0"
metadata:
  author: "AEOS; photographic reference supplied by user"
  version: "1.1.0"
  owner_agent: "codenavi-agent"
---

# fleet-mapping

Read and follow `00_skills/(mapping)/fleet-mapping/SKILL.md` and its relevant local modules.

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity.
```

### S102 | T1 | frontend-blueprint

- path: `.agents/skills/frontend-blueprint/SKILL.md`
- chars: 1196
- outline:
- frontend-blueprint

```markdown
---
name: frontend-blueprint
description: AI frontend specialist and design consultant that guides users through a structured discovery process before generating any code. Collects visual references, design tokens, typography, icons, layout preferences, and brand guidelines to ensure the final output matches the user's vision with high fidelity. Use when the user asks to build, design, create, or improve any frontend interface — websites, landing pages, dashboards, components, apps, emails, forms, modals, or any UI element. Also triggers on "build me a UI", "design a page", "create a component", "improve this layout", "make this look better", "frontend", "interface", "redesign", or when the user provides mockups, screenshots, or design references. Do NOT use for backend logic, API design, database schemas, or non-visual code tasks.
license: CC-BY-4.0
metadata:
  author: Felipe Rodrigues - github.com/felipfr
  version: 1.0.0
  owner_agent: codenavi-agent
---

# frontend-blueprint

Read and follow `00_skills/(architecture)/frontend-blueprint/SKILL.md` and its relevant local modules.

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity.
```

### S103 | T1 | frontend-design

- path: `.agents/skills/frontend-design/SKILL.md`
- chars: 791
- outline:
- frontend-design

```markdown
---
name: frontend-design
description: Create distinctive, production-grade frontend interfaces with high design quality. Use this skill when the user asks to build web components, pages, artifacts, posters, or applications. Generates creative, polished code that avoids generic AI aesthetics. Do NOT use for design review or audit (use web-design-guidelines or web-quality-audit).
license: CC-BY-4.0
metadata:
  author: Impeccable (Paul Bakaus), based on Anthropic frontend-design
  version: 1.0.0
  owner_agent: codenavi-agent
source: https://github.com/pbakaus/impeccable
---

# frontend-design

Read and follow `00_skills/(design)/frontend-design/SKILL.md` and its relevant local modules.

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity.
```

### S104 | T1 | gh-address-comments

- path: `.agents/skills/gh-address-comments/SKILL.md`
- chars: 805
- outline:
- gh-address-comments

```markdown
---
name: gh-address-comments
description: Address review and issue comments on the open GitHub PR for the current branch using gh CLI. Use when user says "address PR comments", "fix review feedback", "respond to PR review", or "handle PR comments". Verifies gh auth first and prompts to authenticate if not logged in. Do NOT use for creating PRs, CI debugging (use gh-fix-ci), or general Git operations.
license: CC-BY-4.0
metadata:
  author: github.com/openai/skills
  version: 1.0.0
  short-description: Address comments in a GitHub PR review
  owner_agent: codenavi-agent
---

# gh-address-comments

Read and follow `00_skills/(development)/gh-address-comments/SKILL.md` and its relevant local modules.

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity.
```

### S105 | T1 | gh-fix-ci

- path: `.agents/skills/gh-fix-ci/SKILL.md`
- chars: 775
- outline:
- gh-fix-ci

```markdown
---
name: gh-fix-ci
description: Use when a user asks to debug or fix failing GitHub PR checks that run in GitHub Actions. Uses `gh` to inspect checks and logs, summarize failure context, draft a fix plan, and implement only after explicit approval. Treats external providers (for example Buildkite) as out of scope and reports only the details URL. Do NOT use for addressing PR review comments (use gh-address-comments) or general CI outside GitHub Actions.
license: CC-BY-4.0
metadata:
  author: github.com/openai/skills
  version: 1.0.0
  owner_agent: codenavi-agent
---

# gh-fix-ci

Read and follow `00_skills/(tooling)/gh-fix-ci/SKILL.md` and its relevant local modules.

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity.
```

### S106 | T1 | girl-voice-composer-simulation-expert

- path: `.agents/skills/girl-voice-composer-simulation-expert/SKILL.md`
- chars: 889
- outline:
- girl-voice-composer-simulation-expert

```markdown
---
name: girl-voice-composer-simulation-expert
description: Direct a TTS / voice-design engine to synthesize a GENERIC, fictional female child voice profile (age band 6-8) in Portuguese (pt-BR) and English (en-US), by producing bounded acoustic parameters (pitch, formants, prosody, syllable rhythm, EQ). Never clones or replicates any identifiable real child. Use when the user requests girl voice composer simulation expert or invokes girl-voice-composer-simulation-expert. Do NOT use for unrelated tools or unapproved remote writes.
license: CC-BY-4.0
metadata:
  author: AEOS
  version: 1.0.0
  owner_agent: codenavi-agent
---

# girl-voice-composer-simulation-expert

Read and follow `00_skills/(tooling)/girl-voice-composer-simulation-expert/SKILL.md` and its relevant local modules.

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity.
```

### S107 | T1 | github-operations

- path: `.agents/skills/github-operations/SKILL.md`
- chars: 642
- outline:
- github-operations

```markdown
---
name: github-operations
description: Governed Git and GitHub operations with runtime-only authentication, immutable safety denials, branch/PR/workflow management and Work Bundle integration. Use when the user requests github operations or invokes github-operations. Do NOT use for unrelated tools or unapproved remote writes.
license: CC-BY-4.0
metadata:
  author: AEOS
  version: 1.0.0
  owner_agent: codenavi-agent
---

# github-operations

Read and follow `00_skills/(tooling)/github-operations/SKILL.md` and its relevant local modules.

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity.
```

### S108 | T1 | grafana-observability-staff

- path: `.agents/skills/grafana-observability-staff/SKILL.md`
- chars: 748
- outline:
- grafana-observability-staff

```markdown
---
name: grafana-observability-staff
description: Deep Staff-level Grafana observability analysis for dashboards, Prometheus metrics, Loki logs, Tempo traces, alerts, exemplars, service maps, SLOs and instrumentation quality. Use when the user requests grafana observability staff or invokes grafana-observability-staff. Do NOT use to restart, scale or mutate live systems without an authorized operations task.
license: CC-BY-4.0
metadata:
  author: AEOS
  version: 1.0.0
  owner_agent: codenavi-agent
---

# grafana-observability-staff

Read and follow `00_skills/(monitoring)/grafana-observability-staff/SKILL.md` and its relevant local modules.

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity.
```

### S109 | T1 | gtm-engineering

- path: `.agents/skills/gtm-engineering/SKILL.md`
- chars: 1069
- outline:
- gtm-engineering

```markdown
---
name: gtm-engineering
description: When the user wants to build GTM automation with code, design workflow architectures, use AI agents for GTM tasks, or implement the 'architecture over tools' principle. Also use when the user mentions 'GTM engineering,' 'GTM automation,' 'n8n,' 'Make,' 'Zapier,' 'workflow automation,' 'Clay API,' 'instruction stacks,' 'AI agents for GTM,' or 'revenue automation.' This skill covers technical GTM infrastructure from workflow design through agent orchestration. Do NOT use for technical implementation, code review, or software architecture.
license: CC-BY-4.0
metadata:
  author: Chad Boyda / agent-gtm-skills
  version: 1.0.0
  original_author: Chad Boyda / agent-gtm-skills
  modified_by: Felipe Rodrigues - github.com/felipfr
  source: https://github.com/chadboyda/agent-gtm-skills
  owner_agent: codenavi-agent
---

# gtm-engineering

Read and follow `00_skills/(gtm)/gtm-engineering/SKILL.md` and its relevant local modules.

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity.
```

### S110 | T1 | gtm-metrics

- path: `.agents/skills/gtm-metrics/SKILL.md`
- chars: 1154
- outline:
- gtm-metrics

```markdown
---
name: gtm-metrics
description: When the user wants to define GTM metrics, build a metrics dashboard, measure pipeline efficiency, or track AI product performance. Also use when the user mentions 'GTM metrics,' 'revenue latency,' 'pipeline metrics,' 'TTFV,' 'time-to-first-value,' 'data health,' 'attribution,' 'conversion rate,' 'CAC,' 'LTV,' 'NRR,' 'GTM dashboard,' 'magic number,' 'pipeline velocity,' or 'funnel metrics.' This skill covers GTM measurement from metric selection through dashboard design, including AI-specific cost metrics, attribution models, and weekly review cadences. Do NOT use for technical implementation, code review, or software architecture.
license: CC-BY-4.0
metadata:
  author: Chad Boyda / agent-gtm-skills
  version: 1.0.0
  original_author: Chad Boyda / agent-gtm-skills
  modified_by: Felipe Rodrigues - github.com/felipfr
  source: https://github.com/chadboyda/agent-gtm-skills
  owner_agent: codenavi-agent
---

# gtm-metrics

Read and follow `00_skills/(gtm)/gtm-metrics/SKILL.md` and its relevant local modules.

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity.
```

### S111 | T1 | handoff-manager

- path: `.agents/skills/handoff-manager/SKILL.md`
- chars: 614
- outline:
- handoff-manager

```markdown
---
name: handoff-manager
description: Maintain a concise, executable `.notebook/HANDOFF.md` representing only the last verified operational state. Use when the user requests handoff manager or invokes handoff-manager. Do NOT use to promote unverified claims or transient task status into durable memory.
license: CC-BY-4.0
metadata:
  author: AEOS
  version: 1.0.0
  owner_agent: codenavi-agent
---

# handoff-manager

Read and follow `00_skills/(learning)/handoff-manager/SKILL.md` and its relevant local modules.

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity.
```

### S112 | T1 | harness-eval

- path: `.agents/skills/harness-eval/SKILL.md`
- chars: 1221
- outline:
- harness-eval

```markdown
---
name: harness-eval
description: 'Evaluate a repo agent harness (AGENTS.md, rules, skills, skill refs) for broken paths/commands, redundant instructions, and usefulness using a stack-agnostic dual-judge protocol with planted traps. HIGH PRIORITY questionnaires at top: Q1 optional docs, Q2 B/C budget before Track A (certainty/tokens). A always runs after Q2; B/C opt-in. ADRs/RFCs excluded from T2. Mixed apply uses 11-mixed-apply.md (KEEP/CUT). Use when the user says harness eval, harness-eval, harness debug, audit AGENTS.md, audit skills/rules, instruction audit, redundancy of agent instructions, usefulness of skills, Ship/Review/Hold/Slim/Keep-core for harness, or wants Track A/B/C harness evaluation. Do NOT use for harness setup or init, feature spec-driven work (tlc-spec-driven), or applying Ship/Slim trims unless the user explicitly asks after the report.'
license: CC-BY-4.0
metadata:
  author: Tech Leads Club - github.com/tech-leads-club
  version: 1.8.3
  owner_agent: codenavi-agent
---

# harness-eval

Read and follow `00_skills/(development)/harness-eval/SKILL.md` and its relevant local modules.

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity.
```

### S113 | T1 | impeccable

- path: `.agents/skills/impeccable/SKILL.md`
- chars: 1247
- outline:
- impeccable

```markdown
---
name: "impeccable"
description: "Use when the user wants to design, redesign, shape, critique, audit, polish, clarify, distill, harden, optimize, adapt, animate, colorize, extract, or otherwise improve a frontend interface. Covers websites, landing pages, dashboards, product UI, app shells, components, forms, settings, onboarding, and empty states. Handles UX review, visual hierarchy, information architecture, cognitive load, accessibility, performance, responsive behavior, theming, anti-patterns, typography, fonts, spacing, layout, alignment, color, motion, micro-interactions, UX copy, error states, edge cases, i18n, and reusable design systems or tokens. Also use for bland designs that need to become bolder or more delightful, loud designs that should become quieter, live browser iteration on UI elements, or ambitious visual effects that should feel technically extraordinary. Not for backend-only or non-UI tasks."
license: "Apache-2.0"
metadata:
  author: "Paul Bakaus"
  version: "4.1.1"
  owner_agent: "codenavi-agent"
---

# impeccable

Read and follow `00_skills/(design)/impeccable/SKILL.md` and its relevant local modules.

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity.
```

### S114 | T1 | incident-commander

- path: `.agents/skills/incident-commander/SKILL.md`
- chars: 588
- outline:
- incident-commander

```markdown
---
name: incident-commander
description: Generate incident triage, rollback and postmortem artifacts. Use when the user requests incident commander or invokes incident-commander. Do NOT use to restart, scale or mutate live systems without an authorized operations task.
license: CC-BY-4.0
metadata:
  author: AEOS
  version: 1.0.0
  owner_agent: codenavi-agent
---

# incident-commander

Read and follow `00_skills/(monitoring)/incident-commander/SKILL.md` and its relevant local modules.

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity.
```

### S115 | T1 | incident-response-assistant

- path: `.agents/skills/incident-response-assistant/SKILL.md`
- chars: 664
- outline:
- incident-response-assistant

```markdown
---
name: incident-response-assistant
description: Support human-led incident triage, RCA and recovery without replacing production authority. Use when the user requests incident response assistant or invokes incident-response-assistant. Do NOT use to restart, scale or mutate live systems without an authorized operations task.
license: CC-BY-4.0
metadata:
  author: AEOS
  version: 1.0.0
  owner_agent: codenavi-agent
---

# incident-response-assistant

Read and follow `00_skills/(monitoring)/incident-response-assistant/SKILL.md` and its relevant local modules.

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity.
```

### S116 | T1 | java-11-expert

- path: `.agents/skills/java-11-expert/SKILL.md`
- chars: 582
- outline:
- java-11-expert

```markdown
---
name: java-11-expert
description: Build and modernize production Java 11 systems with explicit Java 8→11 compatibility analysis. Use when the user requests java 11 expert or invokes java-11-expert. Do NOT use for unrelated languages, domains or production deployment.
license: CC-BY-4.0
metadata:
  author: AEOS
  version: 1.0.0
  owner_agent: codenavi-agent
---

# java-11-expert

Read and follow `00_skills/(development)/java-11-expert/SKILL.md` and its relevant local modules.

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity.
```

### S117 | T1 | java-17-expert

- path: `.agents/skills/java-17-expert/SKILL.md`
- chars: 542
- outline:
- java-17-expert

```markdown
---
name: java-17-expert
description: Implement and migrate LTS Java 17 applications safely. Use when the user requests java 17 expert or invokes java-17-expert. Do NOT use for unrelated languages, domains or production deployment.
license: CC-BY-4.0
metadata:
  author: AEOS
  version: 1.0.0
  owner_agent: codenavi-agent
---

# java-17-expert

Read and follow `00_skills/(development)/java-17-expert/SKILL.md` and its relevant local modules.

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity.
```

### S118 | T1 | java-21-expert

- path: `.agents/skills/java-21-expert/SKILL.md`
- chars: 579
- outline:
- java-21-expert

```markdown
---
name: java-21-expert
description: Design and implement Java 21 production systems and migrations with LTS-aware verification. Use when the user requests java 21 expert or invokes java-21-expert. Do NOT use for unrelated languages, domains or production deployment.
license: CC-BY-4.0
metadata:
  author: AEOS
  version: 1.0.0
  owner_agent: codenavi-agent
---

# java-21-expert

Read and follow `00_skills/(development)/java-21-expert/SKILL.md` and its relevant local modules.

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity.
```

### S119 | T1 | java-25-expert

- path: `.agents/skills/java-25-expert/SKILL.md`
- chars: 619
- outline:
- java-25-expert

```markdown
---
name: java-25-expert
description: Build or migrate production Java 25 projects using only features/APIs verified for the repository toolchain and deployment runtime. Use when the user requests java 25 expert or invokes java-25-expert. Do NOT use for unrelated languages, domains or production deployment.
license: CC-BY-4.0
metadata:
  author: AEOS
  version: 1.0.0
  owner_agent: codenavi-agent
---

# java-25-expert

Read and follow `00_skills/(development)/java-25-expert/SKILL.md` and its relevant local modules.

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity.
```

### S120 | T1 | java-26-expert

- path: `.agents/skills/java-26-expert/SKILL.md`
- chars: 630
- outline:
- java-26-expert

```markdown
---
name: java-26-expert
description: Build or migrate production Java 26 projects with explicit handling of current/preview/incubator status and verified deployment compatibility. Use when the user requests java 26 expert or invokes java-26-expert. Do NOT use for unrelated languages, domains or production deployment.
license: CC-BY-4.0
metadata:
  author: AEOS
  version: 1.0.0
  owner_agent: codenavi-agent
---

# java-26-expert

Read and follow `00_skills/(development)/java-26-expert/SKILL.md` and its relevant local modules.

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity.
```

### S121 | T1 | java-8-expert

- path: `.agents/skills/java-8-expert/SKILL.md`
- chars: 598
- outline:
- java-8-expert

```markdown
---
name: java-8-expert
description: Implement, diagnose and modernize Java 8 systems without silently using APIs or language features introduced later. Use when the user requests java 8 expert or invokes java-8-expert. Do NOT use for unrelated languages, domains or production deployment.
license: CC-BY-4.0
metadata:
  author: AEOS
  version: 1.0.0
  owner_agent: codenavi-agent
---

# java-8-expert

Read and follow `00_skills/(development)/java-8-expert/SKILL.md` and its relevant local modules.

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity.
```

### S122 | T1 | java-bug-solver

- path: `.agents/skills/java-bug-solver/SKILL.md`
- chars: 617
- outline:
- java-bug-solver

```markdown
---
name: java-bug-solver
description: Analyze Java stack traces, identify root causes, generate fixes, validate corrections and preserve verified lessons learned. Use when the user requests java bug solver or invokes java-bug-solver. Do NOT use for unrelated languages, domains or production deployment.
license: CC-BY-4.0
metadata:
  author: AEOS
  version: 1.0.0
  owner_agent: codenavi-agent
---

# java-bug-solver

Read and follow `00_skills/(development)/java-bug-solver/SKILL.md` and its relevant local modules.

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity.
```

### S123 | T1 | java-bug-solver-skill

- path: `.agents/skills/java-bug-solver-skill/SKILL.md`
- chars: 666
- outline:
- java-bug-solver-skill

```markdown
---
name: java-bug-solver-skill
description: Create a Java Bug Solver skill that analyzes stack traces, searches for root causes, generates fixes, validates them and stores lessons learned Use when the user requests java bug solver skill or invokes java-bug-solver-skill. Do NOT use for unrelated languages, domains or production deployment.
license: CC-BY-4.0
metadata:
  author: AEOS
  version: 1.0.0
  owner_agent: codenavi-agent
---

# java-bug-solver-skill

Read and follow `00_skills/(development)/java-bug-solver-skill/SKILL.md` and its relevant local modules.

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity.
```

### S124 | T1 | java-enterprise-modernizer

- path: `.agents/skills/java-enterprise-modernizer/SKILL.md`
- chars: 614
- outline:
- java-enterprise-modernizer

```markdown
---
name: java-enterprise-modernizer
description: Analyze Java/Spring enterprise modernization opportunities safely. Use when the user requests java enterprise modernizer or invokes java-enterprise-modernizer. Do NOT use for unrelated languages, domains or production deployment.
license: CC-BY-4.0
metadata:
  author: AEOS
  version: 1.0.0
  owner_agent: codenavi-agent
---

# java-enterprise-modernizer

Read and follow `00_skills/(development)/java-enterprise-modernizer/SKILL.md` and its relevant local modules.

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity.
```

### S125 | T1 | java-expert

- path: `.agents/skills/java-expert/SKILL.md`
- chars: 609
- outline:
- java-expert

```markdown
---
name: java-expert
description: Implement, diagnose, modernize and migrate real Java projects with version-correct APIs, minimal diffs and evidence-backed verification. Use when the user requests java expert or invokes java-expert. Do NOT use for unrelated languages, domains or production deployment.
license: CC-BY-4.0
metadata:
  author: AEOS
  version: 1.0.0
  owner_agent: codenavi-agent
---

# java-expert

Read and follow `00_skills/(development)/java-expert/SKILL.md` and its relevant local modules.

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity.
```

### S126 | T1 | java-migration

- path: `.agents/skills/java-migration/SKILL.md`
- chars: 592
- outline:
- java-migration

```markdown
---
name: java-migration
description: Analyze Java projects and perform version migrations, API replacements, and build configuration updates. Use when the user requests java migration or invokes java-migration. Do NOT use for unrelated languages, domains or production deployment.
license: CC-BY-4.0
metadata:
  author: AEOS
  version: 1.0.0
  owner_agent: codenavi-agent
---

# java-migration

Read and follow `00_skills/(development)/java-migration/SKILL.md` and its relevant local modules.

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity.
```

### S127 | T1 | java-version-expert

- path: `.agents/skills/java-version-expert/SKILL.md`
- chars: 607
- outline:
- java-version-expert

```markdown
---
name: java-version-expert
description: Route Java work to the exact verified JDK profile without loading unrelated version knowledge. Use when the user requests java version expert or invokes java-version-expert. Do NOT use for unrelated languages, domains or production deployment.
license: CC-BY-4.0
metadata:
  author: AEOS
  version: 1.0.0
  owner_agent: codenavi-agent
---

# java-version-expert

Read and follow `00_skills/(development)/java-version-expert/SKILL.md` and its relevant local modules.

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity.
```

### S128 | T1 | javascript-expert

- path: `.agents/skills/javascript-expert/SKILL.md`
- chars: 643
- outline:
- javascript-expert

```markdown
---
name: javascript-expert
description: Implement, diagnose and modernize JavaScript projects with exact runtime/module-system/browser compatibility and repository-native patterns. Use when the user requests javascript expert or invokes javascript-expert. Do NOT use for unrelated languages, domains or production deployment.
license: CC-BY-4.0
metadata:
  author: AEOS
  version: 1.0.0
  owner_agent: codenavi-agent
---

# javascript-expert

Read and follow `00_skills/(development)/javascript-expert/SKILL.md` and its relevant local modules.

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity.
```

### S129 | T1 | jev-call-expert

- path: `.agents/skills/jev-call-expert/SKILL.md`
- chars: 847
- outline:
- jev-call-expert

```markdown
---
name: jev-call-expert
description: Design, implement, review, and test confidence-aware function calling with TypeSafe Jev, typed tool signatures, Choice and Noul questions, speculative fan-out, and code-owned execution policy. Use when the user asks for Jev tool calling, TypeSafe function routing, natural-language dispatch into typed functions, or repair of a Jev dispatcher. Do NOT use for generic LLM tool calling that does not use TypeSafe, open-ended text generation, or direct execution of untrusted or unapproved actions.
license: CC-BY-4.0
metadata:
  author: AEOS
  version: 2.0.0
  owner_agent: codenavi-agent
---

# jev-call-expert

Read and follow `00_skills/(development)/jev-call-expert/SKILL.md` and its relevant local modules.

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity.
```

### S130 | T1 | jira-assistant

- path: `.agents/skills/jira-assistant/SKILL.md`
- chars: 714
- outline:
- jira-assistant

```markdown
---
name: jira-assistant
description: Manage Jira issues via Atlassian MCP — search, create, update, transition status, and handle sprint tasks. Auto-detects workspace configuration. Use when user says "create a Jira ticket", "update my sprint", "check Jira status", "transition this issue", "search Jira", or "move ticket to done". Do NOT use for Confluence pages (use confluence-assistant).
license: CC-BY-4.0
metadata:
  author: Tech Leads Club
  version: 1.0.0
  owner_agent: codenavi-agent
---

# jira-assistant

Read and follow `00_skills/(development)/jira-assistant/SKILL.md` and its relevant local modules.

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity.
```

### S131 | T1 | jira-confluence-assistant

- path: `.agents/skills/jira-confluence-assistant/SKILL.md`
- chars: 683
- outline:
- jira-confluence-assistant

```markdown
---
name: jira-confluence-assistant
description: Read, analyze and prepare governed Jira/Confluence work while preserving traceability between requirement, code, evidence and documentation. Use when the user requests jira confluence assistant or invokes jira-confluence-assistant. Do NOT use for unrelated languages, domains or production deployment.
license: CC-BY-4.0
metadata:
  author: AEOS
  version: 1.0.0
  owner_agent: codenavi-agent
---

# jira-confluence-assistant

Read and follow `00_skills/(development)/jira-confluence-assistant/SKILL.md` and its relevant local modules.

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity.
```

### S132 | T1 | jira-time-entry-assistant

- path: `.agents/skills/jira-time-entry-assistant/SKILL.md`
- chars: 621
- outline:
- jira-time-entry-assistant

```markdown
---
name: jira-time-entry-assistant
description: Prepare auditable Jira worklog/time-entry proposals from actual task evidence. Use when the user requests jira time entry assistant or invokes jira-time-entry-assistant. Do NOT use for unrelated languages, domains or production deployment.
license: CC-BY-4.0
metadata:
  author: AEOS
  version: 1.0.0
  owner_agent: codenavi-agent
---

# jira-time-entry-assistant

Read and follow `00_skills/(development)/jira-time-entry-assistant/SKILL.md` and its relevant local modules.

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity.
```

### S133 | T1 | judge-benchmark-runner

- path: `.agents/skills/judge-benchmark-runner/SKILL.md`
- chars: 658
- outline:
- judge-benchmark-runner

```markdown
---
name: judge-benchmark-runner
description: Benchmark a deterministic Judge gate against a supplied corpus and fixed thresholds without creating a Judge agent. Use when the user requests judge benchmark runner or invokes judge-benchmark-runner. Do NOT use as deployment authorization or as evidence for checks that were not executed.
license: CC-BY-4.0
metadata:
  author: AEOS
  version: 1.0.0
  owner_agent: codenavi-agent
---

# judge-benchmark-runner

Read and follow `00_skills/(quality)/judge-benchmark-runner/SKILL.md` and its relevant local modules.

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity.
```

### S134 | T1 | kinghost-backup-recovery-expert

- path: `.agents/skills/kinghost-backup-recovery-expert/SKILL.md`
- chars: 696
- outline:
- kinghost-backup-recovery-expert

```markdown
---
name: kinghost-backup-recovery-expert
description: Governed KingHost backup and recovery skill for sites/FTP, databases and email with rollback-safe restore verification. Use when the user requests kinghost backup recovery expert or invokes kinghost-backup-recovery-expert. Do NOT use for unrelated application features or unapproved production changes.
license: CC-BY-4.0
metadata:
  author: AEOS
  version: 1.0.0
  owner_agent: codenavi-agent
---

# kinghost-backup-recovery-expert

Read and follow `00_skills/(cloud)/kinghost-backup-recovery-expert/SKILL.md` and its relevant local modules.

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity.
```

### S135 | T1 | kinghost-clone-site-expert

- path: `.agents/skills/kinghost-clone-site-expert/SKILL.md`
- chars: 706
- outline:
- kinghost-clone-site-expert

```markdown
---
name: kinghost-clone-site-expert
description: Governed KingHost full-site clone skill that acquires an integrity-verified FTP copy without mutating the remote origin and without silently losing files. Use when the user requests kinghost clone site expert or invokes kinghost-clone-site-expert. Do NOT use for unrelated application features or unapproved production changes.
license: CC-BY-4.0
metadata:
  author: AEOS
  version: 1.0.0
  owner_agent: codenavi-agent
---

# kinghost-clone-site-expert

Read and follow `00_skills/(cloud)/kinghost-clone-site-expert/SKILL.md` and its relevant local modules.

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity.
```

### S136 | T1 | kinghost-database-expert

- path: `.agents/skills/kinghost-database-expert/SKILL.md`
- chars: 664
- outline:
- kinghost-database-expert

```markdown
---
name: kinghost-database-expert
description: Governed KingHost MySQL/database engineering skill for creation, access, backup, query analysis, migration and recovery. Use when the user requests kinghost database expert or invokes kinghost-database-expert. Do NOT use for an unrelated implementation change or deployment execution.
license: CC-BY-4.0
metadata:
  author: AEOS
  version: 1.0.0
  owner_agent: codenavi-agent
---

# kinghost-database-expert

Read and follow `00_skills/(architecture)/kinghost-database-expert/SKILL.md` and its relevant local modules.

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity.
```

### S137 | T1 | kinghost-domain-dns-ssl-expert

- path: `.agents/skills/kinghost-domain-dns-ssl-expert/SKILL.md`
- chars: 685
- outline:
- kinghost-domain-dns-ssl-expert

```markdown
---
name: kinghost-domain-dns-ssl-expert
description: Governed KingHost domain, subdomain, DNS and SSL operations with snapshot, rollback and propagation verification. Use when the user requests kinghost domain dns ssl expert or invokes kinghost-domain-dns-ssl-expert. Do NOT use for unrelated application features or unapproved production changes.
license: CC-BY-4.0
metadata:
  author: AEOS
  version: 1.0.0
  owner_agent: codenavi-agent
---

# kinghost-domain-dns-ssl-expert

Read and follow `00_skills/(cloud)/kinghost-domain-dns-ssl-expert/SKILL.md` and its relevant local modules.

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity.
```

### S138 | T1 | kinghost-email-expert

- path: `.agents/skills/kinghost-email-expert/SKILL.md`
- chars: 661
- outline:
- kinghost-email-expert

```markdown
---
name: kinghost-email-expert
description: Governed KingHost email operations for mailbox creation, DNS/MX alignment, Webmail/client setup and recovery without exposing secrets. Use when the user requests kinghost email expert or invokes kinghost-email-expert. Do NOT use for unrelated application features or unapproved production changes.
license: CC-BY-4.0
metadata:
  author: AEOS
  version: 1.0.0
  owner_agent: codenavi-agent
---

# kinghost-email-expert

Read and follow `00_skills/(cloud)/kinghost-email-expert/SKILL.md` and its relevant local modules.

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity.
```

### S139 | T1 | kinghost-expert

- path: `.agents/skills/kinghost-expert/SKILL.md`
- chars: 755
- outline:
- kinghost-expert

```markdown
---
name: kinghost-expert
description: 'Super-skill for complete KingHost Hospedagem operations: panel auth, domains/DNS/SSL, absolute FTP-visible site clone, governed FTP/SSH/Git publish, WordPress/PHP/MySQL, backups, email, antivirus/WAF, cache/performance and rollback-safe production changes. Use when the user requests kinghost expert or invokes kinghost-expert. Do NOT use for unrelated application features or unapproved production changes.'
license: CC-BY-4.0
metadata:
  author: AEOS
  version: 1.0.0
  owner_agent: codenavi-agent
---

# kinghost-expert

Read and follow `00_skills/(cloud)/kinghost-expert/SKILL.md` and its relevant local modules.

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity.
```

### S140 | T1 | kinghost-performance-expert

- path: `.agents/skills/kinghost-performance-expert/SKILL.md`
- chars: 705
- outline:
- kinghost-performance-expert

```markdown
---
name: kinghost-performance-expert
description: Measurement-driven KingHost performance skill for resource consumption, Varnish/cache, PHP runtime, PageSpeed and application/database optimization. Use when the user requests kinghost performance expert or invokes kinghost-performance-expert. Do NOT use for unrelated application features or unapproved production changes.
license: CC-BY-4.0
metadata:
  author: AEOS
  version: 1.0.0
  owner_agent: codenavi-agent
---

# kinghost-performance-expert

Read and follow `00_skills/(cloud)/kinghost-performance-expert/SKILL.md` and its relevant local modules.

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity.
```

### S141 | T1 | kinghost-security-expert

- path: `.agents/skills/kinghost-security-expert/SKILL.md`
- chars: 662
- outline:
- kinghost-security-expert

```markdown
---
name: kinghost-security-expert
description: KingHost hosting security skill for antivirus/malware scanning, quarantine review, WAF, SSL and post-incident verification. Use when the user requests kinghost security expert or invokes kinghost-security-expert. Do NOT use outside authorized defensive scope or to expose secret values.
license: CC-BY-4.0
metadata:
  author: AEOS
  version: 1.0.0
  owner_agent: codenavi-agent
---

# kinghost-security-expert

Read and follow `00_skills/(security)/kinghost-security-expert/SKILL.md` and its relevant local modules.

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity.
```

### S142 | T1 | kinghost-site-publish-ftp-expert

- path: `.agents/skills/kinghost-site-publish-ftp-expert/SKILL.md`
- chars: 711
- outline:
- kinghost-site-publish-ftp-expert

```markdown
---
name: kinghost-site-publish-ftp-expert
description: Governed KingHost PHP/WordPress FTP publishing skill with bounded diffs, backup, approval, rollback and post-deploy verification. Use when the user requests kinghost site publish ftp expert or invokes kinghost-site-publish-ftp-expert. Do NOT use for unrelated application features or unapproved production changes.
license: CC-BY-4.0
metadata:
  author: AEOS
  version: 1.0.0
  owner_agent: codenavi-agent
---

# kinghost-site-publish-ftp-expert

Read and follow `00_skills/(cloud)/kinghost-site-publish-ftp-expert/SKILL.md` and its relevant local modules.

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity.
```

### S143 | T1 | kotlin-expert

- path: `.agents/skills/kotlin-expert/SKILL.md`
- chars: 620
- outline:
- kotlin-expert

```markdown
---
name: kotlin-expert
description: Design and implement Kotlin production systems and migrations against the current stable Kotlin release, with version-aware verification. Use when the user requests kotlin expert or invokes kotlin-expert. Do NOT use for unrelated languages, domains or production deployment.
license: CC-BY-4.0
metadata:
  author: AEOS
  version: 1.0.0
  owner_agent: codenavi-agent
---

# kotlin-expert

Read and follow `00_skills/(development)/kotlin-expert/SKILL.md` and its relevant local modules.

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity.
```

### S144 | T1 | kubernetes-code-context-mapper

- path: `.agents/skills/kubernetes-code-context-mapper/SKILL.md`
- chars: 726
- outline:
- kubernetes-code-context-mapper

```markdown
---
name: kubernetes-code-context-mapper
description: Map Kubernetes pods, workloads, services, labels, metrics, logs and deployment metadata back to repository code, owners, tests and remediation boundaries. Use when the user requests kubernetes code context mapper or invokes kubernetes-code-context-mapper. Do NOT use for unrelated application features or unapproved production changes.
license: CC-BY-4.0
metadata:
  author: AEOS
  version: 1.0.0
  owner_agent: codenavi-agent
---

# kubernetes-code-context-mapper

Read and follow `00_skills/(cloud)/kubernetes-code-context-mapper/SKILL.md` and its relevant local modules.

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity.
```

### S145 | T1 | kubernetes-observability-staff

- path: `.agents/skills/kubernetes-observability-staff/SKILL.md`
- chars: 761
- outline:
- kubernetes-observability-staff

```markdown
---
name: kubernetes-observability-staff
description: Deep Staff-level Kubernetes observability analysis for cluster health, workloads, events, metrics, logs, probes, scheduling, resources, networking and control-plane signals. Use when the user requests kubernetes observability staff or invokes kubernetes-observability-staff. Do NOT use to restart, scale or mutate live systems without an authorized operations task.
license: CC-BY-4.0
metadata:
  author: AEOS
  version: 1.0.0
  owner_agent: codenavi-agent
---

# kubernetes-observability-staff

Read and follow `00_skills/(monitoring)/kubernetes-observability-staff/SKILL.md` and its relevant local modules.

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity.
```

### S146 | T1 | lead-enrichment

- path: `.agents/skills/lead-enrichment/SKILL.md`
- chars: 1056
- outline:
- lead-enrichment

```markdown
---
name: lead-enrichment
description: When the user wants to build data enrichment workflows, score leads against ICP, set up Clay waterfalls, or improve contact data quality. Also use when the user mentions 'enrichment,' 'data enrichment,' 'Clay,' 'waterfall enrichment,' 'ICP scoring,' 'lead scoring,' 'intent data,' 'contact verification,' 'Apollo,' 'ZoomInfo,' or 'data quality.' This skill covers lead enrichment waterfalls, ICP scoring frameworks, and contact verification systems. Do NOT use for technical implementation, code review, or software architecture.
license: CC-BY-4.0
metadata:
  author: Chad Boyda / agent-gtm-skills
  version: 1.0.0
  original_author: Chad Boyda / agent-gtm-skills
  modified_by: Felipe Rodrigues - github.com/felipfr
  source: https://github.com/chadboyda/agent-gtm-skills
  owner_agent: codenavi-agent
---

# lead-enrichment

Read and follow `00_skills/(gtm)/lead-enrichment/SKILL.md` and its relevant local modules.

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity.
```

### S147 | T1 | learning-curator

- path: `.agents/skills/learning-curator/SKILL.md`
- chars: 587
- outline:
- learning-curator

```markdown
---
name: learning-curator
description: Promote verified, reusable engineering lessons into `.notebook/LEARNING.md`. Use when the user requests learning curator or invokes learning-curator. Do NOT use to promote unverified claims or transient task status into durable memory.
license: CC-BY-4.0
metadata:
  author: AEOS
  version: 1.0.0
  owner_agent: codenavi-agent
---

# learning-curator

Read and follow `00_skills/(learning)/learning-curator/SKILL.md` and its relevant local modules.

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity.
```

### S148 | T1 | learning-opportunities

- path: `.agents/skills/learning-opportunities/SKILL.md`
- chars: 805
- outline:
- learning-opportunities

```markdown
---
name: "learning-opportunities"
description: "Identify reusable lessons, durable facts, promotion candidates, ADRs or new skills from finished work. Use for o que aprendemos aqui, isso vale uma lição, isso merece virar skill, o que promovo or balanço da sessão. Do NOT use for writing or verify the continuity quartet (chromatic-mega-brain), build the identified skill (skill-architect), write the ADR (create-adr), or challenge a future decision (the-fool)."
license: "CC-BY-4.0"
metadata:
  author: "Tech Leads Club"
  version: "1.1.0"
  owner_agent: "codenavi-agent"
---

# learning-opportunities

Read and follow `00_skills/(learning)/learning-opportunities/SKILL.md` and its relevant local modules.

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity.
```

### S149 | T1 | legacy-migration-planner

- path: `.agents/skills/legacy-migration-planner/SKILL.md`
- chars: 868
- outline:
- legacy-migration-planner

```markdown
---
name: "legacy-migration-planner"
description: "Use when planning legacy system migrations, codebase modernization, monolith decomposition, microservices consolidation, cross-language rewrites, or framework upgrades. Invoke for strangler fig pattern, incremental migration strategy, or refactoring roadmaps. Do NOT use for domain analysis (use domain-analysis), component sizing (use component-identification-sizing), or step-by-step decomposition plans (use decomposition-planning-roadmap)."
license: "CC-BY-4.0"
metadata:
  author: "Felipe Rodrigues - github.com/felipfr"
  version: "1.0.0"
  owner_agent: "codenavi-agent"
---

# legacy-migration-planner

Read and follow `00_skills/(architecture)/legacy-migration-planner/SKILL.md` and its relevant local modules.

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity.
```

### S150 | T1 | legacy-risk-mapper

- path: `.agents/skills/legacy-risk-mapper/SKILL.md`
- chars: 578
- outline:
- legacy-risk-mapper

```markdown
---
name: legacy-risk-mapper
description: Map legacy risks, modernization blockers and migration strategy. Use when the user requests legacy risk mapper or invokes legacy-risk-mapper. Do NOT use for an unrelated implementation change or deployment execution.
license: CC-BY-4.0
metadata:
  author: AEOS
  version: 1.0.0
  owner_agent: codenavi-agent
---

# legacy-risk-mapper

Read and follow `00_skills/(architecture)/legacy-risk-mapper/SKILL.md` and its relevant local modules.

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity.
```

### S151 | T1 | llm-calibration-temperature-expert

- path: `.agents/skills/llm-calibration-temperature-expert/SKILL.md`
- chars: 717
- outline:
- llm-calibration-temperature-expert

```markdown
---
name: llm-calibration-temperature-expert
description: Engineer and evaluate decoding/calibration behavior for LLM applications instead of treating temperature as a magic quality knob. Use when the user requests llm calibration temperature expert or invokes llm-calibration-temperature-expert. Do NOT use for unrelated languages, domains or production deployment.
license: CC-BY-4.0
metadata:
  author: AEOS
  version: 1.0.0
  owner_agent: codenavi-agent
---

# llm-calibration-temperature-expert

Read and follow `00_skills/(development)/llm-calibration-temperature-expert/SKILL.md` and its relevant local modules.

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity.
```

### S152 | T1 | llm-model-selection-expert

- path: `.agents/skills/llm-model-selection-expert/SKILL.md`
- chars: 682
- outline:
- llm-model-selection-expert

```markdown
---
name: llm-model-selection-expert
description: Select the best current model/model-family for a concrete workload using live authoritative capability information plus project evals. Use when the user requests llm model selection expert or invokes llm-model-selection-expert. Do NOT use for unrelated languages, domains or production deployment.
license: CC-BY-4.0
metadata:
  author: AEOS
  version: 1.0.0
  owner_agent: codenavi-agent
---

# llm-model-selection-expert

Read and follow `00_skills/(development)/llm-model-selection-expert/SKILL.md` and its relevant local modules.

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity.
```

### S153 | T1 | local-secret-vault

- path: `.agents/skills/local-secret-vault/SKILL.md`
- chars: 649
- outline:
- local-secret-vault

```markdown
---
name: "local-secret-vault"
description: "Read authorized local credential vaults safely and expose only masked metadata or ephemeral secret references to governed tools. Use when the user requests local secret vault or invokes local-secret-vault. Do NOT use outside authorized defensive scope or to expose secret values."
license: "CC-BY-4.0"
metadata:
  author: "AEOS"
  version: "1.0.0"
  owner_agent: "codenavi-agent"
---

# local-secret-vault

Read and follow `00_skills/(security)/local-secret-vault/SKILL.md` and its relevant local modules.

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity.
```

### S154 | T1 | lora-qlora-dora-expert

- path: `.agents/skills/lora-qlora-dora-expert/SKILL.md`
- chars: 633
- outline:
- lora-qlora-dora-expert

```markdown
---
name: lora-qlora-dora-expert
description: Implement parameter-efficient fine-tuning for supported open-weight models with reproducible experiments. Use when the user requests lora qlora dora expert or invokes lora-qlora-dora-expert. Do NOT use for unrelated languages, domains or production deployment.
license: CC-BY-4.0
metadata:
  author: AEOS
  version: 1.0.0
  owner_agent: codenavi-agent
---

# lora-qlora-dora-expert

Read and follow `00_skills/(development)/lora-qlora-dora-expert/SKILL.md` and its relevant local modules.

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity.
```

### S155 | T1 | mantis-architecture

- path: `.agents/skills/mantis-architecture/SKILL.md`
- chars: 706
- outline:
- mantis-architecture

```markdown
---
name: mantis-architecture
description: Synthesizes raw learnings and codebase analysis into an interlinked Markdown Knowledge Base (KB). Use at the beginning of a loop to build or update architecture.md, entities, and vulnerabilities. Don't use for generating threat models or formulating execution plans. Use when the user requests mantis architecture or invokes mantis-architecture.
license: CC-BY-4.0
metadata:
  author: AEOS
  version: 1.0.0
  owner_agent: codenavi-agent
---

# mantis-architecture

Read and follow `00_skills/(security)/mantis-architecture/SKILL.md` and its relevant local modules.

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity.
```

### S156 | T1 | mantis-calibrate

- path: `.agents/skills/mantis-calibrate/SKILL.md`
- chars: 629
- outline:
- mantis-calibrate

```markdown
---
name: mantis-calibrate
description: Calculates the final risk score based on empirical evidence and architectural impact. Use when findings have been fully processed by previous stages and you need to append final risk scores to the finding files. Don't use for discovering new vulnerabilities or writing patches.
license: CC-BY-4.0
metadata:
  author: AEOS
  version: 1.0.0
  owner_agent: codenavi-agent
---

# mantis-calibrate

Read and follow `00_skills/(security)/mantis-calibrate/SKILL.md` and its relevant local modules.

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity.
```

### S157 | T1 | mantis-chain

- path: `.agents/skills/mantis-chain/SKILL.md`
- chars: 672
- outline:
- mantis-chain

```markdown
---
name: mantis-chain
description: Analyzes individual security findings to identify and construct complex exploit chains. Use after validation stages to see if multiple low-severity bugs can be combined into a higher impact vulnerability. Don't use for initial codebase auditing or writing patch code. Use when the user requests mantis chain or invokes mantis-chain.
license: CC-BY-4.0
metadata:
  author: AEOS
  version: 1.0.0
  owner_agent: codenavi-agent
---

# mantis-chain

Read and follow `00_skills/(security)/mantis-chain/SKILL.md` and its relevant local modules.

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity.
```

### S158 | T1 | mantis-critic

- path: `.agents/skills/mantis-critic/SKILL.md`
- chars: 639
- outline:
- mantis-critic

```markdown
---
name: mantis-critic
description: Assesses the production viability of findings, filtering out debug-only features and assertion traps. Use when findings have been validated and you need to confirm they are triggerable in production release builds (with assertions disabled). Don't use for writing reproduction scripts or patches.
license: CC-BY-4.0
metadata:
  author: AEOS
  version: 1.0.0
  owner_agent: codenavi-agent
---

# mantis-critic

Read and follow `00_skills/(security)/mantis-critic/SKILL.md` and its relevant local modules.

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity.
```

### S159 | T1 | mantis-dedupe

- path: `.agents/skills/mantis-dedupe/SKILL.md`
- chars: 564
- outline:
- mantis-dedupe

```markdown
---
name: mantis-dedupe
description: Consolidates raw security findings to eliminate redundant reports. Use when raw findings have been generated by the researcher and need consolidation before review. Don't use for initial code auditing or patch generation.
license: CC-BY-4.0
metadata:
  author: AEOS
  version: 1.0.0
  owner_agent: codenavi-agent
---

# mantis-dedupe

Read and follow `00_skills/(security)/mantis-dedupe/SKILL.md` and its relevant local modules.

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity.
```

### S160 | T1 | mantis-history

- path: `.agents/skills/mantis-history/SKILL.md`
- chars: 806
- outline:
- mantis-history

```markdown
---
name: mantis-history
description: Analyzes the repository's version control system (VCS) history to extract past vulnerabilities, security fixes, and vulnerability patterns. Use as an initial pre-processing step to build a historical vulnerabilities database (workspace/historical_learnings.jsonl) that informs subsequent stages about past issues and fixes. Don't use for code reviews, writing test scripts, or patching code. Use when the user requests mantis history or invokes mantis-history.
license: CC-BY-4.0
metadata:
  author: AEOS
  version: 1.0.0
  owner_agent: codenavi-agent
---

# mantis-history

Read and follow `00_skills/(security)/mantis-history/SKILL.md` and its relevant local modules.

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity.
```

### S161 | T1 | mantis-meta-agent

- path: `.agents/skills/mantis-meta-agent/SKILL.md`
- chars: 609
- outline:
- mantis-meta-agent

```markdown
---
name: mantis-meta-agent
description: Acts as the persistent supervisor, launching and monitoring the automated review campaign. Use when running a long-running, continuous security review campaign that needs autonomous coordination. Don't use for executing individual review stages directly.
license: CC-BY-4.0
metadata:
  author: AEOS
  version: 1.0.0
  owner_agent: codenavi-agent
---

# mantis-meta-agent

Read and follow `00_skills/(security)/mantis-meta-agent/SKILL.md` and its relevant local modules.

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity.
```

### S162 | T1 | mantis-patch

- path: `.agents/skills/mantis-patch/SKILL.md`
- chars: 651
- outline:
- mantis-patch

```markdown
---
name: mantis-patch
description: Generates minimal security fixes using transactional isolation (shadow directories or file backups), applies patches, and verifies them. Use when security findings are successfully reproduced and need patches applied and verified. Don't use for initial vulnerability research or reproduction payload generation.
license: CC-BY-4.0
metadata:
  author: AEOS
  version: 1.0.0
  owner_agent: codenavi-agent
---

# mantis-patch

Read and follow `00_skills/(security)/mantis-patch/SKILL.md` and its relevant local modules.

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity.
```

### S163 | T1 | mantis-pipeline-adapter

- path: `.agents/skills/mantis-pipeline-adapter/SKILL.md`
- chars: 616
- outline:
- mantis-pipeline-adapter

```markdown
---
name: mantis-pipeline-adapter
description: Interactively guides the design and implementation of custom deterministic orchestrator harnesses. Use when a user wants to build their own pipeline to wrap and run Mantis skills reliably. Don't use for executing the default pipeline directly.
license: CC-BY-4.0
metadata:
  author: AEOS
  version: 1.0.0
  owner_agent: codenavi-agent
---

# mantis-pipeline-adapter

Read and follow `00_skills/(security)/mantis-pipeline-adapter/SKILL.md` and its relevant local modules.

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity.
```

### S164 | T1 | mantis-plan

- path: `.agents/skills/mantis-plan/SKILL.md`
- chars: 651
- outline:
- mantis-plan

```markdown
---
name: mantis-plan
description: Formulates a targeted defensive security reviewing plan based on the active threat model and historical learnings. Use when starting a security review campaign to map the codebase boundaries and generate a roadmap (workspace/plan.json). Don't use for executing code reviews, writing test scripts, or patching code.
license: CC-BY-4.0
metadata:
  author: AEOS
  version: 1.0.0
  owner_agent: codenavi-agent
---

# mantis-plan

Read and follow `00_skills/(security)/mantis-plan/SKILL.md` and its relevant local modules.

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity.
```

### S165 | T1 | mantis-reflect

- path: `.agents/skills/mantis-reflect/SKILL.md`
- chars: 678
- outline:
- mantis-reflect

```markdown
---
name: mantis-reflect
description: Extracts learnings from execution trajectories at the end of a Mantis loop. Use to parse agent conversations, extract successes, failures, and false assumptions, and append them to workspace/learnings.jsonl. Don't use for analyzing source code or writing patches. Use when the user requests mantis reflect or invokes mantis-reflect.
license: CC-BY-4.0
metadata:
  author: AEOS
  version: 1.0.0
  owner_agent: codenavi-agent
---

# mantis-reflect

Read and follow `00_skills/(security)/mantis-reflect/SKILL.md` and its relevant local modules.

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity.
```

### S166 | T1 | mantis-report

- path: `.agents/skills/mantis-report/SKILL.md`
- chars: 649
- outline:
- mantis-report

```markdown
---
name: mantis-report
description: Generates a human-readable security review packet compiled from confirmed findings and exploit chains. Use at the end of a review cycle to produce stakeholder-facing documentation. Don't use for auditing code or verifying patches directly. Use when the user requests mantis report or invokes mantis-report.
license: CC-BY-4.0
metadata:
  author: AEOS
  version: 1.0.0
  owner_agent: codenavi-agent
---

# mantis-report

Read and follow `00_skills/(security)/mantis-report/SKILL.md` and its relevant local modules.

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity.
```

### S167 | T1 | mantis-reproduce

- path: `.agents/skills/mantis-reproduce/SKILL.md`
- chars: 561
- outline:
- mantis-reproduce

```markdown
---
name: mantis-reproduce
description: Generates and runs crash reproducers to verify security flaws. Use when viable findings exist and you need to write and execute a script or payload to verify the crash. Don't use for code auditing or patching.
license: CC-BY-4.0
metadata:
  author: AEOS
  version: 1.0.0
  owner_agent: codenavi-agent
---

# mantis-reproduce

Read and follow `00_skills/(security)/mantis-reproduce/SKILL.md` and its relevant local modules.

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity.
```

### S168 | T1 | mantis-researcher

- path: `.agents/skills/mantis-researcher/SKILL.md`
- chars: 606
- outline:
- mantis-researcher

```markdown
---
name: mantis-researcher
description: Audits production source code files based on the strategy in workspace/plan.json. Use when a review plan exists and you need to perform static analysis and deep-dive reviews of targeted files. Don't use for planning, deduplicating, or writing patches.
license: CC-BY-4.0
metadata:
  author: AEOS
  version: 1.0.0
  owner_agent: codenavi-agent
---

# mantis-researcher

Read and follow `00_skills/(security)/mantis-researcher/SKILL.md` and its relevant local modules.

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity.
```

### S169 | T1 | mantis-review

- path: `.agents/skills/mantis-review/SKILL.md`
- chars: 537
- outline:
- mantis-review

```markdown
---
name: mantis-review
description: Independently reviews findings and filters out false positives. Use when consolidated findings need validation against the actual source code. Don't use for reproducing crashes or patching code.
license: CC-BY-4.0
metadata:
  author: AEOS
  version: 1.0.0
  owner_agent: codenavi-agent
---

# mantis-review

Read and follow `00_skills/(security)/mantis-review/SKILL.md` and its relevant local modules.

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity.
```

### S170 | T1 | mantis-structural-index

- path: `.agents/skills/mantis-structural-index/SKILL.md`
- chars: 633
- outline:
- mantis-structural-index

```markdown
---
name: mantis-structural-index
description: Builds a content-addressed semantic-unit index from source code for structural context. Use when a pinned or live codebase is available and structural cross-reference data would improve research quality. Don't use for findings analysis, patching, or reporting.
license: CC-BY-4.0
metadata:
  author: AEOS
  version: 1.0.0
  owner_agent: codenavi-agent
---

# mantis-structural-index

Read and follow `00_skills/(security)/mantis-structural-index/SKILL.md` and its relevant local modules.

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity.
```

### S171 | T1 | mantis-summarize

- path: `.agents/skills/mantis-summarize/SKILL.md`
- chars: 677
- outline:
- mantis-summarize

```markdown
---
name: mantis-summarize
description: Pre-processes the repository by generating security-focused summaries (mantis-summary.md) for each directory to make planning and research more efficient. Use when starting a review campaign to map the codebase before threat modeling and planning. Don't use for executing code reviews, writing test scripts, or patching code.
license: CC-BY-4.0
metadata:
  author: AEOS
  version: 1.0.0
  owner_agent: codenavi-agent
---

# mantis-summarize

Read and follow `00_skills/(security)/mantis-summarize/SKILL.md` and its relevant local modules.

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity.
```

### S172 | T1 | mantis-threat-model

- path: `.agents/skills/mantis-threat-model/SKILL.md`
- chars: 732
- outline:
- mantis-threat-model

```markdown
---
name: mantis-threat-model
description: Synthesizes trust boundaries, attack surfaces, and attacker profiles into a living threat model. Use as Stage B of the Knowledge Base generation process, reading architecture and entity definitions from the KB. Don't use for analyzing source code or extracting raw learnings from JSONL files. Use when the user requests mantis threat model or invokes mantis-threat-model.
license: CC-BY-4.0
metadata:
  author: AEOS
  version: 1.0.0
  owner_agent: codenavi-agent
---

# mantis-threat-model

Read and follow `00_skills/(security)/mantis-threat-model/SKILL.md` and its relevant local modules.

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity.
```

### S173 | T1 | marketplace-curator

- path: `.agents/skills/marketplace-curator/SKILL.md`
- chars: 617
- outline:
- marketplace-curator

```markdown
---
name: marketplace-curator
description: Curate reusable capability listings by verified provenance, licensing, scope, compatibility and resource completeness. Use when the user requests marketplace curator or invokes marketplace-curator. Do NOT use for unrelated tools or unapproved remote writes.
license: CC-BY-4.0
metadata:
  author: AEOS
  version: 1.0.0
  owner_agent: codenavi-agent
---

# marketplace-curator

Read and follow `00_skills/(tooling)/marketplace-curator/SKILL.md` and its relevant local modules.

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity.
```

### S174 | T1 | mcp-discovery

- path: `.agents/skills/mcp-discovery/SKILL.md`
- chars: 540
- outline:
- mcp-discovery

```markdown
---
name: mcp-discovery
description: Discover and validate MCP tools and capabilities against AEOS policies. Use when the user requests mcp discovery or invokes mcp-discovery. Do NOT use for unrelated tools or unapproved remote writes.
license: CC-BY-4.0
metadata:
  author: AEOS
  version: 1.0.0
  owner_agent: codenavi-agent
---

# mcp-discovery

Read and follow `00_skills/(tooling)/mcp-discovery/SKILL.md` and its relevant local modules.

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity.
```

### S175 | T1 | mcp-health-check

- path: `.agents/skills/mcp-health-check/SKILL.md`
- chars: 561
- outline:
- mcp-health-check

```markdown
---
name: mcp-health-check
description: Validate MCP runtime health, state, tools, capabilities and security posture. Use when the user requests mcp health check or invokes mcp-health-check. Do NOT use for unrelated tools or unapproved remote writes.
license: CC-BY-4.0
metadata:
  author: AEOS
  version: 1.0.0
  owner_agent: codenavi-agent
---

# mcp-health-check

Read and follow `00_skills/(tooling)/mcp-health-check/SKILL.md` and its relevant local modules.

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity.
```

### S176 | T1 | mcp-poisoning-evaluator

- path: `.agents/skills/mcp-poisoning-evaluator/SKILL.md`
- chars: 664
- outline:
- mcp-poisoning-evaluator

```markdown
---
name: mcp-poisoning-evaluator
description: Evaluate MCP descriptions and responses for instruction injection, tool poisoning and authority escalation within defensive scope. Use when the user requests mcp poisoning evaluator or invokes mcp-poisoning-evaluator. Do NOT use outside authorized defensive scope or to expose secret values.
license: CC-BY-4.0
metadata:
  author: AEOS
  version: 1.0.0
  owner_agent: codenavi-agent
---

# mcp-poisoning-evaluator

Read and follow `00_skills/(security)/mcp-poisoning-evaluator/SKILL.md` and its relevant local modules.

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity.
```

### S177 | T1 | mcp-risk-controller

- path: `.agents/skills/mcp-risk-controller/SKILL.md`
- chars: 563
- outline:
- mcp-risk-controller

```markdown
---
name: mcp-risk-controller
description: Audit MCPs, tool descriptions, capabilities and poisoning risks. Use when the user requests mcp risk controller or invokes mcp-risk-controller. Do NOT use for unrelated tools or unapproved remote writes.
license: CC-BY-4.0
metadata:
  author: AEOS
  version: 1.0.0
  owner_agent: codenavi-agent
---

# mcp-risk-controller

Read and follow `00_skills/(tooling)/mcp-risk-controller/SKILL.md` and its relevant local modules.

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity.
```

### S178 | T1 | memory-curator

- path: `.agents/skills/memory-curator/SKILL.md`
- chars: 573
- outline:
- memory-curator

```markdown
---
name: memory-curator
description: Curate durable, evidence-backed project memory in `.notebook/MEMORY.md`. Use when the user requests memory curator or invokes memory-curator. Do NOT use to promote unverified claims or transient task status into durable memory.
license: CC-BY-4.0
metadata:
  author: AEOS
  version: 1.0.0
  owner_agent: codenavi-agent
---

# memory-curator

Read and follow `00_skills/(learning)/memory-curator/SKILL.md` and its relevant local modules.

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity.
```

### S179 | T1 | memory-governance-auditor

- path: `.agents/skills/memory-governance-auditor/SKILL.md`
- chars: 620
- outline:
- memory-governance-auditor

```markdown
---
name: memory-governance-auditor
description: Audit memory reads/writes for evidence, scope and secret safety. Use when the user requests memory governance auditor or invokes memory-governance-auditor. Do NOT use to promote unverified claims or transient task status into durable memory.
license: CC-BY-4.0
metadata:
  author: AEOS
  version: 1.0.0
  owner_agent: codenavi-agent
---

# memory-governance-auditor

Read and follow `00_skills/(learning)/memory-governance-auditor/SKILL.md` and its relevant local modules.

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity.
```

### S180 | T1 | mermaid-studio

- path: `.agents/skills/mermaid-studio/SKILL.md`
- chars: 1198
- outline:
- mermaid-studio

```markdown
---
name: mermaid-studio
description: Expert Mermaid diagram creation, validation, and rendering with dual-engine output (SVG/PNG/ASCII). Supports all 20+ diagram types including C4 architecture, AWS architecture-beta with service icons, flowcharts, sequence, ERD, state, class, mindmap, timeline, git graph, sankey, and more. Features code-to-diagram analysis, batch rendering, 15+ themes, and syntax validation. Use when users ask to create diagrams, visualize architecture, render mermaid files, generate ASCII diagrams, document system flows, model databases, draw AWS infrastructure, analyze code structure, or anything involving "mermaid", "diagram", "flowchart", "architecture diagram", "sequence diagram", "ERD", "C4", "ASCII diagram". Do NOT use for non-Mermaid image generation, data plotting with chart libraries, or general documentation writing.
license: CC-BY-4.0
metadata:
  author: Felipe Rodrigues - github.com/felipfr
  version: 1.0.1
  owner_agent: codenavi-agent
---

# mermaid-studio

Read and follow `00_skills/(tooling)/mermaid-studio/SKILL.md` and its relevant local modules.

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity.
```

### S181 | T1 | modular-decomposition

- path: `.agents/skills/modular-decomposition/SKILL.md`
- chars: 1253
- outline:
- modular-decomposition

```markdown
---
name: modular-decomposition
description: Runs a sequenced monolith-to-modular pipeline that sizes and inventories components, finds shared domain duplication, addresses flattening and hierarchy issues, analyzes coupling, then groups components into candidate domain-aligned units, with optional embedded DDD strategic analysis for bounded contexts. Use when asking how to split a monolith, size components before extraction, find duplicated domain logic, clean up module hierarchy, measure coupling between modules, or group components into services. Do NOT use for phased extraction roadmaps or prioritization without the prior analysis steps (use decomposition-planning-roadmap after this pipeline), end-to-end legacy migration strategy writeups (use legacy-migration-planner), pure infrastructure capacity sizing, or when you only need DDD without the structural pipeline (install domain-analysis standalone).
license: CC-BY-4.0
metadata:
  author: Tech Leads Club
  version: 1.0.0
  owner_agent: codenavi-agent
---

# modular-decomposition

Read and follow `00_skills/(architecture)/modular-decomposition/SKILL.md` and its relevant local modules.

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity.
```

### S182 | T1 | modular-design-principles

- path: `.agents/skills/modular-design-principles/SKILL.md`
- chars: 1269
- outline:
- modular-design-principles

```markdown
---
name: modular-design-principles
description: 'Technology-agnostic guidance for modular systems: bounded contexts, clear boundaries, composability, state isolation, explicit contracts, failure containment, scaffolding workflows, split/merge criteria, sub-units inside a context, and compliance review signals. Use when designing or reviewing module structure, service boundaries, package layout, cross-cutting dependencies, "how should we split this?", modularity assessments, coupling between domains, greenfield context design, or architecture discussions without assuming a specific framework, language, or repository layout. Do NOT use for executing the full Patterns 1–5 repo decomposition pipeline or per-pattern inventories (use modular-decomposition), phased extraction roadmaps as the main deliverable (use decomposition-planning-roadmap), or end-to-end legacy migration strategy (use legacy-migration-planner).'
license: CC-BY-4.0
metadata:
  author: Tech Leads Club
  version: 1.0.0
  owner_agent: codenavi-agent
---

# modular-design-principles

Read and follow `00_skills/(architecture)/modular-design-principles/SKILL.md` and its relevant local modules.

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity.
```

### S183 | T1 | multi-platform-launch

- path: `.agents/skills/multi-platform-launch/SKILL.md`
- chars: 1069
- outline:
- multi-platform-launch

```markdown
---
name: multi-platform-launch
description: When the user wants to launch a product across multiple platforms, plan a Product Hunt launch, build a waitlist, or execute a multi-channel launch strategy. Also use when the user mentions 'product launch,' 'Product Hunt,' 'launch strategy,' 'waitlist,' 'beta launch,' 'BetaList,' 'Hacker News,' 'launch day,' 'AppSumo,' 'multi-channel launch.' This skill covers multi-platform launch execution from pre-launch through post-launch optimization. Do NOT use for technical implementation, code review, or software architecture.
license: CC-BY-4.0
metadata:
  author: Chad Boyda / agent-gtm-skills
  version: 1.0.0
  original_author: Chad Boyda / agent-gtm-skills
  modified_by: Felipe Rodrigues - github.com/felipfr
  source: https://github.com/chadboyda/agent-gtm-skills
  owner_agent: codenavi-agent
---

# multi-platform-launch

Read and follow `00_skills/(gtm)/multi-platform-launch/SKILL.md` and its relevant local modules.

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity.
```

### S184 | T1 | multirepo-ecosystem-mapper

- path: `.agents/skills/multirepo-ecosystem-mapper/SKILL.md`
- chars: 619
- outline:
- multirepo-ecosystem-mapper

```markdown
---
name: multirepo-ecosystem-mapper
description: Map multi-repo ecosystems, dependencies and ownership boundaries. Use when the user requests multirepo ecosystem mapper or invokes multirepo-ecosystem-mapper. Do NOT use to mutate production or invent architecture without source evidence.
license: CC-BY-4.0
metadata:
  author: AEOS
  version: 1.0.0
  owner_agent: codenavi-agent
---

# multirepo-ecosystem-mapper

Read and follow `00_skills/(mapping)/multirepo-ecosystem-mapper/SKILL.md` and its relevant local modules.

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity.
```

### S185 | T1 | nestjs-modular-monolith

- path: `.agents/skills/nestjs-modular-monolith/SKILL.md`
- chars: 1056
- outline:
- nestjs-modular-monolith

```markdown
---
name: nestjs-modular-monolith
description: Specialist in designing and implementing scalable modular monolith architectures using NestJS with DDD, Clean Architecture, and CQRS patterns. Use when building modular monolith backends, designing bounded contexts, creating domain modules, implementing event-driven module communication, or when user mentions "modular monolith", "bounded contexts", "module boundaries", "DDD", "CQRS", "clean architecture NestJS", or "monolith to microservices". Do NOT use for simple CRUD APIs, frontend work, general NestJS questions without architectural context, or stack-agnostic evolutionary modular monolith design (use evolutionary-modular-architecture).
license: CC-BY-4.0
metadata:
  author: Felipe Rodrigues - github.com/felipfr
  version: 1.0.0
  owner_agent: codenavi-agent
---

# nestjs-modular-monolith

Read and follow `00_skills/(development)/nestjs-modular-monolith/SKILL.md` and its relevant local modules.

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity.
```

### S186 | T1 | netlify-deploy

- path: `.agents/skills/netlify-deploy/SKILL.md`
- chars: 644
- outline:
- netlify-deploy

```markdown
---
name: netlify-deploy
description: Deploy web projects to Netlify using the Netlify CLI (`npx netlify`). Use when the user asks to deploy, host, publish, or link a site/repo on Netlify, including preview and production deploys. Do NOT use for deploying to Vercel, Cloudflare, or Render (use their respective skills).
license: CC-BY-4.0
metadata:
  author: github.com/openai/skills
  version: 1.0.0
  owner_agent: codenavi-agent
---

# netlify-deploy

Read and follow `00_skills/(cloud)/netlify-deploy/SKILL.md` and its relevant local modules.

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity.
```

### S187 | T1 | not-your-babysitter

- path: `.agents/skills/not-your-babysitter/SKILL.md`
- chars: 733
- outline:
- not-your-babysitter

```markdown
---
name: not-your-babysitter
description: 'Assimilated TLC autonomous operator mode (not-your-babysitter 1.0.0). Drive a task to a verified result with evidence-or-stop, three interrupt reasons only, and short literal output. Triggers: not-your-babysitter, nanny mode, work autonomously, stop babysitting, no hand-holding. Do not use for tutorials, verbose walkthroughs, or open-ended brainstorming.'
license: CC-BY-4.0
metadata:
  author: Tech Leads Club
  version: 1.0.0
  owner_agent: codenavi-agent
---

# not-your-babysitter

Read and follow `00_skills/(development)/not-your-babysitter/SKILL.md` and its relevant local modules.

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity.
```

### S188 | T1 | notebook-intelligence

- path: `.agents/skills/notebook-intelligence/SKILL.md`
- chars: 626
- outline:
- notebook-intelligence

```markdown
---
name: notebook-intelligence
description: Maintain compact, fresh project intelligence in `.notebook/` using progressive disclosure. Use when the user requests notebook intelligence or invokes notebook-intelligence. Do NOT use to promote unverified claims or transient task status into durable memory.
license: CC-BY-4.0
metadata:
  author: AEOS
  version: 1.0.0
  owner_agent: codenavi-agent
---

# notebook-intelligence

Read and follow `00_skills/(learning)/notebook-intelligence/SKILL.md` and its relevant local modules.

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity.
```

### S189 | T1 | nx-ci-monitor

- path: `.agents/skills/nx-ci-monitor/SKILL.md`
- chars: 668
- outline:
- nx-ci-monitor

```markdown
---
name: nx-ci-monitor
description: Monitor Nx Cloud CI pipeline status and handle self-healing fixes automatically. Use when user says "watch CI", "monitor pipeline", "check CI status", "fix CI failures", or "self-heal CI". Requires Nx Cloud connection. Do NOT use for local task execution (use nx-run-tasks) or general CI debugging outside Nx Cloud.
license: CC-BY-4.0
metadata:
  author: Tech Leads Club
  version: 1.0.0
  owner_agent: codenavi-agent
---

# nx-ci-monitor

Read and follow `00_skills/(tooling)/nx-ci-monitor/SKILL.md` and its relevant local modules.

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity.
```

### S190 | T1 | nx-generate

- path: `.agents/skills/nx-generate/SKILL.md`
- chars: 858
- outline:
- nx-generate

```markdown
---
name: nx-generate
description: Generate code using Nx generators — scaffold projects, libraries, features, or run workspace-specific generators with proper discovery, validation, and verification. Use when user says "create a new library", "scaffold a component", "generate code with Nx", "run a generator", "nx generate", or any code scaffolding task in a monorepo. Prefers local workspace-plugin generators over external plugins. Do NOT use for running build/test/lint tasks (use nx-run-tasks) or workspace configuration (use nx-workspace).
license: CC-BY-4.0
metadata:
  author: Tech Leads Club
  version: 1.0.0
  owner_agent: codenavi-agent
---

# nx-generate

Read and follow `00_skills/(tooling)/nx-generate/SKILL.md` and its relevant local modules.

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity.
```

### S191 | T1 | nx-run-tasks

- path: `.agents/skills/nx-run-tasks/SKILL.md`
- chars: 687
- outline:
- nx-run-tasks

```markdown
---
name: nx-run-tasks
description: Execute build, test, lint, serve, and other tasks in an Nx workspace using single runs, run-many, and affected commands. Use when user says "run tests", "build my app", "lint affected", "serve the project", "run all tasks", or "nx affected". Do NOT use for code generation (use nx-generate) or workspace configuration (use nx-workspace).
license: CC-BY-4.0
metadata:
  author: Tech Leads Club
  version: 1.0.0
  owner_agent: codenavi-agent
---

# nx-run-tasks

Read and follow `00_skills/(tooling)/nx-run-tasks/SKILL.md` and its relevant local modules.

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity.
```

### S192 | T1 | nx-workspace

- path: `.agents/skills/nx-workspace/SKILL.md`
- chars: 652
- outline:
- nx-workspace

```markdown
---
name: nx-workspace
description: 'Assimilated TLC Nx workspace skill. Configure, explore and optimize Nx monorepos: project boundaries, affected analysis, caching and CI with affected commands. Triggers: nx, monorepo, workspace, projects, targets, affected. Do not use as the primary skill only to run a task or only to generate code.'
license: CC-BY-4.0
metadata:
  author: Tech Leads Club
  version: 1.0.0
  owner_agent: codenavi-agent
---

# nx-workspace

Read and follow `00_skills/(tooling)/nx-workspace/SKILL.md` and its relevant local modules.

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity.
```

### S193 | T1 | observability-architect

- path: `.agents/skills/observability-architect/SKILL.md`
- chars: 607
- outline:
- observability-architect

```markdown
---
name: observability-architect
description: Design logs, traces, metrics, dashboards and alerting. Use when the user requests observability architect or invokes observability-architect. Do NOT use to restart, scale or mutate live systems without an authorized operations task.
license: CC-BY-4.0
metadata:
  author: AEOS
  version: 1.0.0
  owner_agent: codenavi-agent
---

# observability-architect

Read and follow `00_skills/(monitoring)/observability-architect/SKILL.md` and its relevant local modules.

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity.
```

### S194 | T1 | observability-reporter

- path: `.agents/skills/observability-reporter/SKILL.md`
- chars: 623
- outline:
- observability-reporter

```markdown
---
name: observability-reporter
description: Generate execution timeline, metrics, trace summaries and failure analysis. Use when the user requests observability reporter or invokes observability-reporter. Do NOT use to restart, scale or mutate live systems without an authorized operations task.
license: CC-BY-4.0
metadata:
  author: AEOS
  version: 1.0.0
  owner_agent: codenavi-agent
---

# observability-reporter

Read and follow `00_skills/(monitoring)/observability-reporter/SKILL.md` and its relevant local modules.

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity.
```

### S195 | T1 | observability-root-cause-integrator

- path: `.agents/skills/observability-root-cause-integrator/SKILL.md`
- chars: 799
- outline:
- observability-root-cause-integrator

```markdown
---
name: observability-root-cause-integrator
description: Staff-level independent root-cause integrator that consolidates evidence from isolated observability tool analyses and repository code context into a simple, low-impact remediation plan. Use when the user requests observability root cause integrator or invokes observability-root-cause-integrator. Do NOT use to restart, scale or mutate live systems without an authorized operations task.
license: CC-BY-4.0
metadata:
  author: AEOS
  version: 1.0.0
  owner_agent: codenavi-agent
---

# observability-root-cause-integrator

Read and follow `00_skills/(monitoring)/observability-root-cause-integrator/SKILL.md` and its relevant local modules.

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity.
```

### S196 | T1 | openshift-observability-staff

- path: `.agents/skills/openshift-observability-staff/SKILL.md`
- chars: 782
- outline:
- openshift-observability-staff

```markdown
---
name: openshift-observability-staff
description: Deep Staff-level OpenShift observability analysis for platform monitoring, user workload monitoring, alerts, logging, operators, routes, builds, cluster health and supported configuration boundaries. Use when the user requests openshift observability staff or invokes openshift-observability-staff. Do NOT use to restart, scale or mutate live systems without an authorized operations task.
license: CC-BY-4.0
metadata:
  author: AEOS
  version: 1.0.0
  owner_agent: codenavi-agent
---

# openshift-observability-staff

Read and follow `00_skills/(monitoring)/openshift-observability-staff/SKILL.md` and its relevant local modules.

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity.
```

### S197 | T1 | pack-marketplace-auditor

- path: `.agents/skills/pack-marketplace-auditor/SKILL.md`
- chars: 604
- outline:
- pack-marketplace-auditor

```markdown
---
name: pack-marketplace-auditor
description: Audit local pack marketplace quarantine, staging, active packs and trust policy. Use when the user requests pack marketplace auditor or invokes pack-marketplace-auditor. Do NOT use for unrelated tools or unapproved remote writes.
license: CC-BY-4.0
metadata:
  author: AEOS
  version: 1.0.0
  owner_agent: codenavi-agent
---

# pack-marketplace-auditor

Read and follow `00_skills/(tooling)/pack-marketplace-auditor/SKILL.md` and its relevant local modules.

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity.
```

### S198 | T1 | package-trust-engineer

- path: `.agents/skills/package-trust-engineer/SKILL.md`
- chars: 582
- outline:
- package-trust-engineer

```markdown
---
name: package-trust-engineer
description: Verify packages, manifests, quarantine and promotion. Use when the user requests package trust engineer or invokes package-trust-engineer. Do NOT use outside authorized defensive scope or to expose secret values.
license: CC-BY-4.0
metadata:
  author: AEOS
  version: 1.0.0
  owner_agent: codenavi-agent
---

# package-trust-engineer

Read and follow `00_skills/(security)/package-trust-engineer/SKILL.md` and its relevant local modules.

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity.
```

### S199 | T1 | packaging

- path: `.agents/skills/packaging/SKILL.md`
- chars: 520
- outline:
- packaging

```markdown
---
name: packaging
description: Create, inspect, and verify AEOS packages with manifests and checksums. Use when the user requests packaging or invokes packaging. Do NOT use for unrelated tools or unapproved remote writes.
license: CC-BY-4.0
metadata:
  author: AEOS
  version: 1.0.0
  owner_agent: codenavi-agent
---

# packaging

Read and follow `00_skills/(tooling)/packaging/SKILL.md` and its relevant local modules.

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity.
```

### S200 | T1 | paid-creative-ai

- path: `.agents/skills/paid-creative-ai/SKILL.md`
- chars: 1066
- outline:
- paid-creative-ai

```markdown
---
name: paid-creative-ai
description: When the user wants to create AI-generated ad creative, test performance creative, manage creative fatigue, or optimize paid media with AI tools. Also use when the user mentions 'ad creative,' 'performance creative,' 'creative testing,' 'creative fatigue,' 'Meta ads,' 'Google ads,' 'TikTok ads,' 'AI ads,' 'ad budget,' 'ROAS,' 'Advantage+,' or 'Performance Max.' This skill covers AI-powered paid creative from generation through performance optimization. Do NOT use for technical implementation, code review, or software architecture.
license: CC-BY-4.0
metadata:
  author: Chad Boyda / agent-gtm-skills
  version: 1.0.0
  original_author: Chad Boyda / agent-gtm-skills
  modified_by: Felipe Rodrigues - github.com/felipfr
  source: https://github.com/chadboyda/agent-gtm-skills
  owner_agent: codenavi-agent
---

# paid-creative-ai

Read and follow `00_skills/(gtm)/paid-creative-ai/SKILL.md` and its relevant local modules.

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity.
```

### S201 | T1 | parallel-scheduler

- path: `.agents/skills/parallel-scheduler/SKILL.md`
- chars: 592
- outline:
- parallel-scheduler

```markdown
---
name: parallel-scheduler
description: Create deterministic safe schedules for playbook tasks using dependency graph and read/write sets. Use when the user requests parallel scheduler or invokes parallel-scheduler. Do NOT use for unrelated tools or unapproved remote writes.
license: CC-BY-4.0
metadata:
  author: AEOS
  version: 1.0.0
  owner_agent: codenavi-agent
---

# parallel-scheduler

Read and follow `00_skills/(tooling)/parallel-scheduler/SKILL.md` and its relevant local modules.

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity.
```

### S202 | T1 | partner-affiliate

- path: `.agents/skills/partner-affiliate/SKILL.md`
- chars: 1062
- outline:
- partner-affiliate

```markdown
---
name: partner-affiliate
description: When the user wants to build a partner program, launch an affiliate program, design integration partnerships, or create distribution partnerships. Also use when the user mentions 'partnerships,' 'affiliate program,' 'referral program,' 'partner ecosystem,' 'integration partner,' 'reseller,' 'co-marketing,' 'PartnerStack,' or 'revenue share.' This skill covers partner and affiliate program design from recruitment through performance optimization. Do NOT use for technical implementation, code review, or software architecture.
license: CC-BY-4.0
metadata:
  author: Chad Boyda / agent-gtm-skills
  version: 1.0.0
  original_author: Chad Boyda / agent-gtm-skills
  modified_by: Felipe Rodrigues - github.com/felipfr
  source: https://github.com/chadboyda/agent-gtm-skills
  owner_agent: codenavi-agent
---

# partner-affiliate

Read and follow `00_skills/(gtm)/partner-affiliate/SKILL.md` and its relevant local modules.

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity.
```

### S203 | T1 | patch-planner

- path: `.agents/skills/patch-planner/SKILL.md`
- chars: 549
- outline:
- patch-planner

```markdown
---
name: patch-planner
description: Generate patch proposals and rollback plans without applying them. Use when the user requests patch planner or invokes patch-planner. Do NOT use for unrelated languages, domains or production deployment.
license: CC-BY-4.0
metadata:
  author: AEOS
  version: 1.0.0
  owner_agent: codenavi-agent
---

# patch-planner

Read and follow `00_skills/(development)/patch-planner/SKILL.md` and its relevant local modules.

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity.
```

### S204 | T1 | perf-astro

- path: `.agents/skills/perf-astro/SKILL.md`
- chars: 624
- outline:
- perf-astro

```markdown
---
name: perf-astro
description: 'Assimilated TLC Astro performance skill. Optimize Astro sites for Lighthouse: critical CSS, compression, fonts, LCP. Triggers: Astro performance, Astro Lighthouse, astro-critters, optimize Astro. Do not use for non-Astro sites or as the only skill to run a Lighthouse audit.'
license: CC-BY-4.0
metadata:
  author: Tech Leads Club
  version: 1.0.0
  owner_agent: codenavi-agent
---

# perf-astro

Read and follow `00_skills/(performance)/perf-astro/SKILL.md` and its relevant local modules.

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity.
```

### S205 | T1 | perf-lighthouse

- path: `.agents/skills/perf-lighthouse/SKILL.md`
- chars: 698
- outline:
- perf-lighthouse

```markdown
---
name: perf-lighthouse
description: 'Assimilated TLC Lighthouse audit skill. Run Lighthouse via CLI or Node, parse reports, set performance budgets. Triggers: lighthouse, run lighthouse, lighthouse score, performance audit, performance budget. Do not use to implement CWV or generic speed fixes (core-web-vitals, perf-web-optimization) or Astro-only config (perf-astro).'
license: CC-BY-4.0
metadata:
  author: Tech Leads Club
  version: 1.0.0
  owner_agent: codenavi-agent
---

# perf-lighthouse

Read and follow `00_skills/(performance)/perf-lighthouse/SKILL.md` and its relevant local modules.

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity.
```

### S206 | T1 | perf-web-optimization

- path: `.agents/skills/perf-web-optimization/SKILL.md`
- chars: 708
- outline:
- perf-web-optimization

```markdown
---
name: perf-web-optimization
description: 'Assimilated TLC web performance skill. Measure, then cut bundle size, images, caching, lazy loading and page speed. Triggers: web performance, bundle size, page speed, slow site, lazy loading. Do not use for CWV-only metric work (core-web-vitals), only running Lighthouse (perf-lighthouse), or Astro-only config (perf-astro).'
license: CC-BY-4.0
metadata:
  author: Tech Leads Club
  version: 1.0.0
  owner_agent: codenavi-agent
---

# perf-web-optimization

Read and follow `00_skills/(performance)/perf-web-optimization/SKILL.md` and its relevant local modules.

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity.
```

### S207 | T1 | performance-optimizer

- path: `.agents/skills/performance-optimizer/SKILL.md`
- chars: 704
- outline:
- performance-optimizer

```markdown
---
name: performance-optimizer
description: Measure, classify and improve AEOS hot paths across registry loading, skill execution, evidence writing, repository scanning, LSP indexing and TypeScript runtime execution. Use when the user requests performance optimizer or invokes performance-optimizer. Do NOT use for unrelated functionality or unmeasured speculative optimization.
license: CC-BY-4.0
metadata:
  author: AEOS
  version: 1.0.0
  owner_agent: codenavi-agent
---

# performance-optimizer

Read and follow `00_skills/(performance)/performance-optimizer/SKILL.md` and its relevant local modules.

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity.
```

### S208 | T1 | performance-profiler

- path: `.agents/skills/performance-profiler/SKILL.md`
- chars: 612
- outline:
- performance-profiler

```markdown
---
name: performance-profiler
description: Profile AEOS executions, repo scans, hashing, package verification and Judge runtime. Use when the user requests performance profiler or invokes performance-profiler. Do NOT use for unrelated functionality or unmeasured speculative optimization.
license: CC-BY-4.0
metadata:
  author: AEOS
  version: 1.0.0
  owner_agent: codenavi-agent
---

# performance-profiler

Read and follow `00_skills/(performance)/performance-profiler/SKILL.md` and its relevant local modules.

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity.
```

### S209 | T1 | playbook-factory-generator

- path: `.agents/skills/playbook-factory-generator/SKILL.md`
- chars: 649
- outline:
- playbook-factory-generator

```markdown
---
name: playbook-factory-generator
description: Generate a reviewable playbook with explicit step contracts, dependencies, resources and verification gates. Use when the user requests playbook factory generator or invokes playbook-factory-generator. Do NOT use for ordinary one-off coding or human competency lists.
license: CC-BY-4.0
metadata:
  author: AEOS
  version: 1.0.0
  owner_agent: codenavi-agent
---

# playbook-factory-generator

Read and follow `00_skills/(creation)/playbook-factory-generator/SKILL.md` and its relevant local modules.

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity.
```

### S210 | T1 | playbook-optimizer

- path: `.agents/skills/playbook-optimizer/SKILL.md`
- chars: 568
- outline:
- playbook-optimizer

```markdown
---
name: playbook-optimizer
description: Optimize playbooks for execution time, safety and evidence quality. Use when the user requests playbook optimizer or invokes playbook-optimizer. Do NOT use for ordinary one-off coding or human competency lists.
license: CC-BY-4.0
metadata:
  author: AEOS
  version: 1.0.0
  owner_agent: codenavi-agent
---

# playbook-optimizer

Read and follow `00_skills/(creation)/playbook-optimizer/SKILL.md` and its relevant local modules.

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity.
```

### S211 | T1 | playwright-skill

- path: `.agents/skills/playwright-skill/SKILL.md`
- chars: 836
- outline:
- playwright-skill

```markdown
---
name: playwright-skill
description: Complete browser automation with Playwright. Auto-detects dev servers, writes clean test scripts to /tmp. Test pages, fill forms, take screenshots, check responsive design, validate UX, test login flows, check links, automate any browser task. Use when user wants to test websites, automate browser interactions, validate web functionality, or perform any browser-based testing. Do NOT use for quick page debugging or network inspection (use chrome-devtools instead).
license: CC-BY-4.0
metadata:
  author: Tech Leads Club
  version: 1.0.0
  owner_agent: codenavi-agent
---

# playwright-skill

Read and follow `00_skills/(web-automation)/playwright-skill/SKILL.md` and its relevant local modules.

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity.
```

### S212 | T1 | policy-bypass-evaluator

- path: `.agents/skills/policy-bypass-evaluator/SKILL.md`
- chars: 655
- outline:
- policy-bypass-evaluator

```markdown
---
name: policy-bypass-evaluator
description: Evaluate whether explicit policy boundaries reject bypass scenarios without weakening permissions or acceptance criteria. Use when the user requests policy bypass evaluator or invokes policy-bypass-evaluator. Do NOT use outside authorized defensive scope or to expose secret values.
license: CC-BY-4.0
metadata:
  author: AEOS
  version: 1.0.0
  owner_agent: codenavi-agent
---

# policy-bypass-evaluator

Read and follow `00_skills/(security)/policy-bypass-evaluator/SKILL.md` and its relevant local modules.

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity.
```

### S213 | T1 | policy-hardening-auditor

- path: `.agents/skills/policy-hardening-auditor/SKILL.md`
- chars: 606
- outline:
- policy-hardening-auditor

```markdown
---
name: policy-hardening-auditor
description: Audit whether policies cover critical unsafe paths and fail closed. Use when the user requests policy hardening auditor or invokes policy-hardening-auditor. Do NOT use outside authorized defensive scope or to expose secret values.
license: CC-BY-4.0
metadata:
  author: AEOS
  version: 1.0.0
  owner_agent: codenavi-agent
---

# policy-hardening-auditor

Read and follow `00_skills/(security)/policy-hardening-auditor/SKILL.md` and its relevant local modules.

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity.
```

### S214 | T1 | positioning-icp

- path: `.agents/skills/positioning-icp/SKILL.md`
- chars: 1086
- outline:
- positioning-icp

```markdown
---
name: positioning-icp
description: When the user wants to define their ideal customer profile, position an AI product, build messaging architecture, or validate product-market fit. Also use when the user mentions 'ICP,' 'ideal customer profile,' 'positioning,' 'PMF,' 'product-market fit,' 'messaging,' 'buyer persona,' 'enrichment signals,' 'market positioning,' or 'competitive positioning.' This skill covers market positioning, ICP definition, messaging architecture, and PMF validation for AI-native products. Do NOT use for technical implementation, code review, or software architecture.
license: CC-BY-4.0
metadata:
  author: Chad Boyda / agent-gtm-skills
  version: 1.0.0
  original_author: Chad Boyda / agent-gtm-skills
  modified_by: Felipe Rodrigues - github.com/felipfr
  source: https://github.com/chadboyda/agent-gtm-skills
  owner_agent: codenavi-agent
---

# positioning-icp

Read and follow `00_skills/(gtm)/positioning-icp/SKILL.md` and its relevant local modules.

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity.
```

### S215 | T1 | pr-comment-resolver

- path: `.agents/skills/pr-comment-resolver/SKILL.md`
- chars: 608
- outline:
- pr-comment-resolver

```markdown
---
name: pr-comment-resolver
description: Resolve pull-request review comments systematically without blindly obeying incorrect feedback. Use when the user requests pr comment resolver or invokes pr-comment-resolver. Do NOT use for unrelated languages, domains or production deployment.
license: CC-BY-4.0
metadata:
  author: AEOS
  version: 1.0.0
  owner_agent: codenavi-agent
---

# pr-comment-resolver

Read and follow `00_skills/(development)/pr-comment-resolver/SKILL.md` and its relevant local modules.

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity.
```

### S216 | T1 | pr-reviewer

- path: `.agents/skills/pr-reviewer/SKILL.md`
- chars: 536
- outline:
- pr-reviewer

```markdown
---
name: pr-reviewer
description: Review pull requests as an independent evidence-based reviewer. Use when the user requests pr reviewer or invokes pr-reviewer. Do NOT use for unrelated languages, domains or production deployment.
license: CC-BY-4.0
metadata:
  author: AEOS
  version: 1.0.0
  owner_agent: codenavi-agent
---

# pr-reviewer

Read and follow `00_skills/(development)/pr-reviewer/SKILL.md` and its relevant local modules.

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity.
```

### S217 | T1 | pr-reviewer-advanced

- path: `.agents/skills/pr-reviewer-advanced/SKILL.md`
- chars: 569
- outline:
- pr-reviewer-advanced

```markdown
---
name: pr-reviewer-advanced
description: Perform severity-ranked, evidence-backed PR review. Use when the user requests pr reviewer advanced or invokes pr-reviewer-advanced. Do NOT use for unrelated languages, domains or production deployment.
license: CC-BY-4.0
metadata:
  author: AEOS
  version: 1.0.0
  owner_agent: codenavi-agent
---

# pr-reviewer-advanced

Read and follow `00_skills/(development)/pr-reviewer-advanced/SKILL.md` and its relevant local modules.

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity.
```

### S218 | T1 | production-deployment-planner

- path: `.agents/skills/production-deployment-planner/SKILL.md`
- chars: 684
- outline:
- production-deployment-planner

```markdown
---
name: production-deployment-planner
description: Plan production packaging, CI/CD, deployment, observability, rollback and operational readiness for any architecture. Use when the user requests production deployment planner or invokes production-deployment-planner. Do NOT use for unrelated application features or unapproved production changes.
license: CC-BY-4.0
metadata:
  author: AEOS
  version: 1.0.0
  owner_agent: codenavi-agent
---

# production-deployment-planner

Read and follow `00_skills/(cloud)/production-deployment-planner/SKILL.md` and its relevant local modules.

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity.
```

### S219 | T1 | progress-tracker

- path: `.agents/skills/progress-tracker/SKILL.md`
- chars: 609
- outline:
- progress-tracker

```markdown
---
name: progress-tracker
description: Keep `.notebook/PROGRESS.md` as the live, evidence-backed source of truth for the current mission. Use when the user requests progress tracker or invokes progress-tracker. Do NOT use to promote unverified claims or transient task status into durable memory.
license: CC-BY-4.0
metadata:
  author: AEOS
  version: 1.0.0
  owner_agent: codenavi-agent
---

# progress-tracker

Read and follow `00_skills/(learning)/progress-tracker/SKILL.md` and its relevant local modules.

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity.
```

### S220 | T1 | prompt-optimizer

- path: `.agents/skills/prompt-optimizer/SKILL.md`
- chars: 548
- outline:
- prompt-optimizer

```markdown
---
name: prompt-optimizer
description: Convert vague prompts into bounded, evidence-based task prompts. Use when the user requests prompt optimizer or invokes prompt-optimizer. Do NOT use for unrelated tools or unapproved remote writes.
license: CC-BY-4.0
metadata:
  author: AEOS
  version: 1.0.0
  owner_agent: codenavi-agent
---

# prompt-optimizer

Read and follow `00_skills/(tooling)/prompt-optimizer/SKILL.md` and its relevant local modules.

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity.
```

### S221 | T1 | python-ai-productionizer

- path: `.agents/skills/python-ai-productionizer/SKILL.md`
- chars: 593
- outline:
- python-ai-productionizer

```markdown
---
name: python-ai-productionizer
description: Analyze Python AI/RAG systems for production readiness. Use when the user requests python ai productionizer or invokes python-ai-productionizer. Do NOT use for unrelated languages, domains or production deployment.
license: CC-BY-4.0
metadata:
  author: AEOS
  version: 1.0.0
  owner_agent: codenavi-agent
---

# python-ai-productionizer

Read and follow `00_skills/(development)/python-ai-productionizer/SKILL.md` and its relevant local modules.

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity.
```

### S222 | T1 | python-bug-solver-skill

- path: `.agents/skills/python-bug-solver-skill/SKILL.md`
- chars: 678
- outline:
- python-bug-solver-skill

```markdown
---
name: python-bug-solver-skill
description: Create a Python Bug Solver skill that analyzes stack traces, searches for root causes, generates fixes, validates them and stores lessons learned Use when the user requests python bug solver skill or invokes python-bug-solver-skill. Do NOT use for unrelated languages, domains or production deployment.
license: CC-BY-4.0
metadata:
  author: AEOS
  version: 1.0.0
  owner_agent: codenavi-agent
---

# python-bug-solver-skill

Read and follow `00_skills/(development)/python-bug-solver-skill/SKILL.md` and its relevant local modules.

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity.
```

### S223 | T1 | python-expert

- path: `.agents/skills/python-expert/SKILL.md`
- chars: 787
- outline:
- python-expert

```markdown
---
name: python-expert
description: Implement, diagnose, test and modernize production Python projects with version-correct APIs and repository-native packaging, typing, async and framework conventions. Python is allowed in this workspace; AEOS kernel/runtime orchestration stays Node/TypeScript unless a later mission changes that surface. Use when the user requests python expert or invokes python-expert. Do NOT use for unrelated languages, domains or production deployment.
license: CC-BY-4.0
metadata:
  author: AEOS
  version: 1.0.0
  owner_agent: codenavi-agent
---

# python-expert

Read and follow `00_skills/(development)/python-expert/SKILL.md` and its relevant local modules.

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity.
```

### S224 | T1 | python-rag-audit

- path: `.agents/skills/python-rag-audit/SKILL.md`
- chars: 635
- outline:
- python-rag-audit

```markdown
---
name: python-rag-audit
description: Audit Python RAG (Retrieval-Augmented Generation) pipelines for security, data leakage, prompt injection risks, and production readiness. Use when the user requests python rag audit or invokes python-rag-audit. Do NOT use for unrelated languages, domains or production deployment.
license: CC-BY-4.0
metadata:
  author: AEOS
  version: 1.0.0
  owner_agent: codenavi-agent
---

# python-rag-audit

Read and follow `00_skills/(development)/python-rag-audit/SKILL.md` and its relevant local modules.

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity.
```

### S225 | T1 | rag-expert

- path: `.agents/skills/rag-expert/SKILL.md`
- chars: 561
- outline:
- rag-expert

```markdown
---
name: rag-expert
description: Implement or repair Retrieval-Augmented Generation systems with measurable grounding quality. Use when the user requests rag expert or invokes rag-expert. Do NOT use for unrelated languages, domains or production deployment.
license: CC-BY-4.0
metadata:
  author: AEOS
  version: 1.0.0
  owner_agent: codenavi-agent
---

# rag-expert

Read and follow `00_skills/(development)/rag-expert/SKILL.md` and its relevant local modules.

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity.
```

### S226 | T1 | rails-dev

- path: `.agents/skills/rails-dev/SKILL.md`
- chars: 1316
- outline:
- rails-dev

```markdown
---
name: rails-dev
description: 'Opinionated Rails conventions: rich models, concerns, CRUD-everything, state-as-records, minimal dependencies, Minitest with fixtures. Load this skill BEFORE any code-level thinking, not only before editing a file. It is required the moment a task touches Rails code in ANY way: designing or even just discussing a data model, schema, migration, entity, association, field, validation, class, or method name; writing, planning, reviewing, analyzing, testing, debugging, or refactoring; or proposing any model, table, column, route, or code snippet inline in chat. If you are about to name a model or sketch a column you are already in scope, even in an exploratory back-and-forth where no file is written yet. Do not let a "we''re just discussing" framing defer it. Do NOT use for non-Rails backends, NestJS, or general architecture (use nestjs-modular-monolith or coding-guidelines). Use when the user requests rails dev or invokes rails-dev.'
license: CC-BY-4.0
metadata:
  author: William Calderipe - github.com/wcalderipe
  version: 1.0.0
  owner_agent: codenavi-agent
---

# rails-dev

Read and follow `00_skills/(development)/rails-dev/SKILL.md` and its relevant local modules.

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity.
```

### S227 | T1 | react-best-practices

- path: `.agents/skills/react-best-practices/SKILL.md`
- chars: 774
- outline:
- react-best-practices

```markdown
---
name: react-best-practices
description: React and Next.js performance optimization guidelines from Vercel Engineering. Use when writing, reviewing, or refactoring React/Next.js code to ensure optimal performance patterns. Triggers on tasks involving React components, Next.js pages, data fetching, bundle optimization, or performance improvements. Do NOT use for component API architecture or composition patterns (use react-composition-patterns instead).
license: MIT
metadata:
  author: vercel
  version: 1.0.0
  owner_agent: codenavi-agent
---

# react-best-practices

Read and follow `00_skills/(quality)/react-best-practices/SKILL.md` and its relevant local modules.

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity.
```

### S228 | T1 | react-composition-patterns

- path: `.agents/skills/react-composition-patterns/SKILL.md`
- chars: 782
- outline:
- react-composition-patterns

```markdown
---
name: react-composition-patterns
description: React composition patterns that scale. Use when refactoring components with boolean prop proliferation, building flexible component libraries, or designing reusable APIs. Triggers on tasks involving compound components, render props, context providers, or component architecture. Includes React 19 API changes. Do NOT use for React/Next.js performance optimization (use react-best-practices instead).
license: MIT
metadata:
  author: vercel
  version: 1.0.0
  owner_agent: codenavi-agent
---

# react-composition-patterns

Read and follow `00_skills/(architecture)/react-composition-patterns/SKILL.md` and its relevant local modules.

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity.
```

### S229 | T1 | react-expert

- path: `.agents/skills/react-expert/SKILL.md`
- chars: 645
- outline:
- react-expert

```markdown
---
name: react-expert
description: Implement and refactor production React applications using the exact repository React/runtime/framework version and existing component/state/data-fetching conventions. Use when the user requests react expert or invokes react-expert. Do NOT use for unrelated languages, domains or production deployment.
license: CC-BY-4.0
metadata:
  author: AEOS
  version: 1.0.0
  owner_agent: codenavi-agent
---

# react-expert

Read and follow `00_skills/(development)/react-expert/SKILL.md` and its relevant local modules.

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity.
```

### S230 | T1 | react-native-expert

- path: `.agents/skills/react-native-expert/SKILL.md`
- chars: 1014
- outline:
- react-native-expert

```markdown
---
name: react-native-expert
description: Senior React Native and Expo engineer for building production-ready cross-platform mobile apps. Use when building React Native components, implementing navigation with Expo Router, optimizing list and scroll performance, working with animations via Reanimated, handling platform-specific code (iOS/Android), integrating native modules, or structuring Expo projects. Triggers on React Native, Expo, mobile app, iOS app, Android app, cross-platform, native module, FlatList, FlashList, LegendList, Reanimated, Expo Router, mobile performance, app store. Do NOT use for Flutter, web-only React, or backend Node.js tasks.
license: CC-BY-4.0
metadata:
  author: Felipe Rodrigues - github.com/felipfr
  version: 1.0.0
  owner_agent: codenavi-agent
---

# react-native-expert

Read and follow `00_skills/(development)/react-native-expert/SKILL.md` and its relevant local modules.

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity.
```

### S231 | T1 | redaction-evaluator

- path: `.agents/skills/redaction-evaluator/SKILL.md`
- chars: 631
- outline:
- redaction-evaluator

```markdown
---
name: redaction-evaluator
description: Evaluate redaction behavior across authorized outputs and identify sensitive-value leakage or excessive data removal. Use when the user requests redaction evaluator or invokes redaction-evaluator. Do NOT use outside authorized defensive scope or to expose secret values.
license: CC-BY-4.0
metadata:
  author: AEOS
  version: 1.0.0
  owner_agent: codenavi-agent
---

# redaction-evaluator

Read and follow `00_skills/(security)/redaction-evaluator/SKILL.md` and its relevant local modules.

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity.
```

### S232 | T1 | release-readiness-judge

- path: `.agents/skills/release-readiness-judge/SKILL.md`
- chars: 601
- outline:
- release-readiness-judge

```markdown
---
name: release-readiness-judge
description: Validate release readiness using deterministic gates. Use when the user requests release readiness judge or invokes release-readiness-judge. Do NOT use as deployment authorization or as evidence for checks that were not executed.
license: CC-BY-4.0
metadata:
  author: AEOS
  version: 1.0.0
  owner_agent: codenavi-agent
---

# release-readiness-judge

Read and follow `00_skills/(quality)/release-readiness-judge/SKILL.md` and its relevant local modules.

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity.
```

### S233 | T1 | render-deploy

- path: `.agents/skills/render-deploy/SKILL.md`
- chars: 679
- outline:
- render-deploy

```markdown
---
name: render-deploy
description: Deploy applications to Render by analyzing codebases, generating render.yaml Blueprints, and providing Dashboard deeplinks. Use when the user wants to deploy, host, publish, or set up their application on Render's cloud platform. Do NOT use for deploying to Vercel, Netlify, or Cloudflare (use their respective skills).
license: CC-BY-4.0
metadata:
  author: github.com/openai/skills
  version: 1.0.0
  owner_agent: codenavi-agent
---

# render-deploy

Read and follow `00_skills/(cloud)/render-deploy/SKILL.md` and its relevant local modules.

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity.
```

### S234 | T1 | repo-scanner

- path: `.agents/skills/repo-scanner/SKILL.md`
- chars: 540
- outline:
- repo-scanner

```markdown
---
name: repo-scanner
description: Analyze repositories and produce factual ecosystem maps. Use when the user requests repo scanner or invokes repo-scanner. Do NOT use to mutate production or invent architecture without source evidence.
license: CC-BY-4.0
metadata:
  author: AEOS
  version: 1.0.0
  owner_agent: codenavi-agent
---

# repo-scanner

Read and follow `00_skills/(mapping)/repo-scanner/SKILL.md` and its relevant local modules.

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity.
```

### S235 | T1 | report-design

- path: `.agents/skills/report-design/SKILL.md`
- chars: 732
- outline:
- report-design

```markdown
---
name: report-design
description: Apply the pictured offline report layout with semantic theme tokens, complete grids, tooltips, filters/export, drill-down and accessible diagrams. Use when the user says melhorar o relatório HTML, tabela sem filtro or relatório regrediu. Do NOT use for data collection (fleet-mapping), schema changes, skill evaluation, or meeting media (acta-aurea).
license: CC-BY-4.0
metadata:
  author: AEOS; photographic reference supplied by user
  version: 1.0.0
  owner_agent: codenavi-agent
---

# report-design

Read and follow `00_skills/(design)/report-design/SKILL.md` and its relevant local modules.

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity.
```

### S236 | T1 | resolver-comentarios

- path: `.agents/skills/resolver-comentarios/SKILL.md`
- chars: 627
- outline:
- resolver-comentarios

```markdown
---
name: resolver-comentarios
description: Resolve concrete pull-request review comments after inspecting the referenced code and verifying corrections. Use when the user requests resolver comentarios or invokes resolver-comentarios. Do NOT use for unrelated languages, domains or production deployment.
license: CC-BY-4.0
metadata:
  author: AEOS
  version: 1.0.0
  owner_agent: codenavi-agent
---

# resolver-comentarios

Read and follow `00_skills/(development)/resolver-comentarios/SKILL.md` and its relevant local modules.

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity.
```

### S237 | T1 | revisar-pr

- path: `.agents/skills/revisar-pr/SKILL.md`
- chars: 689
- outline:
- revisar-pr

```markdown
---
name: "revisar-pr"
description: "Review a concrete pull-request diff against its requirement, behavior, contracts and repository conventions; return evidence-ranked findings and a local verdict. Use for revisar PR, parecer do diff or code review. Do NOT use for deep security review (revisar-seguranca-pr), remediate unless requested, post a review or decide/execute merge."
license: "CC-BY-4.0"
metadata:
  author: "AEOS"
  version: "1.1.0"
  owner_agent: "codenavi-agent"
---

# revisar-pr

Read and follow `00_skills/(development)/revisar-pr/SKILL.md` and its relevant local modules.

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity.
```

### S238 | T1 | revisar-seguranca-pr

- path: `.agents/skills/revisar-seguranca-pr/SKILL.md`
- chars: 776
- outline:
- revisar-seguranca-pr

```markdown
---
name: revisar-seguranca-pr
description: Review a concrete pull-request diff for authorization, sensitive-data handling and security failures that scans need contextual evidence to assess. Use when the user says revisar segurança deste PR or avaliar este achado CodeQL/Fortify/Trivy. Do NOT use for general PR review (revisar-pr), fleet vulnerability inventory, or known dependency remediation (cve-remediation).
license: CC-BY-4.0
metadata:
  author: AEOS; photographic reference supplied by user
  version: 1.0.0
  owner_agent: codenavi-agent
---

# revisar-seguranca-pr

Read and follow `00_skills/(security)/revisar-seguranca-pr/SKILL.md` and its relevant local modules.

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity.
```

### S239 | T1 | risk-classifier

- path: `.agents/skills/risk-classifier/SKILL.md`
- chars: 623
- outline:
- risk-classifier

```markdown
---
name: risk-classifier
description: Classify the risk level of proposed changes — considering scope, impact, reversibility, test coverage, and security implications. Use when the user requests risk classifier or invokes risk-classifier. Do NOT use outside authorized defensive scope or to expose secret values.
license: CC-BY-4.0
metadata:
  author: AEOS
  version: 1.0.0
  owner_agent: codenavi-agent
---

# risk-classifier

Read and follow `00_skills/(security)/risk-classifier/SKILL.md` and its relevant local modules.

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity.
```

### S240 | T1 | rollback-planner

- path: `.agents/skills/rollback-planner/SKILL.md`
- chars: 601
- outline:
- rollback-planner

```markdown
---
name: rollback-planner
description: Generate rollback plans for proposed changes — defining exactly how to undo every operation safely. Use when the user requests rollback planner or invokes rollback-planner. Do NOT use for unrelated application features or unapproved production changes.
license: CC-BY-4.0
metadata:
  author: AEOS
  version: 1.0.0
  owner_agent: codenavi-agent
---

# rollback-planner

Read and follow `00_skills/(cloud)/rollback-planner/SKILL.md` and its relevant local modules.

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity.
```

### S241 | T1 | runtime-troubleshooting

- path: `.agents/skills/runtime-troubleshooting/SKILL.md`
- chars: 762
- outline:
- runtime-troubleshooting

```markdown
---
name: runtime-troubleshooting
description: Diagnose a running application from read-only logs, metrics, traces, events and repository code without changing the live system. Use when the user says erro em produção, aplicação não sobe or investigar falha em runtime. Do NOT use to restart/scale/deploy, redesign architecture, invent inaccessible broker state, or replace incident ownership.
license: CC-BY-4.0
metadata:
  author: AEOS; photographic reference supplied by user
  version: 1.0.0
  owner_agent: codenavi-agent
---

# runtime-troubleshooting

Read and follow `00_skills/(development)/runtime-troubleshooting/SKILL.md` and its relevant local modules.

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity.
```

### S242 | T1 | rust-expert

- path: `.agents/skills/rust-expert/SKILL.md`
- chars: 632
- outline:
- rust-expert

```markdown
---
name: rust-expert
description: Implement, diagnose, modernize and migrate real Rust projects with version-correct APIs, minimal diffs and evidence-backed verification. Use when the user requests rust expert or invokes rust-expert. Do NOT use for unrelated languages, domains or production deployment.
license: CC-BY-4.0
metadata:
  author: Tech Lead's Club / CodENavi
  version: 1.0.0
  owner_agent: codenavi-agent
---

# rust-expert

Read and follow `00_skills/(development)/rust-expert/SKILL.md` and its relevant local modules.

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity.
```

### S243 | T1 | sales-motion-design

- path: `.agents/skills/sales-motion-design/SKILL.md`
- chars: 1073
- outline:
- sales-motion-design

```markdown
---
name: sales-motion-design
description: When the user wants to choose between PLG and sales-led, design a sales motion, optimize time-to-first-value, or build a value-before-purchase experience. Also use when the user mentions 'PLG,' 'product-led growth,' 'sales-led,' 'sales motion,' 'free trial,' 'freemium,' 'self-serve,' 'demo-first,' 'time-to-first-value,' 'TTFV,' or 'agent-led sales.' This skill covers sales motion selection, value delivery design, and go-to-market motion architecture. Do NOT use for technical implementation, code review, or software architecture.
license: CC-BY-4.0
metadata:
  author: Chad Boyda / agent-gtm-skills
  version: 1.0.0
  original_author: Chad Boyda / agent-gtm-skills
  modified_by: Felipe Rodrigues - github.com/felipfr
  source: https://github.com/chadboyda/agent-gtm-skills
  owner_agent: codenavi-agent
---

# sales-motion-design

Read and follow `00_skills/(gtm)/sales-motion-design/SKILL.md` and its relevant local modules.

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity.
```

### S244 | T1 | secret-redaction-specialist

- path: `.agents/skills/secret-redaction-specialist/SKILL.md`
- chars: 615
- outline:
- secret-redaction-specialist

```markdown
---
name: secret-redaction-specialist
description: Detect and redact sensitive data without exposing raw values. Use when the user requests secret redaction specialist or invokes secret-redaction-specialist. Do NOT use outside authorized defensive scope or to expose secret values.
license: CC-BY-4.0
metadata:
  author: AEOS
  version: 1.0.0
  owner_agent: codenavi-agent
---

# secret-redaction-specialist

Read and follow `00_skills/(security)/secret-redaction-specialist/SKILL.md` and its relevant local modules.

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity.
```

### S245 | T1 | security-audit

- path: `.agents/skills/security-audit/SKILL.md`
- chars: 556
- outline:
- security-audit

```markdown
---
name: security-audit
description: Detect security risks and possible secrets without exposing values. Use when the user requests security audit or invokes security-audit. Do NOT use outside authorized defensive scope or to expose secret values.
license: CC-BY-4.0
metadata:
  author: AEOS
  version: 1.0.0
  owner_agent: codenavi-agent
---

# security-audit

Read and follow `00_skills/(security)/security-audit/SKILL.md` and its relevant local modules.

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity.
```

### S246 | T1 | security-best-practices

- path: `.agents/skills/security-best-practices/SKILL.md`
- chars: 802
- outline:
- security-best-practices

```markdown
---
name: "security-best-practices"
description: "Write and review secure-by-default code by inspected language/framework: Java, Spring Boot 2/3, Apache Camel, Angular, Python, JavaScript/TypeScript and Go. Use for boas práticas de segurança, código Spring seguro, segurança do componente Angular or a prioritized secure-coding report. Do NOT use for a specific deep PR diff (revisar-seguranca-pr), CVE/EOL recon, dependency remediation or threat modeling."
license: "CC-BY-4.0"
metadata:
  author: "Tech Leads Club"
  version: "1.1.0"
  owner_agent: "codenavi-agent"
---

# security-best-practices

Read and follow `00_skills/(security)/security-best-practices/SKILL.md` and its relevant local modules.

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity.
```

### S247 | T1 | security-ownership-map

- path: `.agents/skills/security-ownership-map/SKILL.md`
- chars: 697
- outline:
- security-ownership-map

```markdown
---
name: security-ownership-map
description: 'Assimilated OpenAI/TLC git ownership topology skill. Build people-to-file maps, bus factor and sensitive-code ownership from git history. Triggers: security ownership, bus factor, orphaned sensitive code, CODEOWNERS reality check. Do not use for general maintainer lists or threat modeling (security-threat-model).'
license: CC-BY-4.0
metadata:
  author: Tech Leads Club
  version: 1.0.0
  owner_agent: codenavi-agent
---

# security-ownership-map

Read and follow `00_skills/(security)/security-ownership-map/SKILL.md` and its relevant local modules.

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity.
```

### S248 | T1 | security-threat-model

- path: `.agents/skills/security-threat-model/SKILL.md`
- chars: 684
- outline:
- security-threat-model

```markdown
---
name: security-threat-model
description: 'Assimilated OpenAI/TLC repo-grounded threat model. Enumerate trust boundaries, assets, attacker capabilities, abuse paths and mitigations into Markdown. Triggers: threat model, abuse paths, AppSec threat modeling. Do not use for architecture summaries, security-best-practices reviews, or ownership maps.'
license: CC-BY-4.0
metadata:
  author: Tech Leads Club
  version: 1.0.0
  owner_agent: codenavi-agent
---

# security-threat-model

Read and follow `00_skills/(security)/security-threat-model/SKILL.md` and its relevant local modules.

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity.
```

### S249 | T1 | sentry

- path: `.agents/skills/sentry/SKILL.md`
- chars: 706
- outline:
- sentry

```markdown
---
name: sentry
description: Inspect Sentry issues, summarize production errors, and pull health data via the Sentry API (read-only). Use when user says "check Sentry", "what errors in production?", "summarize Sentry issues", "recent crashes", or "production error report". Requires SENTRY_AUTH_TOKEN. Do NOT use for setting up Sentry SDK, configuring alerts, or non-Sentry error monitoring.
license: CC-BY-4.0
metadata:
  author: github.com/openai/skills
  version: 1.0.0
  owner_agent: codenavi-agent
---

# sentry

Read and follow `00_skills/(monitoring)/sentry/SKILL.md` and its relevant local modules.

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity.
```

### S250 | T1 | seo

- path: `.agents/skills/seo/SKILL.md`
- chars: 690
- outline:
- seo

```markdown
---
name: seo
description: Optimize for search engine visibility and ranking. Use when asked to "improve SEO", "optimize for search", "fix meta tags", "add structured data", "sitemap optimization", or "search engine optimization". Do NOT use for accessibility (use web-accessibility), performance (use core-web-vitals), or comprehensive site audits covering multiple areas (use web-quality-audit).
license: MIT
metadata:
  author: web-quality-skills
  version: 1.0.0
  owner_agent: codenavi-agent
---

# seo

Read and follow `00_skills/(quality)/seo/SKILL.md` and its relevant local modules.

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity.
```

### S251 | T1 | servicenow-incident-assistant

- path: `.agents/skills/servicenow-incident-assistant/SKILL.md`
- chars: 673
- outline:
- servicenow-incident-assistant

```markdown
---
name: servicenow-incident-assistant
description: Convert incident evidence into ServiceNow-ready triage, updates, RCA and closure material. Use when the user requests servicenow incident assistant or invokes servicenow-incident-assistant. Do NOT use to restart, scale or mutate live systems without an authorized operations task.
license: CC-BY-4.0
metadata:
  author: AEOS
  version: 1.0.0
  owner_agent: codenavi-agent
---

# servicenow-incident-assistant

Read and follow `00_skills/(monitoring)/servicenow-incident-assistant/SKILL.md` and its relevant local modules.

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity.
```

### S252 | T1 | shopify-developer

- path: `.agents/skills/shopify-developer/SKILL.md`
- chars: 932
- outline:
- shopify-developer

```markdown
---
name: shopify-developer
description: Complete Shopify development reference covering Liquid templating, OS 2.0 themes, GraphQL APIs, Hydrogen, Functions, and performance optimization (API v2026-01). Use when working with .liquid files, building Shopify themes or apps, writing GraphQL queries for Shopify, debugging Liquid errors, creating app extensions, migrating from Scripts to Functions, or building headless storefronts. Triggers on "Shopify", "Liquid template", "Hydrogen", "Storefront API", "theme development", "Shopify Functions", "Polaris". Do NOT use for non-Shopify e-commerce platforms.
license: CC-BY-4.0
metadata:
  author: Tech Leads Club
  version: 1.0.0
  owner_agent: codenavi-agent
---

# shopify-developer

Read and follow `00_skills/(development)/shopify-developer/SKILL.md` and its relevant local modules.

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity.
```

### S253 | T1 | simulator-ai

- path: `.agents/skills/simulator-ai/SKILL.md`
- chars: 988
- outline:
- simulator-ai

```markdown
---
name: simulator-ai
description: 'Create ans entire constructor for an AI real world medical simulation. A skill that searches the entire internet to find AI real world medical simulator, to simulates patients and medical treatments ''till find THE CURE for diabetes. The skill needs to folow AGENT.md premisses: 4 agents and all layers of knowledge and the validator internal lenses, with all knowledge, extreme honest and never hallucinates to validate architecture, code, implemetation and the simulator itself. Skill must validates them a Use when the user requests simulator ai or invokes simulator-ai. Do NOT use for unrelated languages, domains or production deployment.'
license: CC-BY-4.0
metadata:
  author: AEOS
  version: 1.0.0
  owner_agent: codenavi-agent
---

# simulator-ai

Read and follow `00_skills/(development)/simulator-ai/SKILL.md` and its relevant local modules.

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity.
```

### S254 | T1 | skill-architect

- path: `.agents/skills/skill-architect/SKILL.md`
- chars: 730
- outline:
- skill-architect

```markdown
---
name: "skill-architect"
description: "Design, build, evaluate, score and improve reusable skills through discovery, architecture and minimal evidence-based edits. Use for create a skill, review my skill, rate or score my skill, improve SKILL.md. Do NOT use to identify whether finished work deserves a skill (learning-opportunities), create agent identities, or write a technical design document."
license: "CC-BY-4.0"
metadata:
  author: "Tech Leads Club"
  version: "1.1.1"
  owner_agent: "codenavi-agent"
---

# skill-architect

Read and follow `00_skills/(creation)/skill-architect/SKILL.md` and its relevant local modules.

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity.
```

### S255 | T1 | skill-factory

- path: `.agents/skills/skill-factory/SKILL.md`
- chars: 674
- outline:
- skill-factory

```markdown
---
name: skill-factory
description: Create, refactor, package and validate a reusable workspace skill with precise routing, entrypoint of at most 100 lines and local modules. Use when the user says criar skill, melhorar skills, refatorar SKILL.md or adicionar capacidade reutilizável. Do NOT use for one-off code fixes, human competency lists or new agent identities.
license: CC-BY-4.0
metadata:
  author: AEOS
  version: 2.0.0
  owner_agent: codenavi-agent
---

# skill-factory

Read and follow `00_skills/(creation)/skill-factory/SKILL.md` and its relevant local modules.

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity.
```

### S256 | T1 | skill-factory-generator

- path: `.agents/skills/skill-factory-generator/SKILL.md`
- chars: 639
- outline:
- skill-factory-generator

```markdown
---
name: skill-factory-generator
description: Generate a bounded reusable skill package with concrete routing, local resources and verifiable acceptance gates. Use when the user requests skill factory generator or invokes skill-factory-generator. Do NOT use for ordinary one-off coding or human competency lists.
license: CC-BY-4.0
metadata:
  author: AEOS
  version: 1.0.0
  owner_agent: codenavi-agent
---

# skill-factory-generator

Read and follow `00_skills/(creation)/skill-factory-generator/SKILL.md` and its relevant local modules.

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity.
```

### S257 | T1 | skill-hardener

- path: `.agents/skills/skill-hardener/SKILL.md`
- chars: 547
- outline:
- skill-hardener

```markdown
---
name: skill-hardener
description: Harden skills with contracts, forbidden actions and quality gates. Use when the user requests skill hardener or invokes skill-hardener. Do NOT use for ordinary one-off coding or human competency lists.
license: CC-BY-4.0
metadata:
  author: AEOS
  version: 1.0.0
  owner_agent: codenavi-agent
---

# skill-hardener

Read and follow `00_skills/(creation)/skill-hardener/SKILL.md` and its relevant local modules.

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity.
```

### S258 | T1 | slo-risk-analyzer

- path: `.agents/skills/slo-risk-analyzer/SKILL.md`
- chars: 574
- outline:
- slo-risk-analyzer

```markdown
---
name: slo-risk-analyzer
description: Map engineering operations to SLO/SLA risks and error budgets. Use when the user requests slo risk analyzer or invokes slo-risk-analyzer. Do NOT use for unrelated functionality or unmeasured speculative optimization.
license: CC-BY-4.0
metadata:
  author: AEOS
  version: 1.0.0
  owner_agent: codenavi-agent
---

# slo-risk-analyzer

Read and follow `00_skills/(performance)/slo-risk-analyzer/SKILL.md` and its relevant local modules.

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity.
```

### S259 | T1 | social-media-operator

- path: `.agents/skills/social-media-operator/SKILL.md`
- chars: 657
- outline:
- social-media-operator

```markdown
---
name: social-media-operator
description: Governed TikTok and Instagram operations via browser-based authentication sessions. Use when user asks for social media session management, TikTok/Instagram profile reading, or cookie-based authentication. Do NOT use for OAuth API keys or developer account management.
license: CC-BY-4.0
metadata:
  author: Tech Lead's Club / CodENavi
  version: 1.0.0
  owner_agent: codenavi-agent
---

# social-media-operator

Read and follow `00_skills/(tooling)/social-media-operator/SKILL.md` and its relevant local modules.

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity.
```

### S260 | T1 | social-selling

- path: `.agents/skills/social-selling/SKILL.md`
- chars: 1066
- outline:
- social-selling

```markdown
---
name: social-selling
description: When the user wants to sell through social media, optimize LinkedIn for sales, build DM sequences, or convert content engagement into pipeline. Also use when the user mentions 'social selling,' 'LinkedIn selling,' 'LinkedIn DMs,' 'social prospecting,' 'LinkedIn Sales Navigator,' 'DM sequences,' 'LinkedIn outreach,' 'social pipeline,' or 'LinkedIn optimization.' This skill covers social selling strategy from profile optimization through DM-to-deal conversion. Do NOT use for technical implementation, code review, or software architecture.
license: CC-BY-4.0
metadata:
  author: Chad Boyda / agent-gtm-skills
  version: 1.0.0
  original_author: Chad Boyda / agent-gtm-skills
  modified_by: Felipe Rodrigues - github.com/felipfr
  source: https://github.com/chadboyda/agent-gtm-skills
  owner_agent: codenavi-agent
---

# social-selling

Read and follow `00_skills/(gtm)/social-selling/SKILL.md` and its relevant local modules.

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity.
```

### S261 | T1 | solo-founder-gtm

- path: `.agents/skills/solo-founder-gtm/SKILL.md`
- chars: 1161
- outline:
- solo-founder-gtm

```markdown
---
name: solo-founder-gtm
description: When the user is a solo founder building their GTM motion, wants to scale without hiring, or needs to design an AI agent team for go-to-market. Also use when the user mentions 'solo founder,' 'one-person startup,' 'solopreneur,' 'bootstrapped,' 'no team,' 'AI agents as team,' 'scaling without hiring,' 'founder-led sales,' 'lean GTM,' 'one-person company,' or 'no employees.' This skill covers the complete solo founder GTM playbook from stack selection through agent team design, revenue-stage transitions, time allocation, and when to finally hire. Do NOT use for technical implementation, code review, or software architecture.
license: CC-BY-4.0
metadata:
  author: Chad Boyda / agent-gtm-skills
  version: 1.0.0
  original_author: Chad Boyda / agent-gtm-skills
  modified_by: Felipe Rodrigues - github.com/felipfr
  source: https://github.com/chadboyda/agent-gtm-skills
  owner_agent: codenavi-agent
---

# solo-founder-gtm

Read and follow `00_skills/(gtm)/solo-founder-gtm/SKILL.md` and its relevant local modules.

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity.
```

### S262 | T1 | solve-problems

- path: `.agents/skills/solve-problems/SKILL.md`
- chars: 570
- outline:
- solve-problems

```markdown
---
name: solve-problems
description: Fix defects across any programming language without changing project architecture. Use when the user requests solve problems or invokes solve-problems. Do NOT use for unrelated languages, domains or production deployment.
license: CC-BY-4.0
metadata:
  author: AEOS
  version: 1.0.0
  owner_agent: codenavi-agent
---

# solve-problems

Read and follow `00_skills/(development)/solve-problems/SKILL.md` and its relevant local modules.

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity.
```

### S263 | T1 | spec-driven

- path: `.agents/skills/spec-driven/SKILL.md`
- chars: 744
- outline:
- spec-driven

```markdown
---
name: spec-driven
description: "Tech Lead Club spec-driven 4.0.0: Specify, Design, Tasks, Execute with EARS criteria, proof commands, mutation checks and capture-based screen verification. Use for \"spec-driven\", \"specify feature\", \"implement\", \"verify work\", design and atomic tasks. Do NOT use for pure architecture decomposition or standalone technical design documents."
license: CC-BY-4.0
metadata:
  author: "AEOS; adapted from Felipe Rodrigues - github.com/felipfr"
  version: 4.0.0
  owner_agent: codenavi-agent
---

# spec-driven

Read and follow `00_skills/(development)/spec-driven/SKILL.md` and its relevant local modules.

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity.
```

### S264 | T1 | spec-driven-eval

- path: `.agents/skills/spec-driven-eval/SKILL.md`
- chars: 1022
- outline:
- spec-driven-eval

```markdown
---
name: spec-driven-eval
description: Scores how completely an implementation fulfills a PRD/spec, case by case, and produces a single comparable final grade. Invoke only when explicitly named (e.g. run spec-driven-eval); do not auto-trigger. Use when benchmarking spec-driven implementations, grading acceptance criteria, evaluating whether a feature was 100% implemented, comparing multiple implementations of the same PRD, or auditing implementation and test coverage (unit and e2e) against product requirements. Do NOT use for planning or building features (use tlc-spec-driven), writing PRDs, or general code review unrelated to a spec.
license: CC-BY-4.0
metadata:
  author: Waldemar Neto - github.com/waldemarnt
  version: 1.0.0
  owner_agent: codenavi-agent
disable-model-invocation: true
---

# spec-driven-eval

Read and follow `00_skills/(development)/spec-driven-eval/SKILL.md` and its relevant local modules.

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity.
```

### S265 | T1 | spec-driven-lean

- path: `.agents/skills/spec-driven-lean/SKILL.md`
- chars: 772
- outline:
- spec-driven-lean

```markdown
---
name: spec-driven-lean
description: "Tech Lead Club spec-lean 2.0.0: freeze observable obligations in plan and proof-backed checks, then build and verify mutations and screens. Use for \"spec-driven-lean\", \"plan feature\", \"write the checks\", \"build this plan\", \"verify work\". Do NOT use for standalone design documents, architecture decomposition or work with an existing task list."
license: CC-BY-4.0
metadata:
  author: "AEOS; adapted from Tech Leads Club - github.com/tech-leads-club"
  version: 2.0.0
  owner_agent: codenavi-agent
---

# spec-driven-lean

Read and follow `00_skills/(development)/spec-driven-lean/SKILL.md` and its relevant local modules.

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity.
```

### S266 | T1 | specs

- path: `.agents/skills/specs/SKILL.md`
- chars: 639
- outline:
- specs

```markdown
---
name: specs
description: 'Prevent ad hoc creation and modification by requiring a specification before implementation: scope, rationale, acceptance checks, risks and required evidence. Use when the user requests specs, a specification or a pre-implementation contract. Do NOT use to override approved requirements or expand the user request.'
license: CC-BY-4.0
metadata:
  author: AEOS
  version: 1.0.0
  owner_agent: codenavi-agent
---

# specs

Read and follow `00_skills/(development)/specs/SKILL.md` and its relevant local modules.

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity.
```

### S267 | T1 | splunk-observability-staff

- path: `.agents/skills/splunk-observability-staff/SKILL.md`
- chars: 751
- outline:
- splunk-observability-staff

```markdown
---
name: splunk-observability-staff
description: Deep Staff-level Splunk observability analysis for Splunk Enterprise, ITSI, Observability Cloud, searches, metrics, logs, traces, notable events, episodes and service-impact evidence. Use when the user requests splunk observability staff or invokes splunk-observability-staff. Do NOT use to restart, scale or mutate live systems without an authorized operations task.
license: CC-BY-4.0
metadata:
  author: AEOS
  version: 1.0.0
  owner_agent: codenavi-agent
---

# splunk-observability-staff

Read and follow `00_skills/(monitoring)/splunk-observability-staff/SKILL.md` and its relevant local modules.

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity.
```

### S268 | T1 | staff-iii-architecture-governor

- path: `.agents/skills/staff-iii-architecture-governor/SKILL.md`
- chars: 668
- outline:
- staff-iii-architecture-governor

```markdown
---
name: staff-iii-architecture-governor
description: Plan and select the best architecture for starting a project or changing an existing one. Use when the user requests staff iii architecture governor or invokes staff-iii-architecture-governor. Do NOT use for an unrelated implementation change or deployment execution.
license: CC-BY-4.0
metadata:
  author: AEOS
  version: 1.0.0
  owner_agent: codenavi-agent
---

# staff-iii-architecture-governor

Read and follow `00_skills/(architecture)/staff-iii-architecture-governor/SKILL.md` and its relevant local modules.

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity.
```

### S269 | T1 | staff-tdd-code-builder

- path: `.agents/skills/staff-tdd-code-builder/SKILL.md`
- chars: 605
- outline:
- staff-tdd-code-builder

```markdown
---
name: staff-tdd-code-builder
description: Create or change code according to an architecture plan using TDD by default. Use when the user requests staff tdd code builder or invokes staff-tdd-code-builder. Do NOT use for unrelated languages, domains or production deployment.
license: CC-BY-4.0
metadata:
  author: AEOS
  version: 1.0.0
  owner_agent: codenavi-agent
---

# staff-tdd-code-builder

Read and follow `00_skills/(development)/staff-tdd-code-builder/SKILL.md` and its relevant local modules.

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity.
```

### S270 | T1 | subagent-creator

- path: `.agents/skills/subagent-creator/SKILL.md`
- chars: 770
- outline:
- subagent-creator

```markdown
---
name: "subagent-creator"
description: "Design bounded sequential lenses of codenavi-agent with a single deliverable, explicit evidence packet, minimal tools and verifiable verdict. Use for create verifier, parity auditor, isolated review procedure or specialized work unit. Do NOT use for creating, register or spawn agent identities; use skill-architect for a reusable skill and cursor-subagent-creator for Cursor work-unit guidance."
license: "CC-BY-4.0"
metadata:
  author: "Tech Leads Club"
  version: "1.1.0"
  owner_agent: "codenavi-agent"
---

# subagent-creator

Read and follow `00_skills/(creation)/subagent-creator/SKILL.md` and its relevant local modules.

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity.
```

### S271 | T1 | supply-chain-auditor

- path: `.agents/skills/supply-chain-auditor/SKILL.md`
- chars: 587
- outline:
- supply-chain-auditor

```markdown
---
name: supply-chain-auditor
description: Audit dependencies, provenance, package trust and release integrity. Use when the user requests supply chain auditor or invokes supply-chain-auditor. Do NOT use outside authorized defensive scope or to expose secret values.
license: CC-BY-4.0
metadata:
  author: AEOS
  version: 1.0.0
  owner_agent: codenavi-agent
---

# supply-chain-auditor

Read and follow `00_skills/(security)/supply-chain-auditor/SKILL.md` and its relevant local modules.

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity.
```

### S272 | T1 | tactical-ddd

- path: `.agents/skills/tactical-ddd/SKILL.md`
- chars: 1064
- outline:
- tactical-ddd

```markdown
---
name: tactical-ddd
description: Detects anemic domain models, validates and refactors them into rich domain models, and enforces tactical DDD patterns (Entities, Value Objects, Aggregates, Domain Services, Domain Events). Use when the user asks to validate, review, or check domain models or DDD code; detect anemia; refactor domain objects; improve encapsulation; or mentions terms like "anemic model", "rich domain", "aggregate", "value object", "domain event", "ubiquitous language", "is this good DDD", "does this follow DDD", or "check my domain". Do NOT use for module or service boundary design, architectural decomposition, strategic DDD context mapping, or code outside the domain layer (DTOs, controllers, infrastructure adapters).
license: CC-BY-4.0
metadata:
  author: Tech Leads Club
  version: 1.0.0
  owner_agent: codenavi-agent
---

# tactical-ddd

Read and follow `00_skills/(architecture)/tactical-ddd/SKILL.md` and its relevant local modules.

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity.
```

### S273 | T1 | task-graph-builder

- path: `.agents/skills/task-graph-builder/SKILL.md`
- chars: 557
- outline:
- task-graph-builder

```markdown
---
name: task-graph-builder
description: Build a deterministic task graph from a playbook and objective. Use when the user requests task graph builder or invokes task-graph-builder. Do NOT use for unrelated tools or unapproved remote writes.
license: CC-BY-4.0
metadata:
  author: AEOS
  version: 1.0.0
  owner_agent: codenavi-agent
---

# task-graph-builder

Read and follow `00_skills/(tooling)/task-graph-builder/SKILL.md` and its relevant local modules.

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity.
```

### S274 | T1 | technical-design-doc-creator

- path: `.agents/skills/technical-design-doc-creator/SKILL.md`
- chars: 682
- outline:
- technical-design-doc-creator

```markdown
---
name: technical-design-doc-creator
description: 'Assimilated TLC TDD writer. Create architecture-level Technical Design Documents through discovery. Triggers: write a design doc, create a TDD, technical spec, architecture document, RFC, design proposal, criar um TDD. Do not use for README, API docs, or general docs (docs-writer).'
license: CC-BY-4.0
metadata:
  author: Tech Leads Club
  version: 1.0.0
  owner_agent: codenavi-agent
---

# technical-design-doc-creator

Read and follow `00_skills/(creation)/create-technical-design-doc/SKILL.md` and its relevant local modules.

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity.
```

### S275 | T1 | telemetry-bug-root-cause-solver

- path: `.agents/skills/telemetry-bug-root-cause-solver/SKILL.md`
- chars: 746
- outline:
- telemetry-bug-root-cause-solver

```markdown
---
name: telemetry-bug-root-cause-solver
description: Resolve bugs from logs, metrics, traces, events, alerts and stack traces by correlating runtime evidence with code, tests, rollback and learning records. Use when the user requests telemetry bug root cause solver or invokes telemetry-bug-root-cause-solver. Do NOT use to restart, scale or mutate live systems without an authorized operations task.
license: CC-BY-4.0
metadata:
  author: AEOS
  version: 1.0.0
  owner_agent: codenavi-agent
---

# telemetry-bug-root-cause-solver

Read and follow `00_skills/(monitoring)/telemetry-bug-root-cause-solver/SKILL.md` and its relevant local modules.

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity.
```

### S276 | T1 | test-gap-analyzer

- path: `.agents/skills/test-gap-analyzer/SKILL.md`
- chars: 630
- outline:
- test-gap-analyzer

```markdown
---
name: test-gap-analyzer
description: Analyze the gap between source code and test coverage — identifying untested modules, functions, and edge cases. Use when the user requests test gap analyzer or invokes test-gap-analyzer. Do NOT use as deployment authorization or as evidence for checks that were not executed.
license: CC-BY-4.0
metadata:
  author: AEOS
  version: 1.0.0
  owner_agent: codenavi-agent
---

# test-gap-analyzer

Read and follow `00_skills/(quality)/test-gap-analyzer/SKILL.md` and its relevant local modules.

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity.
```

### S277 | T1 | test-generation

- path: `.agents/skills/test-generation/SKILL.md`
- chars: 564
- outline:
- test-generation

```markdown
---
name: test-generation
description: Detect test gaps and generate proposed tests in sandbox. Use when the user requests test generation or invokes test-generation. Do NOT use as deployment authorization or as evidence for checks that were not executed.
license: CC-BY-4.0
metadata:
  author: AEOS
  version: 1.0.0
  owner_agent: codenavi-agent
---

# test-generation

Read and follow `00_skills/(quality)/test-generation/SKILL.md` and its relevant local modules.

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity.
```

### S278 | T1 | test-strategy-architect

- path: `.agents/skills/test-strategy-architect/SKILL.md`
- chars: 626
- outline:
- test-strategy-architect

```markdown
---
name: test-strategy-architect
description: Build test strategy across unit/integration/contract/e2e/security/performance. Use when the user requests test strategy architect or invokes test-strategy-architect. Do NOT use as deployment authorization or as evidence for checks that were not executed.
license: CC-BY-4.0
metadata:
  author: AEOS
  version: 1.0.0
  owner_agent: codenavi-agent
---

# test-strategy-architect

Read and follow `00_skills/(quality)/test-strategy-architect/SKILL.md` and its relevant local modules.

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity.
```

### S279 | T1 | test-writer

- path: `.agents/skills/test-writer/SKILL.md`
- chars: 621
- outline:
- test-writer

```markdown
---
name: test-writer
description: Generate proposed test files in sandbox directory based on evidence from source code analysis. Never writes to real test directories. Use when the user requests test writer or invokes test-writer. Do NOT use as deployment authorization or as evidence for checks that were not executed.
license: CC-BY-4.0
metadata:
  author: AEOS
  version: 1.0.0
  owner_agent: codenavi-agent
---

# test-writer

Read and follow `00_skills/(quality)/test-writer/SKILL.md` and its relevant local modules.

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity.
```

### S280 | T1 | tests-expert

- path: `.agents/skills/tests-expert/SKILL.md`
- chars: 813
- outline:
- tests-expert

```markdown
---
name: tests-expert
description: Runs the application's real functional and end-to-end checks after a bug fix or new behavior, before that work is called done. Use when the user says corrigir, consertar, implementar, código novo, nova funcionalidade, fix the bug, new feature, prove que funciona, teste funcional, teste de ponta a ponta, end-to-end, e2e, or when a previous window left an open tests-expert failure. Do NOT use for unit tests, class tests, coverage, or tests derived from the implementation.
license: CC-BY-4.0
metadata:
  author: AEOS
  version: 1.0.0
  owner_agent: codenavi-agent
---

# tests-expert

Read and follow `00_skills/(quality)/tests-expert/SKILL.md` and its relevant local modules.

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity.
```

### S281 | T1 | the-fool

- path: `.agents/skills/the-fool/SKILL.md`
- chars: 726
- outline:
- the-fool

```markdown
---
name: "the-fool"
description: "Stress-test a pending decision, plan or claim with its rationale, alternatives and reversibility; expose concrete threats, fragile assumptions and evidenced biases. Use for advogado do diabo, challenge this, pre-mortem, red team or blind spots. Do NOT use to decide for the owner, implement the solution, or harvest lessons from finished work (learning-opportunities)."
license: "CC-BY-4.0"
metadata:
  author: "Tech Leads Club"
  version: "1.1.0"
  owner_agent: "codenavi-agent"
---

# the-fool

Read and follow `00_skills/(decision-making)/the-fool/SKILL.md` and its relevant local modules.

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity.
```

### S282 | T1 | the-judge

- path: `.agents/skills/the-judge/SKILL.md`
- chars: 1287
- outline:
- the-judge

```markdown
---
name: the-judge
description: Evidence-first pull request judge that reviews a PR and posts one consolidated GitHub review with inline comments via the gh CLI. Runs the repo's own deterministic checks first, researches current official docs before any claim about external libraries or APIs, then reviews correctness, security, structural quality (code judo, spaghetti growth, file-size limits), and AI slop including useless code comments. Every finding must carry evidence, every comment passes a deterministic noise gate before posting, and the verdict (APPROVE, COMMENT, REQUEST_CHANGES) is weighed by findings. Use when asked to review a PR, judge this PR, review this branch or diff before merge, run the-judge, "revise esse PR", "faca o code review", or "julgue esse PR". Do NOT use for reviewing prose or documents, fixing CI failures, resolving merge conflicts, writing the fix itself, or responding to review comments (use gh-address-comments).
license: CC-BY-4.0
metadata:
  author: Felipe Rodrigues - github.com/felipfr
  version: 1.4.0
  owner_agent: codenavi-agent
---

# the-judge

Read and follow `00_skills/(quality)/the-judge/SKILL.md` and its relevant local modules.

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity.
```

### S283 | T1 | the-jury

- path: `.agents/skills/the-jury/SKILL.md`
- chars: 700
- outline:
- the-jury

```markdown
---
name: "the-jury"
description: "Evaluate a decidable question through 3 or 5 orthogonal sequential lenses of codenavi-agent, then tally a verdict with dissent and evidence. Use for monte um júri, painel de decisão or compare options through multiple perspectives. Do NOT use to spawn agents, claim independent cognition, merely critique (the-fool) or implement the decision."
license: "CC-BY-4.0"
metadata:
  author: "Tech Leads Club"
  version: "1.1.0"
  owner_agent: "codenavi-agent"
---

# the-jury

Read and follow `00_skills/(decision-making)/the-jury/SKILL.md` and its relevant local modules.

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity.
```

### S284 | T1 | threat-modeler

- path: `.agents/skills/threat-modeler/SKILL.md`
- chars: 591
- outline:
- threat-modeler

```markdown
---
name: threat-modeler
description: Produce AEOS threat models for prompt injection, tool poisoning, secret leakage and package tampering. Use when the user requests threat modeler or invokes threat-modeler. Do NOT use outside authorized defensive scope or to expose secret values.
license: CC-BY-4.0
metadata:
  author: AEOS
  version: 1.0.0
  owner_agent: codenavi-agent
---

# threat-modeler

Read and follow `00_skills/(security)/threat-modeler/SKILL.md` and its relevant local modules.

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity.
```

### S285 | T1 | tlc-discover

- path: `.agents/skills/tlc-discover/SKILL.md`
- chars: 766
- outline:
- tlc-discover

```markdown
---
name: tlc-discover
description: Interviews an unshaped idea into a verdict and a design document - decisions, flows, schema, contracts - that anyone can plan from without having been in the room. Use when the user says "research this", "help me understand this problem", "should we build this", "discovery", "explore this problem", or "tlc-discover". Do NOT use to cut a finished design into tasks, or to implement.
license: CC-BY-4.0
metadata:
  author: Tech Leads Club - github.com/tech-leads-club
  version: 0.9.0
  owner_agent: codenavi-agent
---

# tlc-discover

Read and follow `00_skills/(development)/tlc-discover/SKILL.md` and its relevant local modules.

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity.
```

### S286 | T1 | tlc-generative-engine-optimization

- path: `.agents/skills/tlc-generative-engine-optimization/SKILL.md`
- chars: 1269
- outline:
- tlc-generative-engine-optimization

```markdown
---
name: tlc-generative-engine-optimization
description: Generative Engine Optimization (GEO) specialist — the technical, on-page publishing work that makes a given page or site discoverable, understandable, trustworthy, quotable, and fresh for AI answer engines (Google AI Overviews, ChatGPT Search, Bing Copilot, Perplexity). Use when asked to 'optimize this page/site for GEO', 'optimize for AI search / answer engines', 'get my page cited by ChatGPT/Perplexity', 'improve AI visibility/citability', 'write an llms.txt', 'add citation-ready structure or schema for AI answers', 'otimizar para busca com IA', or to audit/create/improve a codebase for generative search. Do NOT use for AI-driven SEO content strategy or programmatic pages at scale (use ai-seo), classic keyword/SERP ranking (use seo), accessibility (use web-accessibility), or multi-area site audits (use web-quality-audit).
license: MIT
metadata:
  author: Fernando Paladini - github.com/paladini
  version: 1.0.0
  owner_agent: codenavi-agent
---

# tlc-generative-engine-optimization

Read and follow `00_skills/(quality)/tlc-generative-engine-optimization/SKILL.md` and its relevant local modules.

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity.
```

### S287 | T1 | tlc-implement

- path: `.agents/skills/tlc-implement/SKILL.md`
- chars: 690
- outline:
- tlc-implement

```markdown
---
name: tlc-implement
description: 'Implement a work already planned: extracts a checklist, builds it, and proves every check with an independent verifier. Use when the user says "extract a checklist", "build this ticket", "implement this spec", or "tlc-implement". Do NOT use when nobody has decided what to build, or to design the work.'
license: CC-BY-4.0
metadata:
  author: Tech Leads Club - github.com/tech-leads-club
  version: 0.1.0
  owner_agent: codenavi-agent
---

# tlc-implement

Read and follow `00_skills/(development)/tlc-implement/SKILL.md` and its relevant local modules.

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity.
```

### S288 | T1 | tlc-plan

- path: `.agents/skills/tlc-plan/SKILL.md`
- chars: 604
- outline:
- tlc-plan

```markdown
---
name: tlc-plan
description: 'Assimilated TLC tlc-plan 0.2.0. Turn a decided PRD, design doc, RFC or ticket into grounded tasks with observable criteria. Triggers: tlc-plan, write the task, cut this PRD into tasks, turn this design doc into work. Do not use for discovery or implementation.'
license: CC-BY-4.0
metadata:
  author: Tech Leads Club
  version: 1.0.0
  owner_agent: codenavi-agent
---

# tlc-plan

Read and follow `00_skills/(development)/tlc-plan/SKILL.md` and its relevant local modules.

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity.
```

### S289 | T1 | tlc-prd

- path: `.agents/skills/tlc-prd/SKILL.md`
- chars: 800
- outline:
- tlc-prd

```markdown
---
name: tlc-prd
description: "Interviews an idea into a PRD file covering situation, problem, success, boundary, and journey states, and stops before any technical design. Use when the user says \"write the PRD\", \"create the PRD\", \"PRD\", \"product spec\", \"product requirements\", \"tlc-prd\", or \"what does the product need to decide\". Do NOT use for designing a solution, choosing technology, publishing the document, or cutting the PRD into tasks."
license: CC-BY-4.0
metadata:
  author: "Tech Leads Club - github.com/tech-leads-club"
  version: 1.0.0
  owner_agent: codenavi-agent
---

# tlc-prd

Read and follow `00_skills/(development)/tlc-prd/SKILL.md` and its relevant local modules.

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity.
```

### S290 | T1 | tlc-spec-driven

- path: `.agents/skills/tlc-spec-driven/SKILL.md`
- chars: 741
- outline:
- tlc-spec-driven

```markdown
---
name: tlc-spec-driven
description: "Tech Lead Club spec-driven 4.0.0: Specify, Design, Tasks, Execute with EARS criteria, proof commands, mutation checks and capture-based screen verification. Use for \"tlc-spec-driven\", \"specify feature\", \"implement\", \"verify work\", design and atomic tasks. Do NOT use for pure architecture decomposition or standalone technical design documents."
license: CC-BY-4.0
metadata:
  author: "Felipe Rodrigues - github.com/felipfr"
  version: 4.0.0
  owner_agent: codenavi-agent
---

# tlc-spec-driven

Read and follow `00_skills/(development)/tlc-spec-driven/SKILL.md` and its relevant local modules.

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity.
```

### S291 | T1 | tlc-spec-lean

- path: `.agents/skills/tlc-spec-lean/SKILL.md`
- chars: 741
- outline:
- tlc-spec-lean

```markdown
---
name: tlc-spec-lean
description: "Tech Lead Club spec-lean 2.0.0: freeze observable obligations in plan and proof-backed checks, then build and verify mutations and screens. Use for \"tlc-spec-lean\", \"plan feature\", \"write the checks\", \"build this plan\", \"verify work\". Do NOT use for standalone design documents, architecture decomposition or work with an existing task list."
license: CC-BY-4.0
metadata:
  author: "Tech Leads Club - github.com/tech-leads-club"
  version: 2.0.0
  owner_agent: codenavi-agent
---

# tlc-spec-lean

Read and follow `00_skills/(development)/tlc-spec-lean/SKILL.md` and its relevant local modules.

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity.
```

### S292 | T1 | token-budget-governor

- path: `.agents/skills/token-budget-governor/SKILL.md`
- chars: 696
- outline:
- token-budget-governor

```markdown
---
name: token-budget-governor
description: Prevent token waste across GPT, Codex, Claude, DeepSeek and local/free models by enforcing scoped prompts, compact context and narrow internal lenses contracts. Use when the user requests token budget governor or invokes token-budget-governor. Do NOT use to promote unverified claims or transient task status into durable memory.
license: CC-BY-4.0
metadata:
  author: AEOS
  version: 1.0.0
  owner_agent: codenavi-agent
---

# token-budget-governor

Read and follow `00_skills/(learning)/token-budget-governor/SKILL.md` and its relevant local modules.

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity.
```

### S293 | T1 | tool-router-audit

- path: `.agents/skills/tool-router-audit/SKILL.md`
- chars: 573
- outline:
- tool-router-audit

```markdown
---
name: tool-router-audit
description: Audit whether AEOS code and playbooks enforce Tool Router for every external action. Use when the user requests tool router audit or invokes tool-router-audit. Do NOT use for unrelated tools or unapproved remote writes.
license: CC-BY-4.0
metadata:
  author: AEOS
  version: 1.0.0
  owner_agent: codenavi-agent
---

# tool-router-audit

Read and follow `00_skills/(tooling)/tool-router-audit/SKILL.md` and its relevant local modules.

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity.
```

### S294 | T1 | typesafe-ai

- path: `.agents/skills/typesafe-ai/SKILL.md`
- chars: 1066
- outline:
- typesafe-ai

```markdown
---
name: typesafe-ai
description: 'Build AI-powered software with TypeSafe: small units of AI intelligence you can use like programming primitives. Its System One models, including Jev, turn natural language and application state into typed judgments and probabilities that code can combine. Use when a feature needs programmable common sense, when brainstorming what AI could make possible in an app, or when an LLM prompt-and-parse step could become a structured decision. Applications include routing, ranking, extraction, verification, and interactive experiences; these are starting points, not the limits. Read live docs and cookbooks to find useful patterns and discover new combinations. Do NOT use for unrelated languages, domains or production deployment.'
license: MIT
metadata:
  author: AEOS
  version: 1.0.0
  owner_agent: codenavi-agent
---

# typesafe-ai

Read and follow `00_skills/(development)/typesafe-ai/SKILL.md` and its relevant local modules.

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity.
```

### S295 | T1 | unique-environment-auditor

- path: `.agents/skills/unique-environment-auditor/SKILL.md`
- chars: 672
- outline:
- unique-environment-auditor

```markdown
---
name: unique-environment-auditor
description: Audit a target environment inventory for conflicting tool versions, duplicated configuration and unmet runtime requirements. Use when the user requests unique environment auditor or invokes unique-environment-auditor. Do NOT use for unrelated languages, domains or production deployment.
license: CC-BY-4.0
metadata:
  author: AEOS
  version: 1.0.0
  owner_agent: codenavi-agent
---

# unique-environment-auditor

Read and follow `00_skills/(development)/unique-environment-auditor/SKILL.md` and its relevant local modules.

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity.
```

### S296 | T1 | universal-project-factory

- path: `.agents/skills/universal-project-factory/SKILL.md`
- chars: 664
- outline:
- universal-project-factory

```markdown
---
name: universal-project-factory
description: Plan and generate a sandbox-first project from zero to production for any requested architecture, language set and database set. Use when the user requests universal project factory or invokes universal-project-factory. Do NOT use for ordinary one-off coding or human competency lists.
license: CC-BY-4.0
metadata:
  author: AEOS
  version: 1.0.0
  owner_agent: codenavi-agent
---

# universal-project-factory

Read and follow `00_skills/(creation)/universal-project-factory/SKILL.md` and its relevant local modules.

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity.
```

### S297 | T1 | v1-readiness-auditor

- path: `.agents/skills/v1-readiness-auditor/SKILL.md`
- chars: 603
- outline:
- v1-readiness-auditor

```markdown
---
name: v1-readiness-auditor
description: Validate AEOS against v1.0 release gates and generate blocking report. Use when the user requests v1 readiness auditor or invokes v1-readiness-auditor. Do NOT use as deployment authorization or as evidence for checks that were not executed.
license: CC-BY-4.0
metadata:
  author: AEOS
  version: 1.0.0
  owner_agent: codenavi-agent
---

# v1-readiness-auditor

Read and follow `00_skills/(quality)/v1-readiness-auditor/SKILL.md` and its relevant local modules.

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity.
```

### S298 | T1 | vercel-deploy

- path: `.agents/skills/vercel-deploy/SKILL.md`
- chars: 644
- outline:
- vercel-deploy

```markdown
---
name: vercel-deploy
description: Deploy applications and websites to Vercel. Use when the user requests deployment actions like "deploy my app", "deploy and give me the link", "push this live", or "create a preview deployment". Do NOT use for deploying to Netlify, Cloudflare, or Render (use their respective skills).
license: CC-BY-4.0
metadata:
  author: github.com/openai/skills
  version: 1.0.0
  owner_agent: codenavi-agent
---

# vercel-deploy

Read and follow `00_skills/(cloud)/vercel-deploy/SKILL.md` and its relevant local modules.

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity.
```

### S299 | T1 | video-outreach

- path: `.agents/skills/video-outreach/SKILL.md`
- chars: 1059
- outline:
- video-outreach

```markdown
---
name: video-outreach
description: When the user wants to build video-first cold outreach, create personalized video at scale, implement async selling, or use AI demo generation for prospecting. Also use when the user mentions 'video outreach,' 'personalized video,' 'video prospecting,' 'Tavus,' 'Sendspark,' 'HeyGen,' 'video email,' 'async selling,' 'video demo,' or 'made this for you.' This skill covers video-first outreach systems from personalization through conversion optimization. Do NOT use for technical implementation, code review, or software architecture.
license: CC-BY-4.0
metadata:
  author: Chad Boyda / agent-gtm-skills
  version: 1.0.0
  original_author: Chad Boyda / agent-gtm-skills
  modified_by: Felipe Rodrigues - github.com/felipfr
  source: https://github.com/chadboyda/agent-gtm-skills
  owner_agent: codenavi-agent
---

# video-outreach

Read and follow `00_skills/(gtm)/video-outreach/SKILL.md` and its relevant local modules.

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity.
```

### S300 | T1 | voiceai

- path: `.agents/skills/voiceai/SKILL.md`
- chars: 698
- outline:
- voiceai

```markdown
---
name: voiceai
description: 'Provide an evidence-backed voice interface for AEOS. Activating this skill is treated as explicit current-session consent for `voiceai` to record user audio or transcribe audio from user-authorized audio/video media within the declared scope. The skill can: Use when the user requests voiceai or invokes voiceai. Do NOT use for unrelated tools or unapproved remote writes.'
license: CC-BY-4.0
metadata:
  author: AEOS
  version: 1.0.0
  owner_agent: codenavi-agent
---

# voiceai

Read and follow `00_skills/(tooling)/voiceai/SKILL.md` and its relevant local modules.

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity.
```

### S301 | T1 | vox-aurum

- path: `.agents/skills/vox-aurum/SKILL.md`
- chars: 804
- outline:
- vox-aurum

```markdown
---
name: "vox-aurum"
description: "Transcribe authorized local bare audio offline with a verified local Whisper model, preserving spoken language and literal output; optionally use an explicitly requested GPU. Use for transcreva esse áudio, áudios dessa pasta, audio to text or transcrição offline. Do NOT use for meeting/call video even if only transcrever is requested (acta-aurea), diarized minutes, live dictation, editing/translation or voice cloning."
license: "CC-BY-4.0"
metadata:
  author: "AEOS; photographic reference supplied by user"
  version: "1.1.1"
  owner_agent: "codenavi-agent"
---

# vox-aurum

Read and follow `00_skills/(tooling)/vox-aurum/SKILL.md` and its relevant local modules.

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity.
```

### S302 | T1 | vuln-obsol-recon

- path: `.agents/skills/vuln-obsol-recon/SKILL.md`
- chars: 746
- outline:
- vuln-obsol-recon

```markdown
---
name: vuln-obsol-recon
description: Assess known vulnerabilities and lifecycle risk for the exact versions detected in repository/runtime evidence. Use when the user says esta versão tem CVE, tecnologia está obsoleta or mapear vulnerabilidade e EOL. Do NOT use for base synchronization, patch implementation, deep PR security review or invented versions without manifests/runtime evidence.
license: CC-BY-4.0
metadata:
  author: AEOS; photographic reference supplied by user
  version: 1.0.0
  owner_agent: codenavi-agent
---

# vuln-obsol-recon

Read and follow `00_skills/(security)/vuln-obsol-recon/SKILL.md` and its relevant local modules.

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity.
```

### S303 | T1 | web-accessibility

- path: `.agents/skills/web-accessibility/SKILL.md`
- chars: 717
- outline:
- web-accessibility

```markdown
---
name: web-accessibility
description: Audit and improve web accessibility following WCAG 2.1 guidelines. Use when asked to "improve accessibility", "a11y audit", "WCAG compliance", "screen reader support", "keyboard navigation", or "make accessible". Do NOT use for SEO (use seo), performance (use core-web-vitals), or comprehensive site audits covering multiple areas (use web-quality-audit).
license: MIT
metadata:
  author: web-quality-skills
  version: 1.0.0
  owner_agent: codenavi-agent
---

# web-accessibility

Read and follow `00_skills/(quality)/web-accessibility/SKILL.md` and its relevant local modules.

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity.
```

### S304 | T1 | web-best-practices

- path: `.agents/skills/web-best-practices/SKILL.md`
- chars: 685
- outline:
- web-best-practices

```markdown
---
name: web-best-practices
description: 'Assimilated TLC/web-quality best-practices skill. Apply modern web security, compatibility, and code-quality checks. Triggers: apply best practices, security audit, modernize code, code quality review, check for vulnerabilities. Do not use as the primary skill for accessibility, SEO (ai-seo), or a full multi-area audit.'
license: MIT
metadata:
  author: Tech Leads Club
  version: 1.0.0
  owner_agent: codenavi-agent
---

# web-best-practices

Read and follow `00_skills/(quality)/web-best-practices/SKILL.md` and its relevant local modules.

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity.
```

### S305 | T1 | web-design-guidelines

- path: `.agents/skills/web-design-guidelines/SKILL.md`
- chars: 763
- outline:
- web-design-guidelines

```markdown
---
name: web-design-guidelines
description: Review UI code for Web Interface Guidelines compliance. Use when asked to "review my UI", "check accessibility", "audit design", "review UX", or "check my site against best practices". Focuses on visual design and interaction patterns. Do NOT use for performance audits (use core-web-vitals), SEO (use seo), or comprehensive site audits (use web-quality-audit).
license: CC-BY-4.0
metadata:
  author: vercel
  version: 1.0.0
  argument-hint: <file-or-pattern>
  owner_agent: codenavi-agent
---

# web-design-guidelines

Read and follow `00_skills/(design)/web-design-guidelines/SKILL.md` and its relevant local modules.

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity.
```

### S306 | T1 | web-quality-audit

- path: `.agents/skills/web-quality-audit/SKILL.md`
- chars: 669
- outline:
- web-quality-audit

```markdown
---
name: web-quality-audit
description: 'Assimilated TLC/web-quality multi-area audit. Review performance, accessibility, SEO and best practices in one pass. Triggers: audit my site, review web quality, check page quality, optimize my website across areas. Do not use for a single-area job (core-web-vitals, ai-seo, best-practices, perf-lighthouse).'
license: MIT
metadata:
  author: Tech Leads Club
  version: 1.0.0
  owner_agent: codenavi-agent
---

# web-quality-audit

Read and follow `00_skills/(quality)/web-quality-audit/SKILL.md` and its relevant local modules.

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity.
```

### S307 | T1 | whatsapp-simulator

- path: `.agents/skills/whatsapp-simulator/SKILL.md`
- chars: 615
- outline:
- whatsapp-simulator

```markdown
---
name: whatsapp-simulator
description: Generate synthetic WhatsApp-style conversation fixtures for testing conversational systems, support flows and automation. Use when the user requests whatsapp simulator or invokes whatsapp-simulator. Do NOT use for unrelated tools or unapproved remote writes.
license: CC-BY-4.0
metadata:
  author: AEOS
  version: 1.0.0
  owner_agent: codenavi-agent
---

# whatsapp-simulator

Read and follow `00_skills/(tooling)/whatsapp-simulator/SKILL.md` and its relevant local modules.

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity.
```

### S308 | T1 | wordpress-expert

- path: `.agents/skills/wordpress-expert/SKILL.md`
- chars: 777
- outline:
- wordpress-expert

```markdown
---
name: wordpress-expert
description: Staff-level WordPress engineering super-skill for one-shot site mapping, clean-code AI-assisted project creation/modification, the complete installed plugin universe, governed remote wp-admin operations, themes/blocks/layout, third-party integrations and production-safe changes. Use when the user requests wordpress expert or invokes wordpress-expert. Do NOT use for unrelated languages, domains or production deployment.
license: CC-BY-4.0
metadata:
  author: AEOS
  version: 1.0.0
  owner_agent: codenavi-agent
---

# wordpress-expert

Read and follow `00_skills/(development)/wordpress-expert/SKILL.md` and its relevant local modules.

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity.
```

### S309 | T1 | workbench-profile-resolver

- path: `.agents/skills/workbench-profile-resolver/SKILL.md`
- chars: 649
- outline:
- workbench-profile-resolver

```markdown
---
name: workbench-profile-resolver
description: Resolve the smallest compatible workbench profile from task scope, available capabilities and explicit constraints. Use when the user requests workbench profile resolver or invokes workbench-profile-resolver. Do NOT use for unrelated tools or unapproved remote writes.
license: CC-BY-4.0
metadata:
  author: AEOS
  version: 1.0.0
  owner_agent: codenavi-agent
---

# workbench-profile-resolver

Read and follow `00_skills/(tooling)/workbench-profile-resolver/SKILL.md` and its relevant local modules.

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity.
```

### S901 | T1 | Clean coding tips

- path: `(deck)/S901.md`
- chars: 202
- outline:
- Clean Coding Tips

```markdown
# Clean Coding Tips

- Prefer clear variable names and small functions.
- Follow SOLID and keep layers thin.
- Write readable comments when needed.
- Prefer composition over inheritance when practical.
```

### S902 | T1 | Assistant highlights

- path: `(deck)/S902.md`
- chars: 133
- outline:
- Assistant Highlights

```markdown
# Assistant Highlights

- Works with natural language.
- Returns relevant results quickly.
- Most efficient first step for any task.
```

### S903 | T1 | Module boundary rule

- path: `(deck)/S903.md`
- chars: 489
- outline:
- Module Boundary Rule
  - Critical

```markdown
# Module Boundary Rule

## Critical

- Never reach into another module's private storage or internal data access layer.
- Call only that module's documented public API or exported interface.
- Writes that span modules must use the project's declared transaction or unit-of-work boundary for the owning module — do not open a second write path around it.
- If you need data owned elsewhere, go through that owner module; do not import its internal repositories, tables, or storage helpers.
```

