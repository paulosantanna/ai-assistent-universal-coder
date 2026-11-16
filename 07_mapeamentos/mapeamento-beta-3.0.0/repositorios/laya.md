# laya — beta 3.0.0

Updated: 2026-10-27
Entry point: [índice](../README.md) · [mapa estruturado](../mapa.json)

Arquivos com hash: 697; fingerprint: `311954a82dbcf7a8a288572ac3daa82e763dc51020e9cda3bd1b087409901be5`.
Git próprio: True; HEAD: `052bc5533ac60d6f798dc80693fa8a382dfb40f4`; branch: `main`.
Estado local: limpo; detalhes em inventory.json.

## Atualizações e reconciliação

Snapshot atual 052bc55; retrieval RRF/FTS5 compartilhado e backends CLI constam do código/docs atuais. App laya não é o serviço Laya/Jev por semelhança nominal.

## Dimensões e evidências

### Propósito

**declarado** — Central local de notificações e cartões de ações com pesquisa/classificação por LLM.

[laya/README.md:8](../../../02_repositorios/laya/README.md)

### Arquitetura

**documentado** — Três processos documentados: Tauri/Svelte, engine Python/FastAPI e n8n como gateway externo.

[laya/docs/architecture.md:47](../../../02_repositorios/laya/docs/architecture.md)

### Fluxo

**documentado** — Ferramentas enviam eventos por n8n; engine prepara Action Cards, UI pede decisão e n8n executa ações aprovadas.

[laya/README.md:45](../../../02_repositorios/laya/README.md)

### Dados

**código presente** — Retrieval compartilhado contém extração de palavras-chave e Reciprocal Rank Fusion; FTS5 permanece na camada db.

[laya/engine/laya/retrieval.py:64](../../../02_repositorios/laya/engine/laya/retrieval.py)

### Interfaces

**observado** — Engine tem rotas HTTP e módulo MCP http_server; providers/CLI externos têm autorização própria.

[laya/engine/laya/main.py:38](../../../02_repositorios/laya/engine/laya/main.py)

### Configuração/deploy

**observado** — Tauri Rust/npm é fixado em 2.12.0; release desktop depende do pareamento dos manifests.

[laya/ui/src-tauri/Cargo.toml:28](../../../02_repositorios/laya/ui/src-tauri/Cargo.toml)

### Operação

**observado** — Gerenciamento SQLite registra conexão e rollback; serviços externos não sondados.

[laya/engine/laya/db/sqlite.py:79](../../../02_repositorios/laya/engine/laya/db/sqlite.py)

### Fine-tuning

**não demonstrado na amostra** — Sem conclusão positiva nesta revisão estática; não equivale a ausência universal.


### RAG

**código presente** — Contexto híbrido semântico/FTS5 e fusão RRF compartilhada.

[laya/engine/laya/retrieval.py:64](../../../02_repositorios/laya/engine/laya/retrieval.py)

### Pós-treino

**não demonstrado na amostra** — Sem conclusão positiva nesta revisão estática; não equivale a ausência universal.


### Inferência

**documentado** — Backends locais e cloud descritos; instruções do produto não criam agentes do workspace.

[laya/README.md:16](../../../02_repositorios/laya/README.md)

### Tecnologias/versões

**declarado** — Ver declarações extraídas e manifests; versões instaladas e compatibilidade não verificadas.

[laya/engine/requirements.txt:11](../../../02_repositorios/laya/engine/requirements.txt)
[laya/engine/requirements.txt:12](../../../02_repositorios/laya/engine/requirements.txt)
[laya/engine/requirements.txt:13](../../../02_repositorios/laya/engine/requirements.txt)
[laya/engine/requirements.txt:14](../../../02_repositorios/laya/engine/requirements.txt)
[laya/engine/requirements.txt:17](../../../02_repositorios/laya/engine/requirements.txt)
[laya/engine/requirements.txt:20](../../../02_repositorios/laya/engine/requirements.txt)
[laya/engine/requirements.txt:21](../../../02_repositorios/laya/engine/requirements.txt)
[laya/engine/requirements.txt:24](../../../02_repositorios/laya/engine/requirements.txt)

### Vulnerabilidades

**não verificado** — Sem consulta de CVE/EOL nesta missão.


### Obsolescência

**não verificado** — Sem consulta de CVE/EOL nesta missão.


## Declarações de versão

| Manifest / declaração | Valor | Evidência |
|---|---|---|
| dependency | fastapi>=0.131.0,<1 | [laya/engine/requirements.txt:11](../../../02_repositorios/laya/engine/requirements.txt) |
| dependency | uvicorn>=0.41.0 | [laya/engine/requirements.txt:12](../../../02_repositorios/laya/engine/requirements.txt) |
| dependency | uvloop>=0.22.1; sys_platform != "win32" | [laya/engine/requirements.txt:13](../../../02_repositorios/laya/engine/requirements.txt) |
| dependency | starlette>=0.52.1,<1 | [laya/engine/requirements.txt:14](../../../02_repositorios/laya/engine/requirements.txt) |
| dependency | aiosqlite>=0.22.1 | [laya/engine/requirements.txt:17](../../../02_repositorios/laya/engine/requirements.txt) |
| dependency | httpx>=0.28.1 | [laya/engine/requirements.txt:20](../../../02_repositorios/laya/engine/requirements.txt) |
| dependency | aiohttp>=3.13.5 | [laya/engine/requirements.txt:21](../../../02_repositorios/laya/engine/requirements.txt) |
| dependency | aiosmtplib>=5.1.0 | [laya/engine/requirements.txt:24](../../../02_repositorios/laya/engine/requirements.txt) |
| dependency | litellm>=1.81.14,<2 | [laya/engine/requirements.txt:27](../../../02_repositorios/laya/engine/requirements.txt) |
| dependency | openai>=2.21.0,<3 | [laya/engine/requirements.txt:28](../../../02_repositorios/laya/engine/requirements.txt) |
| dependency | tiktoken>=0.12.0 | [laya/engine/requirements.txt:29](../../../02_repositorios/laya/engine/requirements.txt) |
| dependency | mcp>=1.0.0,<2 | [laya/engine/requirements.txt:30](../../../02_repositorios/laya/engine/requirements.txt) |
| dependency | chromadb>=1.5.4,<2 | [laya/engine/requirements.txt:35](../../../02_repositorios/laya/engine/requirements.txt) |
| dependency | onnxruntime>=1.18.0,<1.24 ; python_full_version < '3.11' or (sys_platform == 'darwin' and python_full_version < '3.14') | [laya/engine/requirements.txt:40](../../../02_repositorios/laya/engine/requirements.txt) |
| dependency | onnxruntime>=1.18.0,<2 ; python_full_version >= '3.11' and (sys_platform != 'darwin' or python_full_version >= '3.14') | [laya/engine/requirements.txt:41](../../../02_repositorios/laya/engine/requirements.txt) |
| dependency | structlog>=25.5.0 | [laya/engine/requirements.txt:48](../../../02_repositorios/laya/engine/requirements.txt) |
| dependency | python-dotenv>=1.2.1 | [laya/engine/requirements.txt:51](../../../02_repositorios/laya/engine/requirements.txt) |
| dependency | keyring>=25.7.0 | [laya/engine/requirements.txt:52](../../../02_repositorios/laya/engine/requirements.txt) |
| dependency | bcrypt>=5.0.0 | [laya/engine/requirements.txt:53](../../../02_repositorios/laya/engine/requirements.txt) |
| dependency | PyYAML>=6.0.3 | [laya/engine/requirements.txt:54](../../../02_repositorios/laya/engine/requirements.txt) |
| dependency | pydantic>=2.12.5,<3 | [laya/engine/requirements.txt:57](../../../02_repositorios/laya/engine/requirements.txt) |
| dependency | jsonschema>=4.26.0 | [laya/engine/requirements.txt:58](../../../02_repositorios/laya/engine/requirements.txt) |
| dependency | tzdata>=2025.1 | [laya/engine/requirements.txt:64](../../../02_repositorios/laya/engine/requirements.txt) |
| dependency | tqdm>=4.67.3 | [laya/engine/requirements.txt:67](../../../02_repositorios/laya/engine/requirements.txt) |
| dependency | tenacity>=9.1.4 | [laya/engine/requirements.txt:68](../../../02_repositorios/laya/engine/requirements.txt) |
| dependency | rich>=14.3.3 | [laya/engine/requirements.txt:69](../../../02_repositorios/laya/engine/requirements.txt) |
| dependency | psutil>=6.0.0 | [laya/engine/requirements.txt:73](../../../02_repositorios/laya/engine/requirements.txt) |
| dependency | setuptools>=80.0.0 | [laya/engine/requirements.txt:78](../../../02_repositorios/laya/engine/requirements.txt) |
| name | ui | [laya/ui/package.json:2](../../../02_repositorios/laya/ui/package.json) |
| version | 0.0.1 | [laya/ui/package.json:4](../../../02_repositorios/laya/ui/package.json) |
| dependencies:@tauri-apps/api | 2.12.0 | [laya/ui/package.json:26](../../../02_repositorios/laya/ui/package.json) |
| dependencies:@tauri-apps/plugin-os | 2.4.0 | [laya/ui/package.json:37](../../../02_repositorios/laya/ui/package.json) |
| dependencies:@tauri-apps/plugin-process | 2.4.0 | [laya/ui/package.json:37](../../../02_repositorios/laya/ui/package.json) |
| dependencies:@tauri-apps/plugin-shell | 2.4.0 | [laya/ui/package.json:37](../../../02_repositorios/laya/ui/package.json) |
| dependencies:@tauri-apps/plugin-updater | 2.13.0 | [laya/ui/package.json:40](../../../02_repositorios/laya/ui/package.json) |
| dependencies:dompurify | ^3.4.17 | [laya/ui/package.json:41](../../../02_repositorios/laya/ui/package.json) |
| dependencies:marked | ^17.0.4 | [laya/ui/package.json:42](../../../02_repositorios/laya/ui/package.json) |
| devDependencies:@skeletonlabs/skeleton | ^4.12.0 | [laya/ui/package.json:18](../../../02_repositorios/laya/ui/package.json) |
| devDependencies:@skeletonlabs/skeleton-svelte | ^4.12.0 | [laya/ui/package.json:18](../../../02_repositorios/laya/ui/package.json) |
| devDependencies:@sveltejs/adapter-auto | ^7.0.0 | [laya/ui/package.json:20](../../../02_repositorios/laya/ui/package.json) |
| devDependencies:@sveltejs/adapter-static | ^3.0.10 | [laya/ui/package.json:21](../../../02_repositorios/laya/ui/package.json) |
| devDependencies:@sveltejs/kit | ^2.70.3 | [laya/ui/package.json:22](../../../02_repositorios/laya/ui/package.json) |
| devDependencies:@sveltejs/vite-plugin-svelte | ^6.2.4 | [laya/ui/package.json:23](../../../02_repositorios/laya/ui/package.json) |
| devDependencies:@tailwindcss/postcss | ^4.2.2 | [laya/ui/package.json:24](../../../02_repositorios/laya/ui/package.json) |
| devDependencies:@tailwindcss/vite | ^4.2.0 | [laya/ui/package.json:25](../../../02_repositorios/laya/ui/package.json) |
| devDependencies:@tauri-apps/cli | 2.12.0 | [laya/ui/package.json:26](../../../02_repositorios/laya/ui/package.json) |
| devDependencies:@types/dompurify | ^3.0.5 | [laya/ui/package.json:27](../../../02_repositorios/laya/ui/package.json) |
| devDependencies:svelte | ^5.55.7 | [laya/ui/package.json:28](../../../02_repositorios/laya/ui/package.json) |
| devDependencies:svelte-check | ^4.3.6 | [laya/ui/package.json:29](../../../02_repositorios/laya/ui/package.json) |
| devDependencies:tailwindcss | ^4.3.0 | [laya/ui/package.json:30](../../../02_repositorios/laya/ui/package.json) |
| devDependencies:typescript | ^5.9.3 | [laya/ui/package.json:31](../../../02_repositorios/laya/ui/package.json) |
| devDependencies:vite | ^7.3.7 | [laya/ui/package.json:32](../../../02_repositorios/laya/ui/package.json) |
| devDependencies:vitest | ^4.1.12 | [laya/ui/package.json:33](../../../02_repositorios/laya/ui/package.json) |
| name | laya-app | [laya/ui/src-tauri/Cargo.toml:2](../../../02_repositorios/laya/ui/src-tauri/Cargo.toml) |
| version | 1.0.4 | [laya/ui/src-tauri/Cargo.toml:3](../../../02_repositorios/laya/ui/src-tauri/Cargo.toml) |
| edition | 2021 | [laya/ui/src-tauri/Cargo.toml:8](../../../02_repositorios/laya/ui/src-tauri/Cargo.toml) |
| rust-version | 1.90 | [laya/ui/src-tauri/Cargo.toml:9](../../../02_repositorios/laya/ui/src-tauri/Cargo.toml) |

## Qualidade e limites

Workflows: 3; arquivos candidatos a testes: 128. Não executados.

- Amostra semântica seletiva; hash e busca textual não equivalem a auditoria integral.
- Nenhum runtime, treino, publicação ou sincronização remota executado.
- Fontes modificadas/não rastreadas fazem parte deste snapshot local.
