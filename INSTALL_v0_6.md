# AEOS Evolution Pack v0.6 — MCP Runtime Expansion Layer

## Objetivo

Este pacote evolui o AEOS para a camada **v0.6 — MCP Runtime Expansion Layer**.

Ele adiciona contratos, configurações, registries, playbooks, skills e skeletons de runtime para:

- Tool Router controlado;
- MCP Runtime local;
- MCP client via stdio;
- filesystem read-only;
- filesystem write-sandbox;
- git read-only;
- test-runner controlado;
- package local;
- MCP health check;
- MCP discovery;
- timeout/retry/redaction;
- políticas de segurança por conector.

## Onde descompactar

Descompacte este ZIP por cima do projeto AEOS:

```powershell
cd E:\GitHub\aeos\AEOS_CHIEF_STAFF_v1
Expand-Archive -Path "C:\Users\SEU_USUARIO\Downloads\aeos_evolution_pack_v0_6_mcp_runtime.zip" -DestinationPath . -Force
```

## Regra importante

Este pacote é um **overlay incremental**. Ele não substitui a Constituição do AEOS. Ele adiciona a camada MCP Runtime.

## Ainda proibido nesta versão

- secrets runtime real;
- browser com login;
- database write;
- deploy;
- shell irrestrito;
- push;
- merge;
- force push;
- escrita fora do sandbox;
- leitura de valores reais de secrets;
- bypass de Tool Router.

## Próximo prompt para o agente

Use dentro de `E:\GitHub\aeos\AEOS_CHIEF_STAFF_v1`:

```text
Leia INSTALL_v0_6.md, AEOS_V0_6_MCP_RUNTIME.md, AEOS_TOOL_ROUTER_RUNTIME.md, aeos/config/mcp.runtime.yaml, aeos/config/tool-router.config.yaml e aeos/registries/mcps.registry.yaml. Implemente a camada AEOS v0.6 MCP Runtime Expansion garantindo que todo acesso externo passe pelo Tool Router, Permission Engine, Policy Engine, MCP Registry, Evidence Store e Judge. Não implemente secrets runtime real, browser com login, deploy, shell irrestrito, push ou merge.
```
