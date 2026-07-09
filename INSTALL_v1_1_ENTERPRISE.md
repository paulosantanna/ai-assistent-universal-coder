# AEOS Unique Environment Pack v1.1 Enterprise — Instalação

Este é um pacote grande e consolidado para transformar o AEOS em um ambiente AI-First único, extensível e governado.

## Onde descompactar

```powershell
cd E:\GitHub\aeos\AEOS_CHIEF_STAFF_v1
Expand-Archive -Path "C:\Users\SEU_USUARIO\Downloads\aeos_unique_environment_pack_v1_1_enterprise.zip" -DestinationPath . -Force
```

## Recomendação

Antes de descompactar:

```powershell
cd E:\GitHub\aeos\AEOS_CHIEF_STAFF_v1
git checkout -b aeos/unique-environment-v1-1
git status
```

## O que este pacote adiciona

- Ambiente AEOS Enterprise.
- Blueprints por stack.
- Packs de domínio.
- Skill Factory avançada.
- Playbook Factory avançada.
- MCP Gateway.
- LCP Studio.
- Workbench profiles.
- Test harness.
- Corpus sintético de validação.
- Evals anti-alucinação.
- Observabilidade avançada.
- Compliance/Audit.
- Security hardening.
- Templates de projetos Java, Python, Fullstack, AI/RAG e DevOps.
- Runbooks de incidentes.
- Fixtures grandes para testes de performance, cache, evidência e Judge.

## Não é lixo de padding

O ZIP passa de 10 MB porque inclui fixtures sintéticos e corpus de validação para testar:
- scanners;
- stack detector;
- evidence cache;
- hash-chain;
- Judge;
- redaction;
- package verification;
- playbook execution;
- agent runtime;
- prompt injection defense;
- MCP tool poisoning defense.

## Próximo prompt para o agente

```text
Leia INSTALL_v1_1_ENTERPRISE.md, AEOS_UNIQUE_ENVIRONMENT_SPEC.md, AEOS_ENTERPRISE_ARCHITECTURE.md, AEOS_WORKBENCH_PROFILES.md e os registries em aeos/registries. Implemente o AEOS v1.1 Enterprise Unique Environment como overlay incremental, priorizando: Workbench Profiles, Blueprint Engine, Skill/Playbook Factory, Evaluation Harness, Security Hardening, Test Harness, MCP Gateway, LCP Studio e validação com fixtures sintéticos. Não implemente auto-merge, auto-deploy, shell irrestrito, secrets reais, browser autenticado com cookies reais, bypass de auditoria ou qualquer mutação fora de política.
```
