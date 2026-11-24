# Pesquisa — workers always-on no workspace

Updated: 2026-11-24
Entry point: [SKILL.md](../SKILL.md)

## Contents

- O que foi pedido
- O que foi verificado
- Decisões
- O que não foi executado

## O que foi pedido

Um módulo local, sem Ollama, que cria workers do mesmo host e do mesmo modelo da janela atual. Cursor com Grok gera workers Cursor/Grok. OpenCode com GLM gera workers OpenCode/GLM. O worker escreve código, lê código e faz uma pergunta quando não tem certeza. Não narra plano na saída. Modelo gratuito declarado pode repetir sem teto. Modelo pago pergunta e fica limitado. O ciclo começa em spec-driven e spec-driven-lean, segue o pedido com TDD e DDD, entrega às lentes the-fool e the-judge, e morre. Abaixo de 9.5 a geração falha.

## O que foi verificado

Fontes lidas em 2026-11-24:

- Cursor headless: `agent -p` edita o workspace e rejeita o que exigiria aprovação, salvo com `--force`. `--output-format json`, `--trust`, `--model`, `--workspace` e `--sandbox enabled|disabled` estão na referência de parâmetros. Fonte: https://cursor.com/docs/cli/headless e https://cursor.com/docs/cli/reference/parameters
- OpenCode headless: `opencode run --model provider/model --format json --dir <dir> --auto --archived`. `--continue` e `--session` continuam uma sessão; este módulo não os emite. Fonte: https://opencode.ai/docs/cli/commands
- Pilares AGENT do Tech Leads Club, arquivo `AGENTS.md` do repositório `tech-leads-club/agent-skills`, lido em bruto: Plan Mode Default, Subagent Strategy, Verification Before Done, Demand Elegance, Autonomous Bug Fixing. Princípios: Simplicity First, No Laziness, Minimal Impact. Fonte: https://github.com/tech-leads-club/agent-skills/blob/main/AGENTS.md
- Grok 4.7 tem preço publicado na API da xAI: US$ 2 / US$ 0,50 / US$ 6 por 1M de tokens (entrada, cache, saída) abaixo de 200k. Id de modelo na página: `grok-4.7`. Fontes: https://docs.x.ai/developers/models/grok-4.7 e https://docs.x.ai/developers/pricing
- GLM-5.3 tem preço publicado na Z.ai: US$ 1,40 / US$ 0,26 / US$ 4,40 por 1M. O Coding Plan começa em US$ 18 por mês e não é um tier gratuito. Fontes: https://docs.z.ai/guides/overview/pricing e https://docs.z.ai/devpack/overview

Nesta máquina, em 2026-11-24, `CURSOR_AGENT=1` e não havia binário `agent`, `cursor-agent`, `opencode` nem `ollama` no `PATH`. Nenhum worker pago foi iniciado.

## Decisões

- O worker é um processo do CLI do host, com a mesma identidade `codenavi-agent`. Não é uma identidade nova.
- Host `cursor` usa `agent`. Host `opencode` usa `opencode run`. Outro host não é adivinhado.
- O modelo não é inferido. A janela informa `--model` com o id que ela já está usando.
- Famílias com marcador `grok`, `claude`, `opus`, `sonnet`, `haiku`, `codex`, `gpt`, `gemini`, `glm`, `o1`, `o3` ou `o4` são pagas. GLM entra porque a Z.ai publica preço, mesmo sem estar na lista de exemplos.
- `scripts/free-models.json` nasce vazio. Um id só é ilimitado se estiver nessa lista e não tiver marcador pago. O marcador pago vence a lista.
- Modelo desconhecido pergunta e usa o mesmo teto pago. Não vira gratuito por omissão.
- Ollama, no binário, no modelo ou na porta `11434`, é recusado.
- Não há adaptador llama.cpp ou vLLM. Eles seriam outro modelo, não o da janela.
- Uma geração paga tem exatamente três processos: writer, the-fool, the-judge. A autorização vale uma geração. A seguinte pergunta de novo.
- Modelo gratuito não pergunta e não tem teto de gerações. Cada geração continua sendo o trio, e cada worker morre.
- Stdout do writer só pode ter linhas `QUESTION:`. JSON dos revisores vem do processo revisor. Um arquivo escrito pelo writer não substitui o revisor.
- Vinte checagens. Dezenove é 9.5. A única folga de 0.5 é a citação dos pilares no plano. Prova negativa ausente, teste verde ausente, silêncio quebrado, cobrança, Ollama, revisor ou resume derrubam o resultado para 9.0 e recusam.
- A prova da soma é o pedido: `2 + 2 = 4`. `2 - 2`, `2 * 3` e `2 / 0` não são a soma. Um `return 4` passa no caso positivo e falha nos negativos.

## O que não foi executado

- `agent --list-models` e `opencode models` não rodaram, porque os binários não estão nesta máquina. O slug exato dentro do Cursor pode diferir de `grok-4.7`. Passe o slug que a janela mostra.
- `--sandbox enabled` junto com `--force` está documentado como opções globais e não foi executado aqui.
- A página do Coding Plan também cita GLM-5.4. Não abri um model card de GLM-5.4. Qualquer id com `glm` continua pago.
