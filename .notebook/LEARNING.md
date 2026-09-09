# LEARNING

Updated: 2026-09-09

## Validated learnings

### Separate continuity concerns instead of using one oversized memory file
- Context/trigger: long-running workspace work needs state continuity across sessions without contaminating durable memory with transient logs.
- Problem/failure mode: mixing current progress, durable facts, handoff state and generalized lessons creates stale or contradictory context.
- Root cause: different information lifetimes were stored in the same undifferentiated artifact.
- Verified correction/prevention: use four bounded artifacts — HANDOFF, MEMORY, PROGRESS and LEARNING — and cross-link instead of duplicating.
- Reuse scope: all material CodENavi-governed workspaces.
- Evidence: `references/CODENAVI_CONTINUITY_STANDARD.md`
- Confidence: high
- Updated: 2026-09-09
