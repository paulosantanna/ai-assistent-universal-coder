# Padrão TLC do workspace

Updated: 2026-10-12
Entry point: [catálogo](INDEX.md), [inventário das imagens](images.manifest.json).

O contrato raiz é `AGENTS.md`. Existe uma identidade: `codenavi-agent`. Perfis históricos são lentes internas; Judge é um gate determinístico. Fonte importada não concede autoridade de execução.

## Estrutura e ordem

1. `00_skills/(categoria)/nome-da-skill/SKILL.md` é a entrada canônica.
2. Frontmatter: `name`, `description`, `license`, `metadata.author`, `metadata.version`, `metadata.owner_agent`. Preserve campos de invocação suportados.
3. Descrição: resultado concreto, gatilhos reais e exclusões. Nome em kebab-case igual à pasta.
4. Corpo: título, governança, procedimento específico, entradas/saídas, riscos, verificação e módulos com condição de leitura.
5. Conte todas as linhas físicas de SKILL.md: máximo 100, incluindo frontmatter. Preserve procedimentos extensos e exemplos em módulos locais; não compacte conteúdo para contornar o limite.
6. Use `references/` para instruções e fontes, `scripts/` para helpers reais, `templates/` e `assets/` para recursos de saída existentes. Não invente ferramentas ou arquivos para completar uma árvore visual.
7. Recursos TLC originais ficam em `references/tlc/`, com hashes e licença; procedimentos operativos adaptados ficam fora desse snapshot. Compatibilidade e descoberta apontam à entrada canônica.
8. Execute BRIEFING → RECON → PLAN → EXECUTE → VERIFY → DEBRIEF. Use o quarteto `.notebook/` com divulgação progressiva. Evidência/permissão obrigatória ausente bloqueia a operação dependente.

## Requisitos observados, em ordem das fotos

| Fotos | Contrato aplicado |
| --- | --- |
| 2112–2118 | Angular 8→20: uma major por etapa, compatibilidade oficial, paridade de UI/custom elements/HTTP/assíncrono. |
| 2119–2129 | the-fool: reversibilidade, steelman, premortem, pressupostos frágeis e vieses como lentes. |
| 2130–2138 | acta-aurea: áudio offline, transcrição/diarização, confirmar nomes, call.json e atas/HTML/SRT/VTT. |
| 2139–2148 | vox-aurum: transcrição Whisper offline simples, separada do fluxo de atas. |
| 2149–2180 | AGENTS: hierarquia workspace/categoria/projeto, português com identificadores técnicos em inglês, shell e segredos de runtime. |
| 2181–2190 | Decisão, paridade e revisão como lentes internas, sem criar agentes. |
| 2191–2213 | revisar-pr: revisão geral de PR distinta de revisão profunda de segurança; convenções do repositório efetivamente observado. |
| 2214–2222 | report-design: módulos próprios, tabelas completas, filtros/exportação/drilldown, tooltips, acessibilidade e reprodução offline. |
| 2223–2271 | skill-architect: discovery → architecture → craft → validate → deliver, exemplos/padrões/checklist locais. |
| 2272–2279 | Delegação histórica limitada a unidades de trabalho/lentes sob a identidade raiz. |
| 2280–2300 | Documentação distinta da memória operacional; Java 17 com diagnóstico e APIs da versão correta. |
| 2301–2316 | chromatic-mega-brain: MEMORY hierárquica e quarteto de continuidade, sem persona cognitiva adicional. |
| 2317–2333 | fleet-mapping: evidência micro/macro, cruzamento entre siglas e pacote portátil. |
| 2334–2377 | Sincronização CVE, remediação conhecida, sincronização EOL, segurança profunda de PR e recon de vulnerabilidade/obsolescência distintos. |
| 2378–2443 | Mapping portátil: intake, mapas, cobertura, relatórios completos, referências comprováveis e conhecimento sem duplicação. |
| 2444–2452 | Tokens de design transcritos em report-design; fontes/logos oficiais ausentes não são inventados. |
| 2453–2460 | Runtime troubleshooting: logs/métricas/traces/código, leitura em produção, sem restart/scale implícito. |
| 2461–2467 | Java 21 como escopo separado e correto para a versão. |
| 2468–2500 | CodENavi: ciclo de missão, princípios, notebook e cookie externo como referência de runtime, nunca conteúdo persistido. |

Todas as 770 IDs foram baixadas e receberam OCR; os 389 hashes únicos foram analisados em sequência por estrutura e tema. O manifesto guarda ordem, IDs e hashes, sem copiar fotos/OCR privados para o catálogo.

## Verificação reproduzível

`python "00_skills/(creation)/skill-factory/scripts/validate-workspace.py" --json-out 00_skills/validation.report.json`

Verifica instalação, frontmatter, limite físico, links operativos, descoberta nativa, 92 pacotes TLC e integridade dos 777 recursos originais. Não executa provedores externos. Recursos, autenticação e autorização de uma skill são verificados ao invocá-la.

## Atualização de 2026-10-13

As 77 imagens adicionais usam a mesma hierarquia canônica e acrescentam Impeccable, avaliação de skills existentes, seleção de aprendizado, camadas de frota e segurança Java/Spring/Camel/Angular. Veja [atualização](PHOTO-UPDATE.md), [estrutura](PHOTO-STRUCTURE.md) e [manifesto](images.2026-10-13.manifest.json). O limite local continua 100 linhas físicas mesmo quando uma captura sugere 500. Novos nomes sem corpo são pastas reservadas, não capacidades inventadas.
