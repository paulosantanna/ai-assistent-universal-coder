package com.aeos.telemetry.core;

import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertNotNull;
import static org.junit.jupiter.api.Assertions.assertTrue;

/** C1 e C2: bootstrap de uma linha instala a telemetria; endpoint malformado é fail-soft. */
class BootstrapConfigTest {

    @Test
    void startInstallsSdkWithServiceNameAndEndpoint() {
        TestRuntimeProvider.lastConfig = null;
        Telemetry telemetry = TelemetryBootstrap.start(builder -> builder
                .serviceName("svc-demo")
                .preset("otelcol")
                .endpoint("http://127.0.0.1:4318"));
        try {
            assertFalse(telemetry.noop());
            ResolvedConfig config = TestRuntimeProvider.lastConfig;
            assertNotNull(config);
            assertEquals("svc-demo", config.serviceName());
            assertEquals(Preset.OTELCOL, config.preset());
            assertEquals("http://127.0.0.1:4318", config.baseEndpoint());
            assertNotNull(telemetry.openTelemetry());
            assertNotNull(telemetry.openTelemetry().getTracer("test"));
        } finally {
            telemetry.shutdown();
        }
    }

    @Test
    void invalidEndpointIsFailSoft() {
        Telemetry telemetry = TelemetryBootstrap.start(builder -> builder
                .serviceName("svc-broken")
                .endpoint("ht!tp://bad"));
        try {
            assertTrue(telemetry.noop());
            assertTrue(telemetry.diagnostics().stream().anyMatch(d -> d.contains("endpoint base inválido")));
        } finally {
            telemetry.shutdown();
        }
    }
}
