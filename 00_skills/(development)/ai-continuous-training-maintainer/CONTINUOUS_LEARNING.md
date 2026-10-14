# CONTINUOUS_LEARNING.md
# AI Continuous Training Maintainer — Continuous Learning Engine

## 1. Purpose

Improve future maintenance decisions through governed accumulation, validation, reuse and invalidation of knowledge within this skill.

## 2. Learning objectives

- Improve CVE detection accuracy
- Reduce false positives in SAST analysis
- Accelerate dependency update cycle
- Improve code quality suggestions
- Reduce regression rate
- Improve Quality-Judge evaluation consistency

## 3. Learning loop

```
Execution (Phase 0-6.5)
→ Quality-Judge Evaluation (score + gaps)
→ Knowledge Extraction (what worked, what failed)
→ Candidate Lesson (memory/LESSONS.md)
→ Validation (2+ ocorrências ou revisão)
→ Promotion (knowledge/POSITIVE_KNOWLEDGE.md)
→ Reuse in next iteration/execution
→ Revalidation (periodic)
```

## 4. Per-iteration learning

Cada iteração de recursão gera aprendizado:
- O que foi tentado
- O que funcionou (score aumentou)
- O que falhou (score não mudou ou piorou)
- Gaps identificados pelo Quality-Judge

## 5. Learning from recursion

```
Iteração 1: Tentativa A → Score 7.5 → Gap: X
Iteração 2: Tentativa B → Score 9.0 → Gap: Y
Iteração 3: Tentativa C → Score 10.0 → ✅

Lesson: "Para resolver gap X, abordagem B funciona melhor que A"
Confidence: MEDIUM (2 iterações de evidência)
```

## 6. Rules

- Toda execução gera aprendizado (mesmo BLOCKED)
- Separação fato vs inferência
- Validação antes de promoção
- Provenance obrigatória (execution_id)
- Nenhum aprendizado é promovido sem evidência reproduzível
