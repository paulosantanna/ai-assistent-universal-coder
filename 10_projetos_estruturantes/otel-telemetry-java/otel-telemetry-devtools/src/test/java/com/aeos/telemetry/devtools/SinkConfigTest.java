package com.aeos.telemetry.devtools;

import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.io.TempDir;

import java.io.IOException;
import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import java.nio.charset.StandardCharsets;
import java.nio.file.Path;
import java.time.Duration;
import java.util.Map;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertTrue;

/** C16: bind default loopback:14318, overrides por env, 403 sem token; C17: disabled → 503 sem gravar. */
class SinkConfigTest {

    private static final HttpClient CLIENT = HttpClient.newHttpClient();

    @Test
    void loopbackDefaultAndOverrides() {
        SinkConfig defaults = SinkConfig.fromEnv(Map.of());
        assertEquals("127.0.0.1", defaults.host());
        assertEquals(14318, defaults.port());
        assertFalse(defaults.authRequired());
        assertFalse(defaults.disabled());
        assertEquals("otlp-sink", defaults.dir());
        assertEquals(32L * 1024 * 1024, defaults.maxBytes());
        assertEquals(5, defaults.maxFiles());
        assertEquals(Duration.ofMinutes(1440), defaults.maxAge());

        SinkConfig overrides = SinkConfig.fromEnv(Map.of(
                "OTELTELEMETRY_SINK_HOST", "0.0.0.0",
                "OTELTELEMETRY_SINK_PORT", "15000",
                "OTELTELEMETRY_SINK_DIR", "out/sink",
                "OTELTELEMETRY_SINK_MAX_MB", "1",
                "OTELTELEMETRY_SINK_MAX_FILES", "3",
                "OTELTELEMETRY_SINK_MAX_AGE_MINUTES", "60"));
        assertEquals("0.0.0.0", overrides.host());
        assertEquals(15000, overrides.port());
        assertTrue(overrides.authRequired(), "host não-loopback exige token");
        assertEquals(1024 * 1024, overrides.maxBytes());
        assertEquals(3, overrides.maxFiles());
        assertEquals(Duration.ofMinutes(60), overrides.maxAge());

        SinkConfig withToken = SinkConfig.fromEnv(Map.of(
                "OTELTELEMETRY_SINK_HOST", "127.0.0.1",
                "OTELTELEMETRY_SINK_TOKEN", "segredo"));
        assertTrue(withToken.authRequired(), "token configurado exige auth mesmo no loopback");
        assertFalse(withToken.toString().contains("segredo"),
                "toString() nunca deve ecoar o token");
    }

    @Test
    void missingTokenReturns403(@TempDir Path tempDir) throws Exception {
        SinkConfig config = SinkConfig.of("127.0.0.1", 0, "token-certo", false,
                tempDir.resolve("otlp-sink").toString(), 32L * 1024 * 1024, 5, Duration.ofMinutes(1440));
        OtlpSinkServer server = new OtlpSinkServer(config);
        server.start();
        try {
            String base = "http://127.0.0.1:" + server.port();

            HttpResponse<String> noAuth = post(base + "/v1/traces", TestPayloads.traceProtobuf("s1"), null);
            assertEquals(403, noAuth.statusCode());
            assertTrue(noAuth.body().contains("403"));

            HttpResponse<String> wrongAuth = post(base + "/v1/traces",
                    TestPayloads.traceProtobuf("s1"), "token-errado");
            assertEquals(403, wrongAuth.statusCode());

            HttpResponse<String> apiNoAuth = get(base + "/api/traces");
            assertEquals(403, apiNoAuth.statusCode());

            HttpResponse<String> healthNoAuth = get(base + "/api/health");
            assertEquals(200, healthNoAuth.statusCode(), "health é isento de auth");

            HttpResponse<String> withAuth = post(base + "/v1/traces",
                    TestPayloads.traceProtobuf("span-com-token"), "token-certo");
            assertEquals(200, withAuth.statusCode());
        } finally {
            server.close();
        }
    }

    @Test
    void disabledReturns503(@TempDir Path tempDir) throws Exception {
        SinkConfig config = SinkConfig.of("127.0.0.1", 0, null, true,
                tempDir.resolve("otlp-sink").toString(), 32L * 1024 * 1024, 5, Duration.ofMinutes(1440));
        OtlpSinkServer server = new OtlpSinkServer(config);
        server.start();
        try {
            String base = "http://127.0.0.1:" + server.port();
            HttpResponse<String> response = post(base + "/v1/traces", TestPayloads.traceProtobuf("s1"), null);
            assertEquals(503, response.statusCode());
            HttpResponse<String> api = get(base + "/api/traces");
            assertEquals(503, api.statusCode());
            HttpResponse<String> health = get(base + "/api/health");
            assertEquals(200, health.statusCode(), "health permanece disponível");

            // nada gravado
            assertFalse(java.nio.file.Files.exists(tempDir.resolve("otlp-sink").resolve("traces.jsonl")));
        } finally {
            server.close();
        }
    }

    private static HttpResponse<String> post(String url, byte[] body, String token)
            throws IOException, InterruptedException {
        HttpRequest.Builder builder = HttpRequest.newBuilder(URI.create(url))
                .header("Content-Type", "application/x-protobuf")
                .POST(HttpRequest.BodyPublishers.ofByteArray(body));
        if (token != null) {
            builder.header("Authorization", "Bearer " + token);
        }
        return CLIENT.send(builder.build(), HttpResponse.BodyHandlers.ofString(StandardCharsets.UTF_8));
    }

    private static HttpResponse<String> get(String url) throws IOException, InterruptedException {
        return CLIENT.send(HttpRequest.newBuilder(URI.create(url)).GET().build(),
                HttpResponse.BodyHandlers.ofString(StandardCharsets.UTF_8));
    }
}
