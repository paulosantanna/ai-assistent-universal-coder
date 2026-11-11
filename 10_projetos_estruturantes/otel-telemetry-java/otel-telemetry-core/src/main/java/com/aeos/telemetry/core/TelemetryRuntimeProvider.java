package com.aeos.telemetry.core;

/** SPI: o módulo de exporters registra a implementação que monta o SDK OTel a partir da config resolvida.
 *  Descoberto via ServiceLoader; sem provider no classpath o bootstrap ativa no-op com diagnóstico. */
public interface TelemetryRuntimeProvider {

    TelemetryRuntime create(ResolvedConfig config);
}
