<!-- Package: 00_skills/(creation)/create-adr; relative command/resource examples resolve from that package or workspace root. -->

## Common Anti-Patterns to Avoid

### Title as a Question

**BAD**: `# ADR-001: Should we use PostgreSQL?`

**GOOD**: `# ADR-001: Use PostgreSQL for Primary Storage`

Titles should record the decision, not the question. Future readers need to know *what was decided*, not what was considered.

---

### Vague Context

**BAD**:
```
We needed a database and chose PostgreSQL.
```

**GOOD**:
```
Our application requires a relational database with strong ACID guarantees.
The team has deep PostgreSQL experience. MySQL was evaluated but lacks
native support for JSONB columns, which our schema design requires.
Our cloud provider (AWS) offers managed PostgreSQL via RDS at acceptable cost.
```

Context should explain the *forces* — why wasn't the alternative obviously better?

---

### Consequences Without Trade-offs

**BAD**:
```
## Consequences
PostgreSQL is fast and reliable.
```

**GOOD**:
```
## Consequences
- Enables JSONB columns and advanced indexing for our query patterns
- Team expertise means fast onboarding and fewer operational surprises
- Adds operational burden compared to a managed NoSQL service
- Schema migrations require careful planning in a relational model
```

Honest trade-offs are what make ADRs valuable years later.

---

### Editing Instead of Superseding

**BAD**: Editing an old ADR to change the decision after the fact.

**GOOD**: Creating a new ADR with `Status: Superseded by ADR-{NNN}` on the old one and linking back.

ADRs are historical records. The old decision was correct *given what was known at the time*. Superseding preserves that context.

---

### Missing the "Why Not" Rationale

**BAD**:
```
## Decision
We will use Redis for session storage.
```

**GOOD**:
```
## Decision
We will use Redis for session storage. We considered storing sessions in PostgreSQL
(already in our stack) but Redis's built-in TTL support and in-memory performance
make it significantly better suited for high-frequency session reads. The operational
cost of an additional service is justified by the simplified session expiry logic.
```

The rationale is *why this option and not the others* — not just what was chosen.

---
