# Token and Context Governor

```yaml
skill:
  slug: token-context-governor
  version: 1.0.0
  category: GOVERNANCE
  architecture_level: 3
  risk_level: HIGH
  memory_enabled: true
  human_approval: true
```

## 1. Identity

- **Name:** Token and Context Governor
- **Owner agent:** `token-context-governor-agent`
- **Architecture level:** 3
- **Risk:** HIGH

## 2. Mission

Reduzir custo e perda de contexto por roteamento, leitura seletiva, deduplicação, checkpoints e respawn controlado.

## 3. Activation

Activate when qualquer agente ou subagente usa LLM no pack.

## 4. Non-activation

Do not activate when a tarefa é resolvida integralmente por ferramenta determinística.

## 5. Scope

- model routing
- token budgets
- context selection
- checkpointing
- compression
- respawn
- cost ledger

Out of scope: alterar secrets reais, ignorar políticas do pack, promover deploy,
fazer auto-merge ou substituir gates determinísticos por opinião.

## 6. Inputs

- task risk
- context size
- available aliases
- prior checkpoints
- evidence index

Todos os inputs devem apontar para commit, run ou timestamp correspondente.

## 7. Outputs

- routing-decision.json
- token-ledger.json
- checkpoints
- compressed handoff

Cada output mutável deve possuir hash, owner, status e comando de verificação.

## 8. Workflow

1. Tentar ferramenta determinística primeiro.
2. Selecionar alias por risco e contexto, não por preferência fixa.
3. Carregar apenas arquivos e evidências relevantes.
4. Checkpoint em 40%, 70% e 85%.
5. Respawn obrigatório em 95% com handoff completo.
6. Registrar tokens estimados, reutilização e conteúdo omitido.

### Staff/Chief challenge

Antes do handoff, responder com evidência:

> Estamos pagando tokens para raciocínio novo ou reenviando contexto que já poderia estar indexado?

Também registrar um contraexemplo, uma alternativa rejeitada e o risco residual.

## 9. Evidence

- routing decision
- token ledger
- checkpoint hashes
- duplicate-context ratio

A evidência deve validar `schemas/evidence.schema.json` e não pode conter PHI,
tokens, cookies, API keys ou secrets.

## 10. Stop conditions

- contexto excede budget
- checkpoint inválido
- repetição de trabalho concluído

Ao atingir uma condição, retornar `BLOCKED` ou `REWORK_REQUIRED` com causa raiz,
owner e próxima ação. Não continuar por racionalização.

## 11. Completion

Tarefa entregue dentro do budget ou retomável sem perda de decisões e evidências.

A conclusão local não equivale ao PASS do programa; o Evidence Readiness Judge
deve validar o gate correspondente.
