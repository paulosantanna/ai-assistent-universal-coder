# Skills e pastas das imagens de 2026-10-13

Updated: 2026-10-13
Entrada: pasta Drive `1xB9o93nQlLUGB7utNVXPVIIUYcV4K4Tn`, 77 imagens IMG_2700–IMG_2776.

Objetivo: atualizar as instruções e a estrutura do workspace conforme as referências observadas. O contrato raiz permanece byte-idêntico; há apenas `codenavi-agent`.

## Requisitos observados

| Fotos | Mudança |
| --- | --- |
| 2700–2704 | subagent-creator: entrega única, mínimo privilégio, evidência sem intenção e parecer explícito; adaptar perfis a lentes locais. |
| 2705–2715 | skill-architect 1.1.1: criar e avaliar/melhorar existentes, baseline e rubrica 0–100, frontmatter inline, revisão mínima. |
| 2716–2723 | impeccable 4.1.1: modos Persuade/Operate/Read/Experience, comandos, referências e scripts; adaptar quatro perfis a lentes. |
| 2724–2731 | learning-opportunities: AAR, recorrência/causa/ação/custo/não óbvio, regra de três, roteamento sem escrever o quarteto. |
| 2732–2738 | fleet-mapping: corporação/sigla/repo; templates, dependências externas, snapshot distinto de runtime, relatório offline. |
| 2739–2748 | security-best-practices: referências Java/Spring/Camel/Angular, três modos, convenções comprovadas e controle de falsos positivos. |
| 2749–2755 | acta-aurea: gravação de reunião exige pacote completo, call.json, nomes/off-topic confirmados, player por File API, qualidade da diarização. |
| 2756–2761 | vox-aurum 1.1.1: áudio simples, CPU/GPU explícita, modelos locais, texto literal e salvamento conforme pedido. |
| 2762–2767 | revisão de código/paridade: lentes somente leitura com formato e critérios distintos. |
| 2768–2772 | the-fool/the-jury: lentes de crítica e deliberação, racional/suposições, graus de evidência e mudança fundamentada. |
| 2773–2776 | 01_siglas/_comum e ferramentas; cofre externo por seção, CR/CRLF normalizados, somente metadados mascarados. |

## Decisões de implementação

- Preservar as 301 skills existentes e os 777 recursos TLC; adicionar Impeccable usando a tag oficial `skill-v4.1.1`, commit `5a149f3fdb1b5793f10567233b1dcab98fc305fd`.
- Entradas de até 100 linhas físicas; detalhes em módulos com condições de leitura. Não copiar paths locais Santander como caminhos existentes deste workspace.
- Instruções operativas não criam `.devin/agents`, perfis TOML ou outras identidades. Lentes sequenciais não oferecem independência cognitiva verdadeira; declarar esta limitação.
- Criar pastas numeradas observadas e modelos de notas; não inventar dados de siglas, ambientes, acessos, fontes/logos ou conteúdo de skills vistas só pelo nome.
- Preservar referências históricas/upstream. Atualizar somente os pontos operativos e a descoberta afetada.
- Os helpers de mídia usados nas fotos não foram fornecidos. Implementar contratos locais explícitos para transcrição/extrair/diarizar/build, com dependências opcionais verificadas ao uso; não instalar modelos, CUDA ou bibliotecas nesta missão.
- A skill local preexistente dark-videos-knowledge-base está fora do catálogo e excede o limite. Modularizar preservando o corpo integral, sem inventar validação do repositório que descreve.

## Gates de aceitação

- [x] 77 imagens contabilizadas por ID/hash e inspecionadas por OCR + leitura visual.
- [x] Requisitos acima ligados a arquivos reais; lacunas de material documentadas.
- [x] 301 pacotes originais e 777 recursos TLC preservados; Impeccable 4.1.1 licenciado e rastreável.
- [x] Nomes/pastas, frontmatter inline e descrição positiva/negativa verificáveis; nenhuma nova identidade.
- [x] Toda SKILL.md <=100 linhas; corpo da skill local extensa preservado como referência.
- [x] Links, catálogo, registro e descoberta nativa consistentes.
- [x] Scripts importados/adaptados passam checks relevantes; context.mjs funciona no diretório de um projeto de fixture.
- [x] Helpers de mídia validam erros e produzem artefatos determinísticos a partir de fixture sintética; não alegar validação real de Whisper/diarização.
- [x] AGENTS.md e recursos não relacionados preservados por hash.
- [x] Continuidade e resultado final refletem a verificação e as lacunas reais.

Evidência local ignorada: `.tools/photo-update/`. Manifesto público contém IDs/hashes e rastreabilidade, nunca fotos/OCR privados nem URLs temporárias de download.
