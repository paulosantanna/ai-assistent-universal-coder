# Correções propostas e critérios de aceitação
Updated: 2026-10-15. Owner: codenavi-agent.
Entry point: [fluxo revisado](README.md). Estado: planejamento histórico da revisão. Correções de código R1–R6 aplicadas conforme [verificação posterior](APPLIED.md); direitos, expansão do corpus, avaliação real e projeção continuam condicionados aos dados/contratos necessários.

| Ordem | Ação delimitada | Aceitação verificável |
|---|---|---|
| 1 | Recuperar coleta interrompida por IDs de fonte/janela/checkpoint, após conferir processo atual | Um recibo por job; nenhum replay cego; progresso separado de incompatibilidade e retomada |
| 2 | Resolver direitos e estado atual de cada documento | Treino recusa licença ausente; recuperação só aceita o predicado de uso definido |
| 3 | Corrigir R1/R2: filtro compartilhado para índice, busca e grafo | Rejeitado/retratado/fora de where nunca aparece em evidência ou fatos utilizáveis; revogação remove derivados |
| 4 | Reconciliar disponibilidade documental e vetorial | Cada chunk marcado embedded tem ID confirmado no vector store; cada documento pronto tem todos os chunks exigidos; falhas parciais permanecem explícitas |
| 5 | Criar projeção MongoDB→MCP somente com identidade e versão definidas | Um ID por documento/versão; origem preservada; reprocessamento idempotente; SSE apenas após commit e replay sem duplicar versões |
| 6 | Corrigir R3/R4: execução, splits e promoção | QLoRA failed permanece failed; smoke não é elegível; eval não entra no treino; zero probes implica not_evaluated; promoção exige base/candidato reais e holdout humano |
| 7 | Ampliar corpus e rotular avaliação por dificuldade/domínio | Famílias independentes antes de gerar exemplos; teste com questões fora de título e multi-hop real; cada métrica tem denominador/estado |
| 8 | Calibrar Laya na tarefa biomédica, mantendo decisão determinística | Só influenciar rota/ranking após revisão/medição no domínio; fallback híbrido quando confiança/calibração forem insuficientes |

## R6 — Média: prontidão e avaliação precisam de estados explícitos

`application/rag/indexer.py:13` marca chunks após upsert e reconcilia IDs já existentes. Nesse caminho não atualiza `documents.indexed`; o importador inicial cria a flag como false. O campo deve ser derivado/reconciliado após confirmar todos os chunks, sem tratar um único upsert como conclusão de todo o corpus. Ausência de evidência de vetores nesta revisão deve continuar `not_verified`, mesmo quando o campo `embedded` for true em outra leitura.

`graph_extracted=true` é uma marca de processamento; não garante fatos extraídos. Mostrar `processing_status`, `entity_count`, `fact_count`, versão e erro separadamente. Não considerar o grafo vazio uma falha de conexão sem consultar a saúde do backend.

`application/eval/suite.py:12` mede recuperação por título do próprio corpus. Conservar isso como smoke; registrar `not_evaluated` para métricas ausentes em vez de zero ou um artificiais. Não transportar os resultados dos experimentos técnicos Laya/Qwen para essa base MongoDB.

## Preservação

Manter MongoDB como fonte original, os checkpoints técnicos anteriores intactos e os artefatos biomédicos separados. Nenhum novo MCP, treinamento, download de modelos ou promoção é necessário para concluir a revisão. Implementações futuras devem ser testadas primeiro com falhas reproduzidas e depois com um recorte autorizado, sem alterar os critérios para acomodar o resultado.
