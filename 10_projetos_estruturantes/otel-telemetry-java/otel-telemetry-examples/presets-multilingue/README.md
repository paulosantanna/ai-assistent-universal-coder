# Presets multilíngue — contrato `OTEL_*` único

Todos os SDKs oficiais OpenTelemetry falam OTLP. A biblioteca Java e estes apps usam o **mesmo
contrato de variáveis de ambiente**; só muda o pacote por linguagem.

Pré-requisito comum para os walks locais: subir o sink offline (`otel-telemetry-devtools`):

```bash
# a partir de 10_projetos_estruturantes/otel-telemetry-java, com JAVA_HOME apontando para .tools/jdk25
./mvnw -q install -DskipTests -pl otel-telemetry-devtools
./mvnw -q -pl otel-telemetry-devtools dependency:build-classpath -Dmdep.outputFile=target/cp.txt
# classpath = jar + conteúdo de cp.txt (separador ';' no Windows, ':' no Linux)
java -cp "otel-telemetry-devtools/target/otel-telemetry-devtools-1.0.0.jar;otel-telemetry-devtools/target/cp.txt" \
    com.aeos.telemetry.devtools.SinkMain   # no Windows, expanda o cp.txt no -cp (Get-Content -Raw)
# dashboard: http://127.0.0.1:14318/
```

Comando provado nesta máquina (Windows/PowerShell, 2026-11-11): `cp.txt` via
`dependency:build-classpath` + `java -cp "otel-telemetry-devtools\target\classes;<cp.txt>"`.

| Preset da lib Java | Env equivalentes no SDK de cada linguagem |
| --- | --- |
| `offline` | `OTEL_EXPORTER_OTLP_ENDPOINT=http://127.0.0.1:14318` |
| `otelcol` | `OTEL_EXPORTER_OTLP_ENDPOINT=http://<collector>:4318` (http/protobuf) ou `:4317` (grpc) |
| `splunk` | `OTEL_EXPORTER_OTLP_ENDPOINT=<url>` + `OTEL_EXPORTER_OTLP_HEADERS=...` |
| `dynatrace` | `OTEL_EXPORTER_OTLP_ENDPOINT=https://<tenant>.live.dynatrace.com` + `OTEL_DYNATRACE_TOKEN` |
| `grafana` | `OTEL_GRAFANA_INSTANCE=<url>` + `OTEL_GRAFANA_TOKEN` |

> **Status de verificação (2026-11-11):** as rotas de `dynatrace` e `grafana` na biblioteca Java
> estão rotuladas **NÃO VERIFICADO (J1)** — a documentação dos vendors estava inacessível (403/404)
> na data da consulta. Para os SDKs abaixo, use sempre a documentação oficial vigente de cada
> linguagem; o contrato `OTEL_EXPORTER_OTLP_*` é padrão OTel e não depende do vendor.

## Node (verificável — demo incluso)

Arquivo: [`node/demo.mjs`](node/demo.mjs) · runtime provisionado: Node 24 (verificado nesta máquina).

```bash
# rode em um diretório scratch FORA do repositório para não poluir o projeto com
# package.json/node_modules do demo (copie o demo.mjs para lá)
npm init -y
npm i @opentelemetry/sdk-node @opentelemetry/exporter-trace-otlp-proto \
      @opentelemetry/api @opentelemetry/resources @opentelemetry/semantic-conventions
OTEL_EXPORTER_OTLP_ENDPOINT=http://127.0.0.1:14318 node demo.mjs
```

Verificação (walk C23, executada 2026-11-11): com o sink no ar, `node demo.mjs` exportou
10 spans `demo.round` → `traces.jsonl` gravado → `GET /api/traces` retorna os spans →
dashboard em `/` exibe na aba Traces (prova com playwright).

## Python

Runtime NÃO provisionado nesta máquina — contrato documentado (C24). Instale `opentelemetry-sdk`,
`opentelemetry-exporter-otlp-proto-http` e aponte:

```bash
export OTEL_EXPORTER_OTLP_ENDPOINT=http://127.0.0.1:14318
export OTEL_EXPORTER_OTLP_PROTOCOL=http/protobuf
export OTEL_SERVICE_NAME=demo-python
python demo.py   # tracer().start_as_current_span(...) como em demo.mjs
```

## .NET

Runtime NÃO provisionado — contrato documentado (C24). Pacote `OpenTelemetry.Exporter.OpenTelemetryProtocol`:

```bash
export OTEL_EXPORTER_OTLP_ENDPOINT=http://127.0.0.1:14318
export OTEL_SERVICE_NAME=demo-dotnet
# AddOtlpExporter() no builder; endpoint por env ou AddOtlpExporter(o => o.Endpoint = new Uri(env))
```

## Go

Runtime NÃO provisionado — contrato documentado (C24). Pacote `go.opentelemetry.io/otel/exporters/otlp/otlptrace/otlptracehttp`:

```go
exporter, _ := otlptracehttp.New(ctx) // lê OTEL_EXPORTER_OTLP_ENDPOINT do ambiente
```

## Rust (experimental)

Runtime NÃO provisionado; o ecossistema Rust/OTel muda rápido — trate como experimental (C24).
Crates: `opentelemetry`, `opentelemetry-otlp` (feature `http-proto`), `opentelemetry_sdk`:

```rust
// ExporterBuilder::new().with_http().with_endpoint("http://127.0.0.1:14318/v1/traces")
// a API dos crates evolui independentemente do contrato env acima
```

## Verificação

- **C23 (walk)**: `node/demo.mjs` com sink no ar → spans no dashboard (Node provisionado).
- **C24 (walk)**: este README tem as 5 seções com env e modo de verificação.
