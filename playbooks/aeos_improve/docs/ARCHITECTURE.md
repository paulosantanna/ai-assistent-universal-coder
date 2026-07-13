# Arquitetura do pack

```text
User / AEOS CLI
       |
       v
Improvement Program Orchestrator
       |
       +--> Repository Baseline Cartographer
       +--> Token and Context Governor
       |
       +--> Wave executors (skills)
       |       |
       |       +--> independent Staff/Chief reviewer
       |       +--> Security and Clinical Safety Reviewer
       |
       +--> Evidence Store / Handoffs / Checkpoints
       |
       v
Deterministic Gate Validator
       |
       v
Evidence Readiness Judge
       |
       +--> PASS
       +--> REWORK_REQUIRED
       +--> BLOCKED
```

## Separação de responsabilidades

- Orchestrator não implementa domínio.
- Implementador não julga o próprio trabalho.
- Safety reviewer não modifica silenciosamente o patch.
- Judge não corrige; ele valida ou devolve.
- Token governor controla contexto e custo, não decisões técnicas.
- Baseline cartographer não muta o projeto.

## Paralelismo

Steps podem ser paralelos somente quando não compartilham path, contrato,
schema, fixture global, migração ou approval.
