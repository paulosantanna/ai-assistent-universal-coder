## fixall — MCPs e skills de QA e pentest — 2026-11-25

Updated: 2026-11-25. Entry point: `.notebook/fixall.md`.

- Fact: `qa-expert-mcp` e `pentexpert-mcp` não estavam no workspace nem na lista de repositórios de `paulosantanna` em 2026-11-25. Foram escritos aqui. Sem chave TypeSafe, nenhuma pontuação JEV foi gravada.
- Fact: o artigo https://arxiv.org/html/2401.05856 lista sete falhas de RAG. O oitavo pedido não foi inventado.
- Fact: o PTES não abriu nesse dia (HTTP 502, falha TLS e README 404). As fases não foram armazenadas.
- Decision: `test-expert` cobre as categorias; `qa-expert` é alias; `tests-expert` continua o charter funcional e de ponta a ponta. O playbook `fixall` não envia ao GitHub se o pedido não autorizar.

## Arquitetura cloud AWS e Azure — fatos verificados — 2026-11-14

Updated: 2026-11-14. Entry point: `cloud-architecture/README.md`. Evidence: `cloud-architecture-mcp/evidence/claims.json`, `cloud-architecture-mcp/providers/*/prices.json`, `02_repositorios/AIHealthResearch/infra/*`.

- Fact: AWS App Runner está fechado a novos clientes; a migração oficial é ECS Express Mode (sem custo adicional). ECS Express com sub-redes privadas provisiona ALB interno. Evidence: documentação oficial, 2026-11-14 (`apprunner-availability-change.html`, `express-service-work.html`).
- Fact: preços de lista (Price List pública, sa-east-1 contra us-east-1): endpoint de interface US$ 0,021/h por AZ contra US$ 0,01; OCU OpenSearch Serverless US$ 0,381 contra US$ 0,24; ACU Aurora Serverless v2 US$ 0,25 contra US$ 0,12; ml.g5.xlarge hospedagem US$ 2,394 contra US$ 1,408; Fargate ARM64 vCPU 20% abaixo do x86. Evidence: `providers/aws/prices.json` (SHA-256 por arquivo).
- Fact: AIHealthResearch as-is (CFN): 9 endpoints de interface x 2 AZ; endpoint SageMaker com `InitialInstanceCount 2` sempre ligado e `ModelInstanceType` sem padrão; Object Lock do arquivo em GOVERNANCE 365 dias; Lambda Fetcher sem VPC (saída pública por desenho). Evidence: `infra/workloads.json`, `infra/render_stack.py`, `infra/foundation.json`. Custo as-is US$ 6.046,85/mês (premissas no modelo).
- Fact: Azure Brazil South (PostgreSQL Flexible): HA com redundância de zona bloqueado temporariamente para servidor novo; backup geo-redundante indisponível. Evidence: página oficial, 2026-11-14.
- Fact: Artifact Signing (GA) tem validação pública restrita a EUA, Canadá, UE, UK e outros; individuo brasileiro não elegível. Evidence: FAQ oficial, 2026-11-14.
- Fact: a varredura de rotas do workspace (2026-11-14) achou mais duas APIs locais além das quatro já conhecidas: `science-studio/integration/dark_api.py` (5 rotas, jobs com subprocessos) e `rag-graph-laya-mcp/model_server.py` (5 rotas, formato OpenAI, GPU). Ambas estão em `cloud-architecture/local-apis.json`. Exclusão: `live-server.mjs` da skill de design (ferramenta de desenvolvimento).
- Fact: MyDigitalBuddy não tem crate HTTP nem telemetria (`Cargo.toml`, README, PRIVACIDADE.md); a nuvem serve só para distribuição (S3 + CloudFront + OIDC).
- Fact: existem duas cópias do AIHealthResearch: `02_repositorios/AIHealthResearch` (HEAD `5878719f`, árvore limpa, usada nesta missão) e `E:\Github\AIHealthResearch` (existe; não analisada).
- Decision (proposta, pendente do dono): AIHealthResearch alvo sem escala a zero na inferência (p95 de 15 s), Spot com checkpoint no treino, Object Lock em compliance só após ADR. Evidence: `cloud-architecture/docs/aws-aihealthresearch.md`.
- Limit: triagem do JEV em 65 claims foi calibrada com controles (48/50 positivos, 15/15 negativos na rodada final); é triagem, não prova.

## otel-telemetry-java — biblioteca OTel Java OTLP-only verificada; pins de 2026-11-11

Updated: 2026-11-11. Entry point: `10_projetos_estruturantes/otel-telemetry-java/pom.xml`.

- Fact: biblioteca completa existe e compila: core/exporters/adapters/starter/devtools + 2 examples, `mvnw verify` reactor exit 0 (estado final); artefatos `--release 21` sobre JDK 25.0.5+8 (`.tools/`, gitignored). Pins verificados em fonte primária (2026-11-11): OTel BOM 1.68.0, instrumentation 2.33.1-alpha, proto 1.11.1-alpha (→ protobuf 4.36.2), Boot 4.1.2, junit 5.14.4, snakeyaml 2.7, logback 1.5.38, micrometer 1.17.2, uPlot 1.6.32, Vite 6.4.6, Vitest 4.1.12 (bump pós-fixes F6; 10 GHSAs in-scope zerados). Evidence: `pom.xml`; consultas Maven Central/npm registry/OSV na sessão.
- Decision (plano v3, owner): OTLP-only (AD-001); precedência env > sysprop > yaml > builder (AD-003); sink JSONL por sinal em loopback 127.0.0.1:14318; fail-soft — qualquer falha de config vira no-op com diagnostics, segredo nunca em diagnostics/toString (AD-006/AD-003); dashboard iife clássico servido pelo jar do sink. Rotas dynatrace/grafana **NÃO VERIFICADO (J1)** — vendor docs 403/404 em 2026-11-11; rótulo no código (`Presets.java`) até doc real confirmar.
- Fact: prepush `cve_google` pós-fixes: **56 findings, ZERO in-scope** — o escopo real era 10 GHSAs (8 vite + 2 vitest), não 11: o "11º" contado antes era `GHSA-3pq3-5fj3-cg6v` de **axios**, pre-existing. Os 56 são pre-existing de outros pontos do workspace; `tinypool@1.1.1` (2 CRITICAL, fixed ≥2.1.1/2.1.2) rastreado ao lockfile de `10_projetos_estruturantes/ai-engineer-rpg` (o lock deste projeto não contém tinypool). Vetores dos pins antigos eram dev server/UI, não executados pelo projeto (`vite build` + `vitest run`). Evidence: OSV api.osv.dev (2026-11-11); `.aeos/prepush/report.json`.
- Fact: projeto **commitado** como `f821fcd2` (74 arquivos, 2026-11-11; escopo só `10_projetos_estruturantes/otel-telemetry-java`). Walks C20/C21/C23/C24 + F2 executados com playwright como **pacote Python** (site-packages do Python314; browsers chromium-1243 em `%LOCALAPPDATA%\ms-playwright` — `npx playwright` NÃO existe no workspace). Demo node do C23 roda em scratch FORA do repo (npm i poluiria o projeto). Evidence: verification.md (Fixes/Walks); `C:\Users\paulo\AppData\Local\Temp\opencode\c23walk\`.

---

## buraco-negro-90min — primeira entrega 90 min 100% IA; GATE 5 mede a trilha (2026-11-10)

Updated: 2026-11-10. Entry point: `D:\Git\dark-videos\.work\buraco-negro-90min\delivery\final.mp4`.

- Decision: o componente "Música audível LRA>15" do GATE 5 (`science-studio/studio.py` gate_final_score) mede a **trilha** registrada pelo mix (`<preview>.audio-mix.json`, chave `music`), não o preview: LRA no preview de narrada contínua + ducking 8:1 tem teto físico ~5-6 LU (p10/p95 fixados pela voz; massa só-bed 4,33% < 10% exigida para p10 ≤ −30; curva music-db −17/−8/−2 → LRA 1,9/3,0/4,2). Operador autorizou; threshold intocado (>15); fail-closed sem registro/trilha → 0 pts. Evidence: `.notebook/PROGRESS.md` (2026-11-10); brain `89a67cdb…`.
- Fact: LRA do preview não responde a `--music-db`: o relative gate do EBU (média −20 dB) exclui as janelas do bed; a voz domina 90%+ das janelas. A mesma trilha mediu LRA 18,2 standalone (I −18,04). Evidence: PROGRESS 2026-11-10 (curva calibrada por fatia de 2400 s).
- Fact: histórico anterior dos gates conflita consigo mesmo (HANDOFF 2026-10-30: LRA 31,3 + score 10,0 vs MEMORY: LRA 1,3 no mesmo vídeo) e o `science-studio/` é untracked (sem git history) — notas históricas de métrica precisam medição reprodutível no artefato existente. Evidence: `.notebook/HANDOFF.md` (2026-10-30) vs `.notebook/MEMORY.md`; delivery do elétron apagado.
- Evidence: entrega verificada — final.mp4 3068,2 MB, sha256 `23fc2b00…` == approval.json == preview.mp4 (byte-fiel); gates 10,0/10; review 5 checks com amostragem declarada; `publish: false` no handoff.json.

---

## ai-engineer-rpg — RPG web de Engenharia de IA completo e verificado

Updated: 2026-11-10. Entry point: `10_projetos_estruturantes/ai-engineer-rpg/package.json`.

- Fact: o RPG web de mesa (React+Vite+TS, 100% client-side) está completo em `10_projetos_estruturantes/ai-engineer-rpg/` — engine puro em `src/engine/*`, conteúdo autoral em `src/content/*` (pack v1.1.0: 7 reinos, 56 lições, 56 missões, 231 questões, 51 fontes, 78 termos, capstone de 8 competências), store `gameStore.ts` com `useSyncExternalStore` (sem zustand) e UI em `src/ui/*`. Suíte 55/55, build ok (chunk 867.65 kB), mutações 3/3. Estado operacional em `.notebook/HANDOFF.md` e provas em `.notebook/PROGRESS.md`.
- Fact: a distribuição é standalone: `npm run build` emite `dist/index.html` que abre por duplo clique sem servidor (formato iife, script clássico sem `type="module"`, caminhos relativos, CSS embutido no chunk). Code-splitting conflita com o iife — só vale com hosting http. Evidence: `vite.config.ts` (plugin `iife-classic-index-html`); `.notebook/LEARNING.md` (lição file://).
- Fact: o certificado verifica-se por recálculo do SHA-256 do dossiê canônico (JSON ordenado por chave → código `AIE-AAAA-HASH8`), não por assinatura PKI. O pdf-lib grava metadados Info como UTF-16BE hex, então o teste de PDF usa leitura estrutural (`PDFDocument.load`), não varredura ASCII. Evidence: `10_projetos_estruturantes/ai-engineer-rpg/tests/certificate.test.ts`; `src/engine/certificate.ts`.
- Fact: expansão de conteúdo v1.1.0 (2026-11-10): 8 lições e 8 missões por reino (chefão em `rN-m8`, kind `boss`) com 2 lições técnicas novas por domínio; `realm0.ts` exemplar + 6 reinos reescritos por subagentes paralelos (r2/r5 falharam só no relatório após completar os writes). Chefões mudaram de id (`rN-m6` → `rN-m8`); saves antigos não afetam o jogo novo (owner sem progresso). Evidence: `.notebook/PROGRESS.md` (seção RPG); `.notebook/ai-engineer-rpg.md`.
- Evidence: `.specs/features/ai-rpg-engineer/{plan,checks,verification}.md` no projeto; gate formal final pendente de commit (política do owner).

---

## Portão antes do push

Updated: 2026-11-09. Entry point: `quality/prepush/prepush.py`.

- Decision: o push deste workspace passa por seis backends no mesmo comando local e em `.github/workflows/prepush-gate.yml`: OSV Google, registro público da biblioteca, endoflife.date, recurso de versão do PE, SAST alinhado ao commit atual de `semgrep/semgrep-rules` e segurança estática alinhada ao release atual do gitleaks. Fonte indisponível ou velha bloqueia. Exceção sem data não vale.
- Fact: `deploy-expert-unique` cita OSV e CodeQL; `E:\Github\AIHealthResearch\.github\workflows\ci.yml` executa Bandit e pip-audit e não esses dois passos. MyDigitalBuddy é o workflow que já consulta a OSV e exige Rust stable.
- Fact: `.venv/` e `.state/` não são o produto. A corrida que os incluiu apontou JDK e pacotes de terceiros; a corrida seguinte, sem eles, manteve os CVE dos locks do projeto.
- Evidence: `.notebook/prepush-gate.md`; `quality/prepush/README.md`.

---

## Padrão DO NOT INVENT / NUNCA INVENTE: escopo, registro e aceitação

Updated: 2026-11-09. Entry point: `00_skills/do-not-invent.manifest.json`.

- Fact: 46 skills declaravam a regra no `SKILL.md` original, na descrição ou no corpo. O registro guarda a cláusula literal de cada uma. Evidence: `00_skills/do-not-invent.manifest.json`; original em `.tools/skill-restructure/backup/` (ignorado pelo git).
- Decision: a regra é padrão do entrypoint (`SKILL.md`). Na descrição, é aceita como limite negativo pelas formas `negation` e `qualified` do manifesto. Se uma cláusula registrada sumir, o validador reprova. O architect upstream (`references/tlc/scripts/validate_skill.py`) permanece byte-idêntico; a aceitação fica no validador do workspace. Evidence: `validate-workspace.py` (`accepts_anti_invention`, check `DO NOT INVENT clause missing`); `00_skills/upstream.manifest.json`.
- Fact: módulos `references/usage-and-verification.md` carregam a regra genérica ("Never invent data, claim an unrun check passed…") em cerca de 200 skills. Não foram alterados pela reestruturação. Evidence: `00_skills/(development)/codenavi/references/usage-and-verification.md`.

---

## Padrão de skills: descrição de roteamento até 150 caracteres e seção Response

Updated: 2026-11-09. Entry point: `00_skills/STANDARD.md` (seção "Formato enxuto — 2026-11-09").

- Fact: o catálogo exibe cerca de 150 caracteres de cada descrição. Antes da reestruturação, 327 de 327 descrições nativas passavam desse limite, e gatilhos e exclusões ficavam fora da parte visível. Evidence: `00_skills/VERIFICATION.md` (seção 2026-11-09).
- Decision: descrição canônica com até 150 caracteres, `Use when`/`Use for` e `Do NOT use for`; a mesma string vai ao catálogo, ao `.agents/skills`, ao registro e ao INDEX. O validador exige igualdade entre canônico, catálogo e ponteiro nativo (`Stale routing description`). Evidence: `00_skills/(creation)/skill-factory/scripts/validate-workspace.py`.
- Decision: todo SKILL.md canônico termina com `## Response` (resultado primeiro, evidência, bloqueios, próximo passo; schema definido prevalece). Evidence: `00_skills/STANDARD.md`.
- Fact: `(design)/impeccable` é importado com hash pinado em `source.manifest.json`. Alterar o `SKILL.md` dele quebra o check de proveniência do validador. Evidence: erro `impeccable provenance` observado em 2026-11-09.
- Fact: a governança vigente das skills é `CodENavi Full Workspace v2`, conforme AGENTS.md. A nota `workspace-governance.md` citava `CodENavi v1` e foi corrigida. Evidence: `AGENTS.md`, `00_skills/STANDARD.md`.

---

## dark-videos: trava de contexto visual e modo canal dark (100% IA)
Updated: 2026-11-08. Entry point: `science-studio/context_gate.py`.
- Fact: a fábrica Science Studio, consumida pelo app dark-videos via `D:\Git\dark-videos\backend\app\api\science_studio.json` (`home` → `E:\Github\ai-assistent-universal-coder\science-studio`), produz vídeos 100% IA para canal dark: roteiro por LLM local (`providers.py script`), narração por voz IA (`voice_kokoro.py`/`voice_google.py`; a voz do criador nunca é usada, sem clonagem de terceiros), visuais gerados por IA (`providers.py assets`) ou curados com licença (`build_layers.py`); `speech_balloons: false` é obrigatório no contrato.
- Decision (operador, 2026-11-08): PROIBIDO qualquer frame visual fora do contexto do roteiro. GATE 3 determinístico (`context_gate.gate_visual_context` dentro de `studio.run_gates`) falha fechada: vínculo provado pelo ledger `assets/prompts.json` (cena + prompt exato + `generated=true`) ou por nome de asset que cita o contexto; famílias de domínio são dados declarados (`DOMAIN_FAMILIES`); violação grava `context_report.json` e bloqueia; `build_layers.py` bloqueia cena zero-match (exit 2) em vez de atribuir asset arbitrário. Sem bypass.
- Evidence: `science-studio/test_context_gate.py` (17 testes stdlib); fumaça de `run_gates` (GATE 3 FAIL sem proveniência; `proven` → GATE 4); suíte existente verde (9 studio + 1 assemble_script + 1 voice_kokoro); brain `cb456e0c`/`59e22ee2`; `PLAYBOOK-FACTORY.md` regra 7 + modo canal dark. Sem commit.

## DeepSeek V4.1 — continuação sem reescrever o shard
Updated: 2026-11-03. Entry point: `D:/Git/DeepSeek-V4.1-Flash-1017-UNCENSORED-FP8/trainer/README.md`.
- Decision: a continuação deste checkpoint é um LoRA sobre uma cópia bf16 congelada. O shard original não é destino de treino. Experts roteados FP4 e tabelas Engram ficam congelados.
- Fact: em 2026-11-03 havia 29 de 48 shards. `layers.10.attn.wo_b.weight` em `model-00013` é `[5120, 8192]` F8_E4M3; um passo CPU ficou em drift 0,000114. `model-00003` não está no disco.
- Evidence: `python -m unittest trainer.tests.test_continual` (15 OK) e a fumaça desse tensor. Não é métrica de qualidade do modelo.

## Documentário do elétron — visuais 1×
Updated: 2026-11-01. Entry point: `.work/electron-factory-90min/evidence/visual-sources-1x.md`.
- Fact: a versão entregue em `D:\Git\dark-videos\documentario-eletron-90min-FINAL-YOUTUBE.mp4` tem 5.400 s, H.264 1440×1080/24 fps, aspecto 4:3 nativo e faixa MP3 copiada do áudio aprovado. SHA-256: `9498B3BA4FB224CB7B4382C5ECB360E67B94426C5E7332BB15BDD5B0C5AD3C7F`.
- Decision: fontes de vídeo reutilizáveis precisam de licença verificada; as partes 1 e 2 da palestra de Linus Pauling (1957) estão catalogadas pelo Science History Institute com Public Domain Mark 1.0. Trechos contínuos sem repetição, velocidade nativa, cartelas retiradas e proporção preservada.
- Evidence: `.work/electron-factory-90min/evidence/{visual-sources-1x.md,visual-delivery-1x.json}`; páginas institucionais `digital.sciencehistory.org/works/{twr0k94,r7qoyok}`.
## iDentifyer — semântica do visor Wi-Fi
Updated: 2026-10-29. Entry point: E:/Github/iDentifyer/docs/WIFI_VIEW.md.
- Fact: web/src/wifi-view.js apresenta exclusivamente snapshot real de /api/sensors dentro do vídeo ativo; não derivaRF de pixels/detecções. Conexão/%/RSSI reais verificados no ramo conectado; sinais continuam globais ao enlace.
- Decision: não desenhar captura espacialRF sem dados/validação; campo de ausência/erro/stale remove números correntes. Postura e sinais faciais são modalidades independentes preservadas.

---

## iDentifyer — sinais físicos faciais
Updated: 2026-10-29. Entry point: domain/identifyer.md.
- Fact: MediaPipe tasks-vision1.2.0/modelo FaceLandmarker/WASM locais; web/src/face-signals.js interpreta somente mouthSmile/jawOpen/eyeBlink. Barra0–100 representa coeficiente visual do sorriso, não estado emocional. Rosto ambíguo recebe abstenção; nenhum ponto desenhado e nenhum sinal salvo. Evidência: E:/Github/iDentifyer/docs/FACE_SIGNALS.md.
- Decision: preservar classe/confiança da caixa, complementar apenas pessoas; modelos novos ficam opcionais, falha permite retry/COCO ativo. Versões npm existentes, runtime Rust/sensores/fusão/banco preservados. Verificado: .work/identifyer-visible-signals/deployment.json.

---

## iDentifyer — desenho de aquisição externa
Updated: 2026-10-29. Entry point: domain/identifyer.md.
- Decision: caminho inicial documentado é Lepton3.5 radiométrico+PureThermal3 e parESP32-C6TX/RX; aquisição é etapa separada de fusão. Lepton é sensor e PureThermal é interface; confirmar composição do conjunto.
- Decision: CSI da cena não atribui identidade/track por coincidência temporal. Associação térmica por alvo exige calibração e condição observável de validade; homografia de plano não prova correspondência em volume3D. Fonte: E:/Github/iDentifyer/docs/FUSION_PLAN.md e FUSION_REVIEW.md.

---

## iDentifyer — contrato de postura
Updated: 2026-10-29. Entry point: domain/identifyer.md.
- Fact: extensão local MoveNet SinglePose/TFJS existente + web/src/posture.js descreve geometria de braços/tronco; gate de pessoa independente do limiar visual, abstenção e nenhuma persistência de pose. Não infere idade/humor/traços/intenções/criminalidade. Evidência: E:/Github/iDentifyer/docs/POSTURE.md.
- Decision: preservar revisão nativa de sensores e executável atual ao instalar somente frontend/modelo/docs. Staging antigo .work/identifyer/project requer reconciliação antes de reaplicar. Evidência: .work/identifyer-posture/deployment.json.

---

## iDentifyer — provedores reais Windows
Updated: 2026-10-29. Entry point: domain/identifyer.md.
- Fact: src/wifi_windows.rs usa bindings oficiais WLAN, distingue rádio/conexão de qualidade/RSSI; src/sensors.rs consulta temperatura real GPU NVIDIA com executável absoluto/args fixos e limites. Não confundir GPU térmica interna com imagem IR do ambiente.
- Decision: não converter estado desconhecido/ausência/N/A em desligado/zero. Rede desconectada não prova ausência de placa. Evidência: E:/Github/iDentifyer/docs/evidence/{sensor-upgrade,sensors-installed}.json e SENSORS_REVIEW.md.

---

## iDentifyer — arquitetura e capacidade verificável
Updated: 2026-10-29. Entry point: domain/identifyer.md.
- Fact: E:/Github/iDentifyer usa Rust/Axum loopback18741, SQLite de metadados manuais e inferência COCO-SSD local no navegador; nenhum frame enviado. Evidência: docs/PLAN.md, docs/VERIFICATION.md e change-manifest.json no projeto.
- Decision: rádio/temperatura interna não identificam nem localizam seres vivos; RF/CSI/radiometria precisam hardware/calibração próprios. Entrega experimental, sem aprovação de produção; limites em docs/THE_FOOL.md.

---

## Science Studio local production contract

Updated: 2026-10-27. Entry point: `flows/science-studio.md`.
- Fact: eight original TLC-format scientific Motion Comic skills compose one shared Python/FFmpeg playbook, with PT-BR profiles 60/600/3600/5400 s, local project/assets, scene cache and separate reviewed delivery. They remain skills of codenavi-agent, not new identities or official TLC upstream packages.
- Decision: source traceability and technical hash gates never replace scientific/artistic/voice review; explicit human checks precede export and remote publication is separate. Local AI adapters require actual licensed engines/weights/workflows; instruction discovery does not install models.
- Evidence: `science-studio/{PLAYBOOK,CONTRACT}.md`, `studio.py`, `providers.py`, `VERIFICATION.json`; D:/Git/dark-videos integration pointers in the flow note. Local engines later provisioned and smoke-verified in `.work/science-engines/{README.md,verification.json}`; isolated runtime paths are explicit, not inferred from the caller Python/PATH.
- Verified duration contract: explicitly authored totals up to 6600 s are accepted by studio.py:validate, with matching scene sums; four profile defaults unchanged. Evidence: science-studio/test_studio.py:test_custom_110_minute_duration_requires_matching_scenes and .work/meu-filme/core-contract-verification.json.
- Verified publishing extension: D:/Git/dark-videos/backend/app/modules/publishing/original.py validates approved horizontal exports and persists idempotent original jobs in AppSetting; dispatch.publish_original shares the existing upload transport/global lock. Native IDs resume confirmation only. Original film y49FNgkmR_w was confirmed public with matching metadata. Evidence: .work/science-youtube/{publication.json,installed.json,verification.json}; flows/science-studio.md. Preserve this installed extension when updating the older factory integration template.

---

# MEMORY

Updated: 2026-10-24

## Active memory

### workspace-brain (2026-11-08)
- Fact: the brain lives at `E:\Github\workspace-brain` (CLI `python -m brain`, SQLite FTS5 with BM25). Notebook entry: `.notebook/workspace-brain.md`. Spec: `E:\Github\workspace-brain\.specs\features\workspace-brain\`.
- Fact: the JEV API, from the OpenAPI snapshot, is `POST https://api.typesafe.ai/v1/systemone` with `Authorization: Bearer <key>`. `GET /v1/models` returned `jev-latest` and `jev-preview` on 2026-11-08. The key is read in memory from `E:\cookier\JEV`, a single bare token; it is never printed, copied or stored.
- Fact: GitHub REST search works without login (10 search requests per minute). `gh` is installed but not logged in.
- Decision: this workspace allows no delegation to subagents (AGENTS.md; spec-driven rule 6). Skills run as sequential lenses, labelled self-verified.
- Evidence: `.work/workspace-brain/evidence/` (run files, `judge-report.md`, `the-fool-report.md`).
- Fact (2026-11-08, silver labels, owner validation pending): with 45 dark-channel repositories (amendment A2; 210 labelled pairs), the gate at probability 0.9 gives precision 0.984 [0.917; 0.997] and recall 0.768 with 64 approvals: pre-registered verdict pass. Thumbnail precision 0.833 (1 FP); video_assembly recall 0.607. The 35-repository v1 sample stays inconclusive by size. Evidence: `.work/workspace-brain/evidence/dark-channel-eval/eval-summary.md`.
- Updated: 2026-11-08

### Repository knowledge snapshot beta 3.0.0
- Fact: `07_mapeamentos/mapeamento-beta-3.0.0/` mapeia os 17 diretórios locais de `02_repositorios`, incluindo ncm; guarda notas individuais, matriz por dimensão, estado Git, hashes e comparação com evidências anteriores.
- Decision: beta 2 permanece histórico; sem baseline completo não alegar diff integral 2→3. Código presente, bibliografia, smoke e runtime comprovado são estados distintos; cópias E: e D: não são intercambiáveis.
- Evidence: `.notebook/graph/repositorios-beta-3.0.0.md`; pacote `{README,CONHECIMENTO,ATUALIZACOES}.md`, `mapa.json`, `evidencias.json`, `verificacao.json`.
- Updated: 2026-10-27

### dark-videos: destinos independentes de Instagram
- Fact: publishing_0004 identifica publicação por vídeo+conta+placement. `destinations.ensure_instagram_destinations` completa Reel/Story ausente na janela, sem copiar recibo nativo nem rearmar a falha do outro destino. API publish-now e release chamam o preenchimento; lookups de criação incluem placement.
- Decision: Story recusado por duração conserva seu destino/erro; não vira outro Reel. Unicidade antiga não pode ser restaurada enquanto existirem pares, sem decisão explícita sobre os dados.
- Evidence: `D:/Git/dark-videos/backend/app/modules/publishing/destinations.py`; migração publishing_0004 e testes `test_instagram_destinations.py`; `.work/instagram-both/`.
- Updated: 2026-10-27


### dark-videos: publicação em clique único e retry de agendamento atual
- Fact: `schedule/page.tsx` envia o pedido no primeiro clique. `immediate.NATIVE_RETRY_ERRORS` e `_retry_records` usam a linha nativa atual para retomar agendamentos identificados, inclusive quando o registro terminal do lote conserva erro antigo; uploads incertos não são rearmados por essa regra.
- Evidence: `D:/Git/dark-videos/backend/tests/modules/publishing/test_click_recovery.py`; `.work/publish-all-click/{reproduce.log,installed.json,live-final.json}`. Testes de retomada não provam publicação remota de todo o lote.
- Updated: 2026-10-26


### TLC spec workflow version pins
- Fact: `tlc-spec-driven` and `spec-driven` use 4.0.0 (`ef2672d`); `tlc-spec-lean` and `spec-driven-lean` use the explicitly requested 2.0.0 (`2fca1d1`), not newer main releases.
- Decision: resolve each source commit from the package entry in `00_skills/upstream.manifest.json`, not the historical top-level snapshot commit. Immutable source lives under `references/tlc/`; executable local helpers live under `scripts/` and include the Windows signal/process-tree adaptation.
- Evidence: package `references/provenance.md`, upstream manifest, `.work/tlc-spec-upgrade/EVIDENCE.md`. Root one-agent contract applies: sequential self-verification never counts as independent review.
- Updated: 2026-10-26


### dark-videos: "Publicar tudo agora" — clique re-arma só falhas de pré-upload; escolhedor do IG é muro (24/10)
- Status: corrigido **sem commit** e aplicado ao vivo; backlog parqueado aguardando as sessões.
- Fact: `immediate.start_batch(retry_existing=True)` passa a selecionar BLOCKED
  `source_frame_review_unavailable` e FAILED `browser_login_required`/`cookie_file_locked`/
  `vault_unavailable` **sem id nativo** (raise sites antes de qualquer upload); `_retry_records`
  re-arma também registro `skipped` dessas linhas, e linha conhecida do lote não muda de estado
  fora dele. Falhas ambíguas (`publish_interrupted`, `*_publish_failed`, `platform_*_unconfirmed`)
  e linhas com id nativo permanecem paradas — nunca duplicar. `browser_post._login_wall` reconhece
  o escolhedor "Usar outro perfil"/`accounts/emailsignup`, e `_click_labeled` pula controles de
  cadastro (Playwright casa nome por substring: "Criar" clicava "Criar nova conta").
- Estado aplicado: lote `1cd4c5ab` 184 registros; 99 linhas `browser_login_required` aguardando
  reconexão (IG 37 / TikTok 28 / YouTube 34); 0 duplicata e 0 publicação nova.
- Decision: re-arm automático continua restrito (`REPLAYABLE`); é o clique explícito do operador
  que libera o backlog seguro. Sessões (IG/TikTok deslogados; identidade do YouTube) só o operador
  resolve — o lote retoma sozinho após novo grant de conta ou num novo clique.
- Evidence: `E:/Github/ai-assistent-universal-coder/.work/publish-now-nothing/{EVIDENCE.md,live-after.json,rearm-applied.json}`;
  testes `test_mass_retry.py`, `test_browser_post_helpers.py`, `test_session_precedence.py`.
- Updated: 2026-10-24

### dark-videos: inspeção de moldura e a falha total do estágio creative (22/10)
- Status: causa raiz diagnosticada e corrigida **sem commit** em `D:\Git\dark-videos` (cópia em execução).
- Fact: a inspeção visual obrigatória (`mining/source_inspection.py`) rejeita candidato a candidato:
  barras uniformes locais (`image_has_bars`) → `existing_source_frame`; modelo de visão (5 quadros
  high) → clean/framed; ausência/falha → bloqueia (falha fechada). Nas execuções de 22/10, das 99
  fontes: 43 barras reais (conferidas), 17 download falho, e **39/39 revisões visuais falharam** por
  timeout de 60 s sob concorrência 8× e/ou cap de tokens do modelo de raciocínio
  (`nvidia/nemotron-3-nano-omni-30b-a3b-reasoning` emite `reasoning_content` ~850-900 tokens antes
  do JSON; cap observado: completion 866 > `max_tokens=800`) → estágio sem nenhuma moldura falha.
- Fix verificado: timeout 150 s só para `build_vision_chat`, `_REVIEW_MAX_TOKENS=1500`, log com
  `exc_info=True`; `OpenAICompatibleChat`/`_Client` aceitam `timeout_seconds` (padrão 60 s);
  52 testes verdes; replay real com 8 workers: aprovados voltam (1 em 17; residual transitório ~6%).
- Decision: não afrouxar a falha fechada da revisão; tratar origem do acervo (reposts com moldura)
  e/ou retry como próximos passos de estoque, não como bypass.
- Evidence: `.work/frame-review-fix/RESULTADO.md`; `pipeline_runs.state` (run 6caf519b);
  `~/.local/share/dark-videos/media/sources/`; testes `tests/modules/mining/test_ptbr_unframed.py`.
- Updated: 2026-10-22

### NCM (Next-Concept Modeling) retained knowledge
- Status: mapping artifact + **sudoku-hard claim reproduced** in an isolated venv; remaining claims unreproduced.
- Fact: `02_repositorios/ncm` @ `c702742` (HazyResearch, MIT, 5 commits) is an inference/eval release of a coarse-to-fine architecture: multiscale residual VQ-VAE tokenizer (K levels, EMA codebooks, `Phi` residual conv, `fine_drop`) + transformer predicting one level per step with intra-level parallelism (`block_diagonal` attention, per-level RoPE, codebook-tied heads, CFG ramp) — K steps, not L tokens. Deep mapping package: `07_mapeamentos/mapeamento-ncm/` (alpha/beta/celta + comparison CSV); focused note `.notebook/ncm-next-concept-modeling.md`.
- Reproduced (2026-10-21): sudoku-hard **solved 86.25% (1725/2000)**, cell 98.36% vs blog claim 86.1%; official HF checkpoints (sha256 == LFS oids; config byte-identical) in `.work/ncm-repro/`; RTX 5080 + torch 2.11.0+cu128 + Python 3.14.7; 12 forwards/board. Evidence: `.work/ncm-repro/RESULTADO.md`.
- Decision: speed/quality claims for other tasks (21×/10×/31× faster; 4–5× fewer training tokens; easy/medium Sudoku) remain **unreproduced**; release has no training code; nothing else executed.
- Evidence: `07_mapeamentos/mapeamento-ncm/{README,alpha,beta,celta}.md`, `matriz-comparativa-ncm.csv`, `.notebook/ncm-next-concept-modeling.md`, `.work/ncm-repro/RESULTADO.md`, git commit/status of the target, arXiv:2610.14162.
- Updated: 2026-10-21

### NCM aplicado ao dark-videos (seleção coarse-to-fine com Laya)
- Status: implementado e verificado em testes/smoke no alvo; **não ativado em runtime** (app parado; sem commit).
- Fact: `D:/Git/dark-videos/backend/app/modules/learning/ncm.py` aplica o paradigma do NCM à seleção:
  nível grosso (conceito = token dominante dobrado do título/legenda) pontua todo o pool numa passada
  sem modelo, com prior aprendido dos números por rede (`LearningRecord` de resultado com `views_24h` +
  conteúdo; `AccountMedia`/`AccountInsightSnapshot` com legenda; suavização `LEARNING_NCM_MIN_SAMPLES`);
  o Laya (nível fino) julga só o shortlist (`LEARNING_NCM_SHORTLIST_PER_PLATFORM`, 32/rede). Score mantém
  0,65·baseline + 0,35·jev com ajuste ≤ ±10% (`NCM_NUDGE`) e breakdown `ncm`/`ncm_<rede>_prior`;
  `LearnStage` grava `ncm_concept`. Sem observação o prior é desconhecido (nunca inventado) e o
  comportamento é exatamente o anterior.
- Evidence: `D:/Git/dark-videos/.specs/features/ncm-selection/{plan,checks}.md`, `docs/rag-laya.md`,
  `.notebook/ncm-selection.md`; `E:/Github/ai-assistent-universal-coder/.work/ncm-selection/EVIDENCE.md`
  (462 testes learning+mining com o mesmo conjunto de 25 falhas pré-existentes; smoke 500→32/rede,
  125→8 chamadas Laya por rede).
- Decision: não usar o modelo/checkpoints do NCM (release de inferência, sem treino/domínio de vídeo);
  o que se aplica é o paradigma. O prior mede o passado da rede, não probabilidade calibrada
  (Laya segue `model_uncalibrated`).
- Updated: 2026-10-21

### Source-backed repository/skill routing
- Status: static mapping artifact; not external runtime validation.
- Fact: `07_mapeamentos/repositorios-skills/` records canonical catalog IDs, per-project ten-dimension maps, four applicability states and file/line/hash evidence. Source projects are read-only; aliases do not count as additional skills.
- Evidence: `07_mapeamentos/repositorios-skills/{README.md,mapa.json,verificacao.json,browser-verificacao.json}`; focused note `repositorios-skills.md`.
- Decision: refresh on source/catalog drift; never infer a local integration from name similarity, runtime availability from instructions, or CVE/EOL safety from manifests.
- Updated: 2026-10-13


### Canonical TLC instruction discovery
- Status: active instruction catalog; external runtime availability is not inferred.
- Fact: `00_skills/(category)/slug/` holds 316 active instruction packages and 319 native canonical/alias pointers (verified 2026-10-27). The original92 TLC snapshots retain source6df68d52; demo and tlc-prd bring source coverage to94 with per-package commits. Latest recognized TLC control commit is tracked in quality/tlc-upstream.json by the daily monitor, not frozen in memory. Impeccable4.1.1 remains5a149f3f. SKILL.md retains the100-line physical cap; source resources retain attribution, canonical LF digests and executable flags, with historical acquired_sha256 where applicable.
- Evidence: `00_skills/catalog.json`, `00_skills/upstream.manifest.json`, `quality/tlc-upstream.json`; entrypoints `capability-ci.md`, `tlc-skills.md`. Photo verification is the historical302-package snapshot.
- Decision: preserve external deletions; never restore removed AEOS runtime/configuration from stale notes. Existing skill instructions remain usable subject to actual prerequisite checks.
- Updated: 2026-10-13

### Photo-derived skill activation boundaries
- Status: active instructions, not external runtime installation.
- Fact: the 2026-10-13 batch changes learning-opportunities to AAR/reusable-knowledge selection (quartet writing remains with its owning skills) and skill-architect to creating/evaluating/scoring/improving skills. Meeting/call video routes to acta-aurea even for a transcription-only verb; bare audio routes to vox-aurum. Impeccable source profiles are sequential local lenses, never new identities or genuinely blind independent review.
- Evidence: `00_skills/PHOTO-UPDATE.md`, affected canonical SKILL.md files, `00_skills/PHOTO-STRUCTURE.md`.
- Decision: name-only photographed skills remain inactive folders pending real contracts; official fonts/logo, private runtime integrations and absent speech engines are not inferred from photographs.
- Updated: 2026-10-13

### Runtime pointer reconciliation
- Status: current workspace boundary.
- Fact: the external reorganization removed root aeos/runtime/scripts/templates/references during the skill migration. Historical entries below retain prior verified observations, but references to deleted routers/registries/MCP configurations do not establish current runtime availability. Current instruction paths/catalog are the source of discovery truth.
- Evidence: `PROGRESS.md:Final acceptance evidence`, `00_skills/VERIFICATION.md`.
- Updated: 2026-10-12


### csharp-expert current stable pin
- Status: retained instruction knowledge; removed runtime pointers are historical
- Fact: `csharp-expert` is a TLC-format skill of `codenavi-agent` for production C# source. The folder id is `csharp-expert` because the TLC kebab-case check rejects `#`; the description triggers on `c#-expert`. New code targets C# 14 on .NET 10.0.12 (SDK 10.0.401, LTS, support through 2028-11-14). An existing project keeps its declared TFM. .NET 11.0.0-rc.1 / C# 15 stays unused unless the repository already targets it. There is no C# docs MCP.
- Historical/runtime evidence (check availability before use): `00_skills/(development)/csharp-expert/SKILL.md`, `00_skills/(development)/csharp-expert/references/current-release.md`, `aeos/registries/skills.csharp-expert.additions.yaml`
- Updated: 2026-10-09

### tests-expert oracle
- Status: retained instruction knowledge; removed runtime pointers are historical
- Fact: `tests-expert` runs real functional and end-to-end checks after a bug fix or new behavior. The user request is the only oracle. Frozen expectations cannot be edited to match a failing application. An open failure is `.aeos/tests-expert/RESUME.md` for a later context window, not a `MEMORY.md` entry. Unit and class tests are outside this skill.
- Historical/runtime evidence (check availability before use): `00_skills/(quality)/tests-expert/SKILL.md`, `00_skills/(quality)/tests-expert/scripts/charter.mjs`, `aeos/registries/skills.tests-expert.additions.yaml`, `tests/node/tests-expert-charter.test.cjs`
- Updated: 2026-10-08

### Architecture knowledge skills and MCP
- Status: retained instruction knowledge; removed runtime pointers are historical
- Fact: ADR, ADL, ASR and AKM are governed TLC-format skills owned by `codenavi-agent`: `architecture-decision-record` (derived from TLC `create-adr` 1.0.0, updated to MADR 4.0.0), `architecture-decision-log`, `architecturally-significant-requirement` and the super-skill `architecture-knowledge-management`. MCP `architecture-knowledge` is governed by `architecture-knowledge-management`, allowed by playbook `architecture-knowledge-lifecycle`, serves the skills through TLC progressive disclosure and runs their scripts offline. Accepted ADRs are immutable and numbers are never reused.
- Historical/runtime evidence (check availability before use): `aeos/registries/skills.architecture-knowledge.additions.yaml`, `aeos/mcps/architecture-knowledge.mcp.yaml`, `aeos/knowledge/architecture-knowledge-map.json`, `tests/node/architecture-knowledge-mcp.test.cjs`
- Updated: 2026-10-07

### TypeSafe Jev function-calling skill
- Status: retained instruction knowledge; removed runtime pointers are historical
- Fact: Upstream `typesafe-ai` is installed for agent use, and project-native `jev-call-expert` governs confidence-aware natural-language dispatch into allowlisted typed functions. Jev supplies bounded Choice/Noul judgments; code retains validation, defaults, authorization, confirmation and invocation.
- Historical/runtime evidence (check availability before use): `.agents/skills/typesafe-ai/SKILL.md`, `00_skills/(development)/jev-call-expert/SKILL.md`, `aeos/registries/skills.typesafe.additions.yaml`
- Updated: 2026-09-17

### Canonical agent identity
- Status: retained instruction knowledge; removed runtime pointers are historical
- Fact: AEOS has exactly one agent identity: `codenavi-agent`; specialization belongs to skills, playbooks, MCPs, LSPs/LCPs, lenses and tools.
- Historical/runtime evidence (check availability before use): `AGENT.md`, `aeos/registries/agents.registry.yaml`
- Updated: 2026-09-09

### Canonical mission lifecycle
- Status: active
- Fact: Material missions follow `BRIEFING → RECON → PLAN → EXECUTE → VERIFY → DEBRIEF`.
- Evidence: `AGENT.md`
- Updated: 2026-09-09

### Continuity quartet
- Status: active
- Fact: Material work uses `.notebook/HANDOFF.md`, `.notebook/MEMORY.md`, `.notebook/PROGRESS.md` and `.notebook/LEARNING.md` with non-overlapping responsibilities.
- Evidence: `references/CODENAVI_CONTINUITY_STANDARD.md`
- Updated: 2026-09-09

### Universal runtime authentication
- Status: active
- Fact: Every resolved AEOS playbook can access core `runtime-auth` and `runtime-http`; skills exchange opaque runtime session references rather than raw cookies/tokens/passwords. External cookie files may be consumed in place but credential contents never enter persisted/model-facing artifacts.
- Evidence: `references/CODENAVI_RUNTIME_AUTH_STANDARD.md`, `runtime/src/kernel/runtime-auth-broker.ts`, `runtime/src/kernel/registry-loader.ts`
- Updated: 2026-09-11

### Overlay registries are runtime-active
- Status: active
- Fact: Runtime loading of skills, playbooks, MCPs and LCPs resolves active fragments from `overlay.registry.index.yaml`; overlay-only entries are not documentation-only.
- Evidence: `runtime/src/kernel/registry-loader.ts`, `tests/node/runtime-auth-broker.test.cjs`
- Updated: 2026-09-11

### WordPress complete plugin universe
- Status: active
- Fact: `wordpress-expert` inventories and operates every plugin in `wp-content/plugins` and `wp-content/mu-plugins` (regular, must-use, single-file; active and inactive). A static catalog is not a ceiling. `kinghost-wordpress-publish` uploads those full plugin trees with the theme.
- Evidence: `00_skills/(development)/wordpress-expert/PLUGINS.md`, `kinghost-control-mcp/wordpress-ops.mjs:listLocalWordpressPlugins`, `wordpress_knowledge.plugin_universe_plan`
- Updated: 2026-09-16

### WordPress first-run Beta Mapping
- Status: retained instruction knowledge; removed runtime pointers are historical
- Fact: `wordpress-expert` performs a full read-only Beta Mapping only when no valid consolidated site map exists. Later runs reuse the map and use lightweight drift/preflight; full remap requires explicit request or invalid/corrupt map.
- Historical/runtime evidence (check availability before use): `00_skills/(development)/wordpress-expert/BETA_MAPPING.md`, `aeos/playbooks/wordpress-expert-site-lifecycle.playbook.md`
- Updated: 2026-09-11

### WordPress knowledge authority
- Status: retained instruction knowledge; removed runtime pointers are historical
- Fact: Official WordPress developer/project documentation is normative for API/security semantics; Reddit is retained as non-normative community evidence for operational experience, edge cases and failure patterns.
- Historical/runtime evidence (check availability before use): `aeos/mcps/wordpress-knowledge.mcp.yaml`, `aeos/mcp-servers/wordpress-knowledge-mcp.mjs`
- Updated: 2026-09-11

### Rei do ABC WordPress clone anchor
- Status: active
- Fact: `https://reidoabc.com.br` maps to site id `3015e2f77281a57c0f638d5ae2f64ed86a7694fbe018bbe926f36319d945d6d5`; its local working clone path is `E:\GitHub\repos-workspace\reidoabc`.
- Evidence: `.aeos/wordpress/sites/3015e2f77281a57c0f638d5ae2f64ed86a7694fbe018bbe926f36319d945d6d5/beta-map.json`, `E:\GitHub\repos-workspace\reidoabc\README.md`
- Updated: 2026-09-11

### Rei do ABC full local WordPress runtime
- Status: active
- Fact: `E:\GitHub\repos-workspace\reidoabc` is the complete local WordPress/WooCommerce evaluation runtime, using PHP 8.5, MySQL 8.4 and the black-and-gold `reidoabc-gourmet-reference` theme. `E:\GitHub\repos-workspace\reidoabc-wordpress` is the preserved reference package, not the runtime target. Neither is deployed to KingHost.
- Evidence: `E:\GitHub\repos-workspace\reidoabc\README.md`, `E:\GitHub\repos-workspace\reidoabc\docs\reference-gourmet-mobile.png`, `.notebook\PROGRESS.md`
- Updated: 2026-09-12

### DevOps workflow guardians
- Status: active
- Fact: GitHub Actions specialization must not recreate subagent identities. Per-workflow coverage uses `WorkflowGuardianLens`; per-job/matrix coverage uses `JobGuardianWorkUnit`, all owned by `codenavi-agent`.
- Evidence: `00_skills/(cloud)/devops-pipeline-engineering/SKILL.md`, `00_skills/(tooling)/github-operations/actions/GUARDIANS.md`
- Updated: 2026-09-11

### Latest-SHA CI truth
- Status: active
- Fact: GitHub API HTTP success is not pipeline success. Merge evidence is valid only when all repository-required Actions/jobs/checks for the current expected head SHA are terminal and successful; corrective pushes invalidate prior-SHA CI evidence.
- Evidence: `scripts/aeos-devops-pipeline-governance.mjs`, `00_skills/(cloud)/devops-pipeline-engineering/SKILL.md`
- Updated: 2026-09-11

### Repository deletion policy
- Status: active
- Fact: AEOS permanently denies repository deletion even for owner/admin requests. Deletion is manual-only outside AEOS and cannot be approved, delegated or automated.
- Evidence: `00_skills/(tooling)/github-operations/SKILL.md`, `00_skills/(cloud)/devops-pipeline-engineering/PERMISSIONS.yaml`
- Updated: 2026-09-11

### GitHub credential handling
- Status: active
- Fact: PAT/secret values are runtime-only; tracked configuration contains references, not values. GitHub credentials never enter model context, Token Manager, evidence, notebook or Git bundles.
- Evidence: `00_skills/(tooling)/github-operations/SKILL.md`, `00_skills/(tooling)/github-operations/POLICY.md`
- Updated: 2026-09-11

### Python is allowed in the workspace
- Status: active
- Fact: The zero-Python inventory policy is retired. Python source and project metadata are allowed. Skill-local `*.py` validators are first-class. AEOS kernel/runtime orchestration remains Node/TypeScript unless a later mission changes that surface.
- Evidence: `references/PYTHON_WORKSPACE_POLICY.md`, `scripts/aeos-python-workspace-guard.mjs`
- Updated: 2026-09-12

### Spec-driven feature skills assimilated
- Status: retained instruction knowledge; removed runtime pointers are historical
- Fact: Installed Tech Lead's Club `tlc-spec-driven` 3.3.0 and `tlc-spec-lean` 1.0.0 are governed AEOS skills `spec-driven` and `spec-driven-lean`, owned by `codenavi-agent`. Source sub-agent roles are lenses. `specs` remains the mutating preflight. Overlay fragment: `aeos/registries/skills.spec-driven.additions.yaml`.
- Historical/runtime evidence (check availability before use): `00_skills/(development)/spec-driven/SKILL.md`, `00_skills/(development)/spec-driven-lean/SKILL.md`, `aeos/registries/overlay.registry.index.yaml`
- Updated: 2026-09-12

### KingHost one-command WordPress publish
- Status: retained instruction knowledge; removed runtime pointers are historical
- Fact: Playbook `kinghost-wordpress-publish` publishes a locally altered WordPress/PHP/WooCommerce tree onto an already-hosted KingHost domain via `npm run aeos:kinghost:publish`. Default APPLY is scoped `wp-content` code. Live orders, customers, `siteurl`/`home`, payment secrets and `wp-config.php` stay on production. `--replace-database` is blocked on this path.
- Historical/runtime evidence (check availability before use): `aeos/playbooks/kinghost-wordpress-publish.playbook.md`, `scripts/aeos-kinghost-publish.mjs`, `kinghost-control-mcp/index.mjs:publishPreflight`
- Updated: 2026-09-16

### KingHost control MCP and expert super-skill
- Status: retained instruction knowledge; removed runtime pointers are historical
- Fact: `kinghost-control` is the KingHost Hospedagem control plane: cookie-jar panel login, existing domain list/select, already-created user inventory (redacted), WordPress/PHP/MySQL/WooCommerce, site clone and FTP tree publish. `kinghost-expert` governs the production FSM. Passwords and cookie values are never persisted or returned to the model. `kinghost-commerce` remains the SSH/SFTP/Postgres commerce adapter.
- Historical/runtime evidence (check availability before use): `aeos/mcps/kinghost-control.mcp.yaml`, `00_skills/(cloud)/kinghost-expert/SKILL.md`, `kinghost-control-mcp/index.mjs`, `kinghost-control-mcp/knowledge.mjs`
- Updated: 2026-09-16

### TLC catalog skills copied into the workspace
- Status: retained instruction knowledge; removed runtime pointers are historical
- Fact: Installed TLC skills `not-your-babysitter`, `cursor-subagent-creator`, `subagent-creator`, `skill-architect`, `technical-design-doc-creator`, `best-practices`, `the-fool`, `the-jury`, `ai-seo`, `nx-workspace`, `tlc-plan`, `learning-opportunities`, `perf-astro`, `core-web-vitals`, `perf-lighthouse`, `perf-web-optimization`, `security-best-practices`, `security-ownership-map`, `security-threat-model` and `web-quality-audit` live under `skills/` and overlay fragment `aeos/registries/skills.tlc-catalog.additions.yaml`. All are owned by `codenavi-agent`. `cursor-subagent-creator`, `subagent-creator` and `the-jury` remap source subagents to lenses; they must not register another agent identity. Session teaching from `learning-opportunities` is not a LEARNING.md promotion unless `learning-curator` verifies it. `security-audit` / `threat-modeler` remain the existing AEOS audit playbooks; the TLC trio does not replace them.
- Historical/runtime evidence (check availability before use): `aeos/registries/skills.tlc-catalog.additions.yaml`, `00_skills/(creation)/cursor-subagent-creator/SKILL.md`, `00_skills/(decision-making)/the-jury/SKILL.md`
- Updated: 2026-09-12

### Kotlin current-stable language expert
- Status: retained instruction knowledge; removed runtime pointers are historical
- Fact: `kotlin-expert` follows the `java-21-expert` skill contract and loads current stable Kotlin through `docs-kotlin-current`. Resolved version is Kotlin 2.4.20. The MCP is governed by `kotlin-expert`.
- Historical/runtime evidence (check availability before use): `00_skills/(development)/kotlin-expert/SKILL.md`, `aeos/mcps/docs-kotlin-current.mcp.yaml`, `aeos/docs/sources/language-docs.registry.yaml`
- Updated: 2026-09-13

### Open PRs require a Why/Porquê section
- Status: active
- Fact: Every open pull request must describe why the change exists. `github-operations` and `devops-pipeline-engineering` block PR create/update/merge when Why/Porquê is missing, empty or a placeholder. The gate exists so later worktrees keep adequate context. Executable check: `scripts/aeos-devops-pipeline-governance.mjs` `evaluatePrWhy()` / `mergeReadiness()`.
- Evidence: `00_skills/(tooling)/github-operations/SKILL.md`, `00_skills/(cloud)/devops-pipeline-engineering/SKILL.md`, `scripts/aeos-devops-pipeline-governance.mjs`, `.github/PULL_REQUEST_TEMPLATE.md`
- Updated: 2026-09-13

### RAG Node.js MCP stores the TLC repository's causal model
- Status: retained instruction knowledge; removed runtime pointers are historical
- Fact: `rag-node` is the governed offline Node.js/Express RAG MCP. Its 1.1.0 knowledge map derives from all 22 files and 12 commits of TLC source repo `odanieldcs/rag-api` at `27f7aab`, classifies it as 2-Step RAG, records why each indexing/query/serving step exists, and separates the educational baseline from current production guidance backed by official LangChain, OpenAI, Qdrant, MDN and Express docs.
- Historical/runtime evidence (check availability before use): `aeos/knowledge/rag-node-course-map.json`, `aeos/mcps/rag-node.mcp.yaml`, `aeos/mcp-servers/rag-node-mcp.mjs`, `tests/node/rag-node-mcp.test.cjs`
- Updated: 2026-09-18

### Dark-videos creative runtime contracts
- Durable creative/worker contracts are recorded in D:/Git/dark-videos/.notebook/MEMORY.md; source and verification pointer: `.work/creative-repair/RESULTADO.md`. The local model provider input modality was verified with actual image calls; text-model availability alone does not establish visual review capability.
- Updated: 2026-10-13

### Dark-videos scheduled publication contracts
Updated:2026-10-13
Entry point: D:/Git/dark-videos/.notebook/MEMORY.md
- Validated transaction/renderer/child-job contracts and source pointers live in the target notebook. Verified correction and functional charter: .work/publishing-fix/RESULTADO.md; .work/publishing-fix/state.json.

### Agenda distinguishes the queue from blocked history
Updated:2026-10-13
Entry point: backend/app/modules/publishing/api.py:schedule
- `publications` contains up to100 nonblocked upcoming rows; `blocked_publications` holds up to100 historical blocked rows separately. `upcoming_counts` spans the full eligible-status queue and `blocked_count` spans all blocked rows. The frontend marks blocked dates as previous schedules and offers no publishing action for them.
- Language admission checks ORIGINAL source title OR description, not the generated publishing copy. Confirmed by user; current code mining/metadata_policy.py and dispatch.py:_job.
- Evidence: E:/Github/ai-assistent-universal-coder/.work/youtube-unblock/RESULTADO.md; test_schedule_history.py and schedule/page.test.tsx.

### Asynchronous YouTube processing receipt
Updated:2026-10-13
Entry point: backend/app/modules/publishing/browser_post.py:_click_done/_youtube_dialog
- The processing notice can remain open after the Public save; receipt timing and shadow roots must be observed throughout the completion window. It is not publication proof: the same captured media ID must pass owned-channel Public/metadata confirmation. Capture is nonblocking because some flows expose the link only after save.
- Evidence: E:/Github/ai-assistent-universal-coder/.work/youtube-publish-now/RESULTADO.md; test_youtube_processing.py and receipt_applied-processing-tests.json. Final real-upload behavior remains a separate verification gate.













<!-- RGL-IMPLEMENTATION -->
### Source-backed GraphRAG + Laya capability
- Status: local runtime/protocol verified, not production-effectiveness certification.
- Fact: rag-graph-laya-mcp is a standalone official-SDK MCP with local Graphiti/Neo4j visualization, typed Laya decisions and separate RLCD/QLoRA experiments. One local API owns jobs/model state; clients do not duplicate GPU runtimes.
- Decision: source acquisition, source analysis, graph indexing, training and human-reviewed quality are distinct evidence states. No automatic model promotion; uncalibrated/truncated Laya decisions retain hybrid fallback.
- Evidence: rag-graph-laya-mcp/README.md, app/contracts.py, verification.json, quality/capabilities.json; focused note rag-graph-laya.md.
- Updated:2026-10-15
<!-- /RGL-IMPLEMENTATION -->

<!-- RGL-MONGO-REVIEW -->
### MongoDB corpus and technical MCP remain distinct
- Fact: rag-graph-laya-mcp currently uses its technical source catalog/SQLite/Graphiti; no MongoDB ingestion connector is implied by the read-only MongoDB review script.
- Decision: future DiabeticsresearchJEV integration must preserve document/version/source identity, parent eligibility and purpose-specific rights. Technical synthetic calibration does not establish biomedical task calibration.
- Evidence: rag-graph-laya-mcp/app/service.py; docs/mongodb-review/README.md; scripts/review_mongodb.js.
- Updated:2026-10-15
<!-- /RGL-MONGO-REVIEW -->



<!-- RGL-MONGO-FIXES -->
### Applied source-level RAG/ML eligibility contract
- Fact: DiabeticsresearchJEV now revalidates parent acceptance/retraction and source version across retrieval/index/graph; training additionally requires explicit rights, disjoint stable family partitions and current train-only inputs. Smoke cannot silently replace QLoRA or promote a serving adapter.
- Decision: no numeric accuracy is inferred from stored answers or absent probes; comparison/promotion requires actual reviewed runtime evidence. A source-code fix does not connect MongoDB to the separate technical MCP or make an unlicensed corpus trainable.
- Evidence:02_repositorios/DiabeticsresearchJEV/FLOW-HARDENING.md; rag-graph-laya-mcp/docs/mongodb-review/applied-verification.json.
- Updated:2026-10-15
<!-- /RGL-MONGO-FIXES -->


- Política obrigatória desde2026-10-14: dispatch prepara uploads antecipados; somente remote_id e scheduled_for exato retornados pelo Studio autorizam PLATFORM_SCHEDULED/carrier=platform. PENDING/SCHEDULED são reservas locais. Nenhum fallback worker ou publicação imediata em caso de falha. Fontes: publishing/release.py:_release_locked, dispatch.py:_run_dispatch/_write, studio_schedule.py; testes test_platform_schedule.py/test_native_studio_receipts.py.
- TikTok Stories da fila foram convertidos em vídeos normais por autorização explícita (78 registros). Studio pode desativar apenas sua verificação simples opcional por autorização do usuário; copyright e inspeções obrigatórias do projeto permanecem ativos. Fonte: studio_schedule.py:disable_tiktok_optional_check e browser_post.py:_finish_tiktok_scheduled.
- Stories Instagram recusados pelo próprio Studio por duração excessiva podem ser convertidos em Reels por autorização explícita, preservando a mesma mídia já revisada e o horário futuro. Fonte: dispatch.py:_publish; contrato test_platform_schedule.py:test_long_story_retries_same_reviewed_media_as_full_reel. Nenhuma alteração de fonte/inspeção é autorizada por essa conversão.
- Atividade do preparador no Windows exige GetExitCodeProcess==STILL_ACTIVE, além de um handle válido. Um processo encerrado com handle retido não prova atividade. Fonte: publishing/outlive.py:pid_alive; regressão test_platform_schedule.py:test_exited_windows_process_is_not_mistaken_for_a_running_preparer.
- Retenção de fonte inclui publicações FAILED: uma plataforma já agendada não autoriza apagar o original necessário à nova inspeção de outra plataforma. Fonte: mining/acquire.py:_STILL_NEEDED; test_platform_schedule.py:test_original_bytes_survive_a_failed_studio_schedule_until_all_posts_are_saved.
- Copyright TikTok deve ser relido no elemento atual, pois o Studio remonta essa seção. Somente o resultado verde permite agendar; espera expirada mantém bloqueio. Fonte: browser_post.py:_finish_tiktok_scheduled; test_native_studio_receipts.py:test_copyright_review_reads_the_remounted.

<!-- MYPY-SOURCE-IDENTITY -->
### Source-local API startup
- Fact: scripts/run_api.py inserts the checkout src before importing FastAPI; copied editable installs can otherwise resolve a different checkout. Use explicit PYTHONPATH/MYPYPATH for CLI and static checks. Runtime verification compares in-process module paths/hashes with listener identity; health alone does not certify loaded source.
- Evidence:02_repositorios/DiabeticsresearchJEV/scripts/run_api.py; parent workspace rag-graph-laya-mcp/docs/mongodb-review/typing-runtime-verification.json. Updated:2026-10-15.
<!-- /MYPY-SOURCE-IDENTITY -->

---

### Dark-videos / Science Studio: documentário do elétron (pipeline completo, voz Kokoro + mix documental)
Updated: 2026-10-29. Entry point: `.work/electron-descoberta/`.
- Fact: tema "Como o elétron foi descoberto e suas curiosidades que intrigam até hoje", profile short 60 s, PT-BR, 6 cenas (10 s cada), 10 fontes (APS, Royal Institution, Britannica, Millikan 1913, Northwestern EDM/subestrutura, Fermilab g-2, History.com, Wikipedia).
- Fact: correções de código para o `generate` funcionar de forma autônoma:
  * `science-studio/studio.py`: `studio_root()` + `resolve_command()` — caminhos relativos no `providers.json` resolvidos contra a raiz do estúdio quando não existem no diretório do projeto (subprocess roda com `cwd=root`).
  * `science-studio/providers.py` script: tolerância a campos ausentes do JSON do LLM (preenche defaults do `scene_schema`) + coerção de `duration` string→int.
  * `science-studio/studio.py` configure: novo `--voice-engine {piper,kokoro,google}` (+ `--kokoro-python`, `--kokoro-voice`, `--google-voice`); `--voice-model` só é exigido no motor piper.
- Fact: motores de voz do Science Studio (3 adapters, mesmo contrato de áudio `audio/{i:04}.wav` + `scene['audio']`):
  * `science-studio/voice_kokoro.py` — Kokoro-82M PT-BR local/offline/gratuito (pesos Apache-2.0 no cache HF do usuário), vozes `pm_alex` (masculina, padrão do projeto), `pm_santa`, `pf_dora`; ajusta a taxa natural de fala antes de um atempo residual mínimo; ambiente canônico `.work/science-engines/kokoro-venv` (torch 2.11+cu128, CUDA ativo na RTX 5080).
  * `science-studio/voice_google.py` — Google Cloud TTS real (vozes Google da conta); chave só em runtime via `GOOGLE_TTS_API_KEY`, falha fechada sem chave e valida o nome da voz na API (`--list-voices`).
  * `science-studio/providers.py voice` — Piper legado preservado para projetos já vinculados ao modelo `.onnx`.
- Fact: `science-studio/audio_mix.py` — etapa explícita de entrega: EQ + compressor + loudnorm na voz, base musical calma (procedural de 5 harmônicos ou arquivo fornecido) e ducking por `sidechaincompress`; `--in-place` substitui o preview e atualiza `render.json`, de modo que o artefato aprovado e o exportado são os mesmos bytes. Medido no vídeo do elétron: I = -16,0 LUFS, true peak -1,5 dBFS, LRA 1,3 LU.
- Fact: pipeline generate completo executado: research → script → assets (ComfyUI SDXL + BiRefNet matte RGBA) → voice (Kokoro pm_alex) → render preview.mp4 (60,02 s, 1080×1920) → mix documental → review (5 checks) → export. final.mp4 = 46.842.411 bytes, sha256 `920158da8740257a54b4e43add21eae5276a403282a150f26b31ff6406b2a6ed`, approval.json e delivery/final.mp4 com hash idêntico; published=false.
- REGRA OPERACIONAL (obrigatória): TODA VEZ que criar/salvar um vídeo do dark-videos/Science Studio, o destino padrão é `D:\Git\dark-videos`. A entrega deste projeto foi copiada para `D:\Git\dark-videos\.work\electron-descoberta\` (delivery + `voices/{pm_alex,pm_santa,pf_dora}.wav` para A/B + `copy-report.json`).
- Limites honestos: não há ferramenta "nemontron-voicechat" no ambiente (nemotron/NVIDIA é família de LLM, sem TTS de clonagem); clonar a voz real de narradores de YouTube sem autorização foi descartado por direitos/consentimento; a voz Google autêntica depende de chave da conta do usuário (o free tier do Google Cloud TTS exige conta/cobrança habilitada); o YouTube não é acessível para análise dos 16 vídeos de referência; Kokoro é voz sintética genérica de altíssima fidelidade, não uma cópia de locutor específico; a aprovação auditiva final continua sendo do operador.
- Artefatos: `.work/electron-descoberta/{sources.json,project.json,providers.json,workflow-background.json,workflow-foreground.json,stages.json,audio_postprocess.py}` e `.work/electron-descoberta/delivery/{final.mp4,subtitles.srt,project.json,approval.json,handoff.json}`.

---
### Science Studio: normalizador de pronúncia PT-BR (narração documental fluida)
Updated: 2026-10-30. Entry point: `science-studio/ptbr_pronunciation.py`.
- Fact: novo módulo `normalize_for_speech(texto, language='pt-BR')` converte escrita para forma falada naturalmente em PT-BR, sem jamais trocar o idioma (rejeita qualquer outro). Regras: anos por extenso (2020 -> dois mil e vinte; 1897 -> mil oitocentos e noventa e sete), bilhões fracionados (13.5bi/13.5 bilhões de anos luz -> treze bilhões e meio de anos luz), iniciais com ponto (Thomas J. J. -> Thomas Jota Jota; G. J. Stoney -> Gê Jiota Stoney; J. J. Thomson -> Jota Jota Thomson), notação científica (1,602 x 10^-19 -> um vírgula seis zero dois vezes dez menos dezenove; 2 x 10^-20 -> duas vezes dez menos vinte), frações (1/1836 -> um sobre mil oitocentos e trinta e seis) e g-2 -> g menos dois.
- Fact: integrado em `science-studio/voice_kokoro.py` e `science-studio/voice_google.py` (normaliza a narração antes da síntese, guarda de idioma pt-BR) e em `science-studio/studio.py:subtitles()` (legendas usam a forma falada para ficar sincronizada com o áudio).
- Fact: vídeo do elétron regenerado com Kokoro pm_alex + normalizador (6 cenas, ratio ~0,998), render, mix documental (I=-16,0 LUFS, ducking), review 5 checks aprovada, export e entrega copiada para `D:\Git\dark-videos\.work\electron-descoberta\` (REGRA OBRIGATÓRIA: todo vídeo dark-videos/Science Studio é salvo em `D:\Git\dark-videos`).
- Limite: voz Google real (`pt-BR-Neural2-B`) exige `GOOGLE_TTS_API_KEY` do operador (falha fechada sem chave); não existe "nemotron-voicechat" (Nemotron = família LLM NVIDIA, sem TTS/clonagem); não se clona narrador real sem autorização; aprovação auditiva final continua do operador.
- Verificação: testes puros de normalização passam (12 exemplos, incluindo todos os citados pelo operador); imports de `studio`, `voice_kokoro`, `voice_google` OK.

---
### Dark-videos / Science Studio: redo do documentário "O elétron" (90 min, 5400 s) (2026-10-30)
Updated: 2026-10-30. Entry point: `D:\Git\dark-videos\.work\electron-descoberta-90min\delivery\`.
- Fact: mesmo pipeline do vídeo de 60 s escalado para 90 min: 90 cenas × 60 s (capítulos 0–8), roteiro reescrito sem repetições (dedup), voz Kokoro pm_alex regenerada em CUDA, render h264 1080×1920 30fps, mix documental (trilha procedural -21dB + ducking sidechain, voz -16.22 LUFS), review 5 checks aprovada, export.
- Fact: defeitos do vídeo anterior corrigidos e verificados: 0 silêncios >1s no mix final (mudo do ~36:11 eliminado); narração sem repetições; nenhum dos 180 assets é jogo/filme/série (auditoria de direitos); música de fundo sempre presente.
- Fact: pontuação final técnica 9.5/10; aprovação artística/final (ouvir/assistir íntegro) cabe ao operador.
- Fact: entrega em `D:\Git\dark-videos\.work\electron-descoberta-90min\delivery\{final.mp4, subtitles.srt, project.json, approval.json, handoff.json}` (REGRA OBRIGATÓRIA: D:\Git\dark-videos). Publicação não executada (publish=false).

---
### DeepSeek V4.1 Flash — contratos de referência
Updated: 2026-10-31. Entry point: `.notebook/graph/deepseek-v41-flash.md`.
- Fact: para o derivado no commit `c19ca5ca4eaeb79d29fdf08aea8327da95b1116a` e a base `1bae0e1088993b9b82de08f59de5be5a34e42170`, o índice de 96.085 tensores tem mapeamento igual; 21 OIDs de shards são iguais e 27 diferentes. Diferença por tensor não foi medida. Evidência: `.aeos/evidence/deepseek-v41-base-compare.json`.
- Fact: a CLI de referência usa 4.096 posições por padrão no modo arquivo e 65.536 no interativo, embora a configuração HF declare 1.048.576; o caminho de geração é autoregressivo. Evidência: `.aeos/evidence/deepseek-v41-reference-contract.json`, `inference/generate.py` e `inference/model.py` no alvo.

- Status superseded (2026-11-01): regras posteriores exigem apenas mídia animada e máximo editorial de 3 s com pessoas; a versão baseada em palestra não é entrega válida. Estado atual em .notebook/HANDOFF.md e PROGRESS.md.

- Correção 2026-11-01: regras posteriores exigem mídia animada e pessoas até 3 s, então a edição de palestra não satisfaz a entrega; estado ativo em .notebook/HANDOFF.md e PROGRESS.md.

- Correção 2026-11-01: requisitos posteriores pedem mídia animada e pessoas até 3 s; render de palestra não satisfaz entrega. Estado atual em .notebook/HANDOFF.md e PROGRESS.md.


### Padrões de governança restaurados (references/)
- Status: active
- Fact: `references/CODENAVI_CONTINUITY_STANDARD.md` e `references/CODENAVI_FULL_WORKSPACE_STANDARD.md` foram restaurados em 2026-11-16 de `faac5adf^` (bytes idênticos; só ponteiros mortos reconciliados) porque o `AGENTS.md` vigente os cita. Harness Track A: 2 quebras → 0. Seguem removidos (reorg 2026-10-12): `CODENAVI_WORKSPACE_STANDARD.md`, `CODENAVI_NOTEBOOK_SPEC.md`, `CODENAVI_RUNTIME_AUTH_STANDARD.md` e `AGENT.md` raiz.
- Decision: refina "preservar remoções externas": restaura-se apenas o que o `AGENTS.md` atual exige; `AGENTS.md` não foi editado.
- Evidence: `.harness-eval/runs/2026-11-16-fix1/04-correctness.md`, `references/`.
- Updated: 2026-11-16

### skills-quality-eval (qualidade por skill)
- Status: active
- Fact: 324 skills canônicas + 3 aliases declarados em `catalog.json` (`accessibility`, `best-practices`, `technical-design-doc-creator`) = 327 ponteiros; não é defeito. Roteamento para `references/` (>=2 links) em 306/324 (94,4%), medido em código; 18 sem roteamento listados em `.work/skills-quality-eval/eval-report-v2.json`.
- Fact: JEV vs rótulos prata em amostras novas de 60: `gov_codenavi` 1,00, `provenance_pointer` 0,88, `fail_closed` 1,00 (holdout 1); `secrets_runtime_only` 1,00 com 44 aprovações (holdout 2, após emenda A2). Limite: rótulos feitos pelo mesmo agente; só 2 negativos verdadeiros em `secrets_runtime_only`.
- Evidence: `.specs/skills-quality-eval/rubric.md` (A1, A2), `.work/skills-quality-eval/{eval-report-v2,eval-report-v3}.json`.
- Updated: 2026-11-16
