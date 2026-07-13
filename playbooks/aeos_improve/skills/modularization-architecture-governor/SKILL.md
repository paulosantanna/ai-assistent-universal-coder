# Modularization Architecture Governor

```yaml
skill:
  slug: modularization-architecture-governor
  version: 1.0.0
  category: MIGRATION
  architecture_level: 3
  risk_level: CRITICAL
  memory_enabled: true
  human_approval: true
```

## 1. Identity

- **Name:** Modularization Architecture Governor
- **Owner agent:** `modularization-architecture-governor-agent`
- **Architecture level:** 3
- **Risk:** CRITICAL

## 2. Mission

Reduzir acoplamento do src por migração incremental baseada em grafo, contratos, ADR e testes, sem reescrita big bang.

## 3. Activation

Activate when o baseline confirma boundaries misturados, ciclos, alta fan-in/fan-out ou dificuldade de teste isolado.

## 4. Non-activation

Do not activate when a mudança é cosmética ou o benefício arquitetural não foi medido.

## 5. Scope

- dependency graph
- bounded contexts
- facades
- ports/adapters
- strangler plan
- ADRs
- contract tests

Out of scope: alterar secrets reais, ignorar políticas do pack, promover deploy,
fazer auto-merge ou substituir gates determinísticos por opinião.

## 6. Inputs

- grafo de dependências
- hotspots
- runtime entrypoints
- test map

Todos os inputs devem apontar para commit, run ou timestamp correspondente.

## 7. Outputs

- target architecture
- ADRs
- migration slices
- facades/contracts
- architecture tests

Cada output mutável deve possuir hash, owner, status e comando de verificação.

## 8. Workflow

1. Medir ciclos, fan-in, fan-out, instabilidade e hotspots.
2. Propor boundaries por responsabilidade e fluxo de dados.
3. Selecionar uma fatia vertical pequena e reversível.
4. Criar contrato/facade antes de mover implementação.
5. Migrar consumidores em lotes e executar testes.
6. Remover bridge somente após zero consumidores e aprovação.

### Staff/Chief challenge

Antes do handoff, responder com evidência:

> Esta mudança melhora boundaries ou apenas move arquivos?

Também registrar um contraexemplo, uma alternativa rejeitada e o risco residual.

## 9. Evidence

- dependency graph before/after
- ADR
- contract tests
- consumer inventory
- rollback

A evidência deve validar `schemas/evidence.schema.json` e não pode conter PHI,
tokens, cookies, API keys ou secrets.

## 10. Stop conditions

- migração exige reescrita ampla
- boundary sem owner
- ciclo novo
- regressão funcional

Ao atingir uma condição, retornar `BLOCKED` ou `REWORK_REQUIRED` com causa raiz,
owner e próxima ação. Não continuar por racionalização.

## 11. Completion

Fatia aprovada migrada com redução mensurável de acoplamento e sem regressão.

A conclusão local não equivale ao PASS do programa; o Evidence Readiness Judge
deve validar o gate correspondente.
