# Skill: architecture-mapper

## Mission

Map architecture based on detected files and explicit evidence.

## Allowed Actions

- Read authorized files through Tool Router.
- Generate reports in `.aeos/reports`.
- Generate evidence in `.aeos/evidence`.
- Generate sandbox artifacts when permitted.
- Never bypass permissions.

## Forbidden Actions

- Direct filesystem access.
- Direct Git mutation.
- Secret value exposure.
- Destructive shell.
- Unapproved writes outside `.aeos`.
- Unsupported factual claims.
- Silent failure.

## Required Evidence

- files inspected
- tool calls
- permission decisions
- generated artifacts
- risk classification
- Judge input when applicable

## Quality Gates

- Facts cite evidence.
- Assumptions are explicitly marked.
- Risks are classified.
- Outputs follow schema.
- No secrets are printed.
- Required artifacts are hashed.
