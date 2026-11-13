# Playbook: operar o workspace-brain

Updated: 2026-11-06

## Objetivo

Manter o cérebro útil para todas as IAs/CLIs do PC com custo de tokens controlado.

## 1. Bootstrap (uma vez)

1. `npm install` no pacote `workspace-brain`.
2. `wb init` com `WORKSPACE_BRAIN_ROOT=E:\Github\workspace-brain`.
3. `wb install-agents` e registar MCP em Cursor, OpenCode, Claude, Codex.
4. Ajustar `manifests/model-contract.json` para o id **DeepSeek 4.1** exposto pelo OpenCode.

## 2. Ingestão recursiva

1. `wb ingest <repo>` após clones novos.
2. `wb map-seeds` para expandir com URLs curadas (Jev).
3. Confirmar `wb manifest` — `chunk_count` cresce.

## 3. Uso pelas IAs

1. Preferir `brain_search` antes de pedir contexto longo ao modelo.
2. `brain_ask` para respostas com citações ao corpus.
3. `brain_record_event` no fim de sessões que alterem código/skills.

## 4. Workspace-memory (refinada)

1. Após trabalho significativo: `wb dream` (ou `brain_dream`); com DeepSeek, `wb dream --llm`.
2. Só criar notas com **regra + evidência + armadilhas** — nunca “salvar tudo”.
3. Início de sessão nas IAs: carregar `brain_memory_bootstrap` (não colar wiki inteira).
4. Wiki inchada → resumir ou apagar páginas redundantes com o corpus.

Referência: [workspace-memory.md](../docs/workspace-memory.md) (técnicas do ecossistema Anthropic / vídeo `qSDDSUcegkQ`).

## 5. Reindexação

1. Comparar `events/events.ndjson` com paths alterados.
2. `brain_ingest_path` nos diretórios afetados.

## 5. Verificação

- `wb doctor` — credenciais presentes (boolean), layout OK.
- `npm test` — smoke local.

## Evidência

Logs em `logs/` (sem segredos). Manifestos versionados em `manifests/`.
