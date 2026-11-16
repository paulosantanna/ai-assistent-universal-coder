# skills-quality-eval: avaliação por skill (JEV + código)

Updated: 2026-11-16. Entry point: `.specs/skills-quality-eval/rubric.md` (A1, A2). Evidence: `.work/skills-quality-eval/`.

- Fact: estrutura em código (`.work/skills_quality_eval_v2.py:routing_links`), semântica em Nouls atômicos; limiar 0,7; veredito por dimensão: precisão >= 0,85 com >= 20 aprovações.
- Fact: roteamento `references/` 306/324; sem roteamento: `eval-report-v2.json` → `workflow_modules_deterministic.without_routing_ids`.
- Fact: holdout 1 (60): gov 1,00, provenance 0,88, fail_closed 1,00. Holdout 2 (60, só secrets após A2): precisão 1,00, 44 aprovações.
- Limit: rótulos prata (mesmo agente); `secrets_runtime_only` com 2 negativos verdadeiros; amostras 60/324.
- Replay: `python .work\skills_quality_eval_v2.py` e `python .work\skills_quality_eval_v3.py` (chave JEV só em memória, via `E:\Github\workspace-brain`).
