package com.aeos.telemetry.core;

/** Os três sinais OTLP suportados pela biblioteca. */
public enum Signal {
    TRACES("traces"),
    METRICS("metrics"),
    LOGS("logs");

    private final String path;

    Signal(String path) {
        this.path = path;
    }

    /** Nome do sinal usado em rotas e arquivos (ex.: "/v1/traces"). */
    public String path() {
        return path;
    }
}
