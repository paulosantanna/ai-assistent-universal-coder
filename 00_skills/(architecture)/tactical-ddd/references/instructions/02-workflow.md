<!-- Package: 00_skills/(architecture)/tactical-ddd; relative command/resource examples resolve from that package or workspace root. -->

## Workflow

Determine the user's intent first:

| Intent | Phases to run |
|--------|--------------|
| "validate / review / check / is this correct?" | Phase 1 + 2 only → report findings, ask before refactoring |
| "fix / refactor / improve / clean up" | Phase 1 + 2 + 3 |
| "how should I design / model this?" | Load [reference.md](../tlc/reference.md) directly |

### Phase 1 — Detect
Load [detection.md](../tlc/detection.md) and scan the target code for anemia signals. Produce a severity score and list of affected classes.

### Phase 2 — Assess
For each affected class, determine the correct building block:

| Has unique identity tracked over time? | Has invariants tying multiple objects? | → Building Block |
|----------------------------------------|----------------------------------------|-----------------|
| Yes | — | **Entity** |
| No | — | **Value Object** |
| Yes (root) + children with shared invariants | Yes | **Aggregate** |
| Operation spans multiple Aggregates/doesn't belong to any | — | **Domain Service** |

Prefer Value Objects over Entities. Prefer small Aggregates over large ones.

**If intent was validate/review**: stop here. Report findings using the output format below. Ask "Would you like me to apply these fixes?" before proceeding.

### Phase 3 — Refactor
Load [refactoring.md](../tlc/refactoring.md) for step-by-step moves. Apply in this order:
1. Replace setter chains with a single expressive method
2. Move service logic into the Aggregate that owns it
3. Add business guards at the top of each method
4. Publish a Domain Event after each successful state change
5. Replace primitive types with Value Objects

For deep pattern questions (boundary design, event modeling, service vs. entity decision), load [reference.md](../tlc/reference.md).

---
