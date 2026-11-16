# skills-quality-eval Rubric (pré-registrado)

Updated: 2026-11-16  
Entry point: `.work/skills-quality-eval/` (evidência fora do git)  
Modelo JEV: `jev-latest` (alias produção; medido como `jev-1.14.0` em 2026-11-16)

## Ordem de operações

1. **Amostra fixada** — 36 skills (estratificadas): 12 `high` governance/eval, 12 domínio técnico, 12 TLC/creation; lista em `sample.json` (SHA fixado antes do JEV).
2. **Excerpts** — primeiros 3000 caracteres de cada `SKILL.md` canônico (mesmo texto para rótulo e juiz).
3. **Rótulos prata** — por dimensão abaixo; `1` só com citação literal no excerpt; `0` se ausência clara; `null` se ambíguo (excluído das métricas).
4. **JEV** — um Noul por dimensão × skill em batches de 6 skills (6×4 = 24 Nouls/request); state = excerpt + `registry_entry` quando existir.
5. **eval-gate** — limiar de aprovação **p ≥ 0.7** (suporte) e **p ≤ 0.3** (rejeição); faixa média = revisão humana. Agregado por dimensão: precisão/recall vs rótulos (exclui `null`).

JEV é **triagem**, não aprovação de deploy ou de skill.

## Dimensões (ground truth)

| ID | Definição positiva (rótulo 1) |
|----|-------------------------------|
| `gov_codenavi` | O texto declara governança CodENavi Full Workspace v2 e skill de `codenavi-agent` (sem identidade de agente extra). |
| `workflow_modules` | O texto lista módulos de workflow/instruções numerados ou roteamento explícito para `references/instructions/`. |
| `boundaries_secrets` | O texto proíbe expor segredos/credenciais e exige falha fechada quando faltam permissões ou evidências. |
| `provenance_pointer` | O texto aponta proveniência, ponteiro de código ou evidência verificável (não só opinião). |

## Keywords congelados (auto-0 se ausentes no excerpt)

- `gov_codenavi`: `codenavi-agent`, `CodENavi Full Workspace`
- `workflow_modules`: `references/instructions`, `Workflow and module routing`
- `boundaries_secrets`: `secrets`, `runtime providers`, `fail closed`, `falha fechada`, `permission`
- `provenance_pointer`: `provenance`, `Evidence:`, `path/`, `references/provenance`

## Limites

- Rótulos prata pelo `codenavi-agent` na mesma sessão — não independentes.
- Amostra 36/324 — inferência para o catálogo inteiro é indicativa.
- Skills com >100 linhas no `SKILL.md` truncadas no excerpt podem perder sinais no final do arquivo.

## Veredito desta rodada

Regra: **PASS parcial** se precisão média das 4 dimensões ≥ 0.85 com ≥ 24 rótulos não-nulos por dimensão **ou** amostra < 40 skills (veredito `indicative` por tamanho).

## Amendment A1 (2026-11-16, declarada ANTES de rodar a v2)

Motivo: a rodada v1 (36 skills escolhidas a mão em parte) mostrou dois defeitos **do rótulo/pergunta, não dos skills** (auditoria de `labels.json`/`judgments.json`):

1. `workflow_modules` (precisão 0,33): os 24 "falsos positivos" roteiam de fato para `references/` (2–3 links, ex. `ai-evals-expert`, `handoff-manager`); o rótulo exigia o cabeçalho literal `Workflow and module routing`. É um fato estrutural, não semântico: passa a ser **medido em código** (sem JEV), em **todos** os skills do catálogo. Regra: nº de links markdown `](references/` no SKILL.md completo; `>= 2` = roteamento presente.
2. `boundaries_secrets` (recall 0,53): pergunta composta (segredos E falha fechada) e keyword `permission` casando com "permission gates". Divide-se em dois Nouls atômicos (prática TypeSafe: uma condição por Noul), com rótulo por **sentença** (keyword + verbo de obrigação/proibição na mesma sentença). Keyword sem a sentença = `null` (excluído).

Dimensões v2 julgadas pelo JEV: `gov_codenavi`, `provenance_pointer` (inalteradas), `secrets_runtime_only`, `fail_closed`.

- `secrets_runtime_only`: sentença com (secret|credential|token|cookie|password) E (never|must not|do not|forbid|runtime|masked|redact|not persist|only).
- `fail_closed`: "fail closed"/"falha fechada", OU sentença com (missing|absent|without|unavailable) E (block|stop|refus|halt|deny).
- Rótulo 0 = nenhuma keyword do conjunto no excerpt; 1 = a sentença casa; `null` = keyword presente sem a sentença.

**Anti-ajuste ao benchmark:** a v2 é medida numa amostra **nova de 60 skills, aleatória pura (sem estratos escolhidos), disjunta das 36 da v1** (seed 20261117). As 36 da v1 viram "dev set" e são reportadas à parte. Regras/regex congeladas neste texto; o relatório grava o hash.

**Veredito pré-registrado (amostra nova, por dimensão JEV):** `pass` se precisão@0,7 >= 0,85 com >= 20 aprovações; senão `review`. Veredito geral: `conclusive` (>= 40 skills); `pass` se todas as 4 dimensões passam. Rótulos continuam prata (mesmo agente), sem dono.


## Amendment A2 (2026-11-16, declarada ANTES de rodar; só `secrets_runtime_only`)

Resultado da v2 (holdout 1, 60 skills): `gov_codenavi` pass (1,00), `provenance_pointer` pass (0,88), `fail_closed` pass (1,00), `secrets_runtime_only` **review** (2 aprovações; 36 FN).
Diagnóstico (feito lendo os 36 FN, portanto o holdout 1 está **queimado** para esta dimensão): os rótulos citam regras legítimas ("Keep secrets in runtime providers." 19x; "Redact secrets, credentials, tokens and sensitive values." 12x), mas a pergunta v2 era mais estreita ("fora de arquivos, logs, prompts ou saídas") e o JEV respondeu ~0,5. Defeito de largura da pergunta, não dos skills.

Mudança: **apenas** o texto da pergunta de `secrets_runtime_only`, com a fronteira sim/não dentro da instrução (o cliente do workspace-brain envia só `instructions`):
> "This skill text contains at least one explicit rule that protects secrets or credentials: keeping them in runtime providers, redacting or masking them, or never persisting them. Answer no if secrets are not mentioned or are mentioned without any protective rule."

Inalterados: rótulo por sentença, limiar 0,7, regra de veredito (precisão >= 0,85 com >= 20 aprovações), as outras 3 dimensões (não são re-medidas: já passaram e re-medir aumentaria comparações sem ganho).
**Holdout 2:** 60 skills aleatórios, seed 20261118, disjuntos do dev set (36) e do holdout 1 (60). Se `review` de novo, o resultado é reportado como está; não há terceira emenda nesta missão.


## Amendment A3 (2026-11-16, declarada ANTES de qualquer execução A3; hash em `.work/skills-quality-eval/a3/prereg.json`)

`frozen_sha256 = e3c59f3358bf0e9cea90a2a7cc03f1b7ddf6f103b85e489a6bc85fbb00e0d5b3` (perguntas, gates, seeds, ids, regras silver).

Motivo: quatro limites declarados nas rodadas anteriores. Correção de cada um:

| Limite anterior | Correção A3 |
|---|---|
| Holdouts de 60/324 | **Todas as 324 skills** do catálogo, nas 4 dimensões JEV. |
| Excerpt de 3000 chars truncava 110/324 (34%) | **`SKILL.md` inteiro** (máx. 11.638 chars; nenhum truncado). |
| Rótulos prata do próprio autor | **2 anotadores cegos de famílias de modelo distintas** (≠ autor) + terceiro votante só nos desacordos; rótulo = maioria. |
| Poucos negativos reais (secrets: 2) | Precisão só vale como `pass` com **≥ 10 negativos** na verdade-terreno; senão `uninformative`. |

Desenho:
- Perguntas: as mesmas do JEV para os anotadores (uma condição cada); `secrets_runtime_only` = texto A2. `workflow_modules` segue em código (sem anotador, sem JEV).
- Anotador responde `1`, `0` ou `u` (incerto) + citação literal para `1`. Cego a: outro anotador, regras silver, saída do JEV, registry.
- Rótulo de consenso = maioria dos votos válidos (1/0) entre A1, A2 e (só se A1≠A2 ou há `u`) A3. Sem maioria = `null`.
- **Confiabilidade** por dimensão (A1×A2, antes de adjudicar): κ de Cohen ≥ 0,70. Se a classe minoritária < 10%, o paradoxo da prevalência vale: exigir AC1 de Gwet ≥ 0,85 **e** concordância bruta ≥ 0,92. Sempre reportar κ, AC1 e concordância bruta.
- **JEV vs consenso**: métrica principal no estrato **S1 = itens em que A1 = A2** (não circular). Regra de A1 mantida: precisão@0,7 ≥ 0,85 com ≥ 20 aprovações; reportar recall, especificidade, Wilson 95%, % na faixa de revisão (0,3–0,7). Sensibilidade: subconjunto livre de tuning (324 − dev 36 − holdout 1 = 228).
- Veredito por dimensão: `pass` | `review` | `uninformative` (< 10 negativos). Veredito geral `pass` só se as 4 forem `pass`.

**Regra de saída do regime silver** (por dimensão; nunca "ouro humano"): sai do silver se (a) confiabilidade passa, (b) `null` ≤ 5% das 324, (c) a **triagem JEV** da evidência resume p ≥ 0,70 nos 3 Nouls atômicos (independência do autor; confiabilidade suficiente; limitação residual de não haver revisão humana não invalida o uso como verdade-terreno para precisão), e (d) o veredito JEV da dimensão não é `uninformative`-por-erro de coleta. Decisão = gate em código ∧ triagem JEV (faixa média = permanece silver). O status resultante é `consenso-IA independente`, **não** `ouro humano`.

Sem emenda pós-hoc: qualquer desvio é registrado como desvio no relatório.
