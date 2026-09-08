# CodENavi Full Workspace Governance Coverage

Governance: CodENavi Full Workspace v2

This document explains how AEOS guarantees that legacy and future artifacts inherit the same operating standard without duplicating the constitution into every file.

## Coverage rule

`aeos/governance/workspace-governance.manifest.json` declares:

`coveragePolicy = all-tracked-files-governed-by-default`

The CI guard `scripts/aeos-full-workspace-standard-guard.mjs` enumerates the real repository with `git ls-files`. Every tracked file is governed by the root `AGENT.md` unless it is an explicitly ignored generated/cache/evidence artifact. There is no opt-in list of old files that can silently be forgotten.

The mandatory lifecycle is:

**BRIEFING → RECON → PLAN → EXECUTE → VERIFY → DEBRIEF**

## Inheritance model

```text
AGENT.md
  ↓
references/CODENAVI_FULL_WORKSPACE_STANDARD.md
  ↓
nearest subtree AGENT.md
  ↓
artifact-specific contract
  ↓
runtime capability/policy/Judge/approval enforcement
```

Local contracts specialize the root standard and cannot weaken it.

## Coverage matrix

| Surface | Local specialization | Core enforcement |
|---|---|---|
| Agents | `aeos/agents/AGENT.md` | registry/capability/handoff/runtime |
| Subagents | `aeos/subagents/AGENT.md` | delegation scope + capability gates |
| Canonical skills | `skills/AGENT.md` | registry + SkillExecutor/tool router |
| Legacy/generated AEOS skills | `aeos/skills/AGENT.md` | registry + runtime capability policy |
| External-agent skill mirrors | `.agents/AGENT.md` | canonical skill contract wins on conflict |
| Playbooks | `aeos/playbooks/AGENT.md` | PlaybookEngine + Judge/approval/rollback |
| MCPs | `aeos/mcps/AGENT.md` | tool routers/adapters + allowlists |
| LCPs | `aeos/lcps/AGENT.md` | registry/context validation |
| LSP/language server | `packages/aeos-language-server/AGENT.md` | parser/index/server tests |
| Registries/overlays | `aeos/registries/AGENT.md` | merged registry loader/validation |
| Capabilities | `aeos/capabilities/AGENT.md` | registered capability model |
| Network capabilities | `aeos/network-capabilities/AGENT.md` | deny-by-default network boundaries |
| Policies/config | `aeos/policies/AGENT.md`, `aeos/config/AGENT.md` | runtime policy/permissions |
| Security | `aeos/security/AGENT.md` | security gates/evals/Judge |
| Connectors/integrations | `aeos/connectors/AGENT.md`, `aeos/integrations/AGENT.md` | provider/contract validation |
| Blueprints | `aeos/blueprints/AGENT.md` | current/target state evidence |
| Schemas | `aeos/schemas/AGENT.md` | schema/runtime compatibility validation |
| Evals/tests | `aeos/evals/AGENT.md`, `tests/AGENT.md` | repository test/eval matrix |
| Memory/knowledge | `aeos/memory/AGENT.md`, `aeos/knowledge/AGENT.md`, `knowledge/AGENT.md` | governed promotion + provenance |
| Knowledge sources | `aeos/knowledge-sources/AGENT.md` | freshness/provenance checks |
| Impact analysis | `aeos/impact-analysis/AGENT.md` | dependency/blast-radius evidence |
| Runtime | `runtime/AGENT.md`, `aeos/runtime/AGENT.md` | fail-closed executors/routers |
| Scripts/guards | `scripts/AGENT.md` | deterministic exit status + CI |
| CI/CD | `.github/AGENT.md` | AEOS Enterprise CI |
| Packages | `packages/AGENT.md` | package-local build/test contracts |
| Templates | `templates/AGENT.md` | representative generated-output validation |
| Documentation | `docs/AGENT.md` | evidence-backed docs + stale-doc correction |
| Provider adapters | `kinghost-commerce-mcp/AGENT.md`, `aura-voice-tool/AGENT.md` | adapter-specific runtime gates |
| Editor/workspace config | `.vscode/AGENT.md` | documented project toolchain/security |
| Legacy runtime | `AEOS_RUNTIME_MVP_v1/AGENT.md` | current root standard overrides legacy rules |

## What “migrated” means for legacy files

A legacy skill/playbook/MCP does not need a copied 100-line CodENavi block to be migrated. Its nearest `AGENT.md` is a binding inherited contract. This avoids hundreds of stale duplicates while allowing the CI guard to prove coverage mechanically.

When an individual legacy artifact is materially edited, its local file should also be normalized toward the current explicit contract structure. Inheritance remains mandatory even before that local normalization.

## CI gate

`npm run aeos:guard:full-workspace`

The guard verifies:

- root constitutional files exist;
- the full standard contains every required artifact family;
- every tracked file is governed by default;
- every required subtree has a local contract;
- every local contract points to the root standard;
- stale nested `AGENT.md`/`AGENTS.md` files cannot remain outside CodENavi;
- artifact-family counts are reported as evidence.

The gate is part of both `aeos:bootstrap` and `aeos:verify`. Therefore a new tracked artifact cannot be merged as “healthy” while escaping root governance.

## Exceptions

Only explicitly declared generated/cache/evidence paths may be excluded from per-file coverage. Exclusion does not grant them authority: generated output remains untrusted until consumed through a governed component.

Any new exception is itself a governance change and requires review.
