# HANDOFF.md
# AI Continuous Training Maintainer — Responsibility Transfer Protocol

## 1. Purpose

Formal transfer of bounded responsibility, context, authority and evidence between agents within this skill.

## 2. Handoff principles

1. Responsibility must be explicit
2. Scope must be bounded
3. Authority must be limited
4. Context must be sufficient but minimal
5. Evidence must travel with claims
6. Assumptions must be visible
7. Risks must not be hidden
8. Acceptance must be acknowledged
9. Scope changes require amendment
10. Completion requires handback acceptance

## 3. Handoff directions

- ROOT → PARENT (domain delegation)
- PARENT → CHILD (atomic task)
- CHILD → PARENT (evidence handback)
- PARENT → ROOT (consolidated handback)
- ROOT → Quality-Judge (evaluation dispatch)

## 4. Canonical handoff envelope

```yaml
handoff:
  handoff_id: <uuid>
  version: 1
  skill: ai-continuous-training-maintainer
  iteration: <recursion iteration number>

  source:
    role: ROOT | PARENT
    domain: <domain>

  target:
    role: PARENT | CHILD | Quality-Judge
    domain: <domain>

  objective:
    statement: <o que fazer>
    expected_outcome: <resultado esperado>

  scope:
    included: <arquivos/diretórios>
    excluded: <fora do escopo>
    allowed_paths: <caminhos permitidos>
    forbidden_paths: <caminhos proibidos>

  context:
    summary: <contexto relevante>
    baseline_ref: <referência ao baseline>
    gaps_from_previous_iteration: <se aplicável>

  constraints:
    technical: <restrições técnicas>
    recursion_count: <iteração atual>
    max_recursion: <limite>

  evidence:
    required: <evidências esperadas>
    format: <formato>

  verification:
    required_tests: <testes obrigatórios>
    acceptance_criteria: <critérios de aceite>
    stop_conditions: <condições de parada>

  expected_handback:
    format: <formato>
    required_sections: <seções obrigatórias>

  acknowledgment:
    receiver_status: ACCEPTED | REJECTED | BLOCKED
    acknowledged_at: <timestamp>
```

## 5. Minimum validity rules

A handoff is invalid when missing: handoff_id, source role, target role, objective, scope, authority limits, acceptance criteria, stop conditions, evidence expectations, expected handback, acknowledgment.

## 6. Handback requirements

Must include: original handoff_id, status, work completed, scope deviations, files changed, commands and tests, evidence index, failures, unresolved findings, risks, candidate lessons, confidence.
