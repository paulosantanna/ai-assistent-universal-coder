# checks

Cada linha é um teste em `scripts/tests/test_request.py`.

- Famílias pagas perguntam e o limite é 3.
- A lista gratuita não torna Grok nem GLM gratuitos.
- Ollama declarado gratuito continua proibido.
- `plan` de Grok não chama executor.
- Contagem paga diferente de 3 é recusada.
- Autorização paga é consumida; a geração seguinte pergunta.
- Modelo gratuito declarado não pergunta e não tem teto.
- Cursor não emite argv do OpenCode, nem resume.
- OpenCode com GLM não emite o binário do Cursor.
- Host vazio de modelo pergunta. Host ollama é recusado. Binário ausente sai 127.
- Worker morto não retoma e a recriação muda o id.
- `2 + 2 = 4`. Subtração, multiplicação e `2 / 0` falham como soma.
- `return 4` passa só no caso positivo e falha nos negativos.
- Prova que aceita `2 - 2` não conta.
- Pergunta permanece; narração sai.
- Geração completa marca 10. Prova negativa ausente fica abaixo de 9.5 mesmo com nota alegada 10.
- Uma citação de pilar faltando permanece em 9.5.
- Stdout do writer não substitui o JSON do revisor.
- Cada termo do glossário é uma classe.
- O CLI de `plan` imprime um JSON e sai 4 para Grok.
