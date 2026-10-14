<!-- Package: 00_skills/(development)/nestjs-modular-monolith; relative command/resource examples resolve from that package or workspace root. -->

## Behavioral Guidelines

These principles govern HOW you work, not just WHAT you build:

**Think Before Coding.** Before implementing any module or layer: state your assumptions about domain boundaries explicitly. If multiple bounded context interpretations exist, present them — don't pick silently. If a simpler module structure exists, say so and push back when warranted. If the domain is unclear, stop and ask — don't guess.

**Simplicity First.** Design the minimum viable architecture: no CQRS unless the domain has distinct read/write patterns. No Event Sourcing unless audit trail is a real requirement. No abstractions for single-use code. If 3 modules suffice, don't create 8. Start with simple services, upgrade to CQRS only when complexity warrants it.

**Surgical Changes.** When working with existing modular monoliths: don't "improve" adjacent modules that aren't part of the task. Match existing style and conventions, even if you'd do it differently. If you spot unrelated issues, mention them — don't fix them silently.

**Goal-Driven Execution.** For every architectural decision, define verifiable success criteria. "Add a new module" → "Module has isolated state, clear interface, passing tests". "Fix communication" → "Events flow correctly, no direct cross-module imports".
