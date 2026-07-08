# AEOS Memory Model — v1.0.0

## 1. Propósito

Define como o AEOS persiste, recupera e utiliza conhecimento entre sessões. Memória é a base do aprendizado contínuo.

## 2. Tipos de Memória

### 2.1 Semantic Memory
Conceitos, fatos e conhecimento geral do domínio.
- Armazena: definições, padrões, tecnologias, convenções.
- Fonte: documentos, schemas, golden knowledge.
- Formato: key-value com embeddings.

### 2.2 Architectural Memory
Decisões arquiteturais e rationale.
- Armazena: ADRs, patterns, trade-offs.
- Fonte: Architecture Decision Records.
- Formato: ADR estruturado + justificativa.

### 2.3 Procedural Memory
Como fazer tarefas (procedimentos, playbooks).
- Armazena: sequências de passos, comandos, checklists.
- Fonte: skills, playbooks executados.
- Formato: lista ordenada de steps.

### 2.4 Episodic Memory
Eventos passados, incluindo falhas e sucessos.
- Armazena: execuções de tarefas, resultados, decisões.
- Fonte: logs de execução, resultados de judge.
- Formato: narrativa temporal.

### 2.5 Operational Memory
Configuração operacional do ambiente.
- Armazena: tool configs, permissões, políticas ativas.
- Fonte: aeos.ecosystem.yaml, policy store.
- Formato: YAML/JSON.

### 2.6 Lessons Learned
Lições extraídas de episódios.
- Do: O que funcionou.
- Don't: O que não funcionou.
- Formato: contexto + causa + ação corretiva.

## 3. Ciclo de Vida

```
Observation → Evidence → Finding → Lesson → Validated Lesson → Golden Knowledge → Principle
```

## 4. Armazenamento

- Memórias são persistidas em JSONL no diretório `workbench/Memory/`.
- Cada tipo de memória tem seu próprio subdiretório.
- Índice de embeddings para busca semântica.
- TTL configurável por tipo de memória.

## 5. Busca

| Tipo de Busca | Algoritmo | Retorno |
|---------------|-----------|---------|
| Semântica | Cosine similarity sobre embeddings | Top 5 memórias relevantes |
| Exata | Match de chave | Memória específica |
| Temporal | Range de timestamp | Memórias em período |
| Por agente | Filtro por agent_id | Memórias do agente |

## 6. Podas

- Memórias não acessadas por 90 dias são arquivadas.
- Memórias arquivadas há 365 dias são excluídas.
- Golden knowledge nunca é podada.
- Lições validadas nunca são podadas.

## 7. Imutabilidade

- Nenhuma memória pode ser alterada, apenas complementada.
- A versão anterior é preservada como "history".
- Toda alteração gera nova entry com referência à anterior.
