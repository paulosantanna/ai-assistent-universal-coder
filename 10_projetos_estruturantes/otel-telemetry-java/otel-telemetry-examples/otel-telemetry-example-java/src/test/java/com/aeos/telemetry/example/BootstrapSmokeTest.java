package com.aeos.telemetry.example;

import com.aeos.telemetry.core.Telemetry;
import com.aeos.telemetry.core.TelemetryBootstrap;
import com.sun.net.httpserver.HttpExchange;
import com.sun.net.httpserver.HttpServer;
import io.opentelemetry.proto.collector.logs.v1.ExportLogsServiceRequest;
import io.opentelemetry.proto.collector.metrics.v1.ExportMetricsServiceRequest;
import io.opentelemetry.proto.collector.trace.v1.ExportTraceServiceRequest;
import org.junit.jupiter.api.Test;

import java.io.IOException;
import java.io.OutputStream;
import java.net.InetSocketAddress;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.atomic.AtomicReference;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;

/** C25: exemplos emitem telemetria com uma linha de bootstrap.
 *  Stub OTLP local (JDK HttpServer) captura os protobufs exportados; o assert roda
 *  APÓS telemetry.shutdown(), que faz o flush (AD-006) e entrega os lotes pendentes. */
class BootstrapSmokeTest {

    @Test
    void oneLineBootstrapExportsTracesMetricsAndLogs() throws Exception {
        AtomicReference<byte[]> traceBody = new AtomicReference<>();
        AtomicReference<byte[]> metricBody = new AtomicReference<>();
        AtomicReference<byte[]> logBody = new AtomicReference<>();

        HttpServer stub = HttpServer.create(new InetSocketAddress("127.0.0.1", 0), 0);
        ExecutorService executor = Executors.newSingleThreadExecutor();
        stub.createContext("/v1/traces", exchange -> capture(exchange, traceBody));
        stub.createContext("/v1/metrics", exchange -> capture(exchange, metricBody));
        stub.createContext("/v1/logs", exchange -> capture(exchange, logBody));
        stub.setExecutor(executor);
        stub.start();
        try {
            int port = stub.getAddress().getPort();

            // >>> a linha de bootstrap do exemplo (Main): serviceName + endpoint via builder
            Telemetry telemetry = TelemetryBootstrap.start(builder -> builder
                    .serviceName("smoke-svc")
                    .endpoint("http://127.0.0.1:" + port));

            telemetry.openTelemetry().getTracer("smoke").spanBuilder("smoke-span").startSpan().end();
            telemetry.openTelemetry().getMeter("smoke")
                    .counterBuilder("smoke.counter").ofDoubles().build().add(2);
            telemetry.openTelemetry().getLogsBridge().get("smoke")
                    .logRecordBuilder()
                    .setBody("smoke log")
                    .setSeverityText("INFO")
                    .emit();

            // shutdown → forceFlush de cada pipeline → export chega ao stub
            telemetry.shutdown();

            assertTrue(traceBody.get() != null && traceBody.get().length > 0, "traces exportados");
            assertTrue(metricBody.get() != null && metricBody.get().length > 0, "metrics exportados");
            assertTrue(logBody.get() != null && logBody.get().length > 0, "logs exportados");

            ExportTraceServiceRequest traces = ExportTraceServiceRequest.parseFrom(traceBody.get());
            assertEquals("smoke-span",
                    traces.getResourceSpans(0).getScopeSpans(0).getSpans(0).getName());

            ExportMetricsServiceRequest metrics = ExportMetricsServiceRequest.parseFrom(metricBody.get());
            // o SDK pode acrescentar auto-observabilidade (otel.sdk.*) ao lote de shutdown —
            // o contrato do app é smoke.counter ESTAR presente, não ser o primeiro item
            boolean smokeCounterExported = false;
            for (int rm = 0; rm < metrics.getResourceMetricsCount() && !smokeCounterExported; rm++) {
                for (int sm = 0; sm < metrics.getResourceMetrics(rm).getScopeMetricsCount() && !smokeCounterExported; sm++) {
                    for (int m = 0; m < metrics.getResourceMetrics(rm).getScopeMetrics(sm).getMetricsCount(); m++) {
                        if ("smoke.counter".equals(
                                metrics.getResourceMetrics(rm).getScopeMetrics(sm).getMetrics(m).getName())) {
                            smokeCounterExported = true;
                            break;
                        }
                    }
                }
            }
            assertTrue(smokeCounterExported, "smoke.counter exportado");

            ExportLogsServiceRequest logs = ExportLogsServiceRequest.parseFrom(logBody.get());
            assertEquals("smoke log",
                    logs.getResourceLogs(0).getScopeLogs(0).getLogRecords(0).getBody().getStringValue());
        } finally {
            stub.stop(0);
            executor.shutdownNow();
        }
    }

    private static void capture(HttpExchange exchange, AtomicReference<byte[]> target) throws IOException {
        try {
            byte[] body = exchange.getRequestBody().readAllBytes();
            target.set(body);
            exchange.getResponseHeaders().set("Content-Type", "application/x-protobuf");
            exchange.sendResponseHeaders(200, 0);
            try (OutputStream out = exchange.getResponseBody()) {
                out.flush();
            }
        } finally {
            exchange.close();
        }
    }
}
