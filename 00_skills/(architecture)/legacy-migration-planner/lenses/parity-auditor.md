# Parity audit lens

Updated: 2026-10-13
Owner: codenavi-agent. Bounded read-only sequential lens, never a new identity. Source: IMG_2765–IMG_2767.

Input packet: antes/, depois/, criterios.md selecting applicable criteria; optional divergencias-esperadas.md with intended output differences. Exclude diff, commit history, authors, task/ticket and intention narratives. Unexpected excluded content is an audit-integrity gap. A sequential pass cannot guarantee genuinely blind context.

| Criterion | Comparison |
| --- | --- |
| Contract | operations, route/method, required input, types and responses; new optional field is compatible, removal/rename/type/required change is not |
| Errors | conditions, codes, HTTP status and messages |
| Data path | read/write tables/columns/queues/topics/cache keys, meaningful order, precision/date/timezone serialization |
| Configuration | environment/property names, requiredness and defaults |
| Dependencies | actual services/hosts/ports, timeout/retry/circuit-breaker values |
| Behavior | same input produces same output; normalize only declared timestamps/generated IDs/nonsemantic log order |

Evaluate only applicable criteria; each result is OK, DIVERGE or NAO VERIFICADO. Final APROVADO requires all applicable criteria verified/compatible or explicitly expected differences. Known unplanned divergence → REPROVADO. Otherwise any evidence gap → INCONCLUSIVO. Missing applicable criteria definition is also inconclusive.
Never ask for context during the audit or guess intent. List missing evidence and the artifact that would resolve it. Do not suggest or perform repairs. Output PT-BR:

```text
VEREDITO: APROVADO | REPROVADO | INCONCLUSIVO
RESUMO: one sentence
POR CRITERIO: criterion — OK | DIVERGE | NAO VERIFICADO
DIVERGENCIAS: [criterion] actual difference; antes/path:line and depois/path:line
NAO VERIFICADO: gap and missing artifact
INTEGRIDADE: OK or excluded content/context contamination
```
No secret values. This procedure is not an independent agent or the deterministic Judge service.
