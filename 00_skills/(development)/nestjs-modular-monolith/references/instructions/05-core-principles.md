<!-- Package: 00_skills/(development)/nestjs-modular-monolith; relative command/resource examples resolve from that package or workspace root. -->

## Core Principles

**10 Modular Monolith Principles** — these override general NestJS defaults when they conflict:

1. **Boundaries**: Clear interfaces between modules, minimal coupling
2. **Composability**: Modules can be recombined dynamically
3. **Independence**: Each module is self-contained with its own domain
4. **Scalability**: Per-module optimization without system-wide changes
5. **Explicit Communication**: Contracts between modules, never implicit
6. **Replaceability**: Any module can be substituted without system impact
7. **Logical Deployment Separation**: Even in monolith, maintain separation
8. **State Isolation**: Strict data boundaries — no shared database tables
9. **Observability**: Module-level monitoring and tracing
10. **Resilience**: Failures in one module don't cascade
