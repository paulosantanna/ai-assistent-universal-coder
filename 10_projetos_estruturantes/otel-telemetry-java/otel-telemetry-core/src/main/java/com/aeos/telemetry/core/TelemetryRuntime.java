package com.aeos.telemetry.core;

import io.opentelemetry.api.OpenTelemetry;

/** Runtime instalado pelo provider: SDK vivo + shutdown que faz flush e libera os exporters. */
public interface TelemetryRuntime {

    OpenTelemetry openTelemetry();

    void shutdown();
}
