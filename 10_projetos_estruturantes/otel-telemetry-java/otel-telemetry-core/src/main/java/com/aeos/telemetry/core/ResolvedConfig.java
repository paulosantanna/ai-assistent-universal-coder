package com.aeos.telemetry.core;

import java.util.ArrayList;
import java.util.Collections;
import java.util.EnumMap;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;

/** Configuração resolvida (env &gt; sysprop &gt; yaml &gt; builder) entregue ao runtime de exporters.
 *  Credenciais ficam apenas em memória: nunca aparecem em diagnostics() nem em toString() (AD-003). */
public final class ResolvedConfig {

    /** Protocolo OTLP (AD-001); default http/protobuf. */
    public enum Protocol {
        HTTP_PROTOBUF("http/protobuf"),
        GRPC("grpc");

        private final String id;

        Protocol(String id) {
            this.id = id;
        }

        public String id() {
            return id;
        }

        public static Protocol parse(String value) {
            if (value != null && "grpc".equalsIgnoreCase(value.trim())) {
                return GRPC;
            }
            return HTTP_PROTOBUF;
        }
    }

    private final Preset preset;
    private final String serviceName;
    private final Protocol protocol;
    private final String baseEndpoint;
    private final Map<Signal, String> signalEndpoints;
    private final Map<Signal, Map<String, String>> headers;
    private final Map<String, String> credentials;
    private final List<String> diagnostics;
    private final boolean valid;

    ResolvedConfig(Preset preset, String serviceName, Protocol protocol, String baseEndpoint,
                   Map<Signal, String> signalEndpoints, Map<Signal, Map<String, String>> headers,
                   Map<String, String> credentials, List<String> diagnostics, boolean valid) {
        this.preset = preset;
        this.serviceName = serviceName;
        this.protocol = protocol;
        this.baseEndpoint = baseEndpoint;
        this.signalEndpoints = Collections.unmodifiableMap(new EnumMap<>(signalEndpoints));
        this.headers = Collections.unmodifiableMap(new EnumMap<>(headers));
        this.credentials = Collections.unmodifiableMap(new LinkedHashMap<>(credentials));
        this.diagnostics = Collections.unmodifiableList(new ArrayList<>(diagnostics));
        this.valid = valid;
    }

    public Preset preset() {
        return preset;
    }

    public String serviceName() {
        return serviceName;
    }

    public Protocol protocol() {
        return protocol;
    }

    /** Endpoint base (OTEL_EXPORTER_OTLP_ENDPOINT ou builder); null quando ausente. */
    public String baseEndpoint() {
        return baseEndpoint;
    }

    /** Endpoint absoluto por sinal (override verbatim); null quando ausente. */
    public String signalEndpoint(Signal signal) {
        return signalEndpoints.get(signal);
    }

    /** Headers declarados por sinal (sem os headers de credencial do preset). */
    public Map<String, String> headers(Signal signal) {
        return headers.getOrDefault(signal, Map.of());
    }

    /** true quando todas as envs de credencial do preset estão presentes e preenchidas. */
    public boolean credentialPresent() {
        for (String env : preset.credentialEnvNames()) {
            String value = credentials.get(env);
            if (value == null || value.isBlank()) {
                return false;
            }
        }
        return true;
    }

    /** Valor de credencial para o header do preset (em memória; GRAFANA junta "instancia:token"). */
    public String credentialValue() {
        if (!preset.requiresCredential() || !credentialPresent()) {
            return null;
        }
        if (preset == Preset.GRAFANA) {
            return credentials.get("OTEL_GRAFANA_INSTANCE") + ":" + credentials.get("OTEL_GRAFANA_TOKEN");
        }
        return credentials.get(preset.credentialEnvNames().get(0));
    }

    /** Valor bruto da credencial de um env específico (ex.: OTEL_GRAFANA_INSTANCE como URL base).
     *  Somente em memória: toString() e diagnostics() nunca a incluem (AD-003). */
    public String credential(String envName) {
        return credentials.get(envName);
    }

    /** Diagnósticos da resolução — nunca contêm valores de credencial. */
    public List<String> diagnostics() {
        return diagnostics;
    }

    /** false quando alguma URL malformada foi detectada (bootstrap ativa no-op). */
    public boolean valid() {
        return valid;
    }

    @Override
    public String toString() {
        return "ResolvedConfig{preset=" + preset + ", serviceName='" + serviceName + "', protocol=" + protocol
                + ", baseEndpoint=" + baseEndpoint + ", signalEndpoints=" + signalEndpoints
                + ", credentialPresent=" + credentialPresent() + ", valid=" + valid + "}";
    }
}
