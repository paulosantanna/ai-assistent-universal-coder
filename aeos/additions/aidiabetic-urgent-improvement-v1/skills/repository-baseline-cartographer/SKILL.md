# Repository Baseline Cartographer

```yaml
skill:
  slug: repository-baseline-cartographer
  version: 1.0.0
  category: ANALYSIS
  architecture_level: 3
  risk_level: HIGH
  memory_enabled: true
  human_approval: true
```

## 1. Identity

- **Name:** Repository Baseline Cartographer
- **Owner agent:** `repository-baseline-cartographer-agent`
- **Architecture level:** 3
- **Risk:** HIGH

## 2. Mission

Produzir baseline factual do repositório e validar cada alegação do plano original antes de qualquer mudança.

## 3. Activation

Activate when uma melhoria depende de fatos sobre rotas, módulos, testes, configurações, dependências, métricas ou fluxos.

## 4. Non-activation

Do not activate when o baseline da mesma revisão e commit já foi validado e permanece atual.

## 5. Scope

- árvore e módulos
- grafo de imports
- rotas
- testes
- CI
- configs
- observabilidade
- alegações do plano

Out of scope: alterar secrets reais, ignorar políticas do pack, promover deploy,
fazer auto-merge ou substituir gates determinísticos por opinião.

## 6. Inputs

- repositório
- commit SHA
- plano original

Todos os inputs devem apontar para commit, run ou timestamp correspondente.

## 7. Outputs

- baseline.json
- claims-matrix.md
- repository-map.md
- risk-register.json

Cada output mutável deve possuir hash, owner, status e comando de verificação.

## 8. Workflow

1. Registrar commit, branch e estado do working tree.
2. Inventariar stack, entrypoints, rotas, testes, workflows e configs.
3. Mapear dependências e possíveis ciclos.
4. Classificar cada alegação como CONFIRMED, REJECTED ou UNKNOWN.
5. Gerar mapa de riscos e recomendações sem mutar arquivos.

### Staff/Chief challenge

Antes do handoff, responder com evidência:

> Um Staff Engineer independente conseguiria reproduzir cada fato deste baseline?

Também registrar um contraexemplo, uma alternativa rejeitada e o risco residual.

## 9. Evidence

- paths e line ranges
- saída de comandos
- contagens reproduzíveis
- commit SHA

A evidência deve validar `schemas/evidence.schema.json` e não pode conter PHI,
tokens, cookies, API keys ou secrets.

## 10. Stop conditions

- repositório inacessível
- estado muda durante scan sem registro
- alegação não verificável marcada como fato

Ao atingir uma condição, retornar `BLOCKED` ou `REWORK_REQUIRED` com causa raiz,
owner e próxima ação. Não continuar por racionalização.

## 11. Completion

Baseline reproduzível e claims matrix completa para o commit analisado.

A conclusão local não equivale ao PASS do programa; o Evidence Readiness Judge
deve validar o gate correspondente.
