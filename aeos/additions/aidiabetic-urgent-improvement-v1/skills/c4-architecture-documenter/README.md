# C4 Architecture Documenter

Skill AEOS Level 3 do pack `aidiabetic-urgent-improvement-v1`.

## Executa

Gerar documentação C4 baseada no código e decisões reais, mantendo rastreabilidade entre diagramas, componentes e ADRs.

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
