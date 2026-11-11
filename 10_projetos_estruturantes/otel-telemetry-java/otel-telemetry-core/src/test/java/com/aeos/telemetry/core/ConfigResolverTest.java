package com.aeos.telemetry.core;

import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.io.TempDir;

import java.nio.file.Files;
import java.nio.file.Path;
import java.util.Map;
import java.util.Properties;

import static org.junit.jupiter.api.Assertions.assertEquals;

/** C3: default offline; camadas env &gt; sysprop &gt; yaml; yaml de chaves planas. */
class ConfigResolverTest {

    @Test
    void offlineIsDefaultPreset() {
        ResolvedConfig config = ConfigResolver.resolve(Map.of(), new Properties(), null,
                TelemetryConfig.builder().build());
        assertEquals(Preset.OFFLINE, config.preset());
        assertEquals("unknown_service", config.serviceName());
        assertEquals(ResolvedConfig.Protocol.HTTP_PROTOBUF, config.protocol());
    }

    @Test
    void syspropOverridesYaml(@TempDir Path tempDir) throws Exception {
        Path yaml = tempDir.resolve("oteltelemetry.yaml");
        Files.writeString(yaml, "preset: dynatrace\nexporter.otlp.endpoint: http://yaml-host:4318\n");
        Properties sysprops = new Properties();
        sysprops.setProperty("oteltelemetry.preset", "grafana");

        ResolvedConfig config = ConfigResolver.resolve(Map.of(), sysprops, yaml, TelemetryConfig.builder().build());
        assertEquals(Preset.GRAFANA, config.preset());
        assertEquals("http://yaml-host:4318", config.baseEndpoint());
    }

    @Test
    void yamlResolvesFlat(@TempDir Path tempDir) throws Exception {
        Path yaml = tempDir.resolve("oteltelemetry.yaml");
        Files.writeString(yaml, "service.name: yaml-svc\nexporter.otlp.traces.endpoint: http://yaml-traces:4318\n");

        ResolvedConfig config = ConfigResolver.resolve(Map.of(), new Properties(), yaml,
                TelemetryConfig.builder().build());
        assertEquals("yaml-svc", config.serviceName());
        assertEquals("http://yaml-traces:4318", config.signalEndpoint(Signal.TRACES));
    }

    @Test
    void envOverridesSysprop() {
        Properties sysprops = new Properties();
        sysprops.setProperty("otel.service.name", "prop-svc");

        ResolvedConfig config = ConfigResolver.resolve(Map.of("OTEL_SERVICE_NAME", "env-svc"), sysprops, null,
                TelemetryConfig.builder().build());
        assertEquals("env-svc", config.serviceName());
    }

    @Test
    void builderHeaderValueWithCommaSurvives() {
        // round-trip por string (k=v,k=v) truncava em ',' — o header do builder fica como Map
        ResolvedConfig config = ConfigResolver.resolve(Map.of(), new Properties(), null,
                TelemetryConfig.builder()
                        .header(Signal.TRACES, "x-tag", "a,b")
                        .build());
        assertEquals("a,b", config.headers(Signal.TRACES).get("x-tag"));
    }
}
