# verification.md — registro manual de proofs (2026-11-11)

Registro HONESTO, manual. O gate formal `check_proofs.py` exige HEAD limpo — impossível sob a
política do owner (nada é commitado sem autorização). Comandos executados nesta sessão, com
`JAVA_HOME=.tools/jdk25/jdk-25.0.5+8`, a partir de `10_projetos_estruturantes/otel-telemetry-java/`.

## Sessão de verificação

| # | Comando | Resultado |
| --- | --- | --- |
| 1 | `mvnw test -pl otel-telemetry-core` | exit 0 — 10/10 (C1, C2, C3, C4, C8) |
| 2 | `mvnw test -pl otel-telemetry-core,otel-telemetry-exporters` | exit 0 — +10/10 (C5, C6, C7) |
| 3 | `mvnw test -pl otel-telemetry-adapters,otel-telemetry-spring-boot-starter` | exit 0 — 4/4 (C9–C12) |
| 4 | `mvnw test -pl otel-telemetry-devtools` | exit 0 — 11/11 (C13–C19, C26, C27) |
| 5 | `npx vitest run tests/loader-cap.test.ts` (devtools/dashboard) | exit 0 — 2/2 (C22, `capsLoadedWindow`) |
| 6 | `npm run build` (dashboard) | exit 0 → `otel-telemetry-devtools/src/main/resources/dashboard/{index.html,dashboard.js,style.css}` |
| 7 | smoke sink + dashboard (jar em execução) | `/` 200 (refs relativas ok) · `/dashboard.js` 200 · `/style.css` 200 · `/api/health` 200 |
| 8 | `mvnw test -pl otel-telemetry-examples/otel-telemetry-example-java` | exit 0 — 1/1 (C25) |
| 9 | `mvnw test -pl otel-telemetry-examples/otel-telemetry-example-spring` | exit 0 (compilação) |
| 10 | `mvnw verify` (reactor completo) | **exit 0** |
| 11 | `mvnw test -pl otel-telemetry-core` (pós-F5: +`builderHeaderValueWithCommaSurvives`) | exit 0 — 11/11 |
| 12 | `npx vitest run tests/loader-cap.test.ts` (vitest 4.1.12, pós-F6) | exit 0 — 2/2 |
| 13 | `npm audit` (dashboard, pós-F6) | 0 vulnerabilidades |
| 14 | `mvnw verify` (pós-F1–F6 + C25 presence-scan + `demo.mjs` com spans + overlay fix) | **exit 0** — estado final |

## Mutações (spec-lean, 3 contratadas)

| M | Alvo | Resultado |
| --- | --- | --- |
| M1 | ConfigResolver: yaml movido para depois de env (inverte AD-003) | **MORTA** — `ConfigResolverTest.syspropOverridesYaml` falhou (exit 1) |
| M2 | JsonlStore.rotate: loop até maxFiles em vez de maxFiles-1 | **SOBREVIVEU na 1ª tentativa** → teste `rotationHonorsCeilings` fortalecido (20→25 appends, teto 512 B → rotação em cascata até traces.3.jsonl) → **MORTA**. Corpo do teste mudou; comando de proof congelado intacto. |
| M3 | auth do sink | 1ª tentativa INVÁLIDA (unreachable statement — não compila, não é kill). Corrigida para `SinkConfig.authRequired() → false` → **MORTA** — `missingTokenReturns403` + `loopbackDefaultAndOverrides` falharam (2/3) |

Mutações revertidas; `mvnw test -pl otel-telemetry-core,otel-telemetry-devtools` exit 0 após reversão.

## Fixes The-Judge (F1–F6, 2026-11-11 — sessão de correção)

| # | Correção | Prova |
| --- | --- | --- |
| F1 | dedup client-side por `recordKey` em `mergeNew` (span `traceId:spanId`; log `timeNs\|\|timeMs:message`; metric `name:last timeMs:value`); servidor mantém filtro inclusivo `>=` | walk C20 no browser: servidor re-envia a linha de fronteira (1 item, filtro `>=`) e a contagem fica **estável em 11** após 3 polls em repouso (sem dedup cresceria ~1/poll) |
| F2 | `apiFetch` com `Authorization: Bearer` + `window.prompt` no primeiro 403 (reenvio único); UI estática continua sem auth por design | sink com `OTELTELEMETRY_SINK_TOKEN=walk-token-123`: 1 prompt → 11 spans `demo.round` visíveis (playwright) |
| F3 | chamada morta `metric?.histogram?.forEach(() => undefined)` removida (loader.ts) | build + vitest 2/2 |
| F4 | `ingestFiles` acumula o lote (contagem regressiva de readers) e aplica o MESMO dedup no modo arquivo (arquivos rotacionados se sobrepõem) | walk C21: 2 arquivos no mesmo input → 11 registros com `demo.round` E `walk.span.idle` (não last-wins, sem duplicatas) |
| F5 | headers do builder ficam `Map<Signal, Map<String,String>>` (`builderHeadersBySignal`) até o fim de `resolve()`; `encodeHeaders` removido; `parseHeaders` só entra quando camada superior definiu a chave | teste novo `builderHeaderValueWithCommaSurvives` — valor `a,b` sobrevive; `mvnw test -pl otel-telemetry-core` 11/11 |
| F6 | pins **vite 6.4.6 + vitest 4.1.12** (OSV: 6.4.4 fecha os 8 GHSAs de vite; vitest exige ≥4.1.11 pelo GHSA-82fw; peer/engines ok com Node 24). Vite 6 default CSS = nome do pacote → `cssFileName: 'style'` em `vite.config.ts` restaura o contrato `style.css` | vitest 4.1.12 — 2/2 · `npm audit` 0 vulnerabilidades · bundle `dashboard.js` + `style.css` revalidado no sink vivo |

C25: `BootstrapSmokeTest` fortalecido para presence-scan (`smokeCounterExported`) — a
self-métrica `otel.sdk.metric_reader.collection.duration` do SDK podia preceder `smoke.counter`
no lote de shutdown (flake 2/3 observado). 5× rerun verde. Comando de proof congelado intacto.

## Walks (2026-11-11 — C20, C21, C23, C24 + F2)

- **C20 PASS** (playwright, live): 10 spans do demo → 3 abas renderizam → linha de fronteira
  gravada no store → 11 → servidor re-envia a fronteira (1 item, filtro `>=`) → 3 polls em
  repouso = estável 11 (prova do F1). Screenshot: `…\Temp\opencode\c23walk\c20-live.png`.
- **C21 PASS** (playwright, `file://`): status "modo arquivo"; ingest de 2 arquivos → 11
  registros com conteúdo dos dois (prova do F4). Screenshot: `…\Temp\opencode\c23walk\c21-file.png`.
- **C23 PASS**: `node demo.mjs` em scratch FORA do repositório (documentado no README
  multilíngue) — 10 spans `demo.round` → `traces.jsonl` (4164 B) → `GET /api/traces` retorna
  `demo.round`/`demo-node` → dashboard exibe na aba Traces.
- **C24 PASS**: README multilíngue percorrido (5 seções, Rust experimental, J1 rotulado); 2
  defeitos documentais corrigidos (path `otel-telemetry-examples/`; classpath two-step provado
  + nota de scratch + `@opentelemetry/api` no `npm i` + data da execução).
- **F2 walk PASS** (ver tabela acima).

Três bugs REAIS encontrados pelos walks (fora dos findings do Judge):
1. **overlay invisível bloqueava TODOS os cliques**: `#drop-overlay{display:flex}` vence o
   `[hidden]` do UA stylesheet → overlay full-screen invisível interceptava a UI inteira.
   Fix: `#drop-overlay[hidden] { display: none; }` (index.html).
2. **demo sem spans**: `demo.mjs` nunca criava spans — nada era exportado (o arquivo nunca
   tinha sido executado). Fix: `trace.getTracer` + span por rodada + `@opentelemetry/api`.
3. **flake C25**: self-métrica `otel.sdk.*` antes de `smoke.counter` — ver nota acima.

## Não executado (honesto)

- **Rotas dynatrace/grafana**: NÃO VERIFICADO (J1) — docs dos vendors 403/404 em 2026-11-11; shape implementado é o definido pelo plano, rotulado no código (`Presets.java`).
- **check_proofs.py formal**: não rodado (política sem commits); este arquivo é o substituto manual.
- **Python/Go/.NET/Rust**: runtimes não provisionados; contrato documentado em `presets-multilingue/README.md` (Node é o único runtime provisionado e verificado neste walk).

## flakes observados

- 1× `ageCeilingRotates`: `@TempDir` do JUnit falhou a limpeza no Windows (`DirectoryNotEmptyException`) — re-execução verde; sem alteração de código. Flake de ambiente, não defeito.

## Estado final (2026-11-11, pós-reversão das mutações)

- `mvnw verify` (reactor completo, estado final): **exit 0** (2ª rodada; o GRAVE "Failed to export metrics to 127.0.0.1:14318" durante o run é o fail-soft esperado do teste do starter sem sink, não falha).
- **Prepush gate: FAIL honesto** — 1ª rodada: 68 findings; split **corrigido**: **10 no escopo desta missão** (vite 5.4.21 — 8 GHSAs, 1 HIGH `GHSA-587h-7wmj-h5pm`; vitest 2.1.9 — 2 GHSAs, 1 CRITICAL `GHSA-82fw-gwwq-j7x9`; severidades e faixas via fonte primária OSV `api.osv.dev/v1/vulns/<id>`, 2026-11-11. O "11º" contado antes era `GHSA-3pq3-5fj3-cg6v` de **axios** — pre-existing) e o restante pre-existing de outros pontos do workspace (axios/pypdf/certifi — fora do diff). Explorabilidade real dos pins antigos: nula no uso (projeto roda só `vite build` + `vitest run`; vetores são `vite dev`, `vitest --ui`/mocker API). **Re-run pós-fixes F1–F6: 56 findings, ZERO vite/vitest — escopo in-scope zerado.** Os 56 são pre-existing de outros pontos do workspace; `tinypool@1.1.1` (2 CRITICAL, fixed ≥2.1.1/2.1.2 no OSV) rastreado ao lockfile de `10_projetos_estruturantes/ai-engineer-rpg` (outra missão; o lock deste projeto não contém tinypool).
- **The-Judge local (degradado — sem PR/gh; `scripts/review_gate.py` ausente do pacote local, regras do gate aplicadas manualmente): veredito COMMENT**, 6 findings, todos 🟡 should-fix: F1 duplicação do registro de fronteira no poll live (dashboard/main.ts:213 + devtools/JsonlStore.java:119); F2 dashboard live sem `Authorization` quando `OTELTELEMETRY_SINK_TOKEN` configurado (main.ts:216 — UI é servida sem auth, modo live fica vazio em silêncio); F3 chamada morta `forEach(() => undefined)` (loader.ts:145); F4 modo arquivo multi-input last-wins (main.ts:243); F5 round-trip de header trunca valor com vírgula (core/ConfigResolver.java:154/191); F6 pins vite/vitest com advisory (OSV). Registro completo: `C:\Users\paulo\AppData\Local\Temp\opencode\judge\findings.json`.
- Scan determinístico de bypasses (74 arquivos do projeto): **0 supressões reais** (TODO = "Todos" em português; `.skip` dentro do bundle uPlot gerado; `as any` em fronteira de parse JSON com narrowing; `Thread.sleep` em gerador de carga de exemplo).
- **Fechamento (2026-11-11, pós-fixes + walks)**: `mvnw verify` com F1–F6 + C25 presence-scan + `demo.mjs` com spans + overlay fix: **exit 0** (rodada final, commando `FINAL-VERIFY=0`). Dashboard: vitest 4.1.12 — 2/2; `npm audit` 0 vulnerabilidades; bundle `dashboard.js` + `style.css` revalidados no sink vivo. Sinks parados; nenhum processo residual.
