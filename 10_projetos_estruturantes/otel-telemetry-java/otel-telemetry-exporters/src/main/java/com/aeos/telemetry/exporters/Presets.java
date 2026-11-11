package com.aeos.telemetry.exporters;

import com.aeos.telemetry.core.Preset;
import com.aeos.telemetry.core.ResolvedConfig;
import com.aeos.telemetry.core.Signal;

import java.util.LinkedHashMap;
import java.util.Map;

/** Forma a URL e os headers de cada preset. Todos os destinos falam OTLP (AD-001);
 *  o preset só define endpoint+auth.
 *
 *  AVISO J1: as rotas e headers de dynatrace e grafana foram definidos pelo plano (owner)
 *  e estão rotulados NÃO VERIFICADO — a documentação dos vendors retornou 403/404 na
 *  consulta de 2026-11-11. A verificação em doc real é pré-condição para remover o rótulo. */
final class Presets {

    private Presets() {
    }

    /** Especificação do destino de um sinal. Lança IllegalArgumentException quando o preset
     *  não tem insumo suficiente (fail-soft: o bootstrap converte em no-op com diagnóstico). */
    static ExporterSpec spec(ResolvedConfig config, Signal signal) {
        Preset preset = config.preset();

        // Override por sinal é usado VERBATIM (sem anexar caminho).
        String override = config.signalEndpoint(signal);
        if (override != null) {
            return new ExporterSpec(signal, override, headers(config, signal));
        }

        return switch (preset) {
            case OFFLINE -> new ExporterSpec(signal, withPath(base(config, "http://127.0.0.1:14318"),
                    signal, config), headers(config, signal));
            case OTELCOL, SPLUNK -> new ExporterSpec(signal,
                    withPath(base(config, defaultOtelcolEndpoint(config)), signal, config),
                    headers(config, signal));
            case DYNATRACE -> dynatrace(config, signal);
            case GRAFANA -> grafana(config, signal);
        };
    }

    private static ExporterSpec dynatrace(ResolvedConfig config, Signal signal) {
        String base = config.baseEndpoint();
        if (base == null || base.isBlank()) {
            // NÃO VERIFICADO J1: rota assumida pelo plano {base}/api/v2/otlp/v1/{signal}
            throw new IllegalArgumentException(
                    "preset dynatrace requer OTEL_EXPORTER_OTLP_ENDPOINT (base https://<tenant>.live.dynatrace.com)");
        }
        if (config.protocol() == ResolvedConfig.Protocol.GRPC) {
            throw new IllegalArgumentException(
                    "preset dynatrace suporta apenas http/protobuf (rota NÃO VERIFICADO J1 para grpc)");
        }
        return new ExporterSpec(signal, stripTrailingSlash(base) + "/api/v2/otlp/v1/" + signal.path(),
                headers(config, signal));
    }

    private static ExporterSpec grafana(ResolvedConfig config, Signal signal) {
        String instance = config.credential("OTEL_GRAFANA_INSTANCE");
        if (instance == null || instance.isBlank()) {
            // NÃO VERIFICADO J1: rota assumida pelo plano {instance}/v1/{signal}
            throw new IllegalArgumentException(
                    "preset grafana requer OTEL_GRAFANA_INSTANCE (URL base do gateway OTLP)");
        }
        if (config.protocol() == ResolvedConfig.Protocol.GRPC) {
            throw new IllegalArgumentException(
                    "preset grafana suporta apenas http/protobuf (rota NÃO VERIFICADO J1 para grpc)");
        }
        return new ExporterSpec(signal, stripTrailingSlash(instance) + "/v1/" + signal.path(),
                headers(config, signal));
    }

    private static String base(ResolvedConfig config, String fallback) {
        String base = config.baseEndpoint();
        return base != null && !base.isBlank() ? base : fallback;
    }

    private static String defaultOtelcolEndpoint(ResolvedConfig config) {
        // Convenção OTLP: 4318 http, 4317 grpc
        return config.protocol() == ResolvedConfig.Protocol.GRPC
                ? "http://localhost:4317"
                : "http://localhost:4318";
    }

    /** Anexa /v1/{signal} ao endpoint base (presets genéricos). */
    private static String withPath(String base, Signal signal, ResolvedConfig config) {
        return stripTrailingSlash(base) + "/v1/" + signal.path();
    }

    private static String stripTrailingSlash(String url) {
        String trimmed = url.trim();
        return trimmed.endsWith("/") ? trimmed.substring(0, trimmed.length() - 1) : trimmed;
    }

    /** Headers do sinal: credencial do preset + headers declarados pelo usuário (usuário vence). */
    private static Map<String, String> headers(ResolvedConfig config, Signal signal) {
        Map<String, String> result = new LinkedHashMap<>();
        switch (config.preset()) {
            case DYNATRACE -> {
                // NÃO VERIFICADO J1: header assumido pelo plano
                String token = config.credentialValue();
                if (token != null) {
                    result.put("Authorization", "Api-Token " + token);
                }
            }
            case GRAFANA -> {
                // NÃO VERIFICADO J1: header assumido pelo plano (instancia:token)
                String bearer = config.credentialValue();
                if (bearer != null) {
                    result.put("Authorization", "Bearer " + bearer);
                }
            }
            default -> {
            }
        }
        result.putAll(config.headers(signal));
        return Map.copyOf(result);
    }
}
