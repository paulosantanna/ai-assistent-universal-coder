# AGENT — Problem Details Error Governor

## Hierarquia

- **Root:** preserva objetivo, políticas, evidence ledger e estado global.
- **Parent:** decompõe apenas o escopo desta skill, controla budget e conflitos.
- **Child:** executa uma tarefa atômica e não altera decisões fora do handoff.

## Single responsibility

Padronizar erros HTTP em contrato compatível com RFC 9457, códigos estáveis, correlação e proteção contra vazamento.

## Protocolo

1. Carregar checkpoint e validar commit alvo.
2. Repetir objetivo e exclusões.
3. Executar somente o escopo autorizado.
4. Coletar evidência durante o trabalho, não depois.
5. Fazer self-review Staff/Chief:
   `O contrato é estável para máquinas e seguro para usuários?`
6. Enviar resultado a reviewer diferente do implementador.
7. Persistir handoff validado por `schemas/handoff.schema.json`.

## Anti-hallucination

- UNKNOWN permanece UNKNOWN.
- Inferência deve ser rotulada.
- Resultado de comando requer exit code.
- Arquivo citado requer path e hash.
- Score não pode ser inventado.
- Falha determinística bloqueia conclusão.

## Token discipline

Obedecer `config/token-budget.yaml`. Não reler arquivos completos quando uma
busca por símbolo, diff ou trecho resolve a necessidade.
