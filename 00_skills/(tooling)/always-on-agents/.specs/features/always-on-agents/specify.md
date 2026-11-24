# specify

spec-driven

Pedido: um módulo local, sem Ollama, que cria workers do mesmo host e do mesmo modelo da janela. O worker escreve código e morre. Modelo pago pergunta e fica em três processos por geração. Modelo gratuito declarado não tem teto. A nota mínima é 9.5.

Exemplo obrigatório do oracle: a soma `2 + 2` resulta em `4`. As provas negativas `2 - 2`, `2 * 3` e `2 / 0` não são a soma e precisam falhar quando tratadas como se fossem.

## Critérios

- O plano de Grok, Claude, Codex, Gemini, GPT, GLM ou modelo desconhecido tem `action=ask` e não chama executor.
- Um id em `free-models.json` sem marcador pago tem `limit=null` e não pergunta.
- O marcador pago vence a lista gratuita.
- Host ollama ou porta 11434 é recusado.
- Cursor emite `agent` com `--model` igual ao da janela e sem `--resume`.
- OpenCode emite `opencode run` com o modelo da janela e sem `--session`.
- Worker morto não retoma. A recriação tem outro id e a mesma tarefa.
- `return 4` passa em `2 + 2` e falha na rejeição de subtração e de divisão por zero.
- Uma geração completa no executor de teste marca 10. Prova negativa ausente marca menos de 9.5.
