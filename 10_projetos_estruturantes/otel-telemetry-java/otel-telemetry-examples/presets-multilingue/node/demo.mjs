// Demo Node oficial do preset multilíngue (C23): usa o SDK OTel JS apontando para o sink.
//
// Uso:
//   1. suba o sink:      java -cp ... com.aeos.telemetry.devtools.SinkMain
//   2. npm i @opentelemetry/sdk-node @opentelemetry/exporter-trace-otlp-proto \
//        @opentelemetry/resources @opentelemetry/semantic-conventions
//   3. OTEL_EXPORTER_OTLP_ENDPOINT=http://127.0.0.1:14318 node demo.mjs
//
// O contrato de env é o mesmo da biblioteca Java: OTEL_EXPORTER_OTLP_ENDPOINT (+headers
// por OTEL_EXPORTER_OTLP_HEADERS=chave=valor,chave2=valor2). O sink grava traces.jsonl
// e o dashboard (http://127.0.0.1:14318/) mostra os spans do demo.

import { trace } from '@opentelemetry/api';
import { NodeSDK } from '@opentelemetry/sdk-node';
import { OTLPTraceExporter } from '@opentelemetry/exporter-trace-otlp-proto';
import { resourceFromAttributes } from '@opentelemetry/resources';
import { ATTR_SERVICE_NAME } from '@opentelemetry/semantic-conventions';

const endpoint = process.env.OTEL_EXPORTER_OTLP_ENDPOINT ?? 'http://127.0.0.1:14318';

const sdk = new NodeSDK({
  resource: resourceFromAttributes({ [ATTR_SERVICE_NAME]: 'demo-node' }),
  traceExporter: new OTLPTraceExporter({ url: `${endpoint}/v1/traces` }),
});

sdk.start();

const tracer = trace.getTracer('demo-node');
const sleep = (ms) => new Promise((resolve) => setTimeout(resolve, ms));

// cada rodada é um span real: sem span não há export (BatchSpanProcessor vazio não envia nada)
async function round(i) {
  const span = tracer.startSpan('demo.round');
  span.setAttribute('demo.round', i);
  await sleep(20 + Math.floor(Math.random() * 50));
  console.log(`[demo-node] rodada ${i} emitida`);
  span.end();
}

for (let i = 1; i <= 10; i++) {
  await round(i);
}

await sdk.shutdown();
console.log('[demo-node] pronto; confira http://127.0.0.1:14318/ no dashboard');
