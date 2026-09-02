# Política de Governança de Pensamento Crítico

## Escopo

Esta política cobre todas as entradas de `aeos/registries/skills.registry.yaml`, inclusive o próprio `critical-thinking-governor`.

## Baseline imutável

Toda skill recebe:

1. `ct-first-principles` para separar fatos, suposições e restrições;
2. `ct-assumption-auditor` para tornar hipóteses testáveis;
3. `ct-evidence-hierarchy` para qualificar a força das provas;
4. `ct-meta-reflection` para desafiar a pergunta e a conclusão.

## Seleção proporcional

A configuração executável define `min_agents`, `max_agents`, gatilhos semânticos e overlays por risco. Agentes de risco são obrigatórios; agentes contextuais ocupam apenas as vagas restantes.

| Risco | Agentes adicionais obrigatórios |
|---|---|
| baixo | nenhum |
| médio | prova do diabo |
| alto | pré-mortem |
| crítico | pré-mortem e bússola ética |

O limite evita inflação de contexto. Um pedido explícito pode selecionar agentes contextuais como Bayes, causalidade, inversão ou debate, mas nunca remover o baseline.

## Relação com Chromatic

Os agentes críticos inspecionam a qualidade do raciocínio de cada skill. Os agentes de cores analisam perspectivas multidisciplinares em decisões complexas. O Synthesis Agent integra sem apagar dissenso. O Judge valida de forma independente.

## Independência e privacidade de raciocínio

Cada agente retorna conclusões estruturadas. Não é permitido solicitar ou persistir cadeia de pensamento privada. O registro deve conter fatos, premissas, evidências, alternativas, riscos, incerteza e conclusão — suficientes para auditoria sem conteúdo cognitivo oculto.

## Gates

A execução é bloqueada quando:

- houver menos ou mais de 20 especialistas no catálogo;
- um agente não existir ou não estiver registrado;
- algum prompt ID estiver duplicado;
- o baseline estiver incompleto;
- uma skill registrada não receber plano;
- o plano exceder o limite;
- o runtime tentar executar uma skill sem plano `PASS`;
- o repositório contiver marcadores de conflito nos contratos governados.
