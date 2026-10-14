<!-- Package: 00_skills/(architecture)/modular-design-principles; relative command/resource examples resolve from that package or workspace root. -->

## Creating a bounded context (workflow)

Use when introducing a **new** cohesive area of the system (greenfield module or extracted domain).

1. **Scope and language** — Name the context; list core nouns/verbs (**ubiquitous language**). Reject vague names that collide with other contexts.
2. **Responsibilities** — What decisions happen **only** here? What is explicitly *out* of scope?
3. **State ownership** — Which facts are **authoritative** in this context? Where are they stored conceptually (even if storage tech is undecided)?
4. **Public contract** — Operations and/or events other contexts may use. Version or evolve this contract intentionally.
5. **Integrations** — For each neighbor: sync call, async message, shared read model, or batch sync? Document **consistency** (immediate, eventual) and **failure** behavior.
6. **Invariants and lifecycles** — What must always be true inside this boundary? What starts/completes a lifecycle?
7. **Isolation check** — Can you test core behavior **without** spinning up unrelated contexts (fakes at ports)?
8. **Observability** — How will you trace a request or job through **this** context with clear identifiers?

**Cross-module interaction** (while designing): prefer the **minimal** contract; define **timeouts**, **retries**, **idempotency** for async; avoid “temporary” direct store access as a shortcut.

---
