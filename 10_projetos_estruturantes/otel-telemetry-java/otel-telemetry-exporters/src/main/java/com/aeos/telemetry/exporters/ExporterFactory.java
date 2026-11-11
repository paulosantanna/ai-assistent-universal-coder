package com.aeos.telemetry.exporters;

import com.aeos.telemetry.core.ResolvedConfig;
import io.opentelemetry.exporter.otlp.http.logs.OtlpHttpLogRecordExporter;
import io.opentelemetry.exporter.otlp.http.metrics.OtlpHttpMetricExporter;
import io.opentelemetry.exporter.otlp.http.trace.OtlpHttpSpanExporter;
import io.opentelemetry.exporter.otlp.logs.OtlpGrpcLogRecordExporter;
import io.opentelemetry.exporter.otlp.metrics.OtlpGrpcMetricExporter;
import io.opentelemetry.exporter.otlp.trace.OtlpGrpcSpanExporter;
import io.opentelemetry.sdk.logs.export.LogRecordExporter;
import io.opentelemetry.sdk.metrics.export.MetricExporter;
import io.opentelemetry.sdk.trace.export.SpanExporter;

import java.util.Map;

/** Cria exporters OTLP (http/protobuf ou grpc) a partir da especificação de preset.
 *  Pacotes verificados no jar opentelemetry-exporter-otlp 1.68.0: grpc em otlp.{trace,metrics,logs}
 *  e http em olp.http.{trace,metrics,logs}; setHeaders recebe Supplier de Map. */
final class ExporterFactory {

    private ExporterFactory() {
    }

    static SpanExporter spanExporter(ResolvedConfig config, ExporterSpec spec) {
        Map<String, String> headers = spec.headers();
        if (config.protocol() == ResolvedConfig.Protocol.GRPC) {
            return OtlpGrpcSpanExporter.builder()
                    .setEndpoint(spec.url())
                    .setHeaders(() -> headers)
                    .build();
        }
        return OtlpHttpSpanExporter.builder()
                .setEndpoint(spec.url())
                .setHeaders(() -> headers)
                .build();
    }

    static MetricExporter metricExporter(ResolvedConfig config, ExporterSpec spec) {
        Map<String, String> headers = spec.headers();
        if (config.protocol() == ResolvedConfig.Protocol.GRPC) {
            return OtlpGrpcMetricExporter.builder()
                    .setEndpoint(spec.url())
                    .setHeaders(() -> headers)
                    .build();
        }
        return OtlpHttpMetricExporter.builder()
                .setEndpoint(spec.url())
                .setHeaders(() -> headers)
                .build();
    }

    static LogRecordExporter logRecordExporter(ResolvedConfig config, ExporterSpec spec) {
        Map<String, String> headers = spec.headers();
        if (config.protocol() == ResolvedConfig.Protocol.GRPC) {
            return OtlpGrpcLogRecordExporter.builder()
                    .setEndpoint(spec.url())
                    .setHeaders(() -> headers)
                    .build();
        }
        return OtlpHttpLogRecordExporter.builder()
                .setEndpoint(spec.url())
                .setHeaders(() -> headers)
                .build();
    }
}
