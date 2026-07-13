# Problem Details Error Governor

```yaml
skill:
  slug: problem-details-error-governor
  version: 1.0.0
  category: GOVERNANCE
  architecture_level: 3
  risk_level: HIGH
  memory_enabled: true
  human_approval: true
```

## 1. Identity

- **Name:** Problem Details Error Governor
- **Owner agent:** `problem-details-error-governor-agent`
- **Architecture level:** 3
- **Risk:** HIGH

## 2. Mission

Padronizar erros HTTP em contrato compatível com RFC 9457, códigos estáveis, correlação e proteção contra vazamento.

## 3. Activation

Activate when endpoints retornam formatos divergentes, mensagens instáveis ou detalhes sensíveis.

## 4. Non-activation

Do not activate when a mudança não envolve superfície de erro HTTP.

## 5. Scope

- exception hierarchy
- global handlers
- problem schema
- machine codes
- correlation ID
- logging policy
- tests

Out of scope: alterar secrets reais, ignorar políticas do pack, promover deploy,
fazer auto-merge ou substituir gates determinísticos por opinião.

## 6. Inputs

- exceptions atuais
- rotas
- request context
- security policy

Todos os inputs devem apontar para commit, run ou timestamp correspondente.

## 7. Outputs

- problem model
- handlers
- error catalog
- tests
- migration notes

Cada output mutável deve possuir hash, owner, status e comando de verificação.

## 8. Workflow

1. Inventariar formatos e status existentes.
2. Definir catálogo de códigos estáveis e mapeamento de exceções.
3. Implementar handlers globais e preservar headers necessários.
4. Separar detalhe interno de mensagem pública.
5. Propagar correlation ID entre resposta, log e trace.
6. Adicionar testes de contrato e redaction.

### Staff/Chief challenge

Antes do handoff, responder com evidência:

> O contrato é estável para máquinas e seguro para usuários?

Também registrar um contraexemplo, uma alternativa rejeitada e o risco residual.

## 9. Evidence

- error catalog
- response snapshots
- security tests
- trace correlation evidence

A evidência deve validar `schemas/evidence.schema.json` e não pode conter PHI,
tokens, cookies, API keys ou secrets.

## 10. Stop conditions

- stack trace exposto
- status semanticamente incorreto
- cliente crítico quebrado sem migração

Ao atingir uma condição, retornar `BLOCKED` ou `REWORK_REQUIRED` com causa raiz,
owner e próxima ação. Não continuar por racionalização.

## 11. Completion

Todas as rotas cobertas retornam contrato uniforme e seguro.

A conclusão local não equivale ao PASS do programa; o Evidence Readiness Judge
deve validar o gate correspondente.
