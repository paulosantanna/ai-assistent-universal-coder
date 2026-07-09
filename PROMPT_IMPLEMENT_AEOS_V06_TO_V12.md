# PROMPT FINAL - IMPLEMENTAR AEOS v0.6 ATE v1.2

Leia todos os arquivos aplicados pelos overlays v0.6, v0.7, v0.8-v1.0, v1.1 e v1.2.

Arquivos principais:
- INSTALL_v0_6.md
- INSTALL_v0_7.md
- INSTALL_v0_8_to_v1_0.md
- INSTALL_v1_1_ENTERPRISE.md
- INSTALL_PRODUCTION_ENTERPRISE_v1_2.md
- AEOS_V0_6_MCP_RUNTIME.md
- AEOS_V0_7_AGENT_RUNTIME.md
- AEOS_V1_0_WORKBENCH_SPEC.md
- AEOS_UNIQUE_ENVIRONMENT_SPEC.md
- AEOS_PRODUCTION_ENTERPRISE_SPEC.md
- AEOS_PRODUCTION_ARCHITECTURE.md
- AEOS_PERFORMANCE_ENGINEERING.md
- AEOS_ENTERPRISE_SECURITY_GOVERNANCE.md
- AEOS_PRODUCTION_READY_CHECKLIST.md

Objetivo:
Implementar o AEOS como ambiente AI-First governado, performatico e production-ready para uso corporativo, respeitando Kernel, Permission Engine, Policy Engine, Tool Router, MCP Runtime, Agent Runtime, Evidence Store, Judge Layer, Packaging Layer, Observability, Performance Budgets, Enterprise Skills e Enterprise Playbooks.

Ordem de implementacao:
1. Validar configs e registries.
2. Criar/atualizar loader de overlay registries.
3. Implementar Tool Router e MCP Runtime v0.6.
4. Implementar Agent Runtime e Delegation Layer v0.7.
5. Implementar Parallel Execution, Conflict Detection e Evidence Cache v0.8-v0.9.
6. Implementar Observability, Advanced Approval e Pack Marketplace.
7. Implementar Workbench Profiles, Blueprint Engine e Evaluation Harness v1.1.
8. Implementar Production Enterprise Layer v1.2.
9. Implementar Enterprise Skills e Enterprise Playbooks.
10. Implementar testes negativos para todos os gates criticos.
11. Rodar readiness audit e gerar Judge final.

Regras nao negociaveis:
- Nao implementar auto-merge.
- Nao implementar auto-deploy.
- Nao permitir shell irrestrito.
- Nao ler secrets reais.
- Nao persistir cookies, tokens ou API keys.
- Nao permitir approval wildcard.
- Nao permitir mutacao fora de policy.
- Nao permitir bypass de Tool Router.
- Nao permitir direct MCP access.
- Nao permitir Judge LLM sobrescrever falha deterministica.
- Nao importar pack diretamente para active.
- Nao aceitar claims sem evidencia.
- Nao finalizar sem Judge report.
- Nao finalizar sem evidence verify.

Ao final, gere:
1. arvore de arquivos alterada;
2. modulos implementados;
3. comandos novos;
4. registries carregados;
5. skills ativadas;
6. playbooks ativados;
7. testes criados;
8. evals executados;
9. performance budget report;
10. security report;
11. production readiness score;
12. Judge final PASS/BLOCKED.
