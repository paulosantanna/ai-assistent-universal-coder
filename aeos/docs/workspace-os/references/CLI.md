# CLI do Workspace OS

## Planejar

```powershell
aeos workspace plan --spec plan.json --target E:\workspace
```

O arquivo UTF-8 deve ter no máximo 1 MiB:

```json
{
  "execution_id": "run-001",
  "hard_token_limit": 10000,
  "tasks": [
    {
      "task_id": "inspect",
      "priority": 10,
      "dependencies": [],
      "hard_token_limit": 2500,
      "metadata": {"objective": "map repository"}
    },
    {
      "task_id": "change",
      "priority": 5,
      "dependencies": ["inspect"],
      "hard_token_limit": 7500
    }
  ]
}
```

O comando valida todo o DAG antes da escrita e persiste plano, budgets, snapshots
e evento inicial numa única transação SQLite.

## Consultar

```powershell
aeos workspace status --execution-id run-001 --target E:\workspace
```

`status` abre o banco em modo somente leitura, verifica integridade do SQLite,
hash-chain, head/contagem, replay de tarefas e conservação/replay de tokens.

## Códigos de saída

- `0`: operação concluída e saída JSON determinística.
- `2`: argumento, plano, persistência, integridade ou execução inexistente.

## Limites honestos

Este slice controla reservas e contabilidade, mas ainda não intercepta providers.
Por isso `hard_cap_verifiable` permanece `false` até existir um adapter conforme.
Nenhuma conclusão é aceita sem uma implementação de `EvidenceVerifier` injetada.
