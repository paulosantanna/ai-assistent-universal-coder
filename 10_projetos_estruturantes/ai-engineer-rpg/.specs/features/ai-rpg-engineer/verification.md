# Verificação — ai-rpg-engineer

Data: 2026-11-10 · Verificação self-verified (autor == verificador, sessão única; gate degradado)

## Gate formal

O gate completo `check_proofs.py` + `validate_verification.py` exige `proofs.md` gerado sobre um commit HEAD limpo. A política desta sessão é **não commitar** (owner), então o gate formal não pode ser fechado sem autorização de commit. As provas abaixo foram executadas manualmente na working-copy e registradas aqui; o item fica residual até a autorização de commit.

## Resultado

| Portão | Comando | Resultado |
| --- | --- | --- |
| Plano | `validate_plan.py ai-rpg-engineer --root 10_projetos_estruturantes/ai-engineer-rpg` | 0 erros, 0 avisos |
| Checks | `validate_checks.py ai-rpg-engineer --root 10_projetos_estruturantes/ai-engineer-rpg` | 0 erros, 1 aviso (proof do `Build:` é comando, não suíte — esperado) |
| Suíte | `npx vitest run` | 7 arquivos, 55/55 verdes |
| TypeScript | `npx tsc --noEmit` | limpo |
| Build | `npm run build` | ok (tsc + vite, 252 módulos; chunk iife único 867.65 kB com CSS embutido) |
| Distribuição | `npm run build` + inspeção de `dist/index.html` e do chunk | script clássico `defer` sem `type="module"`, caminhos relativos, zero `fetch`/`import()` no runtime — abrível por duplo clique (file://). Bug corrigido no smoke do owner: sem `defer`, o script clássico no `<head>` executa antes de `#root` e a página fica branca |

## Mutações (3/3 mortas)

| Mutation | Injected | Detecção | Revertido |
| --- | --- | --- | --- |
| M1 — custo da dica 100→90 (`src/engine/economy.ts`) | `HINT_COST = 90` | 4 falhas direcionadas (economy 3 + store 1: `HINT_COST` e gates de saldo) | sim |
| M2 — limiar do D20 15→16 (`src/engine/economy.ts`) | `D20_THRESHOLD = 16` | 1 falha direcionada (`rollo 15 -> acerto` em tests/d20.test.ts) | sim |
| M3 — peso do capstone 0.16→0.17 (`src/content/capstone.ts`) | `weight: 0.17` em `cap-arq` | 3 falhas direcionadas (Σ pesos do capstone, validação zero-erros, banca) | sim |

Depois das reversões: suíte de volta a 55/55.

## Expansão de conteúdo v1.1.0 (2026-11-10, pedido do owner "algo bem completo")

- Escopo entregue: 8 lições por reino (`rN-l1..l8`; l1–l5 ensino, l6/l7 novas por domínio, l8 síntese), 8 missões por reino (`rN-m1..m8`; chefão movido de `rN-m6` para `rN-m8`, kind `boss`, títulos preservados), 33 questões por reino (231 no total), 51 fontes JEV (21 novas; r3 e r5 com 8) e 26 termos novos no glossário (78 no total). `pack.ts` version → `1.1.0`.
- Execução: `realm0.ts` reescrito do zero como exemplar; demais 6 reinos entregues por 6 subagentes paralelos com contrato rígido (ids, quantidades, pesos JEV/BLURB/tiers intocados). r2 e r5 "falharam" apenas no relatório final (limite do modelo free) depois de completar os writes — qualidade conferida por leitura direta, no nível do exemplar.
- Verificação da rodada: `npx tsc --noEmit` limpo (2×, a segunda via build); `npx vitest run` 55/55 (2×, a última após as edições finais); `npm run build` ok (252 módulos; chunk 867.65 kB); `dist/index.html` standalone conferido (`<script defer src="./assets/index-B3p3VcGr.js">`); varreduras de corrupção zero (CJK `[一-鿿]`, tailandês `[ก-๛]`, cirílico, mojibake `Ã`, literal `\u00`, EN vazado amplo); `correct` variado (~uniforme 0–3 por reino).
- Correções finais: hint r3 EN `'Forget…'` → `'Esquecimento, entrada e saída: as três portas.'`; nome r4 `Braco de Mar` → `Braço de Mar`; glossário reescrito inteiro (52 termos corrigidos + 26 novos).

## PDFs e conteúdo

- `certificate.ts`: página única via `doc.addPage()` (bug `getPage(0)` corrigido antes da suíte).
- Metadados `Info` (Title/Subject/Keywords/Producer) gravados `pdf-lib` como UTF-16 hex; teste estrutural via `PDFDocument.load` (pageCount=1, `getKeywords()` contém o código, `getSubject()` contém o hash) — por isso a varredura ASCII crua não encontra o código (comportamento da biblioteca, documentado no teste).
- Correção de corrupção de gerador varrida com grep (`[一-鿿✓✔]`, tokens vazados) e reescrita completa de `realm2`, `realm4`, `realm5`, `realm6` + ajustes em `realm1`.

## Findings (residuais)

1. **Gate formal pendente de commit** — fechamento `check_proofs/validate_verification` exige HEAD limpo; bloqueado pela política de não commit. Próximo passo: com autorização de commit, rodar `check_proofs.py` e fechar o gate.
2. **Bundle em chunk único (agora 1008.21 kB)** — requisito da distribuição file://: IIFE não admite múltiplos chunks, então code-splitting conflita com a abertura local; só volta a valer se o jogo for hospedado via http.
3. **Self-verified** — nenhum revisor independente; lens única nesta sessão (degradado por design do fluxo).
4. **UI não coberta por vitest** — engine e store cobertos por 55 testes; UI compilada pelo build e revisável pelo próprio `dist/index.html` aberto no navegador (sem npm, conforme correção do owner).

## Profundidade de ensino + dicionário v1.2.0 (2026-11-11, pedidos do owner)

- Escopo entregue: (1) aprofundamento de ensino — cada lição l1–l7 dos 7 reinos recebeu 3 parágrafos appended ("As fórmulas na mesa" com notação plana unicode; "Exemplo resolvido com números" com contas conferidas dígito a dígito espelhando as questões da própria missão; "Pegadinhas que a mesa adora" explicando os distratores) e a l8 síntese recebeu 2 ("Plano de revisão guiado pelo chefão" + "Ritual da mesa"); (2) tooltips ricos — `.tip-card` em CSS puro no hover/foco dos termos destacados das lições (`MissionView.tsx`), com definição + fórmula + exemplo, `title` nativo removido; (3) aba Dicionário — aba "Glossário" renomeada para "Dicionário" (tab id interno `glossario` intacto) e `GlossaryView` reescrita com cards def + fórmula + exemplo.
- Infra: `GlossaryTerm` ganhou `formula?`/`example?` (validador e schema de save intocados); glossário com dois termos novos (`g-l1` L1/Lasso, `g-l2` L2/Ridge) e reestruturado como `baseGlossary` + merge `dictionaryFill[g.id]`; fragmentos por reino em `src/content/dictionary/realm0..6.ts` (export `realmNFill`) e mesclador `dictionary/index.ts`; `pack.ts` version → `1.2.0`.
- Cobertura: script node de conferência — **82 ids no glossário ↔ 82 fills, 0 missing, 0 duplicado, 0 extra** (repartição por reino 12/10/14/11/18/12/5, sem sobreposição). Correção de contagem histórica: a leva v1.1.0 acima registrou "26 novos (78 no total)", mas o glossário real ficou com 28 novos (80); com g-l1/g-l2, o total v1.2.0 é **82** (52 corrigidos + 30 novos).
- Execução: realm0 exemplar na sessão principal; r1–r6 por subagentes com contrato rígido (append-only, terms só com id grep-ado no glossário, PT-BR impecável, contas conferidas, fragmento próprio). "Free usage limit reached" derrubou r1–r4 na 1ª leva em paralelo (r1 só l1 feita; r2–r4 intocados) — retomadas r1, depois r2/r3/r4 bem-sucedidas; estado real sempre conferido por grep/leitura após cada leva (49 blocos "As fórmulas na mesa" = 7×7; 7 "Plano de revisão" = 1×7).
- Integridade: questões, missões, fontes, pesos JEV, BLURB, tiers e schema de save `aierpg/progress/v1` intocados; lições foram append-only (nenhum parágrafo antigo removido ou alterado); parágrafos antigos verificados presentes.
- Verificação da rodada: `npx tsc --noEmit` limpo; `npx vitest run` 55/55 (7 arquivos); portões spec-lean `validate_plan` 0 erros/0 avisos e `validate_checks` 0 erros/1 aviso esperado; `npm run build` ok (260 módulos; chunk `index-BEUga6XB.js`, 1008.21 kB); `dist/index.html` standalone conferido com o chunk novo; cópia à prova de cachê `dist-standalone-v110/` renovada (byte-cópia do dist v1.2.0); varreduras de corrupção zero em todo `src` (CJK `[一-鿿]`, tailandês `[ก-๛]`, cirílico, literal `\u00`, EN vazado; único `Ã` = "NÃO" legítimo em `economy.ts`, pré-existente e fora do escopo).
- Termos acrescentados a `terms` de lições (todos com id grep-ado no glossário): r0-l1 +g-l1/g-l2, r0-l2 +g-backpropagation; r1-l4 +g-cross-validation, r1-l5 +g-observability, r1-l7 +g-reproducibility; r2-l2 +g-l1/g-l2; r3-l7 +g-kv-cache; r4-l1 +g-context-window; r5-l6 +g-observability, r5-l7 +g-golden-set; r6-l1 +g-guardrails, r6-l3 +g-carbon-budget.
