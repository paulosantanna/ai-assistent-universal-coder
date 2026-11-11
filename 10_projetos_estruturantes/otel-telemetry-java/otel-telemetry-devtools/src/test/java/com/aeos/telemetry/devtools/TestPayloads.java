package com.aeos.telemetry.devtools;

import com.google.protobuf.ByteString;
import io.opentelemetry.proto.collector.logs.v1.ExportLogsServiceRequest;
import io.opentelemetry.proto.collector.metrics.v1.ExportMetricsServiceRequest;
import io.opentelemetry.proto.collector.trace.v1.ExportTraceServiceRequest;
import io.opentelemetry.proto.common.v1.AnyValue;
import io.opentelemetry.proto.logs.v1.LogRecord;
import io.opentelemetry.proto.logs.v1.ResourceLogs;
import io.opentelemetry.proto.logs.v1.ScopeLogs;
import io.opentelemetry.proto.logs.v1.SeverityNumber;
import io.opentelemetry.proto.metrics.v1.Gauge;
import io.opentelemetry.proto.metrics.v1.Metric;
import io.opentelemetry.proto.metrics.v1.NumberDataPoint;
import io.opentelemetry.proto.metrics.v1.ResourceMetrics;
import io.opentelemetry.proto.metrics.v1.ScopeMetrics;
import io.opentelemetry.proto.trace.v1.ResourceSpans;
import io.opentelemetry.proto.trace.v1.ScopeSpans;
import io.opentelemetry.proto.trace.v1.Span;

/** Payloads OTLP protobuf válidos para os testes do sink (ids byte16/byte8 e tempo fixo em ns). */
public final class TestPayloads {

    public static final long TIME_NS = 1_700_000_000_000_000_000L; // 2023-11-14T22:13:20Z
    public static final long TIME_MS = TIME_NS / 1_000_000L;

    private TestPayloads() {
    }

    public static byte[] traceProtobuf(String spanName) {
        Span span = Span.newBuilder()
                .setTraceId(ByteString.copyFrom(new byte[]{1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16}))
                .setSpanId(ByteString.copyFrom(new byte[]{21, 22, 23, 24, 25, 26, 27, 28}))
                .setName(spanName)
                .setStartTimeUnixNano(TIME_NS)
                .setEndTimeUnixNano(TIME_NS + 5_000_000L)
                .setKind(Span.SpanKind.SPAN_KIND_SERVER)
                .build();
        return ExportTraceServiceRequest.newBuilder()
                .addResourceSpans(ResourceSpans.newBuilder()
                        .addScopeSpans(ScopeSpans.newBuilder().addSpans(span)))
                .build()
                .toByteArray();
    }

    public static byte[] metricProtobuf(String metricName) {
        NumberDataPoint point = NumberDataPoint.newBuilder()
                .setTimeUnixNano(TIME_NS)
                .setAsDouble(42.5)
                .build();
        Metric metric = Metric.newBuilder()
                .setName(metricName)
                .setGauge(Gauge.newBuilder().addDataPoints(point))
                .build();
        return ExportMetricsServiceRequest.newBuilder()
                .addResourceMetrics(ResourceMetrics.newBuilder()
                        .addScopeMetrics(ScopeMetrics.newBuilder().addMetrics(metric)))
                .build()
                .toByteArray();
    }

    public static byte[] logProtobuf(String message) {
        LogRecord record = LogRecord.newBuilder()
                .setTimeUnixNano(TIME_NS)
                .setSeverityText("INFO")
                .setSeverityNumber(SeverityNumber.SEVERITY_NUMBER_INFO)
                .setBody(AnyValue.newBuilder().setStringValue(message))
                .build();
        return ExportLogsServiceRequest.newBuilder()
                .addResourceLogs(ResourceLogs.newBuilder()
                        .addScopeLogs(ScopeLogs.newBuilder().addLogRecords(record)))
                .build()
                .toByteArray();
    }
}
