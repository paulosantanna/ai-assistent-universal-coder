# Workspace-memory (camadas + dream)

Baseado em práticas de **memória de agente** (transcripts → consolidação offline → contexto pequeno por sessão), alinhado ao relato público da Anthropic sobre memória preditiva e “dreaming”, popularizado em [este vídeo](https://www.youtube.com/watch?v=qSDDSUcegkQ).

## Camadas em `WORKSPACE_BRAIN_ROOT/memory/`

| Camada | Pasta | O que guardar |
| --- | --- | --- |
| L1 Transcripts | `transcripts/*.ndjson` | Rastro bruto (eventos, sonhos) — fonte da verdade para corrigir notas |
| L2 Notes | `notes/*.md` | **Previsões**: regra + **evidência** + **armadilhas** — não “dump” de estado |
| L3 Wiki | `wiki/*.md` | Mapa ligado; resume e aponta, **não** copia o corpus |
| L4 Bootstrap | `session/BOOTSTRAP.md` | O que entra em **toda** sessão (≤ **200** linhas) |

## Princípios (eficiência)

1. **Memória é aposta**: só anote o que sessões futuras provavelmente precisarão.
2. **Não memorizar o observável**: versões em lockfile, árvore de ficheiros, logs regeneráveis → use `brain_search`, não notes.
3. **Memória errada é pior que nenhuma**: toda nota precisa de `evidence[]` rastreável (evento, path, digest).
4. **Dream (`wb dream`)**: offline, reconcilia transcripts/eventos com notas; reconstrói bootstrap; opcional `--llm` (DeepSeek) para achar contradições.
5. **Wiki enxuta**: se `wiki` > ~2 MB, consolidar — evitar “mapa do império”.
6. **Instruir o propósito, não o micro-manual** (modelos fortes): a skill descreve *para que* serve a memória; o agente decide *como* escrever notas.

## Comandos

```bash
wb dream
wb dream --llm
wb bootstrap
wb memory-stats
wb note --title "..." --rule "..." --evidence "events/...,path:foo.ts"
```

## MCP

- `brain_memory_bootstrap` — injete no system/contexto inicial
- `brain_note_upsert` / `brain_note_read`
- `brain_wiki_upsert` / `brain_wiki_read`
- `brain_dream` / `brain_memory_stats`

## Integração com CodENavi

Promoção para `.notebook/MEMORY.md` continua via `chromatic-mega-brain` — o workspace-memory é **operacional e preditivo**; o quartet é **factos verificados**.
