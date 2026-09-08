# AEOS — AI Engineering Operating System

AEOS is a governed AI-first engineering workspace for understanding repositories, planning changes, executing software work, validating outcomes, preserving project intelligence and coordinating agents, skills, MCPs, LCPs and tools.

It is not only a prompt collection. The workspace is designed as an engineering operating system with constitutional governance, capability routing, evidence, memory, security gates, repository intelligence and reusable specialist skills.

## Start here

Read in this order:

1. [`AGENT.md`](AGENT.md) — canonical workspace constitution.
2. [`AGENTS.md`](AGENTS.md) — compatibility entry point for agent-aware tools.
3. [`docs/WORKSPACE_GUIDE.md`](docs/WORKSPACE_GUIDE.md) — complete operating guide.
4. [`docs/REPOSITORY_MAPPING.md`](docs/REPOSITORY_MAPPING.md) — how to onboard and map a repository.
5. [`docs/SKILL_DRIVEN_DOCUMENTATION.md`](docs/SKILL_DRIVEN_DOCUMENTATION.md) — how to generate and continuously improve documentation with skills.
6. [`docs/VALUE_PLAYBOOK.md`](docs/VALUE_PLAYBOOK.md) — how to use the complete workspace to generate engineering and business value.
7. [`.notebook/INDEX.md`](.notebook/INDEX.md) — progressive project intelligence.

## Mandatory execution lifecycle

Every material mission follows:

`BRIEFING → RECON → PLAN → EXECUTE → VERIFY → DEBRIEF`

This means understanding before modification, evidence before claims and verification before completion. Production, destructive and high-impact actions remain subject to AEOS approval, Judge and rollback controls.

## What the workspace does

AEOS combines:

- hierarchical agents and explicit handoffs;
- governed skills and skill routing;
- MCP/tool integration;
- repository and architecture reconnaissance;
- code, dependency, security and performance analysis;
- documentation generation and maintenance;
- progressive `.notebook` knowledge;
- Critical Thinking and evidence generation;
- Chromatic Memory and governed knowledge promotion;
- Java/version expertise and modernization support;
- PR review and dependency maintenance;
- KingHost/site/commerce operations under explicit security gates;
- deny-by-default capability and secret handling.

## Quick start

```bash
npm ci
npm --prefix runtime ci
npm run aeos:bootstrap
npm run aeos:verify
```

For the broader verification matrix:

```bash
npm run aeos:verify:full
```

Java toolchain validation, when required:

```bash
npm run test:java
```

## Mapping a repository

A repository should not be modified before it has a minimum evidence-backed map. The mapping workflow is:

1. identify repository purpose and delivery boundary;
2. detect languages, frameworks, build systems and runtime versions;
3. map entry points, modules and dependency direction;
4. map APIs, events, queues, databases and external integrations;
5. map authentication, authorization, secrets and trust boundaries;
6. map CI/CD, infrastructure and deployment topology;
7. map tests, observability and operational controls;
8. identify architectural decisions, hotspots, risks and unknowns;
9. create/update `.notebook` pointers;
10. generate documentation from observed evidence.

The detailed procedure and expected artifacts are in [`docs/REPOSITORY_MAPPING.md`](docs/REPOSITORY_MAPPING.md).

## Documentation as a skill-driven product

Documentation is not treated as a one-time README export. AEOS uses repository evidence plus specialist skills to generate and incrementally maintain:

- repository overview;
- architecture and C4-like views;
- module/component catalog;
- API/integration documentation;
- data-flow and dependency maps;
- build/run/deploy guides;
- security and trust-boundary documentation;
- ADRs and trade-offs;
- troubleshooting/runbooks;
- modernization and technical-debt plans;
- release/PR documentation.

When a new skill adds a real capability, documentation should expose the new workflow, prerequisites, evidence sources, risks, outputs and verification procedure. See [`docs/SKILL_DRIVEN_DOCUMENTATION.md`](docs/SKILL_DRIVEN_DOCUMENTATION.md).

## Generating value with the full workspace

The highest-value use of AEOS is not invoking isolated skills. It is composing them around an engineering outcome.

Example:

`repository mapping → architecture analysis → code/security/performance analysis → prioritized plan → implementation → tests/evals → PR review → documentation → notebook/memory promotion`

This creates a closed engineering loop in which the workspace can understand the system, make a bounded change, prove the result and retain only validated knowledge.

See [`docs/VALUE_PLAYBOOK.md`](docs/VALUE_PLAYBOOK.md) for workflows covering onboarding, modernization, incident reduction, delivery acceleration, security hardening, documentation recovery and technical-debt prioritization.

## Important skills

The enterprise registry includes foundational skills such as `codenavi`, `notebook-intelligence`, `docs-writer`, `pr-reviewer`, `dependency-updater`, `java-version-expert`, security/evaluation skills and governed KingHost/site analysis and operations.

The registry is the source of truth for registered skills:

`aeos/registries/skills.v1_1_enterprise.additions.yaml`

Do not assume that a skill name implies unrestricted permission. Capabilities, risk level, policies, allowlists and runtime gates still apply.

## Security model

Credentials, tokens, cookies, passwords and private keys are runtime secrets only. They must not be committed, copied to `.notebook`, stored in memory/evidence, echoed to stdout or embedded in generated documentation.

AEOS favors secret references, minimum privilege, explicit authorization, deny-by-default capabilities, bounded tools, dry-run, approval and rollback.

## Project intelligence

`.notebook` stores compact, progressive intelligence about the project. It is not a code mirror and not a dumping ground.

Use pointers to authoritative code/docs, one concept per note, observable facts and an `Updated:` date. Stale knowledge is a defect and must be corrected or deprecated when implementation changes.

## Definition of done

A material AEOS mission is complete only when:

- acceptance criteria are satisfied;
- applicable tests/checks have run;
- security and architectural constraints remain valid;
- evidence supports the completion claim;
- documentation affected by the change is updated;
- `.notebook` is updated when project intelligence changed;
- remaining risks/unknowns are explicit;
- handoff/debrief state is clear.

## Documentation index

- [`docs/WORKSPACE_GUIDE.md`](docs/WORKSPACE_GUIDE.md) — operating model and day-to-day usage.
- [`docs/REPOSITORY_MAPPING.md`](docs/REPOSITORY_MAPPING.md) — deterministic repository reconnaissance/onboarding.
- [`docs/SKILL_DRIVEN_DOCUMENTATION.md`](docs/SKILL_DRIVEN_DOCUMENTATION.md) — documentation generation and evolution.
- [`docs/VALUE_PLAYBOOK.md`](docs/VALUE_PLAYBOOK.md) — outcome/value-oriented compositions.
- [`references/CODENAVI_WORKSPACE_STANDARD.md`](references/CODENAVI_WORKSPACE_STANDARD.md) — CodENavi standard.
- [`references/CODENAVI_NOTEBOOK_SPEC.md`](references/CODENAVI_NOTEBOOK_SPEC.md) — notebook specification.

The root `AGENT.md` always has precedence over convenience documentation when rules conflict.
