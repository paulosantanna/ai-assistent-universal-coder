# workspace-brain: cérebro local determinístico do workspace

Updated: 2026-11-08. Entry point: `E:\Github\workspace-brain\README.md`. Spec: `E:\Github\workspace-brain\.specs\features\workspace-brain\spec.md`.

- Fact: CLI `python -m brain` em `E:\Github\workspace-brain` (stdlib only). SQLite + FTS5 com ranking BM25, aprendizados (error, success, learning, decision), checkpoints de repositórios com digest determinístico, descoberta no GitHub e julgamento com o JEV (`jev-latest`, Noul).
- Fact: run de exemplo dark-channel (2026-11-08): 5 capacidades, 55 repositórios únicos julgados (0 falhas), 5 de 5 capacidades com aprovados, 6 clones shallow em `02_repositorios`, 6 checkpoints com re-scan idêntico. Evidência: `.work/workspace-brain/evidence/` (coverage.json, judgments.json, checkpoints.json).
- Fact: chave do JEV lida em memória de `E:\cookier\JEV`. Nunca gravada. Teste C6 varre brain e evidência.
- Decision: pesos só são aprovados com avaliação medida ≥ 9,0 (`approve-weight`). Avaliação do JEV é triagem, não prova.
- Limit: "acessos" de repositório não são públicos no GitHub; usar estrelas, forks e data do último push.
- Limit: gate de 9,0 usa probabilidade do JEV não calibrada. Falso positivo registrado: biblioteca React Native aprovada com 9,9 em `thumbnail_generation`.
- Limit: licenças `NOASSERTION` em index-tts e edge-tts; verificar antes de reuso.
- Next: owner valida os rótulos prata da medição A2 (45 repositórios) e decide nova rodada com rótulos próprios; servidor MCP; recall com embeddings se BM25 faltar.
- Fact (2026-11-08): gate measured on 45 dark-channel repositories (amendment A2, silver labels, owner validation pending): precision 0.984 [0.917; 0.997], recall 0.768, 64 approvals at 0.9. Pre-registered verdict pass; thumbnail precision 0.833 (1 FP). The 35-repository v1 sample stays inconclusive by size. Evidence: `.work/workspace-brain/evidence/dark-channel-eval/eval-summary.md`.
- Continuity: `HANDOFF.md`, `PROGRESS.md`, `MEMORY.md`, `LEARNING.md` deste projeto citam este arquivo.
- Fact (2026-11-14): 31 entradas gravadas com `--project cloud-architecture` (7 erros reais, 3 decisões, 20 aprendizados, 1 sucesso); a 31ª é o erro de inventário de APIs, gravado depois da varredura de rotas. Harness: recall@3 = 1,0 em 20 consultas em linguagem natural; as consultas foram escritas pelo mesmo agente depois de gravar as lições, então a medida não é independente. Evidência: `.work/cloud-research/evidence/brain-harness.json`.
