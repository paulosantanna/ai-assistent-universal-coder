package com.aeos.telemetry.adapters;

import ch.qos.logback.classic.Logger;
import io.opentelemetry.api.common.AttributeKey;
import io.opentelemetry.api.logs.Severity;
import io.opentelemetry.api.trace.Span;
import io.opentelemetry.sdk.OpenTelemetrySdk;
import io.opentelemetry.sdk.logs.SdkLoggerProvider;
import io.opentelemetry.sdk.logs.data.LogRecordData;
import io.opentelemetry.sdk.logs.export.SimpleLogRecordProcessor;
import io.opentelemetry.sdk.resources.Resource;
import io.opentelemetry.sdk.testing.exporter.InMemoryLogRecordExporter;
import io.opentelemetry.sdk.testing.exporter.InMemorySpanExporter;
import io.opentelemetry.sdk.trace.SdkTracerProvider;
import io.opentelemetry.sdk.trace.export.SimpleSpanProcessor;
import org.junit.jupiter.api.Test;
import org.slf4j.LoggerFactory;

import java.util.List;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertNotNull;

/** C9: evento Logback vira LogRecord com severity, corpo, atributos e contexto de span. */
class LogbackExportTest {

    @Test
    void logRecordCarriesSeverityBodyAndSpanContext() {
        InMemoryLogRecordExporter logExporter = InMemoryLogRecordExporter.create();
        InMemorySpanExporter spanExporter = InMemorySpanExporter.create();
        Resource resource = Resource.getDefault().merge(Resource.builder()
                .put(AttributeKey.stringKey("service.name"), "adapter-svc")
                .build());
        SdkLoggerProvider loggerProvider = SdkLoggerProvider.builder()
                .setResource(resource)
                .addLogRecordProcessor(SimpleLogRecordProcessor.create(logExporter))
                .build();
        SdkTracerProvider tracerProvider = SdkTracerProvider.builder()
                .setResource(resource)
                .addSpanProcessor(SimpleSpanProcessor.create(spanExporter))
                .build();
        OpenTelemetrySdk sdk = OpenTelemetrySdk.builder()
                .setTracerProvider(tracerProvider)
                .setLoggerProvider(loggerProvider)
                .build();

        Adapters.installLogbackAppender(sdk);

        Span caller = sdk.getTracer("test").spanBuilder("caller-span").startSpan();
        try (var ignored = caller.makeCurrent()) {
            Logger logger = (Logger) LoggerFactory.getLogger("adapter.test");
            logger.atInfo().addKeyValue("area", "pagamento").log("pedido processado");
        } finally {
            caller.end();
        }

        List<LogRecordData> records = logExporter.getFinishedLogRecordItems();
        assertEquals(1, records.size());
        LogRecordData record = records.get(0);
        assertEquals("pedido processado", record.getBodyValue().asString());
        assertEquals(Severity.INFO, record.getSeverity());
        assertEquals("INFO", record.getSeverityText());
        assertEquals(caller.getSpanContext().getTraceId(), record.getSpanContext().getTraceId());
        assertEquals(caller.getSpanContext().getSpanId(), record.getSpanContext().getSpanId());
        assertEquals("pagamento", record.getAttributes().get(AttributeKey.stringKey("area")));

        assertEquals(1, spanExporter.getFinishedSpanItems().size());
        assertNotNull(sdk);
    }
}
