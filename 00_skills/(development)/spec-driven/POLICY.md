# Spec-Driven Policy

## Risk classes

- read_only: inspect existing `.specs/` artifacts.
- low: write or refine spec/design/tasks without repository mutation.
- medium: local implementation against an approved spec.
- high: commits, test mutation, multi-file architecture change.
- destructive: push, deploy, production data change — explicit per-action approval.

## Workflow policy

Auto-size depth from feature scope. Specify and Execute are required. Design and Tasks are skipped only when the sizing table allows it. Independent `VerifierLens` is never optional after the last task.

## Commit policy

Atomic per-task commits apply only after explicit user authorization to commit. Never `--no-verify`, force-push or skip hooks.

## Security policy

Do not persist secrets in `.specs/`, evidence, notebook or chat. Do not weaken tests to unblock a gate.
