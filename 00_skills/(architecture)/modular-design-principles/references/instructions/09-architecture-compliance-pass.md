<!-- Package: 00_skills/(architecture)/modular-design-principles; relative command/resource examples resolve from that package or workspace root. -->

## Architecture compliance pass

Use for **reviews** or **audits** without assuming tooling. Treat items as **signals**, not proof — confirm with domain experts.

### Dependency and API signals

- **Inbound vs outbound:** Dependencies should align with your chosen architecture (e.g. domain at the center, adapters outside). **Inward** leaks of infrastructure types into core logic are a smell.
- **Public surface:** Can you list **exported** operations/events/types without including storage or internal services? If not, boundaries are leaky.
- **Neighbor imports:** Types or clients from **module A** used in **module B** — are they only **contract** types, or persistence/implementation types?

### Persistence and data signals

- **Reach-through:** References to another context’s **physical** data (schema, collection, bucket name) outside an agreed contract.
- **Naming collisions:** Same logical name for different things, or shared global IDs without a documented mapping rule.
- **Transaction ownership:** Writes that span contexts without a clear **saga**, **outbox**, or **single-owner** rule and documented failure cases.

### Operational signals

- **Blame:** Incidents where “we don’t know which module owns this row/behavior” → ownership or observability gap.
- **Cascades:** One dependency’s slowdown or failure takes down unrelated user journeys → missing **timeouts**, **bulkheads**, or **degradation** paths.

### Severity heuristic (for reporting)

| Tier | Meaning |
|------|--------|
| **P0** | Data corruption risk, security boundary violation, or cross-context persistence with no contract |
| **P1** | Unclear ownership, leaky public API, missing failure semantics at boundaries |
| **P2** | Observability gaps, composability smells, tech debt that increases future coupling |

**Maturity note:** Scoring is **qualitative** unless the team defines numeric gates. Use trends: fewer P0/P1 over time, clearer contracts.

---
