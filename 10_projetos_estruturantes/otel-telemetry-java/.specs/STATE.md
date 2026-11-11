# Project state — otel-telemetry-java

## Decisions

| ID | Decision | Rationale | Status | Date |
| --- | --- | --- | --- | --- |
| AD-001 | A biblioteca fala apenas OTLP; Dynatrace/Splunk/Grafana/Collector são presets de endpoint+auth | zero lock-in; um fio para todos os backends (plano v3) | active | 2026-11-10 |
| AD-002 | Artefatos compilam `--release 21` com toolchain JDK 25 | class file 69 não carrega em consumidores 17/21 (J-F1, decisão do owner) | active | 2026-11-10 |
| AD-003 | Precedência de configuração: `OTEL_*` env > sysprop `otel.*` > `oteltelemetry.yaml` > builder; credenciais só por runtime env | interop com operadores Kubernetes dos vendors; sem segredo em arquivo rastreado | active | 2026-11-10 |
| AD-004 | Sink offline grava `traces/metrics/logs.jsonl`, uma linha por requisição OTLP decodificada (OTLP JSON), com rotação | formato consumível pelo dashboard sem segunda normalização (door 1) | active | 2026-11-10 |
| AD-005 | Sink bind `127.0.0.1:14318` por padrão; host/porta por config; token opcional; 503 quando disabled | expor telemetria (possível PII) na rede é defeito; 4318 colide com Collector real (J-F3) | active | 2026-11-10 |
| AD-006 | Fail-soft: telemetria nunca derruba o app consumidor | missão da biblioteca; IF config/export falha → no-op + diagnóstico | active | 2026-11-10 |
| AD-007 | `otel-telemetry-devtools` contém sink + dashboard (dashboard é asset do sink) | reduzir superfície de módulos v1 (J-F8) | active | 2026-11-10 |
| AD-008 | Preset Rust nasce com status experimental (SDK 0.x) | opentelemetry (crates) 0.33.1 em 2026-10-09 | active | 2026-11-10 |
| AD-009 | Endpoints/auth de vendor sem doc real ficam rotulados NÃO VERIFICADO no código e no README | gate J1 falha fechada; DO NOT INVENT | active | 2026-11-10 |
