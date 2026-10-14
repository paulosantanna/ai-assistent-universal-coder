# KNOWLEDGE_PROMOTION.md

## Regras de Promoção

Conhecimento candidato a promoção deve:

1. Ter sido observado em 2+ execuções independentes
2. Ter evidência reproduzível
3. Não contradizer conhecimento validado existente
4. Ter sido revisado por humano ou JUDGE Agent

## Pipeline de Promoção

```
Observation
→ Evidence capture
→ Candidate entry (em CANDIDATE_LESSONS.md)
→ Cross-validation (2+ ocorrências)
→ Review (humano ou JUDGE)
→ Promotion to POSITIVE_KNOWLEDGE.md or NEGATIVE_KNOWLEDGE.md
→ Update KNOWLEDGE.md summary
```

## Níveis de Confiança

| Nível | Critério | Ação |
|-------|----------|------|
| LOW | 1 observação, sem revisão | Manter como candidato |
| MEDIUM | 2+ observações, revisado por PARENT | Promover ao Parent memory |
| HIGH | 3+ observações, revisado por JUDGE | Promover ao Shared Knowledge |
| CONFIRMED | Validade por 30+ dias sem contradição | Institutional Knowledge |
