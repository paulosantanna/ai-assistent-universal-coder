# AEOS Memory Model

## Memory Types

```text
semantic/
  general technical knowledge

architectural/
  architecture decisions, ADRs, patterns

procedural/
  how this project builds, tests, deploys, rolls back

episodic/
  executions, incidents, failures, PRs, bugfixes

operational/
  repos, environments, branches, pipelines

lessons_learned/
  what failed and what must not repeat

do/
  preferred patterns

dont/
  anti-patterns and forbidden practices
```

## Rules

- Secrets are never stored in memory.
- Memory updates require evidence.
- Lessons learned must include cause, impact, correction, and prevention.
