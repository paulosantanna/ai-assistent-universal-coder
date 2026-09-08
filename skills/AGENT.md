# AEOS Canonical Skills / Skill Factory contract

Governance: CodENavi Full Workspace v2

This subtree inherits root `AGENT.md` and `references/CODENAVI_FULL_WORKSPACE_STANDARD.md`.

All canonical skills, the Skill Factory, templates and generated skill packages follow **BRIEFING → RECON → PLAN → EXECUTE → VERIFY → DEBRIEF**.

## Skill Factory identity

The Skill Factory converts repeated engineering intent into governed, reusable skill packages. The product is not a prompt; the product is a bounded, validated and maintainable capability contract.

## Mandatory skill contract

Every new or materially revised skill must define or inherit:

- name/id and mission;
- activation criteria and exclusions/non-goals;
- inputs and scope boundaries;
- outputs and evidence;
- owner agent and risk level;
- required registered capabilities;
- tool/MCP/LCP/LSP dependencies;
- freshness requirements for APIs/frameworks/models/providers;
- security/secret handling;
- failure/stop/escalation conditions;
- verification/evals;
- handoff/debrief/documentation/notebook impact.

## Design rules

1. Search for existing overlapping capabilities before creating another skill.
2. Prefer one cohesive reusable capability over prompt duplication.
3. Use the simplest sufficient architecture; no speculative modules or dependencies.
4. Skill text does not grant authority. Runtime capability/policy/Judge/approval controls remain authoritative.
5. Declarative-only skills must not claim executable behavior until adapters/runtime wiring and tests prove it.
6. Verify current framework/API/model behavior against authoritative sources when freshness matters.
7. Tests/evals verify contracts and realistic behavior, not incidental implementation details.
8. No secrets/tokens/cookies/passwords/private keys in skills, examples, notebook, evidence or generated files.
9. Generated code follows repository-native style and surgical-change rules.
10. High-risk validation requires an independent validation pass; generators do not self-approve critical work.

## Skill Factory handoff

Designer → generator:

```yaml
skill_design:
  name:
  slug:
  mission:
  non_goals:
  activation:
  exclusions:
  inputs:
  outputs:
  owner_agent:
  risk_level:
  capabilities:
  dependencies:
  evidence:
  freshness:
  security:
  validation_rules:
```

Generator → validator:

```yaml
validation_request:
  package_path:
  expected_slug:
  registered_path:
  owner_agent:
  risk_level:
  capabilities:
  tests_required:
  manifest_required:
  runtime_wiring_required:
```

## Stop conditions

Stop/fail closed when:

- user intent cannot be represented safely;
- requested authority exceeds registered capabilities;
- destructive/production behavior lacks required approval;
- required tools are unavailable or unsupported;
- current API/provider behavior cannot be verified for a high-risk action;
- validation/evals fail;
- generated structure contradicts the declared contract;
- a duplicate/overlapping skill would create governance ambiguity.

## Existing skills

All legacy skills under `skills/` inherit this contract immediately even if their original text predates CodENavi. When an old skill is materially touched, normalize its own contract toward this structure instead of preserving stale conventions.
