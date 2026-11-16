# Segurança do fluxo RAG inspecionado
Updated: 2026-10-15. Owner: codenavi-agent.
Entry point: [revisão e escopo](README.md). Achados no checkout local `02_repositorios/DiabeticsresearchJEV`; nenhuma exploração de dados reais rejeitados.

## R1 — Alta: filtros divergentes na recuperação

`application/rag/retriever.py:36` constrói BM25 com `iter_chunks({})`. O argumento `where` de `search`, linha48, segue apenas para `vectors.query`; a rota BM25 acrescenta resultados sem revalidar documento pai, aceitação, retratação ou o filtro solicitado. `infrastructure/storage/repositories.py:180` repassa o filtro recebido sem acrescentar um gate.

Reprodução controlada: o vetor retorna vazio; BM25 recebe um chunk artificial cujo documento está em quarentena, fora do `where`; `search` o retorna. Isso confirma quebra de filtro no método, não uma exposição observada na base atual, que contém apenas um documento aceito. Não há evidência suficiente para afirmar como autenticação/ACL de usuários funciona no sistema completo.

Correção: um predicado de elegibilidade comum ao documento pai deve preceder candidatos densos, lexicais e expansão por grafo; repetir a checagem antes de retornar evidência. Invalidar caches e remover derivados quando o estado mudar. Aceitação na coleta não é permissão permanente.

## R2 — Alta: grafo sem gate de entrada do documento

`application/knowledge/graph_service.py:78` seleciona somente `graph_extracted != true`. O repositório não acrescenta aceitação. `ingest_document` extrai e grava entidades/fatos; o FactGate atua sobre fatos e não substitui o gate de admissibilidade do documento pai.

Reprodução controlada: `extract_pending` encaminha um documento artificial em quarentena ao método de ingestão. Correção: exigir aceitação atual e política de retratação antes da extração; validar de novo na recuperação; propagar revogação para fatos e projeções. Testar rejeitado/retratado e mudança posterior de status.

## R3 — Alta: métricas sem execução do candidato podem autorizar promoção

`application/training/continual.py:15` retorna1,0 quando não existem probes; caso existam, procura respostas nos textos das amostras armazenadas. Isso não mede o modelo. `run_continual_cycle` constrói baseline/candidato com incrementos e constantes e atualiza o adaptador para promoted quando o judge aceita esses números. `application/training/trainer.py:106` retorna smoke após exceção do caminho QLoRA.

Reproduções controladas confirmaram acurácia perfeita com zero probes e retorno smoke depois de uma falha simulada de QLoRA. Nenhum modelo foi carregado. A base observada tem zero modelos/execuções; não há promoção real nessa base comprovada pela revisão.

Correção: probes ausentes devem produzir `not_evaluated`; falha QLoRA deve preservar failed e seu motivo; smoke deve ter tipo separado e nunca ser elegível a promoção. Medir base/candidato executados no mesmo holdout e exigir revisão humana antes de promoção.

## R4 — Alta: contaminação entre treino e avaliação

`application/training/trainer.py:108` seleciona splits `train` e `eval` para SFT. `application/training/dataset.py:20,55` produz tarefas e probes a partir do mesmo artigo/chunk, sem agrupamento prévio por família. `application/eval/suite.py:12` usa títulos de documentos do corpus como consultas; esse teste mede recuperação conhecida, com pouca dificuldade no corpus de um documento.

Correção: separar artigo/DOI, versões e famílias antes da geração; treinar somente train; usar validação na seleção e teste humano independente na decisão final. Manter tarefas de título/cloze como smoke explicitamente, sem chamá-las de qualidade clínica ou acurácia do candidato.

## Limites da revisão

Não houve varredura completa de prompt injection, autenticação, endpoints, CVEs ou dependências transitivas do projeto de origem. O MCP atual valida IDs de citações e mantém fallback Laya; esses contratos não demonstram entailment nem transferência de calibração ao domínio da base MongoDB. [Recibos das quatro reproduções](reproductions.json).
