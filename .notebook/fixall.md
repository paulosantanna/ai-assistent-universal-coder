# fixall

Updated: 2026-11-25. Entry: `playbooks/fixall/PLAYBOOK.md`.

- `qa-expert-mcp` e `pentexpert-mcp` não existiam no workspace nem nos repositórios de `paulosantanna` vistos em 2026-11-25. Foram criados com páginas lidas nesse dia. Sem chave TypeSafe, nenhuma nota JEV foi gravada.
- O glossário ISTQB respondeu cascas vazias. Essas categorias ficaram `label_only`.
- O artigo arXiv 2401.05856 lista sete falhas de RAG, não oito. O oitavo não foi criado.
- PTES não abriu (502, TLS, README 404). As fases não foram preenchidas.
- `test-expert` é a skill ampla; `qa-expert` é alias. `tests-expert` continua o charter funcional e de ponta a ponta.
- `python quality/validate.py` estrutural: PASS. `--runtime` neste ambiente falha com `FileNotFoundError` porque não há binário `python` (o CI usa `python`).
