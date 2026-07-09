# AEOS Evolution Pack v0.7 — Agent Runtime & Delegation Layer

## Objetivo

Este pacote evolui o AEOS para a camada **v0.7 — Agent Runtime & Delegation Layer**.

Ele adiciona a fundação para:

- Agent Runtime;
- Root Agent supervisor;
- subagentes especializados;
- task graph;
- delegation policies;
- message protocol entre agentes;
- context routing;
- memory governance;
- escalation rules;
- agent trace;
- Judge v7 para validação de delegação.

## Onde descompactar

Descompacte este ZIP por cima do projeto AEOS:

```powershell
cd E:\GitHub\aeos\AEOS_CHIEF_STAFF_v1
Expand-Archive -Path "C:\Users\SEU_USUARIO\Downloads\aeos_evolution_pack_v0_7_agent_runtime.zip" -DestinationPath . -Force
```

## Ordem esperada

Este pack pressupõe que você já aplicou:

```text
v0.5 — Packaging Layer
v0.6 — MCP Runtime Expansion Layer
```

## Ainda proibido nesta versão

- agente executando ferramenta diretamente;
- agente aprovando o próprio trabalho;
- auto-merge;
- auto-deploy;
- secrets runtime real;
- browser com login;
- shell irrestrito;
- banco com escrita;
- agentes mutando produção;
- subagente ignorando Permission Engine, Policy Engine, Tool Router ou Judge.

## Próximo prompt para o agente

Use dentro de `E:\GitHub\aeos\AEOS_CHIEF_STAFF_v1`:

```text
Leia INSTALL_v0_7.md, AEOS_V0_7_AGENT_RUNTIME.md, AEOS_AGENT_ORCHESTRATION.md, AEOS_AGENT_MESSAGE_PROTOCOL.md, AEOS_TASK_DELEGATION_CONTRACT.md, AEOS_SUBAGENT_SYSTEM.md, AEOS_CONTEXT_ROUTING.md, AEOS_MEMORY_GOVERNANCE.md, AEOS_JUDGE_V7_AGENT_RULES.md e os arquivos em aeos/config relacionados a agent runtime. Implemente a camada AEOS v0.7 Agent Runtime & Delegation Layer garantindo que agentes apenas planejem, deleguem e solicitem ações via Kernel/Tool Router, nunca acessando ferramentas diretamente. O Judge Agent deve permanecer independente de qualquer agente executor.
```
