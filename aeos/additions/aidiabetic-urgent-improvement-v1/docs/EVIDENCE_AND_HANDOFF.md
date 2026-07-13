# Evidência e handoff

Evidence ID recomendado: `EV-<wave>-<skill>-<sequence>`.

Logs devem ser redigidos antes do hash e armazenados em diretório imutável.

O receiver valida schema, checkpoint, verification command e commit antes de
aceitar o handoff.

```text
.aeos-runtime/improvements/<run-id>/
  baseline/
  waves/
  evidence/
  tests/
  benchmarks/
  adrs/
  checkpoints/
  judge/
  rollback/
```
