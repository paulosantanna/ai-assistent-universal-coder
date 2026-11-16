# ai-rpg-engineer checks

Mutations: 3 - briefing do dono (custo da dica, limiar do D20, um peso do capstone)
Build: npm run build; npx tsc --noEmit (lint none - o projeto não tem ESLint configurado)
Plan: `.specs/features/ai-rpg-engineer/plan.md`

## Intent

17 ACs em 8 slices · 2 one-way doors · 0 open, of which 0 block

Trilha de mesa RPG (React+Vite+TS, client-only) que ensina Engenharia de IA do zero ao certificado verificável: economia de pontos (+20/dica 100/D20>=15/-10 clamp), capstone juizado 8 competências (>= 0.85, mínima 0.50), certificado PDF com código `AIE-AAAA-HASH8` + SHA-256 do dossiê. Total 55 testes verdes em 7 arquivos. Expansão de conteúdo v1.1.0: 8 lições e 8 missões por reino (chefão em m8), 231 questões, 51 fontes JEV e 78 termos de glossário.

## Checks

### S1 - conteúdo e validador

**C1** - o pack real passa pelo validador com zero erros e mínimos de 7 reinos, 36+ lições, 30+ missões, 120+ questões, 20+ fontes e 50 termos (AC 1)
Proof: `npx vitest run tests/pack.test.ts -t "atende os mínimos"`
Proof: `npx vitest run tests/pack.test.ts -t "erros de validação"`

**C2** - cada questão tem dica de 8+ caracteres, 3+ opções e índice correto válido (AC 2)
Proof: `npx vitest run tests/pack.test.ts -t "dica >= 8"`

**C3** - fontes reais obedecem ao selo JEV: auto com confiança 0.7+, revisar na faixa 0.5-0.7 e checkedAt presente (AC 4)
Proof: `npx vitest run tests/pack.test.ts -t "selo JEV"`

**C4** - pesos JEV dos reinos somam 1.0; capstone tem 8 competências com pesos somando 1.0, rubricas 0..4 e dissertação mínima de 400 (AC 3)
Proof: `npx vitest run tests/pack.test.ts -t "pesos JEV dos reinos"`
Proof: `npx vitest run tests/pack.test.ts -t "capstone: 8 competências"`

### S2 - economia

**C5** - acerto paga +20 e XP soma só positivos; erro não altera o ledger (AC 5, 6)
Proof: `npx vitest run tests/economy.test.ts -t "entrada de resposta certa"`
Proof: `npx vitest run tests/store.test.ts -t "resposta certa paga"`

**C6** - dica custa exatamente 100, só com saldo suficiente, e repetir a compra não debita de novo (AC 6, idempotência)
Proof: `npx vitest run tests/economy.test.ts -t "comprar a dica debita"`
Proof: `npx vitest run tests/store.test.ts -t "dica custa 100"`
Proof: `npx vitest run tests/economy.test.ts -t "saldo 100 permite dica"`

### S3 - D20

**C7** - D20 com 15 ou mais marca correta (+20); menor que 15 desconta com clamp em zero; uma única tentativa por questão; saldo 100+ recusa a rolagem (AC 7, 8)
Proof: `npx vitest run tests/d20.test.ts -t "D20: limiar"`
Proof: `npx vitest run tests/store.test.ts -t "clamp do desconto"`
Proof: `npx vitest run tests/store.test.ts -t "consome a tentativa"`
Proof: `npx vitest run tests/store.test.ts -t "com saldo >= 100 a rolagem"`

### S4 - progresso

**C8** - missão abre só com a anterior completa; reino n abre com o reino n-1 integral; capstone exige os 7 reinos (AC 9)
Proof: `npx vitest run tests/progress.test.ts -t "cadeia de destravamento"`

### S5 - banca do capstone

**C9** - aprovação em nota considerada 0.85+ com nenhuma competência abaixo de 0.50; dissertação curta, tarefa pendente (score ausente = 0) e clamp de 9 p/ 4 registrados (AC 10, 11)
Proof: `npx vitest run tests/capstone.test.ts -t "limite: exatamente 0.85"`
Proof: `npx vitest run tests/capstone.test.ts -t "abaixo de 0.50"`
Proof: `npx vitest run tests/capstone.test.ts -t "dissertação curta"`
Proof: `npx vitest run tests/capstone.test.ts -t "tarefa ausente"`
Proof: `npx vitest run tests/capstone.test.ts -t "clamp: score 9"`

### S6 - certificado

**C10** - código no formato AIE-AAAA-HASH8; SHA-256 de referência FIPS; canonicalJson dá hash identico com ordem de chave diferente; PDF tem 1 página, header %PDF e metadata com código+hash (AC 12, 13, 14)
Proof: `npx vitest run tests/certificate.test.ts -t "código no formato"`
Proof: `npx vitest run tests/certificate.test.ts -t "FIPS"`
Proof: `npx vitest run tests/certificate.test.ts -t "canonicalJson"`
Proof: `npx vitest run tests/certificate.test.ts -t "PDF válido"`

### S7 - store e persistência

**C11** - submissão do capstone fica registrada; emissão exige capstone aprovado + 7 reinos; progresso persistido normaliza (version 1) e rejeita versão estranha (AC 15, 16)
Proof: `npx vitest run tests/store.test.ts -t "emite certificado"`
Proof: `npx vitest run tests/store.test.ts -t "submissão registrada"`
Proof: `npx vitest run tests/certificate.test.ts -t "normalizeProgress"`

**C12** - export/import roundtrip preserva o estado e JSON inválido retorna false sem tocar o estado (AC 16)
Proof: `npx vitest run tests/store.test.ts -t "roundtrip"`

### S8 - build

**C13** - `npm run build` termina sem erro e o `dist/index.html` gerado é file-friendly: script clássico *deferred* (`defer`, sem `type="module"`/`crossorigin`), caminhos relativos e CSS embutido no chunk iife, sem rede no runtime (AC 17)
Proof: `npm run build`

## Coverage

| Set (size) | Member -> proof | Unproven |
| --- | --- | --- |
| mínimos do pack (6) | reinos 7 C1 · lições 36+ C1 · missões 30+ C1 · questões 120+ C1 · fontes 20+ C1 · glossário 50 C1 | - |
| contrato por questão (3) | dica 8+ C2 · 3+ opções C2 · índice válido C2 | - |
| fontes reais selo JEV (3) | auto 0.7+ C3 · revisar 0.5-0.7 C3 · checkedAt C3 | - |
| pesos e shape do capstone (3) | reinos soma 1.0 C4 · 8 rubricas soma 1.0 C4 · rubricas 0..4 + minChars 400 C4 | - |
| economia (4) | acerto +20 C5 · erro imune C5 · dica debita 100 C6 · gate saldo 100 C6 | - |
| D20 (4) | 15+ acerta C7 · clamp em zero C7 · única tentativa C7 · saldo 100+ recusa C7 | - |
| portões de acesso (3) | missão linear C8 · reino chain C8 · capstone 7 reinos C8 | - |
| banca do capstone (5) | limite 0.85 C9 · mín 0.50 C9 · dissertação C9 · pendência C9 · clamp 9->4 C9 | - |
| certificado (4) | formato código C10 · FIPS C10 · ordem canônica C10 · PDF página/metadata C10 | - |
| store e persistência (4) | submissão C11 · emissão C11 · normalize C11 · roundtrip C12 | - |
| build (1) | tsc + vite C13 | - |

## Swept

- validation: C1, C2, C4
- failure modes: C12
- idempotency: C6
- authorization: n/a - jogo client-side sem API, papéis ou rate limit no escopo
- concurrency: C7 - uma única tentativa de D20 por questão, store serial
- data lifecycle: C11, C12
- dependency failure: existing - loadProgress degrada do idb-keyval para o espelho localStorage e retorna null ao falhar (try/catch na leitura e na gravação)
- state transitions: C7, C8
- observability: n/a - sem requisitos de telemetria nesta fatia (jogo de mesa client-side)

## Handoff

- **Boundary:** C1-C13 fechados na working-copy do projeto (sem commit, política do owner); suíte 55/55 verdes e `tsc --noEmit` limpo (2× cada, a última pós-expansão v1.1.0); build 252 módulos/chunk 867.65 kB; `dist/index.html` standalone conferido; varredura de corrupção zero
