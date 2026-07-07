# OBSERVABILITY.md

> **AEOS Chief/Staff Edition**
>
> This document is part of the AI Engineering Operating System.
> It is designed for AI agents acting as Chief AI Architect, Chief Software Architect,
> Principal Engineer, Staff Software Engineer and Staff AI Engineer.
>
> Core invariants:
> - Evidence before claims.
> - Architecture before implementation.
> - Delegation before context bloat.
> - Verification before completion.
> - Knowledge persistence after every material outcome.
> - Human authority over unsafe or high-impact decisions.


## Purpose

Ensure systems can be understood in production.

## Signals

- logs;
- metrics;
- traces;
- events;
- audit logs;
- model telemetry;
- retrieval telemetry;
- cost telemetry;
- latency telemetry;
- error budgets.

## Requirements

Every production service should define:
- health checks;
- readiness checks;
- key metrics;
- error taxonomy;
- trace boundaries;
- dashboards;
- alerts;
- incident runbook.

## AI observability

Track:
- prompt version;
- model version;
- retrieval sources;
- confidence;
- abstentions;
- safety interventions;
- hallucination flags;
- user feedback.
