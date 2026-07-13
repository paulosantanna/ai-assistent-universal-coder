# Waves e concorrência

| Wave | Foco | Paralelismo |
|---|---|---|
| W0 | baseline, métricas, benchmark | até 3, read-only |
| W1 | OpenAPI, errors, E2E | OpenAPI/errors paralelos; E2E depois |
| W2 | modularização, cache, health | até 3, com approval |
| W3 | config, observability, C4 | config/observability paralelos |
| W4 | release, dead code, pre-commit | release/pre-commit paralelos |
| W5 | benchmark, safety, metrics, judge | validação sem mutação |
