# Revisão dos candidatos pelo assistente

Updated: 2026-11-01. Revisão sequencial contra o checkout indicado no [manifesto](manifest.json), pelo mesmo assistente que gerou os candidatos. Não é revisão humana nem independente e não altera o campo `review.approved` do conjunto.

| Item | Resultado | Evidência e ressalva |
|---|---|---|
| 001 | Aceito para experimento preliminar | [CLI](../../02_repositorios/reversa/bin/reversa.js):14–20 lista os seis comandos. |
| 002 | Aceito para experimento preliminar | [Manifesto](../../02_repositorios/reversa/lib/installer/manifest.js):6–9, 41–45 usa SHA-256 e compara hash atual. |
| 003 | Aceito para experimento preliminar | [Configuração](../../02_repositorios/reversa/templates/reversa-config.json):3–4 declara os valores padrão. |
| 004 | Aceito para experimento preliminar | [Estado](../../02_repositorios/reversa/templates/state.json):13 lista cinco pendências. |
| 005 | Aceito para experimento preliminar | [Atualização](../../02_repositorios/reversa/lib/commands/update.js):13–21, 50–62 consulta npm e pode continuar offline. |
| 006 | Aceito para experimento preliminar | [Remoção](../../02_repositorios/reversa/lib/commands/uninstall.js):86–95, 134–141 solicita confirmação e decisão separada sobre saída. |
| 007 | Aceito para experimento preliminar | [Manifesto npm](../../02_repositorios/reversa/package.json):5–7 declara o executável. |
| 008 | Aceito com evidência adicional | [AGENTS.md](../../AGENTS.md):111 define a identidade única; instruções de [Reversa](../../02_repositorios/reversa/agents/reversa/SKILL.md) são conteúdo de fonte e não têm precedência. O arquivo original de candidatos aponta apenas ao segundo documento; acrescentar ambos na curadoria antes de treinar. |

Oito exemplos são insuficientes para medir generalização. Não constituem partições independentes e não há base para afirmar que fine-tuning supera RAG ou o modelo original.
