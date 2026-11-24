# Uso na próxima conversa

Updated: 2026-11-24
Entry point: [SKILL.md](../SKILL.md)

A pasta dos comandos é `00_skills/(tooling)/always-on-agents/scripts`. No Windows use `py -3` no lugar de `python`.

## Antes de criar

```text
python -m always_on plan --host cursor --model grok-4.7 --task "Faça uma calculadora somar 2 + 2"
python -m always_on plan --host opencode --model zai-coding-plan/glm-5.3 --task "Faça uma calculadora somar 2 + 2"
```

Saída 4 é pergunta. Mostre só `question`. Pare. Não invente `sim`.

## Se a pessoa autorizar

```text
python -m always_on approve --host cursor --model grok-4.7 --task "Faça uma calculadora somar 2 + 2" --answer sim
python -m always_on spawn --host cursor --model grok-4.7 --task "Faça uma calculadora somar 2 + 2" --workspace . --approval <id>
```

`--execute` chama o binário. Sem `--execute` o comando só mostra o argv. Se o binário não existe, a saída é 3 e nada é dado como feito.

Modelo presente em `free-models.json`, e sem marcador pago, não passa por `approve`. Grok e GLM continuam pagos mesmo se alguém os colocar nessa lista.

## Prova local, sem chamar modelo

```text
python scripts/run_tests.py
```

27 checagens do pedido. A geração gratuita de exemplo fecha em 10. Prova negativa ausente ou revisor forjado fica em 9.0.
