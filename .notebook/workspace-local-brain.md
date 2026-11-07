# workspace-local-brain (RAG nuvem + OpenCode + Jev)

Entry point: este documento. Integra com `07_mapeamentos/repositorios-skills/`, `chromatic-mega-brain`, `typesafe-ai`, `jev-call-expert`, `token-budget-governor` e o padrão de pastas de agentes (`.cursor`, `.codex`, `.opencode`, `.claude`, …) em `00_skills/(architecture)/domain-analysis/references/tlc/README.md` (referência a `.opencode/`).

Updated: 2026-11-06

## Objetivo

Definir um **cérebro de conhecimento** para o Universal-coder em que:

- **RAG (recuperação + geração)** é feito **na nuvem** pelo modelo **DeepSeek 4.1**, orquestrado via **OpenCode** — **sem Ollama nem stack de LLM local** para esse pipeline.
- **Armazenamento persistente** (corpus chunkado, caches de embedding se existirem, manifestos de ingestão, eventos de ferramentas, artefactos gerados) vive na pasta **`E:\Github\workspace-brain`** na tua máquina Windows.
- **Jev** (TypeSafe, credenciais em **`E:\JEV`**, só runtime) suporta **mapeamento ampliado da Internet**: priorização de fontes, deduplicação, política de confiança e rotas para **construir um MCP do cérebro**, além de **skills e playbook** escritos nesse caminho.

## Caminhos no Windows

| Papel | Caminho |
| --- | --- |
| Credencial / runtime Jev (API key) | `E:\JEV` — consumir **apenas em runtime**; nunca commitar conteúdo |
| Cérebro (dados, manifestos, MCP gerado, skills/playbooks gerados) | `E:\Github\workspace-brain` |

Espelho em Linux/CI: `WORKSPACE_BRAIN_ROOT`, `JEV_CONFIG_DIR` (sem valores secretos no git).

## Separação de responsabilidades

| Camada | Tecnologia | Função |
| --- | --- | --- |
| Recuperação + síntese (RAG) | **DeepSeek 4.1** via **OpenCode** | Embeddings (se o fluxo OpenCode expuser), rerank, resposta com citações ao corpus registado no manifesto. |
| Julgamentos / roteamento | **Jev** + `typesafe-ai`, `jev-call-expert` | Choice/Noul/Score: vale indexar esta URL? merge com repo conhecido? risco de baixa evidência? |
| Armazenamento | Disco em `E:\Github\workspace-brain` | Chunks, hashes, manifestos, `events.ndjson`, saída do gerador de MCP/skills/playbook — **não** substitui o repositório git do universal-coder salvo decisão explícita de copiar para `00_skills/` / `aeos/`. |
| Continuidade aprovada | `chromatic-mega-brain`, quartet `.notebook/` | Promover só factos verificados para `MEMORY.md` / `LEARNING.md`. |

**Nota:** “Pesos” no disco do cérebro referem-se a **artefactos derivados** (índices, caches, manifestos, eventos). O **modelo DeepSeek** permanece no fornecedor em nuvem; não há treino local dos pesos do foundation model neste desenho.

## Layout sugerido em `E:\Github\workspace-brain`

```
workspace-brain/
  corpus/              # texto chunkado + metadados (repo, path, commit, fonte web)
  manifests/           # versão de modelo (DeepSeek), dimensão, dataset_id, counts
  events/              # NDJSON: alterações por .cursor / .codex / .opencode / .claude / …
  mcp/                 # servidor MCP gerado (código + package.json se aplicável)
  skills/              # rascunhos ou espelho de skills geradas para copy-paste ao workspace
  playbooks/           # playbooks gerados (playbook-factory / convenções AEOS)
  logs/                # runs de ingestão (sem segredos)
```

`.gitignore` local no próprio `workspace-brain` se versionares só parte disto no GitHub.

## Papel do Jev no “mapear a Internet”

- Entrada: lista de seeds (repositórios já mapeados em `07_mapeamentos/repositorios-skills/`, pesquisas incrementais, feeds).
- Jev emite **julgametos tipados** (ex.: incluir URL vs. ignorar; binário de documentação vs. código; overlap com recurso existente).
- Código determinístico: fetch com limites, robots/respeito a ToS, dedupe por URL/hash, escrita em `corpus/` + `manifests/`.
- Saída alimenta o **MCP do cérebro** (tools: `search_brain`, `ingest_report`, `manifest`, etc.) e documentação para **skills** + **playbook** de operação.

## RAG com DeepSeek 4.1 + OpenCode (fluxo lógico)

1. **Ingestão** (local + web curada por Jev) → chunks em `corpus/` + manifesto.
2. **OpenCode** chama API **DeepSeek 4.1** para embedding e/ou etapa de geração conforme contrato do cliente OpenCode (alinhar à documentação OpenCode no teu ambiente).
3. **Consulta**: recuperar top-k do manifesto/corpus, montar contexto, **uma** chamada (ou pipeline fixo) ao modelo com política de citação.
4. **Registo**: append em `events/` quando Cursor/Codex/OpenCode/Claude alterarem ficheiros relevantes para reindexação incremental.

Para custo e escopo: `token-budget-governor` no planeamento de prompts longos.

## Integração com skills do workspace

- **typesafe-ai** + **jev-call-expert**: contratos de julgamento na colheita e no MCP.
- **playbook-factory-generator** / **skill-architect** (quando existir missão): moldar saídas em `workspace-brain/skills/` e `playbooks/`.
- **rag-expert**: revisão de lacunas (injeção, ACL, ciclo de vida de documentos) aplicada ao pipeline **em nuvem**.
- Mapa existente: `07_mapeamentos/repositorios-skills/README.md`.

## Riscos

- **Variação de modelo**: versionar no manifesto o identificador exato exposto pelo OpenSeek/DeepSeek.
- **Determinismo**: temperatura baixa e prompts com “cite apenas corpus”; ainda assim, amostragem pode variar — manifests e hashes de chunk são a âncora reprodutível.
- **Segredos**: nunca colocar `E:\JEV` nem API keys OpenCode no disco do cérebro em texto claro; usar variáveis de ambiente ou gestor secretos do SO.

## Próximas ações executáveis (missão de implementação)

1. Criar árvore em `E:\Github\workspace-brain` conforme layout acima.
2. Fixar contrato do cliente OpenCode + endpoint DeepSeek 4.1 e gravar em `manifests/model-contract.json` (sem segredos).
3. Implementar ingestão (repos + fila Jev para URLs) e export do **MCP** para `.opencode`/Cursor conforme registries AEOS (`aeos/registries/`).
4. Gerar **skill** + **playbook** mínimos que descrevem uso do MCP e do RAG nuvem-only.
5. Opcional: copiar artefactos governados para `00_skills/` após revisão CodENavi.
