# AEOS Skill Factory — CodENavi Single-Agent

Governance: CodENavi Full Workspace v2
Version: 3.0.0
Status: ACTIVE

## Mission

Create, repair, audit and evolve reusable AEOS skills that are executed by the single canonical `codenavi-agent` and governed by the root `AGENT.md` contract.

A skill is a capability contract. It is not an identity, persona or autonomous authority boundary.

## Activation

Activate when the user asks to create, generate, convert, improve, standardize, audit or package an AEOS skill or reusable capability.

Do not activate for one-off answers, human competency lists, game abilities or ordinary functions merely named “skill”.

## Non-negotiable invariants

1. `codenavi-agent` is the only agent identity in AEOS.
2. Specialization is represented by skills, playbooks, MCPs, LCPs, tools, adapters and critical-thinking lenses.
3. A generated skill must never introduce another agent identity, persona prompt, hierarchy or delegation graph.
4. Judge is an independent deterministic runtime gate/service. It is not a prompt persona and is not emitted as a skill artifact.
5. Active AEOS orchestration is Node.js/TypeScript. Python can be a target-project language, but it must not orchestrate AEOS.
6. Evidence precedes completion claims.
7. Secrets remain runtime-only and redacted from prompts, logs, reports, evidence and repository files.
8. High-impact or destructive operations remain subject to policy, permission, approval, rollback and Judge gates.
9. New skills inherit `AGENT.md` and `references/CODENAVI_FULL_WORKSPACE_STANDARD.md`; they must not duplicate the constitution.
10. Prefer the smallest sufficient package and surgical changes.

## Architecture levels

### Level 1 — Contract only

Use for bounded capabilities that need only a `SKILL.md` contract.

```text
<skill>/
└── SKILL.md
```

### Level 2 — Knowledge-backed

Use when the capability needs governed references, schemas or templates.

```text
<skill>/
├── SKILL.md
├── references/
│   └── INDEX.md
├── schemas/
└── templates/
```

Create only the directories that materially serve the skill.

### Level 3 — Executable

Use when deterministic execution is required.

```text
<skill>/
├── SKILL.md
├── references/
│   └── INDEX.md
├── scripts/
├── schemas/
├── tests/
└── templates/
```

Executable AEOS adapters/orchestrators must be Node.js/TypeScript. Target-project helpers may use the project language when appropriate and explicitly bounded.

No architecture level creates an additional agent file.

## Mandatory design sequence

`BRIEFING → RECON → PLAN → EXECUTE → VERIFY → DEBRIEF`

During that lifecycle:

1. extract the reusable objective and non-goals;
2. inspect relevant repository conventions and `.notebook/INDEX.md`;
3. classify risk and required authorities;
4. select the smallest architecture level;
5. define activation and non-activation rules;
6. define input/output contracts and preconditions;
7. define tool, MCP/LCP, security and secret boundaries;
8. define evidence, validation and failure behavior;
9. generate only necessary files;
10. run deterministic validators/tests where available;
11. route high-impact completion through the runtime Judge gate;
12. record only validated reusable project knowledge.

## Required `SKILL.md` concerns

Every production skill must make these concerns explicit, directly or by a governed reference:

- identity of the capability, without creating an agent persona;
- mission;
- activation and non-activation;
- scope and non-goals;
- inputs and outputs;
- preconditions;
- workflow;
- tool and permission policy;
- evidence policy;
- security and secret policy;
- validation;
- stop/failure conditions;
- completion criteria;
- maintenance/version metadata.

## Generated metadata

Prefer this compact metadata block when a skill needs machine-readable metadata:

```yaml
skill:
  name:
  slug:
  version:
  description:
  category:
  architecture_level:
  risk_level:
  activation: []
  exclusions: []
  inputs: []
  outputs: []
  capabilities: []
  memory: false
  human_approval: conditional
  maintainer: AEOS
  governance: CodENavi
```

Do not encode runtime-owned authority in skill metadata.

## Validation rules

A skill is not complete until all applicable checks pass:

- paths and references resolve;
- metadata is internally consistent;
- no placeholders remain in released artifacts;
- examples match the current project/runtime;
- tests verify behavior/contracts rather than implementation trivia;
- executable helpers have explicit error handling;
- risky operations define rollback/approval expectations;
- generated evidence contains no secret values;
- the skill introduces no additional agent identity or delegation model;
- current workspace guards pass.

## Evidence

Evidence may include file paths, validation output, test reports, diffs, schema validation, current documentation citations and artifact hashes. Confidence alone is not evidence.

## Failure behavior

Return `BLOCKED` rather than fabricate success when mandatory inputs, permissions, tools, approval, current documentation or deterministic verification are unavailable.

Do not silently swallow realistic errors. State the blocker and its impact.

## Context economy

Load only the context necessary for the requested capability. Prefer pointers to code and progressive references over copied repositories. Use `.notebook/` for validated project intelligence and keep notes current.

## Completion contract

A skill-factory mission is complete only when the generated capability is minimal, governed, discoverable, testable where executable, free of conflicting local authority and compatible with the current CodENavi single-agent runtime.
