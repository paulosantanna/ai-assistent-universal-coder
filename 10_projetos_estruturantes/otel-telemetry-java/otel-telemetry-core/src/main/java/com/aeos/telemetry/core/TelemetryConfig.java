package com.aeos.telemetry.core;

import java.util.Collections;
import java.util.EnumMap;
import java.util.LinkedHashMap;
import java.util.Map;

/** Configuração explícita do builder — camada de MENOR precedência (AD-003: env &gt; sysprop &gt; yaml &gt; builder). */
public final class TelemetryConfig {

    private final String serviceName;
    private final String preset;
    private final String protocol;
    private final String endpoint;
    private final Map<Signal, String> signalEndpoints;
    private final Map<Signal, Map<String, String>> headers;

    private TelemetryConfig(Builder builder) {
        this.serviceName = builder.serviceName;
        this.preset = builder.preset;
        this.protocol = builder.protocol;
        this.endpoint = builder.endpoint;
        this.signalEndpoints = Collections.unmodifiableMap(new EnumMap<>(builder.signalEndpoints));
        Map<Signal, Map<String, String>> snapshot = new EnumMap<>(Signal.class);
        for (Map.Entry<Signal, Map<String, String>> e : builder.headers.entrySet()) {
            snapshot.put(e.getKey(), Collections.unmodifiableMap(new LinkedHashMap<>(e.getValue())));
        }
        this.headers = Collections.unmodifiableMap(snapshot);
    }

    public String serviceName() {
        return serviceName;
    }

    public String preset() {
        return preset;
    }

    public String protocol() {
        return protocol;
    }

    public String endpoint() {
        return endpoint;
    }

    public String signalEndpoint(Signal signal) {
        return signalEndpoints.get(signal);
    }

    public Map<String, String> headers(Signal signal) {
        return headers.getOrDefault(signal, Map.of());
    }

    public static Builder builder() {
        return new Builder();
    }

    public static final class Builder {
        private String serviceName;
        private String preset;
        private String protocol;
        private String endpoint;
        private final Map<Signal, String> signalEndpoints = new EnumMap<>(Signal.class);
        private final Map<Signal, Map<String, String>> headers = new EnumMap<>(Signal.class);

        public Builder serviceName(String value) {
            this.serviceName = value;
            return this;
        }

        public Builder preset(String value) {
            this.preset = value;
            return this;
        }

        public Builder protocol(String value) {
            this.protocol = value;
            return this;
        }

        public Builder endpoint(String value) {
            this.endpoint = value;
            return this;
        }

        public Builder signalEndpoint(Signal signal, String value) {
            this.signalEndpoints.put(signal, value);
            return this;
        }

        public Builder header(Signal signal, String name, String value) {
            this.headers.computeIfAbsent(signal, s -> new LinkedHashMap<>()).put(name, value);
            return this;
        }

        public Builder headers(Signal signal, Map<String, String> values) {
            if (values != null) {
                this.headers.computeIfAbsent(signal, s -> new LinkedHashMap<>()).putAll(values);
            }
            return this;
        }

        public TelemetryConfig build() {
            return new TelemetryConfig(this);
        }
    }
}
