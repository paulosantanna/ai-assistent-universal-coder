package com.aeos.telemetry.exporters;

import com.aeos.telemetry.core.ResolvedConfig;
import com.aeos.telemetry.core.Signal;
import com.aeos.telemetry.core.TelemetryRuntime;
import com.aeos.telemetry.core.TelemetryRuntimeProvider;
import io.opentelemetry.api.OpenTelemetry;
import io.opentelemetry.api.common.AttributeKey;
import io.opentelemetry.sdk.OpenTelemetrySdk;
import io.opentelemetry.sdk.logs.SdkLoggerProvider;
import io.opentelemetry.sdk.logs.export.BatchLogRecordProcessor;
import io.opentelemetry.sdk.logs.export.LogRecordExporter;
import io.opentelemetry.sdk.metrics.SdkMeterProvider;
import io.opentelemetry.sdk.metrics.export.MetricExporter;
import io.opentelemetry.sdk.metrics.export.PeriodicMetricReader;
import io.opentelemetry.sdk.resources.Resource;
import io.opentelemetry.sdk.trace.SdkTracerProvider;
import io.opentelemetry.sdk.trace.export.BatchSpanProcessor;
import io.opentelemetry.sdk.trace.export.SpanExporter;

import java.util.concurrent.TimeUnit;

/** Implementação SPI instalada por este módulo: monta o SDK OTel completo (traces/metrics/logs)
 *  com exporters OTLP conformes ao preset. Exceções propagam e o bootstrap ativa no-op (AD-006). */
public final class OtlpRuntimeProvider implements TelemetryRuntimeProvider {

    @Override
    public TelemetryRuntime create(ResolvedConfig config) {
        Resource resource = Resource.getDefault().merge(Resource.builder()
                .put(AttributeKey.stringKey("service.name"), config.serviceName())
                .build());

        SpanExporter spanExporter = ExporterFactory.spanExporter(config, Presets.spec(config, Signal.TRACES));
        SdkTracerProvider tracerProvider = SdkTracerProvider.builder()
                .setResource(resource)
                .addSpanProcessor(BatchSpanProcessor.builder(spanExporter).build())
                .build();

        MetricExporter metricExporter = ExporterFactory.metricExporter(config, Presets.spec(config, Signal.METRICS));
        SdkMeterProvider meterProvider = SdkMeterProvider.builder()
                .setResource(resource)
                .registerMetricReader(PeriodicMetricReader.builder(metricExporter).build())
                .build();

        LogRecordExporter logRecordExporter = ExporterFactory.logRecordExporter(config,
                Presets.spec(config, Signal.LOGS));
        SdkLoggerProvider loggerProvider = SdkLoggerProvider.builder()
                .setResource(resource)
                .addLogRecordProcessor(BatchLogRecordProcessor.builder(logRecordExporter).build())
                .build();

        OpenTelemetrySdk sdk = OpenTelemetrySdk.builder()
                .setTracerProvider(tracerProvider)
                .setMeterProvider(meterProvider)
                .setLoggerProvider(loggerProvider)
                .build();

        return new TelemetryRuntime() {
            @Override
            public OpenTelemetry openTelemetry() {
                return sdk;
            }

            @Override
            public void shutdown() {
                // flush ANTES de shutdown de cada pipeline; teto total é vigiado por Telemetry.shutdown()
                tracerProvider.forceFlush().join(2, TimeUnit.SECONDS);
                meterProvider.forceFlush().join(2, TimeUnit.SECONDS);
                loggerProvider.forceFlush().join(2, TimeUnit.SECONDS);
                tracerProvider.shutdown();
                meterProvider.shutdown();
                loggerProvider.shutdown();
            }
        };
    }
}
