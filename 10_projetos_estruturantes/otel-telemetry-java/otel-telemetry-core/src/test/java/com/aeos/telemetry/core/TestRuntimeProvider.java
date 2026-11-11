package com.aeos.telemetry.core;

import io.opentelemetry.api.OpenTelemetry;
import io.opentelemetry.api.common.AttributeKey;
import io.opentelemetry.sdk.OpenTelemetrySdk;
import io.opentelemetry.sdk.logs.SdkLoggerProvider;
import io.opentelemetry.sdk.resources.Resource;
import io.opentelemetry.sdk.trace.SdkTracerProvider;
import io.opentelemetry.sdk.trace.export.BatchSpanProcessor;

import java.util.concurrent.TimeUnit;

/** Provider de teste (registrado em META-INF/services): SDK in-memory que captura a config recebida. */
public final class TestRuntimeProvider implements TelemetryRuntimeProvider {

    public static volatile ResolvedConfig lastConfig;
    public static volatile RecordingSpanExporter lastSpanExporter;

    @Override
    public TelemetryRuntime create(ResolvedConfig config) {
        lastConfig = config;
        RecordingSpanExporter spanExporter = RecordingSpanExporter.create();
        lastSpanExporter = spanExporter;

        Resource resource = Resource.getDefault().merge(Resource.builder()
                .put(AttributeKey.stringKey("service.name"), config.serviceName())
                .build());
        SdkTracerProvider tracerProvider = SdkTracerProvider.builder()
                .setResource(resource)
                .addSpanProcessor(BatchSpanProcessor.builder(spanExporter).build())
                .build();
        SdkLoggerProvider loggerProvider = SdkLoggerProvider.builder()
                .setResource(resource)
                .build();

        OpenTelemetrySdk sdk = OpenTelemetrySdk.builder()
                .setTracerProvider(tracerProvider)
                .setLoggerProvider(loggerProvider)
                .build();

        return new TelemetryRuntime() {
            @Override
            public OpenTelemetry openTelemetry() {
                return sdk;
            }

            @Override
            public void shutdown() {
                // flush ANTES do shutdown: entrega o batch pendente e só então desliga o pipeline.
                tracerProvider.forceFlush().join(2, TimeUnit.SECONDS);
                tracerProvider.shutdown();
                loggerProvider.shutdown();
            }
        };
    }
}
