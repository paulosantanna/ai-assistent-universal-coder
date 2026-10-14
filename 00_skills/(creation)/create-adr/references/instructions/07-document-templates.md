<!-- Package: 00_skills/(creation)/create-adr; relative command/resource examples resolve from that package or workspace root. -->

## Document Templates

### MADR Format (Default)

```markdown
# ADR-{NNN}: {Title}

- **Date**: YYYY-MM-DD
- **Status**: Accepted | Proposed | Deprecated | Superseded by [ADR-NNN]({link})
- **Deciders**: {who was involved in the decision}
- **Tags**: {optional: architecture, security, performance, database, etc.}

## Context and Problem Statement

{Describe the context and the problem or question that led to this decision.
2–4 sentences. What situation forced this choice?}

## Decision Drivers

- {Driver 1 — e.g., "Must support 10k concurrent users"}
- {Driver 2 — e.g., "Team has no Go experience"}
- {Driver 3 — e.g., "Must be deployable on-premise"}

## Considered Options

- {Option A}
- {Option B}
- {Option C — "Do nothing / status quo" when relevant}

## Decision Outcome

Chosen option: **"{Option A}"**, because {concise rationale tied to decision drivers}.

### Positive Consequences

- {Benefit 1}
- {Benefit 2}

### Negative Consequences

- {Trade-off 1 — be honest}
- {Trade-off 2}

## Pros and Cons of the Options

### {Option A} ✅ Chosen

- ✅ {Pro 1}
- ✅ {Pro 2}
- ❌ {Con 1}

### {Option B}

- ✅ {Pro 1}
- ❌ {Con 1}
- ❌ {Con 2}

### {Option C}

- ✅ {Pro 1}
- ❌ {Con 1}

## Links

- {Related ADR, RFC, ticket, or documentation}
- Supersedes: [ADR-{NNN}: {Title}]({link}) (if applicable)
- Superseded by: [ADR-{NNN}: {Title}]({link}) (if applicable)
```

---

### Nygard Format (Minimal)

```markdown
# ADR-{NNN}: {Title}

## Status

Accepted | Proposed | Deprecated | Superseded by ADR-{NNN}

## Context

{What is the situation that led to this decision?
What forces are at play — technical, business, organizational?
What constraints exist? 2–5 sentences.}

## Decision

{What did we decide to do?
State it directly, in active voice: "We will use X" or "We decided to adopt Y."
Include a brief rationale — why this option over the alternatives.}

## Consequences

{What becomes easier or better as a result?}
{What becomes harder or worse? Be honest about trade-offs.}
{What new concerns or constraints does this introduce?}
```

---

### Y-Statement Format (Compact)

```markdown
# ADR-{NNN}: {Title}

**Date**: YYYY-MM-DD | **Status**: Accepted

In the context of **{situation/use case}**,
facing **{concern or constraint}**,
we decided **{the option chosen}**,
to achieve **{quality attribute or goal}**,
accepting **{the downside or trade-off}**.

**Deciders**: {names or roles}
**Links**: {related ADRs, tickets}
```

---
