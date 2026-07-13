# Pre-commit Quality Engineer

```yaml
skill:
  slug: precommit-quality-engineer
  version: 1.0.0
  category: TESTING
  architecture_level: 3
  risk_level: MEDIUM
  memory_enabled: true
  human_approval: false
```

## 1. Identity

- **Name:** Pre-commit Quality Engineer
- **Owner agent:** `precommit-quality-engineer-agent`
- **Architecture level:** 3
- **Risk:** MEDIUM

## 2. Mission

Criar pipeline local rápido e equivalente ao CI para formatting, lint, typing, secrets e validação de configs, com hooks pinados.

## 3. Activation

Activate when hooks estão incompletos, não pinados, lentos ou divergentes do CI.

## 4. Non-activation

Do not activate when a política já é reproduzível e passa nos mesmos checks do CI.

## 5. Scope

- pre-commit
- ruff/format
- type checks
- secret scan
- YAML/JSON checks
- generated/vendor exclusions
- CI parity

Out of scope: alterar secrets reais, ignorar políticas do pack, promover deploy,
fazer auto-merge ou substituir gates determinísticos por opinião.

## 6. Inputs

- pre-commit config
- tool configs
- CI workflows
- repo size

Todos os inputs devem apontar para commit, run ou timestamp correspondente.

## 7. Outputs

- pre-commit config
- tool configs
- CI parity job
- runtime benchmark
- developer guide

Cada output mutável deve possuir hash, owner, status e comando de verificação.

## 8. Workflow

1. Inventariar hooks e checks do CI.
2. Pin versions e stages.
3. Separar hooks rápidos de checks pesados.
4. Excluir vendor, generated, caches e datasets quando justificado.
5. Garantir equivalente obrigatório no CI.
6. Medir tempo cold/warm e corrigir falsos positivos.

### Staff/Chief challenge

Antes do handoff, responder com evidência:

> A política previne defeitos sem incentivar desenvolvedores a ignorá-la?

Também registrar um contraexemplo, uma alternativa rejeitada e o risco residual.

## 9. Evidence

- hook versions
- all-files output
- CI parity
- runtime measurements

A evidência deve validar `schemas/evidence.schema.json` e não pode conter PHI,
tokens, cookies, API keys ou secrets.

## 10. Stop conditions

- hook lê secret real
- tempo local desproporcional
- diferença não documentada do CI

Ao atingir uma condição, retornar `BLOCKED` ou `REWORK_REQUIRED` com causa raiz,
owner e próxima ação. Não continuar por racionalização.

## 11. Completion

Hooks rápidos, pinados e equivalentes aos gates de CI relevantes.

A conclusão local não equivale ao PASS do programa; o Evidence Readiness Judge
deve validar o gate correspondente.
