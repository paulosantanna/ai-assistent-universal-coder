# CONTINUOUS_LEARNING.md

## Ciclo de Aprendizado

```
Execution → Observation → Evidence → Finding
→ Candidate Lesson → Validation → Promotion → Reuse
```

## Regras

1. **Toda execução gera aprendizado**: mesmo execuções com status BLOCKED ou REWORK geram lessons.
2. **Separação fato vs inferência**: Findings são fatos com evidência. Lessons inferem causa raiz.
3. **Validação antes de promoção**: Nenhum conhecimento é promovido sem validação.
4. **Provenance obrigatória**: Todo conhecimento registrado tem execution_id como referência.

## Template de Candidate Lesson

```yaml
lesson:
  execution_id: <id>
  observation: <o que foi observado>
  evidence_ref: <comando/output/file>
  finding: <o que significa>
  lesson_type: positive | negative
  confidence: LOW | MEDIUM | HIGH
  recommendation: <o que fazer/não fazer>
  source: <qual subagente/ferramenta>
```
