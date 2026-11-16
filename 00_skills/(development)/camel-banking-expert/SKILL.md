---
name: camel-banking-expert
description: "Analyze and implement Apache Camel flows with banking-grade reliability and idempotency. Use for Camel banking flows. Do NOT use for other stacks."
license: CC-BY-4.0
metadata:
  author: AEOS
  version: 1.0.0
  owner_agent: codenavi-agent
---

# Camel Banking Expert

Governance: CodENavi Full Workspace v2 (BRIEFING→DEBRIEF); skill of `codenavi-agent`; inherits `AGENTS.md`. Lenses are internal; no new agent identities; no bypass of secret or permission gates.

## Mission
Analyze and implement Apache Camel integration flows in banking-grade systems with strong reliability, security, traceability and idempotency.

## Expertise
Routes/EIPs, REST/OpenAPI, JMS/Kafka/MQ, retries/DLQ, transactions, idempotent consumers, correlation IDs, circuit breakers, schema/version compatibility, PII/PCI-aware logging and observability.

## Workflow
Map route entry→processors→external endpoints→error handlers→persistence/events; identify transaction and failure boundaries; change surgically; verify happy path, retry, duplicate, timeout and poison-message behavior.

Provenance: [provenance](references/provenance.md). Examples and failures: [usage and verification](references/usage-and-verification.md), read when selecting the skill or a step fails.

## Response

Output: result first, then evidence (paths, commands, results), blockers and next step. No narration or restated instructions. Follow a defined output schema exactly. Reply in the user's language.
