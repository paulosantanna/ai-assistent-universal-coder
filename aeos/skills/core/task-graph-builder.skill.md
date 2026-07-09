# Skill: task-graph-builder

## Mission

Build a deterministic task graph from a playbook and objective.

## Allowed Actions

- Read AEOS config and registries.
- Read evidence refs.
- Generate reports.
- Generate task/context/audit artifacts inside `.aeos`.

## Forbidden Actions

- Direct tool access.
- Scope expansion.
- Secret exposure.
- Self-approval.
- Direct mutation of project files.

## Required Evidence

- input refs
- generated artifact refs
- policy decision refs
- task graph refs when applicable
- agent trace refs when applicable

## Quality Gates

- Facts cite evidence.
- Assumptions are marked.
- Risks are classified.
- Outputs match schema.
- No raw secrets.
