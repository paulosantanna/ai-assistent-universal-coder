package com.aeos.telemetry.core;

import org.yaml.snakeyaml.Yaml;

import java.io.InputStream;
import java.net.URI;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.ArrayList;
import java.util.EnumMap;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Locale;
import java.util.Map;
import java.util.Properties;

/** Resolve a configuração em camadas (AD-003): env OTEL_* e OTELTELEMETRY_* vencem sysprop otel.* e oteltelemetry.*,
 *  que vencem oteltelemetry.yaml (chaves planas), que vence o builder. Credenciais vêm EXCLUSIVAMENTE de runtime env. */
public final class ConfigResolver {

    private ConfigResolver() {
    }

    /** Conveniência de produção: env/sysprop reais e o arquivo oteltelemetry.yaml do diretório de trabalho. */
    public static ResolvedConfig resolve(TelemetryConfig builderConfig) {
        return resolve(System.getenv(), System.getProperties(), Path.of(TelemetryBootstrap.CONFIG_FILE), builderConfig);
    }

    public static ResolvedConfig resolve(Map<String, String> env, Properties sysprops, Path yamlPath,
                                         TelemetryConfig builderConfig) {
        List<String> diagnostics = new ArrayList<>();

        // Camada 1: builder (menor precedência)
        Map<String, String> values = new LinkedHashMap<>();
        TelemetryConfig bc = builderConfig == null ? TelemetryConfig.builder().build() : builderConfig;
        put(values, "service.name", bc.serviceName());
        put(values, "preset", bc.preset());
        put(values, "protocol", bc.protocol());
        put(values, "endpoint", bc.endpoint());
        Map<Signal, Map<String, String>> builderHeadersBySignal = new EnumMap<>(Signal.class);
        for (Signal s : Signal.values()) {
            put(values, "endpoint." + s.path(), bc.signalEndpoint(s));
            Map<String, String> builderHeaders = bc.headers(s);
            if (!builderHeaders.isEmpty()) {
                // fica como Map até o fim do resolve: round-trip por string trunca valores com vírgula
                builderHeadersBySignal.put(s, builderHeaders);
            }
        }

        // Camada 2: yaml (chaves planas, namespace exporter.otlp.* normalizado para chaves internas)
        for (Map.Entry<String, String> e : readFlatYaml(yamlPath, diagnostics).entrySet()) {
            values.put(normalizeYamlKey(e.getKey()), e.getValue());
        }

        // Camada 3: sysprop
        put(values, "service.name", sysprops.getProperty("otel.service.name"));
        put(values, "preset", sysprops.getProperty("oteltelemetry.preset"));
        put(values, "protocol", sysprops.getProperty("otel.exporter.otlp.protocol"));
        put(values, "endpoint", sysprops.getProperty("otel.exporter.otlp.endpoint"));
        for (Signal s : Signal.values()) {
            put(values, "endpoint." + s.path(), sysprops.getProperty("otel.exporter.otlp." + s.path() + ".endpoint"));
            put(values, "headers." + s.path(), sysprops.getProperty("otel.exporter.otlp." + s.path() + ".headers"));
        }

        // Camada 4: env (maior precedência)
        put(values, "service.name", env.get("OTEL_SERVICE_NAME"));
        put(values, "preset", env.get("OTELTELEMETRY_PRESET"));
        put(values, "protocol", env.get("OTEL_EXPORTER_OTLP_PROTOCOL"));
        put(values, "endpoint", env.get("OTEL_EXPORTER_OTLP_ENDPOINT"));
        for (Signal s : Signal.values()) {
            String upper = s.path().toUpperCase(Locale.ROOT);
            put(values, "endpoint." + s.path(), env.get("OTEL_EXPORTER_OTLP_" + upper + "_ENDPOINT"));
            put(values, "headers." + s.path(), env.get("OTEL_EXPORTER_OTLP_" + upper + "_HEADERS"));
        }

        Preset preset = Preset.parse(values.get("preset"));
        if (preset == null) {
            diagnostics.add("preset desconhecido (env OTELTELEMETRY_PRESET ou oteltelemetry.preset); usando offline");
            preset = Preset.OFFLINE;
        }

        String serviceName = values.getOrDefault("service.name", "unknown_service");
        ResolvedConfig.Protocol protocol = ResolvedConfig.Protocol.parse(values.get("protocol"));

        // Endpoints com validação de URL (fail-soft sinalizado em valid()).
        Map<Signal, String> signalEndpoints = new EnumMap<>(Signal.class);
        boolean valid = true;
        String base = values.get("endpoint");
        if (base != null && !isHttpUrl(base)) {
            diagnostics.add("endpoint base inválido (" + base + "): use http(s)://host:porta");
            valid = false;
        }
        for (Signal s : Signal.values()) {
            String perSignal = values.get("endpoint." + s.path());
            if (perSignal != null) {
                if (!isHttpUrl(perSignal)) {
                    diagnostics.add("endpoint." + s.path() + " inválido (" + perSignal + "): use http(s)://host:porta");
                    valid = false;
                } else {
                    signalEndpoints.put(s, perSignal.trim());
                }
            }
        }

        // Headers por sinal (k=v,k=v); itens malformados são ignorados SEM ecoar o conteúdo.
        // Headers do builder entram como Map direto quando nenhuma camada superior definiu
        // headers.<signal> — mesma precedência do encode por string, sem o truncamento.
        Map<Signal, Map<String, String>> headers = new EnumMap<>(Signal.class);
        Map<String, String> common = parseHeaders(values.get("headers"), diagnostics, "headers");
        for (Signal s : Signal.values()) {
            Map<String, String> merged = new LinkedHashMap<>(common);
            String perSignal = values.get("headers." + s.path());
            if (perSignal != null) {
                merged.putAll(parseHeaders(perSignal, diagnostics, "headers." + s.path()));
            } else if (builderHeadersBySignal.containsKey(s)) {
                merged.putAll(builderHeadersBySignal.get(s));
            }
            if (!merged.isEmpty()) {
                headers.put(s, merged);
            }
        }

        // Credenciais: exclusivamente de runtime env (AD-003); nunca de yaml/sysprop/builder.
        Map<String, String> credentials = new LinkedHashMap<>();
        for (String envName : preset.credentialEnvNames()) {
            String credential = env.get(envName);
            if (credential != null && !credential.isBlank()) {
                credentials.put(envName, credential);
            }
        }

        return new ResolvedConfig(preset, serviceName, protocol, base, signalEndpoints, headers, credentials,
                diagnostics, valid);
    }

    /** Converte chaves yaml do namespace exporter.otlp.* para as chaves internas de resolução.
     *  Ex.: exporter.otlp.traces.endpoint → endpoint.traces; exporter.otlp.endpoint → endpoint. */
    private static String normalizeYamlKey(String key) {
        if (!key.startsWith("exporter.otlp.")) {
            return key;
        }
        String rest = key.substring("exporter.otlp.".length());
        int dot = rest.indexOf('.');
        if (dot <= 0) {
            // endpoint, protocol, headers (comum) — já são as chaves internas
            return rest;
        }
        String signal = rest.substring(0, dot).toLowerCase(Locale.ROOT);
        String leaf = rest.substring(dot + 1);
        return switch (leaf) {
            case "endpoint" -> "endpoint." + signal;
            case "headers" -> "headers." + signal;
            default -> rest;
        };
    }

    private static void put(Map<String, String> values, String key, String value) {
        if (value != null) {
            values.put(key, value);
        }
    }

    private static Map<String, String> readFlatYaml(Path yamlPath, List<String> diagnostics) {
        if (yamlPath == null || !Files.isRegularFile(yamlPath)) {
            return Map.of();
        }
        try (InputStream in = Files.newInputStream(yamlPath)) {
            Object loaded = new Yaml().load(in);
            if (loaded == null) {
                return Map.of();
            }
            if (!(loaded instanceof Map<?, ?> map)) {
                diagnostics.add("oteltelemetry.yaml ignorado: conteúdo não é um mapa");
                return Map.of();
            }
            Map<String, String> flat = new LinkedHashMap<>();
            for (Map.Entry<?, ?> e : map.entrySet()) {
                if (e.getKey() != null && e.getValue() != null) {
                    flat.put(String.valueOf(e.getKey()).trim(), String.valueOf(e.getValue()).trim());
                }
            }
            return flat;
        } catch (Exception e) {
            diagnostics.add("oteltelemetry.yaml ignorado: " + e.getClass().getSimpleName());
            return Map.of();
        }
    }

    private static Map<String, String> parseHeaders(String raw, List<String> diagnostics, String key) {
        if (raw == null || raw.isBlank()) {
            return Map.of();
        }
        Map<String, String> parsed = new LinkedHashMap<>();
        for (String item : raw.split(",")) {
            int eq = item.indexOf('=');
            if (eq > 0) {
                parsed.put(item.substring(0, eq).trim(), item.substring(eq + 1).trim());
            } else if (!item.isBlank()) {
                // sem ecoar o item: pode conter segredo colocado por operador
                diagnostics.add("header ignorado em " + key + " (formato k=v esperado)");
            }
        }
        return parsed;
    }

    private static boolean isHttpUrl(String value) {
        try {
            URI uri = URI.create(value.trim());
            String scheme = uri.getScheme();
            return ("http".equalsIgnoreCase(scheme) || "https".equalsIgnoreCase(scheme)) && uri.getHost() != null;
        } catch (IllegalArgumentException e) {
            return false;
        }
    }
}
