# AEOS Security Model — v1.0.0

## 1. Propósito

Define as políticas e mecanismos de segurança que protegem o ecossistema AEOS contra vazamento de segredos, ações não autorizadas e violações de integridade.

## 2. Princípios

1. **Zero Trust** — Nenhuma ação é confiável sem verificação.
2. **Least Privilege** — Cada agente tem o mínimo necessário.
3. **Defense in Depth** — Múltiplas camadas de proteção.
4. **Immutable Audit** — Logs de segurança são imutáveis.
5. **Human-in-the-Loop** — Decisões críticas exigem humano.

## 3. Camadas de Segurança

```
Layer 0: Constitution — Regras fundamentais (imutáveis)
Layer 1: Policy Engine — Regras de domínio
Layer 2: Permission Model — Controle de acesso
Layer 3: Tool Router — Validação em tempo real
Layer 4: Secrets Scanner — Detecção de segredos
Layer 5: Redaction Engine — Ofuscação automática
Layer 6: Audit Logger — Registro imutável
```

## 4. Secrets Scanner

### 4.1 Padrões Detectados
- API Keys (formato alfanumérico 16-64 chars)
- AWS Access Keys (AKIA...)
- GitHub Tokens (ghp_..., ghs_...)
- JWT Tokens
- Private Keys (---BEGIN...)
- Connection Strings
- Passwords in code
- Tokens in URLs

### 4.2 Ação em Detecção
1. Bloquear operação imediatamente.
2. Redigir o segredo (replacement com ***).
3. Registrar incidente de segurança.
4. Notificar operador humano.
5. Nunca persistir o valor original.

## 5. Redaction Engine

### 5.1 Entrada
- Logs
- Prompts
- Traces
- Reports
- Evidências
- Arquivos versionados

### 5.2 Mecanismo
```yaml
redaction:
  enabled: true
  mask_char: "*"
  mask_ratio: 0.75
  patterns:
    - regex: "(?i)(password|secret|token|key)[=:]\s*\S+"
      replacement: "$1=***REDACTED***"
    - regex: "AKIA[0-9A-Z]{16}"
      replacement: "AKIA***REDACTED***"
    - regex: "gh[psou]_[0-9a-zA-Z]{36}"
      replacement: "gh***REDACTED***"
```

## 6. Approval System

### 6.1 Ações que Exigem Aprovação
- Deletar arquivos ou diretórios
- Modificar produção
- Alterar políticas de segurança
- Escalar permissões
- Registrar novas ferramentas
- Executar scripts não verificados

### 6.2 Fluxo de Aprovação
```
Agent solicita → Kernel valida → Policy Engine verifica → Approval Request gerado → 
Humano aprova/rejeita → Resultado registrado → Ação executada ou bloqueada
```

## 7. Segurança de Dados

- Nenhum segredo em texto puro em qualquer saída.
- Nenhum segredo em código versionado.
- Nenhum segredo em logs, prompts, traces ou relatórios.
- Evidências são hashadas (SHA256) para integridade.
- Memórias sensíveis são criptografadas.

## 8. Incident Response

| Evento | Severidade | Ação |
|--------|-----------|------|
| Secret detected | Critical | Block + Notify + Incident report |
| Permission violation | High | Block + Notify + Audit |
| Tool router bypass | Critical | Block + Notify + Kill agent |
| Policy change unauthorized | Critical | Revert + Notify + Audit |
| Judge integrity violation | Critical | Invalidate + Notify + Escalate |

## 9. Auditoria

- 100% das operações são logadas.
- Logs de segurança têm retenção de 365 dias.
- Logs são imutáveis (append-only).
- Relatórios de segurança são gerados automaticamente.
