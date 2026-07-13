# Crítica técnica do plano original

## Evidência insuficiente

“~40% E2E”, “45 subpacotes” e “0% documentação de API” precisam de método
reproduzível. O pack exige claims matrix e metric dictionary.

## Escopo possivelmente inventado

“Pagamento” não é considerado fluxo até existir evidência no código,
documentação, telemetria, teste ou interface.

## Gantt inconsistente

Os esforços em dias não combinam com blocos de 30–90 dias, e as datas de 2025
e início de 2026 estão vencidas. O pack usa waves e reestimativa pós-baseline.

## Cache RAG simplificado demais

Redis + TTL não resolve PHI, isolamento, versão de evidência, modelo/prompt/index,
colisão semântica e invalidação. O default é deny para classes de alto risco.

## Health com semântica errada

Dependência externa indisponível não significa processo morto. Liveness externa
pode criar reinícios em cascata.

## Config não deve virar um único mecanismo

Pydantic Settings serve runtime settings. Políticas, parâmetros científicos e
manifests podem continuar em YAML/JSON com schema e provenance.

## Modularização subestimada

Mover dezenas de pacotes sem grafo e contracts aumenta ciclos. A migração deve
ser incremental.

## Accuracy operacional não é trivial

Sem ground truth, dashboards não devem publicar accuracy. Use métricas de
abstention, block rate, citation, retrieval em datasets rotulados e groundedness
em evaluation runs.

## Dead code exige análise de runtime

Plugins, registries, reflection, jobs e configs podem carregar código sem import
estático.

## Release precisa de boundary

Release PR e changelog podem ser automatizados. Auto-merge e auto-deploy não.
