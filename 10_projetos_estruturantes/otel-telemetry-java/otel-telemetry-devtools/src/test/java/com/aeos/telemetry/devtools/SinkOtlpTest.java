package com.aeos.telemetry.devtools;

import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.io.TempDir;

import java.io.IOException;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import java.net.URI;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.time.Duration;
import java.util.List;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertTrue;

/** C13/C14/C26/C27: POST /v1/{sinal} válido grava JSONL + 200; inválido → 400 com causa e arquivo íntegro. */
class SinkOtlpTest {

    private static final HttpClient CLIENT = HttpClient.newHttpClient();

    private static OtlpSinkServer startServer(@TempDir Path tempDir) throws IOException {
        SinkConfig config = SinkConfig.of("127.0.0.1", 0, null, false,
                tempDir.resolve("otlp-sink").toString(), 32L * 1024 * 1024, 5, Duration.ofMinutes(1440));
        OtlpSinkServer server = new OtlpSinkServer(config);
        server.start();
        return server;
    }

    private static HttpResponse<String> post(String url, byte[] body) throws IOException, InterruptedException {
        HttpRequest request = HttpRequest.newBuilder(URI.create(url))
                .header("Content-Type", "application/x-protobuf")
                .POST(HttpRequest.BodyPublishers.ofByteArray(body))
                .build();
        return CLIENT.send(request, HttpResponse.BodyHandlers.ofString(StandardCharsets.UTF_8));
    }

    private static List<String> fileLines(Path dir, String file) throws IOException {
        Path target = dir.resolve("otlp-sink").resolve(file);
        if (!Files.exists(target)) {
            return List.of();
        }
        return Files.readAllLines(target).stream().filter(l -> !l.isBlank()).toList();
    }

    @Test
    void validTracePostAppendsJsonl(@TempDir Path tempDir) throws Exception {
        OtlpSinkServer server = startServer(tempDir);
        try {
            HttpResponse<String> response = post("http://127.0.0.1:" + server.port() + "/v1/traces",
                    TestPayloads.traceProtobuf("checkout-request"));
            assertEquals(200, response.statusCode());
            List<String> lines = fileLines(tempDir, "traces.jsonl");
            assertEquals(1, lines.size());
            assertTrue(lines.get(0).contains("checkout-request"),
                    "linha JSONL deve conter o nome do span (OTLP-JSON)");
        } finally {
            server.close();
        }
    }

    @Test
    void validMetricPostAppendsJsonl(@TempDir Path tempDir) throws Exception {
        OtlpSinkServer server = startServer(tempDir);
        try {
            HttpResponse<String> response = post("http://127.0.0.1:" + server.port() + "/v1/metrics",
                    TestPayloads.metricProtobuf("pedidos.total"));
            assertEquals(200, response.statusCode());
            List<String> lines = fileLines(tempDir, "metrics.jsonl");
            assertEquals(1, lines.size());
            assertTrue(lines.get(0).contains("pedidos.total"));
        } finally {
            server.close();
        }
    }

    @Test
    void validLogPostAppendsJsonl(@TempDir Path tempDir) throws Exception {
        OtlpSinkServer server = startServer(tempDir);
        try {
            HttpResponse<String> response = post("http://127.0.0.1:" + server.port() + "/v1/logs",
                    TestPayloads.logProtobuf("pedido processado"));
            assertEquals(200, response.statusCode());
            List<String> lines = fileLines(tempDir, "logs.jsonl");
            assertEquals(1, lines.size());
            assertTrue(lines.get(0).contains("pedido processado"));
        } finally {
            server.close();
        }
    }

    @Test
    void invalidPayloadReturns400KeepsFileIntact(@TempDir Path tempDir) throws Exception {
        OtlpSinkServer server = startServer(tempDir);
        try {
            HttpResponse<String> bad = post("http://127.0.0.1:" + server.port() + "/v1/traces",
                    new byte[]{1, 2, 3, 4});
            assertEquals(400, bad.statusCode());
            assertTrue(bad.body().contains("payload protobuf inválido"));
            assertTrue(bad.body().contains("cause"),
                    "400 deve informar a causa");

            List<String> before = fileLines(tempDir, "traces.jsonl");
            int countBefore = before.size();

            HttpResponse<String> ok = post("http://127.0.0.1:" + server.port() + "/v1/traces",
                    TestPayloads.traceProtobuf("span-valido"));
            assertEquals(200, ok.statusCode());
            List<String> after = fileLines(tempDir, "traces.jsonl");
            assertEquals(countBefore + 1, after.size(),
                    "payload inválido não deve corromper nem alterar o arquivo existente");
            assertFalse(after.stream().anyMatch(l -> l.contains("\"\"")), "linhas íntegras");
        } finally {
            server.close();
        }
    }
}
