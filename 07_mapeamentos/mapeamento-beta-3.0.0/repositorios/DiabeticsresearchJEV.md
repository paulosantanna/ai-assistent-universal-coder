# DiabeticsresearchJEV — beta 3.0.0

Updated: 2026-10-27
Entry point: [índice](../README.md) · [mapa estruturado](../mapa.json)

Arquivos com hash: 137; fingerprint: `8cefd5d22d4f4c0dacb84576963943d50d3019554081482f5d262b6a94d21a9c`.
Git próprio: True; HEAD: `05b346419db9049163ad3e28d6cac7715d4a9131`; branch: `main`.
Estado local: há alterações/não rastreados; detalhes em inventory.json.

## Atualizações e reconciliação

Registra hardening local: direitos de treinamento, smoke separado, DPO not_run e promoção condicionada. Relatos de testes/runtime são históricos.

## Dimensões e evidências

### Propósito

**declarado** — Pesquisa biomédica em diabetes com coleta multilíngue, GraphRAG e treino contínuo QLoRA.

[DiabeticsresearchJEV/pyproject.toml:8](../../../02_repositorios/DiabeticsresearchJEV/pyproject.toml)

### Arquitetura

**observado** — Camadas application/domain/infrastructure/interfaces; API REST e GraphQL usam serviços compartilhados.

[DiabeticsresearchJEV/src/diabeticsresearchjev/interfaces/api.py:12](../../../02_repositorios/DiabeticsresearchJEV/src/diabeticsresearchjev/interfaces/api.py)

### Fluxo

**código presente** — Ciclo coleta, extrai grafo, indexa, treina candidato e avalia; smoke é distinto de QLoRA.

[DiabeticsresearchJEV/src/diabeticsresearchjev/application/pipeline/full_cycle.py:35](../../../02_repositorios/DiabeticsresearchJEV/src/diabeticsresearchjev/application/pipeline/full_cycle.py)

### Dados

**documentado** — MongoDB nativo e Chroma embutido são documentados; Compose descreve espelhos de serviços de dados.

[DiabeticsresearchJEV/docker-compose.yml:8](../../../02_repositorios/DiabeticsresearchJEV/docker-compose.yml)

### Interfaces

**observado** — HybridRetriever combina Chroma, BM25 e expansão opcional por grafo; GraphQL fica em /graphql.

[DiabeticsresearchJEV/src/diabeticsresearchjev/application/rag/retriever.py:1](../../../02_repositorios/DiabeticsresearchJEV/src/diabeticsresearchjev/application/rag/retriever.py)

### Configuração/deploy

**documentado** — Compose declara serviços locais; comentários de equivalência AWS são intenção, não prova de implantação AWS.

[DiabeticsresearchJEV/docker-compose.yml:2](../../../02_repositorios/DiabeticsresearchJEV/docker-compose.yml)

### Operação

**documentado** — Hardening documenta direitos de treino, separação por família e recibo de avaliação para promoção; resultados históricos não reexecutados.

[DiabeticsresearchJEV/FLOW-HARDENING.md:19](../../../02_repositorios/DiabeticsresearchJEV/FLOW-HARDENING.md)

### Fine-tuning

**código presente** — QLoRA/SFT real separado de smoke; smoke não é elegível para promoção.

[DiabeticsresearchJEV/src/diabeticsresearchjev/application/training/trainer.py:31](../../../02_repositorios/DiabeticsresearchJEV/src/diabeticsresearchjev/application/training/trainer.py)

### RAG

**código presente** — GraphRAG combina recuperação e evidência de grafo; acesso depende de serviços e corpus.

[DiabeticsresearchJEV/src/diabeticsresearchjev/application/knowledge/graphrag.py:31](../../../02_repositorios/DiabeticsresearchJEV/src/diabeticsresearchjev/application/knowledge/graphrag.py)

### Pós-treino

**código presente** — DPO não fabrica preferências; retorna not_run no caminho ainda não executável.

[DiabeticsresearchJEV/src/diabeticsresearchjev/application/training/trainer.py:125](../../../02_repositorios/DiabeticsresearchJEV/src/diabeticsresearchjev/application/training/trainer.py)

### Inferência

**não demonstrado na amostra** — Sem conclusão positiva nesta revisão estática; não equivale a ausência universal.


### Tecnologias/versões

**declarado** — Ver declarações extraídas e manifests; versões instaladas e compatibilidade não verificadas.

[DiabeticsresearchJEV/pyproject.toml:10](../../../02_repositorios/DiabeticsresearchJEV/pyproject.toml)
[DiabeticsresearchJEV/pyproject.toml:21](../../../02_repositorios/DiabeticsresearchJEV/pyproject.toml)
[DiabeticsresearchJEV/pyproject.toml:22](../../../02_repositorios/DiabeticsresearchJEV/pyproject.toml)
[DiabeticsresearchJEV/pyproject.toml:23](../../../02_repositorios/DiabeticsresearchJEV/pyproject.toml)
[DiabeticsresearchJEV/pyproject.toml:24](../../../02_repositorios/DiabeticsresearchJEV/pyproject.toml)
[DiabeticsresearchJEV/pyproject.toml:25](../../../02_repositorios/DiabeticsresearchJEV/pyproject.toml)
[DiabeticsresearchJEV/pyproject.toml:26](../../../02_repositorios/DiabeticsresearchJEV/pyproject.toml)
[DiabeticsresearchJEV/pyproject.toml:27](../../../02_repositorios/DiabeticsresearchJEV/pyproject.toml)

### Vulnerabilidades

**não verificado** — Sem consulta de CVE/EOL nesta missão.


### Obsolescência

**não verificado** — Sem consulta de CVE/EOL nesta missão.


## Declarações de versão

| Manifest / declaração | Valor | Evidência |
|---|---|---|
| name | diabeticsresearchjev | [DiabeticsresearchJEV/pyproject.toml:6](../../../02_repositorios/DiabeticsresearchJEV/pyproject.toml) |
| version | 0.2.0 | [DiabeticsresearchJEV/pyproject.toml:7](../../../02_repositorios/DiabeticsresearchJEV/pyproject.toml) |
| requires-python | >=3.11 | [DiabeticsresearchJEV/pyproject.toml:10](../../../02_repositorios/DiabeticsresearchJEV/pyproject.toml) |
| dependency | pydantic>=2.7.0 | [DiabeticsresearchJEV/pyproject.toml:21](../../../02_repositorios/DiabeticsresearchJEV/pyproject.toml) |
| dependency | pydantic-settings>=2.3.0 | [DiabeticsresearchJEV/pyproject.toml:22](../../../02_repositorios/DiabeticsresearchJEV/pyproject.toml) |
| dependency | fastapi>=0.111.0 | [DiabeticsresearchJEV/pyproject.toml:23](../../../02_repositorios/DiabeticsresearchJEV/pyproject.toml) |
| dependency | uvicorn>=0.30.0 | [DiabeticsresearchJEV/pyproject.toml:24](../../../02_repositorios/DiabeticsresearchJEV/pyproject.toml) |
| dependency | websockets>=12.0 | [DiabeticsresearchJEV/pyproject.toml:25](../../../02_repositorios/DiabeticsresearchJEV/pyproject.toml) |
| dependency | httpx>=0.27.0 | [DiabeticsresearchJEV/pyproject.toml:26](../../../02_repositorios/DiabeticsresearchJEV/pyproject.toml) |
| dependency | rich>=13.7.0 | [DiabeticsresearchJEV/pyproject.toml:27](../../../02_repositorios/DiabeticsresearchJEV/pyproject.toml) |
| dependency | typer>=0.12.0 | [DiabeticsresearchJEV/pyproject.toml:28](../../../02_repositorios/DiabeticsresearchJEV/pyproject.toml) |
| dependency | pymongo>=4.8.0 | [DiabeticsresearchJEV/pyproject.toml:29](../../../02_repositorios/DiabeticsresearchJEV/pyproject.toml) |
| dependency | chromadb>=1.0.0 | [DiabeticsresearchJEV/pyproject.toml:30](../../../02_repositorios/DiabeticsresearchJEV/pyproject.toml) |
| dependency | strawberry-graphql[fastapi]>=0.240.0 | [DiabeticsresearchJEV/pyproject.toml:31](../../../02_repositorios/DiabeticsresearchJEV/pyproject.toml) |
| dependency | numpy>=1.26.0 | [DiabeticsresearchJEV/pyproject.toml:32](../../../02_repositorios/DiabeticsresearchJEV/pyproject.toml) |
| dependency | networkx>=3.3 | [DiabeticsresearchJEV/pyproject.toml:33](../../../02_repositorios/DiabeticsresearchJEV/pyproject.toml) |
| dependency | redis>=5.0.0 | [DiabeticsresearchJEV/pyproject.toml:34](../../../02_repositorios/DiabeticsresearchJEV/pyproject.toml) |
| dependency | neo4j>=5.20.0 | [DiabeticsresearchJEV/pyproject.toml:35](../../../02_repositorios/DiabeticsresearchJEV/pyproject.toml) |
| dependency | boto3>=1.34.0 | [DiabeticsresearchJEV/pyproject.toml:36](../../../02_repositorios/DiabeticsresearchJEV/pyproject.toml) |
| dependency | pypdf>=4.2.0 | [DiabeticsresearchJEV/pyproject.toml:37](../../../02_repositorios/DiabeticsresearchJEV/pyproject.toml) |
| dependency | fonttools>=4.40.0 | [DiabeticsresearchJEV/pyproject.toml:38](../../../02_repositorios/DiabeticsresearchJEV/pyproject.toml) |
| dependency | beautifulsoup4>=4.12.0 | [DiabeticsresearchJEV/pyproject.toml:39](../../../02_repositorios/DiabeticsresearchJEV/pyproject.toml) |
| dependency | lxml>=5.2.0 | [DiabeticsresearchJEV/pyproject.toml:40](../../../02_repositorios/DiabeticsresearchJEV/pyproject.toml) |
| extra:rag | sentence-transformers>=3.0.0 | [DiabeticsresearchJEV/pyproject.toml:45](../../../02_repositorios/DiabeticsresearchJEV/pyproject.toml) |
| extra:rag | rank-bm25>=0.2.2 | [DiabeticsresearchJEV/pyproject.toml:46](../../../02_repositorios/DiabeticsresearchJEV/pyproject.toml) |
| extra:rag | lingua-language-detector>=2.0.0 | [DiabeticsresearchJEV/pyproject.toml:47](../../../02_repositorios/DiabeticsresearchJEV/pyproject.toml) |
| extra:rag | gliner>=0.2.10 | [DiabeticsresearchJEV/pyproject.toml:48](../../../02_repositorios/DiabeticsresearchJEV/pyproject.toml) |
| extra:train | torch>=2.7.0 | [DiabeticsresearchJEV/pyproject.toml:51](../../../02_repositorios/DiabeticsresearchJEV/pyproject.toml) |
| extra:train | transformers>=4.51.0 | [DiabeticsresearchJEV/pyproject.toml:52](../../../02_repositorios/DiabeticsresearchJEV/pyproject.toml) |
| extra:train | peft>=0.15.0 | [DiabeticsresearchJEV/pyproject.toml:53](../../../02_repositorios/DiabeticsresearchJEV/pyproject.toml) |
| extra:train | trl>=0.19.0 | [DiabeticsresearchJEV/pyproject.toml:54](../../../02_repositorios/DiabeticsresearchJEV/pyproject.toml) |
| extra:train | accelerate>=1.0.0 | [DiabeticsresearchJEV/pyproject.toml:55](../../../02_repositorios/DiabeticsresearchJEV/pyproject.toml) |
| extra:train | bitsandbytes>=0.50.0 | [DiabeticsresearchJEV/pyproject.toml:56](../../../02_repositorios/DiabeticsresearchJEV/pyproject.toml) |
| extra:train | datasets>=3.0.0 | [DiabeticsresearchJEV/pyproject.toml:57](../../../02_repositorios/DiabeticsresearchJEV/pyproject.toml) |
| extra:train | mlflow-skinny>=2.14.0 | [DiabeticsresearchJEV/pyproject.toml:58](../../../02_repositorios/DiabeticsresearchJEV/pyproject.toml) |
| extra:pdf-plus | pymupdf>=1.24.0 | [DiabeticsresearchJEV/pyproject.toml:62](../../../02_repositorios/DiabeticsresearchJEV/pyproject.toml) |
| extra:viz | matplotlib>=3.8.0 | [DiabeticsresearchJEV/pyproject.toml:65](../../../02_repositorios/DiabeticsresearchJEV/pyproject.toml) |
| extra:unsloth | unsloth | [DiabeticsresearchJEV/pyproject.toml:67](../../../02_repositorios/DiabeticsresearchJEV/pyproject.toml) |
| extra:agent | langgraph>=0.2.0,<0.3.0 | [DiabeticsresearchJEV/pyproject.toml:71](../../../02_repositorios/DiabeticsresearchJEV/pyproject.toml) |
| extra:agent | neo4j-graphrag>=0.6.1,<1.0.0 | [DiabeticsresearchJEV/pyproject.toml:72](../../../02_repositorios/DiabeticsresearchJEV/pyproject.toml) |
| extra:agent | langchain-core>=0.3.0,<0.4.0 | [DiabeticsresearchJEV/pyproject.toml:73](../../../02_repositorios/DiabeticsresearchJEV/pyproject.toml) |
| extra:agent | langgraph-checkpoint-neo4j>=0.0.1,<0.1.0 | [DiabeticsresearchJEV/pyproject.toml:74](../../../02_repositorios/DiabeticsresearchJEV/pyproject.toml) |
| extra:dev | pytest>=8.2.0 | [DiabeticsresearchJEV/pyproject.toml:77](../../../02_repositorios/DiabeticsresearchJEV/pyproject.toml) |
| extra:dev | pytest-asyncio>=0.23.0 | [DiabeticsresearchJEV/pyproject.toml:78](../../../02_repositorios/DiabeticsresearchJEV/pyproject.toml) |
| extra:dev | ruff>=0.4.0 | [DiabeticsresearchJEV/pyproject.toml:79](../../../02_repositorios/DiabeticsresearchJEV/pyproject.toml) |
| extra:dev | mypy>=1.10.0 | [DiabeticsresearchJEV/pyproject.toml:80](../../../02_repositorios/DiabeticsresearchJEV/pyproject.toml) |
| extra:dev | mongomock>=4.1.0 | [DiabeticsresearchJEV/pyproject.toml:81](../../../02_repositorios/DiabeticsresearchJEV/pyproject.toml) |
| extra:dev | respx>=0.21.0 | [DiabeticsresearchJEV/pyproject.toml:82](../../../02_repositorios/DiabeticsresearchJEV/pyproject.toml) |

## Qualidade e limites

Workflows: 2; arquivos candidatos a testes: 13. Não executados.

- Amostra semântica seletiva; hash e busca textual não equivalem a auditoria integral.
- Nenhum runtime, treino, publicação ou sincronização remota executado.
- Fontes modificadas/não rastreadas fazem parte deste snapshot local.
