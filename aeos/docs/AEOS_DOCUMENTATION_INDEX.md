# AEOS Documentation Index

This repository keeps AEOS documentation in three explicit classes.

## Living Specs

Path: `aeos/docs/specs/`

These documents define the current AEOS operating model and should remain maintained:

- `AEOS_CONSTITUTION.md`
- `AEOS_KERNEL.md`
- `AEOS_POLICY_ENGINE.md`
- `AEOS_PERMISSION_MODEL.md`
- `AEOS_SECURITY_MODEL.md`
- `AEOS_SKILL_CONTRACT.md`
- `AEOS_PLAYBOOK_CONTRACT.md`
- `AEOS_AGENT_CONTRACT.md`
- `AEOS_AGENT_MESSAGE_PROTOCOL.md`
- `AEOS_AGENT_ORCHESTRATION.md`
- `AEOS_SUBAGENT_SYSTEM.md`
- `AEOS_TASK_DELEGATION_CONTRACT.md`
- `AEOS_CONTEXT_ROUTING.md`
- `AEOS_ECOSYSTEM_SCHEMA.md`
- `AEOS_MCP_CONNECTOR_SPEC.md`
- `AEOS_MCP_RUNTIME_CONTRACT.md`
- `AEOS_MCP_SECURITY_PROFILE.md`
- `AEOS_MEMORY_GOVERNANCE.md`
- `AEOS_MEMORY_MODEL.md`
- `AEOS_TOOL_ROUTER_RUNTIME.md`
- `AEOS_WORKBENCH_PROFILES.md`
- `AEOS_PRODUCTION_READY_CHECKLIST.md`

## Runtime Prompt Contract

Path: `aeos/docs/PROMPT_CONTRACT.md`

This document defines the canonical prompt discipline for skills, MCPs, LSP commands, CLI commands and reusable prompt packs. Runtime-facing instructions should reference or implement it when they affect execution behavior.

## Historical Evolution

Path: `aeos/docs/archive/evolution/`

These files are useful for traceability, but they should not be treated as current runtime instructions:

- versioned roadmap files;
- overlay install summaries;
- old runtime expansion notes;
- judge rule snapshots.

## Enterprise Drafts

Path: `aeos/docs/archive/enterprise-drafts/`

These files contain broader production and enterprise ideas. Keep them as reference material until they are promoted into living specs, runtime code, or tested playbooks.

## Large Generated Manuals

Paths:

- `aeos/docs/manuals/`
- `aeos/docs/production/`

These manuals are retained, but should be treated as generated reference material. Before using one as an implementation authority, promote the relevant rule into:

- a living spec;
- a registry entry;
- a playbook;
- a skill;
- a test;
- or a runtime policy.

## Root Directory Rule

Do not add new `AEOS*.md` files at repository root.

New AEOS documentation must go into one of:

- `aeos/docs/specs/`
- `aeos/docs/archive/evolution/`
- `aeos/docs/archive/enterprise-drafts/`
- `aeos/docs/manuals/`
- `aeos/docs/production/`
- `design/`

If a document affects runtime behavior, update the relevant registry, config, tests, or runtime implementation in the same change.
