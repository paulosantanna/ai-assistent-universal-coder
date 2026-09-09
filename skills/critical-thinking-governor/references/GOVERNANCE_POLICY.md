# Política de Governança de Pensamento Crítico

## Escopo

Esta política cobre todas as entradas de `aeos/registries/skills.registry.yaml`, inclusive o próprio `critical-thinking-governor`, e herda o agent único definido em `AGENT.md`.

## Baseline imutável

Toda skill recebe quatro lentes internas:

1. `ct-first-principles` para separar fatos, suposições e restrições;
2. `ct-assumption-auditor` para tornar hipóteses testáveis;
3. `ct-evidence-hierarchy` para qualificar a força das provas;
4. `ct-meta-reflection` para desafiar a pergunta e a conclusão.

## Seleção proporcional

A configuração executável define `min_lenses`, `max_lenses`, gatilhos semânticos e overlays por risco. Lentes de risco são obrigatórias; lentes contextuais ocupam apenas as vagas restantes.

| Risco | Lentes adicionais obrigatórias |
|---|---|
| baixo | nenhuma |
| médio | prova do diabo |
| alto | pré-mortem |
| crítico | pré-mortem e bússola ética |

O limite evita inflação de contexto. Um pedido explícito pode selecionar lentes contextuais como Bayes, causalidade, inversão ou debate, mas nunca remover o baseline.

## Relação com Chromatic

As lentes críticas inspecionam a qualidade do raciocínio de cada skill. Perspectivas Chromatic continuam sendo funções de análise/síntese e não identidades de agent. O Judge valida de forma determinística e independente do executor.

## Modelo de agent

- O único agent registrado é `codenavi-agent`.
- Lentes não são agents, subagents ou personas.
- Nenhuma lente possui MCP, LSP, shell ou permissão própria.
- A especialização pertence à skill que a executa.
- Novos métodos de raciocínio devem ser adicionados como lenses, não como agents.

## Independência e privacidade de raciocínio

Cada lente retorna conclusões estruturadas. Não é permitido solicitar ou persistir cadeia de pensamento privada. O registro deve conter fatos, premissas, evidências, alternativas, riscos, incerteza e conclusão — suficientes para auditoria sem conteúdo cognitivo oculto.

## Gates

A execução é bloqueada quando:

- houver quantidade diferente de 20 lentes no catálogo;
- um ID de lente ou prompt ID estiver duplicado;
- o baseline estiver incompleto;
- uma skill registrada não receber plano;
- o plano exceder o limite;
- o runtime tentar executar uma skill sem plano `PASS`;
- o registry contiver qualquer agent além de `codenavi-agent`;
- qualquer subagent estiver registrado;
- o repositório contiver marcadores de conflito nos contratos governados.
