# dark-videos — beta 3.0.0

Updated: 2026-10-27
Entry point: [índice](../README.md) · [mapa estruturado](../mapa.json)

Arquivos com hash: 618; fingerprint: `d771bad4dde9006608e472d25066b71f61d5a43f1570053514af76e10cdeb872`.
Git próprio: True; HEAD: `440a5b218826efee3e2e38b12e3f6c09f86b6a9b`; branch: `main`.
Estado local: há alterações/não rastreados; detalhes em inventory.json.

## Atualizações e reconciliação

Mapa amplia pgvector para retrieval de lições/chunks, grafo, NCM e LangGraph opcional. Checkout E: tem HEAD 440a5b2 e mudanças locais; atualizações de D: não são herdadas.

## Dimensões e evidências

### Propósito

**declarado** — Aplicação de vídeos curtos com mineração, composição, agenda e publicação social.

[dark-videos/README.md:1](../../../02_repositorios/dark-videos/README.md)

### Arquitetura

**documentado** — Backend Python/FastAPI, workers Celery e frontend Next.js/React; inicialização desktop própria.

[dark-videos/README.md:16](../../../02_repositorios/dark-videos/README.md)

### Fluxo

**observado** — Tarefa publishing.dispatch_due chama run_dispatch para processamento das publicações vencidas.

[dark-videos/backend/app/modules/publishing/tasks.py:17](../../../02_repositorios/dark-videos/backend/app/modules/publishing/tasks.py)

### Dados

**código presente** — Recupera Lesson e KnowledgeChunk por distância cosseno; pondera confiança e recência, com fallback local.

[dark-videos/backend/app/modules/learning/retrieval.py:69](../../../02_repositorios/dark-videos/backend/app/modules/learning/retrieval.py)

### Interfaces

**código presente** — Cliente Laya/Jev e retrieval remoto/local existem; nome não identifica integração com o app laya desta coleção.

[dark-videos/backend/app/modules/learning/retrieval.py:18](../../../02_repositorios/dark-videos/backend/app/modules/learning/retrieval.py)

### Configuração/deploy

**documentado** — Execução desktop Windows documenta PostgreSQL portátil e Redis; ambiente atual não sondado.

[dark-videos/README.md:57](../../../02_repositorios/dark-videos/README.md)

### Operação

**código presente** — LangGraph opcional recupera lições, diagnostica resultados e persiste; o fallback preserva funções existentes.

[dark-videos/backend/app/modules/learning/langgraph_flow.py:28](../../../02_repositorios/dark-videos/backend/app/modules/learning/langgraph_flow.py)

### Fine-tuning

**não demonstrado na amostra** — Sem conclusão positiva nesta revisão estática; não equivale a ausência universal.


### RAG

**código presente** — RAG de lições/chunks via embeddings e fallback; grafo reúne memória local e fatos remotos.

[dark-videos/backend/app/modules/learning/retrieval.py:128](../../../02_repositorios/dark-videos/backend/app/modules/learning/retrieval.py)

### Pós-treino

**não demonstrado na amostra** — Sem conclusão positiva nesta revisão estática; não equivale a ausência universal.


### Inferência

**código presente** — Seleção NCM por conceitos e shortlist aplica paradigma; não carrega o modelo NCM externo.

[dark-videos/backend/app/modules/learning/ncm.py:53](../../../02_repositorios/dark-videos/backend/app/modules/learning/ncm.py)

### Tecnologias/versões

**declarado** — Ver declarações extraídas e manifests; versões instaladas e compatibilidade não verificadas.

[dark-videos/backend/pyproject.toml:10](../../../02_repositorios/dark-videos/backend/pyproject.toml)
[dark-videos/backend/pyproject.toml:11](../../../02_repositorios/dark-videos/backend/pyproject.toml)
[dark-videos/backend/pyproject.toml:12](../../../02_repositorios/dark-videos/backend/pyproject.toml)
[dark-videos/backend/pyproject.toml:13](../../../02_repositorios/dark-videos/backend/pyproject.toml)
[dark-videos/backend/pyproject.toml:14](../../../02_repositorios/dark-videos/backend/pyproject.toml)
[dark-videos/backend/pyproject.toml:15](../../../02_repositorios/dark-videos/backend/pyproject.toml)
[dark-videos/backend/pyproject.toml:16](../../../02_repositorios/dark-videos/backend/pyproject.toml)
[dark-videos/backend/pyproject.toml:17](../../../02_repositorios/dark-videos/backend/pyproject.toml)

### Vulnerabilidades

**não verificado** — Sem consulta de CVE/EOL nesta missão.


### Obsolescência

**não verificado** — Sem consulta de CVE/EOL nesta missão.


## Declarações de versão

| Manifest / declaração | Valor | Evidência |
|---|---|---|
| name | dark-videos-backend | [dark-videos/backend/pyproject.toml:2](../../../02_repositorios/dark-videos/backend/pyproject.toml) |
| version | 0.1.0 | [dark-videos/backend/pyproject.toml:3](../../../02_repositorios/dark-videos/backend/pyproject.toml) |
| requires-python | >=3.12 | [dark-videos/backend/pyproject.toml:5](../../../02_repositorios/dark-videos/backend/pyproject.toml) |
| dependency | alembic>=1.20.0 | [dark-videos/backend/pyproject.toml:7](../../../02_repositorios/dark-videos/backend/pyproject.toml) |
| dependency | argon2-cffi>=25.1.0 | [dark-videos/backend/pyproject.toml:8](../../../02_repositorios/dark-videos/backend/pyproject.toml) |
| dependency | celery[redis]>=5.6.3 | [dark-videos/backend/pyproject.toml:9](../../../02_repositorios/dark-videos/backend/pyproject.toml) |
| dependency | cryptography>=50.0.2 | [dark-videos/backend/pyproject.toml:10](../../../02_repositorios/dark-videos/backend/pyproject.toml) |
| dependency | email-validator>=2.3.0 | [dark-videos/backend/pyproject.toml:11](../../../02_repositorios/dark-videos/backend/pyproject.toml) |
| dependency | fastapi>=0.142.2 | [dark-videos/backend/pyproject.toml:12](../../../02_repositorios/dark-videos/backend/pyproject.toml) |
| dependency | httpx>=0.28.1 | [dark-videos/backend/pyproject.toml:13](../../../02_repositorios/dark-videos/backend/pyproject.toml) |
| dependency | langdetect==1.0.9 | [dark-videos/backend/pyproject.toml:14](../../../02_repositorios/dark-videos/backend/pyproject.toml) |
| dependency | pgvector>=0.5.0 | [dark-videos/backend/pyproject.toml:15](../../../02_repositorios/dark-videos/backend/pyproject.toml) |
| dependency | playwright>=1.55 | [dark-videos/backend/pyproject.toml:16](../../../02_repositorios/dark-videos/backend/pyproject.toml) |
| dependency | pillow>=11 | [dark-videos/backend/pyproject.toml:17](../../../02_repositorios/dark-videos/backend/pyproject.toml) |
| dependency | psycopg[binary]>=3.3.6 | [dark-videos/backend/pyproject.toml:18](../../../02_repositorios/dark-videos/backend/pyproject.toml) |
| dependency | pydantic>=2.13.5 | [dark-videos/backend/pyproject.toml:19](../../../02_repositorios/dark-videos/backend/pyproject.toml) |
| dependency | pydantic-settings>=2.15.0 | [dark-videos/backend/pyproject.toml:20](../../../02_repositorios/dark-videos/backend/pyproject.toml) |
| dependency | redis>=6.4.0 | [dark-videos/backend/pyproject.toml:21](../../../02_repositorios/dark-videos/backend/pyproject.toml) |
| dependency | sqlalchemy>=2.1.3 | [dark-videos/backend/pyproject.toml:22](../../../02_repositorios/dark-videos/backend/pyproject.toml) |
| dependency | uvicorn[standard]>=0.54.0 | [dark-videos/backend/pyproject.toml:23](../../../02_repositorios/dark-videos/backend/pyproject.toml) |
| dependency | yt-dlp[curl-cffi]>=2026.8.19 | [dark-videos/backend/pyproject.toml:24](../../../02_repositorios/dark-videos/backend/pyproject.toml) |
| dependency | opentelemetry-api>=1.45.1 | [dark-videos/backend/pyproject.toml:25](../../../02_repositorios/dark-videos/backend/pyproject.toml) |
| dependency | opentelemetry-sdk>=1.45.1 | [dark-videos/backend/pyproject.toml:26](../../../02_repositorios/dark-videos/backend/pyproject.toml) |
| dependency | opentelemetry-exporter-otlp-proto-http>=1.45.1 | [dark-videos/backend/pyproject.toml:27](../../../02_repositorios/dark-videos/backend/pyproject.toml) |
| dependency | opentelemetry-instrumentation-fastapi>=0.66b1 | [dark-videos/backend/pyproject.toml:28](../../../02_repositorios/dark-videos/backend/pyproject.toml) |
| extra:learning | langchain-core>=0.3.0 | [dark-videos/backend/pyproject.toml:40](../../../02_repositorios/dark-videos/backend/pyproject.toml) |
| extra:learning | langgraph>=0.2.0 | [dark-videos/backend/pyproject.toml:41](../../../02_repositorios/dark-videos/backend/pyproject.toml) |
| name | dark-videos-frontend | [dark-videos/frontend/package.json:2](../../../02_repositorios/dark-videos/frontend/package.json) |
| version | 0.1.0 | [dark-videos/frontend/package.json:3](../../../02_repositorios/dark-videos/frontend/package.json) |
| engines:node | >=22 | [dark-videos/frontend/package.json:37](../../../02_repositorios/dark-videos/frontend/package.json) |
| dependencies:next | 16.4.3 | [dark-videos/frontend/package.json:15](../../../02_repositorios/dark-videos/frontend/package.json) |
| dependencies:react | 19.3.0 | [dark-videos/frontend/package.json:16](../../../02_repositorios/dark-videos/frontend/package.json) |
| dependencies:react-dom | 19.3.0 | [dark-videos/frontend/package.json:16](../../../02_repositorios/dark-videos/frontend/package.json) |
| devDependencies:@tailwindcss/turbopack | ^4 | [dark-videos/frontend/package.json:20](../../../02_repositorios/dark-videos/frontend/package.json) |
| devDependencies:@testing-library/dom | ^10.4.2 | [dark-videos/frontend/package.json:21](../../../02_repositorios/dark-videos/frontend/package.json) |
| devDependencies:@testing-library/jest-dom | ^7.0.1 | [dark-videos/frontend/package.json:22](../../../02_repositorios/dark-videos/frontend/package.json) |
| devDependencies:@testing-library/react | ^16.3.3 | [dark-videos/frontend/package.json:23](../../../02_repositorios/dark-videos/frontend/package.json) |
| devDependencies:@testing-library/user-event | ^14.6.7 | [dark-videos/frontend/package.json:24](../../../02_repositorios/dark-videos/frontend/package.json) |
| devDependencies:@types/node | ^22.20.5 | [dark-videos/frontend/package.json:25](../../../02_repositorios/dark-videos/frontend/package.json) |
| devDependencies:@types/react | ^19 | [dark-videos/frontend/package.json:26](../../../02_repositorios/dark-videos/frontend/package.json) |
| devDependencies:@types/react-dom | ^19 | [dark-videos/frontend/package.json:26](../../../02_repositorios/dark-videos/frontend/package.json) |
| devDependencies:@vitejs/plugin-react | ^6.1.2 | [dark-videos/frontend/package.json:28](../../../02_repositorios/dark-videos/frontend/package.json) |
| devDependencies:eslint | ^9 | [dark-videos/frontend/package.json:29](../../../02_repositorios/dark-videos/frontend/package.json) |
| devDependencies:eslint-config-next | 16.4.3 | [dark-videos/frontend/package.json:15](../../../02_repositorios/dark-videos/frontend/package.json) |
| devDependencies:jsdom | ^29.1.1 | [dark-videos/frontend/package.json:31](../../../02_repositorios/dark-videos/frontend/package.json) |
| devDependencies:tailwindcss | ^4 | [dark-videos/frontend/package.json:20](../../../02_repositorios/dark-videos/frontend/package.json) |
| devDependencies:typescript | ^5 | [dark-videos/frontend/package.json:33](../../../02_repositorios/dark-videos/frontend/package.json) |
| devDependencies:vitest | ^5.0.3 | [dark-videos/frontend/package.json:34](../../../02_repositorios/dark-videos/frontend/package.json) |

## Qualidade e limites

Workflows: 2; arquivos candidatos a testes: 231. Não executados.

- Amostra semântica seletiva; hash e busca textual não equivalem a auditoria integral.
- Nenhum runtime, treino, publicação ou sincronização remota executado.
- Fontes modificadas/não rastreadas fazem parte deste snapshot local.
