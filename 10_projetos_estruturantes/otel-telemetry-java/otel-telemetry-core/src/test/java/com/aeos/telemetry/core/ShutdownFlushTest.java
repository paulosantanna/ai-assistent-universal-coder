package com.aeos.telemetry.core;

import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertNotNull;
import static org.junit.jupiter.api.Assertions.assertTrue;

/** C4: shutdown faz flush do batch pendente dentro do teto de 5 s (AD-006).
 *  O exporter de gravação preserva os dados após o shutdown, ao contrário do
 *  InMemorySpanExporter, que limpa a lista em shutdown() por design upstream. */
class ShutdownFlushTest {

    @Test
    void shutdownFlushesPendingSpan() {
        TestRuntimeProvider.lastSpanExporter = null;
        Telemetry telemetry = TelemetryBootstrap.start(builder -> builder.serviceName("flush-svc"));
        try {
            assertFalse(telemetry.noop());
            RecordingSpanExporter exporter = TestRuntimeProvider.lastSpanExporter;
            assertNotNull(exporter);

            telemetry.tracer("test").spanBuilder("pending-span").startSpan().end();

            // O span está apenas na fila do BatchSpanProcessor (agendamento default de 5 s):
            // ainda nada entregue ao exporter antes do shutdown.
            assertEquals(0, exporter.getFinishedSpanItems().size());
        } finally {
            telemetry.shutdown();
        }
        // O flush executado no shutdown entregou o span pendente, e ele permanece gravado.
        assertTrue(TestRuntimeProvider.lastSpanExporter.getFinishedSpanItems().stream()
                .anyMatch(span -> "pending-span".equals(span.getName())));
    }
}
