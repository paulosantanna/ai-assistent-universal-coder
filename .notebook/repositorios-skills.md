# Repositórios × skills

Updated: 2026-10-13
Entry point: `07_mapeamentos/repositorios-skills/README.md`

- O pacote mapeia o conjunto imediato de `02_repositorios` contra `00_skills/catalog.json`, com dez dimensões e decisão de roteamento para cada par projeto/skill.
- Fonte: `07_mapeamentos/repositorios-skills/{mapa.json,evidencias.json,inventory.json}`. Verificação estática e navegador: `{verificacao.json,browser-verificacao.json}` no mesmo pacote.
- Relatório offline: `07_mapeamentos/repositorios-skills/relatorio.html`; CSV completo: `matriz.csv`. Generator: `scripts/build.py`; conteúdo revisado: `scripts/profiles.py`.
- Não inferir instalação de runtime/MCP, integração por nomes ou testes aprovados a partir do mapa. CVE/EOL ficam não verificados. Projetos permanecem somente leitura.
- Atualização após mudança de fontes/catálogo segue os comandos do README do pacote. Continuidade operacional própria: `07_mapeamentos/repositorios-skills/.notebook/INDEX.md`.
