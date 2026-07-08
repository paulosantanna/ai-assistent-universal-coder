# AEOS Playbook Contract — v1.0.0

## 1. Propósito

Define a estrutura e ciclo de vida de playbooks no ecossistema AEOS. Playbooks são sequências de tarefas orquestradas para atingir objetivos de engenharia.

## 2. Estrutura do Playbook

```yaml
playbook_id: "pb-001"
name: "Playbook Name"
version: "1.0.0"
objective: "Objetivo do playbook"
risk_level: "medium"
stacks: ["java", "spring"]
phases:
  - phase_id: "p1"
    name: "Phase name"
    description: "Phase description"
    tasks:
      - task_id: "t1"
        name: "Task name"
        description: "Task description"
        agent: "architect"
        skill: "skill-001"
        evidence_required: true
        approval_required: false
        rollback_plan: true
evidence_requirements:
  - type: "code"
  - type: "test"
  - type: "diff"
rollback_plan:
  steps:
    - "Reverter commit X"
    - "Restaurar arquivo Y"
  verification: "Validar estado anterior"
approval_required: false
tags: ["migration", "java-21"]
```

## 3. Registro

Playbooks são registrados no Playbook Registry e podem ser:
- **Built-in**: Fornecidos pelo AEOS.
- **Gerados**: Criados pelo generator baseado no scan.
- **Custom**: Criados pelo operador humano.

## 4. Execução

1. Playbook é selecionado (manual ou automático).
2. Fases são executadas sequencialmente.
3. Cada tarefa é delegada ao agente apropriado.
4. Evidência é coletada em cada passo.
5. Ao final, Judge avalia o resultado.
6. Se aprovado, playbook é marcado como completo.
7. Se bloqueado, rollback é executado.

## 5. Recomendação Automática

Baseado no ecosystem scan:
- Stack detectado → playbooks relevantes recomendados.
- Riscos detectados → playbooks de mitigação recomendados.
- Débito técnico → playbooks de refatoração recomendados.

## 6. Rollback

Todo playbook destrutivo deve ter rollback plan:
- Snapshot de estado antes da execução.
- Passos de reversão.
- Verificação de integridade pós-rollback.
- Aprovação humana para rollback automático.
