# otel-telemetry-java

Biblioteca Java de telemetria OpenTelemetry (traces/metrics/logs) com OTLP-only, presets de
destino, sink offline + dashboard e starter Spring Boot. Falha sempre de forma suave: app não
pode derrubar por causa de telemetria (AD-006).

**Ferramental:** roda em JDK 25 (`.tools/jdk25`), bytecode `--release 21`, Maven wrapper.

## Módulos

| Módulo | Papel |
| --- | --- |
| `otel-telemetry-core` | Bootstrap fail-soft + resolução de config (env > sysprop > yaml > builder) |
| `otel-telemetry-exporters` | SPI `OtlpRuntimeProvider`: SDK OTel completo com exporters OTLP por preset |
| `otel-telemetry-adapters` | Logback (appender programático) + Micrometer (bridge upstream) |
| `otel-telemetry-spring-boot-starter` | Auto-config (`oteltelemetry.*`) para Spring Boot 4.1 |
| `otel-telemetry-devtools` | Sink OTLP/HTTP loopback + dashboard (jar servindo `/`) |
| `otel-telemetry-examples/*` | Java puro (1 linha) e Spring Boot, presets multilíngue |

## Quick start

```java
// uma linha; destino por env/sysprop/yaml (default offline → sink local 127.0.0.1:14318)
Telemetry telemetry = TelemetryBootstrap.start(builder -> builder.serviceName("meu-svc"));
```

```bash
# sink + dashboard — classpath em dois passos (evita $(...) aninhado no mvnw; provado nesta máquina)
./mvnw -q install -DskipTests -pl otel-telemetry-devtools
./mvnw -q -pl otel-telemetry-devtools dependency:build-classpath -Dmdep.outputFile=target/cp.txt
java -cp "otel-telemetry-devtools/target/otel-telemetry-devtools-1.0.0.jar;<conteúdo de otel-telemetry-devtools/target/cp.txt>" \
    com.aeos.telemetry.devtools.SinkMain
# dashboard: http://127.0.0.1:14318/ · health: /api/health · auth opcional: OTELTELEMETRY_SINK_TOKEN
```

## Configuração (AD-003)

Precedência: **env > sysprop > `oteltelemetry.yaml` > builder**. Credenciais só de env runtime.

- env: `OTEL_SERVICE_NAME`, `OTELTELEMETRY_PRESET`, `OTEL_EXPORTER_OTLP_ENDPOINT` (e `*_TRACES/_METRICS/_LOGS_ENDPOINT`), `OTEL_EXPORTER_OTLP_HEADERS`
- yaml (chaves planas): `exporter.otlp.endpoint`, `exporter.otlp.traces.endpoint`, `exporter.otlp.traces.headers`
- presets: `offline` (default), `otelcol`, `splunk`, `dynatrace` (http/protobuf + `OTEL_DYNATRACE_TOKEN`), `grafana` (`OTEL_GRAFANA_INSTANCE` + `OTEL_GRAFANA_TOKEN`)
- dynatrace/grafana: somente http/protobuf (grpc rejeitado por design do preset)

## Sink offline (AD-004)

- bind default `127.0.0.1:14318`; `OTELTELEMETRY_SINK_{HOST,PORT,TOKEN,DISABLED,DIR,MAX_MB,MAX_FILES,MAX_AGE_MINUTES}`
- auth exigida com token configurado OU bind não-loopback (`Authorization: Bearer`, comparação constante-tempo); `/api/health` isento
- `disabled=1` → 503 sem gravar; payload inválido → 400 com causa, arquivo íntegro
- gravação: OTLP-JSON uma linha por mensagem (`{signal}.jsonl`), rotação por tamanho/idade com teto de arquivos

## Dashboard

- **live** (servido pelo sink em `/`): consulta `/api/{traces,metrics,logs}?since&limit` a cada 2 s; métricas somadas monotônicas plotadas em modo **delta**
- **arquivo** (duplo clique no `index.html` do jar deszipado — ou `dashboard/public/index.html` compilado): drag-drop de `.jsonl`; bundle iife com caminhos relativos
- cap de carga: janela de 5000 registros em memória (mais recentes), 200 linhas por aba

## Status de verificação (2026-11-11)

| Área | Evidência | Status |
| --- | --- | --- |
| Config (C1-C4, C8) | `mvnw test -pl otel-telemetry-core` — 10/10 | ✅ automatizado |
| Presets/URLs (C5-C7) | `mvnw test -pl otel-telemetry-exporters` — 10/10 | ✅ automatizado (rotas dynatrace/grafana **NÃO VERIFICADO (J1)**: docs 403/404 na data; shape definido pelo plano) |
| Adapters/starter (C9-C12) | `mvnw test -pl otel-telemetry-adapters,otel-telemetry-spring-boot-starter` — 4/4 | ✅ automatizado |
| Sink (C13-C19, C26-C27) | `mvnw test -pl otel-telemetry-devtools` — 11/11 | ✅ automatizado |
| Loader do dashboard (C22) | `npx vitest run tests/loader-cap.test.ts` — 2/2 | ✅ automatizado |
| Dashboard live/arquivo (C20, C21) | walk playwright (2026-11-11): live 10→11→estável com dedup (3 polls em repouso); `file://` + 2 arquivos → 11 registros, não last-wins | ✅ executado |
| Presets multilíngue (C23, C24) | walk (2026-11-11): `node/demo.mjs` → 10 spans `demo.round` → `/api/traces` + dashboard; README 5 linguagens percorrido (2 ajustes de doc aplicados) | ✅ executado (Node; Python/Go/.NET/Rust por contrato) |
| Exemplos (C25) | `BootstrapSmokeTest` — 1/1 | ✅ automatizado |

Notas honestas:
- o gate formal `check_proofs.py` exige HEAD limpo — impossível sob a política sem commits do owner; os proofs acima são os comandos congelados em `.specs/features/otel-telemetry-java/checks.md`, executados nesta sessão com exit 0.
- endpoints de vendor (dynatrace/grafana) e SDKs não provisionados (Python/Go/.NET/Rust) estão documentados como contrato, não como verificação executada.

Correções desta sessão (2026-11-11): F1 dedup de fronteira no poll live · F2 token Bearer via
prompt em 403 · F3 código morto removido · F4 ingest multi-arquivo sem last-wins · F5 header
com vírgula do builder sobrevive ao `resolve()` · F6 pins vite 6.4.6/vitest 4.1.12 (10 GHSAs
in-scope zerados no prepush) · overlay `[hidden]` fix (bloqueava todos os cliques) · demo
node emitindo spans de verdade · C25 presence-scan anti-flake. Provas completas:
`.specs/features/otel-telemetry-java/verification.md`.
