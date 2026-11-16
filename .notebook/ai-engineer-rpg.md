# ai-engineer-rpg

Updated: 2026-11-11. Entry point: `10_projetos_estruturantes/ai-engineer-rpg/package.json`.

RPG web de mesa (React+Vite+TS, client-only) que ensina Engenharia de IA: 7 reinos / 56 lições / 56 missões / 231 questões (pack v1.2.0), economia +20 acerto · dica 100 · D20 ≥ 15 marca · falha −10 com clamp, capstone de 8 competências ponderadas (final ≥ 0.85, nenhuma < 0.50) e certificado PDF `AIE-AAAA-HASH8` + SHA-256 do dossiê canônico.

- Entry point: `src/App.tsx` → telas em `src/ui/*`; regras puras em `src/engine/*`; conteúdo em `src/content/*` (`pack.ts` agrega reinos r0..r6 + `capstone.ts`).
- Ensino (v1.2.0): cada lição l1–l7 tem 3 parágrafos appended ("As fórmulas na mesa", "Exemplo resolvido com números", "Pegadinhas que a mesa adora") e l8 síntese 2 ("Plano de revisão guiado pelo chefão", "Ritual da mesa") — append-only, parágrafos antigos intactos.
- Dicionário (v1.2.0): 82 termos (52 base + 28 expansão + g-l1/g-l2) com `formula`+`example` em `src/content/dictionary/realm0..6.ts`, mesclados por `dictionary/index.ts` (`dictionaryFill`) no `glossary.ts` (`baseGlossary.map`); cobre 82/82 (script node: 0 missing/dup/extra). Aba "Dicionário" (`GlossaryView`) mostra def+fórmula+exemplo; tooltip `.tip-card` no hover/foco dos termos das lições (`MissionView`, `title` nativo removido).
- Store: `src/engine/gameStore.ts` (`useSyncExternalStore`, sem zustand); persistência `aierpg/progress/v1` (idb-keyval + espelho localStorage, try/catch degradando).
- Espec: artifacts spec-driven-lean em `10_projetos_estruturantes/ai-engineer-rpg/.specs/features/ai-rpg-engineer/` (plan 17 ACs/8 slices, checks C1–C13, verification).
- Pendência: commit autorizado → `check_proofs.py` + `validate_verification.py` (gate formal). Como jogar: abrir `dist/index.html` por duplo clique (standalone, iife, sem npm) ou a cópia à prova de cachê `dist-standalone-v110/index.html`. Chunk único 1008.21 kB (v1.2.0) — code-splitting só com hosting http.

Tags: rpg, react, game, education
