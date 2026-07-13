# KNOWLEDGE_PROMOTION.md
# AI Continuous Training Maintainer — Knowledge Promotion Protocol

## 1. Purpose

Governs how raw observations from executions become reusable knowledge within this skill.

Prevents: memory contamination, duplication, overgeneralization, promotion of unverified conclusions, catastrophic forgetting.

## 2. Promotion chain

```
RAW OBSERVATION (execution output)
→ EVIDENCE-BACKED FINDING (comando + output)
→ CANDIDATE LESSON (memory/LESSONS.md)
→ DOMAIN VALIDATION (PARENT review)
→ CROSS-CHECK (2+ occurrences)
→ REVIEW (ROOT or JUDGE)
→ VALIDATED KNOWLEDGE (knowledge/POSITIVE_KNOWLEDGE.md)
→ SHARED KNOWLEDGE (memory/shared/)
```

## 3. Promotion eligibility

A finding is eligible for promotion when:
1. Evidência reproduzível existe (comando + output + exit code)
2. Ocorreu em 2+ execuções independentes
3. Não contradiz conhecimento validado existente
4. Foi revisado por PARENT ou ROOT
5. Proveniência está registrada (execution_id)

## 4. Confidence levels

| Nível | Critério | Ação |
|-------|----------|------|
| LOW | 1 observação | Manter como candidato em LESSONS.md |
| MEDIUM | 2+ observações, revisão PARENT | knowledge/POSITIVE_KNOWLEDGE.md |
| HIGH | 3+ observações, revisão JUDGE | memory/shared/ |
| CONFIRMED | 30+ dias sem contradição | Institutional knowledge |

## 5. Deprecation

Knowledge is deprecated when:
- Contradicted by new evidence
- Context/technology changed
- 90+ dias sem revalidação

## 6. Example

```
Observation: "bandit flagged SQL injection em src/main.py linha 42"
Evidence: bandit -r src/ -f json exit 1, finding B102
Finding: Input de usuário não sanitizado antes de query
Candidate Lesson: "Sempre sanitizar input antes de queries SQL"
Promotion: → POSITIVE_KNOWLEDGE.md após validação em 2 execuções
```
