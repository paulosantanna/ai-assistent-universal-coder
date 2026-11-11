package com.aeos.telemetry.core;

import org.junit.jupiter.api.Test;

import java.util.List;
import java.util.Map;
import java.util.Properties;

import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertTrue;

/** C8: credencial ausente é fail-soft e nenhum diagnóstico contém o valor do segredo. */
class SecretSafetyTest {

    private static final String TOKEN = "SUPERSECRETTOKEN123";

    @Test
    void missingCredentialIsFailSoft() {
        ResolvedConfig config = ConfigResolver.resolve(Map.of("OTELTELEMETRY_PRESET", "dynatrace"),
                new Properties(), null, TelemetryConfig.builder().build());
        Telemetry telemetry = TelemetryBootstrap.install(config);
        try {
            assertTrue(telemetry.noop());
            assertTrue(telemetry.diagnostics().stream().anyMatch(d -> d.contains("credencial ausente")));
            assertTrue(telemetry.diagnostics().stream().anyMatch(d -> d.contains("OTEL_DYNATRACE_TOKEN")));
        } finally {
            telemetry.shutdown();
        }
    }

    @Test
    void noSecretInDiagnostics() {
        TestRuntimeProvider.lastConfig = null;
        Map<String, String> env = Map.of(
                "OTELTELEMETRY_PRESET", "dynatrace",
                "OTEL_DYNATRACE_TOKEN", TOKEN,
                "OTEL_EXPORTER_OTLP_ENDPOINT", "ht!tp://bad");
        ResolvedConfig config = ConfigResolver.resolve(env, new Properties(), null, TelemetryConfig.builder().build());
        assertTrue(config.credentialPresent());

        Telemetry telemetry = TelemetryBootstrap.install(config);
        try {
            assertTrue(telemetry.noop());
            List<String> diagnostics = telemetry.diagnostics();
            assertTrue(diagnostics.stream().anyMatch(d -> d.contains("inválido")));
            for (String diagnostic : diagnostics) {
                assertFalse(diagnostic.contains(TOKEN), "diagnóstico não deve conter o valor do token");
            }
        } finally {
            telemetry.shutdown();
        }
    }

    @Test
    void resolvedConfigToStringOmitsCredentials() {
        ResolvedConfig config = ConfigResolver.resolve(
                Map.of("OTELTELEMETRY_PRESET", "dynatrace", "OTEL_DYNATRACE_TOKEN", TOKEN),
                new Properties(), null, TelemetryConfig.builder().build());
        assertFalse(config.toString().contains(TOKEN));
        assertTrue(config.toString().contains("credentialPresent=true"));
    }
}
