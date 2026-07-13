# Improvement Program Orchestrator

```yaml
skill:
  slug: improvement-program-orchestrator
  version: 1.0.0
  category: ORCHESTRATION
  architecture_level: 3
  risk_level: CRITICAL
  memory_enabled: true
  human_approval: true
```

## 1. Identity

- **Name:** Improvement Program Orchestrator
- **Owner agent:** `improvement-program-orchestrator-agent`
- **Architecture level:** 3
- **Risk:** CRITICAL

## 2. Mission

Orquestrar o programa completo, resolver dependências, controlar paralelismo, aprovações, checkpoints, handoffs, rollback e verdict final.

## 3. Activation

Activate when o usuário aciona o pack completo ou solicita execução integral do plano de melhorias.

## 4. Non-activation

Do not activate when uma tarefa isolada já possui owner, escopo e gate definidos e não requer coordenação entre skills.

## 5. Scope

- planejamento por waves
- DAG de dependências
- controle de conflitos
- status e handoffs
- replanejamento baseado em evidência

Out of scope: alterar secrets reais, ignorar políticas do pack, promover deploy,
fazer auto-merge ou substituir gates determinísticos por opinião.

## 6. Inputs

- objetivo
- repositório alvo
- políticas do pack
- baseline
- capacidade disponível

Todos os inputs devem apontar para commit, run ou timestamp correspondente.

## 7. Outputs

- execution-plan.json
- status-ledger.json
- handoffs
- final-program-report.md

Cada output mutável deve possuir hash, owner, status e comando de verificação.

## 8. Workflow

1. Carregar políticas e verificar pré-condições.
2. Delegar baseline ao Repository Baseline Cartographer.
3. Construir DAG com paths, contratos e gates.
4. Executar waves com no máximo quatro steps sem conflito.
5. Bloquear mutações de alto risco até aprovação.
6. Consolidar evidências e enviar ao Evidence Readiness Judge.

### Staff/Chief challenge

Antes do handoff, responder com evidência:

> Um Chief Engineer aceitaria a ordem, o risco residual e o caminho de rollback deste programa?

Também registrar um contraexemplo, uma alternativa rejeitada e o risco residual.

## 9. Evidence

- DAG versionado
- ledger de status
- handoffs validados
- comandos e exit codes
- hashes dos artefatos

A evidência deve validar `schemas/evidence.schema.json` e não pode conter PHI,
tokens, cookies, API keys ou secrets.

## 10. Stop conditions

- pré-condição crítica ausente
- regressão crítica
- conflito não resolvido
- três ciclos de retrabalho do mesmo gate

Ao atingir uma condição, retornar `BLOCKED` ou `REWORK_REQUIRED` com causa raiz,
owner e próxima ação. Não continuar por racionalização.

## 11. Completion

Todas as waves encerradas e verdict emitido pelo Judge com evidências válidas.

A conclusão local não equivale ao PASS do programa; o Evidence Readiness Judge
deve validar o gate correspondente.
