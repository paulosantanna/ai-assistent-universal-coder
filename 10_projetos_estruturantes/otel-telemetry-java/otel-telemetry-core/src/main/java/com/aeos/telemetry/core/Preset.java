package com.aeos.telemetry.core;

import java.util.List;

/** Destinos pré-configurados. Todos falam OTLP (AD-001); o preset só define endpoint+auth. */
public enum Preset {
    OFFLINE("offline", false, List.of()),
    DYNATRACE("dynatrace", true, List.of("OTEL_DYNATRACE_TOKEN")),
    GRAFANA("grafana", true, List.of("OTEL_GRAFANA_INSTANCE", "OTEL_GRAFANA_TOKEN")),
    SPLUNK("splunk", false, List.of()),
    OTELCOL("otelcol", false, List.of());

    private final String id;
    private final boolean requiresCredential;
    private final List<String> credentialEnvNames;

    Preset(String id, boolean requiresCredential, List<String> credentialEnvNames) {
        this.id = id;
        this.requiresCredential = requiresCredential;
        this.credentialEnvNames = credentialEnvNames;
    }

    public String id() {
        return id;
    }

    public boolean requiresCredential() {
        return requiresCredential;
    }

    public List<String> credentialEnvNames() {
        return credentialEnvNames;
    }

    /** Converte o identificador textual; null/blank devolve OFFLINE; desconhecido devolve null (fail-soft na resolução). */
    public static Preset parse(String value) {
        if (value == null || value.isBlank()) {
            return OFFLINE;
        }
        for (Preset p : values()) {
            if (p.id.equalsIgnoreCase(value.trim())) {
                return p;
            }
        }
        return null;
    }
}
