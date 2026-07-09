# AEOS Production Enterprise Pack v1.2 — Multinational Ready

## Objetivo

Este pacote transforma o AEOS em uma base operacional para ambientes corporativos reais, com foco em:

- governança;
- segurança;
- performance;
- observabilidade;
- auditoria;
- qualidade;
- rollback;
- aprovação;
- supply chain;
- skills e playbooks prontos para uso;
- prompts performáticos para agentes;
- operação em empresas grandes e ambientes regulados.

## Onde descompactar

```powershell
cd E:\GitHub\aeos\AEOS_CHIEF_STAFF_v1

git checkout -b aeos/production-enterprise-v1-2

Expand-Archive -Path "C:\Users\SEU_USUARIO\Downloads\aeos_production_enterprise_pack_v1_2_multinational.zip" -DestinationPath . -Force
```

## Instalação recomendada

1. Criar branch dedicada.
2. Descompactar o ZIP.
3. Rodar auditoria do pacote.
4. Rodar readiness check.
5. Só depois promover os registries.

## Prompt de implementação

```text
Leia INSTALL_PRODUCTION_ENTERPRISE_v1_2.md, AEOS_PRODUCTION_ENTERPRISE_SPEC.md, AEOS_PRODUCTION_ARCHITECTURE.md, AEOS_PERFORMANCE_ENGINEERING.md, AEOS_ENTERPRISE_SECURITY_GOVERNANCE.md e os registries em aeos/registries.

Implemente o AEOS Production Enterprise v1.2 como overlay incremental para uso real em grandes empresas, priorizando:
1. Production profiles;
2. Performance budgets;
3. SLO/SLA guardrails;
4. Enterprise skills;
5. Enterprise playbooks;
6. Optimized prompts;
7. Supply-chain security;
8. Observability with OpenTelemetry-style signals;
9. CI/CD quality gates;
10. Judge enterprise gates;
11. incident and rollback runbooks;
12. benchmark/eval harness.

Regras:
- Não implementar auto-merge.
- Não implementar auto-deploy.
- Não permitir shell irrestrito.
- Não ler secrets reais.
- Não persistir cookies, tokens ou API keys.
- Não permitir approval wildcard.
- Não permitir mutação fora de policy.
- Não permitir bypass de Tool Router.
- Não permitir Judge LLM sobrescrever falha determinística.
- Não importar pack diretamente para active.
- Não aceitar claims sem evidência.
```
