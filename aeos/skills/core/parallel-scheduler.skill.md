# Skill: parallel-scheduler

## Mission

Create deterministic safe schedules for playbook tasks using dependency graph and read/write sets.

## Allowed Actions

- Read AEOS configs through Tool Router.
- Read registries through Tool Router.
- Read evidence and reports.
- Generate reports under `.aeos/reports`.
- Generate evidence under `.aeos/evidence`.

## Forbidden Actions

- Direct filesystem access.
- Direct MCP invocation.
- Secret exposure.
- Approval bypass.
- Policy bypass.
- Unapproved mutation.
- Unsupported factual claims.

## Required Evidence

- config refs
- registry refs
- tool call refs
- policy decision refs
- permission decision refs
- generated report refs

## Quality Gates

- Facts cite evidence.
- Assumptions are marked.
- Risks are classified.
- Blocking conditions are explicit.
- No raw secrets.
- Judge can validate outputs deterministically.
