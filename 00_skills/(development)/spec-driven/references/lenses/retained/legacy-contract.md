# Local AGENT contract — spec-driven

This file specializes root `AGENT.md`; it does not define another agent identity.

## Lifecycle

Follow `BRIEFING -> RECON -> PLAN -> EXECUTE -> VERIFY -> DEBRIEF`. Map Specify/Design/Tasks/Execute onto that lifecycle; do not invent a second agent.

## Delegation

Source "sub-agent" workers and the Verifier are lenses / sequential work units of `codenavi-agent`. Never create, register or spawn another agent identity.

## Mutation

Approved specs authorize local implementation only. Remote, destructive or production actions require an explicit user go-ahead for that action. Commits occur only when the user authorizes them.
