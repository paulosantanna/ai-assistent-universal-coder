package com.aeos.telemetry.core;

import io.opentelemetry.api.OpenTelemetry;
import io.opentelemetry.api.trace.Tracer;

import java.lang.System.Logger;
import java.util.ArrayList;
import java.util.List;
import java.util.concurrent.CountDownLatch;
import java.util.concurrent.TimeUnit;

/** Handle devolvido pelo bootstrap. Fail-soft (AD-006): no-op quando algo falha, sempre com diagnósticos. */
public final class Telemetry {

    private static final Logger LOGGER = System.getLogger(Telemetry.class.getName());
    /** Piso do AC 4: flush do shutdown dentro de 5 s. */
    static final long SHUTDOWN_TIMEOUT_SECONDS = 5;

    private final OpenTelemetry openTelemetry;
    private final boolean noop;
    private final List<String> diagnostics;
    private TelemetryRuntime runtime;

    private Telemetry(OpenTelemetry openTelemetry, boolean noop, List<String> diagnostics, TelemetryRuntime runtime) {
        this.openTelemetry = openTelemetry;
        this.noop = noop;
        this.diagnostics = new ArrayList<>(diagnostics);
        this.runtime = runtime;
    }

    static Telemetry real(TelemetryRuntime runtime, List<String> diagnostics) {
        return new Telemetry(runtime.openTelemetry(), false, diagnostics, runtime);
    }

    static Telemetry noop(List<String> diagnostics) {
        return new Telemetry(OpenTelemetry.noop(), true, diagnostics, null);
    }

    public OpenTelemetry openTelemetry() {
        return openTelemetry;
    }

    public boolean noop() {
        return noop;
    }

    public List<String> diagnostics() {
        return List.copyOf(diagnostics);
    }

    public Tracer tracer(String instrumentationScope) {
        return openTelemetry.getTracer(instrumentationScope);
    }

    /** Flush com teto de 5 s e liberação dos exporters; nunca lança exceção ao app (AD-006). */
    public void shutdown() {
        TelemetryRuntime toClose = runtime;
        if (toClose == null) {
            return;
        }
        runtime = null;
        CountDownLatch done = new CountDownLatch(1);
        Thread worker = new Thread(null, () -> {
            try {
                toClose.shutdown();
            } catch (RuntimeException e) {
                diagnostics.add("falha no shutdown da telemetria: " + e.getClass().getSimpleName());
            } finally {
                done.countDown();
            }
        }, "otel-telemetry-shutdown");
        worker.setDaemon(true);
        worker.start();
        try {
            if (!done.await(SHUTDOWN_TIMEOUT_SECONDS, TimeUnit.SECONDS)) {
                diagnostics.add("shutdown da telemetria não concluiu em " + SHUTDOWN_TIMEOUT_SECONDS + "s; prosseguindo");
            }
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
            diagnostics.add("shutdown da telemetria interrompido");
        }
    }
}
