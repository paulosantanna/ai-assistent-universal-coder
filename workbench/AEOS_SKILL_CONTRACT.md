# AEOS Skill Contract — v1.0.0

## 1. Propósito

Define a estrutura, validação e ciclo de vida de skills no ecossistema AEOS. Skills são unidades de competência reutilizáveis que agentes podem invocar para executar tarefas específicas.

## 2. Estrutura da Skill

```yaml
skill_id: "skill-001"
name: "Skill Name"
version: "1.0.0"
description: "Descrição da skill"
stack: ["java", "spring", "maven"]
objective: "O que esta skill faz"
steps:
  - step_id: "s1"
    name: "Step name"
    description: "Step description"
    tool: "tool.fs.read"
    evidence_required: true
evidence_requirements:
  - type: "code"
    description: "Código modificado"
  - type: "test"
    description: "Testes implementados"
risk_level: "low"
dependencies: []
preconditions:
  - "Pré-condição 1"
postconditions:
  - "Pós-condição 1"
tags: ["java", "migration"]
```

## 3. Registro

Toda skill deve ser registrada no Skill Registry antes do uso.

```yaml
registry:
  - skill_id: "skill-001"
    status: "active"
    version: "1.0.0"
    created: "2026-07-08"
    updated: "2026-07-08"
    verified: true
```

## 4. Factory

O Skill Factory gera skills automaticamente baseado no stack detectado:

1. Scanner detecta stack (ex: Java + Spring + Maven).
2. Factory consulta templates relevantes.
3. Factory gera skill personalizada para o projeto.
4. Skill é registrada e disponibilizada.
5. Agente pode invocar a skill.

## 5. Evaluation

Toda skill deve ser avaliada:

| Critério | Peso |
|----------|------|
| Clareza dos steps | 20% |
| Evidência requerida | 25% |
| Testabilidade | 20% |
| Segurança | 20% |
| Reusabilidade | 15% |

Score mínimo: 7.0/10

## 6. Ciclo de Vida

```
RASCUNHO → REGISTRADA → VERIFICADA → ATIVA → DESATIVADA
                                     ↓
                                  ARQUIVADA
```
