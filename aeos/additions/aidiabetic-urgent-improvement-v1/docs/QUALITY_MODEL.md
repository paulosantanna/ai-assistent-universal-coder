# Modelo de qualidade

Cada gate recebe score de 0 a 10 com critérios e evidências. O score final é a
média ponderada de `config/quality-gates.yaml`.

Floors:

- critical gate falho: sem PASS;
- hash mismatch: BLOCKED;
- PHI/secrets em artefato: BLOCKED;
- regressão crítica: BLOCKED;
- rollback ausente em mudança destrutiva: REWORK_REQUIRED;
- score abaixo de 9.8: REWORK_REQUIRED.

Um LLM não pode reclassificar um teste falho como aprovado.
