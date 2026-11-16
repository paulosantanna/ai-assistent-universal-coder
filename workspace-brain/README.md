# workspace-brain

Cérebro de conhecimento para o **Universal Coder**: corpus e manifestos em disco (`E:\Github\workspace-brain`), **RAG na nuvem** com **DeepSeek** (orquestrado pelo teu fluxo **OpenCode**), curadoria de URLs com **Jev/TypeSafe**, exposto a **Cursor, Codex, OpenCode, Claude** e CLI via **MCP stdio**.

## Instalação (PC Windows)

```powershell
cd E:\Github\workspace-brain
git clone https://github.com/paulosantanna/ai-assistent-universal-coder.git uc-tmp
xcopy /E /I uc-tmp\workspace-brain .
cd E:\Github\workspace-brain
npm install
copy .env.example .env
# Edite .env: chaves só localmente; credenciais Jev em E:\JEV
```

Ou apontar o código no monorepo e só definir dados:

```powershell
$env:WORKSPACE_BRAIN_ROOT = "E:\Github\workspace-brain"
cd E:\Github\ai-assistent-universal-coder\workspace-brain
npm install
npm run doctor
node bin/workspace-brain.mjs init
```

## Credenciais (runtime)

| Segredo | Onde |
| --- | --- |
| DeepSeek | `DEEPSEEK_API_KEY` ou `E:\JEV\deepseek.key` |
| TypeSafe / Jev | `TYPESAFE_API_KEY` ou `E:\JEV\typesafe.key` |
| Raiz do cérebro | `WORKSPACE_BRAIN_ROOT` (default `E:\Github\workspace-brain`) |

Nunca commitar chaves.

## CLI

```powershell
wb init
wb doctor
wb ingest E:\Github\ai-assistent-universal-coder
wb map-seeds
wb search "jev-call-expert"
wb ask "Como registo um evento de alteração?"
wb event --tool cursor --action edit --paths src\foo.ts --summary "ajuste"
wb install-agents
wb mcp
```

## MCP (todas as IAs)

Depois de `wb install-agents`, mescle os ficheiros em `config/mcp.*.json` na configuração do cliente:

- **Cursor**: `.cursor/mcp.json` → servidor `workspace-brain`
- **OpenCode**: conforme `config/mcp.opencode.json`
- **Claude Desktop / Codex**: snippets homólogos em `config/`

Comando do servidor:

```text
node <caminho-do-repo>/workspace-brain/src/mcp-server.mjs
```

Variável obrigatória: `WORKSPACE_BRAIN_ROOT=E:\Github\workspace-brain`

### Workspace-memory

Camadas `memory/` (transcripts, notes, wiki, bootstrap ≤200 linhas) e consolidação `wb dream`. Guia: [docs/workspace-memory.md](docs/workspace-memory.md).

### Tools MCP

| Tool | Função |
| --- | --- |
| `brain_memory_bootstrap` | Contexto curto por sessão |
| `brain_note_upsert` / `brain_dream` | Notas preditivas + consolidação |
| `brain_wiki_*` / `brain_memory_stats` | Wiki + métricas |
| `brain_health` | Status |
| `brain_search` | Busca BM25 no corpus |
| `brain_ask` | RAG DeepSeek |
| `brain_ingest_path` | Ingere diretório |
| `brain_ingest_url` | URL + Jev |
| `brain_map_seeds` | Seeds GitHub / URLs |
| `brain_record_event` | NDJSON de alterações |
| `brain_manifest` | Manifesto atual |

## Modelo DeepSeek 4.1 + OpenCode

Edite `manifests/model-contract.json` após `init` e alinhe `chat_model` ao id que o OpenCode usa para DeepSeek 4.1. O OpenCode pode sobrescrever hints via `OPENCODE_CONFIG_PATH`.

## Skills e playbook

Copiados para a raiz do cérebro em `skills/` e `playbooks/` (ver ficheiros neste pacote). Podem ser promovidos para `00_skills/` do universal-coder após revisão.

## Desenvolvimento

```bash
npm test
npm run mcp
```
