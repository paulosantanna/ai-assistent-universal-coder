# Track C — Surface deck (usefulness)

> run: 2026-11-16-abc
> generated: 2026-11-16T11:53:22.011941+00:00
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

## Surfaces (331)

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
- chars: 465
- outline:
- accessibility

```markdown
---
name: accessibility
description: "Audit and improve web accessibility to WCAG 2.1. Use for a11y audits. Do NOT use for SEO or performance work."
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
- chars: 532
- outline:
- acta-aurea

```markdown
---
name: "acta-aurea"
description: "Authorized meeting video to offline pack: transcript, speakers, minutes. Use for an ata or call transcript. Do NOT use for bare audio (vox-aurum)."
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
- chars: 500
- outline:
- adr-decision-writer

```markdown
---
name: adr-decision-writer
description: "Write ADRs from inspected evidence only. Use when asked for an ADR or decision record. Do NOT use for deployment or unrelated domains."
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
- chars: 507
- outline:
- agent-trace-validator

```markdown
---
name: agent-trace-validator
description: "Validate agent trace completeness and integrity. Use for trace validation. Do NOT use as deployment approval or proof of unexecuted checks."
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
- chars: 506
- outline:
- ai-architecture-expert

```markdown
---
name: ai-architecture-expert
description: "Design or reconstruct production AI architecture with evidence and trade-offs. Use for AI architecture. Do NOT use for deployment."
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
- chars: 671
- outline:
- ai-cold-outreach

```markdown
---
name: ai-cold-outreach
description: "AI cold outreach: emails, deliverability, personalization. Use for cold email or Instantly/Smartlead/Clay stacks. Do NOT use for code work."
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
- chars: 552
- outline:
- ai-continuous-training-maintainer

```markdown
---
name: ai-continuous-training-maintainer
description: "Maintain the aidiabetic-research training pipeline (ML practices, CVE-free deps, SAST). Use for it. Do NOT use for other projects or deployment."
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
- chars: 512
- outline:
- ai-engineering-expert

```markdown
---
name: ai-engineering-expert
description: "Build or refactor production AI systems from requirements to monitored deployment. Use for AI engineering. Do NOT use for unrelated domains."
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
- chars: 496
- outline:
- ai-evals-expert

```markdown
---
name: ai-evals-expert
description: "Turn AI quality claims into reproducible eval evidence. Use for AI quality evaluation. Do NOT use as deployment approval or for unexecuted checks."
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
- chars: 644
- outline:
- ai-pricing

```markdown
---
name: ai-pricing
description: "Price AI products: charge metric, tiers, packaging, margins. Use for AI pricing or BYOK. Do NOT use for code or architecture work."
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
- chars: 504
- outline:
- ai-project-bootstrapper

```markdown
---
name: ai-project-bootstrapper
description: "Bootstrap a real AI project from zero or rebuild one step by step. Use to bootstrap an AI project. Do NOT use for one-off coding."
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
- chars: 642
- outline:
- ai-sdr

```markdown
---
name: ai-sdr
description: "AI SDR deployment: qualification automation, signal routing, sales agents. Use for AI SDR/BDR or autonomous sales. Do NOT use for code work."
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
- chars: 477
- outline:
- ai-seo

```markdown
---
name: ai-seo
description: "Programmatic SEO, competitor pages, AI Overviews/GEO, keyword strategy. Use for SEO or organic traffic. Do NOT use for code review or architecture."
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
- chars: 647
- outline:
- ai-ugc-ads

```markdown
---
name: ai-ugc-ads
description: "UGC ad campaigns: creator recruitment, AI UGC content, scaling. Use for UGC or creator ads (Spark, Arcads). Do NOT use for code work."
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
- chars: 492
- outline:
- angular-20-expert

```markdown
---
name: angular-20-expert
description: "Implement, diagnose or modernize Angular 20 apps without other-major behavior. Use for Angular 20 work. Do NOT use for other stacks."
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
- chars: 574
- outline:
- angular-8-to-20-migration

```markdown
---
name: angular-8-to-20-migration
description: "Migrate Angular 8 to 20 one major per step, keeping UI and async behavior. Use for upgrades. Do NOT use for single-version code (angular-20-expert)."
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
- chars: 515
- outline:
- anti-hallucination-evaluator

```markdown
---
name: anti-hallucination-evaluator
description: "Anti-hallucination check of claims against inspected sources. Use for hallucination audits. Do NOT use as deployment approval."
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
- chars: 525
- outline:
- approval-governance-auditor

```markdown
---
name: approval-governance-auditor
description: "Validate approval scope, expiry, audit trail. Use when asked to audit approvals. Do NOT use outside authorized scope or to expose secrets."
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
- chars: 505
- outline:
- approval-requester

```markdown
---
name: approval-requester
description: "Determine approvals, create requests, track status. Use when asked to request approval. Do NOT use outside authorized scope or to expose secrets."
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
- chars: 563
- outline:
- architecturally-significant-requirement

```markdown
---
name: architecturally-significant-requirement
description: "Judge if a requirement is architecturally significant (ASR). Use for ASR triage. Do NOT use to write ADRs (architecture-decision-record)."
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
- chars: 531
- outline:
- architecture-decision-log

```markdown
---
name: architecture-decision-log
description: "Maintain the ADR log: next number, index, statuses, integrity. Use for ADR index work. Do NOT use to write one ADR (architecture-decision-record)."
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
- chars: 536
- outline:
- architecture-decision-record

```markdown
---
name: architecture-decision-record
description: "Write, supersede or review one ADR (MADR, Nygard, Y-statement) and lint it. Use when asked to record a decision. Do NOT use for the ADR index."
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
- chars: 557
- outline:
- architecture-knowledge-management

```markdown
---
name: architecture-knowledge-management
description: "Govern architecture knowledge: audit missing or stale decisions, recover legacy ones. Use for AKM gaps. Do NOT use for single ADRs or the log index."
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
- chars: 507
- outline:
- architecture-mapper

```markdown
---
name: architecture-mapper
description: "Map architecture from detected files and explicit evidence. Use when asked to map architecture. Do NOT use for implementation or deployment."
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
- chars: 515
- outline:
- atualizar-dependencias

```markdown
---
name: atualizar-dependencias
description: "Update dependencies with manifest/lockfile compatibility and regression evidence. Use for atualizar dependências. Do NOT use for deployment."
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
- chars: 511
- outline:
- automation-orchestrator

```markdown
---
name: automation-orchestrator
description: "Design idempotent multi-step automations from existing skills. Use for automation orchestration. Do NOT use for unapproved remote writes."
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
- chars: 513
- outline:
- aws-advisor

```markdown
---
name: aws-advisor
description: "AWS architecture, security, service choice and troubleshooting. Use for AWS or AWS services (Lambda, S3, IAM, CDK). Do NOT use for other clouds."
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
- chars: 506
- outline:
- best-practices

```markdown
---
name: best-practices
description: "Apply modern web security, compatibility and code-quality checks. Use for web best-practice reviews. Do NOT use for accessibility, SEO or full audits."
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
- chars: 514
- outline:
- blueprint-generator

```markdown
---
name: blueprint-generator
description: "Generate an evidence-based project blueprint: boundaries, components, data, gates. Use for blueprints. Do NOT use for implementation or deployment."
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
- chars: 486
- outline:
- bm25-expert

```markdown
---
name: bm25-expert
description: "Design, tune and evaluate BM25 and hybrid lexical retrieval. Use for BM25 or hybrid search work. Do NOT use for unrelated domains or deployment."
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
- chars: 515
- outline:
- camel-banking-expert

```markdown
---
name: camel-banking-expert
description: "Analyze and implement Apache Camel flows with banking-grade reliability and idempotency. Use for Camel banking flows. Do NOT use for other stacks."
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
- chars: 511
- outline:
- change-trace-auditor

```markdown
---
name: change-trace-auditor
description: "Audit change manifests and rollback plans so changes can be reviewed and reverted. Use for change-trace audits. Do NOT use as deployment approval."
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
- chars: 489
- outline:
- chromatic-mega-brain

```markdown
---
name: chromatic-mega-brain
description: "Maintain hierarchical memory and continuity files. Use to resume a project or update handoff. Do NOT use for fleet mapping."
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
- chars: 500
- outline:
- chrome-devtools

```markdown
---
name: chrome-devtools
description: "Debug and profile pages via Chrome DevTools MCP: console, network, performance. Use for 'debug this page'. Do NOT use for E2E (playwright-skill)."
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
- chars: 512
- outline:
- ci-quality-gate-engineer

```markdown
---
name: ci-quality-gate-engineer
description: "Create CI/CD quality gates for AEOS and target projects. Use when asked for CI quality gates. Do NOT use for production deployment."
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
- chars: 515
- outline:
- cloudflare-deploy

```markdown
---
name: cloudflare-deploy
description: "Deploy apps and infrastructure to Cloudflare (Workers, Pages). Use to deploy or host on Cloudflare. Do NOT use for Vercel, Netlify or Render."
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
- chars: 490
- outline:
- code-analyzer

```markdown
---
name: code-analyzer
description: "Analyze change impact and risks in code. Use for proposed changes. Do NOT use to mutate production or invent architecture without source evidence."
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
- chars: 488
- outline:
- codenavi

```markdown
---
name: codenavi
description: "Investigate unknown codebases and change them surgically. Use for bugs, features or unfamiliar flows. Do NOT use for greenfield, CI/CD or infra."
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
- chars: 518
- outline:
- coding-guidelines

```markdown
---
name: coding-guidelines
description: "Apply target repo coding conventions, with source evidence, before editing. Use for coding guidelines or style matching. Do NOT use for deployment."
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
- chars: 523
- outline:
- compatibility-analyzer

```markdown
---
name: compatibility-analyzer
description: "Analyze dependency compatibility: version conflicts, peer deps, platform limits, breaking changes. Use for compat checks. Do NOT use for deployment."
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
- chars: 528
- outline:
- compliance-audit-exporter

```markdown
---
name: compliance-audit-exporter
description: "Export a redacted audit package mapping controls to verified evidence and gaps. Use for compliance audit exports. Do NOT use as deployment approval."
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
- chars: 537
- outline:
- compliance-evidence-exporter

```markdown
---
name: compliance-evidence-exporter
description: "Export compliance evidence without leaking secrets. Use for compliance evidence exports. Do NOT use as deployment approval or for unexecuted checks."
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
- chars: 554
- outline:
- component-common-domain-detection

```markdown
---
name: component-common-domain-detection
description: "Find duplicated business logic across components. Use for overlap before refactoring. Do NOT use for dependencies (coupling-analysis)."
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
- chars: 549
- outline:
- component-flattening-analysis

```markdown
---
name: component-flattening-analysis
description: "Find misplaced classes and fix component hierarchy. Use for orphaned classes or flattening nested components. Do NOT use for domain grouping."
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
- chars: 562
- outline:
- component-identification-sizing

```markdown
---
name: component-identification-sizing
description: "Map components and measure their size to pick what to extract first. Use for module sizing. Do NOT use for runtime performance or capacity planning."
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
- chars: 501
- outline:
- conflict-detector

```markdown
---
name: conflict-detector
description: "Detect read/write, tool, approval and resource conflicts before parallel runs. Use before parallel work. Do NOT use for unapproved remote writes."
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
- chars: 528
- outline:
- confluence-assistant

```markdown
---
name: confluence-assistant
description: "Confluence operations via Atlassian MCP: search, create, update pages and comments. Use for Confluence requests. Do NOT use for Jira or local files."
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
- chars: 687
- outline:
- content-to-pipeline

```markdown
---
name: content-to-pipeline
description: "Turn content into pipeline: content-led GTM, distribution, repurposing. Use for content marketing or content-led growth. Do NOT use for code work."
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
- chars: 491
- outline:
- context-router

```markdown
---
name: context-router
description: "Resolve minimal context packets from task, LCPs and memory rules. Use for context packets. Do NOT use to promote unverified claims into memory."
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
- chars: 518
- outline:
- continuity-bootstrapper

```markdown
---
name: continuity-bootstrapper
description: "Bootstrap and validate the CodENavi quartet without inventing project state. Use for continuity setup. Do NOT use to promote unverified claims."
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
- chars: 499
- outline:
- core-web-vitals

```markdown
---
name: core-web-vitals
description: "Fix LCP, INP and CLS to current Google thresholds. Use for Core Web Vitals or layout shifts. Do NOT use for bundles (perf-web-optimization)."
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
- chars: 514
- outline:
- cost-token-optimizer

```markdown
---
name: cost-token-optimizer
description: "Optimize LLM and tool costs via context minimization and cache policy. Use for token cost reduction. Do NOT use to drop required evidence or checks."
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
- chars: 507
- outline:
- coupling-analysis

```markdown
---
name: coupling-analysis
description: "Analyze module coupling (strength, distance, volatility). Use for coupling reports. Do NOT use for domain boundaries (domain-analysis)."
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
- chars: 519
- outline:
- create-adr

```markdown
---
name: create-adr
description: "Create an ADR recording a made architectural decision and its rationale. Use for 'write an ADR'. Do NOT use for undecided choices (create-rfc)."
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
- chars: 524
- outline:
- create-rfc

```markdown
---
name: create-rfc
description: "Create RFCs to propose and decide significant changes with stakeholders. Use for 'write an RFC'. Do NOT use for TDDs (technical-design-doc-creator)."
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
- chars: 543
- outline:
- create-technical-design-doc

```markdown
---
name: create-technical-design-doc
description: "Create architecture-level technical design docs via discovery. Use for 'write a design doc' or 'criar um TDD'. Do NOT use for README or API docs."
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
- chars: 530
- outline:
- critical-thinking-governor

```markdown
---
name: critical-thinking-governor
description: "Governs AEOS runs with 20 internal critical-thinking lenses, never agent identities. Use for critical review. Do NOT use for unrelated domains."
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
- chars: 490
- outline:
- csharp-expert

```markdown
---
name: csharp-expert
description: "Write and review production C# on current .NET (C# 14, .NET 10). Use for C#, .NET, csproj or .cs work. Do NOT use for F#, VB or non-.NET code."
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
- chars: 532
- outline:
- cursor-subagent-creator

```markdown
---
name: cursor-subagent-creator
description: "Design Cursor work units: isolated workflows, verifiers, auditors. Use for isolated work units. Do NOT use for one-off skills or agent identities."
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
- chars: 537
- outline:
- cve-advisory-sync

```markdown
---
name: cve-advisory-sync
description: "Refresh an advisory dataset from authorized OSV/GHSA/NVD. Use for CVE base sync. Do NOT use for assessments (vuln-obsol-recon) or patching."
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
- chars: 534
- outline:
- cve-remediation

```markdown
---
name: cve-remediation
description: "Fix a known dependency CVE/GHSA with the smallest compatible change. Use for 'corrigir esta CVE'. Do NOT use for discovery (vuln-obsol-recon)."
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
- chars: 531
- outline:
- dark-videos-knowledge-base

```markdown
---
name: dark-videos-knowledge-base
description: "Navigate the dark-videos repo map; reconcile old paths with evidence. Use for 'mapa do dark-videos'. Do NOT use to claim inventory or publish."
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
- chars: 536
- outline:
- dark-videos-pipeline-expert

```markdown
---
name: dark-videos-pipeline-expert
description: "Run the dark-videos pipeline: mine, rank, frame, publish via dispatch. Use for shorts posting. Do NOT use for a second publisher or cookie export."
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
- chars: 538
- outline:
- database-architecture-planner

```markdown
---
name: database-architecture-planner
description: "Plan database architecture: schema governance, migrations, backup, restore. Use for DB planning. Do NOT use for implementation or deployment."
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
- chars: 561
- outline:
- decomposition-planning-roadmap

```markdown
---
name: decomposition-planning-roadmap
description: "Create decomposition plans and migration roadmaps for splitting monoliths. Use for extraction order. Do NOT use for domain analysis (domain-analysis)."
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
- chars: 492
- outline:
- delegation-auditor

```markdown
---
name: delegation-auditor
description: "Validate delegation against policy, scope, capabilities and risk. Use for delegation audits. Do NOT use for unapproved remote writes."
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
- chars: 490
- outline:
- demo

```markdown
---
name: demo
description: "Record a web app demo video (mp4 and telemetry) on a real desktop. Use for 'record a demo' or screencasts. Do NOT use for tests (playwright-skill)."
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
- chars: 508
- outline:
- dependency-analyzer

```markdown
---
name: dependency-analyzer
description: "Analyze dependencies, upgrade candidates, compatibility and risks. Use for dependency analysis or upgrade planning. Do NOT use for deployment."
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
- chars: 498
- outline:
- dependency-updater

```markdown
---
name: dependency-updater
description: "Update dependencies with minimal blast radius and evidence-backed compatibility. Use for dependency updates. Do NOT use for deployment."
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
- chars: 514
- outline:
- deploy-expert-unique

```markdown
---
name: deploy-expert-unique
description: "AIHealthResearch AWS deploy contract: branch promotion, OSV, CodeQL, validators. Use for AIHealthResearch deploys. Do NOT use for other projects."
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
- chars: 529
- outline:
- deployment-pipeline-expert

```markdown
---
name: deployment-pipeline-expert
description: "Map, diagnose and improve CI/CD and deployment pipelines safely. Use for pipeline diagnosis. Do NOT use for app features or unapproved prod changes."
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
- chars: 529
- outline:
- devops-pipeline-engineering

```markdown
---
name: devops-pipeline-engineering
description: "Governed DevOps, Git and Actions lifecycle: CI recovery, merge readiness. Use for DevOps or Actions work. Do NOT use for unapproved prod changes."
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
- chars: 472
- outline:
- diff-reviewer

```markdown
---
name: diff-reviewer
description: "Review generated diffs and patches for correctness, safety and evidence. Use for diff review. Do NOT use as deployment approval."
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
- chars: 524
- outline:
- docker-devcontainer-engineer

```markdown
---
name: docker-devcontainer-engineer
description: "Generate devcontainer and Docker artifacts in a sandbox. Use for devcontainer or Dockerfile work. Do NOT use for unapproved prod changes."
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
- chars: 497
- outline:
- docs-writer

```markdown
---
name: docs-writer
description: "Write, review and edit docs for structure, tone and accuracy. Use for docs or READMEs. Do NOT use for code comments or API reference generation."
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

### S077 | T1 | documentary-adversarial-judge

- path: `.agents/skills/documentary-adversarial-judge/SKILL.md`
- chars: 533
- outline:
- documentary-adversarial-judge

```markdown
---
name: documentary-adversarial-judge
description: "Adversarial judge of documentary packages: evidence scores, minimum 9.5. Use for julgar o vídeo. Do NOT use to write, mix or approve finally."
license: CC-BY-4.0
metadata:
  author: AEOS
  version: 1.0.0
  owner_agent: codenavi-agent
---

# documentary-adversarial-judge

Read and follow `00_skills/(tooling)/documentary-adversarial-judge/SKILL.md` and its relevant local modules.

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity.
```

### S078 | T1 | documentary-audio-engineer

- path: `.agents/skills/documentary-audio-engineer/SKILL.md`
- chars: 527
- outline:
- documentary-audio-engineer

```markdown
---
name: documentary-audio-engineer
description: "Mix documentary audio: narration and music ducking, -16 LUFS, -1.5 dBFS peak. Use to mix narration or fix loudness. Do NOT use for music choice."
license: CC-BY-4.0
metadata:
  author: AEOS
  version: 1.0.0
  owner_agent: codenavi-agent
---

# documentary-audio-engineer

Read and follow `00_skills/(tooling)/documentary-audio-engineer/SKILL.md` and its relevant local modules.

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity.
```

### S079 | T1 | documentary-factory

- path: `.agents/skills/documentary-factory/SKILL.md`
- chars: 510
- outline:
- documentary-factory

```markdown
---
name: documentary-factory
description: "Runs the documentary factory: six gated roles and a reject-restart loop. Use for full documentary production. Do NOT use for one role or publishing."
license: CC-BY-4.0
metadata:
  author: AEOS
  version: 1.0.0
  owner_agent: codenavi-agent
---

# documentary-factory

Read and follow `00_skills/(tooling)/documentary-factory/SKILL.md` and its relevant local modules.

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity.
```

### S080 | T1 | documentary-music-curator

- path: `.agents/skills/documentary-music-curator/SKILL.md`
- chars: 527
- outline:
- documentary-music-curator

```markdown
---
name: documentary-music-curator
description: "Select calm documentary music with verified license, no Content ID risk. Use for track licensing. Do NOT use for final mix or unlicensed downloads."
license: CC-BY-4.0
metadata:
  author: AEOS
  version: 1.0.0
  owner_agent: codenavi-agent
---

# documentary-music-curator

Read and follow `00_skills/(tooling)/documentary-music-curator/SKILL.md` and its relevant local modules.

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity.
```

### S081 | T1 | documentary-social-video-expert

- path: `.agents/skills/documentary-social-video-expert/SKILL.md`
- chars: 545
- outline:
- documentary-social-video-expert

```markdown
---
name: documentary-social-video-expert
description: "Publication pack: titles, chapters, thumbnails, vertical cuts. Use for YouTube/Reels metadata. Do NOT use to publish (dark-videos-pipeline-expert)."
license: CC-BY-4.0
metadata:
  author: AEOS
  version: 1.0.0
  owner_agent: codenavi-agent
---

# documentary-social-video-expert

Read and follow `00_skills/(tooling)/documentary-social-video-expert/SKILL.md` and its relevant local modules.

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity.
```

### S082 | T1 | documentary-subject-expert

- path: `.agents/skills/documentary-subject-expert/SKILL.md`
- chars: 531
- outline:
- documentary-subject-expert

```markdown
---
name: documentary-subject-expert
description: "Subject expert for documentaries: sourced facts, chapter arc, narration. Use for enredo, roteiro or chapters. Do NOT use to judge or acquire assets."
license: CC-BY-4.0
metadata:
  author: AEOS
  version: 1.0.0
  owner_agent: codenavi-agent
---

# documentary-subject-expert

Read and follow `00_skills/(tooling)/documentary-subject-expert/SKILL.md` and its relevant local modules.

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity.
```

### S083 | T1 | documentary-visual-curator

- path: `.agents/skills/documentary-visual-curator/SKILL.md`
- chars: 531
- outline:
- documentary-visual-curator

```markdown
---
name: documentary-visual-curator
description: "Source on-topic, watermark-free images and GIFs with verified licenses. Use for video visuals. Do NOT use to remove third-party watermarks (policy)."
license: CC-BY-4.0
metadata:
  author: AEOS
  version: 1.0.0
  owner_agent: codenavi-agent
---

# documentary-visual-curator

Read and follow `00_skills/(tooling)/documentary-visual-curator/SKILL.md` and its relevant local modules.

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity.
```

### S084 | T1 | documentation

- path: `.agents/skills/documentation/SKILL.md`
- chars: 489
- outline:
- documentation

```markdown
---
name: documentation
description: "Generate evidence-based documentation in a sandbox. Use for documentation requests. Do NOT use for production deployment or unrelated stacks."
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

### S085 | T1 | documentation-11-layer-mapper

- path: `.agents/skills/documentation-11-layer-mapper/SKILL.md`
- chars: 539
- outline:
- documentation-11-layer-mapper

```markdown
---
name: documentation-11-layer-mapper
description: "11-layer docs from source: purpose, flows, endpoints. Use for docs. Do NOT use to mutate production or invent architecture without source evidence."
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

### S086 | T1 | documentation-mapper

- path: `.agents/skills/documentation-mapper/SKILL.md`
- chars: 508
- outline:
- documentation-mapper

```markdown
---
name: documentation-mapper
description: "Verified enterprise docs from a repo. Use for repo doc mapping. Do NOT use to mutate production or invent architecture without source evidence."
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

### S087 | T1 | domain-analysis

- path: `.agents/skills/domain-analysis/SKILL.md`
- chars: 495
- outline:
- domain-analysis

```markdown
---
name: domain-analysis
description: "Map business domains and service boundaries with DDD strategy. Use for bounded contexts. Do NOT use to group existing components."
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

### S088 | T1 | domain-identification-grouping

- path: `.agents/skills/domain-identification-grouping/SKILL.md`
- chars: 554
- outline:
- domain-identification-grouping

```markdown
---
name: domain-identification-grouping
description: "Group existing components into domains for service planning. Use for component-to-domain mapping. Do NOT use for new domains (domain-analysis)."
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

### S089 | T1 | dynatrace-observability-staff

- path: `.agents/skills/dynatrace-observability-staff/SKILL.md`
- chars: 540
- outline:
- dynatrace-observability-staff

```markdown
---
name: dynatrace-observability-staff
description: "Dynatrace analysis: metrics, logs, traces, Davis problems. Use for Dynatrace investigations. Do NOT use to mutate live systems unless authorized."
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

### S090 | T1 | enterprise-repo-intelligence

- path: `.agents/skills/enterprise-repo-intelligence/SKILL.md`
- chars: 538
- outline:
- enterprise-repo-intelligence

```markdown
---
name: enterprise-repo-intelligence
description: "Map enterprise repos with budgets and evidence. Use for repo mapping. Do NOT use to mutate production or invent architecture without source evidence."
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

### S091 | T1 | enterprise-security-auditor

- path: `.agents/skills/enterprise-security-auditor/SKILL.md`
- chars: 528
- outline:
- enterprise-security-auditor

```markdown
---
name: enterprise-security-auditor
description: "Audit repo and integration security from trust boundaries. Use for security audits. Do NOT use outside authorized scope or to expose secrets."
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

### S092 | T1 | eol-advisory-sync

- path: `.agents/skills/eol-advisory-sync/SKILL.md`
- chars: 523
- outline:
- eol-advisory-sync

```markdown
---
name: eol-advisory-sync
description: "Refresh end-of-life metadata from endoflife.date and maintainers. Use for EOL base sync. Do NOT use for CVE sync or patching."
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

### S093 | T1 | evaluation-runner

- path: `.agents/skills/evaluation-runner/SKILL.md`
- chars: 497
- outline:
- evaluation-runner

```markdown
---
name: evaluation-runner
description: "Run a supplied evaluation suite; report reproducible results and gaps. Use for running a named eval suite. Do NOT use as deployment approval."
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

### S094 | T1 | evidence-cache-auditor

- path: `.agents/skills/evidence-cache-auditor/SKILL.md`
- chars: 515
- outline:
- evidence-cache-auditor

```markdown
---
name: evidence-cache-auditor
description: "Audit evidence cache keys, invalidation and stale-cache risks. Use for evidence cache audits. Do NOT use for unrelated stacks or deployment."
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

### S095 | T1 | evidence-integrity-engineer

- path: `.agents/skills/evidence-integrity-engineer/SKILL.md`
- chars: 526
- outline:
- evidence-integrity-engineer

```markdown
---
name: evidence-integrity-engineer
description: "Validate manifests, hash chains and tamper resistance. Use for evidence integrity checks. Do NOT use for unrelated stacks or deployment."
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

### S096 | T1 | evolutionary-modular-architecture

- path: `.agents/skills/evolutionary-modular-architecture/SKILL.md`
- chars: 589
- outline:
- evolutionary-modular-architecture

```markdown
---
name: evolutionary-modular-architecture
description: "Design modular monoliths: DDD contexts, ports and adapters, resilience. Use for platform design. Do NOT use for simple CRUD or tactical-ddd review."
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

### S097 | T1 | excalidraw-studio

- path: `.agents/skills/excalidraw-studio/SKILL.md`
- chars: 538
- outline:
- excalidraw-studio

```markdown
---
name: excalidraw-studio
description: "Generate .excalidraw diagrams from text: flowcharts, architecture, ER, sequence. Use for 'create a diagram'. Do NOT use for Mermaid (mermaid-studio)."
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

### S098 | T1 | expansion-retention

- path: `.agents/skills/expansion-retention/SKILL.md`
- chars: 675
- outline:
- expansion-retention

```markdown
---
name: expansion-retention
description: "Reduce churn and grow expansion revenue: NRR, upsell, customer success, renewals. Use for retention systems. Do NOT use for code work."
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

### S099 | T1 | fable

- path: `.agents/skills/fable/SKILL.md`
- chars: 473
- outline:
- fable

```markdown
---
name: fable
description: "Standard problem-solving loop: classify, gather evidence, act surgically, verify. Use for non-trivial tasks. Do NOT use for trivial one-step answers."
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

### S100 | T1 | fable-aeos-harness

- path: `.agents/skills/fable-aeos-harness/SKILL.md`
- chars: 511
- outline:
- fable-aeos-harness

```markdown
---
name: fable-aeos-harness
description: "Execution harness wrapping all AEOS skills with the Fable problem-solving loop. Use to run AEOS skills under Fable. Do NOT use for unrelated stacks."
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

### S101 | T1 | fable-domain

- path: `.agents/skills/fable-domain/SKILL.md`
- chars: 491
- outline:
- fable-domain

```markdown
---
name: fable-domain
description: "Research a domain and build a Fable adapter, flowchart, trap fixture and smoke eval. Use for new sector adapters. Do NOT use for unrelated stacks."
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

### S102 | T1 | fable-judge

- path: `.agents/skills/fable-judge/SKILL.md`
- chars: 488
- outline:
- fable-judge

```markdown
---
name: fable-judge
description: "Adversarial verification of finished work: reruns checks, catches false claims. Use for finished-work verification. Do NOT use as deployment approval."
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

### S103 | T1 | fable-loop

- path: `.agents/skills/fable-loop/SKILL.md`
- chars: 485
- outline:
- fable-loop

```markdown
---
name: fable-loop
description: "Multi-stage workflow: evidence lenses, one plan, surgical execution, verification. Use for complex multi-stage work. Do NOT use for trivial tasks."
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

### S104 | T1 | figma

- path: `.agents/skills/figma/SKILL.md`
- chars: 485
- outline:
- figma

```markdown
---
name: figma
description: "Fetch Figma context, screenshots and assets via MCP. Use for Figma URLs or node IDs. Do NOT use for pixel-perfect builds (figma-implement-design)."
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

### S105 | T1 | figma-implement-design

- path: `.agents/skills/figma-implement-design/SKILL.md`
- chars: 536
- outline:
- figma-implement-design

```markdown
---
name: figma-implement-design
description: "Translate Figma nodes into production code with 1:1 fidelity via Figma MCP. Use for Figma URLs to implement. Do NOT use for data fetching (figma)."
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

### S106 | T1 | fine-tuning-expert

- path: `.agents/skills/fine-tuning-expert/SKILL.md`
- chars: 498
- outline:
- fine-tuning-expert

```markdown
---
name: fine-tuning-expert
description: "Decide if fine-tuning is justified; build a governed training pipeline. Use for fine-tuning decisions. Do NOT use for unrelated stacks."
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

### S107 | T1 | fixture-corpus-validator

- path: `.agents/skills/fixture-corpus-validator/SKILL.md`
- chars: 512
- outline:
- fixture-corpus-validator

```markdown
---
name: fixture-corpus-validator
description: "Validate fixture corpus structure, provenance and expected-output contracts. Use for fixture checks. Do NOT use as deployment approval."
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

### S108 | T1 | fleet-mapping

- path: `.agents/skills/fleet-mapping/SKILL.md`
- chars: 533
- outline:
- fleet-mapping

```markdown
---
name: "fleet-mapping"
description: "Map sigla fleet dependencies. Use for mapear a sigla. Do NOT use to fix bugs, provision infra, mutate production or invent business rules."
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

### S109 | T1 | frontend-blueprint

- path: `.agents/skills/frontend-blueprint/SKILL.md`
- chars: 542
- outline:
- frontend-blueprint

```markdown
---
name: frontend-blueprint
description: "Discovery-first frontend design: references, tokens and brand before UI code. Use for building or redesigning UI. Do NOT use for backend or APIs."
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

### S110 | T1 | frontend-design

- path: `.agents/skills/frontend-design/SKILL.md`
- chars: 595
- outline:
- frontend-design

```markdown
---
name: frontend-design
description: "Create distinctive production UIs, avoiding generic AI looks. Use for pages or components. Do NOT use for design audits (web-design-guidelines)."
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

### S111 | T1 | gh-address-comments

- path: `.agents/skills/gh-address-comments/SKILL.md`
- chars: 590
- outline:
- gh-address-comments

```markdown
---
name: gh-address-comments
description: "Address review comments on the open GitHub PR of this branch via gh CLI. Use for 'address PR comments'. Do NOT use for CI debugging (gh-fix-ci)."
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

### S112 | T1 | gh-fix-ci

- path: `.agents/skills/gh-fix-ci/SKILL.md`
- chars: 502
- outline:
- gh-fix-ci

```markdown
---
name: gh-fix-ci
description: "Debug failing GitHub Actions PR checks; apply fixes only after approval. Use for failing checks. Do NOT use for review comments (gh-address-comments)."
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

### S113 | T1 | girl-voice-composer-simulation-expert

- path: `.agents/skills/girl-voice-composer-simulation-expert/SKILL.md`
- chars: 564
- outline:
- girl-voice-composer-simulation-expert

```markdown
---
name: girl-voice-composer-simulation-expert
description: "Direct TTS to synthesize a generic fictional child voice (6-8), pt-BR and en-US. Use for synthetic voice profiles. Do NOT use to clone a real child."
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

### S114 | T1 | github-operations

- path: `.agents/skills/github-operations/SKILL.md`
- chars: 489
- outline:
- github-operations

```markdown
---
name: github-operations
description: "Governed Git and GitHub operations: branches, PRs, workflows. Use for Git or GitHub actions. Do NOT use for unapproved remote writes."
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

### S115 | T1 | grafana-observability-staff

- path: `.agents/skills/grafana-observability-staff/SKILL.md`
- chars: 536
- outline:
- grafana-observability-staff

```markdown
---
name: grafana-observability-staff
description: "Grafana analysis: dashboards, Prometheus, Loki, Tempo, alerts. Use for Grafana investigations. Do NOT use to mutate live systems unless authorized."
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

### S116 | T1 | gtm-engineering

- path: `.agents/skills/gtm-engineering/SKILL.md`
- chars: 670
- outline:
- gtm-engineering

```markdown
---
name: gtm-engineering
description: "Build GTM automation: workflow architecture, AI agents, n8n/Make/Zapier. Use for GTM engineering. Do NOT use for code review or architecture."
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

### S117 | T1 | gtm-metrics

- path: `.agents/skills/gtm-metrics/SKILL.md`
- chars: 649
- outline:
- gtm-metrics

```markdown
---
name: gtm-metrics
description: "Define GTM metrics and dashboards: pipeline velocity, CAC, LTV, NRR, attribution. Use for GTM measurement. Do NOT use for code work."
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

### S118 | T1 | handoff-manager

- path: `.agents/skills/handoff-manager/SKILL.md`
- chars: 484
- outline:
- handoff-manager

```markdown
---
name: handoff-manager
description: "Maintain a concise .notebook/HANDOFF.md of the last verified state. Use for handoff updates. Do NOT use to promote unverified claims."
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

### S119 | T1 | harness-eval

- path: `.agents/skills/harness-eval/SKILL.md`
- chars: 521
- outline:
- harness-eval

```markdown
---
name: harness-eval
description: "Audit an agent harness (AGENTS.md, rules, skills) for broken paths and redundancy. Use for harness audits. Do NOT use for harness setup."
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

### S120 | T1 | impeccable

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

### S121 | T1 | incident-commander

- path: `.agents/skills/incident-commander/SKILL.md`
- chars: 503
- outline:
- incident-commander

```markdown
---
name: incident-commander
description: "Generate incident triage, rollback and postmortem artifacts. Use for incident artifacts. Do NOT use to mutate live systems unless authorized."
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

### S122 | T1 | incident-response-assistant

- path: `.agents/skills/incident-response-assistant/SKILL.md`
- chars: 520
- outline:
- incident-response-assistant

```markdown
---
name: incident-response-assistant
description: "Support human-led incident triage, RCA and recovery. Use for incident support. Do NOT use to mutate live systems unless authorized."
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

### S123 | T1 | java-11-expert

- path: `.agents/skills/java-11-expert/SKILL.md`
- chars: 496
- outline:
- java-11-expert

```markdown
---
name: java-11-expert
description: "Build and modernize Java 11 systems with Java 8-to-11 compatibility analysis. Use for Java 11 work. Do NOT use for other languages or deployment."
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

### S124 | T1 | java-17-expert

- path: `.agents/skills/java-17-expert/SKILL.md`
- chars: 473
- outline:
- java-17-expert

```markdown
---
name: java-17-expert
description: "Implement and migrate LTS Java 17 applications safely. Use for Java 17 work. Do NOT use for other languages or deployment."
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

### S125 | T1 | java-21-expert

- path: `.agents/skills/java-21-expert/SKILL.md`
- chars: 499
- outline:
- java-21-expert

```markdown
---
name: java-21-expert
description: "Design and implement Java 21 systems and migrations with LTS-aware verification. Use for Java 21 work. Do NOT use for other languages or deployment."
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

### S126 | T1 | java-25-expert

- path: `.agents/skills/java-25-expert/SKILL.md`
- chars: 490
- outline:
- java-25-expert

```markdown
---
name: java-25-expert
description: "Build or migrate Java 25 projects using only APIs verified for toolchain and runtime. Use for Java 25 work. Do NOT use for other languages."
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

### S127 | T1 | java-26-expert

- path: `.agents/skills/java-26-expert/SKILL.md`
- chars: 495
- outline:
- java-26-expert

```markdown
---
name: java-26-expert
description: "Build or migrate Java 26 projects; handle preview status and verify runtime compatibility. Use for Java 26 work. Do NOT use for other languages."
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

### S128 | T1 | java-8-expert

- path: `.agents/skills/java-8-expert/SKILL.md`
- chars: 491
- outline:
- java-8-expert

```markdown
---
name: java-8-expert
description: "Implement, diagnose and modernize Java 8 systems without later-version APIs. Use for Java 8 work. Do NOT use for other languages or deployment."
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

### S129 | T1 | java-bug-solver

- path: `.agents/skills/java-bug-solver/SKILL.md`
- chars: 501
- outline:
- java-bug-solver

```markdown
---
name: java-bug-solver
description: "Analyze Java stack traces, find root causes, validate fixes, keep lessons. Use for Java stack traces. Do NOT use for other languages or deployment."
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

### S130 | T1 | java-bug-solver-skill

- path: `.agents/skills/java-bug-solver-skill/SKILL.md`
- chars: 518
- outline:
- java-bug-solver-skill

```markdown
---
name: java-bug-solver-skill
description: "Create a Java bug-solver skill that analyzes stack traces and validates fixes. Use for creating a Java bug solver. Do NOT use for other languages."
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

### S131 | T1 | java-enterprise-modernizer

- path: `.agents/skills/java-enterprise-modernizer/SKILL.md`
- chars: 534
- outline:
- java-enterprise-modernizer

```markdown
---
name: java-enterprise-modernizer
description: "Analyze Java/Spring enterprise modernization opportunities safely. Use for Java/Spring modernization. Do NOT use for other languages or deployment."
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

### S132 | T1 | java-expert

- path: `.agents/skills/java-expert/SKILL.md`
- chars: 478
- outline:
- java-expert

```markdown
---
name: java-expert
description: "Implement, diagnose and migrate Java projects with version-correct APIs and evidence. Use for Java work. Do NOT use for other languages."
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

### S133 | T1 | java-migration

- path: `.agents/skills/java-migration/SKILL.md`
- chars: 497
- outline:
- java-migration

```markdown
---
name: java-migration
description: "Analyze Java projects and perform version migrations, API replacements and build updates. Use for Java migrations. Do NOT use for other languages."
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

### S134 | T1 | java-version-expert

- path: `.agents/skills/java-version-expert/SKILL.md`
- chars: 508
- outline:
- java-version-expert

```markdown
---
name: java-version-expert
description: "Route Java work to the exact verified JDK profile, loading only needed knowledge. Use for JDK version routing. Do NOT use for other languages."
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

### S135 | T1 | javascript-expert

- path: `.agents/skills/javascript-expert/SKILL.md`
- chars: 506
- outline:
- javascript-expert

```markdown
---
name: javascript-expert
description: "Implement, diagnose and modernize JavaScript with exact runtime and module compatibility. Use for JavaScript work. Do NOT use for other languages."
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

### S136 | T1 | jev-call-expert

- path: `.agents/skills/jev-call-expert/SKILL.md`
- chars: 502
- outline:
- jev-call-expert

```markdown
---
name: jev-call-expert
description: "Design and review TypeSafe Jev function calling with typed signatures. Use for Jev calls. Do NOT use for generic tool calling or unapproved actions."
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

### S137 | T1 | jira-assistant

- path: `.agents/skills/jira-assistant/SKILL.md`
- chars: 507
- outline:
- jira-assistant

```markdown
---
name: jira-assistant
description: "Manage Jira issues via Atlassian MCP: search, create, update, transition. Use for Jira tickets. Do NOT use for Confluence (confluence-assistant)."
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

### S138 | T1 | jira-confluence-assistant

- path: `.agents/skills/jira-confluence-assistant/SKILL.md`
- chars: 527
- outline:
- jira-confluence-assistant

```markdown
---
name: jira-confluence-assistant
description: "Prepare governed Jira/Confluence work with traceability to code and evidence. Use for Jira/Confluence tracing. Do NOT use for unrelated stacks."
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

### S139 | T1 | jira-time-entry-assistant

- path: `.agents/skills/jira-time-entry-assistant/SKILL.md`
- chars: 525
- outline:
- jira-time-entry-assistant

```markdown
---
name: jira-time-entry-assistant
description: "Prepare auditable Jira worklog proposals from actual task evidence. Use for Jira time entries. Do NOT use for unrelated stacks or deployment."
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

### S140 | T1 | judge-benchmark-runner

- path: `.agents/skills/judge-benchmark-runner/SKILL.md`
- chars: 510
- outline:
- judge-benchmark-runner

```markdown
---
name: judge-benchmark-runner
description: "Benchmark a deterministic Judge gate against a supplied corpus and thresholds. Use for Judge benchmarks. Do NOT use as deployment approval."
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

### S141 | T1 | kinghost-backup-recovery-expert

- path: `.agents/skills/kinghost-backup-recovery-expert/SKILL.md`
- chars: 538
- outline:
- kinghost-backup-recovery-expert

```markdown
---
name: kinghost-backup-recovery-expert
description: "Governed KingHost backup and rollback-safe restore: sites, databases, email. Use for KingHost backups. Do NOT use for unapproved prod changes."
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

### S142 | T1 | kinghost-clone-site-expert

- path: `.agents/skills/kinghost-clone-site-expert/SKILL.md`
- chars: 530
- outline:
- kinghost-clone-site-expert

```markdown
---
name: kinghost-clone-site-expert
description: "Governed KingHost site clone via verified FTP copy, never mutating the origin. Use for KingHost clones. Do NOT use for unapproved production changes."
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

### S143 | T1 | kinghost-database-expert

- path: `.agents/skills/kinghost-database-expert/SKILL.md`
- chars: 526
- outline:
- kinghost-database-expert

```markdown
---
name: kinghost-database-expert
description: "Governed KingHost MySQL work: access, backup, query analysis, migration, recovery. Use for KingHost databases. Do NOT use for unrelated changes."
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

### S144 | T1 | kinghost-domain-dns-ssl-expert

- path: `.agents/skills/kinghost-domain-dns-ssl-expert/SKILL.md`
- chars: 541
- outline:
- kinghost-domain-dns-ssl-expert

```markdown
---
name: kinghost-domain-dns-ssl-expert
description: "Governed KingHost domain, DNS and SSL changes with snapshot and rollback. Use for KingHost DNS or SSL. Do NOT use for unapproved production changes."
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

### S145 | T1 | kinghost-email-expert

- path: `.agents/skills/kinghost-email-expert/SKILL.md`
- chars: 512
- outline:
- kinghost-email-expert

```markdown
---
name: kinghost-email-expert
description: "Governed KingHost email: mailboxes, DNS/MX, webmail, recovery, no secret exposure. Use for KingHost email. Do NOT use for unapproved prod changes."
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

### S146 | T1 | kinghost-expert

- path: `.agents/skills/kinghost-expert/SKILL.md`
- chars: 493
- outline:
- kinghost-expert

```markdown
---
name: kinghost-expert
description: "KingHost hosting super-skill: domains, FTP/SSH publish, WordPress, MySQL, backups. Use for KingHost work. Do NOT use for unapproved prod changes."
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

### S147 | T1 | kinghost-performance-expert

- path: `.agents/skills/kinghost-performance-expert/SKILL.md`
- chars: 526
- outline:
- kinghost-performance-expert

```markdown
---
name: kinghost-performance-expert
description: "Measured KingHost performance: resources, cache, PHP runtime, PageSpeed. Use for KingHost performance. Do NOT use for unapproved prod changes."
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

### S148 | T1 | kinghost-security-expert

- path: `.agents/skills/kinghost-security-expert/SKILL.md`
- chars: 518
- outline:
- kinghost-security-expert

```markdown
---
name: kinghost-security-expert
description: "KingHost security: malware scans, quarantine, WAF, SSL. Use for KingHost security. Do NOT use outside authorized scope or to expose secrets."
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

### S149 | T1 | kinghost-site-publish-ftp-expert

- path: `.agents/skills/kinghost-site-publish-ftp-expert/SKILL.md`
- chars: 543
- outline:
- kinghost-site-publish-ftp-expert

```markdown
---
name: kinghost-site-publish-ftp-expert
description: "Governed KingHost WordPress/PHP FTP publish with backup and rollback. Use for KingHost publishing. Do NOT use for unapproved production changes."
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

### S150 | T1 | kotlin-expert

- path: `.agents/skills/kotlin-expert/SKILL.md`
- chars: 467
- outline:
- kotlin-expert

```markdown
---
name: kotlin-expert
description: "Design and implement Kotlin systems on the current stable release. Use for Kotlin work. Do NOT use for other languages."
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

### S151 | T1 | kubernetes-code-context-mapper

- path: `.agents/skills/kubernetes-code-context-mapper/SKILL.md`
- chars: 535
- outline:
- kubernetes-code-context-mapper

```markdown
---
name: kubernetes-code-context-mapper
description: "Map Kubernetes workloads, services and logs back to repo code and owners. Use for K8s-to-code mapping. Do NOT use for unapproved prod changes."
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

### S152 | T1 | kubernetes-observability-staff

- path: `.agents/skills/kubernetes-observability-staff/SKILL.md`
- chars: 539
- outline:
- kubernetes-observability-staff

```markdown
---
name: kubernetes-observability-staff
description: "Kubernetes observability: health, workloads, events, probes. Use for K8s investigations. Do NOT use to mutate live systems unless authorized."
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

### S153 | T1 | laya-expert

- path: `.agents/skills/laya-expert/SKILL.md`
- chars: 482
- outline:
- laya-expert

```markdown
---
name: laya-expert
description: "Implement calibrated typed decisions with the Laya SDK. Use for Laya decisions or RLCD training. Do NOT use for open-ended text or GraphRAG."
license: CC-BY-4.0
metadata:
  author: AEOS
  version: 0.1.0
  owner_agent: codenavi-agent
---

# laya-expert

Read and follow `00_skills/(development)/laya-expert/SKILL.md` and its relevant local modules.

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity.
```

### S154 | T1 | lead-enrichment

- path: `.agents/skills/lead-enrichment/SKILL.md`
- chars: 671
- outline:
- lead-enrichment

```markdown
---
name: lead-enrichment
description: "Lead enrichment waterfalls, ICP scoring and contact verification (Clay, Apollo). Use for enrichment or lead scoring. Do NOT use for code work."
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

### S155 | T1 | learning-curator

- path: `.agents/skills/learning-curator/SKILL.md`
- chars: 497
- outline:
- learning-curator

```markdown
---
name: learning-curator
description: "Promote verified, reusable engineering lessons into .notebook/LEARNING.md. Use for learning promotion. Do NOT use to promote unverified claims."
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

### S156 | T1 | learning-opportunities

- path: `.agents/skills/learning-opportunities/SKILL.md`
- chars: 526
- outline:
- learning-opportunities

```markdown
---
name: "learning-opportunities"
description: "Identify reusable lessons and promotion candidates from finished work. Use for session reviews. Do NOT use to write continuity files."
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

### S157 | T1 | legacy-migration-planner

- path: `.agents/skills/legacy-migration-planner/SKILL.md`
- chars: 573
- outline:
- legacy-migration-planner

```markdown
---
name: "legacy-migration-planner"
description: "Plan legacy migrations, strangler-fig rewrites and framework upgrades. Use for migration strategy. Do NOT use for domain analysis (domain-analysis)."
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

### S158 | T1 | legacy-risk-mapper

- path: `.agents/skills/legacy-risk-mapper/SKILL.md`
- chars: 512
- outline:
- legacy-risk-mapper

```markdown
---
name: legacy-risk-mapper
description: "Map legacy risks, modernization blockers and migration strategy. Use for legacy risk mapping. Do NOT use for unrelated implementation or deployment."
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

### S159 | T1 | llm-calibration-temperature-expert

- path: `.agents/skills/llm-calibration-temperature-expert/SKILL.md`
- chars: 554
- outline:
- llm-calibration-temperature-expert

```markdown
---
name: llm-calibration-temperature-expert
description: "Engineer LLM decoding and calibration behavior instead of tuning temperature blindly. Use for LLM calibration. Do NOT use for unrelated stacks."
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

### S160 | T1 | llm-model-selection-expert

- path: `.agents/skills/llm-model-selection-expert/SKILL.md`
- chars: 528
- outline:
- llm-model-selection-expert

```markdown
---
name: llm-model-selection-expert
description: "Select the best current model for a workload, using live capability data and evals. Use for model selection. Do NOT use for unrelated stacks."
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

### S161 | T1 | local-secret-vault

- path: `.agents/skills/local-secret-vault/SKILL.md`
- chars: 516
- outline:
- local-secret-vault

```markdown
---
name: "local-secret-vault"
description: "Read authorized local credential vaults, exposing only masked metadata. Use for local vault access. Do NOT use outside scope or to expose secrets."
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

### S162 | T1 | lora-qlora-dora-expert

- path: `.agents/skills/lora-qlora-dora-expert/SKILL.md`
- chars: 499
- outline:
- lora-qlora-dora-expert

```markdown
---
name: lora-qlora-dora-expert
description: "Implement LoRA, QLoRA or DoRA fine-tuning with reproducible experiments. Use for PEFT work. Do NOT use for unrelated stacks."
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

### S163 | T1 | mantis-architecture

- path: `.agents/skills/mantis-architecture/SKILL.md`
- chars: 511
- outline:
- mantis-architecture

```markdown
---
name: mantis-architecture
description: "Build the Mantis knowledge base (architecture, entities, vulnerabilities). Use at the start of a review loop. Do NOT use for threat models or plans."
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

### S164 | T1 | mantis-calibrate

- path: `.agents/skills/mantis-calibrate/SKILL.md`
- chars: 499
- outline:
- mantis-calibrate

```markdown
---
name: mantis-calibrate
description: "Calculate final risk scores from evidence and architectural impact. Use when findings are processed. Do NOT use to find vulnerabilities or patch."
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

### S165 | T1 | mantis-chain

- path: `.agents/skills/mantis-chain/SKILL.md`
- chars: 474
- outline:
- mantis-chain

```markdown
---
name: mantis-chain
description: "Combine validated findings into exploit chains that raise impact. Use after validation. Do NOT use for initial audits or patch code."
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

### S166 | T1 | mantis-critic

- path: `.agents/skills/mantis-critic/SKILL.md`
- chars: 485
- outline:
- mantis-critic

```markdown
---
name: mantis-critic
description: "Assess production viability of validated findings, filtering debug-only paths. Use for release-build triggerability. Do NOT use for patches."
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

### S167 | T1 | mantis-dedupe

- path: `.agents/skills/mantis-dedupe/SKILL.md`
- chars: 492
- outline:
- mantis-dedupe

```markdown
---
name: mantis-dedupe
description: "Consolidate raw security findings to remove redundant reports. Use before review of raw findings. Do NOT use for auditing code or patch generation."
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

### S168 | T1 | mantis-history

- path: `.agents/skills/mantis-history/SKILL.md`
- chars: 480
- outline:
- mantis-history

```markdown
---
name: mantis-history
description: "Mine VCS history for past vulnerabilities and fixes. Use as first Mantis pre-processing step. Do NOT use for code review or patches."
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

### S169 | T1 | mantis-meta-agent

- path: `.agents/skills/mantis-meta-agent/SKILL.md`
- chars: 487
- outline:
- mantis-meta-agent

```markdown
---
name: mantis-meta-agent
description: "Supervise a long-running automated security review campaign. Use for autonomous campaigns. Do NOT use to run single review stages."
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

### S170 | T1 | mantis-patch

- path: `.agents/skills/mantis-patch/SKILL.md`
- chars: 482
- outline:
- mantis-patch

```markdown
---
name: mantis-patch
description: "Generate minimal security fixes in isolated copies, then apply and verify. Use for reproduced findings. Do NOT use for research or payloads."
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

### S171 | T1 | mantis-pipeline-adapter

- path: `.agents/skills/mantis-pipeline-adapter/SKILL.md`
- chars: 513
- outline:
- mantis-pipeline-adapter

```markdown
---
name: mantis-pipeline-adapter
description: "Design custom deterministic harnesses that wrap Mantis skills. Use for building your own pipeline. Do NOT use to run the default pipeline."
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

### S172 | T1 | mantis-plan

- path: `.agents/skills/mantis-plan/SKILL.md`
- chars: 483
- outline:
- mantis-plan

```markdown
---
name: mantis-plan
description: "Formulate a targeted defensive review plan from the threat model and learnings. Use when starting a campaign. Do NOT use for reviews or patches."
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

### S173 | T1 | mantis-reflect

- path: `.agents/skills/mantis-reflect/SKILL.md`
- chars: 493
- outline:
- mantis-reflect

```markdown
---
name: mantis-reflect
description: "Extract learnings from finished review runs: successes, failures, false assumptions. Use for Mantis reflection. Do NOT use for source or patches."
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

### S174 | T1 | mantis-report

- path: `.agents/skills/mantis-report/SKILL.md`
- chars: 488
- outline:
- mantis-report

```markdown
---
name: mantis-report
description: "Generate a stakeholder security review packet from confirmed findings. Use at the end of a review cycle. Do NOT use for audits or patch checks."
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

### S175 | T1 | mantis-reproduce

- path: `.agents/skills/mantis-reproduce/SKILL.md`
- chars: 485
- outline:
- mantis-reproduce

```markdown
---
name: mantis-reproduce
description: "Write and run crash reproducers to verify security flaws. Use when viable findings exist. Do NOT use for code auditing or patching."
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

### S176 | T1 | mantis-researcher

- path: `.agents/skills/mantis-researcher/SKILL.md`
- chars: 503
- outline:
- mantis-researcher

```markdown
---
name: mantis-researcher
description: "Audit production source files per the review plan with static analysis and deep dives. Use when a plan exists. Do NOT use for planning or patches."
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

### S177 | T1 | mantis-review

- path: `.agents/skills/mantis-review/SKILL.md`
- chars: 489
- outline:
- mantis-review

```markdown
---
name: mantis-review
description: "Independently review findings and filter false positives against source. Use for source validation of findings. Do NOT use for repro or patches."
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

### S178 | T1 | mantis-structural-index

- path: `.agents/skills/mantis-structural-index/SKILL.md`
- chars: 509
- outline:
- mantis-structural-index

```markdown
---
name: mantis-structural-index
description: "Build a content-addressed semantic index of source units. Use when a pinned codebase is available. Do NOT use for findings or patches."
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

### S179 | T1 | mantis-summarize

- path: `.agents/skills/mantis-summarize/SKILL.md`
- chars: 486
- outline:
- mantis-summarize

```markdown
---
name: mantis-summarize
description: "Generate security summaries per directory before planning. Use at the start of a review campaign. Do NOT use for reviews or patches."
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

### S180 | T1 | mantis-threat-model

- path: `.agents/skills/mantis-threat-model/SKILL.md`
- chars: 501
- outline:
- mantis-threat-model

```markdown
---
name: mantis-threat-model
description: "Synthesize trust boundaries, attack surfaces and attackers into a living threat model. Use for KB stage B. Do NOT use for source analysis."
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

### S181 | T1 | marketplace-curator

- path: `.agents/skills/marketplace-curator/SKILL.md`
- chars: 510
- outline:
- marketplace-curator

```markdown
---
name: marketplace-curator
description: "Curate capability listings by provenance, licensing, scope and compatibility. Use for marketplace curation. Do NOT use for unapproved remote writes."
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

### S182 | T1 | mcp-discovery

- path: `.agents/skills/mcp-discovery/SKILL.md`
- chars: 479
- outline:
- mcp-discovery

```markdown
---
name: mcp-discovery
description: "Discover and validate MCP tools and capabilities against AEOS policies. Use for MCP discovery. Do NOT use for unapproved remote writes."
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

### S183 | T1 | mcp-health-check

- path: `.agents/skills/mcp-health-check/SKILL.md`
- chars: 491
- outline:
- mcp-health-check

```markdown
---
name: mcp-health-check
description: "Validate MCP runtime health, tools, capabilities and security posture. Use for MCP health checks. Do NOT use for unapproved remote writes."
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

### S184 | T1 | mcp-poisoning-evaluator

- path: `.agents/skills/mcp-poisoning-evaluator/SKILL.md`
- chars: 522
- outline:
- mcp-poisoning-evaluator

```markdown
---
name: mcp-poisoning-evaluator
description: "Evaluate MCP descriptions and responses for injection and poisoning. Use for MCP reviews. Do NOT use outside authorized scope or to expose secrets."
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

### S185 | T1 | mcp-risk-controller

- path: `.agents/skills/mcp-risk-controller/SKILL.md`
- chars: 492
- outline:
- mcp-risk-controller

```markdown
---
name: mcp-risk-controller
description: "Audit MCPs, tool descriptions, capabilities and poisoning risks. Use for MCP risk audits. Do NOT use for unapproved remote writes."
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

### S186 | T1 | memory-curator

- path: `.agents/skills/memory-curator/SKILL.md`
- chars: 496
- outline:
- memory-curator

```markdown
---
name: memory-curator
description: "Curate durable, evidence-backed memory in .notebook/MEMORY.md. Use for memory curation. Do NOT use to promote unverified claims or transient status."
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

### S187 | T1 | memory-governance-auditor

- path: `.agents/skills/memory-governance-auditor/SKILL.md`
- chars: 525
- outline:
- memory-governance-auditor

```markdown
---
name: memory-governance-auditor
description: "Audit memory reads and writes for evidence, scope and secret safety. Use for memory audits. Do NOT use to promote unverified claims into memory."
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

### S188 | T1 | mermaid-studio

- path: `.agents/skills/mermaid-studio/SKILL.md`
- chars: 529
- outline:
- mermaid-studio

```markdown
---
name: mermaid-studio
description: "Create, validate and render Mermaid diagrams (SVG, PNG, ASCII). Use for diagrams or mermaid files. Do NOT use for chart plotting or image generation."
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

### S189 | T1 | modular-decomposition

- path: `.agents/skills/modular-decomposition/SKILL.md`
- chars: 509
- outline:
- modular-decomposition

```markdown
---
name: modular-decomposition
description: "Monolith-to-modular pipeline: sizing, duplication, hierarchy, coupling. Use for splitting monoliths. Do NOT use for roadmaps."
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

### S190 | T1 | modular-design-principles

- path: `.agents/skills/modular-design-principles/SKILL.md`
- chars: 545
- outline:
- modular-design-principles

```markdown
---
name: modular-design-principles
description: "Modular design principles: bounded contexts, boundaries, contracts, splits. Use for module structure reviews. Do NOT use for decomposition pipelines."
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

### S191 | T1 | motion-comic-animation-expert

- path: `.agents/skills/motion-comic-animation-expert/SKILL.md`
- chars: 542
- outline:
- motion-comic-animation-expert

```markdown
---
name: motion-comic-animation-expert
description: "Motion Comic animation in Python and FFmpeg: camera, layers, parallax. Use for animar camadas or timeline HQ. Do NOT use to promise unrendered output."
license: CC-BY-4.0
metadata:
  author: AEOS
  version: 0.2.0
  owner_agent: codenavi-agent
---

# motion-comic-animation-expert

Read and follow `00_skills/(tooling)/motion-comic-animation-expert/SKILL.md` and its relevant local modules.

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity.
```

### S192 | T1 | motion-comic-art-expert

- path: `.agents/skills/motion-comic-art-expert/SKILL.md`
- chars: 522
- outline:
- motion-comic-art-expert

```markdown
---
name: motion-comic-art-expert
description: "Arte HQ científica em camadas. Use for storyboards ou bíblia visual. Do NOT use para chamar imagem única de animação ou inventar referência anexada."
license: CC-BY-4.0
metadata:
  author: AEOS
  version: 0.2.0
  owner_agent: codenavi-agent
---

# motion-comic-art-expert

Read and follow `00_skills/(tooling)/motion-comic-art-expert/SKILL.md` and its relevant local modules.

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity.
```

### S193 | T1 | multi-platform-launch

- path: `.agents/skills/multi-platform-launch/SKILL.md`
- chars: 680
- outline:
- multi-platform-launch

```markdown
---
name: multi-platform-launch
description: "Plan and run multi-platform product launches: Product Hunt, waitlists, launch day. Use for launch strategy. Do NOT use for code work."
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

### S194 | T1 | multirepo-ecosystem-mapper

- path: `.agents/skills/multirepo-ecosystem-mapper/SKILL.md`
- chars: 528
- outline:
- multirepo-ecosystem-mapper

```markdown
---
name: multirepo-ecosystem-mapper
description: "Map multi-repo ecosystems and owners. Use for multi-repo mapping. Do NOT use to mutate production or invent architecture without source evidence."
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

### S195 | T1 | nestjs-modular-monolith

- path: `.agents/skills/nestjs-modular-monolith/SKILL.md`
- chars: 542
- outline:
- nestjs-modular-monolith

```markdown
---
name: nestjs-modular-monolith
description: "Design NestJS modular monoliths with DDD, CQRS and clean architecture. Use for NestJS bounded contexts. Do NOT use for simple CRUD."
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

### S196 | T1 | netlify-deploy

- path: `.agents/skills/netlify-deploy/SKILL.md`
- chars: 507
- outline:
- netlify-deploy

```markdown
---
name: netlify-deploy
description: "Deploy web projects to Netlify via the CLI, including previews. Use for Netlify deploys or links. Do NOT use for Vercel, Cloudflare or Render."
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

### S197 | T1 | not-your-babysitter

- path: `.agents/skills/not-your-babysitter/SKILL.md`
- chars: 514
- outline:
- not-your-babysitter

```markdown
---
name: not-your-babysitter
description: "Autonomous operator: drive tasks to verified results, evidence-or-stop. Use for autonomous runs. Do NOT use for tutorials or brainstorms."
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

### S198 | T1 | notebook-intelligence

- path: `.agents/skills/notebook-intelligence/SKILL.md`
- chars: 499
- outline:
- notebook-intelligence

```markdown
---
name: notebook-intelligence
description: "Maintain compact, fresh project intelligence in .notebook/. Use for notebook maintenance. Do NOT use to promote unverified claims."
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

### S199 | T1 | nx-ci-monitor

- path: `.agents/skills/nx-ci-monitor/SKILL.md`
- chars: 485
- outline:
- nx-ci-monitor

```markdown
---
name: nx-ci-monitor
description: "Monitor Nx Cloud CI status and handle self-healing fixes. Use for 'watch CI' on Nx. Do NOT use for local task runs (nx-run-tasks)."
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

### S200 | T1 | nx-generate

- path: `.agents/skills/nx-generate/SKILL.md`
- chars: 487
- outline:
- nx-generate

```markdown
---
name: nx-generate
description: "Scaffold code with Nx generators: projects, libraries, features. Use for 'nx generate' tasks. Do NOT use for running tasks (nx-run-tasks)."
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

### S201 | T1 | nx-run-tasks

- path: `.agents/skills/nx-run-tasks/SKILL.md`
- chars: 502
- outline:
- nx-run-tasks

```markdown
---
name: nx-run-tasks
description: "Run Nx build, test, lint, serve and affected tasks in a workspace. Use for 'run tests' or 'nx affected'. Do NOT use for code generation (nx-generate)."
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

### S202 | T1 | nx-workspace

- path: `.agents/skills/nx-workspace/SKILL.md`
- chars: 502
- outline:
- nx-workspace

```markdown
---
name: nx-workspace
description: "Configure and optimize Nx monorepos: boundaries, affected analysis, caching, CI. Use for Nx workspace setup. Do NOT use to run tasks or generate code."
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

### S203 | T1 | observability-architect

- path: `.agents/skills/observability-architect/SKILL.md`
- chars: 511
- outline:
- observability-architect

```markdown
---
name: observability-architect
description: "Design logs, traces, metrics, dashboards, alerting. Use for observability design. Do NOT use to mutate live systems unless authorized."
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

### S204 | T1 | observability-reporter

- path: `.agents/skills/observability-reporter/SKILL.md`
- chars: 524
- outline:
- observability-reporter

```markdown
---
name: observability-reporter
description: "Generate timelines, metrics, trace summaries and failure analysis. Use for observability reports. Do NOT use to mutate live systems unless authorized."
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

### S205 | T1 | observability-root-cause-integrator

- path: `.agents/skills/observability-root-cause-integrator/SKILL.md`
- chars: 559
- outline:
- observability-root-cause-integrator

```markdown
---
name: observability-root-cause-integrator
description: "Merge observability and code evidence into a root-cause plan. Use for root-cause integration. Do NOT use to mutate live systems unless authorized."
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

### S206 | T1 | openshift-observability-staff

- path: `.agents/skills/openshift-observability-staff/SKILL.md`
- chars: 536
- outline:
- openshift-observability-staff

```markdown
---
name: openshift-observability-staff
description: "OpenShift observability: monitoring, alerts, logging, operators. Use for OpenShift work. Do NOT use to mutate live systems unless authorized."
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

### S207 | T1 | pack-marketplace-auditor

- path: `.agents/skills/pack-marketplace-auditor/SKILL.md`
- chars: 525
- outline:
- pack-marketplace-auditor

```markdown
---
name: pack-marketplace-auditor
description: "Audit pack marketplace quarantine, staging, active packs and trust policy. Use for pack marketplace audits. Do NOT use for unapproved remote writes."
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

### S208 | T1 | package-trust-engineer

- path: `.agents/skills/package-trust-engineer/SKILL.md`
- chars: 513
- outline:
- package-trust-engineer

```markdown
---
name: package-trust-engineer
description: "Verify packages, manifests, quarantine and promotion. Use for package trust checks. Do NOT use outside authorized scope or to expose secrets."
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

### S209 | T1 | packaging

- path: `.agents/skills/packaging/SKILL.md`
- chars: 467
- outline:
- packaging

```markdown
---
name: packaging
description: "Create, inspect and verify AEOS packages with manifests and checksums. Use for packaging work. Do NOT use for unapproved remote writes."
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

### S210 | T1 | paid-creative-ai

- path: `.agents/skills/paid-creative-ai/SKILL.md`
- chars: 661
- outline:
- paid-creative-ai

```markdown
---
name: paid-creative-ai
description: "AI paid ad creative: generation, testing, fatigue, ROAS. Use for ad creative or Meta/Google/TikTok ads. Do NOT use for code work."
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

### S211 | T1 | parallel-scheduler

- path: `.agents/skills/parallel-scheduler/SKILL.md`
- chars: 505
- outline:
- parallel-scheduler

```markdown
---
name: parallel-scheduler
description: "Create deterministic safe schedules for playbook tasks from dependency sets. Use for parallel scheduling. Do NOT use for unapproved remote writes."
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

### S212 | T1 | partner-affiliate

- path: `.agents/skills/partner-affiliate/SKILL.md`
- chars: 667
- outline:
- partner-affiliate

```markdown
---
name: partner-affiliate
description: "Design partner and affiliate programs: recruitment, revenue share, co-marketing. Use for partner programs. Do NOT use for code work."
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

### S213 | T1 | patch-planner

- path: `.agents/skills/patch-planner/SKILL.md`
- chars: 485
- outline:
- patch-planner

```markdown
---
name: patch-planner
description: "Generate patch proposals and rollback plans without applying them. Use for patch planning. Do NOT use for unrelated stacks or deployment."
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

### S214 | T1 | perf-astro

- path: `.agents/skills/perf-astro/SKILL.md`
- chars: 497
- outline:
- perf-astro

```markdown
---
name: perf-astro
description: "Optimize Astro sites for Lighthouse: critical CSS, fonts, LCP. Use for Astro performance. Do NOT use for non-Astro sites or Lighthouse-only audits."
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

### S215 | T1 | perf-lighthouse

- path: `.agents/skills/perf-lighthouse/SKILL.md`
- chars: 495
- outline:
- perf-lighthouse

```markdown
---
name: perf-lighthouse
description: "Run Lighthouse via CLI or Node, parse reports, set budgets. Use for Lighthouse audits. Do NOT use for CWV fixes (core-web-vitals)."
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

### S216 | T1 | perf-web-optimization

- path: `.agents/skills/perf-web-optimization/SKILL.md`
- chars: 523
- outline:
- perf-web-optimization

```markdown
---
name: perf-web-optimization
description: "Measure, then cut bundle size, images, caching and page speed. Use for web performance work. Do NOT use for CWV-only work (core-web-vitals)."
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

### S217 | T1 | performance-optimizer

- path: `.agents/skills/performance-optimizer/SKILL.md`
- chars: 505
- outline:
- performance-optimizer

```markdown
---
name: performance-optimizer
description: "Measure and improve AEOS hot paths: registry, skill runs, evidence. Use for measured optimization. Do NOT use for speculative tuning."
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

### S218 | T1 | performance-profiler

- path: `.agents/skills/performance-profiler/SKILL.md`
- chars: 504
- outline:
- performance-profiler

```markdown
---
name: performance-profiler
description: "Profile AEOS runs: repo scans, hashing, package verification, Judge runtime. Use for AEOS profiling. Do NOT use for speculative tuning."
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

### S219 | T1 | playbook-factory-generator

- path: `.agents/skills/playbook-factory-generator/SKILL.md`
- chars: 532
- outline:
- playbook-factory-generator

```markdown
---
name: playbook-factory-generator
description: "Generate a reviewable playbook with step contracts, dependencies and verification gates. Use for playbook generation. Do NOT use for one-off coding."
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

### S220 | T1 | playbook-optimizer

- path: `.agents/skills/playbook-optimizer/SKILL.md`
- chars: 489
- outline:
- playbook-optimizer

```markdown
---
name: playbook-optimizer
description: "Optimize playbooks for execution time, safety and evidence quality. Use for playbook optimization. Do NOT use for one-off coding."
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

### S221 | T1 | playwright-skill

- path: `.agents/skills/playwright-skill/SKILL.md`
- chars: 516
- outline:
- playwright-skill

```markdown
---
name: playwright-skill
description: "Browser automation and E2E tests with Playwright: forms, flows, responsive checks. Use for web tests. Do NOT use for debugging (chrome-devtools)."
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

### S222 | T1 | policy-bypass-evaluator

- path: `.agents/skills/policy-bypass-evaluator/SKILL.md`
- chars: 508
- outline:
- policy-bypass-evaluator

```markdown
---
name: policy-bypass-evaluator
description: "Check policy boundaries reject bypass attempts. Use for bypass evaluations. Do NOT use outside authorized scope or to expose secrets."
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

### S223 | T1 | policy-hardening-auditor

- path: `.agents/skills/policy-hardening-auditor/SKILL.md`
- chars: 519
- outline:
- policy-hardening-auditor

```markdown
---
name: policy-hardening-auditor
description: "Audit policies for unsafe paths and fail-closed behavior. Use for policy hardening. Do NOT use outside authorized scope or to expose secrets."
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

### S224 | T1 | positioning-icp

- path: `.agents/skills/positioning-icp/SKILL.md`
- chars: 676
- outline:
- positioning-icp

```markdown
---
name: positioning-icp
description: "ICP definition, market positioning, messaging and PMF validation for AI-native products. Use for ICP or positioning work. Do NOT use for code work."
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

### S225 | T1 | pr-comment-resolver

- path: `.agents/skills/pr-comment-resolver/SKILL.md`
- chars: 510
- outline:
- pr-comment-resolver

```markdown
---
name: pr-comment-resolver
description: "Resolve PR review comments systematically, without blindly obeying incorrect feedback. Use for PR comment resolution. Do NOT use for deployment."
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

### S226 | T1 | pr-reviewer

- path: `.agents/skills/pr-reviewer/SKILL.md`
- chars: 473
- outline:
- pr-reviewer

```markdown
---
name: pr-reviewer
description: "Review pull requests as an independent, evidence-based reviewer. Use for PR reviews. Do NOT use for deployment or unrelated stacks."
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

### S227 | T1 | pr-reviewer-advanced

- path: `.agents/skills/pr-reviewer-advanced/SKILL.md`
- chars: 493
- outline:
- pr-reviewer-advanced

```markdown
---
name: pr-reviewer-advanced
description: "Perform severity-ranked, evidence-backed PR reviews. Use for deep PR reviews. Do NOT use for deployment or unrelated stacks."
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

### S228 | T1 | production-deployment-planner

- path: `.agents/skills/production-deployment-planner/SKILL.md`
- chars: 529
- outline:
- production-deployment-planner

```markdown
---
name: production-deployment-planner
description: "Plan production packaging, CI/CD, deployment, observability and rollback. Use for deployment plans. Do NOT use for unapproved prod changes."
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

### S229 | T1 | progress-tracker

- path: `.agents/skills/progress-tracker/SKILL.md`
- chars: 496
- outline:
- progress-tracker

```markdown
---
name: progress-tracker
description: "Keep .notebook/PROGRESS.md as the live, evidence-backed mission checklist. Use for progress tracking. Do NOT use to promote unverified claims."
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

### S230 | T1 | prompt-optimizer

- path: `.agents/skills/prompt-optimizer/SKILL.md`
- chars: 487
- outline:
- prompt-optimizer

```markdown
---
name: prompt-optimizer
description: "Convert vague prompts into bounded, evidence-based task prompts. Use for prompt optimization. Do NOT use for unapproved remote writes."
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

### S231 | T1 | ptbr-documentary-voice-expert

- path: `.agents/skills/ptbr-documentary-voice-expert/SKILL.md`
- chars: 540
- outline:
- ptbr-documentary-voice-expert

```markdown
---
name: ptbr-documentary-voice-expert
description: "Deep male PT-BR documentary narration, scientific pronunciation. Use for narrador de documentário. Do NOT use to clone voices without authorization."
license: CC-BY-4.0
metadata:
  author: AEOS
  version: 0.2.0
  owner_agent: codenavi-agent
---

# ptbr-documentary-voice-expert

Read and follow `00_skills/(tooling)/ptbr-documentary-voice-expert/SKILL.md` and its relevant local modules.

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity.
```

### S232 | T1 | python-ai-productionizer

- path: `.agents/skills/python-ai-productionizer/SKILL.md`
- chars: 520
- outline:
- python-ai-productionizer

```markdown
---
name: python-ai-productionizer
description: "Analyze Python AI/RAG systems for production readiness. Use for Python AI productionization. Do NOT use for unrelated stacks or deployment."
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

### S233 | T1 | python-bug-solver-skill

- path: `.agents/skills/python-bug-solver-skill/SKILL.md`
- chars: 519
- outline:
- python-bug-solver-skill

```markdown
---
name: python-bug-solver-skill
description: "Create a Python bug-solver skill for stack traces and root-cause fixes. Use for creating a Python bug solver. Do NOT use for other languages."
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

### S234 | T1 | python-expert

- path: `.agents/skills/python-expert/SKILL.md`
- chars: 483
- outline:
- python-expert

```markdown
---
name: python-expert
description: "Implement, diagnose, test and modernize Python projects with version-correct APIs. Use for Python work. Do NOT use for other languages."
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

### S235 | T1 | python-rag-audit

- path: `.agents/skills/python-rag-audit/SKILL.md`
- chars: 492
- outline:
- python-rag-audit

```markdown
---
name: python-rag-audit
description: "Audit Python RAG pipelines for security, data leakage and prompt injection. Use for Python RAG audits. Do NOT use for unrelated stacks."
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

### S236 | T1 | rag-expert

- path: `.agents/skills/rag-expert/SKILL.md`
- chars: 477
- outline:
- rag-expert

```markdown
---
name: rag-expert
description: "Implement and evaluate grounded retrieval: hybrid search, reranking, citations. Use for RAG work. Do NOT use for standalone Laya training."
license: CC-BY-4.0
metadata:
  author: AEOS
  version: 1.1.0
  owner_agent: codenavi-agent
---

# rag-expert

Read and follow `00_skills/(development)/rag-expert/SKILL.md` and its relevant local modules.

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity.
```

### S237 | T1 | rag-laya-expert

- path: `.agents/skills/rag-laya-expert/SKILL.md`
- chars: 489
- outline:
- rag-laya-expert

```markdown
---
name: rag-laya-expert
description: "Orchestrate evaluated RAG and GraphRAG with Laya decisions. Use for RAG or GraphRAG with Laya. Do NOT use for standalone graph drawing."
license: CC-BY-4.0
metadata:
  author: AEOS
  version: 0.1.0
  owner_agent: codenavi-agent
---

# rag-laya-expert

Read and follow `00_skills/(development)/rag-laya-expert/SKILL.md` and its relevant local modules.

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity.
```

### S238 | T1 | ragraph-expert

- path: `.agents/skills/ragraph-expert/SKILL.md`
- chars: 493
- outline:
- ragraph-expert

```markdown
---
name: ragraph-expert
description: "Build and evaluate source-backed knowledge-graph retrieval (GraphRAG). Use for GraphRAG or entity resolution. Do NOT use for generic diagrams."
license: CC-BY-4.0
metadata:
  author: AEOS
  version: 0.1.0
  owner_agent: codenavi-agent
---

# ragraph-expert

Read and follow `00_skills/(development)/ragraph-expert/SKILL.md` and its relevant local modules.

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity.
```

### S239 | T1 | rails-dev

- path: `.agents/skills/rails-dev/SKILL.md`
- chars: 507
- outline:
- rails-dev

```markdown
---
name: rails-dev
description: "Rails conventions (rich models, concerns, Minitest). Use for any Rails model, schema or code topic. Do NOT use for non-Rails backends."
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

### S240 | T1 | react-best-practices

- path: `.agents/skills/react-best-practices/SKILL.md`
- chars: 507
- outline:
- react-best-practices

```markdown
---
name: react-best-practices
description: "React/Next.js performance: data fetching, bundles, rendering. Use for React perf work. Do NOT use for component APIs (react-composition-patterns)."
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

### S241 | T1 | react-composition-patterns

- path: `.agents/skills/react-composition-patterns/SKILL.md`
- chars: 531
- outline:
- react-composition-patterns

```markdown
---
name: react-composition-patterns
description: "React composition: compound components, render props, React 19. Use for component API refactors. Do NOT use for performance (react-best-practices)."
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

### S242 | T1 | react-expert

- path: `.agents/skills/react-expert/SKILL.md`
- chars: 492
- outline:
- react-expert

```markdown
---
name: react-expert
description: "Implement and refactor React apps on the repo's exact React version and conventions. Use for React work. Do NOT use for other stacks or deployment."
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

### S243 | T1 | react-native-expert

- path: `.agents/skills/react-native-expert/SKILL.md`
- chars: 545
- outline:
- react-native-expert

```markdown
---
name: react-native-expert
description: "Build production React Native and Expo apps: navigation, lists, native modules. Use for mobile app work. Do NOT use for Flutter or web-only React."
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

### S244 | T1 | redaction-evaluator

- path: `.agents/skills/redaction-evaluator/SKILL.md`
- chars: 509
- outline:
- redaction-evaluator

```markdown
---
name: redaction-evaluator
description: "Evaluate redaction in authorized outputs for leakage and over-redaction. Use for redaction reviews. Do NOT use outside scope or to expose secrets."
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

### S245 | T1 | release-readiness-judge

- path: `.agents/skills/release-readiness-judge/SKILL.md`
- chars: 520
- outline:
- release-readiness-judge

```markdown
---
name: release-readiness-judge
description: "Validate release readiness with deterministic gates. Use for release readiness checks. Do NOT use as deployment approval or for unexecuted checks."
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

### S246 | T1 | render-deploy

- path: `.agents/skills/render-deploy/SKILL.md`
- chars: 501
- outline:
- render-deploy

```markdown
---
name: render-deploy
description: "Deploy apps to Render: analyze code, generate render.yaml Blueprints. Use for Render deploys. Do NOT use for Vercel, Netlify or Cloudflare."
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

### S247 | T1 | repo-scanner

- path: `.agents/skills/repo-scanner/SKILL.md`
- chars: 482
- outline:
- repo-scanner

```markdown
---
name: repo-scanner
description: "Map repositories into factual ecosystems. Use for repo scans. Do NOT use to mutate production or invent architecture without source evidence."
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

### S248 | T1 | report-design

- path: `.agents/skills/report-design/SKILL.md`
- chars: 519
- outline:
- report-design

```markdown
---
name: report-design
description: "Apply the offline report layout: tokens, grids, filters, export, drill-down. Use for HTML report fixes. Do NOT use for data collection."
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

### S249 | T1 | resolver-comentarios

- path: `.agents/skills/resolver-comentarios/SKILL.md`
- chars: 500
- outline:
- resolver-comentarios

```markdown
---
name: resolver-comentarios
description: "Resolve concrete PR review comments after inspecting code and verifying fixes. Use for PR comment fixes. Do NOT use for deployment."
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

### S250 | T1 | revisar-pr

- path: `.agents/skills/revisar-pr/SKILL.md`
- chars: 495
- outline:
- revisar-pr

```markdown
---
name: "revisar-pr"
description: "Review a PR diff against requirements and conventions, ranked findings. Use for revisar PR. Do NOT use for security review (revisar-seguranca-pr)."
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

### S251 | T1 | revisar-seguranca-pr

- path: `.agents/skills/revisar-seguranca-pr/SKILL.md`
- chars: 552
- outline:
- revisar-seguranca-pr

```markdown
---
name: revisar-seguranca-pr
description: "Review a PR diff for authorization, sensitive data and security failures. Use for PR security review. Do NOT use for general review (revisar-pr)."
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

### S252 | T1 | risk-classifier

- path: `.agents/skills/risk-classifier/SKILL.md`
- chars: 499
- outline:
- risk-classifier

```markdown
---
name: risk-classifier
description: "Classify change risk: scope, impact, reversibility, coverage. Use for risk classification. Do NOT use outside authorized scope or to expose secrets."
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

### S253 | T1 | rollback-planner

- path: `.agents/skills/rollback-planner/SKILL.md`
- chars: 495
- outline:
- rollback-planner

```markdown
---
name: rollback-planner
description: "Generate rollback plans that define how to undo every operation safely. Use for rollback planning. Do NOT use for unapproved production changes."
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

### S254 | T1 | runtime-troubleshooting

- path: `.agents/skills/runtime-troubleshooting/SKILL.md`
- chars: 563
- outline:
- runtime-troubleshooting

```markdown
---
name: runtime-troubleshooting
description: "Diagnose apps from read-only logs. Use for runtime failures. Do NOT use to restart, scale, deploy, redesign or invent inaccessible broker state."
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

### S255 | T1 | rust-expert

- path: `.agents/skills/rust-expert/SKILL.md`
- chars: 513
- outline:
- rust-expert

```markdown
---
name: rust-expert
description: "Implement, diagnose, modernize and migrate Rust projects with version-correct APIs. Use for Rust work. Do NOT use for other languages or deployment."
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

### S256 | T1 | sales-motion-design

- path: `.agents/skills/sales-motion-design/SKILL.md`
- chars: 683
- outline:
- sales-motion-design

```markdown
---
name: sales-motion-design
description: "Choose PLG vs sales-led, design the sales motion and time-to-first-value. Use for sales motion or free-trial design. Do NOT use for code work."
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

### S257 | T1 | science-research-expert

- path: `.agents/skills/science-research-expert/SKILL.md`
- chars: 518
- outline:
- science-research-expert

```markdown
---
name: science-research-expert
description: "Revisar fontes de ciência. Use for checar afirmações científicas. Do NOT use para inventar referências, certificar medicina ou renderizar vídeo."
license: CC-BY-4.0
metadata:
  author: AEOS
  version: 0.2.0
  owner_agent: codenavi-agent
---

# science-research-expert

Read and follow `00_skills/(tooling)/science-research-expert/SKILL.md` and its relevant local modules.

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity.
```

### S258 | T1 | science-script-expert

- path: `.agents/skills/science-script-expert/SKILL.md`
- chars: 511
- outline:
- science-script-expert

```markdown
---
name: science-script-expert
description: "Escrever roteiros científicos PT-BR sincronizados com storyboard. Use for roteiro de ciência. Do NOT use for pesquisa sem fontes ou arte final."
license: CC-BY-4.0
metadata:
  author: AEOS
  version: 0.2.0
  owner_agent: codenavi-agent
---

# science-script-expert

Read and follow `00_skills/(tooling)/science-script-expert/SKILL.md` and its relevant local modules.

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity.
```

### S259 | T1 | science-studio-expert

- path: `.agents/skills/science-studio-expert/SKILL.md`
- chars: 501
- outline:
- science-studio-expert

```markdown
---
name: science-studio-expert
description: "Orquestrar Science Studio AI do tema ao Motion Comic revisável. Use for criar vídeo de ciência. Do NOT use to publish without review."
license: CC-BY-4.0
metadata:
  author: AEOS
  version: 0.2.0
  owner_agent: codenavi-agent
---

# science-studio-expert

Read and follow `00_skills/(tooling)/science-studio-expert/SKILL.md` and its relevant local modules.

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity.
```

### S260 | T1 | science-vfx-expert

- path: `.agents/skills/science-vfx-expert/SKILL.md`
- chars: 504
- outline:
- science-vfx-expert

```markdown
---
name: science-vfx-expert
description: "Plan controlled science VFX: gravitational lens, particles, glow. Use for VFX científicos em Motion Comic. Do NOT use to claim validated physics."
license: CC-BY-4.0
metadata:
  author: AEOS
  version: 0.2.0
  owner_agent: codenavi-agent
---

# science-vfx-expert

Read and follow `00_skills/(tooling)/science-vfx-expert/SKILL.md` and its relevant local modules.

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity.
```

### S261 | T1 | science-video-review-expert

- path: `.agents/skills/science-video-review-expert/SKILL.md`
- chars: 534
- outline:
- science-video-review-expert

```markdown
---
name: science-video-review-expert
description: "Review and package science Motion Comic videos before export. Use for QA de vídeo de ciência. Do NOT use to self-approve or publish without request."
license: CC-BY-4.0
metadata:
  author: AEOS
  version: 0.2.0
  owner_agent: codenavi-agent
---

# science-video-review-expert

Read and follow `00_skills/(tooling)/science-video-review-expert/SKILL.md` and its relevant local modules.

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity.
```

### S262 | T1 | secret-redaction-specialist

- path: `.agents/skills/secret-redaction-specialist/SKILL.md`
- chars: 532
- outline:
- secret-redaction-specialist

```markdown
---
name: secret-redaction-specialist
description: "Detect and redact sensitive data without exposing raw values. Use for secret redaction. Do NOT use outside authorized scope or to expose secrets."
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

### S263 | T1 | security-audit

- path: `.agents/skills/security-audit/SKILL.md`
- chars: 498
- outline:
- security-audit

```markdown
---
name: security-audit
description: "Detect security risks and possible secrets without exposing values. Use for security audits. Do NOT use outside authorized scope or to expose secrets."
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

### S264 | T1 | security-best-practices

- path: `.agents/skills/security-best-practices/SKILL.md`
- chars: 537
- outline:
- security-best-practices

```markdown
---
name: "security-best-practices"
description: "Review secure-by-default code (Java, Spring, Angular, Python, JS, Go). Use for secure coding. Do NOT use for PR diffs (revisar-seguranca-pr)."
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

### S265 | T1 | security-ownership-map

- path: `.agents/skills/security-ownership-map/SKILL.md`
- chars: 511
- outline:
- security-ownership-map

```markdown
---
name: security-ownership-map
description: "Map git ownership: people-to-file, bus factor, orphaned sensitive code. Use for bus-factor checks. Do NOT use for threat models."
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

### S266 | T1 | security-threat-model

- path: `.agents/skills/security-threat-model/SKILL.md`
- chars: 521
- outline:
- security-threat-model

```markdown
---
name: security-threat-model
description: "Repo-grounded threat model: trust boundaries, assets, attackers, abuse paths. Use for threat modeling. Do NOT use for architecture summaries."
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

### S267 | T1 | sentry

- path: `.agents/skills/sentry/SKILL.md`
- chars: 480
- outline:
- sentry

```markdown
---
name: sentry
description: "Inspect Sentry issues and production errors via the read-only API. Use for 'check Sentry' reports. Do NOT use for SDK setup or alerts."
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

### S268 | T1 | seo

- path: `.agents/skills/seo/SKILL.md`
- chars: 469
- outline:
- seo

```markdown
---
name: seo
description: "Optimize search visibility: meta tags, structured data, sitemaps. Use for 'improve SEO' requests. Do NOT use for accessibility or full site audits."
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

### S269 | T1 | servicenow-incident-assistant

- path: `.agents/skills/servicenow-incident-assistant/SKILL.md`
- chars: 545
- outline:
- servicenow-incident-assistant

```markdown
---
name: servicenow-incident-assistant
description: "Turn incident evidence into ServiceNow triage, updates and RCA. Use for ServiceNow incident work. Do NOT use to mutate live systems unless authorized."
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

### S270 | T1 | shopify-developer

- path: `.agents/skills/shopify-developer/SKILL.md`
- chars: 517
- outline:
- shopify-developer

```markdown
---
name: shopify-developer
description: "Shopify reference: Liquid, themes, GraphQL, Hydrogen, Functions. Use for .liquid files or Shopify apps. Do NOT use for other e-commerce platforms."
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

### S271 | T1 | simulator-ai

- path: `.agents/skills/simulator-ai/SKILL.md`
- chars: 487
- outline:
- simulator-ai

```markdown
---
name: simulator-ai
description: "Build a governed AI medical simulator. Use for simulator construction. Never hallucinates or invents results; do NOT use for unrelated stacks."
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

### S272 | T1 | skill-architect

- path: `.agents/skills/skill-architect/SKILL.md`
- chars: 518
- outline:
- skill-architect

```markdown
---
name: "skill-architect"
description: "Build, score and improve reusable skills with minimal evidence-based edits. Use for creating or reviewing skills. Do NOT use for agent identities."
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

### S273 | T1 | skill-factory

- path: `.agents/skills/skill-factory/SKILL.md`
- chars: 481
- outline:
- skill-factory

```markdown
---
name: skill-factory
description: "Create, refactor and validate workspace skills with precise routing. Use for criar or refatorar skills. Do NOT use for agent identities."
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

### S274 | T1 | skill-factory-generator

- path: `.agents/skills/skill-factory-generator/SKILL.md`
- chars: 510
- outline:
- skill-factory-generator

```markdown
---
name: skill-factory-generator
description: "Generate a bounded reusable skill package with routing and verifiable gates. Use for skill generation. Do NOT use for unrelated coding."
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

### S275 | T1 | skill-hardener

- path: `.agents/skills/skill-hardener/SKILL.md`
- chars: 472
- outline:
- skill-hardener

```markdown
---
name: skill-hardener
description: "Harden skills with contracts, forbidden actions and quality gates. Use for skill hardening. Do NOT use for unrelated coding."
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

### S276 | T1 | slo-risk-analyzer

- path: `.agents/skills/slo-risk-analyzer/SKILL.md`
- chars: 495
- outline:
- slo-risk-analyzer

```markdown
---
name: slo-risk-analyzer
description: "Map engineering operations to SLO/SLA risks and error budgets. Use for SLO risk analysis. Do NOT use for unmeasured speculative tuning."
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

### S277 | T1 | social-media-operator

- path: `.agents/skills/social-media-operator/SKILL.md`
- chars: 538
- outline:
- social-media-operator

```markdown
---
name: social-media-operator
description: "Governed TikTok/Instagram operations via cookie or browser sessions. Use for social profile reads. Do NOT use for OAuth keys or developer accounts."
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

### S278 | T1 | social-selling

- path: `.agents/skills/social-selling/SKILL.md`
- chars: 661
- outline:
- social-selling

```markdown
---
name: social-selling
description: "LinkedIn social selling: profile optimization, DM sequences, DM-to-deal conversion. Use for LinkedIn selling. Do NOT use for code work."
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

### S279 | T1 | solo-founder-gtm

- path: `.agents/skills/solo-founder-gtm/SKILL.md`
- chars: 661
- outline:
- solo-founder-gtm

```markdown
---
name: solo-founder-gtm
description: "GTM playbook for solo founders: stack, AI agent team, revenue stages, hiring. Use for solo-founder GTM. Do NOT use for code work."
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

### S280 | T1 | solve-problems

- path: `.agents/skills/solve-problems/SKILL.md`
- chars: 490
- outline:
- solve-problems

```markdown
---
name: solve-problems
description: "Fix defects across any language without changing project architecture. Use for defect fixes. Do NOT use for unrelated stacks or deployment."
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

### S281 | T1 | spec-driven

- path: `.agents/skills/spec-driven/SKILL.md`
- chars: 540
- outline:
- spec-driven

```markdown
---
name: spec-driven
description: "Spec-driven 4.0.0 (TLC): specify, design, tasks, execute with EARS and mutation checks. Use for feature specs. Do NOT use for pure architecture."
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

### S282 | T1 | spec-driven-eval

- path: `.agents/skills/spec-driven-eval/SKILL.md`
- chars: 563
- outline:
- spec-driven-eval

```markdown
---
name: spec-driven-eval
description: "Grade how fully an implementation fulfills a PRD, with one comparable score. Use when explicitly named. Do NOT use to build (tlc-spec-driven)."
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

### S283 | T1 | spec-driven-lean

- path: `.agents/skills/spec-driven-lean/SKILL.md`
- chars: 563
- outline:
- spec-driven-lean

```markdown
---
name: spec-driven-lean
description: "Tech Lead Club spec-lean 2.0.0: freeze obligations in proof-backed checks, then build. Use for spec-driven-lean work. Do NOT use for design docs."
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

### S284 | T1 | specs

- path: `.agents/skills/specs/SKILL.md`
- chars: 467
- outline:
- specs

```markdown
---
name: specs
description: "Require a spec before implementation: scope, checks, risks. Use for pre-implementation contracts. Do NOT use to override approved requirements."
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

### S285 | T1 | splunk-observability-staff

- path: `.agents/skills/splunk-observability-staff/SKILL.md`
- chars: 525
- outline:
- splunk-observability-staff

```markdown
---
name: splunk-observability-staff
description: "Splunk analysis: searches, metrics, logs, traces, notable events. Use for Splunk work. Do NOT use to mutate live systems unless authorized."
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

### S286 | T1 | staff-iii-architecture-governor

- path: `.agents/skills/staff-iii-architecture-governor/SKILL.md`
- chars: 537
- outline:
- staff-iii-architecture-governor

```markdown
---
name: staff-iii-architecture-governor
description: "Plan and select architecture for new projects or changes. Use for architecture selection. Do NOT use for implementation or deployment."
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

### S287 | T1 | staff-tdd-code-builder

- path: `.agents/skills/staff-tdd-code-builder/SKILL.md`
- chars: 523
- outline:
- staff-tdd-code-builder

```markdown
---
name: staff-tdd-code-builder
description: "Create or change code from an architecture plan using TDD by default. Use for TDD builds from a plan. Do NOT use for unrelated stacks or deployment."
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

### S288 | T1 | studio-creation-tlc

- path: `.agents/skills/studio-creation-tlc/SKILL.md`
- chars: 509
- outline:
- studio-creation-tlc

```markdown
---
name: studio-creation-tlc
description: "TLC rule for Dark Videos media (spec-driven, Spotify). Use for media creation with a role skill. Do NOT use as substitute or to upload mined files."
license: CC-BY-4.0
metadata:
  author: AEOS
  version: 1.0.0
  owner_agent: codenavi-agent
---

# studio-creation-tlc

Read and follow `00_skills/(tooling)/studio-creation-tlc/SKILL.md` and its relevant local modules.

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity.
```

### S289 | T1 | subagent-creator

- path: `.agents/skills/subagent-creator/SKILL.md`
- chars: 522
- outline:
- subagent-creator

```markdown
---
name: "subagent-creator"
description: "Design bounded lenses of codenavi-agent with one deliverable and a verdict. Use for verifier or audit units. Do NOT use to create agent identities."
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

### S290 | T1 | supply-chain-auditor

- path: `.agents/skills/supply-chain-auditor/SKILL.md`
- chars: 503
- outline:
- supply-chain-auditor

```markdown
---
name: supply-chain-auditor
description: "Audit dependency provenance and release integrity. Use for supply-chain audits. Do NOT use outside authorized scope or to expose secrets."
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

### S291 | T1 | tactical-ddd

- path: `.agents/skills/tactical-ddd/SKILL.md`
- chars: 487
- outline:
- tactical-ddd

```markdown
---
name: tactical-ddd
description: "Detect anemic domain models and refactor to rich DDD models. Use for DDD model reviews. Do NOT use for service boundaries or DTOs."
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

### S292 | T1 | task-graph-builder

- path: `.agents/skills/task-graph-builder/SKILL.md`
- chars: 484
- outline:
- task-graph-builder

```markdown
---
name: task-graph-builder
description: "Build a deterministic task graph from a playbook and objective. Use for task graphs. Do NOT use for unapproved remote writes."
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

### S293 | T1 | technical-design-doc-creator

- path: `.agents/skills/technical-design-doc-creator/SKILL.md`
- chars: 545
- outline:
- technical-design-doc-creator

```markdown
---
name: technical-design-doc-creator
description: "Create architecture-level technical design docs via discovery. Use for 'write a design doc' or 'criar um TDD'. Do NOT use for README or API docs."
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

### S294 | T1 | telemetry-bug-root-cause-solver

- path: `.agents/skills/telemetry-bug-root-cause-solver/SKILL.md`
- chars: 550
- outline:
- telemetry-bug-root-cause-solver

```markdown
---
name: telemetry-bug-root-cause-solver
description: "Resolve bugs from logs, metrics and traces via runtime evidence and code. Use for telemetry RCA. Do NOT use to mutate live systems unless authorized."
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

### S295 | T1 | test-gap-analyzer

- path: `.agents/skills/test-gap-analyzer/SKILL.md`
- chars: 503
- outline:
- test-gap-analyzer

```markdown
---
name: test-gap-analyzer
description: "Analyze test coverage gaps: untested modules and edge cases. Use for test gap analysis. Do NOT use as deployment approval or for unexecuted checks."
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

### S296 | T1 | test-generation

- path: `.agents/skills/test-generation/SKILL.md`
- chars: 493
- outline:
- test-generation

```markdown
---
name: test-generation
description: "Detect test gaps and generate proposed tests in a sandbox. Use for test generation. Do NOT use as deployment approval or for unexecuted checks."
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

### S297 | T1 | test-strategy-architect

- path: `.agents/skills/test-strategy-architect/SKILL.md`
- chars: 521
- outline:
- test-strategy-architect

```markdown
---
name: test-strategy-architect
description: "Build test strategy: unit, contract, e2e, security, performance. Use for test planning. Do NOT use as deployment approval or for unexecuted checks."
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

### S298 | T1 | test-writer

- path: `.agents/skills/test-writer/SKILL.md`
- chars: 484
- outline:
- test-writer

```markdown
---
name: test-writer
description: "Generate proposed tests in a sandbox from evidence; never real test dirs. Use for test proposals. Do NOT use as approval or for unexecuted checks."
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

### S299 | T1 | tests-expert

- path: `.agents/skills/tests-expert/SKILL.md`
- chars: 485
- outline:
- tests-expert

```markdown
---
name: tests-expert
description: "Run real functional and e2e checks after a fix or new behavior. Use for fixes, new features or e2e tests. Do NOT use for unit tests or coverage."
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

### S300 | T1 | the-fool

- path: `.agents/skills/the-fool/SKILL.md`
- chars: 508
- outline:
- the-fool

```markdown
---
name: "the-fool"
description: "Stress-test a pending decision: threats, fragile assumptions, blind spots. Use for devil's advocate or pre-mortem. Do NOT use to decide for the owner."
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

### S301 | T1 | the-judge

- path: `.agents/skills/the-judge/SKILL.md`
- chars: 515
- outline:
- the-judge

```markdown
---
name: the-judge
description: "Evidence-first PR judge: repo checks, correctness, security, one GitHub review. Use for 'review this PR' or 'julgue esse PR'. Do NOT use for CI fixes."
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

### S302 | T1 | the-jury

- path: `.agents/skills/the-jury/SKILL.md`
- chars: 497
- outline:
- the-jury

```markdown
---
name: "the-jury"
description: "Tally a verdict on a decidable question through 3 or 5 orthogonal lenses. Use for decision panels. Do NOT use to spawn agents or implement."
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

### S303 | T1 | threat-modeler

- path: `.agents/skills/threat-modeler/SKILL.md`
- chars: 496
- outline:
- threat-modeler

```markdown
---
name: threat-modeler
description: "Produce AEOS threat models for prompt injection, tool poisoning and secret leakage. Use for AEOS threat models. Do NOT use outside authorized scope."
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

### S304 | T1 | tlc-discover

- path: `.agents/skills/tlc-discover/SKILL.md`
- chars: 525
- outline:
- tlc-discover

```markdown
---
name: tlc-discover
description: "Interview an unshaped idea into a verdict and design doc. Use for 'should we build this' or discovery. Do NOT use to cut tasks or implement."
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

### S305 | T1 | tlc-generative-engine-optimization

- path: `.agents/skills/tlc-generative-engine-optimization/SKILL.md`
- chars: 582
- outline:
- tlc-generative-engine-optimization

```markdown
---
name: tlc-generative-engine-optimization
description: "Make pages citable by AI answer engines (GEO): schema, llms.txt, structure. Use for GEO or AI citability. Do NOT use for AI SEO strategy (ai-seo)."
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

### S306 | T1 | tlc-implement

- path: `.agents/skills/tlc-implement/SKILL.md`
- chars: 520
- outline:
- tlc-implement

```markdown
---
name: tlc-implement
description: "Implement planned work: extract a checklist, build it, prove each check. Use for 'build this ticket'. Do NOT use to design the work."
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

### S307 | T1 | tlc-plan

- path: `.agents/skills/tlc-plan/SKILL.md`
- chars: 479
- outline:
- tlc-plan

```markdown
---
name: tlc-plan
description: "Turn a decided PRD or design doc into tasks with observable criteria. Use for task cutting. Do NOT use for discovery or implementation."
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

### S308 | T1 | tlc-prd

- path: `.agents/skills/tlc-prd/SKILL.md`
- chars: 511
- outline:
- tlc-prd

```markdown
---
name: tlc-prd
description: "Interview an idea into a PRD: problem, success, boundaries, journeys. Use for 'write the PRD'. Do NOT use to design solutions or cut tasks."
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

### S309 | T1 | tlc-spec-driven

- path: `.agents/skills/tlc-spec-driven/SKILL.md`
- chars: 528
- outline:
- tlc-spec-driven

```markdown
---
name: tlc-spec-driven
description: "TLC spec-driven 4.0.0: specify, design, tasks, execute with EARS and proof checks. Use for feature specs. Do NOT use for pure architecture."
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

### S310 | T1 | tlc-spec-lean

- path: `.agents/skills/tlc-spec-lean/SKILL.md`
- chars: 531
- outline:
- tlc-spec-lean

```markdown
---
name: tlc-spec-lean
description: "TLC spec-lean 2.0.0: freeze obligations in proof-backed checks, then build. Use for plan feature or write checks. Do NOT use for design docs."
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

### S311 | T1 | token-budget-governor

- path: `.agents/skills/token-budget-governor/SKILL.md`
- chars: 518
- outline:
- token-budget-governor

```markdown
---
name: token-budget-governor
description: "Prevent token waste with scoped prompts, compact context and narrow lenses. Use for token budget governance. Do NOT use to promote unverified claims."
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

### S312 | T1 | tool-router-audit

- path: `.agents/skills/tool-router-audit/SKILL.md`
- chars: 504
- outline:
- tool-router-audit

```markdown
---
name: tool-router-audit
description: "Audit whether AEOS code and playbooks enforce Tool Router for external actions. Use for Tool Router audits. Do NOT use for unapproved remote writes."
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

### S313 | T1 | typesafe-ai

- path: `.agents/skills/typesafe-ai/SKILL.md`
- chars: 485
- outline:
- typesafe-ai

```markdown
---
name: typesafe-ai
description: "Build AI features with TypeSafe models (Jev): typed judgments as code primitives. Use for programmable AI decisions. Do NOT use for unrelated stacks."
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

### S314 | T1 | unique-environment-auditor

- path: `.agents/skills/unique-environment-auditor/SKILL.md`
- chars: 528
- outline:
- unique-environment-auditor

```markdown
---
name: unique-environment-auditor
description: "Audit an environment inventory for conflicting versions and unmet runtime needs. Use for environment audits. Do NOT use for unrelated stacks."
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

### S315 | T1 | universal-project-factory

- path: `.agents/skills/universal-project-factory/SKILL.md`
- chars: 528
- outline:
- universal-project-factory

```markdown
---
name: universal-project-factory
description: "Plan and generate sandbox-first projects from zero to production for any stack. Use for project generation. Do NOT use for ordinary one-off coding."
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

### S316 | T1 | v1-readiness-auditor

- path: `.agents/skills/v1-readiness-auditor/SKILL.md`
- chars: 501
- outline:
- v1-readiness-auditor

```markdown
---
name: v1-readiness-auditor
description: "Validate AEOS against v1.0 release gates and generate a blocking report. Use for v1 readiness checks. Do NOT use as deployment approval."
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

### S317 | T1 | vercel-deploy

- path: `.agents/skills/vercel-deploy/SKILL.md`
- chars: 501
- outline:
- vercel-deploy

```markdown
---
name: vercel-deploy
description: "Deploy apps and websites to Vercel, including previews. Use for Vercel deploys or live links. Do NOT use for Netlify, Cloudflare or Render."
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

### S318 | T1 | video-outreach

- path: `.agents/skills/video-outreach/SKILL.md`
- chars: 659
- outline:
- video-outreach

```markdown
---
name: video-outreach
description: "Video-first cold outreach: personalized video at scale, async selling, AI demos. Use for video prospecting. Do NOT use for code work."
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

### S319 | T1 | voiceai

- path: `.agents/skills/voiceai/SKILL.md`
- chars: 468
- outline:
- voiceai

```markdown
---
name: voiceai
description: "Voice interface for AEOS; activation is consent for authorized audio only. Use for voice input or transcription. Do NOT use for remote writes."
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

### S320 | T1 | vox-aurum

- path: `.agents/skills/vox-aurum/SKILL.md`
- chars: 517
- outline:
- vox-aurum

```markdown
---
name: "vox-aurum"
description: "Transcribe authorized bare audio offline with local Whisper. Use for offline transcription. Do NOT use for meeting video (acta-aurea)."
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

### S321 | T1 | vuln-obsol-recon

- path: `.agents/skills/vuln-obsol-recon/SKILL.md`
- chars: 531
- outline:
- vuln-obsol-recon

```markdown
---
name: vuln-obsol-recon
description: "Assess CVE and EOL risk. Use for CVE checks. Do NOT use for base sync, patching or invented versions without manifests/runtime evidence."
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

### S322 | T1 | web-accessibility

- path: `.agents/skills/web-accessibility/SKILL.md`
- chars: 473
- outline:
- web-accessibility

```markdown
---
name: web-accessibility
description: "Audit and improve web accessibility to WCAG 2.1. Use for a11y audits. Do NOT use for SEO or performance work."
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

### S323 | T1 | web-best-practices

- path: `.agents/skills/web-best-practices/SKILL.md`
- chars: 514
- outline:
- web-best-practices

```markdown
---
name: web-best-practices
description: "Apply modern web security, compatibility and code-quality checks. Use for web best-practice reviews. Do NOT use for accessibility, SEO or full audits."
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

### S324 | T1 | web-design-guidelines

- path: `.agents/skills/web-design-guidelines/SKILL.md`
- chars: 551
- outline:
- web-design-guidelines

```markdown
---
name: web-design-guidelines
description: "Review UI code against Web Interface Guidelines: visual and interaction patterns. Use for 'review my UI'. Do NOT use for performance or SEO audits."
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

### S325 | T1 | web-quality-audit

- path: `.agents/skills/web-quality-audit/SKILL.md`
- chars: 489
- outline:
- web-quality-audit

```markdown
---
name: web-quality-audit
description: "Multi-area web audit: performance, accessibility, SEO, best practices. Use for 'audit my site'. Do NOT use for single-area work."
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

### S326 | T1 | whatsapp-simulator

- path: `.agents/skills/whatsapp-simulator/SKILL.md`
- chars: 491
- outline:
- whatsapp-simulator

```markdown
---
name: whatsapp-simulator
description: "Generate synthetic WhatsApp-style conversation fixtures for testing. Use for chat fixtures. Do NOT use for unapproved remote writes."
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

### S327 | T1 | wordpress-expert

- path: `.agents/skills/wordpress-expert/SKILL.md`
- chars: 499
- outline:
- wordpress-expert

```markdown
---
name: wordpress-expert
description: "Staff-level WordPress super-skill: site mapping, clean-code changes, plugins, themes. Use for WordPress work. Do NOT use for unrelated stacks."
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

### S328 | T1 | workbench-profile-resolver

- path: `.agents/skills/workbench-profile-resolver/SKILL.md`
- chars: 528
- outline:
- workbench-profile-resolver

```markdown
---
name: workbench-profile-resolver
description: "Resolve the smallest compatible workbench profile from scope and constraints. Use for profile selection. Do NOT use for unapproved remote writes."
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

