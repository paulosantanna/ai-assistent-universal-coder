<!-- Package: 00_skills/(architecture)/modular-design-principles; relative command/resource examples resolve from that package or workspace root. -->

## Sub-units inside a bounded context

Sometimes one outer boundary is right, but inside it there are **named sub-areas** (subdomains, feature areas). Principles still apply **within** the context.

**Ownership**

- Each sub-unit should **own** its slice of model and persistence concerns where possible — avoid one mega registration layer that wires **every** store and repository for **every** sub-unit in one place (encourages reach-through and hidden coupling).

**Cross-sub-unit access**

- Prefer **internal application APIs** or **thin internal facades** (same context, explicit surface) over peers importing each other’s storage types directly.
- For async flows, prefer **enriched payloads** so handlers do not **chat** across sub-units for data that could travel with the event/command.

**Shared kernel inside the context**

- Small, stable shared types or enums can live in a **narrow shared area** — but resist a growing “utils” dump that becomes the real coupling point.

**Anti-pattern:** A single “persistence” or “data” sub-module that becomes the **only** place that knows about all tables/documents for all sub-units, and everyone else reaches through it — same problems as cross-context reach-through, **inside** the boundary.

---
