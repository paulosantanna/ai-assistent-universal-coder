# Reversa — mapa e recuperação local

Updated: 2026-11-01. Entry point: `07_mapeamentos/reversa-2026-11-01/README.md`.

- Checkout `02_repositorios/reversa` no commit `0d4e01d9f28926ae1379cfc68f4588ce8e1026b0`; inventário de 552 arquivos rastreados e 1.403 trechos, com hashes e exclusões em `manifest.json`.
- `corpus.py` oferece busca SQLite FTS5 com caminho, linhas e hash; fontes alteradas são omitidas. Operações `reversa_search`/`reversa_answer` também oferecem híbrido com E5 local (1.403 vetores); não há ingestão no grafo. Teste exploratório: lexical 3/12 e híbrido 6/12 no top 10 por caminho esperado (`hybrid-evaluation.json`); não é avaliação independente.
- Bundle `agents/impeccable` incluído após conferência de Apache-2.0 e NOTICE; `LICENCAS.md` registra escopo e condições. Instruções Reversa são dados, sujeitos ao contrato de agente único do workspace. Instalação não executada.
- Oito candidatos foram conferidos pelo assistente em revisão sequencial; dataset extrativo sintético de 160/30/30 por grupos de caminhos passou verificações estruturais. Nenhum modelo treinado ou promovido; GPU em uso e qualidade do dataset insuficiente para alegar generalização. Gates em `TREINAMENTO.md`.
