## TLC spec versions — PR e merge autorizados

Updated: 2026-10-26. Entry point: `.notebook/tlc-spec-versions.md`.
Working set: quatro pacotes spec-driven/lean, fontes, descoberta e metadados relacionados.
Próximo passo: validar o candidato, publicar PR com Why, verificar os checks, integrar na master e verificar o SHA final. Alterações locais de outras tarefas ficam fora do PR.

---

# Handoff ativo: agendamento obrigatório nos Studios
Updated: 2026-10-14
Entry point: E:/Github/ai-assistent-universal-coder/.work/studio-scheduling/PROGRESS.md

- Usuário exige salvamento antecipado dentro dos Studios. Reservas locais não são agendamentos confirmados. Fallback worker/imediato removido; 112 marcadores ativos retirados; histórico preservado.
- 78 Stories TikTok convertidos em vídeos normais por autorização. Usuário autorizou desligar somente a verificação simples opcional do Studio; direitos autorais e gates do dark-videos continuam obrigatórios.
- Recibos confirmados no snapshot 2026-10-14T23:30:25.634727+00:00: 56; conjunto de IDs/data/hora/carrier em .work/studio-scheduling/queue-state.json. Pilotos: YT CXbOhtFIAc4 para15/10 18h; Reel2217587485455644 para22/10 18h; TikTok7696588738721221894 para14/10 16:05; Story1332840945473219 para14/10 20h. Readbacks independentes em *-reconciled.json/verified-native-times.json. Nunca reenviar IDs confirmados.
- 16 arquivos de código/testes instalados com hashes e backups. Suíte focada instalada: 51 checks backend passaram (exit_code=0); frontend17, TypeScript74, mypy11 e Ruff passaram. Suíte completa do projeto não foi executada.
- Corrigido PID Windows falso-ativo: pid_alive consulta GetExitCodeProcess/STILL_ACTIVE; regressão com subprocesso encerrado passou. Correções do lote: switch TikTok remonta após toggle; editor anterior só é descartado se corresponder a registro inativo próprio, sem excluir posts; Meta usa legenda completa do checkbox e busca nativa, não título abreviado. Readbacks ampliados para listas virtualizadas.
- Usuário autorizou converter apenas Stories longos recusados pelo Meta em Reels, preservando bytes/horário. Implementado em dispatch._publish; não corta mídia nem bypassa gates. 07694f convertido e depois recusado por existing_source_frame; permanece bloqueado. Stories aceitos continuam Stories, com receipt própria.
- API/Next/PostgreSQL/Redis ativos. Preparador nativo existente em background PID46568, alive=True; somente uploads antecipados, sem publicação por horário local. 90 elegíveis disponíveis; 159 reservas/falhas ainda sem confirmação; 0 marcadores worker ativos. Quota YouTube observada até15/10 11:52:55 São Paulo; fonte/review indisponíveis continuam recusados.
- Próximos: observar o escoamento via queue_state.py; investigar falhas sem replay cego; confirmar limites/recibos restantes e atualizar relatório. Não afirmar todos salvos enquanto houver reservas. Instruções de publicação due-time e PIDs abaixo são históricos supersedidos.

## Histórico:

# Esteira TLC de capacidades — 2026-10-14
Entry point: quality/README.md; .notebook/capability-ci.md
- Implementação/gates completos:305 skills/308 descoberta/94TLC, catalog/distribution/hash/syntax PASS e42 testes adversariais/protocolo. Checkout Git exato e CI Linux PASS; baseline anterior tinha441 erros de hash e3 helpers sem modo executável. AGENTS.md preservado.
- User escolheu incorporação automática: novos pacotes e updates de auto-imports sem alterações locais, depois de candidato isolado e gates; publisher separado apenas para paths permitidos, push normal. Diariamente09:23UTC; regras desconhecidas/erro de rede bloqueiam atualização. TLC consultado7f93bf3b; demo/tlc-prd incorporados e mapa histórico antes órfão registrado.
- Inventário real:1adaptador KingHost com self-test,3pacotes MCP em quarentena,0LSP instalados. Não afirmar conformidade de protocolos desses pacotes nem eficácia de305 skills em produção.
- Publicado/integrado6734c51c: CI38654364112 terminal success. CI inicial38650490307 e manutenção manual38650523248 também success; o bot publicou d81f3de6 atualizando a observação TLC6e7a50e7. Essa mudança remota foi integrada por merge normal antes do push corretivo, mantendo3 modos executáveis100755. Sem pendência da esteira solicitada; monitor diário bloqueia novidades incompatíveis ou falhas de fonte. Missões de aplicações abaixo permanecem independentes.

## Histórico:

## Histórico:

# Merge local da branch principal — 2026-10-14
Entry point: .notebook/PROGRESS.md:Merge da branch principal
- Merge solicitado concluído: principal remoto é master; main não existe. git merge origin/master retornou Already up to date. HEAD/origin/master8333fedaec27f0353a3a54e5403350b1bcfa3401.
- Nenhum add/commit/reset/checkout/push feito por esta missão. Índice mudou por atividade externa durante a inspeção; arquivos preparados devem ser revisados pelo responsável antes de qualquer commit. Verificações amplas de fixtures tiveram restrições de acesso; não inferir checkout limpo.
- Sem pendência do merge. Missão de agendamento abaixo permanece independente.

 publish approved YouTube videos now
Updated:2026-10-13
Entry point: E:/Github/ai-assistent-universal-coder/.work/youtube-publish-now/RESULTADO.md

- User explicitly requested immediate publication of the previously verified34 YouTube records. Result:3Public/anonymous-playable,27scheduled,1failed quota,3inspection blocks (2existing frame/1review unavailable). The42 earlier blocks and3 historical drafts were preserved; other networks were outside this batch.
- Public IDs:uXL9BtCVX3g, VTl3NwRnsuY,03_17P98KIg; exact metadata and ownership verified in Studio. Two false failures were reconciled to already-public IDs via native retry; no duplicate upload.
- YouTube account cooldown in the app ends2026-10-14 21:36:44 America/Sao_Paulo. Native dispatcher last verified alive PID35980. Keep the27 queued; retry the quota-failed record through the native endpoint after rechecking eligibility. Do not blindly repeat published IDs or bypass source gates.
- browser_post.py now handles asynchronous processing receipts across shadow roots and confirms exact public metadata.74 final browser/helper checks and Ruff/mypy pass;5 older expanded fixture failures reproduced unchanged with original source. No fresh upload with the final patch was proven because of source refusal/quota; controlled delayed-receipt browser check passed.
- Next: confirm later queue outcomes and native-worker liveness; resume the28 pending after cooldown; revalidate temporary vision failure only after provider evidence changes. Existing-frame sources remain blocked. Full34 publication is still externally limited.

# Handoff: YouTube queue and blocked history
Updated:2026-10-13
Entry point: E:/Github/ai-assistent-universal-coder/.work/youtube-unblock/RESULTADO.md

- User confirmed source-original pt-BR title OR description; foreign-language and existing-frame refusals remain enforced.
-34 YouTube posts scheduled13/10 21h through22/10 08h, all future/prime/real, source-admitted and duplicate-free. No approved YouTube-copy item is missing its publication row; zero reactivations or new uploads in this mission.
-39 historical YouTube blocks:36 language/3 variants of one framed source. Instagram has3 language blocks. API now returns blocked_publications separately from the100 upcoming rows and reports full queue counts; frontend displays separate collapsed history and original-source language explanation.
-80 native tests,17 frontend tests, static checks and real Edge/Chromium UI/API/blocked409 guards passed. API refreshed; scheduler PID25748 preserved. Evidence in report and JSON artifacts.
- Next: observe scheduled dispatch outcomes; only reconsider a refused source when original evidence changes. Future remote uploads and a fresh-byte reinspection of the unavailable framed source are not claimed complete.

# Handoff: publishing repair and scheduled posts
Updated:2026-10-13
Entry point: E:/Github/ai-assistent-universal-coder/.work/publishing-fix/RESULTADO.md

- 216 future posts:98 Instagram,98 TikTok,20 YouTube; zero duplicate account/time and all prime slots. First18h YouTube item confirmed PUBLIC18:02:08 at rYg2JmlF_Ug. Seven current drafts reconciled; three old drafts preserved.
- Recovery run ac7d5e6c-0a58-444b-943a-9ea4326c85f2 succeeded.121 remaining sources accounted for;15 extra source packages recovered across two passes.106 source refusals and42 historical blocked publications remain; do not bypass their current language/source gates.
- Native scheduler active (actual pid9972 at final verification), API/frontend and pipeline worker healthy. Earlier publisher stop boundary is superseded by this user's scheduled-publication authorization; bulk runner/beat were not resumed. Refresh process evidence before any later reload. Continue through native dispatch at due times; no early Postar agora.
- Next: independently confirm later scheduled outcomes, revalidate temporary visual/provider failures only when evidence changes, preserve known draft IDs and current source-byte gates. Final source/runtime/charter evidence is in the report; broader source cleanup remains a separate historical task.

## Previous handoff (historical state)
# Latest handoff: publishing diagnostic
Updated: 2026-10-13
Entry point: `.work/publishing-monitor/RESULTADO.md`.

- Diagnosis complete; app untouched. Last observed16:23 local: current pipeline worker active,20 packages/60 copies,184 Stories; schedule running since15:41 holding its transaction;91 generic Story failures, individual causes unavailable.
- Agenda43 legacy origin_unknown blocks from2026-10-12:39 fail current pt-BR metadata,4 pass metadata but all content rejected. No automatic bulk reactivation justified.
- Next implementation scope if requested: move Story acquisition/inspection outside schedule reservation transaction, add actionable failure/progress reporting, revalidate old quarantine through all current gates. API/DB/Redis healthy; frontend3000 became unavailable during observation, cause unverified. Snapshots and source pointers in report. Prior application/catalog missions retained below.

## Previous handoff
# Latest handoff: dark-videos creative repair
Updated: 2026-10-13
Entry point: `.work/creative-repair/RESULTADO.md`.

- Local correction applied and verified; API and pipeline-only worker ready. Detailed operational continuity is `D:/Git/dark-videos/.notebook/HANDOFF.md`. No full candidate replay or publication. Previous application constraints remain in that notebook.

## Previous handoff
# HANDOFF

Updated: 2026-10-13
Entry point: `07_mapeamentos/repositorios-skills/README.md`; mapping continuity: `repositorios-skills.md`. Prior catalog/application work remains recorded below.

## Latest verified mission: repositórios × skills
- Concluído: 11 diretórios de `02_repositorios`, dez com Git próprio e um pacote; 302 skills canônicas e 3.322 decisões. Análise estática seletiva, com 529 ponteiros em 150 arquivos; 5.736 arquivos no inventário delimitado/167 entradas excluídas/zero erros.
- Entrega: `07_mapeamentos/repositorios-skills/{README.md,relatorio.html,mapa.json,matriz.csv,repositorios/}`. Evidências e scripts de regeneração no mesmo pacote; continuidade própria em `.notebook/` do pacote.
- Verificado: fontes citadas/skills por SHA-256 e inventário por metadados preservados; links/coverage válidos e duas regenerações byte-idênticas.23 verificações no Edge/Chromium via file:// passam, incluindo CSV real e ausência de rede.
- Limites: runtime/produção/MCP, CVE/EOL e suites dos projetos não verificados. Go/Flutter/PowerShell/Svelte/n8n/C++/Swift sem especialistas canônicos; Flame e stubs do iBunny separados de intenção documental. Não tratar API LAYA como a aplicação local laya.
- Sem pendência desta entrega. Atualizar o pacote se fontes/catálogo mudarem; missão BETA/RAG/fine-tuning preexistente em PROGRESS permanece independente. Nenhum projeto/skill alterado, instalação, execução de manutenção, treino, publicação ou commit/push.

## Latest verified mission: skills and folders from new Drive images
- Completed the authorized local update from 77 images IMG_2700–IMG_2776 in folder `1xB9o93nQlLUGB7utNVXPVIIUYcV4K4Tn`; all downloaded/OCR/visually inspected, safe ID/hash accounting in `00_skills/images.2026-10-13.manifest.json`.
- 302 canonical packages / 305 native discovery entries; 827 SKILL.md entrypoints, max99 physical lines; 2,872 operative links; zero structural errors/warnings. Impeccable4.1.1 pinned/licensed with local sequential lenses. All777 TLC resources unchanged; AGENTS.md byte-identical, no missing/unrelated baseline resource changes. Source-derived numbered folders and pending-contract skill folders documented in `00_skills/PHOTO-STRUCTURE.md`.
- 30 actual CLI/FFmpeg/Chromium fixture checks and107 JavaScript syntax checks pass. Supplemental validator rejects duplicated photo IDs. Media helpers implement the photographed contracts locally; Whisper/torch/Resemblyzer/sklearn are absent, so real recognition/speaker quality was not verified or claimed. Official Santander fonts/logo and corporate contracts/access remain unprovided; no fabricated assets/providers.
- Evidence: `00_skills/{validation.report.json,photo-update-verification.json,PHOTO-UPDATE.md}`; scoped backups/acquisition/helpers in ignored `.tools/photo-update/`; requirements `.specs/skills-images-2026-10-13/SPEC.md`.
- No pending local update action. At future audio use, resolve approved engine/model prerequisites and verify the actual recording; at future name-only skill activation, obtain its actual contract. Do not treat sequential self-review as independently blind cognition. No commits/pushes, hooks, model downloads or external publication performed.

## Previous verified mission: prepared mining package applied
- Applied37 manifest files to D:/Git/dark-videos;497 unrelated files and other .env fields preserved. langdetect1.0.9 installed; budget600/cap500/workers4 loaded. Baseline45; installed suite197 passed, plus10 legacy fake-media scenarios on explicit fixture-aware replay. Ruff/mypy/74-file TypeScript pass. Local API reloaded, database/Redis HTTP readiness healthy. Evidence: `.work/mining-apply/RESULTADO.md`.
- Authorized package changes admission to title OR description pt-BR, with proven Asian origin blocked and mandatory unframed-source inspection. Supersedes historical Americas-only admission below. No new publication, quarantine reactivation or draft deletion. Remote-vision/edit/schedule full-cycle validation remains separate; sources can be unavailable.

## Previous verified mission: real YouTube validation
- PASS: native app HTTP, Studio and anonymous playback confirm https://youtube.com/shorts/A33R_kGmOVc published/PUBLIC, matching nonempty metadata. One unique upload; same item resumed/reconciled, no duplicates/deletions. Three old drafts deliberately preserved per user choice, independently rechecked.
- Verified original Estado de Minas BH clip; only one source received BR/source_review. Native creative/schedule gates pass. Fixed Dailymotion URL reconstruction, trailing editor newline, known-ID resume, success-share confirmation and already-public reconciliation.14 Chromium contracts and84 native checks verified, Ruff/mypy/final hashes pass.
- Frozen charter96e9eb14fd84e0c1bc4ed0e0b910134d186502ae8b06013f2683b2ed923674dc passed. Evidence/result: `.work/youtube-recovery/{RESULTADO.md,final-result.json,state.json,remote-verification.json,final-manifest.json}`. API left healthy; bulk stopped, frontend closed. No remaining live validation for this task; broader origin cleanup is separate, and user chose retaining the three drafts.

## Previous checkpoint: YouTube metadata correction
- Applied scoped Studio correction in dark-videos, preserving other changes and Americas guard. Seven original browser failures reproduced; eight Chromium contracts pass. Native171 pass/one identical baseline Instagram fake failure; Ruff/mypy pass. Three applied file hashes match and fresh import succeeds.
- Current Studio: six Public rows and three interrupted drafts; opened draft title framed/description empty. No remote writes. Application services stopped at verification; reopen to load fixed code. No live full upload claimed without origin-proven content; old draft attribution/recovery remains open.
- Evidence: `.work/youtube-metadata/{RESULTADO.md,manifest.json,browser-baseline.json,browser-result.json,native-baseline.json,native-result.json,static-result.json,runtime-result.json}`. Next actions: application HANDOFF; retain unknown-origin quarantine and stopped bulk publisher.

## Previous open mission: Americas-only sources
- User narrowed ALL authorization: eliminate content outside the Americas; no non-American-origin publication permitted. Bulk runner and native detached/Celery publicadores stopped immediately. Latest ledger37IG/40TT recorded published,43 pending/failed; no active publishing rows at inspected checkpoint. YouTube remains0 new uploads, quota409.
-120 entries reference19 sources; no country evidence. Origin guard deployed at rank/admit, legacy framing/backfill, schedule/release and dispatch before media, with persisted provenance.43 rows blocked/origin_unknown,40 content items/40 selections rejected.64 native checks plus lint/types/frontend typecheck passed; actual app200/selected0/43blocked and manual post-now/retry409 without new attempt. Desktop/API/frontend reloaded; no restart of the owned bulk/detached sender.
- Earlier Studio snapshot showed9 Shorts drafts/no published videos; superseded by 2026-10-13 six Public rows/three drafts. No remote deletion yet: pending user identification whether those9 are the Indian clips to remove, plus country criterion (verified filming/original-source proof versus declared creator country). Do not guess geography or delete unknown-origin posts.
- Working set/evidence: `.work/americas-only/{progress.md,manifest.json,quarantine-result.json,native-http-evidence.jsonl,app-probe.json,live-refusal.json,youtube-inventory.json,RESUME.md}`. Frozen guard checks pass; cleanup remains open. Next: resolve pending identification, remove verified outside material and re-run the unchanged cleanup check. Preserve credentials/user changes; no blind resumption of publish.py.
- Final reload confirmed desktop23540/API/frontend live; all15 manifest after_sha256 hashes match. Debrief: `.work/americas-only/RESULTADO.md`. Before admitting new YouTube items, preserve the original observed cooldown: quarantine replaced failed quota markers with origin_unknown; original history remains in quarantine-result.json and live-publish evidence.

## Previous mission: publish ALL through the real app
- User explicitly authorized all existing publications as a real functional test. Inventory 120 rows; Agenda UI exposes 100. Credentials stay in runtime memory.
- Real app failures reproduced and corrected: partial Post matched feed Repost; exact visible selectors passed94 native checks and live Create/file input. Known Reels information notice then blocked Crop/Next; scoped acknowledgement passed15 relevant checks/types/style and subsequent real Instagram upload was independently confirmed on the account.
- Serial120-item runner stopped on the newer geographic restriction. Current progress: `.work/live-publish/inventory-current.json`; raw redacted results in `attempts.jsonl`. Old functional charter remains open/frozen, now subject to narrower eligibility; do not blindly resume publish.py.

## Previous verified mission: scheduled publication failures
- Status: COMPLETED_WITH_DISCLOSED_LIMITATIONS. Six publishing defects reproduced and corrected; 93 native checks plus lint/types passed. Restored 31 future schedules under row/slot guards and publishing locks.
- Instagram reuses registered confirmed login profile; TikTok cookie dismissal preserves upload/drafts; YouTube waits remain scheduled and cooldown ignores deferred-row updates, with retry eligibility after quota expiry.
- Current app/API/frontend reopened with refreshed idle publicador. External limits: 11 actual YouTube quota failures; app retry deadline 2026-10-13 01:37:36 America/Sao_Paulo. One interrupted TikTok outcome requires account review; no blind replay or direct upload test.
- Evidence/rollback: `.work/schedule-failures/evidence_index.md`, `rollback_plan.md`, `manifest.json`. No package additions, commit/push or unrelated worktree overwrite.

## Previous mission: desktop startup repair
- Status: COMPLETED_WITH_DISCLOSED_LIMITATIONS. User's Python 3.14 desktop command is running; API/frontend live and Edge child opened.
- Removed premature database UPDATE, restored existing PostgreSQL Windows connection/session/migration contracts, preserved explicit URL query options. Six source originals preserved under `.work/desktop-startup/before/`; unrelated application changes retained, no commit/push.
- Verified: 94 desktop/regression + four connector tests; source lint/types; real PostgreSQL/Redis preflight and exact-command startup. Expanded service checks have two baseline Linux-only assertions failing on Windows and two skips; no full backend suite claimed.
- Evidence/next actions: `.work/desktop-startup/evidencias/testes.md`; app is already open. Prior Agenda/provider limitations remain in the target application's notebook.

## Previous skill catalog handoff
Entry point: `00_skills/INDEX.md`; durable catalog facts: `tlc-skills.md`.

## Objective
- Completed the requested image-based TLC skill refactor and full TLC import using canonical `00_skills`.

## Last verified state
- 301 active packages, all 92 TLC packages and 777 source resources preserved; 770 Drive IDs/389 distinct images accounted in order.
- 824 SKILL.md entries verified, maximum 99 physical lines; 2,742 operative local links resolve. Skill-architect reports zero errors/warnings across active packages.
- Native discovery: 304 `.agents/skills/` entries (canonical + three aliases), plus the existing deploy-expert `.codex` entry updated.
- ADR and ADL helper CLIs preserve baseline bytes/output after relocation; installation charter status PASSED.
- Report and verification boundaries: `00_skills/validation.report.json`, `00_skills/VERIFICATION.md`. Live checklist and detailed evidence are in PROGRESS.md.

## Working set and decisions
- `00_skills/`: canonical category packages, catalog/registry, photo/upstream/migration manifests, STANDARD.md and validation report.
- `00_skills/(creation)/skill-factory/scripts/validate-workspace.py`: real installation validator.
- `skills/`: compatibility entrypoints; native `.agents/skills/`/`.codex/skills/` read canonical packages.
- Root chosen explicitly by the user; external deletions preserved. One agent identity: codenavi-agent; historical roles are internal lenses.

## Limits and risks
- The concurrent external reorganization removed `aeos/`, runtime/scripts/templates/references. Earlier notebook claims about their live routers/MCPs are historical. No deleted runtime restored.
- Instruction registration does not install/connect external services or grant permissions; verify actual prerequisites when using a skill.
- OCR/structural review covered every image; additional visual inspection used samples. No automated comparison of every photographed line was performed. Missing official font/logo assets were not fabricated.

## Next executable actions
- No pending action for the installation mission. For future changes, run the documented validator, synchronize catalog/discovery metadata and run any changed helper's relevant behavior checks.
- Revalidate external provider/runtime requirements when the corresponding skill is invoked.

## Evidence pointers
- User-request specification: `.specs/tlc-skills-standardization/SPEC.md`.
- Source/image accounting and versions: `00_skills/upstream.manifest.json`, `00_skills/images.manifest.json`.
- Ignored baseline/backups, OCR and raw CLI charter evidence: `.tools/tlc-migration/`; these are local evidence, not published skill resources.
# Publicação direta na master — 2026-10-14
Entry point: .notebook/PROGRESS.md:Commit e push direto para master
- Usuário autorizou commit e push direto usando github-operations. Revisão excluiu11979 artefatos temporários do índice preservando os arquivos no disco e acrescentou regras de ignore.
- Seleção:5688 arquivos do projeto; catálogo302/827/2871 links PASS; sintaxe75Python/140JavaScript PASS;21 candidatos de segredos são exemplos de documentação, nenhum token/chave privada detectado pelas regras executadas.
- Publicado: ac7bd4f3ce4c3f642369ce5e610f2aa8e4ab5bf6 na origin/master por push normal; SHA remoto/HEAD/origin/master iguais após releitura, checkout limpo. Correções mínimas: link obsoleto de chromatic-mega-brain e três comentários inválidos em client.mjs. Workflows herdados apontam para package.json/scripts/runtime ausentes; statuses=[] no conector não comprova CI verde. Sem pendência do commit/push solicitado; uma eventual atualização do CI requer trabalho próprio.
- Missões operacionais abaixo permanecem independentes.

