# Repositórios × skills do workspace

Updated: 2026-10-13
Owner: codenavi-agent

Objetivo: mapear todos os diretórios imediatos de `02_repositorios` e relacioná-los ao catálogo canônico `00_skills/catalog.json`, com evidências estáticas e limitações explícitas.

Escopo: inventário de fontes próprias, propósito declarado, dez dimensões de fleet-mapping, associação de skills por necessidade observada, relações comprovadas, lacunas e relatório local. Fontes somente leitura. Não executar aplicações, utilitários de remoção, instalações, auditorias remotas, treino, publicação ou alterações Git.

Saída: pacote autocontido `07_mapeamentos/repositorios-skills/`, com Markdown, JSON, HTML offline, mapas individuais, manifesto de evidências e ferramentas de regeneração/verificação. Skills são instruções da identidade única; nenhuma presença de MCP/runtime é inferida.

Premissas: sem siglas/perfis corporativos fornecidos, preservar os nomes reais. Mapeamento estático não comprova produção, segurança, suporte nem testes aprovados. Inventário limitado às árvores não excluídas, com exclusões explícitas; sem promessa de auditoria integral de cada linha.

Riscos: credenciais e dados locais excluídos; análise conservadora de snippets. Preservar missões e alterações preexistentes. Dependências e lockfiles distinguem faixa declarada de versão resolvida; sem aconselhar upgrades sem verificação oficial futura.

Aceitação:
- [x] Cobrir todos os diretórios de entrada, distinguindo Git próprio de pacote.
- [x] Fontes citadas por arquivo/linha/hash, sem valores de credenciais.
- [x] Onze mapas com dez dimensões e lacunas explícitas.
- [x] Decisão de aplicabilidade para cada combinação repositório/skill canônica; especialidades ausentes identificadas.
- [x] Relatório filtrável/exportável offline, navegação e verificação em navegador real.
- [x] Regeneração determinística, ponteiros/hashes válidos e preservação das fontes examinadas.
- [x] Continuidade atualizada sem substituir outras missões.

Evidência: `07_mapeamentos/repositorios-skills/{verificacao.json,browser-verificacao.json}`. Cobertura: 11 diretórios × 302 skills = 3.322 decisões; 529 ponteiros em 150 arquivos examinados. Projetos não executados. CVE/EOL não verificados.
