---
name: critical-thinking-governor
description: Governa toda execução de skills do AEOS com uma seleção limitada e auditável de 20 lentes internas de pensamento crítico. As lentes são especializações da skill e nunca identidades de agent.
---

# Critical Thinking Governor

Governance: CodENavi image standard

## Missão

Aplicar pensamento crítico proporcional ao risco antes, durante e depois de cada skill do AEOS sem criar agents especialistas e sem transformar tarefas simples em debates artificiais.

## Contrato obrigatório

1. Toda skill registrada recebe um plano de governança antes de executar.
2. O plano sempre inclui as lentes de primeiros princípios, auditoria de suposições, hierarquia de evidências e metarreflexão.
3. Lentes adicionais são selecionadas por risco e sinais do pedido, respeitando o limite configurado.
4. Skills de risco alto ou crítico recebem a lente pré-mortem; risco crítico também recebe a lente de bússola ética.
5. Ausência, corrupção ou inconsistência do plano bloqueia a execução.
6. O Judge permanece um gate determinístico independente; ele não é uma persona de agent.
7. A execução inteira herda `AGENT.md` e o ciclo BRIEFING → RECON → PLAN → EXECUTE → VERIFY → DEBRIEF.

## Limites

As lentes de pensamento crítico:

- são funções internas da skill, não agents ou subagents;
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
→ Lentes obrigatórias + lentes proporcionais ao risco
→ Execução da skill
→ Evidência e contradições
→ Chromatic Synthesis quando aplicável
→ Judge determinístico
```

## Fontes canônicas

- Agent único: `AGENT.md`.
- Política executável: `aeos/config/critical-thinking-governance.config.json`.
- Regras e matriz de seleção: `references/GOVERNANCE_POLICY.md`.

Não crie arquivos `.agent.md`, `.subagent.md` ou identidades adicionais para implementar uma lente.

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
npm run aeos:guard:single-agent
npm run aeos:verify
```

A skill só está válida quando as 20 lentes estão íntegras, nenhuma delas existe como agent, todas as skills estão cobertas e o runtime falha fechado sem plano válido.
