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

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;

/** C18/C19: /api/{traces,metrics,logs} 200 com dados e 400 em parâmetro inválido; /api/health 200. */
class SinkApiTest {

    private static final HttpClient CLIENT = HttpClient.newHttpClient();

    private static OtlpSinkServer startServer(@TempDir Path tempDir) throws IOException {
        SinkConfig config = SinkConfig.of("127.0.0.1", 0, null, false,
                tempDir.resolve("otlp-sink").toString(), 32L * 1024 * 1024, 5, Duration.ofMinutes(1440));
        OtlpSinkServer server = new OtlpSinkServer(config);
        server.start();
        return server;
    }

    private static HttpResponse<String> get(String url) throws IOException, InterruptedException {
        HttpRequest request = HttpRequest.newBuilder(URI.create(url)).GET().build();
        return CLIENT.send(request, HttpResponse.BodyHandlers.ofString(StandardCharsets.UTF_8));
    }

    @Test
    void apiRoutesStatuses(@TempDir Path tempDir) throws Exception {
        OtlpSinkServer server = startServer(tempDir);
        try {
            String base = "http://127.0.0.1:" + server.port();
            // grava um payload de cada sinal
            assertEquals(200, post(base + "/v1/traces", TestPayloads.traceProtobuf("span-api")).statusCode());
            assertEquals(200, post(base + "/v1/metrics", TestPayloads.metricProtobuf("api.metric")).statusCode());
            assertEquals(200, post(base + "/v1/logs", TestPayloads.logProtobuf("log-api")).statusCode());

            HttpResponse<String> traces = get(base + "/api/traces?limit=1");
            assertEquals(200, traces.statusCode());
            assertTrue(traces.body().contains("span-api"));

            HttpResponse<String> metrics = get(base + "/api/metrics");
            assertEquals(200, metrics.statusCode());
            assertTrue(metrics.body().contains("api.metric"));

            HttpResponse<String> logs = get(base + "/api/logs?since=0&limit=100");
            assertEquals(200, logs.statusCode());
            assertTrue(logs.body().contains("log-api"));

            HttpResponse<String> invalidSince = get(base + "/api/traces?since=abc");
            assertEquals(400, invalidSince.statusCode());
            assertTrue(invalidSince.body().contains("since"));

            HttpResponse<String> invalidLimit = get(base + "/api/logs?limit=0");
            assertEquals(400, invalidLimit.statusCode());
            assertTrue(invalidLimit.body().contains("limit"));
        } finally {
            server.close();
        }
    }

    @Test
    void healthOk(@TempDir Path tempDir) throws Exception {
        OtlpSinkServer server = startServer(tempDir);
        try {
            HttpResponse<String> response = get("http://127.0.0.1:" + server.port() + "/api/health");
            assertEquals(200, response.statusCode());
            assertEquals("{\"ok\":true}", response.body());
        } finally {
            server.close();
        }
    }

    private static HttpResponse<String> post(String url, byte[] body)
            throws IOException, InterruptedException {
        HttpRequest request = HttpRequest.newBuilder(URI.create(url))
                .header("Content-Type", "application/x-protobuf")
                .POST(HttpRequest.BodyPublishers.ofByteArray(body))
                .build();
        return CLIENT.send(request, HttpResponse.BodyHandlers.ofString(StandardCharsets.UTF_8));
    }
}
