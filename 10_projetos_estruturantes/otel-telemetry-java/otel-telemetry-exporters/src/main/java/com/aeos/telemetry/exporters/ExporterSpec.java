package com.aeos.telemetry.exporters;

import com.aeos.telemetry.core.Signal;

import java.util.Map;

/** Destino concreto de um sinal: URL final e headers (credencial do preset + headers do usuário). */
public record ExporterSpec(Signal signal, String url, Map<String, String> headers) {
}
