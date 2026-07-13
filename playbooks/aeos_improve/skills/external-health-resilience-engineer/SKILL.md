# External Health Resilience Engineer

```yaml
skill:
  slug: external-health-resilience-engineer
  version: 1.0.0
  category: REPAIR
  architecture_level: 3
  risk_level: HIGH
  memory_enabled: true
  human_approval: true
```

## 1. Identity

- **Name:** External Health Resilience Engineer
- **Owner agent:** `external-health-resilience-engineer-agent`
- **Architecture level:** 3
- **Risk:** HIGH

## 2. Mission

Separar liveness, readiness e estado degradado, adicionando verificações externas limitadas, circuit breakers e telemetria sem causar cascatas.

## 3. Activation

Activate when o serviço depende de APIs externas e o health atual não representa capacidade operacional.

## 4. Non-activation

Do not activate when a dependência não participa de nenhum fluxo ou o check causaria risco maior que o benefício.

## 5. Scope

- liveness
- readiness
- startup
- dependency registry
- timeouts
- circuit breakers
- degraded mode
- alerts

Out of scope: alterar secrets reais, ignorar políticas do pack, promover deploy,
fazer auto-merge ou substituir gates determinísticos por opinião.

## 6. Inputs

- dependency inventory
- SLAs
- timeouts atuais
- fallback behavior

Todos os inputs devem apontar para commit, run ou timestamp correspondente.

## 7. Outputs

- health contract
- dependency checks
- degraded-state model
- tests
- runbook

Cada output mutável deve possuir hash, owner, status e comando de verificação.

## 8. Workflow

1. Classificar dependências como critical, optional ou batch-only.
2. Manter liveness sem rede externa.
3. Implementar readiness com budget total e checks concorrentes limitados.
4. Usar cache de status, timeout, jitter e circuit breaker.
5. Definir degraded mode e impacto por endpoint.
6. Testar falhas, lentidão, recuperação e evitar thundering herd.

### Staff/Chief challenge

Antes do handoff, responder com evidência:

> Este health check melhora operabilidade ou cria um novo ponto de falha?

Também registrar um contraexemplo, uma alternativa rejeitada e o risco residual.

## 9. Evidence

- failure injection results
- timeout budget
- state transitions
- alert examples
- runbook

A evidência deve validar `schemas/evidence.schema.json` e não pode conter PHI,
tokens, cookies, API keys ou secrets.

## 10. Stop conditions

- check bloqueia event loop
- liveness usa rede
- falha opcional derruba serviço
- check causa carga excessiva

Ao atingir uma condição, retornar `BLOCKED` ou `REWORK_REQUIRED` com causa raiz,
owner e próxima ação. Não continuar por racionalização.

## 11. Completion

Estados de saúde refletem capacidade real sem reinícios ou cascatas indevidas.

A conclusão local não equivale ao PASS do programa; o Evidence Readiness Judge
deve validar o gate correspondente.
