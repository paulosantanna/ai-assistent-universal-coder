# Skill-Driven Documentation

## Principle

AEOS documentation must be derived from repository evidence and verified behavior. Skills accelerate documentation; they do not authorize invention.

The canonical sequence is:

`map → analyze → collect evidence → write → verify → index → maintain`

## Roles of relevant skills

### `codenavi`

Enforces the workspace lifecycle and disciplined reconnaissance/planning/execution/verification/debrief behavior.

### `notebook-intelligence`

Maintains compact project intelligence and pointers needed for future missions.

### `docs-writer`

Transforms verified evidence into human-readable repository, architecture, development and operations documentation.

### `pr-reviewer`

Checks changes for correctness, regressions, missing evidence and documentation impact.

### `dependency-updater`

Produces evidence for dependency/version changes that may require compatibility, migration or operational documentation updates.

### `java-version-expert`

Adds version-aware Java/JDK reasoning to modernization and compatibility documentation.

### Analysis/security/performance skills

Provide evidence for architecture, code, security, data and performance documents. Their findings should remain traceable to observed code/config/runtime evidence.

## Creating documentation for a newly mapped repository

1. Complete the relevant sections of `REPOSITORY_MAPPING.md`.
2. Identify the intended audience: developer, architect, SRE/operator, security reviewer, product/domain owner or mixed.
3. Select only useful artifacts.
4. Feed verified evidence to `docs-writer`.
5. Mark uncertain relationships explicitly.
6. Validate commands, paths, versions and links against the repository.
7. Run applicable build/tests where documentation makes behavioral claims.
8. Add durable pointers to `.notebook`.
9. Review documentation in the same PR as the implementation when coupled.

## Incrementing documentation when a new skill is added

Every new skill must answer whether it changes workspace usage.

If yes, update documentation with this contract:

```text
Skill ID:
Problem solved:
When to use:
When not to use:
Owner agent:
Risk level:
Capabilities:
Required inputs/access:
Evidence sources:
Outputs:
Security constraints:
Composes with:
Verification:
Example workflow:
```

Do not duplicate the full `SKILL.md` into general documentation. Link to the authoritative skill and document the user-facing operating model.

## Documentation impact matrix

| Change | Likely docs to inspect |
|---|---|
| New skill | README, workspace guide, skill workflows |
| New MCP/tool | integration/tooling docs, security model |
| Runtime/JDK upgrade | setup, build, deployment, compatibility |
| New API/event | architecture, integrations, data flow |
| DB/schema change | data model, migration/rollback, operations |
| Auth/security change | trust boundaries, controls, runbooks |
| Deployment change | CI/CD, operations, rollback/recovery |
| Performance change | performance baseline, SLO/operational docs |
| Incident fix | troubleshooting, gotcha/notebook, regression evidence |

## Architecture documentation

Architecture docs should answer decisions and relationships, not merely list folders.

Recommended views:

- **Context:** actors and external systems.
- **Containers/services:** deployable/runtime boundaries.
- **Components:** important internal responsibilities.
- **Data flow:** how critical information moves and persists.
- **Trust boundaries:** where privilege/identity/data sensitivity changes.
- **Deployment:** runtime topology and infrastructure relationships.
- **Failure propagation:** how critical dependencies fail and recover.

Label inferred/unknown relationships. Avoid diagrams that imply certainty unsupported by code/runtime evidence.

## ADR generation

Generate an ADR when a decision is durable and has meaningful alternatives/trade-offs.

An ADR should capture:

- context/problem;
- decision;
- alternatives considered;
- why the decision was selected;
- consequences/trade-offs;
- security/operational implications;
- evidence/reference;
- status/date.

Do not create ADRs retroactively for trivial implementation details.

## Runbook generation

Operational documentation must be executable by another engineer.

Include:

- trigger/symptoms;
- prerequisites/access;
- safe diagnostics;
- expected observations;
- decision points;
- mitigation/recovery;
- rollback;
- escalation/stop conditions;
- verification after recovery.

Never embed credentials or production secret values.

## Preventing stale documentation

Documentation drift is controlled by:

1. same-change documentation updates;
2. notebook pointers to authoritative implementation;
3. PR review checking documentation impact;
4. commands/versions copied from manifests rather than memory;
5. explicit `Updated:` metadata where useful;
6. deleting or deprecating invalid documentation instead of accumulating contradictions.

## Verification checklist

Before declaring generated documentation complete:

- paths exist;
- commands match current scripts/build system;
- versions match manifests/toolchains;
- architecture claims have evidence;
- no secrets/PII leaked;
- links resolve within the repository;
- examples are consistent with actual interfaces;
- inferred facts are labeled;
- old contradictory docs are updated/deprecated;
- `.notebook` contains only durable intelligence, not duplicated prose.
