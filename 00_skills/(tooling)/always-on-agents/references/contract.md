# Contrato dos workers

Updated: 2026-11-24
Entry point: [SKILL.md](../SKILL.md)

## Linguagem

HostSession é a janela. BillingDecision diz se o modelo pergunta. WorkerLife nasce e morre. RequestOracle guarda o pedido. ReviewGate calcula a nota. Sum é o exemplo pedido: só adição.

Os oito pilares citados no plano são os do `AGENTS.md` do Tech Leads Club, listados em [research](research.md).

## Saída

O writer grava arquivos. Na stdout, a única linha permitida começa com `QUESTION:`. Plano, progresso e "vou fazer" reprovam o silêncio. O pai da conversa mostra só o campo `question` ou a nota e os caminhos alterados.

## Ciclo

1. `specify.md` com spec-driven, o pedido, `2 + 2` e o resultado `4`, mais `2 - 2`, `2 * 3` e `2 / 0`.
2. `plan.md` com spec-driven-lean e os oito pilares.
3. `glossary.md` com HostSession, BillingDecision, WorkerLife, RequestOracle, ReviewGate e Sum.
4. Testes do pedido. A suíte verde cobre a soma e a rejeição das outras operações. A prova negativa precisa terminar com código diferente de zero.
5. Processos separados da lente the-fool e da lente the-judge. Fool aceita `SEGUIR` ou `SEGUIR COM AJUSTE` com ameaças. Judge aceita só `APPROVE` sem findings.
6. Os três processos morrem. `resume` é erro. Nova tentativa usa ids novos.

## Cobrança

Grok, Claude, Codex, Gemini, GPT e GLM perguntam. A resposta útil é `sim`, `yes` ou `aprovo`. Qualquer outro texto continua na pergunta. A geração paga tem três processos e a autorização não se reaproveita. Gratuito declarado não pergunta e não tem teto. Ollama para antes de criar processo.

## Nota

ReviewGate lê a pasta da geração. Não lê uma nota que o worker tenha escrito. Dezenove checagens é 9.5. As checagens duras, se falharem, limitam a nota a 9.0: Ollama, cobrança, prova negativa, testes, silêncio, fool, judge, morte, resume e revisor vindo de processo. A citação incompleta dos pilares é a única falta que ainda pode ficar em 9.5.

## Comandos do host

Cursor, sem `--resume` e sem `--continue`:

`agent -p --output-format json --trust --force --sandbox enabled --workspace <dir> --model <modelo> <prompt>`

OpenCode, sem `--continue` e sem `--session`:

`opencode run --model <modelo> --format json --dir <dir> --auto --archived <prompt>`

Os argumentos são uma lista. Não há shell. `--force` existe porque o modo headless do Cursor recusa comando de teste sem ele. O risco fica no registro da pesquisa: o sandbox foi pedido e não foi executado nesta máquina.
