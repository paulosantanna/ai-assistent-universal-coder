package com.aeos.telemetry.devtools;

import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.io.TempDir;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.time.Duration;
import java.time.Instant;
import java.util.List;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertTrue;

/** C15: rotação por teto de tamanho/idade com limite de arquivos; readRecent ordena do mais novo. */
class JsonlStoreTest {

    private static String line(String spanName, long timeNs) {
        return "{\"resourceSpans\":[{\"scopeSpans\":[{\"spans\":[{\"name\":\"" + spanName
                + "\",\"startTimeUnixNano\":\"" + timeNs + "\"}]}]}]}";
    }

    @Test
    void rotationHonorsCeilings(@TempDir Path tempDir) throws IOException {
        MutableClock clock = new MutableClock(Instant.parse("2026-11-11T10:00:00Z"));
        // 512 B de teto, 4 arquivos no total (ativo + 3 rotações); ~150 B/linha →
        // rotação a cada ~4 appends: 20 appends forçam rotação em cascata até traces.3.jsonl.
        JsonlStore store = JsonlStore.create(
                SinkConfig.of("127.0.0.1", 14318, null, false, tempDir.toString(),
                        512, 4, Duration.ofMinutes(1440)),
                "traces", clock);

        for (int i = 1; i <= 25; i++) {
            store.append(line("span-" + i, TestPayloads.TIME_NS + i));
        }

        Path active = tempDir.resolve("traces.jsonl");
        assertTrue(Files.exists(active));
        // rotação profunda aconteceu de fato (senão o teto nunca é testado)
        assertTrue(Files.exists(tempDir.resolve("traces.3.jsonl")),
                "rotação em cascata deve preencher traces.1..3.jsonl");
        // limite: NUNCA existe traces.{maxFiles}.jsonl (teto de arquivos, AD-004)
        assertFalse(Files.exists(tempDir.resolve("traces.4.jsonl")),
                "rotação além do teto de arquivos deve descartar as mais antigas");
        assertTrue(Files.size(active) <= 1024, "arquivo ativo recomeça após rotação");

        // readRecent: mais recente primeiro, com teto
        List<String> recent = store.readRecent(null, 5);
        assertEquals(5, recent.size());
        assertTrue(recent.get(0).contains("span-25"),
                "a linha mais nova vem primeiro");
        assertFalse(recent.get(0).contains("\"span-1\""),
                "a linha mais nova não deve ser a primeira (span-1 antigo)");

        // filtro since (epoch millis) usa a marca temporal embutida
        long afterAll = (TestPayloads.TIME_NS / 1_000_000L) + 1000;
        assertTrue(store.readRecent(afterAll, 10).isEmpty(),
                "since maior que os timestamps não deve retornar nada");
        List<String> sinceZero = store.readRecent(0L, 100);
        int total = sinceZero.size();
        assertTrue(total >= 15 && total < 25,
                "teto de arquivos descarta as linhas mais antigas (retidas=" + total + ")");
    }

    @Test
    void ageCeilingRotates(@TempDir Path tempDir) throws IOException {
        MutableClock clock = new MutableClock(Instant.parse("2026-11-11T10:00:00Z"));
        JsonlStore store = JsonlStore.create(
                SinkConfig.of("127.0.0.1", 14318, null, false, tempDir.toString(),
                        32L * 1024 * 1024, 5, Duration.ofMinutes(30)),
                "traces", clock);

        store.append(line("antes", TestPayloads.TIME_NS));
        clock.advance(Duration.ofMinutes(31));
        store.append(line("depois", TestPayloads.TIME_NS + 1));

        // a linha "antes" foi rotacionada por idade; o ativo tem apenas a nova
        assertEquals(1, store.activeLineCount());
        assertTrue(Files.exists(tempDir.resolve("traces.1.jsonl")),
                "rotação por idade cria traces.1.jsonl");
        assertTrue(Files.readString(tempDir.resolve("traces.1.jsonl")).contains("antes"));

        assertEquals(1_700_000_000_000L, store.lineTimeMs(line("x", TestPayloads.TIME_NS)),
                "conversão ns→ms da marca embutida");
        assertEquals(0, store.lineTimeMs("{\"sem\":\"tempo\"}"),
                "linha sem marca temporal conta como 0");
    }
}
