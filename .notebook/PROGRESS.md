# Arquitetura cloud: pesquisa AWS/Azure, MCPs e modelos AWS (MyDigitalBuddy, AIHealthResearch) — 2026-11-14

# TLC spec versions — publicação e merge

Updated: 2026-10-26. Entry point: `.notebook/tlc-spec-versions.md`.
- [x] Fontes exatas, quatro pacotes e hashes locais verificados.
- [x] Checkout isolado da master remota preserva alterações locais de outras tarefas.
- [~] Gates do candidato, PR, merge autorizado e monitoramento do SHA final.
- [ ] Concluir somente com workflows/checks do SHA final terminais e verdes.

---

# Missão ativa: agendamento obrigatório nos Studios
Updated: 2026-10-14
Entry point: E:/Github/ai-assistent-universal-coder/.work/studio-scheduling/PROGRESS.md


Updated: 2026-11-14. Entry point: `cloud-architecture-mcp/README.md`. Evidence: `.work/cloud-research/` (fora do git: claims, triagem JEV run1/run2, snapshots de preço, scripts). Decisões e modelos: `cloud-architecture/README.md`.

## Checklist

- [x] BRIEFING: objetivo, escopo e critérios de aceite fixados. Restrições: sem deploy na nuvem, sem commit, chave JEV só pelo cliente do `workspace-brain` (sem impressão), sem dado do AIHealthResearch enviado ao JEV.
- [x] RECON: notebook lido; CloudFormation real do AIHealthResearch (`infra/foundation.json`, `workloads.json`, `render_stack.py`) e docs (ARCHITECTURE, PRODUCTION_PLAN, THREAT_MODEL) lidos; MyDigitalBuddy lido (`Cargo.toml` sem crate HTTP, CI, README, PRIVACIDADE); APIs locais mapeadas (FastAPI em AIHealthResearch 30+ rotas com SSE, `model_server` `/ping` `/invocations`, `rag-graph-laya-mcp/app/web.py` 4 rotas, sink OTLP `/v1/*` e `/api/*`).
- [x] PESQUISA AWS: fatos verificados na documentação oficial (App Runner fechado a novos clientes; ECS Express Mode sem custo extra e ALB interno com sub-redes privadas; Aurora Serverless v2 com 0 ACU; cobrança de VPC endpoint por AZ e hora; CloudFront PriceClass_100/200 sem América do Sul; S3 Vectors GA; OpenSearch com 3 dedicated masters; SageMaker async com scale-to-zero, Managed Spot até 90% com checkpoint; Compute Savings Plans cobrem Fargate/Lambda; OTLP do CloudWatch; OIDC para GitHub; Well-Architected com 6 pilares).
- [x] PESQUISA AZURE: Microsoft Learn (WAF com 5 pilares; Container Apps escala a zero exceto por CPU/memória; PostgreSQL Flexible com HA zonal bloqueado em Brazil South para novos servidores e sem backup geo-redundante; AI Search híbrido com RRF; Blob WORM; endpoint online do ML sem escala-zero documentada; Monitor OTel com distro Java; Retail Prices API sem autenticação); Artifact Signing (sem validação pública para indivíduos no Brasil); Azure MCP oficial em `microsoft/mcp` (v3.0.0).
- [x] PREÇOS: snapshot AWS pela Price List pública (sem credenciais; 327 SKUs; SHA-256 por arquivo) para sa-east-1 e us-east-1; snapshot Azure pela Retail Prices API (brazilsouth e eastus). Lacunas registradas como não verificadas: NAT, KMS, CloudFront, Cognito, Lambda, armazenamento de logs.
- [x] JEV: 65 claims (50 positivos, 15 controles negativos/ausência), Noul via cliente do `workspace-brain`. Rodada 1: positivos 43/50, negativos 15/15. Seis trechos foram corrigidos para verbatim (pergunta inalterada), rodada 2: positivos 48/50, negativos 15/15. Dois casos limítrofes verificados à mão. Evidência: `.work/cloud-research/evidence/jev-triage-run1.json` e `jev-triage.json`.
- [x] MCPs: `cloud-architecture-mcp/` com servidor AWS e servidor Azure (JSON-RPC stdio sem dependências; ferramentas: listar/obter padrões e armadilhas, revisar arquitetura, mapear API local, estimar custo mensal).
- [x] TESTES: unidade do motor, protocolo stdio, regressão de cada armadilha aprendida, mapeamento das APIs locais (AIHealthResearch, sink OTLP, rag-graph-laya, workers e desktop).
- [x] MODELOS AWS: `cloud-architecture/` com arquitetura exclusiva do MyDigitalBuddy (distribuição estática, sem backend, sem telemetria) e do AIHealthResearch (contas separadas, cenário as-is do CFN e cenário otimizado), com custo reproduzível.
- [x] HARNESS workspace-brain: `learn` de erros e aprendizados, depois `search` por consulta natural para medir se cada erro volta ao recuperar (recall do aprendizado).
- [x] VERIFY: suíte `node --test` verde, custo reproduzido pelo MCP igual ao cálculo do script, JEV e dossiê consistentes.
- [ ] DEBRIEF: HANDOFF, MEMORY, LEARNING, INDEX e nota nova; relato final com riscos.

## Achados que mudam o desenho (verificados)

- AIHealthResearch: a inferência SageMaker do CFN fica com `InitialInstanceCount: 2` sempre ligado e `ModelInstanceType` sem padrão; com `ml.g5.xlarge` em sa-east-1 isso custa cerca de US$ 3,5 mil/mês só em endpoint. Evidência: `02_repositorios/AIHealthResearch/infra/workloads.json` (EndpointConfig) e `infra/render_stack.py` (`ModelInstanceType`).
- AIHealthResearch: 9 VPC endpoints de interface × 2 AZ custam cerca de US$ 276/mês só em hora em sa-east-1 (US$ 0,021/h por endpoint por AZ), antes de dados. Evidência: `infra/render_stack.py` (loop de endpoints) e preço AmazonVPC sa-east-1.
- AIHealthResearch: a Lambda `Fetcher` roda fora da VPC (sem `VpcConfig`) e tem saída pública; os demais workers estão em sub-redes privadas sem NAT. Desenho coerente, mas precisa ser explícito no modelo.
- AIHealthResearch: o `ModelInstanceType` e a escolha de tipo de instância precisam de decisão; o projeto proíbe endpoints externos de LLM, então Bedrock fica fora (ARCHITECTURE.md, regra 1).
- MyDigitalBuddy: app desktop Rust sem crate HTTP e sem telemetria (`Cargo.toml`, README). Não há runtime de nuvem a modelar; a arquitetura AWS é só distribuição e CI.
- Segunda cópia do AIHealthResearch em `E:\Github\AIHealthResearch` (existe; não é a referenciada pelo usuário). Usei `02_repositorios/AIHealthResearch` (HEAD `5878719f`, árvore limpa).

## Working set

- `.work/cloud-research/` (evidência, fora do git), `cloud-architecture-mcp/` (novo), `cloud-architecture/` (novo). Nenhum arquivo dos repositórios em `02_repositorios/` foi alterado.

## Verificação (2026-11-14)

- `node --test` em `cloud-architecture-mcp/`: 39 de 39 verdes (conhecimento íntegro, 27 armadilhas de regra, cálculo de custo, protocolo stdio real).
- `node --test` em `cloud-architecture/`: 16 de 16 verdes (mapeamento das 8 APIs locais nos dois provedores, totais de custo dos modelos, e conferência de que cada fonte existe).
- Inventário ampliado após a varredura de rotas em segundo plano (concluída com código 0): `science-studio/integration/dark_api.py` (5 rotas) e `rag-graph-laya-mcp/model_server.py` (5 rotas) entraram em `cloud-architecture/local-apis.json`. Excluído: `live-server.mjs` da skill de design (ferramenta de desenvolvimento, não serviço de produção). Lição registrada: inventário por caminhos escolhidos à mão deixou duas APIs de fora.
- Custo reproduzido por Python independente (`.work/cloud-research/verify_costs.py`): as-is US$ 6.046,85; alvo US$ 2.735,52 (diferença de até US$ 0,01); economia de 54,8%.
- Harness de memória (`.work/cloud-research/brain_learn_and_eval.py`): 30 entradas gravadas no `workspace-brain` (mais 1 erro de inventário gravado depois da varredura: 31 no total), recall@3 = 1,0 em 20 consultas, escritas pelo mesmo agente (não independente).
- JEV: rodada 1 positivos 43/50, rodada final 48/50; negativos e ausência 15/15 nas duas. Triagem, não prova.
- Varredura de credenciais em `.work/cloud-research` e nas pastas novas: sem chave; o cliente do `workspace-brain` lê a chave só em memória e não é chamado com a chave impressa.
- Pendências que não foram verificadas: ver `cloud-architecture/README.md` (decisões do dono e preços não extraídos).

---

# Biblioteca de telemetria OTel Java (otel-telemetry-java) — 2026-11-10

Updated: 2026-11-11. Entry point: `10_projetos_estruturantes/otel-telemetry-java/pom.xml`. Evidence: `10_projetos_estruturantes/otel-telemetry-java/.specs/features/otel-telemetry-java/{plan,checks}.md`; plano v3 aprovado na conversa (The-Judge: REQUEST_CHANGES → ajustado; The-Fool: SEGUIR COM AJUSTE).

## Checklist

- [x] PLAN: plano v3 fechado com owner — toolchain JDK 25.0.5+8, artefato `--release 21`, Maven wrapper, presets multilíngue (Python/Node/.NET/Go/Rust), sink offline + dashboard, local `10_projetos_estruturantes/`; findings J-F1..J-F7 aplicados.
- [x] F0 spec-lean: `STATE.md` + `plan.md` + `checks.md`; gates `validate_plan` 0/0 e `validate_checks` 0/0 (27 checks, mutações 3, 3 doors).
- [x] F1 toolchain+core: JDK 25.0.5+8 (zip + sha256 `636bdc13…`) e Maven 3.9.16 em `.tools/` (gitignored); scaffold 7 módulos + `mvnw` (only-script); `mvnw test -pl otel-telemetry-core` verde 10/10 exit 0 (C1,C2,C3,C4,C8) em 2026-11-11. Lição: `InMemorySpanExporter.shutdown()` limpa a lista upstream → asserções pós-shutdown exigem `RecordingSpanExporter` próprio; yaml usa namespace `exporter.otlp.*` normalizado para chaves internas.
- [x] F2 exporters: `OtlpRuntimeProvider` via `META-INF/services` + `Presets`/`ExporterSpec`/`ExporterFactory`; `PresetEndpointTest` 10/10 (C5,C6,C7) exit 0. Jars reais checados (1.68.0): grpc em `otlp.{trace,metrics,logs}`, http em `otlp.http.{trace,metrics,logs}` (logs plural), `setHeaders(Supplier<Map>)`.
- [x] F3 adapters+starter: `Adapters` (appender Logback anexo programático — `install()` upstream só configura appenders já declarados em XML; bridge Micrometer `create`), `OtelTelemetryAutoConfiguration` + properties record; LogbackExportTest/MicrometerBridgeTest/StarterAutoConfigTest 4/4 exit 0 (C9,C10,C11,C12). Descobertas: bridge usa `DoubleCounter` → tipo DOUBLE_SUM (`getLongSumData()` devolve empty); `InMemoryMetricReader` mudou para `sdk.testing.exporter`; micrometer-core/logback-classic são compileOnly upstream (pinados 1.17.2/1.5.38); Boot 4: `AutoConfigurations` em `boot.autoconfigure`, sem `withAutoConfiguration()`.
- [x] F4 devtools: `OtlpSinkServer` (JDK HttpServer) + `JsonlStore` (rotação por tamanho/idade, teto de arquivos) + `SinkConfig` (env OTELTELEMETRY_SINK_*) + `SinkMain`; devtools 11/11 exit 0 (C13,C14,C15,C16,C17,C18,C19,C26,C27). Lições: `JsonFormat.printer()` é pretty-print → JSONL exige `omittingInsignificantWhitespace()`; `InvalidProtocolBufferException` estende `IOException` → catch específico (400) ANTES do genérico (500); proto 1.11.1-alpha: `SeverityNumber` é enum top-level em `logs.v1` (não aninhado em LogRecord).
- [x] F5 dashboard: projeto `otel-telemetry-devtools/dashboard/` (Vite 5.4.21 lib-mode iife + uPlot 1.6.32, Vitest 2.1.9); loader puro com cap MAX_RECORDS=5000 (janela deslizante mantém recentes); `capsLoadedWindow` 2/2 vitest exit 0 (C22); `npm run build` → `src/main/resources/dashboard/{index.html,dashboard.js,style.css}` com caminhos relativos + script defer clássico; smoke do sink: `/`, `/dashboard.js`, `/style.css`, `/api/health` todos 200 (fix: `resourceFor` mapeia `/style.css` → `dashboard/style.css` no classpath). Walks C20/C21 executados em 2026-11-11 (ver item de walks).
- [x] F6 presets+examples: `presets-multilingue/{README.md,node/demo.mjs}` (5 linguagens, Rust experimental, status J1 honesto); `otel-telemetry-example-java` `Main` (1 linha + carga) + `BootstrapSmokeTest` 1/1 (C25 — stub JDK HttpServer captura protobuf, parse após shutdown); exemplo Spring (`Application`+`HelloController`+properties offline, dep adapters adicionada) compila; `README.md` do projeto com tabela de status de verificação.
- [x] F7 verify: `mvnw verify` reactor completo **exit 0 duas vezes** (última no estado final pós-reversão; GRAVE "Failed to export metrics 127.0.0.1:14318" é o fail-soft esperado do starter sem sink). Mutações: M1 precedência **MORTA** (`syspropOverridesYaml`); M2 rotação maxFiles **SOBREVIVEU** → `rotationHonorsCeilings` fortalecido (25 appends, teto 512 B, cascata até traces.3.jsonl) → **MORTA**; M3 1ª tentativa INVÁLIDA (unreachable statement não compila) → corrigida p/ `SinkConfig.authRequired()→false` → **MORTA** (`missingTokenReturns403` + `loopbackDefaultAndOverrides`); todas revertidas, core+devtools re-verdes. Prepush: **FAIL** honesto — 68 CVEs, **11 no escopo** (pins vite 5.4.21 / vitest 2.1.9 desta missão; OSV 2026-11-11: 1 CRITICAL `GHSA-5xrq-8626-4rwp` + 1 HIGH `GHSA-587h-7wmj-h5pm`; vetores = dev server/UI, não executados), resto pre-existing (axios/pypdf/certifi, outros pontos do workspace). The-Judge local (degradado, sem PR/gh): **COMMENT**, 6 findings 🟡 — F1 duplicação do registro de fronteira no poll live (main.ts:213 + JsonlStore.java:119), F2 dashboard live sem `Authorization` com token (main.ts:216), F3 `forEach(() => undefined)` morto (loader.ts:145), F4 multi-arquivo last-wins (main.ts:243), F5 round-trip de header trunca valor com vírgula (ConfigResolver.java:154/191), F6 pins com advisory — registro em `C:\Users\paulo\AppData\Local\Temp\opencode\judge\findings.json`; `review_gate.py` ausente no pacote local → regras do gate aplicadas manualmente. Commit executado em 2026-11-11 após fixes/walks (ver itens abaixo).
- [x] Fixes F1–F6 (owner: "siga do 1 ao 3", 2026-11-11): F1 dedup client-side por `recordKey` em `mergeNew` (span `traceId:spanId`; log `timeNs||timeMs:message`; metric `name:last timeMs:value`); F2 `apiFetch` com `Authorization: Bearer` + `window.prompt` no 1º 403 (reenvio único); F3 código morto removido; F4 `ingestFiles` acumula o lote + MESMO dedup no modo arquivo (arquivos rotacionados se sobrepõem); F5 headers do builder ficam `Map<Signal,Map>` (`builderHeadersBySignal`) até o fim do `resolve()`, `encodeHeaders` removido + teste `builderHeaderValueWithCommaSurvives` (core 11/11); F6 pins **vite 6.4.6/vitest 4.1.12** (OSV: 6.4.4 fecha os 8 GHSAs de vite; vitest exige ≥4.1.11 pelo GHSA-82fw; peer/engines ok com Node 24) + `cssFileName: 'style'` (Vite 6 default CSS virou o nome do pacote → contrato `style.css` restaurado). C25 flake fixado: `BootstrapSmokeTest` presence-scan (`smokeCounterExported`) — self-métrica `otel.sdk.metric_reader.collection.duration` podia preceder `smoke.counter` no lote de shutdown (flake 2/3 observado; 5× rerun verde). `mvnw verify` FINAL exit 0.
- [x] Walks (owner pediu execução, 2026-11-11; playwright como pacote Python + chromium-1243): **C20 PASS** (10 spans → 3 abas → fronteira → 11 → servidor re-envia 1 item filtro `>=` → 3 polls em repouso estável 11 = prova do F1; `c20-live.png`); **C21 PASS** (file:// "modo arquivo"; 2 arquivos → 11 registros com `demo.round` E `walk.span.idle`, não last-wins = prova do F4; `c21-file.png`); **C23 PASS** (demo.mjs corrigido para emitir spans reais via `trace.getTracer` + `@opentelemetry/api` — antes NADA era exportado; rodado em scratch FORA do repo; 10 spans → `traces.jsonl` → `/api/traces` retorna `demo.round`); **C24 PASS** (README 5 linguagens percorrido; 2 defeitos doc corrigidos: path `otel-telemetry-examples/` + classpath two-step provado + nota scratch + data); **F2 walk PASS** (sink com `OTELTELEMETRY_SINK_TOKEN=walk-token-123`: 1 prompt → 11 spans). Três bugs reais achados pelos walks: overlay `#drop-overlay{display:flex}` vence o `[hidden]` do UA e bloqueava TODOS os cliques (fix CSS); demo sem spans; flake C25. Screenshots/scripts em `C:\Users\paulo\AppData\Local\Temp\opencode\c23walk\`.
- [x] Commit autorizado (owner: "siga do 1 ao 3", passo 3): **f821fcd2** `feat(otel-telemetry-java): add OTel telemetry library with offline sink and dashboard` — 74 arquivos, 6972 inserções, escopo só do diretório do projeto (`.notebook/` fora; dry-run conferido: sem `node_modules/target/cp.txt`). Prepush re-run: **56 findings, ZERO vite/vitest — in-scope zerado**; contagem corrigida 11→10 (o "11º" era `GHSA-3pq3` de axios, pre-existing); `tinypool@1.1.1` (2 CRITICAL) rastreado ao lock de `ai-engineer-rpg`, outra missão.

---

# RPG Engenharia de IA (ai-engineer-rpg) — 2026-11-11

Updated: 2026-11-11. Entry point: `10_projetos_estruturantes/ai-engineer-rpg/package.json` (scripts build/test). Evidence: `10_projetos_estruturantes/ai-engineer-rpg/.specs/features/ai-rpg-engineer/{plan.md,checks.md,verification.md}`.

## Checklist

- [x] BRIEFING/RECON: plano aprovado (`C:\Users\paulo\.opencode\plan\ai-engineer-rpg-web.md`), quarteto lido, projeto aditivo isolado em `10_projetos_estruturantes/ai-engineer-rpg/`; nenhum arquivo alheio tocado.
- [x] Conteúdo completo v1.0.0: 7 reinos (40 lições, 40 missões, 127 questões, 31 fontes JEV, 50 termos); realm2/4/5/6 reescritos após varredura de corrupção; `validateContentPack(pack)` 0 erros.
- [x] Engine + store + UI: `economy/d20/progress/capstone/certificate/persistence/gameStore` + HUD, MapView, MissionView, CapstoneView, CertificateView, GlossaryView, GuildaView.
- [x] Suíte: 55/55 verdes em 7 arquivos vitest (economy 9, d20 8, capstone 8, progress 5, pack 8, certificate 6, store 11); `tsc --noEmit` limpo.
- [x] Portões spec-lean: `validate_plan` 0 erros/0 warnings; `validate_checks` 0 erros/1 warning esperado (proof do `Build:` é comando, não suíte).
- [x] Mutações 3/3 mortas e revertidas: M1 `HINT_COST=90` (4 falhas), M2 `D20_THRESHOLD=16` (1 falha), M3 peso cap-arq `0.17` (3 falhas); após reverter, suíte de volta a 55/55.
- [x] Build: `npm run build` ok (tsc + vite, 252 módulos; aviso de chunk 719 kB > 500 kB, não erro).
- [x] `verification.md` registrado no projeto com portões, mutações e findings.
- [x] Correção do owner: jogo abrível sem npm — build file://-friendly (formato iife + plugin pós-build: tag clássica `defer` em vez de module; CSS embutido no chunk); 2ª rodada corrigiu página branca (script clássico no `<head>` sem defer rodava antes de `#root`); plan/checks/verification atualizados; suíte 55/55.
- [x] Expansão v1.1.0 (pedido do owner "algo bem completo"): 8 lições/reino (l6/l7 novas por domínio + l8 síntese), 8 missões/reino (chefão movido de `rN-m6` para `rN-m8`, títulos preservados), 33 questões/reino (total 231), 51 fontes JEV (21 novas), glossário 78 termos (52 corrigidos + 26 novos); realm0 exemplar reescrito + 6 subagentes paralelos para r1–r6 (r2/r5 "falharam" só no relatório final após completar os writes — qualidade conferida por leitura); pesos JEV, BLURB e tiers intocados.
- [x] Verificação da expansão: `tsc --noEmit` limpo (2×), `vitest run` 55/55 (2×, última pós-edições), build ok (252 módulos, chunk 867.65 kB), `dist/index.html` standalone (`defer`) conferido, varreduras de corrupção/EN zero (CJK, tailandês, cirílico, `Ã`, `\u00`, EN amplo); correções: hint r3 EN → PT-BR, r4 `Braço de Mar`, `pack.ts` 1.1.0.
- [x] Revisão de questões (pedido do owner, 2026-11-11): painel recolhível "✅ Respondidas nesta missão" em `src/ui/MissionView.tsx` — enunciado, correta destacada, explicação, selo via (acerto/D20), dica se comprada; abre por padrão ao entrar em missão já completa; só UI (engine/store/schema/pack intocados). Suíte 55/55; build ok (chunk `index-B3ax5_yR.js`, 868.82 kB); `dist-standalone-v110` renovada.
- [x] Profundidade de ensino v1.2.0 (pedido do owner "conteúdo raso antes das questões", 2026-11-11): cada lição l1–l7 dos 7 reinos ganhou 3 parágrafos appended — "As fórmulas na mesa:" (notação plana unicode), "Exemplo resolvido com números:" (contas conferidas dígito a dígito, espelhando as questões da própria missão) e "Pegadinhas que a mesa adora:" (distratores explicados); lição l8 (síntese) ganhou 2 ("Plano de revisão guiado pelo chefão:" + "Ritual da mesa"). Parágrafos existentes preservados; questões/missões/fontes/pesos JEV/BLURB/tiers intocados. Exemplar realm0 na sessão principal; r1–r6 via subagentes (r1 retomado após "Free usage limit" parcial na l1 — verificável por leitura; r2–r6 1ª leva: r5/r6 ok, r2/r3/r4 na retomada).
- [x] Dicionário + tooltips v1.2.0: `GlossaryTerm` com `formula?`/`example?`; glossário 82 termos (52 base + 28 expansão + g-l1/g-l2 novos); fragmentos por reino em `src/content/dictionary/realm0..6.ts` (82 fills sem sobreposição: 12/10/14/11/18/12/5) mesclados por `dictionary/index.ts` → `glossary = baseGlossary.map(...)`; conferência node: 82 ids ↔ 82 fills, 0 missing/dup/extra; aba "Glossário" renomeada "Dicionário" (`HUD.tsx`, tab id interno intacto) e `GlossaryView` reescrita com fórmula+exemplo; tooltip CSS puro `.tip-card` no hover/foco dos termos das lições (`MissionView.tsx`), `title` nativo removido.
- [x] Verificação v1.2.0: `tsc --noEmit` limpo; `vitest run` 55/55; portões spec-lean PASS (0/0 + 0 erros/1 warning); build ok (260 módulos, chunk `index-BEUga6XB.js`, 1008.21 kB); varreduras de corrupção/EN zero (único `Ã` = "NÃO" legítimo em economy.ts pré-existente); `dist-standalone-v110` renovada (byte-cópia do dist v1.2.0).
- [!] Gate formal `check_proofs.py`/`validate_verification.py`: exige `proofs.md` sobre commit HEAD limpo; bloqueado pela política de não commit da sessão. Pendente autorização do owner.
- [ ] Commit: não feito (política do owner nesta sessão); mudança fica na working-copy do projeto novo.

---

# Portão antes do push — 2026-11-09

Updated: 2026-11-09. Entry point: `quality/prepush/prepush.py`. Evidence: `quality/prepush/tests/test_prepush.py`; `.aeos/prepush/report.json`.

## Checklist

- [x] RECON: workflows de universal-coder, AIHealthResearch, MyDigitalBuddy, iDentifyer, pdfcraft, FreePDFReader, laya, Engenharia-Reversa, ibunny e DiabeticsresearchJEV. OSV só no MyDigitalBuddy; Bandit/pip-audit no AIHealthResearch; CodeQL citado na skill e ausente no workflow.
- [x] Seis backends com falha fechada se a fonte não atualizar: OSV, bibliotecas, linguagem, PE, SAST, segurança estática.
- [x] Testes de contrato: 15 OK, sem rede.
- [x] Corrida real em 2026-11-09: `fail` com export OSV do mesmo dia. CVE, bibliotecas e linguagem reprovam. SAST, segurança e EXE de aplicação passam depois de excluir `.venv` e `.state`.
- [x] Hook local instalado em `.git/hooks/pre-push`. Workflow `prepush-gate.yml` chama o mesmo comando.
- [ ] O repositório ainda não passa no portão. Próximo passo é atualizar pins/ciclos ou registrar exceção com data. Commit não autorizado.

---

# Padrão DO NOT INVENT / NUNCA INVENTE — 2026-11-09

Updated: 2026-11-09. Entry point: `00_skills/do-not-invent.manifest.json`. Evidence: `00_skills/validation.report.json` (PASS, 0 erros, `do_not_invent: 46`), `00_skills/VERIFICATION.md`.

## Checklist

- [x] RECON: regra localizada no original (backup) em 46 skills, na descrição e/ou no corpo. A compactação removeu a cláusula de 11 descrições (validador em vermelho) e reduziu outras 3 (`simulator-ai`, `continuity-bootstrapper`, `anti-hallucination-evaluator`).
- [x] Registro: `do-not-invent.manifest.json`, com a cláusula literal de cada skill e as formas aceitas para a descrição.
- [x] Validador: `validate-workspace.py` aceita as formas do padrão como limite negativo e reprova cláusula registrada ausente. Teste em vermelho antes da restauração: 11 erros, exatamente as skills esperadas.
- [x] Restauração: 14 descrições reescritas com a cláusula literal dentro de 150 caracteres (`build_final.py`, MANUAL3). `sync.py` passou a gravar também o frontmatter canônico.
- [x] Prova ponta a ponta (`acceptance_test.py`): o architect reprova `Never invent facts.`; o validador do workspace aceita.
- [x] Gate: validador PASS, 0 erros, 78 avisos sem alteração; `verify.py` com 1.207 checagens OK e 0 falhas; retenção 0 perdas.
- [x] Decisão do owner (2026-11-09): aceitação da forma só no validador do workspace; o architect upstream (pinado) permanece inalterado.
- [x] Decisão do owner (2026-11-09): registro cobre só o `SKILL.md`. Módulos `references/` (ex.: `usage-and-verification.md`, com "Never invent data…") ficam fora do registro e não foram alterados.
- [ ] Pendente: incluir skills novas no padrão exige registro manual da cláusula literal.

---

# Reestruturação das skills (formato enxuto) — 2026-11-09

Updated: 2026-11-09. Entry point: `00_skills/STANDARD.md` (seção "Formato enxuto"). Evidence: `00_skills/validation.report.json`, `00_skills/VERIFICATION.md`; backup e medições em `.tools/skill-restructure/` (ignorado pelo git).

## Checklist

- [x] BRIEFING e RECON: `.notebook` lido; superfícies mapeadas (canônico `00_skills`, nativo `.agents/skills`, compat `skills/`, `.codex/skills`); validador em FAIL com 18 erros antes de qualquer edição.
- [x] Defeitos corrigidos: BOM removido de 3 SKILL.md; mojibake em `documentary-adversarial-judge`; 13 digests stale ressincronizados. Gate: validador sem erros.
- [x] Backup completo antes de escrever: 881 arquivos com manifesto de hashes.
- [x] Descrições: 324 reescritas para até 150 caracteres, com gatilho e exclusão. Cláusulas de segurança restauradas (aprovação, escopo autorizado, checks não executados, mutação de sistemas vivos). Gate: `check_desc.py` sem falhas.
- [x] Corpo: governança em uma linha, ponteiros de proveniência unidos, preâmbulo e condições de roteamento encurtados, `## Response` acrescentado. Gate: máximo 99 linhas, 2.980 links preservados.
- [x] Propagação: catálogo, registro, INDEX (324), ponteiros nativos (328), compat (217) e codex (10). Gate: `verify.py` com 1.207 checagens OK e 0 falhas.
- [x] Fonte importada `(design)/impeccable` mantida byte a byte por proveniência (primeira tentativa quebrou o pin de hash e foi revertida).
- [x] Retenção: 0 tokens operacionais do original ausentes; avisos do architect sem perda de marcador de exemplo ou erro.
- [x] Template `SKILL.template.md` em formato enxuto (150 → 45 linhas), com hash atualizado no `MANIFEST.json` da skill-factory.
- [x] STANDARD ganhou a seção "Formato enxuto"; VERIFICATION ganhou a seção 2026-11-09 e a afirmação antiga "zero avisos" foi corrigida.
- [x] Relatório oficial regenerado: PASS, 0 erros, 78 avisos (76 pré-existentes e 2 heurísticos do `studio-creation-tlc` recém-registrado: exemplos e tratamento de erro no corpo).
- [!] Medição de tokens de saída em execução real: não feita. O ganho de resposta é estrutural até haver amostra de uso.
- [x] Decisão do owner (2026-11-09): `studio-creation-tlc` registrado no catálogo e no registro (`risk_level` high, por bloquear envio de mídia); ponteiros sincronizados.
- [x] Decisão do owner (2026-11-09): roteamento repetido no corpo removido por frase, com revisão de decisões. 53 corpos alterados; roteamento duplicado 12.523 → 838 caracteres; conteúdo operativo mantido, pois é a única cópia após a descrição ficar curta.
- [x] Commit: não feito, por decisão do owner. A árvore já tinha ~300 pendências pré-existentes; nenhum reset foi feito.

---

# Cérebro do workspace (workspace-brain) — 2026-11-08

Updated: 2026-11-08. Entry point: `E:\Github\workspace-brain\README.md`. Evidence: `.work/workspace-brain/evidence/`.

## Checklist

- [x] BRIEFING e RECON: `.notebook` lido; skills de governança lidas; API do JEV lida no OpenAPI; chave validada com `GET /v1/models` sem exibir valor.
- [x] Conflito de governança registrado: delegação a subagentes proibida por AGENTS.md e spec-driven. Cada skill roda como lente sequencial, auto-verificada.
- [x] Spec: `workspace-brain/spec.md`, `design.md`, `tasks.md` validados por `validate_spec.py` e `validate_tasks.py`. Gate de fechamento passou.
- [x] Spec leve: `dark-channel-discovery/plan.md` e `checks.md` validados por `validate_plan.py` e `validate_checks.py`.
- [x] TDD vermelho registrado em `tdd-red-run.txt`; implementação posterior e testes verdes.
- [x] Implementação: 46 testes unittest OK; build gate (compileall) OK.
- [x] Mutation checks: 3 de 3 detectados; arquivos restaurados com hash idêntico.
- [x] Run ao vivo: discovery v1 (zerou 2 capacidades) e v2 (amendment A1); judge 55 de 55; coverage 5 de 5; clone 6 shallow; checkpoints 6 com re-scan idêntico.
- [x] Provas C1 a C7 do dark-channel-discovery OK.
- [x] Revisões: the-judge (COMMENT) e the-fool (SEGUIR COM AJUSTE), ambas lentes sequenciais.
- [x] Ingestão: 520 documentos (notas, mapeamentos, docs de 20 repositórios); 8 aprendizados registrados.
- [!] Pesos: nenhum peso registrado ou aprovado. Bloqueado por ausência de avaliação medida ≥ 9,0 (gate ativo, fail closed).
- [x] Medição do gate com projetos de canal dark (protocolo pré-registrado): 35 repositórios, veredito INCONCLUSIVO (amostra < 40). Evidência v1: `.work/workspace-brain/evidence/dark-channel-eval/eval-summary.v1-silver.md`.
- [x] Auditoria dos 2 FP e 13 FN (pedida pelo owner; feita pelo agente, não independente): 3 rótulos mudaram (FP raunakpatil para 1; Hao0321 para nulo; Agents365 para 0). v1 auditada: precisão 0,981, recall 0,825, ainda inconclusiva por tamanho. Bloco `audit` em `labels.json`; antes em `labels.v1-silver.json`.
- [x] Emenda A2 declarada antes da execução e amostra ampliada para 45 repositórios (10 novos; rótulos fixados antes do JEV; JEV só nos novos). Veredito PASS pela regra: precisão 0,984 [0,917; 0,997], 64 aprovações, recall 0,768. Evidência: `.work/workspace-brain/evidence/dark-channel-eval/eval-summary.md`.
- [!] Ressalvas do pass: miniatura com precisão 0,833 (não passa por capacidade); 6 zeros automáticos de miniatura podem ser positivos fora da janela de 3000 caracteres; aprovações verdadeiras não auditadas; ampliação decidida após ver o v1.
- [ ] Owner valida os rótulos auditados e os 10 novos; decide se o pass sustenta decisão, a pergunta de miniatura e a janela de 3000 caracteres.
- [x] Conhecimento da medição gravado no brain (RAG): `ingest-notes` e 14 registros (5 decisões, 5 aprendizados, 3 erros, 1 sucesso); gravação idempotente; 14 de 14 recuperados no topo da busca. Evidência: `.work/workspace-brain/evidence/knowledge-2026-11-08/knowledge-report.json`.
- [!] Licenças `NOASSERTION` em `index-tts` e `edge-tts`: verificar antes de qualquer reuso.
- [ ] Servidor MCP para o brain (próxima etapa; acesso atual via CLI e `.notebook`).
- [ ] Recall com embeddings, se BM25 faltar em perguntas com sinônimos.
- [ ] Commit e push: não autorizados nesta missão.
# Produção real: "Buracos Negros" 90 min dentro do dark-videos — 2026-11-09

Updated: 2026-11-09 (tarde). Entry point: `D:\Git\dark-videos\.work\buraco-negro-90min\`. Objetivo: 90 min 100% IA com VÍDEO REAL (ESO/NASA) e vídeo de direção nova após rejeição do estilo cartoon pelo operador. Pasta do projeto foi esvaziada externamente (~17h14): sobreviveu só `assets/real/` + `assets/inspect/`; roteiro e demais reconstruídos.

## Checklist
- [x] Fumaça SDXL: descartada (direção nova = somente material real/3D fotorrealista).
- [x] Acervo real (assets/real/, 26 clipes; inspeção visual em 15 folhas): ACEITOS 7 — eso1907d/e/f-hd, eso2208-eht-mwb/mwi/mwg-hd (1080p25 CC BY 4.0 ESO) + nasa-smbh-simulacao (720p30, 133,4 s); REJEITADOS os demais (texto/rótulos/logos/escuro/resolução baixa).
- [x] Sondagens de contrato refeitas pós-limpeza: render/validate/review/export, gates 1–5, context_gate 'named', voice_kokoro, music_gen, audio_mix.
- [x] Pipeline alternativa: real_assets.py (Temp) — codifica 180 camadas kind=video (bg 1920×1080 scale 1.08; fg 960×540 scale 0.5 canto inferior), `-t 59.98`, fps 30, slowdown/crop/offset determinísticos por cena (reuso com variação homologado), nome com tokens da cena própria (GATE 3 'named'); ledger assets/video-source-ledger.json.
- [x] GATE 2 reparado para vídeo: ffmpeg 9.0.2 removeu `-vsync`; cópia do assetguard com `-fps_mode` compilada em Temp (`assetguard-fpsmode\target\release\assetguard.exe`), binário canônico do repo intacto; `ASSETGUARD_BIN` como override. Detect: clean 1,0 em eso1907f-hd.
- [x] sources.json reconstruído (21 fontes; clipes re-pointados para cdn.eso.org verificado 200; LIGO validado com ctx unverified — proxy MITM local; Einstein trocado para enciclopédia acessível).
- [x] music/calm.wav (90 min procedural, 48 kHz estéreo, seed 42) — GATE 4 cobre.
- [x] Script capítulo 1 (10 cenas) validado: 0 problemas após word_fix.py (pad ≤136/retrim >136; sinônimos contra repetição).
- [~] Capítulos 2–9 em redação por 8 subagentes com validação própria (check_scene 108–136w + regra rep >2×); aguardando.
- [x] Capítulos 2–9 entregues pelos 8 redatores; revalidação independente nossa: 90/90 cenas OK (check_scene), 0 claims soltas; período e físicas conferidas na leitura; 2 pontos de pontuação corrigidos no cap. 8.
- [x] assemble_script.py executado: 90 cenas, 5400 s, sources_usable=22, **problem_count=0** → project.json escrito.
- [x] Fumaça real_assets --limit 2: 4 camadas (bg 1920x1080 / fg 960x540, 59,967 s @30fps), nomes com tokens do contexto (GATE 3), assetguard clean 1,0 no derivado; project.json intocado em modo limit.
- [x] Bug rel-path corrigido no real_assets (rel = assets/layers/<nome>, base = raiz do projeto — contrato de studio.asset).
- [x] Bug de duração corrigido: cortexreal = (duracao − 2×frame) → factor/janela com margem; 3 tentativas automáticas; conforme corrida: 180/180 camadas codificadas e anexadas ao project.json; ledger honesto em assets/video-source-ledger.json.
- [x] Teoria do render validada com teste da cena 1: camada tpad (TARGET 60,0) → composite 60,000000 s exato; TARGET/EXPECTED_MIN atualizados (60,0 / 59,98) + tpad=stop_mode=clone no filtro + caso especial cena-06 (recorte fechado 692x390@614,346, fator 3,7406) reproduzindo a versão validada visualmente.
- [x] 2º bug de duração isolado com prova: `-ss` fora da grade de quadros da fonte (ex.: 35,0417 vs grade 30fps) corta o quadro de fronteira → 1799 quadros (59,967 s) sempre; tpad não cobre porque o clone cai em pts 60,000 e é excluído pelo corte. Fix 1: quantizar start para a grade (floor). Fix 2 (definitivo): o argv formatava `%.2f` e ARREDONDAVA PARA CIMA passando do quadro fixado (prova: `-ss 47.57` → 1799; `-ss 35.03` → 1800; `-ss 47.5662` = grade−5e-4 → 1800/60,000000) — seek com epsilon abaixo do ponto fixado + `.4f`. Corrida retomada: 179/180 retomadas, só cena-79-bg re-encode.
- [x] Pre-check GATE 3: PASS — 180/180 camadas no contexto do roteiro, 0 violações (context_report.json).
- [x] Pre-check GATE 2: primeira passada 179/180 clean — 1 suspect (cena-06-bg, temporal_static_overlay); inspeção visual dos quadros: NENHUM texto/logo (falso positivo de cantos escuros no mwi); re-encode com recorte fechado 0,72 centrado + ledger atualizado → clean static_ratio 0,0. Segunda passada: **180/180 clean, exit 0**.
- [x] Voice Kokoro pm_alex: 90/90 cenas (audio/0000.wav … + scene['audio'] no project.json).
- [x] Re-encode 180/180 com tpad TARGET 60,0: **todas em exatamente 60,000000 s** (min=max=60,0; banda <59,98: 0). project.json anexado + ledger reescrito.
- [x] Pre-check GATE 3: PASS — 180/180 no contexto do roteiro, 0 violações. Pre-check GATE 2: 180/180 clean, exit 0 (cena-06-bg com recorte fechado já no encoder).
- [x] Render concluído: **preview.mp4 5400,021354 s** (dentro de ±0,5 s) + render.json (fingerprint 2dac1a01…, video_sha256 6deb2998…, srt sha 97578c9e…, status awaiting_review).
- [~] audio_mix em curso (--input preview --in-place --music calm.wav --record render.json).
- [ ] review (--reviewer --checks science visual voice subtitles rights) → export → delivery/.
- [x] Re-mix concluído com trilha dinâmica: preview final LRA 1,90 (inalterado) — curva calibrada por fatia 2400 s: music-db −17→1,9 · −8→3,0 · −2→4,2 (~1 pt/6 dB; teto físico ≈ 5-6).
- [x] Análise estrutural provada (ebur128, n=23.991 janelas de 0,1 s no mix −8): p10=−20,1 / p50=−16,2 / p95=−15,3; massa <−28 = 4,33%; gaps de voz: 80 ocorrências ≥0,8 s, 581 s de 5400 (10,8%), max 14,2 s; janelas 3 s inteiras dentro de gap ≈ 6-7% — exigiria ≥10% da massa < −30,3 para LRA>15: **impossível por construção** neste formato (narrada contínua + ducking 8:1), mesmo com bed silencioso total (e bed mudo >3 s perderia 2,5 pts do próprio gate).
- [x] Arqueologia de intenção fechada: componente em `studio.py:445-449` mede o **preview** e exige input_lra > 15; `science-studio/` é **untracked** (sem histórico git); HANDOFF 2026-10-30 registra pass do elétron com "LRA 31,3 (música audível)" + score 10,0 vs MEMORY com LRA 1,3 para o mesmo vídeo — notas conflitantes; "LRA 31,3 com 0 silêncios >1 s" é fisicamente contraditório (p10 ≈ −46 demandaria ≥10% de massa muda real detectável); delivery de referência apagado (`electron-descoberta-90min` não existe; `electron-factory-90min` vazio); bed procedural (audio_mix.py:28-41) tem tremolo ±0,5 dB + afades 4 s — nada gera janelas sub-−30.
- [x] **FAIL ABERTA resolvida (decisão do operador, 2026-11-10): medir a trilha.** Componente 3 do GATE 5 reescrito: mede a trilha registrada pelo mix (`preview.audio-mix.json` → `music/calm-swell.wav`); fail-closed (registro ausente/ilegível ou arquivo inexistente → LRA 0 → 0 pts); threshold intocado (>15). Suíte 28 testes verde.
- [x] gates 1–5: **TODOS PASSARAM — Score 10,0/10** (ASSETGUARD_BIN ativo).
- [x] review aprovado (`approval.json`: 5 checks science/visual/voice/subtitles/rights; reviewer com amostragem declarada) → **export concluído**: `delivery/` com final.mp4 3068,2 MB + subtitles.srt + project.json + approval.json + handoff.json (`publish: false`); sha256 final.mp4 `23fc2b00…` == approval == preview.mp4 (byte-fiel).
- [x] Debrief concluído: HANDOFF/MEMORY atualizados; brain decision `89a67cdb…` + learning `b68bb114…` (sem commit); temporários de calibração e repros apagados; permanecem `preview-narration.mp4` (pré-mix reutilizável) e `music/calm-swell.wav` (trilha final). Pendência única: aprovação artística final do operador (assistir/ouvir íntegro); publicação nunca automática.
- [ ] Commit: não autorizado.

# dark-videos: trava de contexto visual (GATE 3) — 2026-11-08

Updated: 2026-11-08. Entry point: `science-studio/context_gate.py`. Evidence: `science-studio/test_context_gate.py` + fumaça de gates.

## Checklist

- [x] BRIEFING/RECON: quarteto + `science-studio/PLAYBOOK-FACTORY.md` lidos; brain consultado (sem aprendizado prévio sobre trava de contexto — não é correção repetida); pipeline mapeado (providers → build_layers → studio gates); integração dark-videos confirmada (`D:\Git\dark-videos\backend\app\api\science_studio.json` aponta `home` para esta fábrica).
- [x] Causa raiz de frames fora de contexto identificada: `build_layers.py` atribuía silenciosamente o primeiro asset em ordem alfabética quando nenhum token casava (score 0); caminho SDXL gerava imagens sem prova de vínculo roteiro→imagem.
- [x] `context_gate.py` (novo): tokenização PT/EN (acentos, plural, stopwords), famílias de domínio declaradas como dados (`DOMAIN_FAMILIES`), ledger de proveniência `assets/prompts.json`, gate falha fechada + `context_report.json`.
- [x] `providers.py`: grava proveniência (cena, prompt exato, seed, generated) de background/foreground; reuso sem prova registra `generated=false` e o gate bloqueia.
- [x] `build_layers.py`: seleção via `select_scene_assets`; zero-match → exit 2 listando todas as cenas bloqueadas ANTES de codificar; fundo reusa asset em contexto em vez de cair no próximo (score 0).
- [x] `studio.py`: `run_gates` agora executa 5 gates; GATE 3 = trava de contexto visual.
- [x] Testes: 17 novos (`test_context_gate.py`, stdlib puro) OK; regressão zero (9 studio + 1 assemble_script + 1 voice_kokoro OK); py_compile OK.
- [x] Fumaça de encadeamento (`run_gates` real): sem proveniência → `GATE 3 FAIL ... FORA DO CONTEXTO`; com ledger `proven` → segue ao GATE 4. exit 0.
- [x] `PLAYBOOK-FACTORY.md`: regra 7 (PROIBIDO frame fora de contexto) + modo canal dark + seção da trava.
- [x] Brain: decision `cb456e0c` + learning `59e22ee2` registrados (`python -m brain learn`).
- [x] Quarteto atualizado (PROGRESS/HANDOFF/MEMORY/LEARNING).
- [ ] Commit/push: não autorizado nesta missão.
- [ ] Primeira produção real usando a trava (nenhuma produção em andamento foi tocada).

# Trainer contínuo DeepSeek V4.1 — 2026-11-03
- [x] Trainer de continuação em `D:/Git/DeepSeek-V4.1-Flash-1017-UNCENSORED-FP8/trainer/`: base congelada, LoRA, EWC, replay, gate de Fisher depois do Adam, teto de deriva e retomada de checkpoint.
- [x] `python -m unittest trainer.tests.test_continual`: 15 OK.
- [x] Fumaça CPU em `layers.10.attn.wo_b.weight` do shard presente `model-00013`: 1 passo, drift 0,000114, base sem gradiente. `model-00003` ausente.
- [ ] Caches de ativação reais ainda não existem. Sem eles o adapter não continua o comportamento do modelo. Qualidade não foi medida.

# DocumentÃ¡rio Factory â€” correÃ§Ã£o visual em andamento â€” 2026-11-01
- [!] VersÃ£o anterior reprovada: palestra mostra pessoas por mais de 3 s e nÃ£o atende Ã  regra de mÃ­dia animada. NÃ£o tratar como final.
- [!] Acervo local: 32 GIFs medidos = 187,27 s nativos combinados; NASA SVS 3314 baixado/verificado = 20,19 s. Total insuficiente; nÃ£o renderizar falsamente 90 min.
- [ ] Adquirir/verificar mÃ­dia licenciada em movimento; 5.400 s Ãºnicos sem repetiÃ§Ã£o nem stills e pessoas atÃ© 3 s.
- [ ] Remontar com MP3 aprovado, sem textos/cartelas/barras, sem deformar aspecto e em velocidade original.
- [ ] RevisÃ£o The-Fool: direitos/proveniÃªncia; 3 s nÃ£o Ã© safe harbor; revisÃ£o sequencial nÃ£o Ã© independente.
- [ ] Validar e entÃ£o atualizar destino/entrega.
- [x] Baixado MP4 NASA SVS 3314 pela URL oficial verificada; ffprobe confirmou 20,186854 s, 640Ã—480, 29,97 fps. NÃ£o cobre a lacuna material.
- [!] 90 min ainda bloqueados por acervo animado Ãºnico insuficiente. EvidÃªncia em .work/electron-factory-90min/evidence/CORRECAO-DIREITOS-E-VISUAIS.md.



- [x] Avaliado candidato Internet Archive A Is for Atom (882,78 s; 320Ã—240); rejeitado em amostragem por crÃ©ditos/letreiros e rÃ³tulos no prÃ³prio quadro, alÃ©m de resoluÃ§Ã£o/formato inadequados. EvidÃªncia em CORRECAO-DIREITOS-E-VISUAIS.md.

## Mapeamento 02_repositorios â€” 2026-11-01
- [x] Inventariar todos os diretÃ³rios e registrar estado local sem executar cÃ³digo dos projetos.
- [x] Gerar notas individuais, relaÃ§Ãµes verificÃ¡veis e limites; verificar cobertura e hashes.

- [x] InventÃ¡rio e notas de 18 diretÃ³rios: 9672 arquivos; verificaÃ§Ã£o de cobertura, fingerprints, Git e links PASS em 07_mapeamentos/mapeamento-2026-11-01/verificacao.json.
- [x] Os 17 fingerprints anteriores coincidem; reversa acrescentado. AnÃ¡lise estÃ¡tica e seletiva, sem execuÃ§Ã£o dos projetos.


## Reversa: inteligÃªncia para RAG e treinamento â€” 2026-11-01
- [x] Mapear fontes, contratos, riscos e proveniÃªncia do checkout local.
- [x] Criar corpus e recuperaÃ§Ã£o local verificÃ¡vel; registrar avaliaÃ§Ã£o e limitaÃ§Ãµes.
- [x] Preparar dados candidatos para revisÃ£o e plano de fine-tuning sem promover modelo.


## CorreÃ§Ã£o do documentÃ¡rio do elÃ©tron â€” 2026-11-01
- [x] Continuar pesquisa por fontes NASA SVS e inspecionar arquivos locais com ffprobe/contact sheets.
- [x] Rejeitar clips com texto/rÃ³tulos embutidos: Electron Beltway, Leaky Radiation Belts, Prompt Electron Acceleration e Fermi 14-year.
- [x] Registrar quatro candidatos animados sem texto visÃ­vel na amostragem (NASA 3314 sem datas, pulsar elÃ©trons/pÃ³sitrons, criaÃ§Ã£o de pares Fermi, Ride the Electron), duraÃ§Ã£o nova combinada 156,52 s; Ride the Electron tem apenas 352Ã—240 e precisa aprovaÃ§Ã£o de qualidade.
- [x] Confirmar download GammaCreation incompleto/corrompido; nÃ£o contar sua duraÃ§Ã£o.
- [!] RevisÃ£o The-Fool do novo corte: inconclusiva por ausÃªncia de novo render e inventÃ¡rio completo. RevisÃ£o feita em sequÃªncia pelo mesmo agente, nÃ£o independente.
- [!] Bloqueio objetivo: quatro candidatos novos somam 2min36,52s; mesmo somando o inventÃ¡rio GIF bruto de 3min07,27s, fica muito abaixo de 90 minutos e os GIFs ainda nÃ£o estÃ£o aprovados individualmente. NÃ£o repetir, desacelerar ou usar stills para preencher lacuna.
- [ ] Buscar novos assets Ãºnicos animados e licenciados, manter MP3 aprovado e regras visuais. EvidÃªncia: `.work/electron-factory-90min/evidence/CORRECAO-DIREITOS-E-VISUAIS.md`.


- [x] Continuação da busca: inspecionados NASA 3312 no-dates, 20066, 4649 e 10332 com ffprobe/contact sheets; adicionados quatro candidatos (duração adicional conjunta 102,574 s), nenhum texto/pessoa visível na amostragem.
- [x] Rejeitado NASA 182 (11,323 s) por símbolos e-/e+ embutidos visíveis; rejeitados também os overlays registrados acima.
- [!] Oito candidatos medidos = 259,093 s (4:19,093); faltam 5.140,907 s (85:40,907), sem contar GIFs não auditados. Não gerar falso full.
- [x] The-Fool: desafio sequencial aplicado. SEGUIR COM AJUSTE para adquirir fontes; gate de entrega INCONCLUSÃO, pois não há novo render/ledger completo; crítica não independente.

## Reversa — execução complementar — 2026-11-01
- [x] Revisar licenças locais MIT/Apache e incluir fontes elegíveis; 552 arquivos, 1403 trechos e verificação de integridade PASS.
- [x] Integrar busca e resposta ao MCP; 21 testes e Ruff PASS; busca real HTTP verificada.
- [x] Avaliar e melhorar recuperação: lexical 3/12 e híbrido 6/12 no top 10 da amostra exploratória.
- [x] Usuário delegou a revisão dos oito candidatos ao assistente; registro sequencial em REVISAO-ASSISTENTE.md.
- [!] Geração real foi interrompida por pressão de GPU; servidor de modelo desta tarefa encerrado para liberar memória.

- [x] Usuário delegou revisão ao assistente; oito itens conferidos em REVISAO-ASSISTENTE.md, sem alegar revisão humana independente.
- [x] Gerado dataset sintético 160/30/30, verificadas proveniência, hashes, grupos de caminhos e abstenções; não é dataset gold ou independente por projeto.

- [x] Índice E5 em CPU: 1403 vetores, integridade PASS; busca híbrida disponível e testada via HTTP no serviço.
- [x] Comparação exploratória por caminho esperado: lexical 3/12 e híbrido 6/12 no top 10; conjunto pequeno e não independente.
- [!] Fine-tuning real e resposta gerada ao vivo não concluídos: GPU compartilhada ~4 GB livres e 94–96% de uso; baseline e dados sintéticos ainda não sustentam qualidade. Não executar sobre cargas em andamento.



## Correção da avaliação de skills/repositórios — 2026-11-16
Entry point: `.specs/skills-quality-eval/rubric.md`. Evidence: `.work/skills-quality-eval/`, `.harness-eval/runs/2026-11-16-fix1/`.

- [x] Mapa repositórios×skills regenerado para 17×324 (5508 decisões); `verify.py` PASS com regeneração byte-idêntica; hashes de `00_skills/catalog.json` atualizados (13 skills com drift).
- [x] Harness Track A: 2 quebras (`AGENTS.md` → `references/CODENAVI_*_STANDARD.md`) corrigidas restaurando os 2 arquivos de `faac5adf^` com ponteiros reconciliados; novo run `2026-11-16-fix1`: 0 quebras. `AGENTS.md` intocado (`git diff` vazio).
- [x] Diagnóstico: 3 "aliases" fora do catálogo não eram defeito (declarados em `aliases`).
- [x] Rubrica A1 (workflow em código; secrets/fail-closed atômicos; holdout 1 de 60): 3 de 4 dimensões pass; `secrets_runtime_only` review.
- [x] Rubrica A2 (só `secrets_runtime_only`, holdout 2 de 60): pass, precisão 1,00, 44 aprovações.
- [ ] Não feito: Track B/C do harness (exigem juízes independentes); 18 skills sem roteamento não alteradas; `AGENT.md` raiz citado em `00_skills/(learning)/continuity-bootstrapper/SKILL.md` e `docs/` segue inexistente.
- Limites: rótulos prata pelo mesmo agente; `secrets_runtime_only` com só 2 negativos verdadeiros; nada commitado.


## Follow-up 2026-11-16 (batch completion)
- Track C usefulness: J1+J2 complete (331 surfaces). Merged -> `10-usefulness-agreement.md` (trap PASS; Slim 8, Keep 166, Mixed 4, Hold 150). J1=J2=`gpt-5.6-sol-medium`.
- Track B J1 complete (1075) in `05-redundancy-j1.md`. Judge2 relaunched on grok after Gemini quota.
- A1 complete 6/6. A2 relaunched 6/6 on deepseek (Gemini quota; overwrites prior A2-shard-1 for family consistency).
- JEV v4: 324/324 done. Blocked on A2 + B-J2 for IAA/final and Track B agreement.


## skills-quality-eval A3 result (2026-11-16)
- A1 GPT + A2 Composer + A3 Composer (adjudication): IAA pass all 4 dims; null_share fail_closed 0.6% (ok), others 0%.
- JEV vs S1 consensus: secrets_runtime_only **pass** (prec 1.00, n=321, neg=80); fail_closed **pass** (prec 0.992, n=292, neg=55); gov/provenance **uninformative** (0 negatives).
- JEV triage exit-silver: **all 4 remain silver** (T1_independence and/or T3_sufficiency < 0.70). Evidence: `.work/skills-quality-eval/a3/{iaa-v4,eval-report-v4,triage-decision-v4}.json`.
- Cause of stay-silver: annotator independence weaker than pre-registered (A2/A3 same Composer family after Gemini quota); gov/provenance have no negatives so cannot measure precision discrimination.
