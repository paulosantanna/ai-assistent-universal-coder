# Tipagem e runtime corrigidos

Updated: 2026-10-15. Owner: codenavi-agent. Herda o AGENTS.md do workspace.
Entry point: [estado aplicado](APPLIED.md). [Recibo verificável](typing-runtime-verification.json).

Os 48 erros restantes do mypy foram corrigidos no checkout `02_repositorios/DiabeticsresearchJEV`. O modo strict permanece ativo, sem novos ignores, dependências ou relaxamento de configuração. O baseline desta etapa passou 92 testes; a versão final passa 100, com Ruff aprovado e zero erros nos 86 arquivos de código.

As correções alinham as assinaturas dos conectores ao contrato de paginação opcional; declaram os idiomas suportados nas classes extensíveis; tipam passagens/contexto do GraphRAG e o container de serviços; preservam a serialização JSON do GraphQL; validam atributos HTML antes de usar URLs; e normalizam embeddings para os tipos aceitos pelo Chroma. O fallback de embeddings descarta um provedor com dimensão inválida antes de voltar ao hashing. As oito novas regressões cobrem atributos HTML, resultados NumPy/fallback, anos opcionais no DOAJ e respostas JSON reais do GraphQL. Os 26 testes de endurecimento R1–R6 continuam aprovados, incluindo Chroma temporário real.

## Serviços verificados

| Serviço | Endereço | Estado observado |
|---|---|---|
| API biomédica | http://127.0.0.1:8000 | Iniciada neste checkout; PID 49000 atende HTTP 200 e GraphQL |
| Modelos locais | http://127.0.0.1:8008/v1/models | Recarregado; PID 68372 atende HTTP 200, sem pausa |
| MCP e grafo | http://127.0.0.1:8765 | Recarregado; PID 66624 atende HTTP 200, modelos/Neo4j disponíveis |

Os PIDs acima identificam os processos que escutam; os launchers têm PIDs próprios no recibo. Não havia API biomédica na porta 8000 antes desta etapa. O inicializador `scripts/run_api.py` seleciona o `src` do checkout antes dos imports, pois o ambiente virtual copiado ainda referencia uma instalação editável externa. A origem e os hashes dos módulos API/GraphQL/serviços foram conferidos dentro do processo carregado, além da identidade dos listeners e das páginas `/ui/graph` e `/ui/live`.

A primeira tentativa de recarga encerrou o serviço de modelos antes de uma falha de permissão do ambiente. A recuperação confirmou que a porta estava livre, iniciou somente o serviço próprio e atualizou o recibo; o restart subsequente do MCP também foi concluído. A verificação final confirmou ambos ativos. MongoDB PID 30980 e Neo4j PID 61308 mantiveram os horários originais de criação. Não foram iniciados coletores ou treinos.

## Dados e limites

Leitura agregada somente leitura: contagens e fingerprint do corpus MongoDB inalterados. Permanecem 1 documento, 1 chunk e 3560 termos. Os direitos de treino, a revisão humana do holdout e a avaliação pareada de modelos continuam pendentes. Nenhum checkpoint foi promovido. O endpoint de modelos está pronto; pesos são carregados sob demanda e nenhuma nova inferência foi usada nesta verificação.

Persistem dois avisos de depreciação em dependências, sem falhas nos checks. O checkout externo e as alterações anteriores foram preservados. Não houve commit ou push. Baseline, backups, logs completos e recibos intermediários estão em `.work/mypy-runtime/` no workspace; o JSON vinculado conserva hashes antes/depois, contagens, PIDs e resultados agregados sem dados clínicos ou credenciais.
