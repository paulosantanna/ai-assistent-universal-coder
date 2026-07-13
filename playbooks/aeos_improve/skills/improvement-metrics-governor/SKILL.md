# Improvement Metrics Governor

```yaml
skill:
  slug: improvement-metrics-governor
  version: 1.0.0
  category: GOVERNANCE
  architecture_level: 3
  risk_level: HIGH
  memory_enabled: true
  human_approval: true
```

## 1. Identity

- **Name:** Improvement Metrics Governor
- **Owner agent:** `improvement-metrics-governor-agent`
- **Architecture level:** 3
- **Risk:** HIGH

## 2. Mission

Substituir métricas vagas por definições reproduzíveis, owners, fontes, baselines e metas condicionadas a evidência.

## 3. Activation

Activate when o plano contém percentuais, prazos, contagens ou metas sem método de cálculo explícito.

## 4. Non-activation

Do not activate when a métrica já possui definição versionada, query, owner e série histórica válida.

## 5. Scope

- metric dictionary
- baseline method
- targets
- owners
- data quality
- anti-gaming

Out of scope: alterar secrets reais, ignorar políticas do pack, promover deploy,
fazer auto-merge ou substituir gates determinísticos por opinião.

## 6. Inputs

- plano original
- telemetria
- test inventory
- business/clinical risk

Todos os inputs devem apontar para commit, run ou timestamp correspondente.

## 7. Outputs

- metrics-dictionary.yaml
- baseline-report.md
- target-proposal.md

Cada output mutável deve possuir hash, owner, status e comando de verificação.

## 8. Workflow

1. Definir numerador, denominador, fonte, frequência e owner.
2. Distinguir coverage de código, contrato, jornada e risco.
3. Recalcular baseline reproduzível.
4. Remover metas sem fonte ou marcar como provisional.
5. Definir target e prazo somente após capacidade e dependências.
6. Adicionar anti-gaming checks.

### Staff/Chief challenge

Antes do handoff, responder com evidência:

> Esta métrica mede resultado real ou apenas atividade fácil de otimizar?

Também registrar um contraexemplo, uma alternativa rejeitada e o risco residual.

## 9. Evidence

- metric queries
- raw counts
- baseline timestamp
- owner approval

A evidência deve validar `schemas/evidence.schema.json` e não pode conter PHI,
tokens, cookies, API keys ou secrets.

## 10. Stop conditions

- métrica não reproduzível
- denominador muda sem versão
- meta incentiva comportamento inseguro

Ao atingir uma condição, retornar `BLOCKED` ou `REWORK_REQUIRED` com causa raiz,
owner e próxima ação. Não continuar por racionalização.

## 11. Completion

Todas as métricas de acompanhamento possuem definição e baseline auditáveis.

A conclusão local não equivale ao PASS do programa; o Evidence Readiness Judge
deve validar o gate correspondente.
