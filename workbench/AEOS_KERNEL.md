# AEOS Kernel Specification — v1.0.0

## 1. Propósito

O Kernel é o núcleo operacional do AEOS Workbench. Ele orquestra agentes, roteia chamadas de ferramentas, gerencia contexto, aplica políticas de segurança e mantém o ciclo de vida do ambiente.

## 2. Arquitetura

```
┌─────────────────────────────────────────────────┐
│                   Kernel                         │
│  ┌──────────┐  ┌──────────┐  ┌──────────────┐  │
│  │ Tool     │  │ Scheduler│  │ Context      │  │
│  │ Router   │  │          │  │ Manager      │  │
│  ├──────────┤  ├──────────┤  ├──────────────┤  │
│  │ Policy   │  │ Memory   │  │ Evidence     │  │
│  │ Enforcer │  │ Bridge   │  │ Collector    │  │
│  ├──────────┤  ├──────────┤  ├──────────────┤  │
│  │ Audit    │  │ Rollback │  │ Security     │  │
│  │ Logger   │  │ Manager  │  │ Validator    │  │
│  └──────────┘  └──────────┘  └──────────────┘  │
└─────────────────────────────────────────────────┘
```

## 3. Componentes

### 3.1 Tool Router
- Único ponto de entrada para acesso a recursos externos.
- Valida permissões antes de encaminhar.
- Registra toda chamada com timestamp, agente, parâmetros e resultado.
- Aplica política de segurança (secrets detection, destructive action check).
- Bloqueia chamadas não autorizadas.

### 3.2 Scheduler
- Gerencia fila de tarefas.
- Controla concorrência (max_concurrent_tasks = 5).
- Implementa retry com backoff.
- Persiste estado da fila para recuperação.

### 3.3 Context Manager
- Mantém contexto compartilhado entre agentes.
- Implementa windowing sliding para gerenciamento de tokens.
- Preserva histórico relevante.
- Expurga informações sensíveis automaticamente.

### 3.4 Policy Enforcer
- Carrega e interpreta políticas do Policy Engine.
- Aplica regras em tempo de execução.
- Bloqueia violações.
- Gera evidência de decisão.

### 3.5 Memory Bridge
- Interface entre Kernel e Memory System.
- Resgata memórias relevantes para contexto.
- Persiste novas memórias.
- Suporta busca semântica e procedural.

### 3.6 Evidence Collector
- Recebe evidências dos agentes.
- Valida formato e conteúdo.
- Persiste no Evidence Store.
- Gera hash de integridade.

### 3.7 Audit Logger
- Registra toda operação do Kernel.
- Logs são imutáveis e timestamped.
- Suporta exportação para formato JSON.

### 3.8 Rollback Manager
- Mantém snapshots de estado.
- Executa rollback quando necessário.
- Verifica integridade pós-rollback.

### 3.9 Security Validator
- Escaneia inputs e outputs por segredos.
- Aplica redação automática.
- Bloqueia vazamentos.

## 4. Ciclo de Operação

```
1. INICIALIZAR — Carregar configuração, verificar integridade, validar ambiente.
2. ESCUTAR — Aguardar requisições de agentes ou comandos CLI.
3. ROTEAR — Validar permissões, encaminhar ao tool handler.
4. EXECUTAR — Executar ação com monitoramento.
5. COLETAR — Registrar evidências, métricas e logs.
6. AVALIAR — Verificar resultado contra políticas.
7. RESPONDER — Retornar resultado ao agente requisitante.
8. PERSISTIR — Atualizar memória, armazenar evidências.
```

## 5. Interface

```typescript
interface Kernel {
  initialize(config: KernelConfig): Promise<KernelStatus>;
  route(request: ToolRequest): Promise<ToolResponse>;
  execute(task: Task): Promise<TaskResult>;
  collect(event: Evidence): Promise<void>;
  evaluate(result: TaskResult): Promise<JudgeEvaluation>;
  shutdown(): Promise<void>;
}
```

## 6. Políticas de Kernel

| Política | Descrição | Ação em Violação |
|----------|-----------|------------------|
| no_direct_access | Nenhum agente acessa recursos externos diretamente | Bloquear chamada |
| destructive_approval | Ações destrutivas requerem aprovação humana | Bloquear até aprovação |
| evidence_required | Toda alteração requer evidência | Bloquear finalização |
| secrets_blocked | Nenhum segredo em texto puro | Redigir e bloquear |
| judge_separation | Judge ≠ Implementador | Invalidar julgamento |

## 7. Tratamento de Erros

- Erros de permissão → Bloquear e notificar.
- Erros de validação → Rejeitar com descrição.
- Erros de execução → Retentar (até 3x) ou falhar.
- Erros críticos → Shutdown seguro com dump de estado.
