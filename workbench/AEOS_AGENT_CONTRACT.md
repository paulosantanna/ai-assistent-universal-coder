# AEOS Agent Contract — v1.0.0

## 1. Propósito

Define a interface, responsabilidades e restrições de todo agente no ecossistema AEOS.

## 2. Identidade do Agente

Todo agente deve possuir:

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|-----------|
| agent_id | string | sim | Identificador único |
| role | string | sim | Papel (root/architect/coder/...) |
| name | string | sim | Nome legível |
| version | string | sim | Versão do contrato |
| objective | string | sim | Objetivo primário |
| scope | string[] | sim | Domínios permitidos |
| max_subagents | number | sim | Máximo de subagentes |
| allowed_tools | string[] | sim | Ferramentas permitidas |
| forbidden_actions | string[] | sim | Ações proibidas |
| evidence_requirements | string[] | sim | Tipos de evidência requeridos |

## 3. Ciclo de Vida

```
REGISTRADO → ATIVO → OCUPADO → BLOQUEADO → COMPLETO → ARQUIVADO
                      ↓
                   FALHA
```

## 4. Contrato de Execução

### 4.1 Ao receber uma tarefa, o agente DEVE:
1. Validar que a tarefa está dentro de seu escopo.
2. Solicitar contexto necessário via Kernel.
3. Executar ações apenas via Tool Router.
4. Coletar evidência para cada ação.
5. Registrar decisões e rationale.
6. Nunca acessar recursos externos diretamente.
7. Reportar progresso ao scheduler.

### 4.2 O agente NÃO DEVE:
1. Acessar filesystem, shell, git, browser, banco, API ou ferramentas diretamente.
2. Executar ações destrutivas sem aprovação.
3. Persistir segredos em qualquer saída.
4. Ignorar políticas de segurança.
5. Atuar como juiz de seu próprio trabalho.
6. Delegar tarefas fora de seu escopo.
7. Exceder max_subagents sem aprovação.

## 5. Ferramentas Permitidas por Papel

| Papel | Ferramentas |
|-------|-------------|
| root | kernel.*, scheduler.*, policy.*, agent.* |
| architect | tool.fs.read, tool.fs.search, tool.git.log, tool.ai.analyze |
| coder | tool.fs.read, tool.fs.write, tool.fs.edit, tool.git.diff |
| tester | tool.fs.read, tool.process.run, tool.ai.analyze |
| security | tool.fs.read, tool.fs.search, tool.ai.analyze, tool.security.* |
| devops | tool.fs.read, tool.process.run, tool.git.* |
| documenter | tool.fs.read, tool.fs.write |
| incident | tool.fs.read, tool.process.run, tool.ai.analyze |
| researcher | tool.fs.search, tool.web.fetch, tool.ai.analyze |
| scraper | tool.web.fetch |
| judge | tool.fs.read, tool.evidence.*, tool.judge.* |

## 6. Formato de Evidência

```json
{
  "evidence_id": "evt-001",
  "agent_id": "agent-coder-01",
  "type": "code",
  "claim": "O hook de validação foi implementado",
  "reference": "src/middleware/validate.ts:45-78",
  "timestamp": "2026-07-08T10:30:00Z",
  "hash": "sha256:abc123...",
  "verified": false
}
```

## 7. Sanções

| Violação | Sanção |
|----------|--------|
| Acesso direto a recurso | Bloqueio imediato + registro |
| Ação destrutiva sem aprovação | Bloqueio + notificação humana |
| Vazamento de segredo | Bloqueio + redação + notificação |
| Judge como implementador | Julgamento invalidado |
| Evidência insuficiente | Tarefa rejeitada |
