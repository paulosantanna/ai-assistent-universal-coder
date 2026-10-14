# laya — mapa estático de skills

Updated: 2026-10-13

Entry point: ../README.md

Tipo: Git próprio. Arquivos no inventário delimitado: 682; entradas excluídas: 3.

[Voltar ao índice](../README.md) · [Matriz completa](../matriz.csv)

## Dez dimensões

| Dimensão | Estado | Observação | Evidência |
| --- | --- | --- | --- |
| Tecnologias e versões | declarado | Declarações extraídas dos manifests, incluindo faixas e extras. Não são versões instaladas nem prova de compatibilidade. Lockfiles permanecem nas fontes para análise posterior. | [02_repositorios/laya/engine/requirements.txt:11](../../../02_repositorios/laya/engine/requirements.txt); [02_repositorios/laya/engine/requirements.txt:12](../../../02_repositorios/laya/engine/requirements.txt); [02_repositorios/laya/engine/requirements.txt:13](../../../02_repositorios/laya/engine/requirements.txt); demais fontes em mapa.json/declarações abaixo |
| Arquitetura | documentado | Três processos documentados: Tauri/Svelte, engine Python/FastAPI e n8n como gateway externo. | [02_repositorios/laya/docs/architecture.md:47](../../../02_repositorios/laya/docs/architecture.md) |
| Propósito | declarado | Central local de notificações e cartões de ações com pesquisa/classificação por LLM. | [02_repositorios/laya/README.md:8](../../../02_repositorios/laya/README.md) |
| Fluxo | documentado | Ferramentas enviam eventos por n8n; engine prepara Action Cards, UI pede decisão e n8n executa ações aprovadas. | [02_repositorios/laya/README.md:45](../../../02_repositorios/laya/README.md) |
| Dados | observado | SQLite assíncrono com transações; FTS5/BM25 complementa recuperação vetorial Chroma. | [02_repositorios/laya/engine/laya/db/fts.py:4](../../../02_repositorios/laya/engine/laya/db/fts.py) |
| Configuração/deploy | observado | Tauri Rust/npm é fixado em 2.12.0; release desktop depende do pareamento dos manifests. | [02_repositorios/laya/ui/src-tauri/Cargo.toml:28](../../../02_repositorios/laya/ui/src-tauri/Cargo.toml) |
| Operação/observabilidade | observado | Gerenciamento SQLite registra conexão e rollback; serviços externos não sondados. | [02_repositorios/laya/engine/laya/db/sqlite.py:79](../../../02_repositorios/laya/engine/laya/db/sqlite.py) |
| Interfaces/dependências | observado | Engine tem rotas HTTP e módulo MCP http_server; providers/CLI externos têm autorização própria. | [02_repositorios/laya/engine/laya/main.py:37](../../../02_repositorios/laya/engine/laya/main.py) |
| Vulnerabilidades | não verificado | Nenhuma consulta atual a advisories/scanner foi executada; não equivale a ausência de CVEs. | Sem verificação nesta missão |
| Obsolescência | não verificado | Datas de suporte/EOL não consultadas. Versões declaradas não comprovam suporte atual. | Sem verificação nesta missão |

## Declarações dos manifests

Faixas e extras são preservados; versões instaladas/resolvidas não foram verificadas.

| Declaração | Valor | Fonte |
| --- | --- | --- |
| declaration | fastapi>=0.131.0,<1 | [02_repositorios/laya/engine/requirements.txt:11](../../../02_repositorios/laya/engine/requirements.txt) |
| declaration | uvicorn>=0.41.0 | [02_repositorios/laya/engine/requirements.txt:12](../../../02_repositorios/laya/engine/requirements.txt) |
| declaration | uvloop>=0.22.1; sys_platform != "win32" | [02_repositorios/laya/engine/requirements.txt:13](../../../02_repositorios/laya/engine/requirements.txt) |
| declaration | starlette>=0.52.1,<1 | [02_repositorios/laya/engine/requirements.txt:14](../../../02_repositorios/laya/engine/requirements.txt) |
| declaration | aiosqlite>=0.22.1 | [02_repositorios/laya/engine/requirements.txt:17](../../../02_repositorios/laya/engine/requirements.txt) |
| declaration | httpx>=0.28.1 | [02_repositorios/laya/engine/requirements.txt:20](../../../02_repositorios/laya/engine/requirements.txt) |
| declaration | aiohttp>=3.13.5 | [02_repositorios/laya/engine/requirements.txt:21](../../../02_repositorios/laya/engine/requirements.txt) |
| declaration | aiosmtplib>=5.1.0 | [02_repositorios/laya/engine/requirements.txt:24](../../../02_repositorios/laya/engine/requirements.txt) |
| declaration | litellm>=1.81.14,<2 | [02_repositorios/laya/engine/requirements.txt:27](../../../02_repositorios/laya/engine/requirements.txt) |
| declaration | openai>=2.21.0,<3 | [02_repositorios/laya/engine/requirements.txt:28](../../../02_repositorios/laya/engine/requirements.txt) |
| declaration | tiktoken>=0.12.0 | [02_repositorios/laya/engine/requirements.txt:29](../../../02_repositorios/laya/engine/requirements.txt) |
| declaration | mcp>=1.0.0,<2 | [02_repositorios/laya/engine/requirements.txt:30](../../../02_repositorios/laya/engine/requirements.txt) |
| declaration | chromadb>=1.5.4,<2 | [02_repositorios/laya/engine/requirements.txt:35](../../../02_repositorios/laya/engine/requirements.txt) |
| declaration | onnxruntime>=1.18.0,<1.24 ; python_full_version < '3.11' or (sys_platform == 'darwin' and python_full_version < '3.14') | [02_repositorios/laya/engine/requirements.txt:40](../../../02_repositorios/laya/engine/requirements.txt) |
| declaration | onnxruntime>=1.18.0,<2 ; python_full_version >= '3.11' and (sys_platform != 'darwin' or python_full_version >= '3.14') | [02_repositorios/laya/engine/requirements.txt:41](../../../02_repositorios/laya/engine/requirements.txt) |
| declaration | structlog>=25.5.0 | [02_repositorios/laya/engine/requirements.txt:44](../../../02_repositorios/laya/engine/requirements.txt) |
| declaration | python-dotenv>=1.2.1 | [02_repositorios/laya/engine/requirements.txt:47](../../../02_repositorios/laya/engine/requirements.txt) |
| declaration | keyring>=25.7.0 | [02_repositorios/laya/engine/requirements.txt:48](../../../02_repositorios/laya/engine/requirements.txt) |
| declaration | bcrypt>=5.0.0 | [02_repositorios/laya/engine/requirements.txt:49](../../../02_repositorios/laya/engine/requirements.txt) |
| declaration | PyYAML>=6.0.3 | [02_repositorios/laya/engine/requirements.txt:50](../../../02_repositorios/laya/engine/requirements.txt) |
| declaration | pydantic>=2.12.5,<3 | [02_repositorios/laya/engine/requirements.txt:53](../../../02_repositorios/laya/engine/requirements.txt) |
| declaration | jsonschema>=4.26.0 | [02_repositorios/laya/engine/requirements.txt:54](../../../02_repositorios/laya/engine/requirements.txt) |
| declaration | tzdata>=2025.1 | [02_repositorios/laya/engine/requirements.txt:60](../../../02_repositorios/laya/engine/requirements.txt) |
| declaration | tqdm>=4.67.3 | [02_repositorios/laya/engine/requirements.txt:63](../../../02_repositorios/laya/engine/requirements.txt) |
| declaration | tenacity>=9.1.4 | [02_repositorios/laya/engine/requirements.txt:64](../../../02_repositorios/laya/engine/requirements.txt) |
| declaration | rich>=14.3.3 | [02_repositorios/laya/engine/requirements.txt:65](../../../02_repositorios/laya/engine/requirements.txt) |
| declaration | psutil>=6.0.0 | [02_repositorios/laya/engine/requirements.txt:69](../../../02_repositorios/laya/engine/requirements.txt) |
| declaration | setuptools>=80.0.0 | [02_repositorios/laya/engine/requirements.txt:74](../../../02_repositorios/laya/engine/requirements.txt) |
| name | ui | [02_repositorios/laya/ui/package.json:2](../../../02_repositorios/laya/ui/package.json) |
| version | 0.0.1 | [02_repositorios/laya/ui/package.json:4](../../../02_repositorios/laya/ui/package.json) |
| @tauri-apps/api | 2.12.0 | [02_repositorios/laya/ui/package.json:26](../../../02_repositorios/laya/ui/package.json) |
| @tauri-apps/plugin-os | 2.4.0 | [02_repositorios/laya/ui/package.json:37](../../../02_repositorios/laya/ui/package.json) |
| @tauri-apps/plugin-process | 2.4.0 | [02_repositorios/laya/ui/package.json:37](../../../02_repositorios/laya/ui/package.json) |
| @tauri-apps/plugin-shell | 2.4.0 | [02_repositorios/laya/ui/package.json:37](../../../02_repositorios/laya/ui/package.json) |
| @tauri-apps/plugin-updater | 2.13.0 | [02_repositorios/laya/ui/package.json:40](../../../02_repositorios/laya/ui/package.json) |
| dompurify | ^3.4.2 | [02_repositorios/laya/ui/package.json:41](../../../02_repositorios/laya/ui/package.json) |
| marked | ^17.0.4 | [02_repositorios/laya/ui/package.json:42](../../../02_repositorios/laya/ui/package.json) |
| @skeletonlabs/skeleton | ^4.12.0 | [02_repositorios/laya/ui/package.json:18](../../../02_repositorios/laya/ui/package.json) |
| @skeletonlabs/skeleton-svelte | ^4.12.0 | [02_repositorios/laya/ui/package.json:18](../../../02_repositorios/laya/ui/package.json) |
| @sveltejs/adapter-auto | ^7.0.0 | [02_repositorios/laya/ui/package.json:20](../../../02_repositorios/laya/ui/package.json) |
| @sveltejs/adapter-static | ^3.0.10 | [02_repositorios/laya/ui/package.json:21](../../../02_repositorios/laya/ui/package.json) |
| @sveltejs/kit | ^2.61.1 | [02_repositorios/laya/ui/package.json:22](../../../02_repositorios/laya/ui/package.json) |
| @sveltejs/vite-plugin-svelte | ^6.2.4 | [02_repositorios/laya/ui/package.json:23](../../../02_repositorios/laya/ui/package.json) |
| @tailwindcss/postcss | ^4.2.2 | [02_repositorios/laya/ui/package.json:24](../../../02_repositorios/laya/ui/package.json) |
| @tailwindcss/vite | ^4.2.0 | [02_repositorios/laya/ui/package.json:25](../../../02_repositorios/laya/ui/package.json) |
| @tauri-apps/cli | 2.12.0 | [02_repositorios/laya/ui/package.json:26](../../../02_repositorios/laya/ui/package.json) |
| @types/dompurify | ^3.0.5 | [02_repositorios/laya/ui/package.json:27](../../../02_repositorios/laya/ui/package.json) |
| svelte | ^5.55.7 | [02_repositorios/laya/ui/package.json:28](../../../02_repositorios/laya/ui/package.json) |
| svelte-check | ^4.3.6 | [02_repositorios/laya/ui/package.json:29](../../../02_repositorios/laya/ui/package.json) |
| tailwindcss | ^4.3.0 | [02_repositorios/laya/ui/package.json:30](../../../02_repositorios/laya/ui/package.json) |
| typescript | ^5.9.3 | [02_repositorios/laya/ui/package.json:31](../../../02_repositorios/laya/ui/package.json) |
| vite | ^7.3.2 | [02_repositorios/laya/ui/package.json:32](../../../02_repositorios/laya/ui/package.json) |
| vitest | ^4.1.10 | [02_repositorios/laya/ui/package.json:33](../../../02_repositorios/laya/ui/package.json) |
| name | laya-app | [02_repositorios/laya/ui/src-tauri/Cargo.toml:2](../../../02_repositorios/laya/ui/src-tauri/Cargo.toml) |
| version | 1.0.4 | [02_repositorios/laya/ui/src-tauri/Cargo.toml:3](../../../02_repositorios/laya/ui/src-tauri/Cargo.toml) |
| edition | 2021 | [02_repositorios/laya/ui/src-tauri/Cargo.toml:8](../../../02_repositorios/laya/ui/src-tauri/Cargo.toml) |
| rust-version | 1.90 | [02_repositorios/laya/ui/src-tauri/Cargo.toml:9](../../../02_repositorios/laya/ui/src-tauri/Cargo.toml) |
| serde_json | 1.0 | [02_repositorios/laya/ui/src-tauri/Cargo.toml:3](../../../02_repositorios/laya/ui/src-tauri/Cargo.toml) |
| serde | 1.0 | [02_repositorios/laya/ui/src-tauri/Cargo.toml:3](../../../02_repositorios/laya/ui/src-tauri/Cargo.toml) |
| log | 0.4 | [02_repositorios/laya/ui/src-tauri/Cargo.toml:3](../../../02_repositorios/laya/ui/src-tauri/Cargo.toml) |
| tauri | =2.12.0 | [02_repositorios/laya/ui/src-tauri/Cargo.toml:28](../../../02_repositorios/laya/ui/src-tauri/Cargo.toml) |
| tauri-plugin-log | =2.10.0 | [02_repositorios/laya/ui/src-tauri/Cargo.toml:29](../../../02_repositorios/laya/ui/src-tauri/Cargo.toml) |
| tauri-plugin-shell | =2.4.0 | [02_repositorios/laya/ui/src-tauri/Cargo.toml:30](../../../02_repositorios/laya/ui/src-tauri/Cargo.toml) |
| tauri-plugin-dialog | =2.8.0 | [02_repositorios/laya/ui/src-tauri/Cargo.toml:31](../../../02_repositorios/laya/ui/src-tauri/Cargo.toml) |
| tauri-plugin-updater | =2.13.0 | [02_repositorios/laya/ui/src-tauri/Cargo.toml:32](../../../02_repositorios/laya/ui/src-tauri/Cargo.toml) |
| tauri-plugin-process | =2.4.0 | [02_repositorios/laya/ui/src-tauri/Cargo.toml:30](../../../02_repositorios/laya/ui/src-tauri/Cargo.toml) |
| reqwest | 0.12 | [02_repositorios/laya/ui/src-tauri/Cargo.toml:43](../../../02_repositorios/laya/ui/src-tauri/Cargo.toml) |
| tokio | 1 | [02_repositorios/laya/ui/src-tauri/Cargo.toml:3](../../../02_repositorios/laya/ui/src-tauri/Cargo.toml) |
| tauri-plugin-decorum | =1.1.1 | [02_repositorios/laya/ui/src-tauri/Cargo.toml:52](../../../02_repositorios/laya/ui/src-tauri/Cargo.toml) |
| tauri-plugin-os | =2.4.0 | [02_repositorios/laya/ui/src-tauri/Cargo.toml:30](../../../02_repositorios/laya/ui/src-tauri/Cargo.toml) |
| which | 6 | [02_repositorios/laya/ui/src-tauri/Cargo.toml:54](../../../02_repositorios/laya/ui/src-tauri/Cargo.toml) |
| flate2 | 1 | [02_repositorios/laya/ui/src-tauri/Cargo.toml:3](../../../02_repositorios/laya/ui/src-tauri/Cargo.toml) |
| tar | 0.4 | [02_repositorios/laya/ui/src-tauri/Cargo.toml:3](../../../02_repositorios/laya/ui/src-tauri/Cargo.toml) |
| zip | 2 | [02_repositorios/laya/ui/src-tauri/Cargo.toml:8](../../../02_repositorios/laya/ui/src-tauri/Cargo.toml) |
| sha2 | 0.10 | [02_repositorios/laya/ui/src-tauri/Cargo.toml:58](../../../02_repositorios/laya/ui/src-tauri/Cargo.toml) |
| getrandom | 0.3 | [02_repositorios/laya/ui/src-tauri/Cargo.toml:61](../../../02_repositorios/laya/ui/src-tauri/Cargo.toml) |

## Skills diretamente relacionadas

| Skill | Aplicação | Fonte |
| --- | --- | --- |
| [ai-architecture-expert](../../../00_skills/(architecture)/ai-architecture-expert/SKILL.md) | Necessidade observada: ai. Usar na tarefa correspondente, respeitando o contrato da skill. | [02_repositorios/laya/README.md:8](../../../02_repositorios/laya/README.md) |
| [ai-engineering-expert](../../../00_skills/(development)/ai-engineering-expert/SKILL.md) | Necessidade observada: ai. Usar na tarefa correspondente, respeitando o contrato da skill. | [02_repositorios/laya/README.md:8](../../../02_repositorios/laya/README.md) |
| [ai-evals-expert](../../../00_skills/(quality)/ai-evals-expert/SKILL.md) | Necessidade observada: ai. Usar na tarefa correspondente, respeitando o contrato da skill. | [02_repositorios/laya/README.md:8](../../../02_repositorios/laya/README.md) |
| [anti-hallucination-evaluator](../../../00_skills/(quality)/anti-hallucination-evaluator/SKILL.md) | Necessidade observada: ai. Usar na tarefa correspondente, respeitando o contrato da skill. | [02_repositorios/laya/README.md:8](../../../02_repositorios/laya/README.md) |
| [approval-governance-auditor](../../../00_skills/(security)/approval-governance-auditor/SKILL.md) | Especialização adequada ao contrato/estrutura observados; ativar apenas na tarefa correspondente. | [02_repositorios/laya/engine/laya/main.py:37](../../../02_repositorios/laya/engine/laya/main.py); [02_repositorios/laya/README.md:45](../../../02_repositorios/laya/README.md) |
| [automation-orchestrator](../../../00_skills/(tooling)/automation-orchestrator/SKILL.md) | Especialização adequada ao contrato/estrutura observados; ativar apenas na tarefa correspondente. | [02_repositorios/laya/engine/laya/main.py:37](../../../02_repositorios/laya/engine/laya/main.py); [02_repositorios/laya/README.md:45](../../../02_repositorios/laya/README.md) |
| [bm25-expert](../../../00_skills/(development)/bm25-expert/SKILL.md) | Necessidade observada: rag. Usar na tarefa correspondente, respeitando o contrato da skill. | [02_repositorios/laya/engine/laya/main.py:37](../../../02_repositorios/laya/engine/laya/main.py) |
| [ci-quality-gate-engineer](../../../00_skills/(development)/ci-quality-gate-engineer/SKILL.md) | Necessidade observada: ci. Usar na tarefa correspondente, respeitando o contrato da skill. | [02_repositorios/laya/.github/workflows/engine-deps.yml:1](../../../02_repositorios/laya/.github/workflows/engine-deps.yml); [02_repositorios/laya/.github/workflows/pages.yml:1](../../../02_repositorios/laya/.github/workflows/pages.yml); [02_repositorios/laya/.github/workflows/release.yml:1](../../../02_repositorios/laya/.github/workflows/release.yml) |
| [context-router](../../../00_skills/(learning)/context-router/SKILL.md) | Especialização adequada ao contrato/estrutura observados; ativar apenas na tarefa correspondente. | [02_repositorios/laya/engine/laya/main.py:37](../../../02_repositorios/laya/engine/laya/main.py); [02_repositorios/laya/README.md:45](../../../02_repositorios/laya/README.md) |
| [cost-token-optimizer](../../../00_skills/(learning)/cost-token-optimizer/SKILL.md) | Especialização adequada ao contrato/estrutura observados; ativar apenas na tarefa correspondente. | [02_repositorios/laya/engine/laya/main.py:37](../../../02_repositorios/laya/engine/laya/main.py); [02_repositorios/laya/README.md:45](../../../02_repositorios/laya/README.md) |
| [database-architecture-planner](../../../00_skills/(architecture)/database-architecture-planner/SKILL.md) | Necessidade observada: database. Usar na tarefa correspondente, respeitando o contrato da skill. | [02_repositorios/laya/engine/laya/db/fts.py:4](../../../02_repositorios/laya/engine/laya/db/fts.py) |
| [deployment-pipeline-expert](../../../00_skills/(cloud)/deployment-pipeline-expert/SKILL.md) | Necessidade observada: ci. Usar na tarefa correspondente, respeitando o contrato da skill. | [02_repositorios/laya/.github/workflows/engine-deps.yml:1](../../../02_repositorios/laya/.github/workflows/engine-deps.yml); [02_repositorios/laya/.github/workflows/pages.yml:1](../../../02_repositorios/laya/.github/workflows/pages.yml); [02_repositorios/laya/.github/workflows/release.yml:1](../../../02_repositorios/laya/.github/workflows/release.yml) |
| [devops-pipeline-engineering](../../../00_skills/(cloud)/devops-pipeline-engineering/SKILL.md) | Necessidade observada: ci. Usar na tarefa correspondente, respeitando o contrato da skill. | [02_repositorios/laya/.github/workflows/engine-deps.yml:1](../../../02_repositorios/laya/.github/workflows/engine-deps.yml); [02_repositorios/laya/.github/workflows/pages.yml:1](../../../02_repositorios/laya/.github/workflows/pages.yml); [02_repositorios/laya/.github/workflows/release.yml:1](../../../02_repositorios/laya/.github/workflows/release.yml) |
| [javascript-expert](../../../00_skills/(development)/javascript-expert/SKILL.md) | Necessidade observada: javascript. Usar na tarefa correspondente, respeitando o contrato da skill. | [02_repositorios/laya/docs/architecture.md:47](../../../02_repositorios/laya/docs/architecture.md) |
| [llm-model-selection-expert](../../../00_skills/(development)/llm-model-selection-expert/SKILL.md) | Necessidade observada: ai. Usar na tarefa correspondente, respeitando o contrato da skill. | [02_repositorios/laya/README.md:8](../../../02_repositorios/laya/README.md) |
| [mcp-discovery](../../../00_skills/(tooling)/mcp-discovery/SKILL.md) | Necessidade observada: mcp. Usar na tarefa correspondente, respeitando o contrato da skill. | [02_repositorios/laya/engine/laya/main.py:37](../../../02_repositorios/laya/engine/laya/main.py) |
| [mcp-health-check](../../../00_skills/(tooling)/mcp-health-check/SKILL.md) | Necessidade observada: mcp. Usar na tarefa correspondente, respeitando o contrato da skill. | [02_repositorios/laya/engine/laya/main.py:37](../../../02_repositorios/laya/engine/laya/main.py) |
| [mcp-poisoning-evaluator](../../../00_skills/(security)/mcp-poisoning-evaluator/SKILL.md) | Necessidade observada: mcp. Usar na tarefa correspondente, respeitando o contrato da skill. | [02_repositorios/laya/engine/laya/main.py:37](../../../02_repositorios/laya/engine/laya/main.py) |
| [mcp-risk-controller](../../../00_skills/(tooling)/mcp-risk-controller/SKILL.md) | Necessidade observada: mcp. Usar na tarefa correspondente, respeitando o contrato da skill. | [02_repositorios/laya/engine/laya/main.py:37](../../../02_repositorios/laya/engine/laya/main.py) |
| [python-bug-solver-skill](../../../00_skills/(development)/python-bug-solver-skill/SKILL.md) | Necessidade observada: python. Usar na tarefa correspondente, respeitando o contrato da skill. | [02_repositorios/laya/README.md:45](../../../02_repositorios/laya/README.md) |
| [python-expert](../../../00_skills/(development)/python-expert/SKILL.md) | Necessidade observada: python. Usar na tarefa correspondente, respeitando o contrato da skill. | [02_repositorios/laya/README.md:45](../../../02_repositorios/laya/README.md) |
| [python-rag-audit](../../../00_skills/(development)/python-rag-audit/SKILL.md) | Necessidade observada: rag. Usar na tarefa correspondente, respeitando o contrato da skill. | [02_repositorios/laya/engine/laya/main.py:37](../../../02_repositorios/laya/engine/laya/main.py) |
| [rag-expert](../../../00_skills/(development)/rag-expert/SKILL.md) | Necessidade observada: rag. Usar na tarefa correspondente, respeitando o contrato da skill. | [02_repositorios/laya/engine/laya/main.py:37](../../../02_repositorios/laya/engine/laya/main.py) |
| [rust-expert](../../../00_skills/(development)/rust-expert/SKILL.md) | Necessidade observada: rust. Usar na tarefa correspondente, respeitando o contrato da skill. | [02_repositorios/laya/docs/architecture.md:47](../../../02_repositorios/laya/docs/architecture.md) |
| [chrome-devtools](../../../00_skills/(tooling)/chrome-devtools/SKILL.md) | Necessidade observada: browser. Usar na tarefa correspondente, respeitando o contrato da skill. | [02_repositorios/laya/docs/architecture.md:47](../../../02_repositorios/laya/docs/architecture.md) |
| [gh-fix-ci](../../../00_skills/(tooling)/gh-fix-ci/SKILL.md) | Necessidade observada: ci. Usar na tarefa correspondente, respeitando o contrato da skill. | [02_repositorios/laya/.github/workflows/engine-deps.yml:1](../../../02_repositorios/laya/.github/workflows/engine-deps.yml); [02_repositorios/laya/.github/workflows/pages.yml:1](../../../02_repositorios/laya/.github/workflows/pages.yml); [02_repositorios/laya/.github/workflows/release.yml:1](../../../02_repositorios/laya/.github/workflows/release.yml) |
| [playwright-skill](../../../00_skills/(web-automation)/playwright-skill/SKILL.md) | Necessidade observada: browser. Usar na tarefa correspondente, respeitando o contrato da skill. | [02_repositorios/laya/docs/architecture.md:47](../../../02_repositorios/laya/docs/architecture.md) |

## Uso condicionado

- **atualizar-dependencias**: Somente em missão de atualização com baseline e compatibilidade.
- **compatibility-analyzer**: Ao verificar troca de linguagem/runtime/dependência.
- **dependency-updater**: Somente em atualização autorizada, preservando lockfiles.
- **github-operations**: GitHub é fonte anunciada; nenhum acesso externo foi testado.
- **jira-confluence-assistant**: Jira é fonte anunciada; conexão e autorização não verificadas.
- **local-secret-vault**: Só se a tarefa depender de credenciais autorizadas; não abrir para mapear.
- **observability-root-cause-integrator**: Requer incidente/sintomas e telemetria atual.
- **pr-reviewer**: Requer PR/diff concreto.
- **pr-reviewer-advanced**: Requer PR/diff concreto e evidências de revisão.
- **release-readiness-judge**: Requer release concreta e checks determinísticos.
- **gh-address-comments**: Requer comentários de PR e alvo concreto.
- **cve-advisory-sync**: Só ao solicitar consulta atual de advisories oficiais.
- **cve-remediation**: Requer CVE/GHSA concreto, versão afetada e correção autorizada.
- **eol-advisory-sync**: Requer consulta atual de suporte oficial para os produtos declarados.
- **revisar-seguranca-pr**: Requer diff de PR e escopo de segurança.
- **vuln-obsol-recon**: Inventário estático é ponto de partida; auditoria de CVE/EOL não foi executada.
- **runtime-troubleshooting**: Requer runtime/logs atuais; o mapa é estático.

## Testes/CI

112 arquivos candidatos por nome/caminho; não corresponde a quantidade de testes executados. 3 workflows encontrados. Suites não executadas.

- [02_repositorios/laya/.github/workflows/engine-deps.yml:1](../../../02_repositorios/laya/.github/workflows/engine-deps.yml)
- [02_repositorios/laya/.github/workflows/pages.yml:1](../../../02_repositorios/laya/.github/workflows/pages.yml)
- [02_repositorios/laya/.github/workflows/release.yml:1](../../../02_repositorios/laya/.github/workflows/release.yml)

## Lacunas

- Sem skill especialista Svelte/SvelteKit ou n8n no catálogo.
- React não é a stack de UI deste projeto.
- As identidades/agents do produto não criam outras identidades CodENavi no workspace.
