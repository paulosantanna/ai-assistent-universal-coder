# AEOS Policy Engine — v1.0.0

## 1. Propósito

O Policy Engine interpreta e aplica regras de conduta em tempo de execução. É o guardião da Constituição no plano operacional.

## 2. Arquitetura

```
Request → Policy Enforcer → Rule Matcher → Decision → Action
                ↑                 ↑
           Policy Store      Rule Cache
```

## 3. Hierarquia de Políticas

```
Constitutional (imutável)
├── Artifacto I: Primazia da Evidência
├── Artifacto II: Soberania Humana
├── Artifacto III: Separação de Poderes
│
Domain Policies (mutável com aprovação)
├── Ecosystem Scanning Policy
├── Code Modification Policy
├── Security Policy
├── Memory Policy
├── Judge Policy
│
Operational Policies (mutável com aprovação)
├── Tool Access Policy
├── Agent Delegation Policy
├── Evidence Collection Policy
└── Logging Policy
```

## 4. Formato de Regra

```yaml
rule_id: "pol-001"
name: "No Direct Filesystem Access"
type: "constitutional"
description: "Nenhum agente pode acessar filesystem diretamente"
scope: ["all"]
condition: "request.target == 'filesystem' AND request.source != 'kernel.tool_router'"
action: "block"
severity: "critical"
message: "Acesso direto a filesystem bloqueado. Use Kernel/Tool Router."
```

## 5. Engine de Decisão

| Input | Processo | Output |
|-------|----------|--------|
| Tool request | Match rules → Evaluate conditions → Aggregate decisions | ALLOW / BLOCK / REQUIRE_APPROVAL |
| Agent action | Match rules → Evaluate conditions → Aggregate decisions | ALLOW / BLOCK / REQUIRE_APPROVAL |
| Evidence submission | Validate format → Check completeness | VALID / INVALID |
| Task completion | Check evidence → Check approvals → Check rollback | READY / BLOCKED |

## 6. Cache e Performance

- Regras constitucionais são cacheadas em memória.
- Regras de domínio são recarregadas a cada 5 minutos.
- Regras operacionais são avaliadas em tempo real.
- Toda decisão é cacheadada por 60 segundos.

## 7. Auditoria

Toda decisão do Policy Engine é registrada:
- timestamp, request, rule matched, decision, agent_id.
- Logs são imutáveis.
- Relatórios de violação são gerados automaticamente.
