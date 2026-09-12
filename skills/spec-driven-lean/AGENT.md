# Local AGENT contract — spec-driven-lean

This file specializes root `AGENT.md`; it does not define another agent identity.

## Lifecycle

Follow `BRIEFING -> RECON -> PLAN -> EXECUTE -> VERIFY -> DEBRIEF`. Map Plan/Checks/Build/Verify onto that lifecycle.

## Delegation

Source builder batches and the Verifier are lenses / sequential work units of `codenavi-agent`. The builder never writes `verification.md`.

## Mutation

Approved plan/checks authorize local implementation only. Remote, destructive or production actions require an explicit user go-ahead. Commits occur only when the user authorizes them.
