# Clinical RAG Cache Engineer

```yaml
skill:
  slug: clinical-rag-cache-engineer
  version: 1.0.0
  category: AI_ML
  architecture_level: 3
  risk_level: CRITICAL
  memory_enabled: true
  human_approval: true
```

## 1. Identity

- **Name:** Clinical RAG Cache Engineer
- **Owner agent:** `clinical-rag-cache-engineer-agent`
- **Architecture level:** 3
- **Risk:** CRITICAL

## 2. Mission

Projetar cache exato/semântico seguro para RAG somente quando benchmark, privacidade, versionamento e invalidação provarem valor.

## 3. Activation

Activate when o baseline mede repetição de queries e latência/custo relevantes no pipeline RAG.

## 4. Non-activation

Do not activate when não há benchmark, a consulta é personalizada/alto risco ou o cache violaria isolamento clínico.

## 5. Scope

- query classification
- exact cache
- semantic cache experiment
- key design
- TTL
- invalidation
- isolation
- benchmarks

Out of scope: alterar secrets reais, ignorar políticas do pack, promover deploy,
fazer auto-merge ou substituir gates determinísticos por opinião.

## 6. Inputs

- query samples anonimizadas ou sintéticas
- pipeline versions
- latency baseline
- privacy policy

Todos os inputs devem apontar para commit, run ou timestamp correspondente.

## 7. Outputs

- cache ADR
- safe-query policy
- implementation
- benchmark report
- invalidation and isolation tests

Cada output mutável deve possuir hash, owner, status e comando de verificação.

## 8. Workflow

1. Medir frequência, similaridade, latência e custo sem coletar PHI.
2. Classificar queries em SAFE_CACHE, EXACT_ONLY e NO_CACHE.
3. Incluir tenant/user scope quando aplicável e versões de evidência, índice, modelo e prompt na chave.
4. Implementar exact cache antes de semantic cache.
5. Executar avaliação de colisão semântica, stale evidence e cross-user leakage.
6. Ativar gradualmente apenas se gates de segurança e desempenho passarem.

### Staff/Chief challenge

Antes do handoff, responder com evidência:

> O ganho de latência justifica o risco de entregar evidência clínica errada ou obsoleta?

Também registrar um contraexemplo, uma alternativa rejeitada e o risco residual.

## 9. Evidence

- hit rate
- p50/p95/p99 before/after
- semantic collision tests
- privacy review
- invalidation proof

A evidência deve validar `schemas/evidence.schema.json` e não pode conter PHI,
tokens, cookies, API keys ou secrets.

## 10. Stop conditions

- PHI detectada
- cross-user hit
- evidence stale
- ganho não significativo
- qualidade degradada

Ao atingir uma condição, retornar `BLOCKED` ou `REWORK_REQUIRED` com causa raiz,
owner e próxima ação. Não continuar por racionalização.

## 11. Completion

Cache aprovado apenas para classes seguras, com ganho medido e testes de isolamento/invalidação.

A conclusão local não equivale ao PASS do programa; o Evidence Readiness Judge
deve validar o gate correspondente.
