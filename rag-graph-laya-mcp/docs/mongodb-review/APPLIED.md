# Correções R1–R6 aplicadas
Updated: 2026-10-15. Owner: codenavi-agent.
Entry point: [revisão original](README.md). Evidência: [recibo aplicado](applied-verification.json).

As correções foram aplicadas ao checkout `02_repositorios/DiabeticsresearchJEV`. O relatório de auditoria anterior permanece como retrato das falhas nos originais; a implementação atual está descrita em [FLOW-HARDENING.md](../../../02_repositorios/DiabeticsresearchJEV/FLOW-HARDENING.md).

| Achado | Comportamento corrigido |
|---|---|
| R1 | Predicado comum para vetor/BM25, filtros de metadados limitados, chunks atuais e revalidação após reranking |
| R2 | Gate do pai na extração direta/pendente e na travessia; versões de origem; invalidação de fatos sem suporte atual; espelho sem autoridade para liberar conteúdo |
| R3 | QLoRA mantém falha explícita; smoke separado; métricas ausentes ficam null/not_evaluated; promoção exige recibo de avaliação real, revisão e melhoria; registro legado não libera serving |
| R4 | Famílias e versões em partições estáveis; SFT só usa train do ciclo; fontes/hashes revalidados; holdouts excluídos também de replay legado |
| R5 | Licença e autorização explícita por finalidade antes de gerar/treinar; acesso aberto não preenche permissão automaticamente |
| R6 | Índice confirma IDs vetoriais e prontidão de todos os chunks; grafo tem estado/contagens separados; avaliação por título é smoke com denominador; skip distingue motivo |

Verificação atual: **100 testes aprovados, Ruff aprovado e zero erros no mypy strict dos 86 arquivos de código**. A etapa R1–R6 começou com66 testes e13 regressões congeladas que falharam nos originais; terminou com92 testes e48 erros preexistentes. A correção posterior resolveu esses48 erros e adicionou oito regressões de fronteiras HTML, embeddings, DOAJ e JSON. Detalhes e runtime atual em [TYPING-RUNTIME.md](TYPING-RUNTIME.md); [recibo atual](typing-runtime-verification.json). O recibo aplicado anterior permanece como evidência histórica dessa primeira etapa.

A leitura real posterior confirmou contagens e fingerprint inalterados:1documento/1chunk/3.560termos; zero documentos com direitos de treino verificados. Os82arquivos originais de código/testes fora do conjunto esperado foram preservados; inicialização/configuração preexistentes mantidas. Dados de origem e checkpoints foram preservados. Os serviços de aplicação foram recarregados na etapa posterior descrita abaixo; MongoDB e Neo4j mantiveram seus processos.

O ambiente virtual copiado aponta para outro checkout; os testes selecionaram explicitamente o `src` corrigido. O novo `scripts/run_api.py` seleciona esse mesmo código antes dos imports. A API biomédica foi iniciada na porta8000; o MCP8765 e o serviço de modelos8008 foram recarregados, com identidade/PIDs/HTTP verificados. O checkout externo não foi modificado.

Continuam como pré-requisitos de dados: resolver direitos, ampliar estudos independentes, revisar holdout e executar avaliação pareada real. A integração MongoDB→MCP técnico é uma projeção futura com contrato próprio; não foi criada como efeito dessas correções. Não houve novo treino, inferência biomédica, download de modelos, commit ou push.
