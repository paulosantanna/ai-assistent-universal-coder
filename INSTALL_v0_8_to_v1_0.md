# AEOS Major Evolution Pack v0.8 → v1.0

## Objetivo

Este pacote é um **overlay grande e consolidado** para evoluir o AEOS além dos passos pequenos anteriores.

Ele cobre:

```text
v0.8  — Parallel Execution, Dependency Graph & Conflict Detection
v0.9  — Advanced Approval, Evidence Cache, Observability & Notifications
v0.95 — Security Hardening, Secrets Governance, Compliance & Pack Marketplace
v1.0  — Stable AEOS Workbench Readiness
```

## Onde descompactar

```powershell
cd E:\GitHub\aeos\AEOS_CHIEF_STAFF_v1
Expand-Archive -Path "C:\Users\SEU_USUARIO\Downloads\aeos_major_evolution_pack_v0_8_to_v1_0.zip" -DestinationPath . -Force
```

## Este pacote pressupõe que você já aplicou

```text
aeos_bootstrap_pack_v0_5.zip
aeos_evolution_pack_v0_6_mcp_runtime.zip
aeos_evolution_pack_v0_7_agent_runtime.zip
```

## O que este pacote adiciona

- Parallel Playbook Engine com dependências e conflito read/write.
- Evidence Cache com chave forte e invalidação segura.
- Advanced Approval Gateway com expiração, escopo, assinatura local e audit trail.
- Observability com traces, metrics, logs, token/cost accounting e run dashboard.
- Test Runner real controlado com parser de resultados.
- PR Workflow governado, sem merge automático.
- Local Pack Marketplace para skills/playbooks/LCPs/MCP profiles.
- Security Hardening com threat model, secret redaction, package quarantine e trust policy.
- Compliance templates: LGPD/GDPR-ready docs, audit logs e retention policy.
- v1.0 readiness checklist com gates obrigatórios.

## Ainda proibido

- auto-merge;
- deploy automático;
- force push;
- bypass de auditoria;
- secrets runtime sem política dedicada;
- shell irrestrito;
- browser com login usando cookies reais sem governança;
- banco com escrita;
- produção sem aprovação humana explícita;
- executar código baixado sem quarentena/verificação.

## Próximo prompt para seu agente

```text
Leia INSTALL_v0_8_to_v1_0.md, AEOS_V1_0_WORKBENCH_SPEC.md e todos os arquivos AEOS_V0_8_*, AEOS_V0_9_*, AEOS_V0_95_* deste pacote. Implemente as camadas v0.8 a v1.0 como overlay incremental, respeitando integralmente a Constituição AEOS, Kernel, Permission Engine, Policy Engine, Tool Router, MCP Runtime, Agent Runtime, Evidence Store, Judge Layer e Packaging Layer. Priorize segurança, evidência, rollback, aprovação granular, integridade e bloqueios determinísticos. Não implemente auto-merge, deploy automático, shell irrestrito, secrets runtime real sem política, browser autenticado com cookies reais ou qualquer bypass de auditoria.
```
