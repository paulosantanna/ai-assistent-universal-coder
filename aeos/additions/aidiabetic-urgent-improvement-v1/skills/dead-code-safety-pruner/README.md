# Dead Code Safety Pruner

Skill AEOS Level 3 do pack `aidiabetic-urgent-improvement-v1`.

## Executa

Remover código morto em lotes pequenos somente após análise estática, entrypoints dinâmicos, cobertura, imports e rollback.

## Entrada mínima

- target repository;
- commit SHA;
- baseline ou handoff válido;
- policies do pack.

## Saída mínima

- artefato principal;
- evidence ledger;
- tests/verification;
- Staff/Chief review;
- handoff ao próximo owner.

## Validação

```powershell
py -3 .\scripts\validate_contract.py
py -3 -m pytest .\tests -ra
```
