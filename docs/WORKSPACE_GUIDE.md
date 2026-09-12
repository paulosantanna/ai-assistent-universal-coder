# AEOS Workspace Operating Guide

## 1. Purpose

This guide explains how to operate AEOS as a reusable engineering workspace rather than as a collection of isolated prompts.

AEOS exists to turn an engineering objective into a governed, evidence-backed lifecycle:

`understand → decide → change → verify → document → retain validated knowledge`

All work inherits `AGENT.md` and the CodENavi lifecycle.

## 2. Mental model

Think of the workspace as six cooperating planes:

1. **Governance plane** — `AGENT.md`, policies, capabilities, Judge, approvals and security constraints.
2. **Intelligence plane** — `.notebook`, repository evidence, memory and promoted knowledge.
3. **Reasoning plane** — agents, Critical Thinking, planning and architectural decision support.
4. **Execution plane** — skills, MCPs, LCPs and bounded tools.
5. **Verification plane** — builds, tests, evals, security/performance checks and evidence.
6. **Value plane** — documentation, modernization, delivery acceleration, reliability and business outcomes.

A skill may participate in several planes, but it never bypasses governance.

## 3. First use on any project

### BRIEFING

Define:

- desired outcome;
- business/technical reason;
- acceptance criteria;
- target repository/environment;
- constraints and non-goals;
- risk level;
- whether production/destructive access is involved.

### RECON

Read in order:

1. root `AGENT.md`/`AGENTS.md`;
2. `.notebook/INDEX.md` if present;
3. repository README and local agent instructions;
4. build manifests and workspace configuration;
5. code entry points and tests;
6. CI/CD and infrastructure;
7. relevant skills and MCP contracts;
8. authoritative documentation when framework/provider behavior matters.

Do not start implementation while material unknowns remain hidden.

### PLAN

Create the smallest sufficient plan. Every step should have:

- objective;
- evidence/input;
- change or analysis action;
- verification;
- rollback/stop condition when risky.

### EXECUTE

Use the narrowest skill/tool capable of the operation. Preserve repository conventions. Do not perform opportunistic unrelated refactoring.

### VERIFY

Run repository-native checks. At minimum consider:

- build/type/static checks;
- unit tests;
- integration/contract tests;
- security checks;
- architecture/invariant checks;
- performance checks when the change affects a hot path;
- documentation consistency.

### DEBRIEF

Record:

- what changed;
- evidence/results;
- unresolved risks;
- changed assumptions;
- documentation updates;
- `.notebook` updates;
- handoff/next action.

## 4. Using skills correctly

Skills are specialist contracts, not permission escalation.

A good invocation supplies:

- the outcome;
- repository or bounded scope;
- known constraints;
- required evidence;
- expected output;
- definition of done.

Prefer compositions. For example, a modernization mission can use repository mapping, `java-version-expert`, dependency analysis, architecture analysis, security evaluation, implementation, `pr-reviewer`, `docs-writer` and notebook intelligence in sequence.

## 5. Adding a new repository to the workspace

Do not copy the whole repository into notes. Map it using `docs/REPOSITORY_MAPPING.md`.

The workspace should be able to answer after mapping:

- What does this repository own?
- How is it built and run?
- What are its entry points?
- Which components depend on which?
- Which external systems does it communicate with?
- Where does data enter, move and persist?
- What are its trust boundaries?
- How is it tested and deployed?
- What are its critical failure modes?
- Where are the most expensive technical risks?
- Which facts are observed and which remain inferred/unknown?

If these questions cannot be answered, the map is incomplete.

## 6. Documentation lifecycle

Documentation is generated from evidence and evolves with the implementation.

Recommended documentation set for a mature mapped repository:

```text
docs/
├── README-or-overview.md
├── architecture/
│   ├── context.md
│   ├── containers.md
│   ├── components.md
│   ├── data-flow.md
│   └── decisions/
├── development/
│   ├── local-setup.md
│   ├── build-test.md
│   └── conventions.md
├── operations/
│   ├── deployment.md
│   ├── observability.md
│   ├── troubleshooting.md
│   └── rollback-recovery.md
├── security/
│   ├── trust-boundaries.md
│   └── controls.md
└── integrations/
    └── ...
```

Generate only artifacts justified by the repository. Empty template sprawl is not value.

## 7. Adding or incrementing skills

A new skill should exist because it adds a distinct reusable capability, not because another prompt would be convenient.

Before adding one:

1. search existing registry/skills for overlap;
2. define mission and non-goals;
3. identify owner agent and risk level;
4. use existing capability IDs only, or formally extend the capability model;
5. define inputs/outputs and evidence;
6. define security boundaries;
7. define verification/evals;
8. declare CodENavi governance;
9. register the skill;
10. update user-facing documentation if the capability changes how the workspace is operated.

After adding a skill, run the applicable AEOS guards and verification suite.

## 8. Documentation generated by skills

Use `docs-writer` after evidence-producing skills, not before them.

Example pipeline:

`RECON → architecture/code/data analysis → evidence → docs-writer → verify links/claims → notebook update`

This prevents polished but fictional documentation.

When a new skill is introduced, document:

- what problem it solves;
- when to use it;
- when not to use it;
- required inputs/access;
- outputs;
- composition with other skills;
- security/risk constraints;
- verification procedure;
- one realistic workflow.

## 9. Full-workspace value loop

The workspace produces maximum value when it closes the feedback loop:

```text
Repository/Problem
      ↓
Recon + Mapping
      ↓
Architecture / Code / Data / Security / Performance Analysis
      ↓
Prioritized Decision + Plan
      ↓
Governed Implementation
      ↓
Tests + Evals + Review
      ↓
Documentation + Evidence
      ↓
Notebook / Validated Memory
      ↺
```

This reduces repeated reconnaissance, stale tribal knowledge and unverified AI-generated changes.

## 10. Common high-value missions

### New repository onboarding

Map repository → generate architecture/development docs → identify risk/hotspots → seed `.notebook` → establish verification baseline.

### Legacy modernization

Map current state → identify runtime/dependency constraints → define target state → incremental migration → regression/performance/security verification → ADR/docs update.

### Incident/root-cause work

Map failure path → collect evidence → reproduce → identify root cause and blast radius → minimal correction → regression test → operational documentation/notebook gotcha.

### Security hardening

Map trust boundaries → dependency/config/code review → prioritize exploitable paths → guarded remediation → security tests/evals → control documentation.

### Performance optimization

Measure baseline → identify bottleneck → change one causal factor → remeasure → reject regressions → record reproducible evidence.

### Documentation recovery

Map code/runtime/deployment first → compare existing docs to observed state → remove stale claims → generate missing high-value docs → create maintenance pointers.

## 11. Commands

Core:

```bash
npm run aeos:bootstrap
npm run aeos:verify
npm run aeos:verify:full
```

Governance:

```bash
npm run aeos:guard:python-workspace
npm run aeos:guard:skill-adapters
npm run aeos:guard:critical-thinking
npm run aeos:guard:codenavi
```

Java matrix when applicable:

```bash
npm run test:java
npm run test:matrix:full
```

KingHost adapter smoke test when applicable:

```bash
npm run aeos:kinghost:smoke
```

## 12. Definition of a healthy workspace

A healthy AEOS workspace has:

- one clear constitutional source of truth;
- no stale duplicate agent instructions;
- skills registered and bounded by real capabilities;
- no secrets in durable artifacts;
- notebook knowledge that points to authoritative sources;
- reproducible verification;
- documentation that reflects observed implementation;
- explicit unknowns rather than invented certainty;
- measurable engineering outcomes.
