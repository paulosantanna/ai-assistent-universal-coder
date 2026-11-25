## Skill sem licença não entra como cópia integral — 2026-11-25

Updated: 2026-11-25. Entry point: `00_skills/(video)/remotion-best-practices/references/provenance.md`. Evidence: `gh api repos/remotion-dev/skills` devolveu `license: null` em 2026-11-25.

- Trigger: o usuário pede para internalizar uma skill pública cujo repositório não declara licença.
- Root cause: copiar os ensaios e assets seria redistribuir texto sem licença detectada, e o entrypoint ainda quebraria o teto de 100 linhas.
- Fix/prevention: reescrever as regras lidas, apontar a documentação oficial e registrar o que ficou de fora.
- Reuse scope: qualquer pacote de skill de terceiro sem licença SPDX ou arquivo LICENSE.

## Skill NVIDIA longa não entra no catálogo como arquivo único — 2026-11-25

Updated: 2026-11-25. Entry point: `00_skills/(creation)/skill-factory/scripts/validate-workspace.py`. Evidence: `validate-workspace.py` PASS depois da adaptação das 45 skills; o corpo original passava de 100 linhas e apontava para arquivos fora do pacote.

- Trigger: importar uma skill cujo `SKILL.md` passa de 100 linhas físicas ou liga para `../../scripts` e `AGENTS.md` de outro repositório.
- Root cause: o validador conta todas as linhas do entrypoint e segue cada link Markdown local até um arquivo versionado.
- Fix/prevention: entrypoint curto com gates; procedimento em `references/`; link quebrado vira texto; assinatura OMS e eval não copiados não contam como verificação.
- Reuse scope: qualquer pacote de skill de terceiros acima do teto de linhas ou com referências fora da pasta.

## Link relativo no grafo de skills precisa existir no checkout publicado — 2026-11-16

Updated: 2026-11-16. Entry point: `00_skills/(creation)/skill-factory/scripts/validate-workspace.py` (`markdown_links`). Evidence: anotação `skill-contract` em `rag-graph-laya-mcp/docs/mongodb-review/APPLIED.md` no run `43953048760`.

- Trigger: um Markdown alcançado a partir de uma skill aponta para um arquivo que só existe na máquina local.
- Root cause: o validador segue links locais e exige o destino no disco. `02_repositorios/` não entra no checkout do CI.
- Fix/prevention: caminho externo fica em código ou texto; link navegável só para arquivo versionado.
- Reuse scope: qualquer documentação puxada pelo grafo de `SKILL.md`.

## Gate de linguagem olha o binário do runner, não só a versão declarada no workflow — 2026-11-16

Updated: 2026-11-16. Entry point: `quality/prepush/backends/language.py`, `.github/workflows/prepush-gate.yml`. Evidence: simulação com runtime `24.22.2` → `language-outdated`; `26.13.1` → sem achados. Imagem `ubuntu-latest` (2026-11) documenta Node 24.22.2 e o ciclo endoflife atual é 26.

- Trigger: workflow que roda `prepush.py` sem instalar o Node do ciclo atual.
- Root cause: o backend acrescenta `node --version` do processo às declarações e exige o ciclo e o patch atuais. Declarar `node-version: 26` em outro workflow não altera o PATH deste job.
- Fix/prevention: o job que executa o gate instala o mesmo Node exigido pelo ciclo, com a action pinada por SHA.
- Reuse scope: qualquer checagem que mistura versão declarada e versão do processo no runner.

## Pacote novo ou pin direto desatualizado derruba o gate mesmo com o código já na master — 2026-11-16

Updated: 2026-11-16. Entry point: `quality/validate.py`, `quality/prepush/backends/libraries.py`. Evidence: Actions `43870090127` e `43870089967` no SHA `66737bb9`.

- Trigger: push para master com skills, um diretório `*-mcp` e um pin PyPI alterados sem o metadado que o gate compara.
- Root cause: `skills-baseline.json` e `baseline_hash` de quarentena são o aceite estrutural; diretório `*-mcp` fora de `capabilities.json` é drift; biblioteca direta com `==` falha assim que o registro publica uma versão maior.
- Fix/prevention: no mesmo commit do pacote, atualizar o baseline ou a revisão com o hash novo, registrar o diretório MCP com o tools/list real, e republicar o pin e os locks juntos.
- Reuse scope: qualquer gate que compara inventário ou pin com uma fonte externa ou com um hash de árvore.

## Inventário de superfícies começa por varredura do repositório, não por lista escolhida à mão — 2026-11-14

Updated: 2026-11-14. Entry point: `cloud-architecture/local-apis.json` e o teste de inventário em `cloud-architecture/tests/local-api-mapping.test.mjs`. Evidence: a lista manual de 6 APIs deixou de fora duas APIs FastAPI (`science-studio/integration/dark_api.py` e `rag-graph-laya-mcp/model_server.py`); a varredura de rotas, feita depois, achou as duas.

- Trigger: mapeamento de APIs locais com caminhos escolhidos à mão a partir de lembranças da sessão.
- Root cause: busca restrita a diretórios conhecidos; a exclusão de pastas grandes na varredura também reduziu o escopo sem registro.
- Fix/prevention: varredura de rotas do repositório inteiro antes do mapeamento, com exclusões declaradas; teste que confere que cada fonte descrita existe no disco e que o inventário é exatamente o conjunto esperado.
- Reuse scope: qualquer levantamento de componentes, APIs ou dependências antes de um desenho de arquitetura.

## Regra sem armadilha de regressão não impede o erro de voltar — cada regra precisa de um modelo que a dispare — 2026-11-14

Updated: 2026-11-14. Entry point: `cloud-architecture-mcp/tests/engine.test.mjs` (mapa TRAPS). Evidence: 27 regras, 27 armadilhas, 39 testes verdes.

- Trigger: lições de arquitetura cloud precisavam não se repetir em missões futuras.
- Root cause: regra escrita sem caso negativo pode deixar de disparar em silêncio quando o código muda.
- Fix/prevention: cada regra tem um modelo-armadilha que precisa disparar; cada erro aprendido aponta para uma claim suportada (fato correto) e para uma claim rejeitada (armadilha); a suíte falha se alguma regra sumir.
- Reuse scope: qualquer motor de revisão de configuração ou de política.

## Triagem de claims por modelo: trecho encurtado com reticências derruba o resultado — 2026-11-14

Updated: 2026-11-14. Entry point: `.work/cloud-research/evidence/jev-triage-run1.json` (rodada 1) e `jev-triage.json` (final). Evidence: uma claim suportada recebeu p=0,28 com trecho sem a frase condicional e p=0,89 com a frase verbatim.

- Trigger: 7 falhas na rodada 1 de triagem JEV.
- Root cause: trechos resumidos com reticências perderam sujeito, número ou condição; o juízo passou a valer para um fragmento.
- Fix/prevention: trecho verbatim com a frase inteira; pergunta do modelo inalterada; manter todas as rodadas como evidência; incluir controles negativos para medir separação.
- Reuse scope: qualquer checagem de afirmação contra fonte, com modelo juiz.

## Preço de nuvem sem credencial: usar snapshot público, com hash, e falhar quando a chave não casa — 2026-11-14

Updated: 2026-11-14. Entry point: `cloud-architecture-mcp/scripts/build_prices.py` (`pick_aws` falha com 0 ou >1 linha). Evidence: ferramenta de preço AWS exigiu credenciais; filtro com igualdade exata ignorou SKUs com sufixo `-Hosting` e `-Training`.

- Trigger: ferramenta dinâmica de preço sem credencial; SKUs faltando sem erro.
- Root cause: dependência de credencial em ferramenta de conveniência; filtro sem contagem exata.
- Fix/prevention: Price List pública em JSON com SHA-256; gerador que falha por chave ambígua ou ausente; motor que recusa SKU desconhecido (sem preço inventado).
- Reuse scope: comparação de custo entre provedores.

## Campo de região pertence ao provedor, não ao descritor — 2026-11-14

Updated: 2026-11-14. Entry point: `cloud-architecture-mcp/shared/engine.mjs` (`mapAzure`, campo `azure_region`). Evidence: o mapeador Azure lia a região AWS sa-east-1 e perdia a restrição de Brazil South.

- Trigger: mapeamento para dois provedores a partir de um descritor comum.
- Root cause: um único campo `region` serviu aos dois lados.
- Fix/prevention: um campo de região por provedor, com padrão explícito; teste que cobre os dois lados.

## Revisor automático bloqueia listagem recursiva de diretório de credenciais; Python inline quebra no PowerShell — 2026-11-14

Updated: 2026-11-14. Entry point: `.notebook/workspace-brain.md` (regras de chave JEV). Evidence: bloqueio do revisor em `Get-ChildItem -Recurse` sobre o diretório de chave; três quebras de parser com Python inline.

- Trigger: busca da chave de API do JEV e scripts de manipulação de JSON no PowerShell.
- Root cause: listagem ampla de diretório de credenciais; aspas e `$` do PowerShell dentro de Python.
- Fix/prevention: testar apenas o caminho conhecido e usar o cliente do `workspace-brain`, sem listar nem imprimir a chave; escrever scripts em arquivo e executar com `python arquivo.py`.
- Reuse scope: qualquer tarefa com credenciais locais ou JSON complexo no Windows.

## `node --test` sem argumento no Node 24 — 2026-11-14

Updated: 2026-11-14. Entry point: `cloud-architecture/` (rodar `node --test` sem argumento). Evidence: `node --test tests` falhou com MODULE_NOT_FOUND; `node --test` sem argumento encontrou os 13 testes.

- Trigger: rodar a suíte passando um diretório como argumento.
- Fix/prevention: descoberta padrão do Node sem argumento; scripts do `package.json` com `node --test`.

## CSS de autor com `display` vence o `[hidden]` do UA — overlay invisível bloqueia a UI inteira

Updated: 2026-11-11. Entry point: `otel-telemetry-devtools/dashboard/public/index.html` (`#drop-overlay[hidden]`).

- Trigger: walk C20 no browser — o primeiro `page.click` em qualquer aba travava; nenhum teste estático nem smoke HTTP pegava (HTML/JS "corretos").
- Root cause: `#drop-overlay { display: flex }` do autor sobrescreve o `[hidden] { display: none }` do UA stylesheet — overlay full-screen fica invisível mas intercepta TODOS os cliques. Regra de CSS de autor sempre vence o atributo `hidden` nativo.
- Fix/prevention: regra explícita `#drop-overlay[hidden] { display: none; }`; em UI servida, walk de browser com clique real em cada fluxo é o único gate que captura esse defeito (smoke de assets 200 não testa interação).
- Reuse scope: qualquer UI com overlay/modal/tooltip alternado por atributo `hidden` (HTML puro ou framework que o renderiza).
- Evidence: verification.md (Walks — bug 1); `mvnw verify` exit 0 pós-fix; screenshot `c20-live.png`.

## Mutante que não compila não é kill — valide a compilação do mutante antes de contar

Updated: 2026-11-11. Entry point: `10_projetos_estruturantes/otel-telemetry-java/.specs/features/otel-telemetry-java/verification.md` (M3).

- Trigger: mutação M3 planejada como injeção de retorno inacessível no sink; `mvnw test` não compilou e a suíte nem rodou.
- Root cause: um mutante com statement inacessível é **erro de compilação**, não teste — o "kill" só vale quando o mutante compila e um teste falha. Contar compile-error como kill infla o gate.
- Fix/prevention: projetar a mutação num comportamento observável (`SinkConfig.authRequired() → false`); compilar o mutante antes de ler o resultado; registrar tentativa inválida como INVÁLIDA e corrigir o alvo.
- Reuse scope: qualquer gate de mutação (spec-lean, PIT, maven).
- Evidence: verification.md — M3 1ª tentativa inválida; corrigida → morta por `missingTokenReturns403` + `loopbackDefaultAndOverrides`.

## Mutante que sobrevive é teste fraco — fortaleça o corpo do teste, não o comando de proof

Updated: 2026-11-11. Entry point: `otel-telemetry-devtools/src/test/java/com/aeos/telemetry/devtools/JsonlStoreTest` (`rotationHonorsCeilings`).

- Trigger: mutação M2 (rotação usa `maxFiles` em vez de `maxFiles-1`) sobreviveu com a suíte verde.
- Root cause: o teste exercitava o caminho mas com carga fraca — appends insuficientes para provocar a rotação em cascata; sobrevivência sinaliza teste fraco, não mutante inofensivo.
- Fix/prevention: fortalecer o CORPO do teste (mais appends, teto menor, assert da cascata até `traces.3.jsonl`) mantendo o comando de proof congelado; re-rodar com o mutante (morte), reverter e provar volta ao verde.
- Reuse scope: qualquer mutação sobrevivente antes de classificá-la como "equivalente".
- Evidence: verification.md — M2 SOBREVIVEU → teste fortalecido (25 appends, teto 512 B) → MORTA; core+devtools re-verdes após reversão.

## Fetch incremental com since=máximo + filtro >= re-ingere o registro de fronteira

Updated: 2026-11-11. Entry point: `otel-telemetry-devtools/dashboard/src/main.ts:213` + `otel-telemetry-devtools/src/main/java/com/aeos/telemetry/devtools/JsonlStore.java:119`.

- Trigger: dashboard live re-ingeria o registro mais novo a cada poll — com tráfego parado, a tabela crescia uma cópia por poll.
- Root cause: cliente manda `since = max(tempo visto)` e servidor filtra `tempo >= since`; o registro de fronteira satisfaz o filtro e volta sempre. Qualquer API incremental montada em par com `since = max` + filtro inclusivo tem o mesmo bug.
- Fix/prevention: dedup por chave estável no merge OU `since = max + 1` / filtro exclusivo no servidor; provar com duas polls idênticas sob tráfego parado (mesma contagem).
- Reuse scope: qualquer fetch incremental (logs, métricas, feeds) entre cliente e servidor próprios.
- Evidence: finding F1 do The-Judge (`C:\Users\paulo\AppData\Local\Temp\opencode\judge\findings.json`).

## Script de módulo não roda em file:// — distribuição local de SPA exige iife clássico

Updated: 2026-11-10. Entry point: `10_projetos_estruturantes/ai-engineer-rpg/vite.config.ts`.

- Trigger: o dono pediu abrir o jogo pelo `index.html` sem npm; a expectativa natural era que `base './'` + build padrão bastassem.
- Root cause: em página `file://` o Chromium/Firefox bloqueiam `<script type="module">` (CORS de módulos), e o Vite marca a entrada como módulo **mesmo com** `rollupOptions.output.format: 'iife'`. Isso cria **duas** armadilhas encadeadas: (1) o Vite move o script para o `<head>`, e módulo é sempre *deferred* — quando a tag vira clássica, ela executa antes de `<div id="root">` existir e o React morre com container nulo (página branca); (2) nesse formato o CSS deixa de ser arquivo e passa a ser injetado em runtime pelo JS (`createElement('style')` + `head.appendChild`).
- Fix/prevention: para app Vite distribuído como arquivo local: `output.format: 'iife'` + `inlineDynamicImports` + plugin pós-build (`generateBundle`, `enforce: 'post'`) que troca `type="module"` por `defer` e remove `crossorigin` do asset html — `transformIndexHtml` não serve porque roda antes da injeção dos assets de build. O `defer` é obrigatório: reproduz o comportamento deferred que módulos tinham. Provar antes: sem `import.meta`, sem `import()` dinâmico, sem `fetch`, caminhos relativos, CSS dentro do chunk.
- Reuse scope: qualquer app React/Vite entregue como arquivo local (jogos, aulas, certificados offline).
- Evidence: `dist/index.html` (tag clássica) + `dist/assets/index-*.js` contendo o stylesheet injetado; suíte 55/55 e build 252 módulos após a mudança.

## Metadados de PDF não ficam em ASCII cru — verifique recarregando o documento

Updated: 2026-11-10. Entry point: `node_modules/pdf-lib/cjs/api/PDFDocument.js:381-385`.

- Trigger: teste do certificado fazia varredura textual dos bytes (`latin.includes('AIE-2026-…')`); o header `%PDF` casava, mas o código do certificado nunca aparecia, parecendo documento corrompido.
- Root cause: em pdf-lib 1.17, `setKeywords`/`setSubject` gravam strings de Info via `PDFHexString.fromText` — os bytes ficam em UTF-16BE hexadecimal, então busca ASCII crua nunca casa, mesmo com o conteúdo válido no documento.
- Fix/prevention: para afirmações sobre metadados de PDF, recarregar o documento (`PDFDocument.load`) e ler pela API (`getKeywords()`, `getSubject()`) em vez de varrer bytes; shape estrutural (pageCount, header) fica na varredura.
- Reuse scope: qualquer geração/leitura de PDF (pdf-lib, pdf-js) com teste ou evidência dependente de conteúdo de metadados.
- Evidence: `10_projetos_estruturantes/ai-engineer-rpg/tests/certificate.test.ts` (verificação estrutural via `PDFDocument.load`, suíte 55/55); leitura direta do código-fonte do pdf-lib confirmando `PDFHexString.fromText`.

## Componente de gate medindo o artefato errado não é salvo por reengenharia do fluxo

Updated: 2026-11-10. Entry point: `science-studio/studio.py:445-449`.

- Trigger: GATE 5 exigindo `input_lra > 15` medido no preview de 90 min com narração contínua + ducking 8:1; a parcela de 1,5 pts bloqueou a entrega com 8,5/10 (threshold ≥ 9,5).
- Root cause: LRA é p95−p10 do short-term gated. Com voz presente a maior parte do tempo, p95 e p10 são fixados pela voz (−15,3/−20,1 medidos); exigir p10 ≤ −30 demanda ≥10% da massa de janelas < −30 e a massa "só-música" real (gaps ≥ 3 s) é ~4-7% — teto físico ≈ 5-6 LU. O componente mede o **preview** enquanto a intenção registrada ("Música audível") descreve a **trilha**.
- Fix/prevention: ao criar componente de gate com threshold numérico, validar ANTES a variante limitante: medir a métrica no objeto onde ela é fisicamente realizável (trilha pura: 18,2 ✓) e provar a distribuição alvo (bins de p10/p95) antes de congelar o valor; em produção, provar a impossibilidade pela distribuição e pela curva de calibração (db×LRA) em vez de girar parâmetros.
- Reuse scope: qualquer gate com métrica de percentil (LRA, DR, crest, p95) aplicada a artefato misto (voz+música).
- Evidence: `.notebook/PROGRESS.md` (2026-11-10): curva music-db −17→1,9 / −8→3,0 / −2→4,2; HANDOFF 2026-10-30 registra LRA 31,3 vs MEMORY LRA 1,3 no mesmo vídeo (conflito histórico irresolúvel — delivery de referência apagado), `science-studio/` untracked.



Updated: 2026-11-09. Entry point: `quality/prepush/prepush.py`.

- Trigger: o pedido era analisar os validadores de CI e bloquear push desatualizado, inclusive CVE e SAST.
- Root cause: o texto de `deploy-expert-unique` lista OSV e CodeQL, mas `AIHealthResearch/.github/workflows/ci.yml` não executa esses passos. A primeira varredura também leu `.venv` e `.state` como se fossem o produto e apontou JDK, site-packages e testes de terceiros.
- Fix/prevention: confirmar o passo no workflow antes de afirmar que o gate existe. Excluir ambiente, cache e runtime local antes de relatar achado. A segunda corrida, só com locks do projeto, manteve certifi, pypdf, axios, undici e follow-redirects.
- Reuse scope: qualquer portão de segurança ou comparação entre skill e CI. Evidence: `00_skills/(development)/deploy-expert-unique/SKILL.md`; `E:\Github\AIHealthResearch\.github\workflows\ci.yml`; `.aeos/prepush/report.json`.

## Compactação de descrição remove cláusula de segurança sem alarme

Updated: 2026-11-09. Entry point: `00_skills/do-not-invent.manifest.json`.

- Trigger: o owner apontou que a regra "DO NOT INVENT / NUNCA INVENTE" tinha sido perdida em skills. A varredura por padrão estreito (do/never/nunca + invent) pegou só 7 dos 12 casos da descrição.
- Root cause: a regra aparece em formas variadas ("No invented X", "Invent X" como item de lista, "sem inventar", "without inventing", "invent architecture without source evidence"). A reescrita para 150 caracteres cortou o qualificador "without source evidence" e removeu cláusulas inteiras. O validador não checava essas cláusulas, então não reprovou.
- Fix/prevention: varredura ampla (EN/PT, negação e qualificador) antes e depois de reescrever; registro com a cláusula literal por skill; validador que reprova cláusula ausente. Testar o vermelho antes de restaurar (11 erros esperados).
- Reuse scope: qualquer compactação de documentação com regra de segurança ou de não fabricação. Evidence: `.tools/skill-restructure/invent_broad.py` (saída antes/depois, ignorada pelo git) e check `DO NOT INVENT clause missing` em `validate-workspace.py`.

## Medir duplicação por frase, não por prefixo, antes de prometer ganho de tokens

Updated: 2026-11-09. Entry point: `00_skills/VERIFICATION.md` (seção 2026-11-09).

- Trigger: a primeira estimativa, por prefixo de 60 caracteres, apontou 212 corpos e ~75 mil caracteres duplicados.
- Root cause: prefixo casa com qualquer trecho que começa igual, não com o texto repetido. A medição por frase literal deu 225 corpos e ~38 mil caracteres, dos quais ~12,5 mil eram roteamento removível.
- Fix/prevention: medir por frase com fronteira de palavra e classificar cada uma (roteamento, coberta, conteúdo único) antes de relatar um número. Frases de conteúdo que só existem no corpo não são duplicação a remover.
- Reuse scope: qualquer deduplicação de documentação ou prompt. Evidence: saídas de `dup_measure.py` (antes e depois) registradas no VERIFICATION.

## Validar o baseline e respeitar proveniência por hash antes de reestruturar skills

Updated: 2026-11-09. Entry point: `00_skills/(creation)/skill-factory/scripts/validate-workspace.py`.

- Trigger: a primeira execução do validador, antes de qualquer edição, retornou FAIL com 18 erros.
- Root cause: BOM UTF-8 em 3 SKILL.md, lido sem `utf-8-sig` pelo `validate_skill.py`; um arquivo com dupla codificação UTF-8→cp1252; 13 digests do catálogo desatualizados por edições posteriores ao registro.
- Fix/prevention: remover o BOM; reverter só os segmentos de mojibake (maior prefixo que decodifica em UTF-8), sem tocar acentos legítimos como `NÃO`; recalcular digest com a própria função `digest()` do validador, que normaliza CRLF. Medir o baseline antes de editar.
- Reuse scope: qualquer conjunto de skills com catálogo e digest. Evidence: `00_skills/VERIFICATION.md` (2026-11-09) e `00_skills/validation.report.json`.
- Trigger: compactar o corpo de `(design)/impeccable` quebrou o check de proveniência.
- Root cause: `source.manifest.json` pina o hash do `SKILL.md` adaptado; qualquer edição quebra o pin.
- Fix/prevention: antes de editar um arquivo, procurar manifesto que o pina (`source.manifest.json`, `upstream.manifest.json`). Restaurar os bytes originais e excluir esses arquivos das transformações.
- Reuse scope: qualquer reestruturação de conteúdo importado. Evidence: erro `impeccable provenance` e restauração a partir do backup, validador PASS após a correção.

## Otimizar descrição de roteamento: medir a parte visível, não o arquivo

Updated: 2026-11-09. Entry point: `00_skills/VERIFICATION.md` (seção 2026-11-09).

- Trigger: encurtar descrições de 355 para 141 caracteres em média reduziu o texto dos ponteiros em 59,5%, mas o catálogo visível caiu só 6,0%.
- Root cause: o harness exibe ~150 caracteres de cada descrição; a parte além disso já não custava tokens no catálogo, mas escondia gatilhos e exclusões.
- Fix/prevention: limitar a descrição a 150 caracteres, com gatilho e exclusão no início, e medir o catálogo pela parte visível. Encurtar além de 150 quase não economiza no catálogo; o ganho real é a completude do roteamento.
- Reuse scope: qualquer catálogo de skills ou ferramentas com descrição truncada pelo harness. Evidence: `00_skills/VERIFICATION.md` (medidas antes/depois).

## Comandos Python inline no PowerShell falham com aspas aninhadas

Updated: 2026-11-09. Entry point: sessão Windows deste workspace.

- Trigger: três tentativas de `python -c "..."` com `\"` dentro da string foram recusadas pelo PowerShell.
- Root cause: o PowerShell não trata `\"` como escape; a string termina antes do código Python.
- Fix/prevention: gravar a lógica em um arquivo `.py` (em `.tools/` quando for auxiliar) e executá-lo; evitar `python -c` com aspas aninhadas.
- Reuse scope: qualquer automação Python executada por PowerShell neste workspace. Evidence: três recusas registradas na sessão de 2026-11-09.

## Ranking sem piso de pertinência transforma "sem casamento" em "casamento arbitrário"
Updated: 2026-11-08. Entry point: `science-studio/context_gate.py:select_scene_assets`.
- Trigger: frames visuais fora do contexto do roteiro em vídeos de canal dark do dark-videos.
- Root cause: `build_layers.py` ranqueava assets por sobreposição de tokens e, com score 0, escolhia silenciosamente o primeiro em ordem alfabética — cena de átomo podia receber frame de outro assunto.
- Fix/prevention: seleção pura levanta `OffContextError` quando o melhor score é 0; `build_layers.py` falha (exit 2) listando todas as cenas bloqueadas antes de codificar; o gate de aprovação (GATE 3) re-verifica com proveniência (ledger de prompts) ou nome em contexto; o fundo reusa o asset em contexto em vez do próximo com score 0.
- Reuse scope: qualquer pipeline que atribua itens por similaridade — exigir piso mínimo de pertinência e bloquear explicitamente o caso zero; fail closed não pode ser um ranking silencioso.
- Evidence: `test_context_gate.py` (`test_zero_match_levanta_erro_bloqueante` e afins); fumaça `gates-context-smoke` (GATE 3 FAIL ↔ proven); brain `59e22ee2`.

## Adam anula atenuação feita só no gradiente
Updated: 2026-11-03. Entry point: `D:/Git/DeepSeek-V4.1-Flash-1017-UNCENSORED-FP8/trainer/protect.py`.
- Trigger: Fisher uniforme em `B` quase não mudou o tamanho do passo sob AdamW.
- Root cause: o passo do Adam é a razão dos momentos; um fator positivo em todo o gradiente se cancela.
- Fix/prevention: aplicar o gate `1/(1+F)` no delta do parâmetro depois do `optimizer.step`, e manter o teto de `||ΔW||` contra a matriz congelada. Não escrever o treino de volta no shard FP8/FP4.
- Reuse: continuação com Adam em cima de checkpoint quantizado. Evidence: `trainer/tests/test_continual.py`.

## Bloquear baseline divergente antes de aplicar frontend concorrente
Updated: 2026-10-29. Entry point: .work/identifyer-wifi-view/install.py.
- Trigger: app.js recebeu atualização de sinais faciais durante a implementação do visorWi-Fi.
- Root cause: staging ainda refletia apenas a versão anterior com postura.
- Prevention: validar hashes de baseline antes de qualquer escrita/backup; o primeiro deploy recusou o conflito, depois staging foi reconstruído do instalado e apenas hooksWi-Fi reaplicados. ContratosWi-Fi/postura/face13 e browser7 passaram antes/depois.
- Reuse: atualizações concorrentes fora deGit que compartilhem bundle/HTML/CSS; preservar módulo/deps/modelos e não sobrescrever staging antigo. Evidence: .work/identifyer-wifi-view/{baseline,browser-installed,installation}.json e docs/WIFI_VIEW_REVIEW.md no projeto.

---

## Consultar provedores reais antes de declarar módulo sem dados
Updated: 2026-10-29. Entry point: E:/Github/iDentifyer/src/sensors.rs.
- Trigger: todas as modalidades apareciam indisponíveis no Windows.
- Root cause: temperatura Windows não tinha provedor; parser netsh dependia de sinal de enlace, mas o rádio existente estava ativo e desconectado.
- Fix/prevention: inventariar hardware e APIs separadamente; NVIDIA oferece temperatura real e WLAN nativa oferece estado de rádio mesmo sem enlace. Validar enums unknown/on/off sem transformar desconhecido em falso.
- Reuse: adapters de telemetria Windows; sensor ausente, driver sem suporte, permissão negada e leitura de estado são resultados distintos. Evidence: sensor-upgrade/sensors-installed e SENSORS_REVIEW.md do projeto.

---

## TFJS com muitos shards em HTTP/1 local
Updated: 2026-10-29. Entry point: E:/Github/iDentifyer/scripts/pack_model.py.
- Trigger: COCO-SSD/TFJS4.22 travava após seis respostas de shards4MB; timeout180s no browser, apesar de cada arquivo ser baixável isoladamente.
- Root cause: loadWeightsAsArrayBuffer espera todos os headers antes de consumir corpos; pool HTTP/1 pode bloquear downloads restantes.
- Fix/prevention: concatenar pesos na ordem original do grupo, reescrever somente paths, preservar hashes upstream e verificar inferência real. Depois o fluxo completo passou em cerca10s, sem alterar tensores.
- Reuse scope: modelos multipart TFJS servidos por HTTP/1 local; confirmar comportamento antes de aplicar. Evidence: projeto docs/VERIFICATION.md, web/models/coco-ssd/manifest.json e docs/evidence/browser.json.

---

## Validar o contrato global antes de renderizar capítulos longos

Updated: 2026-10-27. Entry point: science-studio/studio.py:validate.
- Trigger: produção de 110 minutos em onze capítulos; cada capítulo passava, mas o total excedia o antigo limite de 90 minutos.
- Root cause: validação isolada das partes não exercitou o contrato do projeto inteiro antes do trabalho caro.
- Prevention: validar duração/soma do master já na fase de roteiro; testar o novo limite e a rejeição de totais divergentes. JSON válido/contagem de palavras não verificam correção científica ou prosa utilizável.
- Scope: produção em lotes com gates globais. Evidence: .work/meu-filme/core-contract-verification.json, draft-chapters/REVIEW.md e full-media-verification.json.

---

## Filtros de inventário devem distinguir modelos-fonte de pesos

Updated: 2026-10-27. Entry point: `07_mapeamentos/mapeamento-beta-3.0.0/scripts/scan.py`.
- Trigger: remapeamento inclui arquitetura NCM e pontes Java/Swift/C++.
- Root cause: excluir a árvore inteira models omite código Python; restringir extensões à stack principal omite pontes de outros runtimes.
- Prevention: filtrar pesos/binários pelo tipo/tamanho e exigir que todo locador de fato pertença ao inventário hashado; a revisão semântica permanece seletiva.
- Scope: inventários multilíngues com pesos/dados e código misturados. Evidence: gate detectou ponte Java fora do inventário; filtros corrigidos, models/ incluído e 577 evidências validadas em `07_mapeamentos/mapeamento-beta-3.0.0/verificacao.json`.

---

## Validar portabilidade de helpers importados sem alterar a fonte retida

Updated: 2026-10-26. Entry point: `00_skills/(development)/spec-driven/scripts/mutate.py:kill_group`.
- Trigger: selftests de helpers TLC importados falham no Windows.
- Root cause: sinais Unix (`SIGHUP`) e encerramento de grupo por `os.killpg` não existem em Windows.
- Prevention: snapshots oficiais ficam intactos; cópias locais registram somente sinais presentes e encerram a árvore de provas com taskkill no Windows. Timeout e restauração byte a byte precisam de prova executada, além de parse/sintaxe.
- Scope: helpers de mutação e outros subprocessos multiplataforma. Evidência: `.work/tlc-spec-upgrade/EVIDENCE.md`, `verification.json` (timeout + selftests).

---

# LEARNING

Updated: 2026-10-24

Updated: 2026-11-13


## Validated learnings

### The wording of a judge question defines what the gate approves
- Trigger: the thumbnail question "generates thumbnails or images for video content" approved two visual generators at 0.92 and 0.96, and thumbnail_generation precision fell to 0.60 on 5 approvals.
- Root cause: the question measures any image for video, not the intent (a cover image for a video). A rubric written from intent disagrees with the question, and the gate inherits the question's breadth.
- Verified prevention: write the ground truth from the intent first, measure the production question against it, and report precision per capability. Under the literal reading the two false positives become true positives (precision 1.00), so the decision is about the question, not the judge's reading.
- Reuse scope: any LLM-judged gate whose question names a category broader than the decision.
- Evidence: `.work/workspace-brain/evidence/dark-channel-eval/eval-report.json` (false_positives), `eval-summary.md` (scenario B).
- Confidence: high for the measured effect; the fix (question amendment) is not yet tested. Updated: 2026-11-08

### A keyword that sits inside another word produces false evidence
- Trigger: the draft labeller marked "script" as present in Shaarav4795/ClippedAI (7 hits), but the hits came from "transcription".
- Root cause: substring matching ignores word boundaries; the rubric lists were frozen before this was seen.
- Verified prevention: no edit to the frozen list (its hash is in the report). The manual label was decided from the full sentence, and the limit is recorded in the rubric. A new rubric must use word boundaries.
- Reuse scope: any keyword-based draft labeller or retrieval filter.
- Evidence: `.specs/features/dark-channel-eval/rubric.md` (known limit); grep output in `eval-summary.md` sources.
- Confidence: high. Updated: 2026-11-08

### A pre-registered minimum sample is a verdict rule, not a note
- Trigger: the measurement had 35 repositories against a pre-registered minimum of 40. Precision was 0.962, which would have passed the pooled rule.
- Root cause: the minimum lived only in the plan; the verdict function did not check it, so the code would have reported "pass".
- Verified prevention: encode the minimum in `verdict()` and in the frozen evidence test (`test_c5`), then check the report against it. The verdict is now inconclusive, and the test passes.
- Reuse scope: any measurement with a pre-registered acceptance rule.
- Evidence: `brain/evaluate.py` (`verdict`), `tests/test_dark_channel_eval_evidence.py` (test_c5, test_c7), `eval-report.json` (`verdict`, `sample_repos`).
- Confidence: high. Updated: 2026-11-08

### A silver label can contradict the text it was drafted from
- Trigger: a thumbnail false positive (raunakpatil, p=0.96) was labelled 0 as "does not make thumbnails", but the judged text said "make a thumbnail (photo or new AI artwork)" and the full README has a thumbnail designer.
- Root cause: the label was written from a feature summary, not re-read against the quote the judge saw.
- Verified prevention: before accepting a false positive or negative, re-read the judged text for that capability and the full README for intent. A label that contradicts the judged text is a labelling error. The audit kept the pre-audit labels in `labels.v1-silver.json` and recorded each change in `labels.json` (`audit`).
- Reuse scope: any silver-label audit of a gate measurement.
- Evidence: `.work/workspace-brain/evidence/dark-channel-eval/labels.v1-silver.json` (before), `labels.json` (audit block), `eval-summary.md` (audit table).
- Confidence: high for this case (the quote is in the judged text). Updated: 2026-11-08

### A fixed text window turns missing evidence into automatic negatives
- Trigger: 10 of 33 thumbnail automatic zeros have a thumbnail keyword in the full README, outside the 3000-character window the judge read; 6 look like generators on a first reading.
- Root cause: the judge and the draft labeller read the same window, so a capability that appears later is invisible to both, and the automatic zero is an artifact of the window.
- Verified prevention: count automatic zeros against the full README before stating recall. Sensitivity with the 6 as positives: thumbnail recall 1.00 to 0.455, pooled recall 0.768 to 0.716, verdict unchanged. A window change needs a declared amendment.
- Reuse scope: any measurement whose judge input is truncated and whose labels come from that same input.
- Evidence: `_a2-window-check.py` output and sensitivity S12 in `eval-summary.md` (keyword candidates, not audited).
- Confidence: medium; the six are keyword candidates, not audited. Updated: 2026-11-08

### Native-command arguments with embedded double quotes are split by PowerShell
- Trigger: `python -m brain learn --body "..."` where the text contained double-quoted words; three of eight records were rejected.
- Root cause: PowerShell re-parses quotes when it passes arguments to a native executable, so the body was split at each embedded quote.
- Verified prevention: keep double quotes out of native-command arguments (use single quotes or pass the text through a file). The CLI rejected the leftover arguments with exit 2, so no wrong record was stored; the three were re-recorded and the search confirmed them.
- Reuse scope: any PowerShell call of a native CLI with free text.
- Evidence: learn runs in `E:\Github\workspace-brain` (2026-11-08); `unrecognized arguments` in the first attempt.
- Confidence: high. Updated: 2026-11-08

### Count the tests in a redirected log before trusting a green run
- Trigger: `python -m unittest discover ... > file 2>&1` in PowerShell produced a log with 40 of 43 tests; the missing module looked absent.
- Root cause: stderr from a test that prints JSON was turned into a PowerShell error record during redirection, which cut the log short.
- Verified prevention: capture with `2>&1 | Out-String`, then compare the `Ran N tests` line with the expected count. A rerun gave 43 tests with the same code.
- Reuse scope: any test run in PowerShell whose output is saved for evidence.
- Evidence: `.work/workspace-brain/evidence/unit-run-3.txt` (incomplete) versus `unit-run-final.txt` (46 tests).
- Confidence: high. Updated: 2026-11-08

### Shortlist bounds need a test before the first real download
- Trigger: the spec promised at most 6 clones per run, but the code limited only 2 per capability (up to 10). It was found before any clone ran.
- Root cause: the bound lived in a spec assumption, not in a test.
- Verified prevention: write each numeric bound as a unit test first (`test_clone_run_bounds_total_and_keeps_one_per_capability`), watch it fail, then implement and rerun.
- Reuse scope: any pipeline that downloads or spends budget per run.
- Evidence: `brain/pipeline.py:clone_run`, `tests/test_pipeline.py`, `clones.json` (6 cloned, 2 skipped_bound).
- Confidence: high. Updated: 2026-11-08


### Playwright `get_by_role(name=...)` matches substrings: a short label can click the wrong control
- Trigger: dark-videos Instagram publishing failed with `browser_file_input_missing`; the create
  step silently navigated to `/accounts/emailsignup/` instead of opening the composer.
- Root cause: `get_by_role("link", name="Criar")` matched the account-chooser link
  "Criar nova conta" (accessible names match as case-insensitive substrings). The chooser page was
  also not classified as a login wall, so the flow walked straight into it and reported the wrong
  failure.
- Verified prevention: (a) treat the chooser's own text ("Usar outro perfil") and the signup URL as
  a login wall; (b) skip any candidate control whose label names a signup ("nova conta",
  "new account", "sign up") before clicking; (c) prefer exact-name matching for short labels.
- Outcome (measured): live outcome flipped from `instagram_publish_failed`/`browser_file_input_missing`
  to the truthful `browser_login_required`; the row parks for reconnection instead of reporting a
  fake upload problem. Unit tests cover the real page text and the signup link.
- Reuse scope: any Playwright flow clicking by accessible name where a short label ("Criar", "Post",
  "OK", "Create") can collide with a longer control.
- Evidence: `D:/Git/dark-videos/backend/app/modules/publishing/browser_post.py` (`_login_wall`,
  `_signup_control`); `tests/modules/publishing/test_browser_post_helpers.py`; live DB rows
  `scheduled/browser_login_required`.
- Confidence: high (mechanism proven with a controlled retry and a DOM dump, then fixed and tested).
- Updated: 2026-10-24


### A button that "does nothing" usually selects zero rows: give the explicit click its own safe re-arm
- Trigger: dark-videos "Publicar tudo agora" produced no publications; the button, API and worker
  were all healthy.
- Root cause: the batch selected only queued rows with no error while every row was terminal
  (blocked/failed), so the click added zero records. Automatic re-arm was intentionally narrow
  (one pre-file-input error), so nobody covered the operator's explicit intent.
- Verified prevention: give the explicit operator action its own selection of duplicate-safe
  failures (raise sites before any upload, no native platform id), keep ambiguous outcomes stopped
  for automatic retries, never flip a row already tracked by the batch (the batch record owns that
  decision), and accept settled `skipped` records for those safe rows so a later failure is not
  stranded.
- Outcome (measured): one click re-armed 88 rows; 99 rows landed in `waiting_account` on the real
  blockers (dead sessions) instead of vanishing, zero duplicates, and the UI reported the reconnect
  need.
- Reuse scope: any queue or "do everything now" button whose selection can silently return empty.
- Evidence: `D:/Git/dark-videos/backend/app/modules/publishing/immediate.py` (`RESUME_ERRORS`,
  `start_batch`, `_retry_records`); `.work/publish-now-nothing/{EVIDENCE.md,live-after.json}`.
- Confidence: high (unit tests plus a live applied run with before/after row states).
- Updated: 2026-10-24


### Reasoning vision calls: a 60 s timeout and a tight max_tokens fail a whole review stage
- Trigger: dark-videos `frame` stage failed with 0 frames for 3 consecutive real runs; every
  visual review raised `source_frame_review_unavailable` (39/39 per run) while the same code and
  key worked in isolated probes.
- Root cause (two stacked, both reproduced): (a) the shared AI client used a fixed 60 s HTTP
  timeout; five high-detail frames to a reasoning model took 9.5-72 s per call, and under the
  stage's 8-way concurrency calls crossed 60 s, retried, crossed again, and died as
  "network error"; (b) the provider model returns `reasoning_content` (~850-900 tokens) before a
  ~20-token JSON body; with `max_tokens=800` some provider routings let the reasoning consume the
  budget, so the JSON never arrived and every answer failed schema validation. A fail-closed
  design then blocks every candidate and the stage aborts.
- Verified prevention: per-role timeout (vision review 150 s, default 60 s untouched), token
  budget sized above observed reasoning length (1500), and `exc_info=True` on the per-candidate
  rejection log so the provider error (timeout/HTTP/schema) is visible next time. Repro harness:
  synthetic control image (must return `clean`), 8-way concurrent replay on the real files, and
  a raw-response probe showing `reasoning_content` length vs `completion_tokens`.
- Outcome (measured): 100% review failure → 1 transient failure in 17 calls; a call that needed
  98 s now completes; approvals return (1.5-5 per ~99 candidates, matching the healthy day);
  52 tests green with zero new failures on the module.
- Reuse scope: any pipeline calling reasoning/"omni" models through a shared HTTP client or with
  a fixed token cap — size timeouts and budgets for reasoning tokens, and load-test at the
  production concurrency, not serially.
- Evidence: `E:/Github/ai-assistent-universal-coder/.work/frame-review-fix/RESULTADO.md`;
  `D:/Git/dark-videos/backend/app/core/ai.py` + `modules/mining/source_inspection.py`.
- Confidence: high (mechanism reproduced both ways; fix re-verified end-to-end on real files).
- Updated: 2026-10-22


### Batch-capped judges: add a learned coarse screen instead of shrinking batches
- Trigger: `estimate_virality` split every candidate pool into batches of 4 because the local Laya
  service caps the request state at 10,000 characters — with a 500-video pool × 3 networks that is
  375 calls per mine, and the batch cap silently set the cost model.
- Root cause: the fine judge was the only selector; nothing used the per-network evidence the app
  already had (outcomes with `views_24h` and account-media numbers, both with their content).
- Verified prevention: add a level-0 concept screen (deterministic content token → prior learned from
  observed numbers, shrunk toward the network mean; unknown stays unknown) that scores the whole pool
  in one no-model pass, then send only a bounded shortlist to the fine judge. Keep the old blend
  exactly when no prior exists and keep a separate boom gate so a strong candidate is never starved.
- Outcome (measured): 500 candidates → 32/rede; equivalent Laya calls 125 → 8 per network (−94%);
  coarse pass 23–103 ms; 462 tests with the same 25 pre-existing failures as the baseline.
- Reuse scope: any pipeline whose expensive per-item judge has a payload/batch cap.
- Evidence: `D:/Git/dark-videos/backend/app/modules/learning/ncm.py`; `.work/ncm-selection/EVIDENCE.md`.
- Confidence: high (mechanism + tests + smoke; predictive gain still awaits real outcomes).
- Updated: 2026-10-21


### Reproducing a paper claim: verify artifact hashes before trusting the number
- Trigger: reproducing NCM sudoku-hard from Hugging Face checkpoints (claim: 86.1% solved).
- Root cause: a claim is only reproducible with the exact artifacts; silent corruption or a divergent config invalidates the comparison.
- Verified prevention: download only the task subset (`hf download --include`), compare SHA256 against the HF LFS oids, diff the shipped `config.yaml` against the repo config, and record the exact toolchain versions + command before running.
- Outcome: solved 86.25% (1725/2000), cell 98.36% vs claimed 86.1% — exact reproduction.
- Reuse scope: any checkpoint-based benchmark reproduction.
- Evidence: `.work/ncm-repro/RESULTADO.md`; `02_repositorios/ncm` (no diffs).
- Updated: 2026-10-21


### Released research repos: .gitignore and configs reveal what the release omits
- Trigger: mapping a paper repo (ncm) from its clone only; the README describes the full system while the release is inference/eval only.
- Root cause: research checkpoint releases usually strip training loops, data prep and baselines; some config knobs survive without any implementing code.
- Verified prevention: cross-check (a) `.gitignore` ignored artifacts (vendored MDLM baseline, ~29G checkpoints), (b) config knobs with no implementation (`aux.code_corruption`, `fine_drop.dual/w_full/w_trunc`), and (c) entry points/dependencies — then label paper/blog numbers as unreproduced claims.
- Reuse scope: mapping or integrating any research repo published as a checkpoint/inference release.
- Evidence: `02_repositorios/ncm/.gitignore:219-221`; `config/eval/lm1b-*.yaml:118-124` vs absence in `models/quant.py`; `07_mapeamentos/mapeamento-ncm/beta.md` §9.
- Updated: 2026-10-21


### A fail-closed upstream monitor stays red without a recognition runbook
- Trigger: the daily TLC monitor failed on every scheduled run from 2026-11-06 with `Unsupported TLC rule change: CONTRIBUTING.md` after a documentation-only upstream change.
- Root cause: the gate correctly refused unrecognized control text, but recognizing a reviewed hash was an undocumented manual step, so eight consecutive runs (42195114515 to 43401412946) stayed red.
- Verified recognition: diff the changed upstream file against the locked commit, confirm no local gate consumes the text, update only the control hash, then rerun the apply chain on a throwaway clone (apply, validate, candidate, publish against a bare remote) before merging.
- Reuse scope: any pinned-upstream control or hash lock whose monitor fails closed.
- Evidence: PR #56 `27ceb253` recognized the hash; AEOS Enterprise CI on that SHA passed; simulated chain PASS. Failure notification routing was not verified.
- Confidence: high for the recognition procedure.
- Updated: 2026-11-13


### Modular Markdown must resolve from the module location
- Trigger: moving a long SKILL.md body into local section modules changed link bases; category folder names also contain parentheses.
- Root cause: root-relative resource examples were not all executable links, and a simple Markdown destination regex cannot parse balanced category parentheses or distinguish inline-code examples.
- Verified prevention: preserve section order, resolve real links relative to each module, retain source snapshots unchanged, parse balanced destinations and exclude fenced/inline-code examples. Keep required runtime-provider files explicit rather than fabricating absent resources.
- Reuse scope: large skill migrations and documentation/module relocation.
- Evidence: `00_skills/(creation)/skill-factory/scripts/validate-workspace.py`; current `00_skills/validation.report.json` verifies 2,872 operative links and 777 original TLC resource hashes.
- Updated: 2026-10-13


### CRLF line endings break regex parsing in Node test files
- Context/trigger: `npm run test:node:jest` failed on `architecture-knowledge-skills.test.cjs` and `tests-expert-charter.test.cjs` with `TypeError: object null is not iterable` and `Cannot read properties of null (reading '1')`.
- Problem/failure mode: Skills edited on Windows had CRLF (`\r\n`) line endings, but test regexes used `^---\n([\s\S]*?)\n---\n([\s\S]*)$` which expects LF (`\n`). The frontmatter regex returned `null` because `\r\n` doesn't match `\n`.
- Root cause: Files created/modified on Windows without normalization. Test regexes don't handle CRLF.
- Verified correction/prevention: Add `.replace(/\r\n/g, "\n")` before regex execution in test files. Normalize all skill files to LF on commit. Consider adding a pre-commit hook or CI check for line endings.
- Reuse scope: any Node test that parses YAML frontmatter or markdown with regexes across the workspace.
- Evidence: `tests/node/architecture-knowledge-skills.test.cjs:53`, `tests/node/tests-expert-charter.test.cjs:190`; CI run 38094530204 failed, 38095199770 passed after fix.
- Confidence: high
- Updated: 2026-10-10

### TLC skill ids reject characters outside kebab-case
- Context/trigger: a requested skill name contains `#`, spaces, or capitals.
- Problem/failure mode: `00_skills/(creation)/skill-architect/scripts/validate_skill.py` fails `folder_kebab_case` and `name_kebab_case` for any id outside `^[a-z0-9]+(-[a-z0-9]+)*$`.
- Root cause: the Tech Lead Club name rule and the validator use the same kebab-case pattern. `#` is not part of that pattern.
- Verified correction/prevention: use a kebab-case folder and `name`, and keep the original phrase in the description triggers. `csharp-expert` carries the trigger `c#-expert`.
- Reuse scope: any new skill whose requested name is not kebab-case.
- Evidence: `00_skills/(creation)/skill-architect/scripts/validate_skill.py`; `validate_skill.py 00_skills/(development)/csharp-expert` PASS on 2026-10-09.
- Confidence: high
- Updated: 2026-10-09

### Do not stack a generic bug boost onto the verification skill
- Context/trigger: `tests-expert` aliases included `corrigir` while its mission already contains `bug`.
- Problem/failure mode: `corrigir bug Java com testes` ranked `tests-expert` above `java-docs-bug-solver`. CI run `37850206011` failed `tests/node/skill-router.test.cjs`.
- Root cause: the shared bug boost and the skill's own correction alias each add 8, so the ride-along skill outranks the domain skill.
- Verified correction/prevention: keep the functional, end-to-end, and new-behavior phrases on `tests-expert`. Let the shared bug boost supply the ride-along score. `scripts/aeos-skill-router.mjs`.
- Reuse scope: any skill that must be selected beside a domain skill, not instead of it.
- Evidence: `tests/node/skill-router.test.cjs`
- Confidence: high
- Updated: 2026-10-08

### Freeze the user request before judging a bug fix
- Context/trigger: a functional check written after seeing the broken application, or rewritten once that check fails.
- Problem/failure mode: the expectation is changed until the suite passes, so the run no longer says whether the requested behavior exists.
- Root cause: the implementation, or the failure itself, was used as the oracle.
- Verified correction/prevention: freeze the user request and its checks before the run (`00_skills/(quality)/tests-expert/scripts/charter.mjs`). A later edit with the same request exits 2. A failure is stored in `.aeos/tests-expert/RESUME.md` and the application is fixed against the same checks.
- Reuse scope: any acceptance check whose job is to prove a requested fix or new behavior, rather than to lock the current code.
- Evidence: `tests/node/tests-expert-charter.test.cjs`
- Confidence: high
- Updated: 2026-10-08

### A real Shorts run has to close with the full top, not whatever the first search returned
- Context/trigger: dark-videos Painel showed 1 mined video and 1 selected after "escolher o top 20".
- Problem/failure mode: the public YouTube search kept at most 20 hits from a single "shorts" query, then ranking accepted a short list. The synthetic sample does not fill a live run.
- Root cause: `YtDlpSearchConnector.fetch_recent` used `min(limit, 20)` on one results URL, and `RankStage` did not require `target_count` on a real run.
- Verified correction/prevention: search several fixed queries, widen the lookback (7, 14, 30, then 90 days) until the pool can fill the top plus the reserve, and fail the rank and the final creative gate when a real run is still short. Dry-run simulation may still use the synthetic sample.
- Reuse scope: dark-videos mining and any other "top N" selector that silently shrinks.
- Evidence: pipeline run `6f685c35-c719-43d7-a081-1b980801a2ad` on 2026-10-09 mined 30, selected 20, packaged 20, scheduled 40. An earlier run with one query selected 7 and correctly failed the new floor.
- Confidence: high
- Updated: 2026-10-09

### Instagram browser upload uses the local file, ffmpeg, and the create dialog
- Context/trigger: Agenda showed Instagram `@topvideosbrasil_oficial` as Falhou with the generic "Falha na publicação".
- Problem/failure mode: `publications.last_error` was `media_provider_unconfigured` even though `source.mp4` was already on disk. Later attempts failed compose, then the file picker, then a feed Share button.
- Root cause: dispatch looked only in `PUBLISHING_MEDIA_TMP_DIR` (the code default was `/tmp/dark-videos-media`, not the desktop folder) and then asked a data provider that is not configured. ffmpeg was not on the worker PATH. The Instagram file input appears only after "Novo post", and "Compartilhar" on the home feed is a different button from the one inside the dialog.
- Verified correction/prevention: the media default is `~/.local/share/dark-videos/media`, and dispatch also searches that folder. Frame rendering looks up a WinGet ffmpeg when PATH is stale. The browser flow clicks "Novo post", waits for `input[type=file]`, and clicks Avançar and Compartilhar only inside `div[role=dialog]`. The Agenda maps those error codes into Portuguese.
- Reuse scope: dark-videos publish, and any browser uploader that must not click a control outside the dialog.
- Evidence: publication `0b471f64-35db-4905-81b8-5f9c2a16c646` is published. The profile grid shows `https://www.instagram.com/topvideosbrasil_oficial/reel/DeSb60QJH4G/` (2026-10-09).
- Confidence: high
- Updated: 2026-10-09

### OpenTelemetry Python does not redact app tokens, and an empty header list is unset
- Context/trigger: wiring OpenTelemetry SDK 1.45.1 and `opentelemetry-instrumentation-fastapi` 0.66b1 into dark-videos, with an in-app diagnostics page.
- Problem/failure mode: exported spans can keep `token=` query values, and `OTEL_INSTRUMENTATION_HTTP_CAPTURE_HEADERS_SERVER_REQUEST=.*` copies Cookie headers onto spans. The stock `LoggingHandler` also forwards raw extras and exception messages.
- Root cause: `redact_query_parameters` only redacts `AWSAccessKeyId`, `Signature`, `X-Goog-Signature` and `sig`. The ASGI middleware treats a false header list as unset (`capture_list or env`). `LoggingHandler._get_attributes` copies `exc_info` and log extras before application redaction.
- Verified correction/prevention: deny header capture with the regex `(?!)`, wrap the span exporter so attributes, exception events and the status description go through `app.core.redaction`, and bridge logs with a handler that redacts before the spool and before the OTel logger. Do not attach `LoggingHandler` directly.
- Reuse scope: Python services using FastAPI instrumentation and the OTLP HTTP exporter together with an existing redaction module.
- Evidence: installed sources in the dark-videos venv (`opentelemetry/util/http.py`, `opentelemetry/instrumentation/asgi/__init__.py`, `opentelemetry/sdk/_logs/__init__.py`); `backend/tests/observability/test_signals.py` passed on 2026-10-09.
- Confidence: high
- Updated: 2026-10-09

### A root log bridge fills a diagnostics ring with scheduler chatter
- Context/trigger: dark-videos attached a redacted log handler to the root logger while Celery beat dispatched `publishing.dispatch_due`.
- Problem/failure mode: the in-app log list showed only "task received" and "task succeeded" lines, so a real failure was hard to see under "Tudo".
- Root cause: Celery INFO logs propagate to the root handler, and the shared ring keeps the last 300 lines.
- Verified correction/prevention: drop `celery.*` below WARNING; keep warnings and errors. Store errors in a separate ring so they are not evicted by chatter.
- Reuse scope: any process that forwards the root logger into a bounded operator view while Celery beat is running.
- Evidence: diagnostics page in the browser on 2026-10-09; `backend/tests/observability/test_signals.py::test_celery_info_is_omitted_and_errors_stay_redacted`.
- Confidence: high
- Updated: 2026-10-09

### AEOS stdio MCP servers must answer newline-delimited JSON for real MCP clients
- Context/trigger: validating the `architecture-knowledge` MCP with the official `@modelcontextprotocol/sdk` 1.29.0 stdio client.
- Problem/failure mode: `rag-node` and `wordpress-knowledge` reply only with `Content-Length` frames; the SDK client's `initialize` times out, so MCP clients such as Cursor cannot use them although the AEOS harness tests pass.
- Root cause: the MCP stdio transport is newline-delimited JSON, while the AEOS servers and harness use LSP-style `Content-Length` framing, so harness tests never exercise the spec transport.
- Verified correction/prevention: reply in the framing of each request (`aeos/mcp-servers/architecture-knowledge-mcp.mjs:send()`), test both framings, and connect once with the SDK `Client` + `StdioClientTransport` before claiming client compatibility. The installed `@modelcontextprotocol/inspector-cli` 0.22.0 cannot run standalone (it imports a monorepo `package.json`); use the SDK client.
- Reuse scope: every AEOS stdio MCP server.
- Evidence: `tests/node/architecture-knowledge-mcp.test.cjs`; SDK handshake on 2026-10-07: `architecture-knowledge` connected with 10 tools, `rag-node` and `wordpress-knowledge` timed out.
- Confidence: high
- Updated: 2026-10-07

### Delimit short acronym aliases in substring routers
- Context/trigger: adding ADR, ASR and AKM aliases to `scripts/aeos-skill-router.mjs` boosts.
- Problem/failure mode: `request.includes("adr")` also fires on Portuguese words such as "padrão", boosting the ADR skill for unrelated requests.
- Root cause: boost aliases are plain substring matches without word boundaries.
- Verified correction/prevention: use space-delimited acronym aliases (`" adr "`, `" adr."`, `" adr-"`) against a space-padded request; existing aliases are unaffected because none begin or end with a space.
- Reuse scope: any short alias added to router boosts or keyword triggers.
- Evidence: `tests/node/skill-router-overlay.test.cjs` ("ignores 'adr' inside other words").
- Confidence: high
- Updated: 2026-10-07

### Quote YAML scalars that contain a colon
- Context/trigger: AEOS Enterprise CI failed on PR #42 while `runtime-auth-broker.test.cjs` loaded overlay registries.
- Problem/failure mode: a descriptive `skill_intent` with `control: cookie-jar` made js-yaml throw `bad indentation of a mapping entry`.
- Root cause: unquoted YAML plain scalars cannot contain `: ` ; the overlay loader parses the fragment strictly.
- Verified correction/prevention: quote `skill_intent` (and similar free-text scalars) whenever they include a colon; add a contract test that the value is quoted.
- Reuse scope: every AEOS overlay YAML fragment (`skill_intent`, `mission`, descriptions).
- Evidence: Actions run `35052357725`, `aeos/registries/mcps.kinghost.additions.yaml`, `tests/node/runtime-auth-broker.test.cjs`
- Confidence: high
- Updated: 2026-09-16

### Current language-expert skills must resolve version from official releases
- Context/trigger: `kotlin-expert` had to load "the latest Kotlin" the same way `java-21-expert` loads a versioned docs MCP.
- Problem/failure mode: pinning `docs-kotlin-current.resolved_version` from model memory would ship a stale compiler line.
- Root cause: Kotlin current-stable moves independently of this workspace; GitHub latest and kotlinlang.org What's New are the authority.
- Verified correction/prevention: resolve current stable from JetBrains/kotlin latest tag plus `kotlinlang.org/docs/whatsnew*.html` and `releases.html`; store it on `docs-kotlin-current` and `references/current-release.md`; reconfirm with `language_docs.version_status` before treating a newer tag as current.
- Reuse scope: any `docs-*-current` language expert skill.
- Evidence: JetBrains/kotlin `v2.4.20` (2026-09-07), https://kotlinlang.org/docs/whatsnew2420.html, `aeos/mcps/docs-kotlin-current.mcp.yaml`
- Confidence: high
- Updated: 2026-09-13

### Do not use ASCII `\\b` after accented PR-heading keywords
- Context/trigger: `evaluatePrWhy("## Porquê\\n...")` was BLOCKED while `## Why` passed.
- Problem/failure mode: Portuguese Why headings would fail the required-PR-context gate.
- Root cause: `ê` is not an ASCII word character, so `porqu[eê]\\b` never sees a word boundary before the newline.
- Verified correction/prevention: terminate the keyword with `(?=[\\s:#]|$)` instead of `\\b`.
- Reuse scope: any heading parser for Portuguese/Unicode keywords.
- Evidence: `tests/node/devops-pipeline-engineering.test.cjs`, `scripts/aeos-devops-pipeline-governance.mjs`
- Confidence: high
- Updated: 2026-09-13

### `git ls-files` through default execFileSync overflows after large worktrees
- Context/trigger: tracking `.work/reidoabc-wordpress-runtime` grew the index past 13k paths; `aeos-single-agent-guard` called `execFileSync("git", ["ls-files", "-z"])`.
- Problem/failure mode: CI dies in the first quality gate with `ENOBUFS` before later guards run.
- Root cause: Node's default `maxBuffer` is 1 MiB; a NUL-terminated full-tree listing exceeds it.
- Verified correction/prevention: list tracked files through a shared helper with a 64 MiB buffer; ignore vendor `.work/` in full-workspace and Python inventory.
- Reuse scope: any guard that shells `git ls-files` against a large tracked tree.
- Evidence: Actions run `34705050420`, `scripts/lib/git-tracked-files.mjs`
- Confidence: high
- Updated: 2026-09-12

### WooCommerce page assignment and rewrite state must be verified separately
- Context/trigger: the local WooCommerce cart page was published and assigned, yet its generated `/cart/` URL returned HTTP 404.
- Problem/failure mode: confirming only `woocommerce_cart_page_id` can falsely suggest the customer route is available.
- Root cause: permalink rewrite rules were stale after page setup.
- Verified correction/prevention: verify the public route itself after assigning WooCommerce pages; flush rewrites when the page exists and its canonical URL still 404s.
- Reuse scope: local WordPress/WooCommerce bootstrap or page reassignment.
- Evidence: `.notebook/PROGRESS.md`, `E:\GitHub\repos-workspace\reidoabc` local runtime smoke on 2026-09-12.
- Confidence: high
- Updated: 2026-09-12

### Zero-Python inventory blocks assimilated skill gates
- Context/trigger: feature skills that ship `scripts/*.py` were copied into the workspace while `aeos-no-python-guard.mjs` still failed on any `*.py`.
- Problem/failure mode: assimilation could look complete in registries and still be blocked by bootstrap/verify.
- Root cause: a workspace-wide language ban treated skill tools as policy violations.
- Verified correction/prevention: allow Python in the workspace; keep Node for kernel orchestration; make the guard require declared skill scripts instead of forbidding them.
- Reuse scope: any later assimilation of a skill that ships Python validators or project metadata.
- Evidence: `references/PYTHON_WORKSPACE_POLICY.md`, `scripts/aeos-python-workspace-guard.mjs`, `.notebook/PROGRESS.md`
- Confidence: high
- Updated: 2026-09-12


### Bootstrap containerized WordPress through a physical script
- Context/trigger: local WordPress installation and WooCommerce seed data needed to run inside a Docker container without leaking generated credentials.
- Problem/failure mode: ad hoc PHP fed through a container stdin can be interpreted inconsistently and makes exit-status validation less clear.
- Root cause: bootstrap logic was coupled to shell transport rather than a versioned PHP entry point.
- Verified correction/prevention: run a repository-owned bootstrap PHP script through `docker compose exec`, pass the generated local admin secret only as a runtime environment variable, and fail PowerShell on a non-zero exit code.
- Reuse scope: local Docker WordPress initialization and other containerized PHP migrations.
- Evidence: `E:\GitHub\repos-workspace\reidoabc\scripts\bootstrap-local-wordpress.ps1`, `.notebook\PROGRESS.md`.
- Confidence: high
- Updated: 2026-09-12

### Validate external cookie files before any content preview
- Context/trigger: WordPress runtime access was requested through an external cookie path, but the requested `.txt` file was missing and a nearby file was not a cookie jar.
- Problem/failure mode: treating a nearby credential-looking file as a cookie source can expose plaintext credentials during diagnostics and still fail authentication.
- Root cause: file existence and cookie-jar format were not validated before inspecting nearby candidate content.
- Verified correction/prevention: first verify exact path existence, then validate Netscape/Set-Cookie shape without printing contents; if invalid, stop credential handling and request/procure a real cookie jar or governed backup/export access.
- Reuse scope: any AEOS workflow that consumes external cookie/cookie-jar files for authenticated HTTP.
- Evidence: `.notebook/PROGRESS.md`, `.aeos/wordpress/sites/3015e2f77281a57c0f638d5ae2f64ed86a7694fbe018bbe926f36319d945d6d5/security-audit.json`
- Confidence: high
- Updated: 2026-09-11

### Centralize runtime credentials behind opaque sessions
- Context/trigger: session-authenticated systems such as remote WordPress require cookie jars, while workspace rules prohibit persisting credential values.
- Problem/failure mode: implementing cookie reading separately in each skill/MCP either duplicates security logic or pushes raw credentials into model/tool parameters.
- Root cause: credential acquisition and credential use were coupled to domain adapters.
- Verified correction/prevention: keep acquisition/materialization in a central runtime broker; return opaque session refs; make governed adapters consume the session internally with TTL, host scoping, redaction and shutdown cleanup.
- Reuse scope: every AEOS integration that requires cookies, environment credentials or future credential-provider adapters.
- Evidence: `runtime/src/kernel/runtime-auth-broker.ts`, `runtime/src/kernel/tool-router.ts`, `references/CODENAVI_RUNTIME_AUTH_STANDARD.md`, AEOS Enterprise CI runs #154/#155.
- Confidence: high
- Updated: 2026-09-11

### Overlay registries must be active in the execution runtime
- Context/trigger: WordPress skills/playbooks/MCPs were correctly indexed as overlay fragments but the kernel still loaded several base registries directly.
- Problem/failure mode: an artifact can exist, pass documentation/static checks and still be unreachable by real playbook execution.
- Root cause: registry overlay resolution and execution-time registry loading had diverged.
- Verified correction/prevention: load base + active overlay fragments by registry type with deterministic replacement order; test that overlay-only skill/playbook/MCP IDs resolve and that core runtime MCPs are injected.
- Reuse scope: all future AEOS registry extensions.
- Evidence: `runtime/src/kernel/registry-loader.ts`, `tests/node/runtime-auth-broker.test.cjs`.
- Confidence: high
- Updated: 2026-09-11

### Separate continuity concerns instead of using one oversized memory file
- Context/trigger: long-running workspace work needs state continuity across sessions without contaminating durable memory with transient logs.
- Problem/failure mode: mixing current progress, durable facts, handoff state and generalized lessons creates stale or contradictory context.
- Root cause: different information lifetimes were stored in the same undifferentiated artifact.
- Verified correction/prevention: use four bounded artifacts — HANDOFF, MEMORY, PROGRESS and LEARNING — and cross-link instead of duplicating.
- Reuse scope: all material CodENavi-governed workspaces.
- Evidence: `references/CODENAVI_CONTINUITY_STANDARD.md`
- Confidence: high
- Updated: 2026-09-09

### Shared Node test files must respect every configured test runner
- Context/trigger: a new `.test.cjs` file is executed by both Jest and Mocha in `aeos:verify:full`.
- Problem/failure mode: Mocha `before` failed under Jest; switching blindly to Jest `beforeAll` then failed under Mocha.
- Root cause: the repository intentionally points more than one test runner at the same test glob, so runner-specific lifecycle globals are not portable.
- Verified correction/prevention: use a small compatibility selection (`beforeAll` when available, otherwise `before`) or runner-neutral test structure; verify the full matrix, not only the first runner.
- Reuse scope: all shared `tests/node/**/*.test.cjs` suites.
- Evidence: PR #26 recovery cycles 1–3; `tests/node/devops-pipeline-engineering.test.cjs`.
- Confidence: high
- Updated: 2026-09-11

### CI recovery must invalidate previous-SHA success after every corrective push
- Context/trigger: recursive pipeline repair creates a new commit for each root-cause correction.
- Problem/failure mode: treating a green older SHA as merge evidence can merge code that was never verified.
- Root cause: CI state was correlated to branch/PR conceptually rather than to the immutable head commit.
- Verified correction/prevention: bind run/job/check evidence and merge approval to expected head SHA; rediscover all relevant runs after every push.
- Reuse scope: every GitHub Actions recovery/merge workflow.
- Evidence: `scripts/aeos-devops-pipeline-governance.mjs`, `00_skills/(cloud)/devops-pipeline-engineering/SKILL.md`.
- Confidence: high
- Updated: 2026-09-11

## Slow work in scheduling transactions and unowned process cleanup
Updated:2026-10-13
Entry point: E:/Github/ai-assistent-universal-coder/.work/publishing-fix/RESULTADO.md
Trigger: approved posts remain invisible while Stories are evaluated; an execution ends abruptly during subprocess-heavy work.
Verified defects: network/media work held the reservation transaction; phrase renderer silently discarded wrapped lines; PID cleanup was requested even after an owned job was closed (two controlled safety failures).
Prevention: commit approved work first, keep acquisition outside reservation transactions, checkpoint each result, fit all text before drawing, compare composed pictures to their source reference, and terminate owned jobs/handles instead of reusing numeric PID graphs.80 concurrent real subprocess checks and resumed source recovery passed. The exact cause of the earlier abrupt exit was not observed, so do not promote that causal attribution.
Reuse: asynchronous media pipelines, delayed publishing and Windows subprocess supervision.

### Refusal history must not consume the operational queue window
Updated:2026-10-13
Entry point: backend/tests/modules/publishing/test_schedule_history.py
- Trigger: old blocked rows and new scheduled posts appear together at the same dates, making a healthy queue look blocked.
- Root cause: one chronological100-row window includes both statuses;101 older refusals hide a valid upcoming row.
- Fix/prevention: separate active and refusal queries/windows, expose aggregate totals, label prior dates and regression-check both queue visibility and blocked action guards.
- Reuse: bounded dashboards and job queues retaining refusal/audit history.
- Evidence: E:/Github/ai-assistent-universal-coder/.work/youtube-unblock/RESULTADO.md; original failing baseline, corrected test and actual browser verification.

### Keep accepted upload, processing and public confirmation distinct
Updated:2026-10-13
Entry point: backend/tests/modules/publishing/test_youtube_processing.py
- Trigger: enabled Public save yielded an open processing notice and the app marked an already-public video failed.
- Observed evidence: native failure screenshot and subsequent exact Studio ID/metadata plus anonymous playback. Controlled delayed4s notice reproduced the short observation-window defect; actual live notice arrival time was not measured.
- Prevention: observe the provider receipt for the complete save window, traverse current shadow roots, keep the upload identity, and require the owned public metadata before accepting processing. Reconcile uncertain results by exact ID rather than upload again.
- Reuse: asynchronous media providers whose visible upload receipt precedes final availability.
- Evidence: E:/Github/ai-assistent-universal-coder/.work/youtube-publish-now/RESULTADO.md; original/delayed baselines, corrected browser checks and remote verification artifacts.
# Git source integrity across operating systems
Updated: 2026-10-14
Entry point: quality/common.py:canonical; quality/validate.py:executable_resources
- Trigger: Windows checkout passes, published/clean Git checkout fails hashes or direct helper invocation.
- Root cause: CRLF acquisition hashes differ from normalized Git blobs; Windows staging can drop executable modes while file bytes match.
- Verified correction: UTF-8 textual hashes normalize CRLF toLF (binary hashes stay exact); retain acquired_sha256, declare LF attributes and executable metadata; assert100755 in Git/CI. Baseline441 export hash errors and3 missing helper modes reproduced;42 tests, clean exported blobs and remote Linux CI38654364112 prove the corrections.
- Reuse: cross-platform skill/resource distribution and any source-pinned tool bundle. Evidence: quality/tests/test_gates.py; .specs/tlc-capability-ci/SPEC.md; GitHub CI38650490307 and the final commit's workflow evidence.


### Recibos nativos e interfaces que remontam controles
Updated: 2026-10-14
Entry point: backend/app/modules/publishing/studio_schedule.py
- Trigger: upload salvo, mas a consulta local informa falha, ou um controle continua esperando depois de estar pronto.
- Causa verificada: listas virtualizadas exigem rolagem no contêiner com overflow, e React pode substituir o nó de um checkbox/botão durante a operação. Na lista TikTok real, a leitura parcial retornou11 itens; a leitura até o fim retornou70.
- Prevenção: reler locators após mudanças; identificar o contêiner pela geometria/overflow; exigir ID, conta, legenda quando disponível e horário nativo antes de confirmar. Conferir resultados incertos antes de reenviar.
- Reuso: automações de Studios com tabelas virtuais e formulários controlados. Evidências: test_native_studio_receipts.py; .work/studio-scheduling/tiktok-census.json; meta-failures-readback.json.

<!-- RGL-IMPLEMENTATION -->
### Installed SDK contracts and a real first training step are acceptance gates
- Trigger: published Graphiti/MCP/Laya/TRL APIs differ from an upstream branch or assumed shorthand.
- Root cause: Graphiti treats supplied UUIDs as existing episodes; MCP2 uses constructor handlers; Laya gold is a probability distribution; TRL1.15 fused loss calls an unavailable Triton function on Windows.
- Verified prevention: inspect pinned installed signatures/source, run native preprocessing, prove an actual step before full training, and use supported extension points. Preserve failed evidence/base weights; never label a handshake or train-loss decrease as domain quality.
- Reuse scope: SDK integrations, retrieval pipelines and local PEFT training.
- Evidence: rag-graph-laya-mcp/app/providers.py, worker.py, app/portable_sft.py, VERIFICATION.md;19functional/protocol tests and real model/graph experiments.
- Updated:2026-10-15
<!-- /RGL-IMPLEMENTATION -->

<!-- RGL-MONGO-REVIEW -->
### Verify each producer's hash and span contract before declaring corruption
- Trigger: MongoDB chunk hash differs from SHA256(text), and literal abstract slicing differs from stored chunk text.
- Root cause: inspected producer hashes document_id+":"+text and packs title/sentences with normalized spaces while retaining original span boundaries.
- Verified prevention: read the producer contract, compare the correct digest and normalized source span, and report mismatch types separately. Do not overwrite source hashes to fit a consumer's assumed scheme.
- Reuse scope: corpus migrations, RAG importers and provenance audits.
- Evidence: DiabeticsresearchJEV/application/scraping/ingest.py:266, application/text/chunker.py:63; rag-graph-laya-mcp/docs/mongodb-review/evidence.json.
- Updated:2026-10-15
<!-- /RGL-MONGO-REVIEW -->

### Seletores nativos que mudam de estado entre campos
Updated: 2026-10-16
Entry point: D:/Git/dark-videos/backend/app/modules/publishing/studio_schedule.py:tiktok_datetime
- Trigger: horário solicitado23:05 retornava17:05/17:10/19:05 no Studio. Causas reproduzidas: data pode abrir o painel; um clique cego o fecha; opções ocultas recebem eventos sintéticos; rolar a página para alcançar uma opção pode dispensar o popup.
- Prevenção: centralizar relógio na tela e opção na coluna, verificar visibilidade, reabrir entre campos e exigir leitura exata antes de salvar.
- Reuso: seletores controlados que preservam opções ocultas no DOM. Evidências: .work/studio-scheduling/{picker-baseline-tests.json,picker-viewport-baseline-tests.json,stage-picker-tests.json,installed-picker-tests.json,tiktok-hour-centered.json}.

## Lote terminal pode divergir da linha reparada
Updated: 2026-10-26. Entry point: `.work/publish-all-click/reproduce.log`.
- Trigger: pedido explícito de retomada retorna zero embora existam agendamentos válidos.
- Causa: retry consulta só estados/erros históricos do registro, ignorando reparos posteriores na linha de publicação.
- Prevenção: reavaliar estado e identidade nativa atuais na ação explícita; conservar o caminho sem novo upload e exigir recibo real de sucesso.
- Reuso: filas persistidas com registro agregado e entidade operacional mutável. Prova: sete regressões em `test_click_recovery.py`, baseline falha/correção passa; sem generalizar para reenvio de uploads incertos.


## Destino faz parte da identidade da publicação
Updated: 2026-10-27. Entry point: `.work/instagram-both/PLAN.md`.
- Trigger: mesma mídia deve ser enviada para duas superfícies da mesma conta.
- Causa: unicidade e consultas só por conteúdo+conta tratavam Reel e Story como alternativas.
- Prevenção: incluir destino em constraint e lookups; criar contraparte sem copiar id/recibo/estado de sucesso; manter falhas independentes e completar de forma idempotente.
- Evidência: oito testes em test_instagram_destinations.py, teste HTTP com ambos os placements e constraint real no smoke. Reuso: filas com múltiplos destinos por identidade de conteúdo.

## Controles próximos a resultados dinâmicos
Updated: 2026-10-29. Entry point: .work/identifyer-posture/deployment.json.
- Trigger: resultado de câmera altera altura entre localizar e clicar um botão; teste gerou metadados sintéticos inesperados.
- Root cause: botão opcional abaixo de detecções com altura variável; o deslocamento levou o clique ao controle de salvar.
- Fix/prevention: posicionar controles junto a uma área estável e verificar ausência de mutações HTTP em fluxos somente de análise. Teste de postura instalado confirmou zero POST/DELETE.
- Reuse scope: interfaces com atualizações contínuas e controles de ação abaixo de conteúdo variável. Evidência: scripts/browser_pose.py e docs/VERIFICATION.md do iDentifyer.

---

## LLM JSON schema: coergir tipos antes de validar capítulo
Updated: 2026-10-29. Entry point: science-studio/providers.py:script.
- Trigger: estágio `script` do dark-videos falhou com `KeyError: 'duration'` e, noutro execução, `KeyError: 'scenes'` (modelo Qwen3:4b retornou duração como string e omitiu chaves).
- Root cause: saída de LLM não é confiável quanto a tipos/presença de campos do esquema esperado.
- Fix/prevention: coercionar `duration` string→int antes da soma do capítulo e preencher defaults do scene_schema para campos ausentes; nunca tratar saída crua do modelo como contrato válido.
- Reuse scope: qualquer adapter de roteiro que consome JSON de modelo local. Evidence: `.work/electron-descoberta/project.json` (6 cenas validadas, 60 s).
- Confidence: high. Updated: 2026-10-29

---

## Science Studio generate: argv aceita caminhos relativos (resolvidos contra a raiz do estúdio); voz Piper exige narrações no ratio [0.85, 1.2]
Updated: 2026-10-29. Entry point: science-studio/studio.py:generate, providers.py:voice.
- Trigger: `generate` falhou ao executar os providers (`science-studio/providers.py` não encontrado com `cwd=` diretório do projeto) e o estágio `voice` rejeitou narrações (ratio fora de [0.85, 1.2]). O estágio `script` também falhava com saída de LLM instável (chaves ausentes, duração como string).
- Root cause: `generate` executa subprocessos com `cwd=root` (diretório do projeto), então caminhos relativos no `providers.json` (ex. `science-studio/providers.py`) são procurados dentro do diretório do projeto e não encontrados. O Piper/Faber gera áudios com duração imprevisível, fora da faixa aceita.
- Fix/prevention: `studio.py` ganhou `studio_root()` + `resolve_command()` — caminhos relativos no argv que não existem no diretório do projeto são resolvidos contra a raiz do estúdio (onde ficam os providers/workflows locais), permitindo `providers.json` com caminhos relativos. O estágio `script` agora preenche defaults do `scene_schema` para campos ausentes e coerge `duration` string→int. Narrações ajustadas manualmente para duração de áudio entre 85% e 120% da duração da cena.
- Reuse scope: qualquer uso do `studio.py generate` com providers locais e adaptação de roteiro para TTS local. Evidence: `.work/electron-descoberta/providers.json` (caminhos relativos funcionando), `delivery/final.mp4` (60 s entregue).
- Confidence: high. Updated: 2026-10-29

---

## Áudio documental: mixagem real (amix + ducking) e voz local de qualidade
Updated: 2026-10-29. Entry point: `science-studio/audio_mix.py`, `science-studio/voice_kokoro.py`.
- Trigger: usuário pediu voz fluida no padrão Google para documentário, simulação de voz para YouTube e música de fundo calma; o pedido citava "nemontron-voicechat", inexistente no ambiente.
- Root cause/limite: `amerge` não é mixagem (une canais; só "funcionou" porque o downmix para mono averaging), a mixagem anterior era aparente; `amix` exige pesos separados por espaço (':' quebra o parse: "No option name near '0.28:0.18...'"); a única voz local era Piper (robótica); clonar a voz real de narradores de YouTube sem autorização é inválido por consentimento/licença, e nemotron (NVIDIA) é família de LLM sem TTS de clonagem.
- Fix/prevention: `science-studio/audio_mix.py` — voz com EQ + compressor + loudnorm, base musical calma (procedural de 5 harmônicos com aecho/tremolo ou arquivo fornecido), ducking por `sidechaincompress` (voz como sidechain) e `amix` com `normalize=0` + pesos por espaço; `--in-place --record render.json` mantém preview revisado e export como o mesmo arquivo. Voz: `science-studio/voice_kokoro.py` (Kokoro-82M PT-BR, pm_alex/pm_santa/pf_dora) ajustando a taxa natural de fala antes de um atempo residual mínimo; `science-studio/voice_google.py` para voz Google real, com chave só em runtime e falha fechada.
- Regra operacional: todo vídeo dark-videos/Science Studio é salvo em `D:\Git\dark-videos`; a voz default é o adapter local Kokoro.
- Reuse scope: qualquer entrega Science Studio/dark-videos com narração, trilha e ducking. Evidence: `science-studio/{voice_kokoro.py,voice_google.py,audio_mix.py}`, `.work/electron-descoberta/{audio/kokoro-report.json,preview.audio-mix.json}`, `D:\Git\dark-videos\.work\electron-descoberta\copy-report.json`, delivery/final.mp4 (I=-16,0 LUFS, true peak -1,5 dBFS).
- Confidence: high (áudio gerado, medido com ebur128 e hash approval == export). Updated: 2026-10-29


## Medir fatos estruturais em código e perguntas atômicas ao JEV — 2026-11-16
- Trigger: `workflow_modules` com precisão 0,33 e `boundaries_secrets` com recall 0,53 numa amostra de 36 skills.
- Root cause: o defeito estava no rótulo/pergunta, não nos skills. (1) Rótulo por cabeçalho literal classificou como 0 skills que roteiam de fato para `references/`; (2) pergunta composta (segredos E falha fechada) e keyword `permission` casando com "permission gates".
- Fix/prevention: fato estrutural (contagem de links) vira checagem em código sobre os 324 skills; pergunta composta vira dois Nouls atômicos; rótulo por sentença (keyword + verbo de obrigação), `null` quando ambíguo. Depois de ler os falsos negativos a amostra fica queimada: declarar emenda ANTES e medir em amostra nova disjunta (A1: 60, A2: 60). Uma pergunta mais estreita que o rótulo faz o Noul ficar perto de 0,5.
- Reuse scope: qualquer eval JEV/LLM-judge com rótulos prata. Evidence: `.specs/skills-quality-eval/rubric.md`, `.work/skills-quality-eval/`. Confidence: high (secrets 36 FN → 0 FN em amostra nova). Updated: 2026-11-16

## `git show rev^:path` em `cmd` restaura arquivo vazio — 2026-11-16
- Trigger: restauração de `references/*.md` com `cmd /c "git show faac5adf^:... > f"` gerou arquivos de 0 bytes.
- Root cause: `^` é caractere de escape no `cmd`; a revisão virou `faac5adf:`. O redirecionamento criou o arquivo antes do erro do git.
- Fix/prevention: ler os bytes via `subprocess` do Python e comparar com `git show` antes de seguir. Reuse scope: restauração de arquivos do histórico no Windows. Confidence: high. Updated: 2026-11-16

## Regravação de arquivo grande falha intermitente no Windows (Errno 22)
- Trigger: `verify.py` FAIL só em 'Regeneração 2' (`OSError 22` ao abrir `mapa.json` p/ escrita logo após escrevê-lo); build isolado passava.
- Causa: observador externo segura o arquivo recém-escrito (3,3 MB). Reproduzido sem o código do projeto: 5/30 regravações idênticas falharam em rajada.
- Fix: `scripts/build.py:save()` com 8 tentativas e recuo, re-levanta erro acionável (não engole); `matriz.csv` passou a usar `save()` (hash idêntico antes/depois). Evidência: verify PASS 5/5 após o fix.
- Reuso: gerador com regeneração byte-idêntica que reescreve o mesmo arquivo em sequência no Windows deve tolerar lock transitório. Um PASS isolado não prova que um erro intermitente sumiu: repetir N vezes.

