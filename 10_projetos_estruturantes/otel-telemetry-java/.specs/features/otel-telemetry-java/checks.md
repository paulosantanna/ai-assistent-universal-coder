# otel-telemetry-java checks

Mutations: 3
Build: `mvnw -q verify`; `npm run build` (devtools/dashboard)
Plan: `.specs/features/otel-telemetry-java/plan.md`

## Intent

Ver o plano: `.specs/features/otel-telemetry-java/plan.md`. 27 checks em 7 slices · 3 one-way doors · 1 incerteza aberta (endpoints de vendor), tratada por rotulagem AD-009, nunca por invenção.

## Checks

### S1 - Bootstrap resolve e instala a telemetria

**C1** - `TelemetryBootstrap.start` ativa SDK com `service.name` do builder e endpoint configurado (AC 1)
Proof: `mvnw -q test -pl otel-telemetry-core -Dtest=BootstrapConfigTest`

**C2** - Endpoint malformado ativa SDK no-op com diagnóstico, sem exceção ao app (AC 2)
Proof: `mvnw -q test -pl otel-telemetry-core -Dtest=BootstrapConfigTest#invalidEndpointIsFailSoft`

**C3** - Sem preset configurado, o default é `offline`; sysprop e yaml resolvem abaixo do env (AC 3)
Proof: `mvnw -q test -pl otel-telemetry-core -Dtest=ConfigResolverTest#offlineIsDefaultPreset,syspropOverridesYaml,yamlResolvesFlat`

**C4** - `Telemetry.shutdown()` faz flush do batch dentro do timeout (AC 4)
Proof: `mvnw -q test -pl otel-telemetry-core -Dtest=ShutdownFlushTest`

### S2 - Presets por sinal e segredos

**C5** - Preset `dynatrace`: URL por sinal `{base}/api/v2/otlp/v1/{traces,metrics,logs}` + header `Api-Token` de runtime (AC 5)
Proof: `mvnw -q test -pl otel-telemetry-exporters -Dtest=PresetEndpointTest#dynatracePerSignalUrlsAndHeader`

**C6** - Preset `grafana`: Basic auth no gateway OTLP por sinal (AC 6)
Proof: `mvnw -q test -pl otel-telemetry-exporters -Dtest=PresetEndpointTest#grafanaPerSignalUrlsAndAuth`

**C7** - Presets `splunk`/`otelcol`: OTLP padrão 4317/4318 sem header proprietário (AC 7)
Proof: `mvnw -q test -pl otel-telemetry-exporters -Dtest=PresetEndpointTest#plainOtlpPresets`

**C8** - Credencial ausente → fail-soft; nenhum caso imprime o valor do token (AC 8)
Proof: `mvnw -q test -pl otel-telemetry-core -Dtest=SecretSafetyTest#missingCredentialAndNoSecretInDiagnostics`

### S3 - Logs e métricas do app

**C9** - Record Logback vira log OTLP com severity e trace id quando em span ativo (AC 9)
Proof: `mvnw -q test -pl otel-telemetry-adapters -Dtest=LogbackExportTest`

**C10** - Meter Micrometer vira métrica OTLP pela bridge (AC 10)
Proof: `mvnw -q test -pl otel-telemetry-adapters -Dtest=MicrometerBridgeTest`

### S4 - Spring Boot

**C11** - Starter autoconfigura telemetria de `oteltelemetry.*` no contexto Boot (AC 11)
Proof: `mvnw -q test -pl otel-telemetry-spring-boot-starter -Dtest=StarterAutoConfigTest`

**C12** - Sem Spring no classpath, o starter não carrega beans (condicional) (AC 12)
Proof: `mvnw -q test -pl otel-telemetry-spring-boot-starter -Dtest=StarterAutoConfigTest#inertWithoutSpring`

### S5 - Sink offline

**C13** - `POST /v1/traces` válido → linha JSONL em `traces.jsonl` + 200 (AC 13)
Proof: `mvnw -q test -pl otel-telemetry-devtools -Dtest=SinkOtlpTest#validTracePostAppendsJsonl`

**C14** - `POST` inválido → 400 com causa, arquivo íntegro (AC 14)
Proof: `mvnw -q test -pl otel-telemetry-devtools -Dtest=SinkOtlpTest#invalidPayloadReturns400KeepsFileIntact`

**C15** - Rotação por teto de tamanho/idade com limite de arquivos (AC 15)
Proof: `mvnw -q test -pl otel-telemetry-devtools -Dtest=JsonlStoreTest#rotationHonorsCeilings`

**C16** - Bind default `127.0.0.1:14318`; host/porta/token por config; chamador sem token → 403 (AC 16)
Proof: `mvnw -q test -pl otel-telemetry-devtools -Dtest=SinkConfigTest#loopbackDefaultAndOverrides,missingTokenReturns403`

**C17** - Sink `disabled` → 503 sem gravar (AC 17)
Proof: `mvnw -q test -pl otel-telemetry-devtools -Dtest=SinkConfigTest#disabledReturns503`

**C18** - `/api/traces`|`/api/logs`|`/api/metrics` respondem 200 com dados gravados e 400 em parâmetro inválido (Surface)
Proof: `mvnw -q test -pl otel-telemetry-devtools -Dtest=SinkApiTest#apiRoutesStatuses`

**C19** - `/api/health` responde 200 `{"ok":true}` (Surface)
Proof: `mvnw -q test -pl otel-telemetry-devtools -Dtest=SinkApiTest#healthOk`

**C26** - `POST /v1/metrics` válido → linha JSONL em `metrics.jsonl` + 200 (AC 13)
Proof: `mvnw -q test -pl otel-telemetry-devtools -Dtest=SinkOtlpTest#validMetricPostAppendsJsonl`

**C27** - `POST /v1/logs` válido → linha JSONL em `logs.jsonl` + 200 (AC 13)
Proof: `mvnw -q test -pl otel-telemetry-devtools -Dtest=SinkOtlpTest#validLogPostAppendsJsonl`

### S6 - Dashboard

**C20** - Live: dashboard lista traces/logs/métricas via `/api/*` e desenha métricas em modo delta (AC 18)
Proof: walk - subir sink com dados de exemplo, abrir `http://127.0.0.1:14318/`, conferir as três abas e o gráfico delta

**C21** - Arquivo local: duplo clique no `dist/index.html` + drag-and-drop de JSONL renderiza os mesmos painéis; bundle iife com caminhos relativos (AC 19)
Proof: walk - abrir `dist/index.html` por duplo clique, arrastar `traces.jsonl` gerado pelo sink

**C22** - JSONL enorme carrega janela limitada sem travar (AC 20)
Proof: `npx vitest run tests/loader-cap.test.ts -t capsLoadedWindow` (devtools/dashboard)

### S7 - Presets multilíngue e exemplos

**C23** - App Node/TS oficial apontando `OTEL_EXPORTER_OTLP_ENDPOINT` ao sink aparece no dashboard (AC 21; Python/Go/.NET/Rust pelo mesmo contrato documentado)
Proof: walk - rodar `presets-multilingue/node/demo.mjs` com sink no ar e conferir no `/api/traces`

**C24** - Documento por linguagem existe com contrato `OTEL_*` idêntico (Python, Node, .NET, Go, Rust-experimental) (AC 21)
Proof: walk - abrir `presets-multilingue/README.md` e conferir as 5 seções com env e verificação

**C25** - Exemplos Spring e Java puro emitem telemetria com uma linha de bootstrap (AC 22)
Proof: `mvnw -q test -pl otel-telemetry-examples/otel-telemetry-example-java -Dtest=BootstrapSmokeTest`

## Coverage

| Set (size) | Member -> proof | Unproven |
| --- | --- | --- |
| rotas do sink (10) | `POST /v1/traces` 200 C13 · `POST /v1/traces` 400 C14 · `POST /v1/traces` 503 C17 · `POST /v1/metrics` 200 C26 · `POST /v1/logs` 200 C27 · `POST /v1/*` 403 C16 · `/api/*` 200 C18 · `/api/*` 400 C18 · `/api/*` 403 C16 · `/api/health` 200 C19 | - |
| presets (4) | dynatrace C5 · grafana C6 · splunk/otelcol C7 · offline C13 | - |
| sinais por preset (12) | dynatrace traces C5 · dynatrace metrics C5 · dynatrace logs C5 · grafana traces C6 · grafana metrics C6 · grafana logs C6 · otelcol traces C7 · otelcol metrics C7 · otelcol logs C7 · offline traces C13 · offline metrics C26 · offline logs C27 | - |
| precedência de config (4) | env C1 · sysprop C3 · yaml C3 · builder C1 | - |
| modos do dashboard (2) | live C20 · arquivo local C21 | - |
| linguagens do preset (5) | node C23 · python C24 · dotnet C24 · go C24 · rust C24 | - |
| spring presente/ausente (2) | presente C11 · ausente C12 | - |

## Swept

- validation: C14, C18
- failure modes: C2, C8, C17
- idempotency: n/a - sink é append-only; repetição de payload é aceitável em telemetria
- authorization: C16 (token opcional, loopback default, 403)
- concurrency: C15 (gravação concorrente sob rotação, testada com 2 threads)
- data lifecycle: C15 (rotação+teto), C22 (cap do loader)
- dependency failure: C2/C8 (exporter inacessível → fail-soft no app)
- state transitions: C3 (default offline), C17 (disabled)
- observability: a biblioteca é o sujeito; autodiagnóstico coberto por C2/C8

## Handoff

- (pendente — preenchido pelo builder ao fechar slices)
