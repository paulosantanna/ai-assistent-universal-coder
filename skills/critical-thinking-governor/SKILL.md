---
name: critical-thinking-governor
description: Governa toda execução de skills do AEOS com uma seleção limitada e auditável de 20 agentes de pensamento crítico. Ativa automaticamente no roteamento e no runtime; não substitui skills de domínio, ferramentas, testes ou o Judge independente.
---

# Critical Thinking Governor

## Missão

Aplicar pensamento crítico proporcional ao risco antes, durante e depois de cada skill do AEOS, sem transformar tarefas simples em debates artificiais.

## Contrato obrigatório

1. Toda skill registrada recebe um plano de governança antes de executar.
2. O plano sempre inclui primeiros princípios, auditoria de suposições, hierarquia de evidências e metarreflexão.
3. Agentes adicionais são selecionados por risco e sinais do pedido, respeitando o limite configurado.
4. Skills de risco alto ou crítico recebem análise pré-mortem; risco crítico também recebe bússola ética.
5. Ausência, corrupção ou inconsistência do plano bloqueia a execução.
6. O Judge permanece independente e avalia a evidência resultante.

## Limites

Os agentes de pensamento crítico:

- não executam MCPs, LSPs, shell ou mutações;
- não substituem especialistas de domínio;
- não promovem memória por conta própria;
- não expõem cadeia de pensamento privada;
- não inventam probabilidades, fontes ou fatos;
- registram somente conclusões auditáveis, premissas, evidências, riscos e limitações.

## Fluxo

```text
Pedido
→ Skill Router
→ Skill selecionada
→ Plano Critical Thinking
→ Agentes obrigatórios + agentes proporcionais ao risco
→ Execução da skill
→ Evidência e contradições
→ Chromatic Synthesis quando aplicável
→ Judge independente
```

## Fontes canônicas

- Política executável: `aeos/config/critical-thinking-governance.config.json`.
- Contratos dos agentes: `agents/*.md`.
- Regras e matriz de seleção: `references/GOVERNANCE_POLICY.md`.

Leia a referência ao alterar seleção, limites, gates ou integração com Chromatic/Judge.

## Saída mínima

Cada análise selecionada deve produzir, quando aplicável:

- `facts`;
- `assumptions`;
- `evidence_refs`;
- `risks`;
- `recommendation`;
- `confidence` com base explícita;
- `limitations`;
- `blocking_conditions`.

## Validação

Execute:

```bash
npm run aeos:guard:critical-thinking
npm run aeos:verify
```

A skill só está válida quando os 20 agentes existem, estão registrados, o catálogo é íntegro, todas as skills estão cobertas e o runtime falha fechado sem plano.
