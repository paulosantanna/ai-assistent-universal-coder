# GitHub Actions Guardian Lenses

This document defines bounded execution contexts owned by the single canonical `codenavi-agent`. Guardians are **not subagents and not independent agent identities**.

## WorkflowGuardianLens

One per relevant workflow run. Tracks workflow/run ID, attempt, triggering SHA, status/conclusion, requiredness, child jobs/checks and evidence refs. It does not mutate code.

## JobGuardianWorkUnit

One per job/matrix child. Tracks job ID/name, matrix dimensions, status/conclusion, failing step, normalized failure fingerprint and root-cause group. It does not mutate code.

## Root-cause specialist lenses

The orchestrating skill may select a bounded lens for Python, Java/Maven, Java/Gradle, Node, Docker, workflow YAML, dependencies, security, infrastructure, testing, performance, release engineering, branch protection or PR governance.

Specialist lenses receive compact redacted evidence packets and never receive credentials.

## Concurrency

Independent root-cause analysis may run in parallel. Mutations touching the same source path, workflow, lockfile, configuration or branch-protection resource are serialized.

## Chief/Staff gate

Before mutation, the selected lens must issue `APPROVED`, `NEEDS_REWORK` or `REJECTED` for the proposed repair. `REJECTED` blocks mutation and `NEEDS_REWORK` requires a revised plan.
