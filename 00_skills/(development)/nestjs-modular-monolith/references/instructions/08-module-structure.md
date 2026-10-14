<!-- Package: 00_skills/(development)/nestjs-modular-monolith; relative command/resource examples resolve from that package or workspace root. -->

## Module Structure

Recommended NX monorepo structure:

```
apps/
  api/                          # NestJS application entry point
    src/
      main.ts                   # Bootstrap with Fastify adapter
      app.module.ts             # Root module importing all domain modules

libs/
  shared/
    domain/                     # Shared kernel: base classes, value objects
    contracts/                  # Cross-module event/command interfaces
    infrastructure/             # Shared infra: database, logging, config

  [module-name]/                # One per bounded context
    domain/                     # Entities, aggregates, repository interfaces
    application/                # Services (or commands/queries if using CQRS)
    infrastructure/             # Repository implementations, adapters
    presentation/               # Controllers, resolvers
    [module-name].module.ts     # NestJS module definition
```
