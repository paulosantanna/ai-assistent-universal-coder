package com.aeos.telemetry.exporters;

import com.aeos.telemetry.core.ConfigResolver;
import com.aeos.telemetry.core.ResolvedConfig;
import com.aeos.telemetry.core.Signal;
import com.aeos.telemetry.core.TelemetryConfig;
import org.junit.jupiter.api.Test;

import java.util.Map;
import java.util.Properties;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.junit.jupiter.api.Assertions.assertTrue;

/** C5–C7: modelagem de URL/headers por preset. Rotas de dynatrace/grafana são NÃO VERIFICADO J1
 *  (definidas pelo plano; doc do vendor inacessível em 2026-11-11). */
class PresetEndpointTest {

    private ResolvedConfig resolve(Map<String, String> env) {
        return ConfigResolver.resolve(env, new Properties(), null, TelemetryConfig.builder().build());
    }

    @Test
    void dynatraceShapesUrlAndApiTokenHeader() {
        ResolvedConfig config = resolve(Map.of(
                "OTELTELEMETRY_PRESET", "dynatrace",
                "OTEL_DYNATRACE_TOKEN", "DT-TOKEN",
                "OTEL_EXPORTER_OTLP_ENDPOINT", "https://abc123.live.dynatrace.com"));

        ExporterSpec traces = Presets.spec(config, Signal.TRACES);
        assertEquals("https://abc123.live.dynatrace.com/api/v2/otlp/v1/traces", traces.url());
        assertEquals("Api-Token DT-TOKEN", traces.headers().get("Authorization"));

        ExporterSpec metrics = Presets.spec(config, Signal.METRICS);
        assertEquals("https://abc123.live.dynatrace.com/api/v2/otlp/v1/metrics", metrics.url());
        ExporterSpec logs = Presets.spec(config, Signal.LOGS);
        assertEquals("https://abc123.live.dynatrace.com/api/v2/otlp/v1/logs", logs.url());
    }

    @Test
    void grafanaShapesUrlAndBearerHeader() {
        ResolvedConfig config = resolve(Map.of(
                "OTELTELEMETRY_PRESET", "grafana",
                "OTEL_GRAFANA_INSTANCE", "https://gateway.example.grafana.net/otlp",
                "OTEL_GRAFANA_TOKEN", "GF-TOKEN"));

        ExporterSpec traces = Presets.spec(config, Signal.TRACES);
        assertEquals("https://gateway.example.grafana.net/otlp/v1/traces", traces.url());
        assertEquals("Bearer https://gateway.example.grafana.net/otlp:GF-TOKEN",
                traces.headers().get("Authorization"));
    }

    @Test
    void offlineDefaultsToLocalSink() {
        ResolvedConfig config = resolve(Map.of());
        assertEquals("http://127.0.0.1:14318/v1/traces", Presets.spec(config, Signal.TRACES).url());
        assertEquals("http://127.0.0.1:14318/v1/metrics", Presets.spec(config, Signal.METRICS).url());
        assertEquals("http://127.0.0.1:14318/v1/logs", Presets.spec(config, Signal.LOGS).url());
    }

    @Test
    void otelcolDefaultsHttp4318AndGrpc4317() {
        ResolvedConfig http = resolve(Map.of("OTELTELEMETRY_PRESET", "otelcol"));
        assertEquals("http://localhost:4318/v1/traces", Presets.spec(http, Signal.TRACES).url());

        ResolvedConfig grpc = ConfigResolver.resolve(Map.of("OTELTELEMETRY_PRESET", "otelcol"),
                new Properties(), null,
                TelemetryConfig.builder().protocol("grpc").build());
        assertEquals("http://localhost:4317/v1/traces", Presets.spec(grpc, Signal.TRACES).url());
    }

    @Test
    void splunkUsesGenericOtlpShape() {
        ResolvedConfig config = resolve(Map.of("OTELTELEMETRY_PRESET", "splunk"));
        assertEquals("http://localhost:4318/v1/traces", Presets.spec(config, Signal.TRACES).url());
    }

    @Test
    void perSignalEndpointOverrideUsedVerbatim() {
        ResolvedConfig config = resolve(Map.of(
                "OTEL_EXPORTER_OTLP_TRACES_ENDPOINT", "http://custom-collector:9999/abc",
                "OTEL_EXPORTER_OTLP_ENDPOINT", "http://base:4318"));
        assertEquals("http://custom-collector:9999/abc", Presets.spec(config, Signal.TRACES).url());
        // sinal sem override segue o shape do preset sobre o endpoint base
        assertEquals("http://base:4318/v1/metrics", Presets.spec(config, Signal.METRICS).url());
    }

    @Test
    void userHeadersMergeOverPreset() {
        ResolvedConfig config = resolve(Map.of(
                "OTELTELEMETRY_PRESET", "dynatrace",
                "OTEL_DYNATRACE_TOKEN", "DT-TOKEN",
                "OTEL_EXPORTER_OTLP_ENDPOINT", "https://abc123.live.dynatrace.com",
                "OTEL_EXPORTER_OTLP_TRACES_HEADERS", "X-Tenant=minha-tenant"));
        Map<String, String> headers = Presets.spec(config, Signal.TRACES).headers();
        assertEquals("Api-Token DT-TOKEN", headers.get("Authorization"));
        assertEquals("minha-tenant", headers.get("X-Tenant"));
    }

    @Test
    void dynatraceWithoutBaseFailsSoftly() {
        ResolvedConfig config = resolve(Map.of(
                "OTELTELEMETRY_PRESET", "dynatrace",
                "OTEL_DYNATRACE_TOKEN", "DT-TOKEN"));
        IllegalArgumentException error = assertThrows(IllegalArgumentException.class,
                () -> Presets.spec(config, Signal.TRACES));
        assertTrue(error.getMessage().contains("OTEL_EXPORTER_OTLP_ENDPOINT"));
    }

    @Test
    void dynatraceWithGrpcFailsSoftly() {
        ResolvedConfig config = ConfigResolver.resolve(
                Map.of("OTELTELEMETRY_PRESET", "dynatrace", "OTEL_DYNATRACE_TOKEN", "DT-TOKEN"),
                new Properties(), null,
                TelemetryConfig.builder().protocol("grpc").build());
        assertThrows(IllegalArgumentException.class, () -> Presets.spec(config, Signal.TRACES));
    }

    @Test
    void grafanaWithoutInstanceFailsSoftly() {
        ResolvedConfig config = resolve(Map.of(
                "OTELTELEMETRY_PRESET", "grafana",
                "OTEL_GRAFANA_TOKEN", "GF-TOKEN"));
        assertThrows(IllegalArgumentException.class, () -> Presets.spec(config, Signal.TRACES));
    }
}
