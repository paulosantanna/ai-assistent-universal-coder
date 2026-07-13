# Evidence Readiness Judge

```yaml
skill:
  slug: evidence-readiness-judge
  version: 1.0.0
  category: VALIDATION
  architecture_level: 3
  risk_level: CRITICAL
  memory_enabled: true
  human_approval: true
```

## 1. Identity

- **Name:** Evidence Readiness Judge
- **Owner agent:** `evidence-readiness-judge-agent`
- **Architecture level:** 3
- **Risk:** CRITICAL

## 2. Mission

Validar determinística e semanticamente gates, evidências, hashes, testes, regressões, rollback e score final.

## 3. Activation

Activate when uma wave ou o programa solicita conclusão, promoção ou verdict.

## 4. Non-activation

Do not activate when a implementação ainda está em progresso ou faltam artefatos obrigatórios.

## 5. Scope

- schema validation
- hash verification
- gate scoring
- critical floors
- claim audit
- rollback proof
- verdict

Out of scope: alterar secrets reais, ignorar políticas do pack, promover deploy,
fazer auto-merge ou substituir gates determinísticos por opinião.

## 6. Inputs

- evidence ledger
- gate results
- test artifacts
- diffs
- ADRs
- security review

Todos os inputs devem apontar para commit, run ou timestamp correspondente.

## 7. Outputs

- judge-report.json
- judge-report.md
- PASS or REWORK_REQUIRED or BLOCKED

Cada output mutável deve possuir hash, owner, status e comando de verificação.

## 8. Workflow

1. Validar schemas e hashes.
2. Verificar comandos, exit codes e artefatos.
3. Aplicar gates e floors críticos sem arredondamento favorável.
4. Reamostrar claims e evidências.
5. Verificar regressão e rollback.
6. Emitir verdict; explicação LLM não substitui falha determinística.

### Staff/Chief challenge

Antes do handoff, responder com evidência:

> Um auditor independente chegaria ao mesmo verdict usando os mesmos artefatos?

Também registrar um contraexemplo, uma alternativa rejeitada e o risco residual.

## 9. Evidence

- validator output
- hash ledger
- score breakdown
- sample audit
- verdict

A evidência deve validar `schemas/evidence.schema.json` e não pode conter PHI,
tokens, cookies, API keys ou secrets.

## 10. Stop conditions

- evidência ausente ou adulterada
- critical gate falho
- score abaixo de 9.8

Ao atingir uma condição, retornar `BLOCKED` ou `REWORK_REQUIRED` com causa raiz,
owner e próxima ação. Não continuar por racionalização.

## 11. Completion

Verdict emitido com cálculo reproduzível e justificativa por gate.

A conclusão local não equivale ao PASS do programa; o Evidence Readiness Judge
deve validar o gate correspondente.
