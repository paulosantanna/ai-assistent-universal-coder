# AIDiabetic Urgent Improvement — Full Playbook

## 1. Objetivo

Executar o conjunto completo de melhorias com o menor tempo de calendário
possível sem sacrificar evidência, segurança clínica, reversibilidade ou
qualidade.

## 2. Estratégia de velocidade

Velocidade vem de baseline compartilhado, DAG explícita, execução paralela sem
conflitos, ferramentas determinísticas antes de LLM, handoffs compactos, testes
focados por patch, suíte ampliada por wave e cache de evidências.

Velocidade não vem de reescrita big bang, pular testes, mascarar flakiness com
retries, habilitar cache clínico sem validação, inventar métricas ou permitir
que o executor aprove o próprio trabalho.

## 3. Wave 0 — Baseline

Nenhum arquivo do projeto é alterado. Entregas:

1. commit e working tree;
2. mapa de módulos e imports;
3. rotas e OpenAPI atual;
4. testes por tipo;
5. journeys observadas;
6. configs e precedência;
7. dependências externas;
8. observabilidade;
9. CI/release;
10. claims matrix;
11. métricas recalculadas;
12. benchmark base.

O esforço e o cronograma são recalculados somente após este gate.

## 4. Wave 1 — Contratos e testes críticos

### OpenAPI

- inventário rota ↔ operação OpenAPI;
- request/response models explícitos;
- tags, auth, errors e exemplos sanitizados;
- schema snapshot;
- breaking-change detection.

### Error handling

- Problem Details compatível com RFC 9457;
- machine code estável;
- correlation ID;
- redaction;
- mapeamento exception ↔ status.

### E2E

- journeys reais, não imaginadas;
- P0 completamente coberto;
- P1 por E2E, integração ou contrato, conforme risco;
- fixtures sintéticas;
- traces em falha;
- flake budget.

## 5. Wave 2 — Arquitetura, cache e resiliência

### Modularização

Não mover dezenas de pacotes de uma vez. Produzir grafo, boundaries, ADR,
facade/contract, uma fatia vertical, testes, métricas before/after e rollback.

### RAG cache

Ordem: benchmark, classificação de query, exact cache, versioned keys,
invalidation, isolation, semantic experiment e rollout opt-in.

`NO_CACHE` é o default para resposta clínica personalizada, PHI,
contraindication, interaction e qualquer saída de alto risco.

### Health

- liveness: processo vivo, sem rede externa;
- startup: inicialização local necessária;
- readiness: capacidade de servir;
- degraded: dependência opcional indisponível;
- checks externos com timeout, circuit breaker, jitter e cache de status.

## 6. Wave 3 — Config, observabilidade e C4

| Classe | Fonte canônica |
|---|---|
| Runtime settings | Pydantic Settings + env/secrets provider |
| Políticas versionadas | YAML/JSON com schema |
| Parâmetros científicos | artefato versionado com provenance |
| Infra/deploy | manifest específico da plataforma |
| Secrets | secret store, nunca repositório |

Observabilidade exige logs, metrics e traces correlacionados, cardinalidade
limitada, redaction, dashboards técnicos/RAG/safety e SLOs acionáveis.

C4 exige Context, Container e Component. Code view só entra quando agrega valor.

## 7. Wave 4 — Release, dead code e pre-commit

Release PR e changelog podem ser automatizados. Auto-merge e auto-deploy
permanecem desabilitados.

Dead code exige análise de entrypoints dinâmicos, lotes pequenos, testes e
rollback.

Pre-commit exige versões pinadas, hooks rápidos, checks pesados no CI, exclusões
justificadas e parity local/CI.

## 8. Wave 5 — Validação final

- suíte completa;
- smoke/readiness/liveness;
- benchmarks before/after;
- security and clinical safety review;
- evidence hash verification;
- scorecard;
- rollback proof;
- verdict.

## 9. Stop conditions globais

- secret ou PHI detectado;
- auth bypass;
- regressão crítica;
- critical gate falho;
- hash mismatch;
- working tree alterada fora do executor;
- rollback não demonstrável;
- três retrabalhos do mesmo gate;
- aprovação obrigatória ausente.

## 10. Saída final

```text
Verdict: PASS | REWORK_REQUIRED | BLOCKED
Score: <computed>
Critical gates: <pass/fail>
Changed files: <count>
Tests: <passed/failed/skipped/baselined>
Performance: <before/after>
Security/clinical findings: <counts>
Rollback: <verified/not verified>
Evidence manifest: <path + sha256>
```
