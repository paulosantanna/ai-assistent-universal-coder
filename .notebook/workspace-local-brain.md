# workspace-local-brain (RAG local + Jev)

Entry point: este documento. Integra com `07_mapeamentos/repositorios-skills/`, `chromatic-mega-brain`, `typesafe-ai`, `jev-call-expert` e (opcional) MCP RAG offline em `aeos/mcp-servers/rag-node-mcp.mjs` (ver `rag-node-mcp.md`).

Updated: 2026-11-06

## Objetivo

Definir um **cérebro de conhecimento local** para o Universal-coder: indexação recursiva de repositórios já mapeados e futuros, **RAG com pesos/embeddings locais** (vetores + metadados no disco), telemetria de **todas** as ferramentas que alteram código (`.cursor`, `.codex`, `.opencode`, `.claude`, etc.) via eventos versionados, e **roteamento/checagens** assistidas por **TypeSafe Jev** (`typesafe-ai` + `jev-call-expert`) — julgamentos tipados + código determinístico para política e execução.

## Caminhos no Windows (máquina do Paulo)

| Papel | Caminho sugerido |
| --- | --- |
| Credencial / runtime Jev (API key) | `E:\JEV` — consumir **apenas em runtime**; nunca commitar conteúdo do diretório |
| Armazenamento do cérebro (vetores, manifestos, logs de ingestão) | `E:\Github\workspace-brain` — fora do git do workspace ou com `.gitignore` agressivo para `store/` |

Em ambientes Linux/CI, espelhar com variáveis (`WORKSPACE_BRAIN_ROOT`, `JEV_CONFIG_DIR`) em vez de letras de unidade.

## Repositórios de referência (RAG / LLM local — curadoria)

Uso: inspiração de pipeline e operação; validar licença e política antes de fork.

| Repo | URL | Por quê |
| --- | --- | --- |
| haiku.rag | https://github.com/ggozad/haiku.rag | RAG “agentic”, híbrido, LanceDB embutido, Ollama por defeito, MCP para integração com fluxos tipo Claude/Codex |
| RagPack | https://github.com/iamAdityafr/ragpack | API/UI leve, Go, LanceDB embutido, BYO embeddings (Ollama) |
| RAG-Local (índice de exemplos) | https://github.com/codenamejason/RAG-Local | Coleção de exemplos Python/TS com Ollama + LanceDB |
| ollama-rag (minimal) | https://github.com/fabiothiroki/ollama-rag | Base mínima Ollama + LanceDB + Python para protótipos |

Stack de referência comum: **Ollama** (LLM + embeddings GGUF local), **LanceDB** ou **pgvector** para vetores, chunking + hash de conteúdo para reprodutibilidade.

## Arquitetura (camadas)

1. **Fontes de verdade**
   - clones sob `02_repositorios` (ou raiz acordada), mais o mapa estático `07_mapeamentos/repositorios-skills/`.
   - Continuidade já governada: `HANDOFF.md`, `MEMORY.md`, `PROGRESS.md`, `LEARNING.md` (`chromatic-mega-brain`).

2. **Ingestão recursiva**
   - Filtros por extensão e `.gitignore`; exclusão de segredos e artefactos (`node_modules`, `dist`, chaves).
   - Chunking com IDs estáveis: `sha256(repo_id + path + byte_range)`; `repo_id` = URL remota + ref git.

3. **Armazenamento (`workspace-brain`)**
   - `store/vectors/` — LanceDB (ou equivalente) **só dados**.
   - `store/manifests/` — JSON/YAML por run de ingestão: versão de modelo de embedding, dimensão, commit SHA, contagens.
   - `events/` — NDJSON de alterações por ferramenta (path, ação, timestamp, hash do diff resumido); **sem** chaves ou PII.

4. **Jev + TypeSafe** (`typesafe-ai`, `jev-call-expert`)
   - Jev responde **Choice / Noul / Score** para: relevância de chunk, necessidade de reindex, conflito de política, prioridade de skill.
   - Código fixo aplica thresholds, validação e chamadas a ingestão/RAG; a API key em `E:\JEV` entra só no cliente SDK em runtime.

5. **Recuperação e “reaprendizado”**
   - **Não** é fine-tuning dos pesos do LLM no sentido de treino contínuo; é **atualização incremental do índice** + opcionalmente *soft prompts* ou resumos curados promovidos ao quartet (MEMORY/LEARNING) com evidência.
   - Reprocessar apenas manifests obsoletos (mudança de modelo ou de ref git).

6. **Hooks para “todas as IAs”**
   - Ponto único: script ou wrapper que cada ferramenta invoca no fim da sessão (ou file watcher com debounce) escrevendo em `events/` e opcionalmente enfileirando ingestão incremental.
   - Determinismo: ordenar por `(timestamp, tool_id, content_hash)`; deduplicar por hash.

## Integração com skills do workspace

- **typesafe-ai** + **jev-call-expert**: contratos de julgamento e política de execução.
- **rag-expert**, **python-rag-audit**: revisão de pipeline e lacunas de produção.
- **chromatic-mega-brain** + **learning-opportunities**: promoção de factos verificados para `.notebook/MEMORY.md` e lições para `LEARNING.md`.
- **enterprise-repo-intelligence** / mapa existente: `07_mapeamentos/repositorios-skills/README.md` como entrada de “o que já foi mapeado”.

## Riscos e limitações

- **Determinismo**: embeddings e amostragem do LLM podem variar entre versões de modelo; fixar modelo + seed onde a API permitir e versionar no manifesto.
- **Segredos**: nunca indexar ficheiros de credenciais; listas de bloqueio no ingestor.
- **Custo de tokens**: RAG reduz contexto enviado ao modelo; ganhos reais dependem de política de top-k e resumos curados no quartet.

## Próximas ações executáveis (quando for missão de implementação)

1. Inicializar `E:\Github\workspace-brain` com `store/`, `manifests/`, `events/` e `.gitignore`.
2. Escolher um motor (p.ex. alinhar a haiku.rag ou pipeline mínimo Ollama+LanceDB).
3. Ligar cliente Jev com key apenas de `E:\JEV` para julgamentos de rota/consolidada.
4. Amarrar ingestão ao output de `07_mapeamentos/repositorios-skills` e a novos clones.
