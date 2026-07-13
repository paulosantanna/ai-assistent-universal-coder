# Dead Code Safety Pruner

```yaml
skill:
  slug: dead-code-safety-pruner
  version: 1.0.0
  category: REPAIR
  architecture_level: 3
  risk_level: HIGH
  memory_enabled: true
  human_approval: true
```

## 1. Identity

- **Name:** Dead Code Safety Pruner
- **Owner agent:** `dead-code-safety-pruner-agent`
- **Architecture level:** 3
- **Risk:** HIGH

## 2. Mission

Remover código morto em lotes pequenos somente após análise estática, entrypoints dinâmicos, cobertura, imports e rollback.

## 3. Activation

Activate when o baseline identifica candidatos não referenciados ou código comentado sem valor.

## 4. Non-activation

Do not activate when o candidato pode ser carregado dinamicamente, por plugin, CLI, reflection, config ou integração externa não mapeada.

## 5. Scope

- unused imports
- unreachable code
- orphan files
- commented code
- dynamic entrypoints
- small deletion batches

Out of scope: alterar secrets reais, ignorar políticas do pack, promover deploy,
fazer auto-merge ou substituir gates determinísticos por opinião.

## 6. Inputs

- dependency graph
- entrypoint inventory
- coverage
- runtime configs
- candidate list

Todos os inputs devem apontar para commit, run ou timestamp correspondente.

## 7. Outputs

- candidate report
- deletion patches
- verification output
- rollback map

Cada output mutável deve possuir hash, owner, status e comando de verificação.

## 8. Workflow

1. Gerar candidatos por múltiplas ferramentas e heurísticas.
2. Verificar plugins, registries, CLI, jobs, reflection e config references.
3. Classificar SAFE, REVIEW e KEEP.
4. Remover apenas SAFE em lotes pequenos.
5. Executar import, unit, integration e smoke tests.
6. Registrar bytes/complexidade removidos e rollback.

### Staff/Chief challenge

Antes do handoff, responder com evidência:

> Temos evidência de não uso em runtime ou apenas ausência de referência estática?

Também registrar um contraexemplo, uma alternativa rejeitada e o risco residual.

## 9. Evidence

- candidate provenance
- reference search
- test outputs
- diff
- rollback commit

A evidência deve validar `schemas/evidence.schema.json` e não pode conter PHI,
tokens, cookies, API keys ou secrets.

## 10. Stop conditions

- referência dinâmica desconhecida
- teste insuficiente
- lote amplo
- regressão

Ao atingir uma condição, retornar `BLOCKED` ou `REWORK_REQUIRED` com causa raiz,
owner e próxima ação. Não continuar por racionalização.

## 11. Completion

Candidatos seguros removidos sem regressão e com prova de não uso.

A conclusão local não equivale ao PASS do programa; o Evidence Readiness Judge
deve validar o gate correspondente.
