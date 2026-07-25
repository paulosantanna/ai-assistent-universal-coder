# ADR-0001: Workspace OS por strangler sobre o núcleo Python

## Status

`PROPOSED`

## Contexto

O AEOS possui runtimes e CLIs concorrentes, enquanto seus componentes de grafo
de tarefas e orçamento de tokens não governam o runtime principal. A auditoria
`chromatic-20260724-workspace-os` também encontrou estados livres, contabilidade
posterior ao consumo e dependências bloqueadas tratadas como concluídas.

O objetivo humano é operar o AEOS como um Workspace OS local, capaz de controlar
tarefas complexas e seu custo de tokens com o menor desperdício possível, sem
substituir correção e evidência por otimização.

## Problema

O sistema precisa de uma autoridade única para:

- estados e dependências de tarefas;
- reservas e consumo de tokens;
- planejamento determinístico;
- checkpoints;
- evidência necessária para conclusão.

Criar outro runtime completo aumentaria a fragmentação. Integrar imediatamente
os runtimes existentes aumentaria o raio de regressão antes de os invariantes
centrais estarem comprovados.

## Restrições

- O primeiro slice não chama modelos, ferramentas, MCPs ou runtimes legados.
- Não migra nem escreve em estados legados.
- Não altera policy, autorização, providers ou automações de merge.
- `BLOCKED` nunca satisfaz uma dependência.
- Uma conclusão exige evidência tipada e verificável.
- Limite rígido de tokens só pode ser alegado para adapters que imponham limite
  e reportem uso confiável.
- Uso real, estimado e não medido permanecem classes distintas.

## Opções consideradas

### 1. Ajustar somente limites e configuração

Rejeitada. Os governadores existentes não interceptam todas as chamadas e não
reservam orçamento antes do consumo.

### 2. Conectar diretamente o gerenciador de tokens existente

Rejeitada como arquitetura final. Ele cobra após o consumo, não é durável e
mantém uma segunda fonte de verdade.

### 3. Criar um microkernel protocol-first paralelo

Adiada. É um possível destino, mas criaria outro runtime antes de existir uma
conformance suite.

### 4. Reescrever o runtime completo

Rejeitada. O risco e a superfície de migração são incompatíveis com o baseline
atual.

### 5. Monólito modular com strangler

Selecionada para o primeiro slice. Um namespace isolado em
`aeos/core/workspace/` introduz contratos e invariantes comprováveis. A adoção
por comandos existentes ocorrerá somente depois de testes diferenciais.

## Decisão proposta

Implementar um `WorkspaceKernel` Python isolado, inicialmente acessível apenas
por:

- `aeos workspace plan`;
- `aeos workspace status`.

O slice conterá:

- tipos fechados para estado de tarefa, resultado e qualidade de medição;
- máquina de estados com revisão otimista;
- DAG validado e scheduler determinístico;
- ledger hierárquico de tokens com reserva, reconciliação e liberação;
- store SQLite transacional exclusivo;
- checkpoints e resultados vinculados à revisão;
- contrato de claims que separa fatos, inferências, suposições e desconhecidos.

## Trust boundary

```text
CLI workspace
      |
      v
WorkspaceKernel -- único commit point do novo namespace
  |-- TaskMachine / DAG
  |-- TokenLedger
  |-- SQLite WorkspaceStore
  `-- Checkpoint / Evidence contracts

Runtimes, providers, MCPs e ferramentas: fora do boundary neste slice.
```

## Consequências

### Positivas

- controle de tarefas e orçamento testável antes de integração;
- rollback por remoção do namespace novo;
- nenhuma quinta implementação de provider ou runtime;
- base para adapters e protocolo público posteriores.

### Negativas

- o slice ainda não executa tarefas reais em modelos;
- SQLite passa a exigir testes de schema, concorrência e recovery;
- coexistência temporária com componentes legados.

## Plano de validação

- testes unitários e de contrato para todos os estados e invariantes;
- property tests para DAG e orçamento;
- concorrência sobre reservas e CAS;
- reopen, recovery e detecção de schema inválido;
- smoke da CLI e códigos de saída;
- regressão Python completa;
- Judge independente após a implementação.

## Rollback

O novo namespace não faz dual-write nem migração. A remoção dos comandos
`workspace` e de `aeos/core/workspace/` restaura o comportamento anterior.
Nenhum rollback poderá reativar comportamento inseguro dentro do novo namespace.

## Gatilho de revisão

Revisar esta ADR após o vertical slice passar pelos gates ou antes de:

- interceptar `agent run`, skills ou playbooks;
- chamar um provider;
- publicar o protocolo para outro CLI;
- migrar estado legado;
- declarar controle rígido de tokens em produção.

## Evidência

- `aeos/core/agent_runtime/task_graph.py`: `BLOCKED` libera dependências.
- `aeos/core/tokens/token_budget_manager.py`: consumo é cobrado antes do bloqueio.
- `aeos/core/token_budget/token_budget.py`: estimativa baseada em caracteres.
- handback `AEOS-20260724-JUDGE-WORKSPACEOS-002`: `PASS_WITH_LIMITATIONS`.
