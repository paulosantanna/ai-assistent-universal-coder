<!-- Package: 00_skills/(architecture)/tactical-ddd; relative command/resource examples resolve from that package or workspace root. -->

## Golden Rules

1. **Behaviour with data** — Objects own both state and the operations that change it
2. **Ubiquitous Language** — Method names come from the domain, not CRUD (`commitTo`, not `setStatus`)
3. **Small Aggregates** — Root + Value Objects by default; add child Entities only for true invariants
4. **One transaction = one Aggregate** — Cross-Aggregate rules use eventual consistency via Domain Events
5. **Reference by ID** — Never hold object references to other Aggregates
6. **Value Objects first** — Use Entities only when individual identity is essential
7. **Domain Services sparingly** — Excessive services → anemic model
8. **Protect invariants** — The Aggregate is the last line of defence; never trust the caller

---
