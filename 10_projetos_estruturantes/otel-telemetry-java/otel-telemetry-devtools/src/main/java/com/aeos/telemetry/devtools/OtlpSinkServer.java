package com.aeos.telemetry.devtools;

import com.google.protobuf.InvalidProtocolBufferException;
import com.google.protobuf.util.JsonFormat;
import com.sun.net.httpserver.HttpExchange;
import com.sun.net.httpserver.HttpServer;
import io.opentelemetry.proto.collector.logs.v1.ExportLogsServiceRequest;
import io.opentelemetry.proto.collector.metrics.v1.ExportMetricsServiceRequest;
import io.opentelemetry.proto.collector.trace.v1.ExportTraceServiceRequest;

import java.io.IOException;
import java.io.OutputStream;
import java.net.InetSocketAddress;
import java.net.URLDecoder;
import java.nio.charset.StandardCharsets;
import java.security.MessageDigest;
import java.time.Clock;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;

/** Sink OTLP/HTTP offline: grava OTLP-JSON rotativo por sinal e serve a API do dashboard.
 *  Rotas: POST /v1/{traces,metrics,logs} · GET /api/{traces,metrics,logs}?since&limit ·
 *  GET /api/health · GET / (dashboard estático do classpath). Auth: Authorization Bearer
 *  quando exigida; /api/health isento. Disabled → 503 sem gravar (AD-004). */
public final class OtlpSinkServer implements AutoCloseable {

    private static final int DEFAULT_API_LIMIT = 100;
    private static final int MAX_API_LIMIT = 500;

    private final HttpServer server;
    private final ExecutorService executor;
    private final SinkConfig config;
    private final JsonlStore traces;
    private final JsonlStore metrics;
    private final JsonlStore logs;

    public OtlpSinkServer(SinkConfig config) throws IOException {
        this(config, Clock.systemUTC());
    }

    public OtlpSinkServer(SinkConfig config, Clock clock) throws IOException {
        this.config = config;
        this.traces = JsonlStore.create(config, "traces", clock);
        this.metrics = JsonlStore.create(config, "metrics", clock);
        this.logs = JsonlStore.create(config, "logs", clock);
        this.executor = Executors.newFixedThreadPool(4);
        this.server = HttpServer.create(new InetSocketAddress(config.host(), config.port()), 0);
        server.createContext("/v1/traces", this::handleOtlp);
        server.createContext("/v1/metrics", this::handleOtlp);
        server.createContext("/v1/logs", this::handleOtlp);
        server.createContext("/api/health", this::handleHealth);
        server.createContext("/api/traces", ex -> handleApi(ex, traces, "traces"));
        server.createContext("/api/metrics", ex -> handleApi(ex, metrics, "metrics"));
        server.createContext("/api/logs", ex -> handleApi(ex, logs, "logs"));
        server.createContext("/", this::handleStatic);
        server.setExecutor(executor);
    }

    public void start() {
        server.start();
    }

    @Override
    public void close() {
        server.stop(0);
        executor.shutdownNow();
    }

    public int port() {
        return server.getAddress().getPort();
    }

    JsonlStore store(String signal) {
        return switch (signal) {
            case "traces" -> traces;
            case "metrics" -> metrics;
            case "logs" -> logs;
            default -> throw new IllegalArgumentException("sinal desconhecido: " + signal);
        };
    }

    private void handleOtlp(HttpExchange exchange) throws IOException {
        String path = exchange.getRequestURI().getPath();
        try {
            if (config.disabled()) {
                send(exchange, 503, "application/json", json("error", "sink desabilitado (503)"));
                return;
            }
            if (!authorized(exchange)) {
                send(exchange, 403, "application/json", json("error", "token ausente ou inválido (403)"));
                return;
            }
            if (!"POST".equalsIgnoreCase(exchange.getRequestMethod())) {
                send(exchange, 405, "application/json", json("error", "use POST /v1/{traces,metrics,logs}"));
                return;
            }
            String signal = signalOf(path, "v1");
            byte[] body = exchange.getRequestBody().readAllBytes();
            String json = toJson(signal, body);
            store(signal).append(json);
            send(exchange, 200, "application/json", "{\"ok\":true,\"signal\":\"" + signal + "\"}");
        } catch (InvalidProtocolBufferException e) {
            // InvalidProtocolBufferException estende IOException: o catch específico
            // (400 com causa) precisa preceder o catch genérico de IOException (500).
            send(exchange, 400, "application/json",
                    "{\"error\":\"payload protobuf inválido\",\"cause\":\""
                            + escape(e.toString()) + "\"}");
        } catch (IllegalArgumentException e) {
            send(exchange, 400, "application/json",
                    "{\"error\":\"payload protobuf inválido\",\"cause\":\""
                            + escape(e.toString()) + "\"}");
        } catch (IOException e) {
            send(exchange, 500, "application/json",
                    "{\"error\":\"falha ao gravar\",\"cause\":\"" + escape(e.toString()) + "\"}");
        } finally {
            exchange.close();
        }
    }

    private void handleApi(HttpExchange exchange, JsonlStore store, String signal) throws IOException {
        try {
            if (config.disabled()) {
                send(exchange, 503, "application/json", json("error", "sink desabilitado (503)"));
                return;
            }
            if (!authorized(exchange)) {
                send(exchange, 403, "application/json", json("error", "token ausente ou inválido (403)"));
                return;
            }
            if (!"GET".equalsIgnoreCase(exchange.getRequestMethod())) {
                send(exchange, 405, "application/json", json("error", "use GET /api/" + signal));
                return;
            }
            Map<String, String> query = queryParams(exchange);
            Long since = null;
            if (query.containsKey("since")) {
                try {
                    since = Long.parseLong(query.get("since"));
                } catch (NumberFormatException e) {
                    send(exchange, 400, "application/json",
                            json("error", "parâmetro since deve ser epoch millis"));
                    return;
                }
            }
            int limit = DEFAULT_API_LIMIT;
            if (query.containsKey("limit")) {
                try {
                    limit = Integer.parseInt(query.get("limit"));
                } catch (NumberFormatException e) {
                    send(exchange, 400, "application/json",
                            json("error", "parâmetro limit deve ser inteiro"));
                    return;
                }
                if (limit < 1 || limit > MAX_API_LIMIT) {
                    send(exchange, 400, "application/json",
                            json("error", "limit deve estar entre 1 e " + MAX_API_LIMIT));
                    return;
                }
            }
            List<String> lines = store.readRecent(since, limit);
            StringBuilder response = new StringBuilder("{\"signal\":\"").append(signal)
                    .append("\",\"count\":").append(lines.size()).append(",\"items\":[");
            for (int i = 0; i < lines.size(); i++) {
                if (i > 0) {
                    response.append(',');
                }
                response.append(lines.get(i));
            }
            response.append("]}");
            send(exchange, 200, "application/json", response.toString());
        } finally {
            exchange.close();
        }
    }

    private void handleHealth(HttpExchange exchange) throws IOException {
        try {
            if (!"GET".equalsIgnoreCase(exchange.getRequestMethod())) {
                send(exchange, 405, "application/json", json("error", "use GET /api/health"));
                return;
            }
            // isenta de auth e de disabled: sonda de vida
            send(exchange, 200, "application/json", "{\"ok\":true}");
        } finally {
            exchange.close();
        }
    }

    private void handleStatic(HttpExchange exchange) throws IOException {
        try {
            if (!"GET".equalsIgnoreCase(exchange.getRequestMethod())) {
                send(exchange, 405, "text/plain", "use GET");
                return;
            }
            String path = exchange.getRequestURI().getPath();
            String resource = resourceFor(path);
            if (resource == null || getClass().getClassLoader().getResource(resource) == null) {
                send(exchange, 404, "text/plain", "recurso não encontrado: " + path);
                return;
            }
            byte[] bytes;
            try (var in = getClass().getClassLoader().getResourceAsStream(resource)) {
                bytes = in == null ? new byte[0] : in.readAllBytes();
            }
            send(exchange, 200, contentTypeOf(resource), bytes);
        } finally {
            exchange.close();
        }
    }

    /** Caminho relativo à raiz do dashboard servida em /: "/" → dashboard/index.html;
     *  /style.css e /dashboard.js (refs relativas do index.html) → dashboard/<nome>;
     *  /dashboard/x → dashboard/x. Segmentos ".." são rejeitados (fail-closed). */
    private static String resourceFor(String path) {
        if ("/".equals(path) || "/dashboard".equals(path)) {
            return "dashboard/index.html";
        }
        String rel = path.startsWith("/") ? path.substring(1) : path;
        if (rel.isBlank() || rel.contains("..")) {
            return null;
        }
        if (rel.startsWith("dashboard/")) {
            return rel;
        }
        return "dashboard/" + rel;
    }

    /** Authorization Bearer constante-tempo; aceita sempre quando auth não exigida. */
    private boolean authorized(HttpExchange exchange) {
        if (!config.authRequired()) {
            return true;
        }
        String header = exchange.getRequestHeaders().getFirst("Authorization");
        if (header == null) {
            return false;
        }
        String expected = "Bearer " + config.token();
        return MessageDigest.isEqual(
                header.getBytes(StandardCharsets.UTF_8), expected.getBytes(StandardCharsets.UTF_8));
    }

    /** Converte o protobuf OTLP do sinal em OTLP-JSON de uma linha (ids em base64).
     *  omittingInsignificantWhitespace é obrigatório: sem ele o printer embute newlines
     *  e quebra o formato JSONL (uma mensagem = uma linha). */
    private static String toJson(String signal, byte[] body) throws InvalidProtocolBufferException {
        return switch (signal) {
            case "traces" -> JsonFormat.printer().omittingInsignificantWhitespace()
                    .print(ExportTraceServiceRequest.parseFrom(body));
            case "metrics" -> JsonFormat.printer().omittingInsignificantWhitespace()
                    .print(ExportMetricsServiceRequest.parseFrom(body));
            case "logs" -> JsonFormat.printer().omittingInsignificantWhitespace()
                    .print(ExportLogsServiceRequest.parseFrom(body));
            default -> throw new IllegalArgumentException("sinal desconhecido: " + signal);
        };
    }

    private static String signalOf(String path, String prefix) {
        String rest = path.startsWith("/" + prefix + "/") ? path.substring(prefix.length() + 2) : null;
        if (rest == null) {
            throw new IllegalArgumentException("rota inválida: " + path);
        }
        int slash = rest.indexOf('/');
        return slash > 0 ? rest.substring(0, slash) : rest;
    }

    private static Map<String, String> queryParams(HttpExchange exchange) {
        Map<String, String> result = new LinkedHashMap<>();
        String raw = exchange.getRequestURI().getRawQuery();
        if (raw == null || raw.isBlank()) {
            return result;
        }
        for (String pair : raw.split("&")) {
            int eq = pair.indexOf('=');
            if (eq <= 0) {
                continue;
            }
            result.put(URLDecoder.decode(pair.substring(0, eq), StandardCharsets.UTF_8),
                    URLDecoder.decode(pair.substring(eq + 1), StandardCharsets.UTF_8));
        }
        return result;
    }

    private static String json(String key, String value) {
        return "{\"" + key + "\":\"" + value + "\"}";
    }

    private static String escape(String value) {
        return value.replace("\\", "\\\\").replace("\"", "\\\"")
                .replace("\n", " ").replace("\r", " ");
    }

    private static String contentTypeOf(String resource) {
        if (resource.endsWith(".html")) {
            return "text/html; charset=utf-8";
        }
        if (resource.endsWith(".js")) {
            return "text/javascript; charset=utf-8";
        }
        if (resource.endsWith(".css")) {
            return "text/css; charset=utf-8";
        }
        return "application/octet-stream";
    }

    private static void send(HttpExchange exchange, int status, String contentType, String body)
            throws IOException {
        send(exchange, status, contentType, body.getBytes(StandardCharsets.UTF_8));
    }

    private static void send(HttpExchange exchange, int status, String contentType, byte[] body)
            throws IOException {
        exchange.getResponseHeaders().set("Content-Type", contentType);
        exchange.sendResponseHeaders(status, body.length == 0 ? -1 : body.length);
        if (body.length > 0) {
            try (OutputStream out = exchange.getResponseBody()) {
                out.write(body);
            }
        }
    }
}
