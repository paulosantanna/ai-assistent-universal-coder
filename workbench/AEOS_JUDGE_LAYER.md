# AEOS Judge Layer — v1.0.0

## 1. Propósito

O Judge Layer é a autoridade de qualidade do AEOS. Ele avalia cada alteração, decisão ou resultado contra critérios objetivos e produz um veredito final que pode aprovar, bloquear ou exigir retrabalho.

## 2. Princípios

1. **Independência** — O Judge nunca pode ser o mesmo agente que implementou a mudança.
2. **Objetividade** — Julgamento é baseado em evidências, não em opinião.
3. **Transparência** — Todo critério, dedução e score é público e rastreável.
4. **Finalidade** — Decisão do Judge é final, sujeita apenas a recurso com novas evidências.
5. **Segurança** — Violações de segurança resultam em BLOCKED imediato.

## 3. Processo de Julgamento

```
1. RECEBER → Receber task + evidências + diff + rollback plan
2. VALIDAR → Verificar completude dos dados
3. AVALIAR → Pontuar cada categoria
4. DEDUZIR → Aplicar deduções por falhas
5. DECIDIR → PASS / BLOCKED / NEEDS_REWORK
6. RELATAR → Gerar judge report detalhado
7. ARQUIVAR → Persistir relatório (imutável)
```

## 4. Categorias de Avaliação

| Categoria | Peso | Descrição | Critérios |
|-----------|------|-----------|-----------|
| Evidence Completeness | 25% | Evidências suficientes? | 6 tipos requeridos presentes |
| Test Coverage | 20% | Testes implementados? | Testes existem e passam |
| Security Validation | 20% | Segredos? Operações inseguras? | Scan limpo |
| Rollback Readiness | 15% | Rollback plan existe e é viável? | Plano documentado e testável |
| Diff Quality | 10% | Diff claro e mínimo? | Diff focado e explicado |
| Code Quality | 10% | Código segue padrões? | Lint, tipos, boas práticas |

## 5. Scoring

```
Score = Σ(peso_i × score_i) - deduções

Onde:
- score_i ∈ [0, 10]
- peso_i ∈ [0, 1], Σ pesos = 1
- deduções ∈ [0, 3] baseado em violações
```

| Score | Decisão |
|-------|---------|
| ≥ 7.0 | PASS |
| 5.0 – 6.9 | NEEDS_REWORK |
| < 5.0 | BLOCKED |

## 6. Condições de Bloqueio

Qualquer uma das seguintes resulta em BLOCKED automático:
- Evidência ausente para tipo requerido.
- Testes ausentes quando requeridos.
- Rollback plan ausente quando requerido.
- Diff summary ausente.
- Secrets detectados.
- Operação insegura detectada.
- Judge é o implementador.
- Score < 5.0.

## 7. Judge Report

```markdown
# AEOS Judge Report

## Metadados
- **Task:** task-001
- **Agent:** agent-coder-01
- **Judge:** agent-judge-01
- **Timestamp:** 2026-07-08T10:30:00Z

## Scores
| Categoria | Score | Peso | Ponderado |
|-----------|-------|------|-----------|
| Evidence | 8.0 | 25% | 2.0 |
| Tests | 7.0 | 20% | 1.4 |
| Security | 10.0 | 20% | 2.0 |
| Rollback | 9.0 | 15% | 1.35 |
| Diff | 8.0 | 10% | 0.8 |
| Quality | 7.0 | 10% | 0.7 |

**Total:** 8.25
**Deduções:** 0.0
**Final:** 8.25

## Decisão
**PASS**

## Evidências
- [evt-001] Código implementado: src/validate.ts:45-78
- [evt-002] Testes passam: npm test -- --coverage

## Falhas
- Nenhuma

## Próximos Passos
1. Fazer merge da branch
2. Atualizar documentação
3. Registrar lição aprendida
```

## 8. Recursos

Se o agente discordar do veredito:
1. Submeter novas evidências.
2. Judge reavalia com evidências adicionais.
3. Se mantido, escalate para Root Agent + humano.
4. Decisão humana é final.
