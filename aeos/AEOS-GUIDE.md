# AEOS Configuration Guide

## Architecture Overview

```
aeos/
  config/           → Central configuration (kernel, capabilities, permissions, policies)
  registries/       → Registries for all pluggable components
  playbooks/        → Operational procedures that orchestrate multiple skills
  skills/           → Specialized capabilities with explicit contracts
    core/           → Built-in skills
    templates/      → Skill templates for generation
    generated/      → Auto-generated skills
  mcps/             → Model Context Providers (external connectors)
  lcps/             → Local Context Packs (rules, context, memory)
  agents/           → Agent definitions (roles, permissions, constraints)
  evidence/         → Execution evidence artifacts
  reports/          → Generated reports
  memory/           → Project memory (ADRs, patterns, conventions)
```

## Layer Responsibilities

| Layer     | Purpose | Analogy |
|-----------|---------|---------|
| **Playbook** | Orchestrates multiple skills to complete an operation | A recipe |
| **Skill** | Teaches how to execute a specific capability | A chef's technique |
| **MCP** | Connects the agent to external tools (filesystem, git, shell) | A kitchen appliance |
| **LCP** | Delivers controlled context (rules, stack, memory) | A cookbook reference |

## How to Add a New Playbook

1. Create the playbook file: `aeos/playbooks/<id>.playbook.md`
2. Follow the required structure: Objective, Preconditions, Agents, Skills, MCPs, Steps, Blocking Conditions, Outputs
3. Register it in: `aeos/registries/playbooks.registry.yaml`
4. Add `playbooks` entry with: id, name, path, risk_level, required_agents, required_skills, required_lcps, allowed_mcps

## How to Add a New Skill

1. Create the skill file: `aeos/skills/core/<id>.skill.md`
2. Follow the required structure: Mission, Allowed Actions, Forbidden Actions, Inputs, Outputs, Evidence Required, Prompt Contract, Quality Gates
3. Register it in: `aeos/registries/skills.registry.yaml`
4. Add `skills` entry with: id, path, version, owner_agent, risk_level, capabilities
5. If it needs new capabilities, add them to: `aeos/config/capabilities.yaml`
6. Grant agent permissions in: `aeos/config/permissions.yaml`

## How to Add a New MCP

1. Create the MCP config file: `aeos/mcps/<id>.mcp.yaml`
2. Define: id, transport, tools, security constraints, redaction rules and `prompt_contract`
3. Register it in: `aeos/registries/mcps.registry.yaml`
4. Add `mcps` entry with: id, type, config, risk_level, capabilities, approval_required
5. Grant agent access in: `aeos/config/permissions.yaml` (agent_to_mcp section)

## How to Add a New LCP

1. Create the LCP file: `aeos/lcps/<id>.lcp.yaml`
2. Define: id, priority, scope, applies_when, rules, required_evidence, forbidden
3. Register it in: `aeos/registries/lcps.registry.yaml`
4. Add `lcps` entry with: id, path, priority, scope, applies_to

## Kernel Load Order

1. Load `aeos/config/aeos.config.yaml`
2. Load `aeos/config/capabilities.yaml`
3. Load `aeos/config/policies.yaml`
4. Load `aeos/config/permissions.yaml`
5. Load registries (agents, skills, playbooks, mcps, lcps)
6. Load selected LCPs (by priority, highest first)
7. Resolve playbook
8. Resolve required skills
9. Resolve required MCPs
10. Check permissions (deny-all default)
11. Execute in dry-run mode
12. Collect evidence
13. Judge validates
14. Only then allow controlled execution

## Security Principles

- No agent accesses filesystem, git, shell, browser, DB, or API directly
- All external access goes through MCP → Permission Engine → Policy Check
- No secrets in code, logs, prompts, traces, reports, or versioned files
- Destructive actions require human approval
- Judge is independent of implementer
- Evidence is required for every action
- Runtime prompts follow `aeos/docs/PROMPT_CONTRACT.md`

## Verification

Use the repository-level verifier before promoting AEOS changes:

```bash
npm run aeos:verify
npm run aeos:verify:full
```

The quick suite validates the AEOS doctor, registry and core tests. The full suite also validates skills, MCP packages, the language server and the TypeScript runtime build.

## Portable Runtime

AEOS resolves local state from the repository by default so the folder can move
between machines or run from removable storage.

```bash
npm run aeos:bootstrap
npm run aeos:bootstrap:deps
```

Portable state lives under `.aeos/` unless overridden by `AEOS_PORTABLE_HOME`.
See `aeos/docs/PORTABLE_RUNTIME.md` for the full contract.

## Execution Contract

The Python execution layer exposes `ExecutionRequest`, `ExecutionResult`, `SkillResolver` and `SkillRunner` under `aeos.core.execution`.

The first supported vertical slice is governed skill dry-run:

```bash
python -m aeos.cli.main skill run repo-scanner --dry-run --target .
```

This resolves the skill from the registry, validates the contract and required inputs, writes runtime evidence under `.aeos/evidence/<execution_id>/`, and returns a structured execution result without running external tools.
